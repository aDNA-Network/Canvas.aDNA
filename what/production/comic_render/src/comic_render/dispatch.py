"""Stages 2+3 — dispatch (generate) + refine: execute each panel's ``render_chain``.

The chain is first-class: ``generate`` fans out ``variant_count`` variants per panel through the
existing ``ImagenWiring`` (path convention ``runs/<comic_id>/<panel>_v{n}.png``); each ``refine``
stage feeds the prior stage's outputs through a ``RefineClient`` (fake now; Vulcan's
``comic_panel_refine`` at H4), passing the manifest's separate ``negative`` channel out-of-band —
the generate protocol carries text only.

Idempotent at panel granularity (roadmap): a panel whose planned outputs all exist on disk is
skipped. ``budget_cap`` is enforced BEFORE any call (R9): projected spend over the cap raises.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from canvas_core.image_generation import ImagenWiring, ImagePrompt

from comic_render.backends import make_generate_client, make_refine_client
from comic_render.manifest import PanelSpec, RenderManifest


class BudgetCapExceededError(RuntimeError):
    """Projected spend would exceed ``manifest.budget_cap`` — nothing was dispatched."""


def _rel(path: Path, base: Path) -> str:
    return str(path.relative_to(base)) if path.is_absolute() else str(path)


def _record_spend(manifest: RenderManifest, calls: int, usd: float) -> None:
    spend = manifest.spend or {"usd": 0.0, "calls": 0}
    spend["usd"] = round(spend.get("usd", 0.0) + usd, 6)
    spend["calls"] = spend.get("calls", 0) + calls
    manifest.spend = spend


def _enforce_budget(manifest: RenderManifest, planned_calls: int, cost_per_call: float) -> None:
    if manifest.budget_cap is None:
        return
    projected = manifest.spend.get("usd", 0.0) + planned_calls * cost_per_call
    if projected > manifest.budget_cap:
        raise BudgetCapExceededError(
            f"projected spend ${projected:.2f} ({planned_calls} calls at ${cost_per_call:.2f}) "
            f"exceeds budget_cap ${manifest.budget_cap:.2f} — nothing dispatched"
        )


def _chain_stages(panel: PanelSpec, stage_kind: str):
    return [s for s in panel.render_chain if s.stage == stage_kind]


def _lora_for(panel: PanelSpec) -> dict[str, Any] | None:
    """The panel's pair-gated LoRA entry, if any (H4 — the refine-stage LoRA slot).

    ``characters[]`` (H5) emits ``trigger_word`` and ``lora_ref`` together or not at all, so the
    first entry carrying a ``lora_ref`` is a trained, safe-to-condition pair. Backends that cannot
    condition on a LoRA ignore it; the roadmap's R3 mitigation is exactly this — "LoRA re-enters
    via the refine chain when trained".
    """
    for character in panel.characters:
        if isinstance(character, dict) and character.get("lora_ref"):
            return character
    return None


def run_generate(
    manifest: RenderManifest,
    manifest_path: str | Path,
    *,
    client_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute every panel's ``generate`` stage. Saves the manifest after each panel (resumable)."""
    manifest_path = Path(manifest_path)
    base = manifest_path.parent
    wiring = ImagenWiring()
    clients: dict[str, Any] = dict(client_overrides or {})
    summary: dict[str, Any] = {"generated": [], "skipped": [], "calls": 0}

    todo: list[tuple[PanelSpec, Any, list[Path]]] = []
    for panel in manifest.dispatchable():
        stages = _chain_stages(panel, "generate")
        if not stages:
            continue
        backend = stages[0].backend
        if backend not in clients:
            clients[backend] = make_generate_client(backend)
        planned = wiring.prepare_variant_paths(base / panel.output_dir, panel.panel_id,
                                               panel.variant_count)
        if all(p.exists() for p in planned):
            panel.results.setdefault("variants", [_rel(p, base) for p in planned])
            panel.results.setdefault("model", getattr(clients[backend], "model_name", backend))
            summary["skipped"].append(panel.panel_id)
            continue
        todo.append((panel, clients[backend], planned))

    if todo:
        cost = max(getattr(c, "cost_per_image", 0.0) for _, c, _ in todo)
        _enforce_budget(manifest, sum(len(p) for _, _, p in todo), cost)

    for panel, client, planned in todo:
        prompt = ImagePrompt(
            text=panel.prompt_text,
            mermaid_layout=panel.spatial_layout,
            compositional_intent=panel.compositional_intent,
            aspect_ratio=panel.aspect_ratio,
        )
        saved = wiring.generate_variants(
            client=client,
            prompt=prompt,
            aspect_ratio=panel.aspect_ratio,
            target_dir=base / panel.output_dir,
            item_id=panel.panel_id,
            count=panel.variant_count,
        )
        cost_per = getattr(client, "cost_per_image", 0.0)
        panel.results["variants"] = [_rel(Path(s), base) for s in saved]
        panel.results["model"] = getattr(client, "model_name", "unknown")
        panel.results["cost_per_image"] = cost_per
        _record_spend(manifest, len(saved), len(saved) * cost_per)
        summary["generated"].append(panel.panel_id)
        summary["calls"] += len(saved)
        manifest.save(manifest_path)

    manifest.save(manifest_path)
    return summary


def run_refine(
    manifest: RenderManifest,
    manifest_path: str | Path,
    *,
    client_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Execute every panel's ``refine`` stage(s) over the generate outputs (optional, chained)."""
    manifest_path = Path(manifest_path)
    base = manifest_path.parent
    clients: dict[str, Any] = dict(client_overrides or {})
    summary: dict[str, Any] = {"refined": [], "skipped": [], "no_refine_stage": [], "calls": 0}

    for panel in manifest.dispatchable():
        stages = _chain_stages(panel, "refine")
        if not stages:
            summary["no_refine_stage"].append(panel.panel_id)
            continue
        current = [base / v for v in (panel.results.get("variants") or [])]
        if not current:
            raise RuntimeError(f"refine before generate for panel {panel.panel_id!r} — run dispatch first")

        for stage_idx, stage in enumerate(stages):
            last = stage_idx == len(stages) - 1
            out_dir = base / panel.output_dir / ("refined" if last else f"refined_s{stage_idx}")
            planned = [out_dir / f"{panel.panel_id}_v{i + 1}.png" for i in range(len(current))]
            if all(p.exists() for p in planned):
                current = planned
                if last:
                    panel.results.setdefault("refined", [_rel(p, base) for p in planned])
                    summary["skipped"].append(panel.panel_id)
                continue

            if stage.backend not in clients:
                clients[stage.backend] = make_refine_client(stage.backend)
            client = clients[stage.backend]
            cost_per = getattr(client, "cost_per_image", 0.0)
            _enforce_budget(manifest, len(planned), cost_per)

            out_dir.mkdir(parents=True, exist_ok=True)
            lora = _lora_for(panel)
            produced: list[Path] = []
            for seed_path, out_path in zip(current, planned):
                seed_image = str(base / stage.seed_image) if stage.seed_image else str(seed_path)
                result = client.refine_image(
                    seed_image=seed_image,
                    prompt=panel.prompt_text,
                    output_path=str(out_path),
                    negative=panel.negative,
                    denoise=stage.denoise if stage.denoise is not None else 0.4,
                    workflow=stage.workflow,
                    lora=lora,
                )
                if not result.get("success"):
                    raise RuntimeError(
                        f"refine failed for {panel.panel_id} ({out_path.name}): "
                        f"{result.get('error', 'unknown error')}"
                    )
                produced.append(Path(result.get("image_path", str(out_path))))
            _record_spend(manifest, len(produced), len(produced) * cost_per)
            summary["calls"] += len(produced)
            current = produced
            if last:
                panel.results["refined"] = [_rel(p, base) for p in produced]
                panel.results["model"] = getattr(client, "model_name", stage.backend)
                if panel.panel_id not in summary["refined"]:
                    summary["refined"].append(panel.panel_id)
            manifest.save(manifest_path)

    manifest.save(manifest_path)
    return summary
