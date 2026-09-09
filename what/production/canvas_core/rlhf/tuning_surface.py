"""Tuning surface — the canvas as the knob panel (`spec_comfyui_canvas_emission` §1.2).

A canvas over one variant (or a small set) whose interaction overlay carries **``input``**
affordances bound to re-render parameters — ``denoise`` · ``steps`` · ``cfg`` · prompt delta ·
optional ``lora_strength`` — plus exactly one **``action``** affordance, ``re_render``.

⛔ **The action produces a record, not an execution.** ``review_dispatch_contract v0``
(`spec_canvas_review_surface` §6, "Still out of scope at v0") ships **no dispatcher, no HTTP
client, no render call and no transport**, and this module adds none. Collecting a tuning surface
writes a *request record* — a JSON file that a driver may later read, or may never read. The
canvas never speaks to ``:8188``; the human never edits workflow JSON.

The record satisfies the contract's six clauses where they apply to its shape:

**D1 derivable intent** — every field comes from collected state (the surface, the variant, the
prompt, the operator's deltas, who asked and when). Nothing is fetched, inferred, or defaulted
from ambient context; a parameter the operator did not set is **absent from the record**, not
silently filled with the run's original value. A dispatcher that wants the original reads the
manifest.
**D2 same contract** — the record names the parent variant's ``workflow`` and ``model`` so a
re-roll runs under the generation contract it descends from rather than becoming a new brief.
**D3 new node linked to parent** — ``parent_variant_id`` is mandatory; nothing here overwrites.
**D4 operator spend gate** — not this module's to enforce, and deliberately not claimed: a
request record is *pre*-spend by construction, which is why writing one is safe and dispatching
one is not.
**D5 refusal atomicity** — a refused request leaves **zero trace**: validation runs before any
file is opened, so a refusal is byte- and file-count-invariant. Asserted by test.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from canvas_core.core import CanvasBuilder
from canvas_core.layout_fit import (
    MIN_EDGE_PAD,
    fit_group_label,
    fit_group_size,
    fit_text_height,
    heading,
)
from canvas_core.rlhf.image_probe import aspect_label, node_size
from canvas_core.rlhf.review_canvas import _dump_frontmatter
from canvas_core.rlhf.run_manifest import ABSENT, Variant, load_run_manifest
from canvas_core.rlhf.variant_board import _vault_relative
from canvas_std import ConformanceLevel, validate_suite

_VAULT_ROOT = Path(__file__).resolve().parents[4]

#: The re-render knobs a tuning surface exposes, with the affordance kind each takes.
TUNING_PARAMS: tuple[str, ...] = ("denoise", "steps", "cfg", "prompt_delta", "lora_strength")

#: Request records land here by default — the data plane, gitignored + canonical on-node
#: (`adr_010`). A request is an artifact of a review, not a tracked source document.
DEFAULT_REQUEST_DIR = _VAULT_ROOT / "what/artifacts/rerender_requests"

_PANEL_W, _IMG_MAX_H = 520, 520
_PAD = 48


class RequestRefused(ValueError):
    """A re-render request that does not satisfy the contract. Nothing is written when raised."""


@dataclass(frozen=True)
class RerenderRequest:
    """A D1-derivable re-render intent. A record — never an execution."""

    request_id: str
    surface: str
    slot_id: str
    parent_variant_id: str
    workflow: str
    model: str
    prompt: str
    requested_by: str
    at: str
    params: dict[str, Any] = field(default_factory=dict)
    prompt_delta: str = ""
    defect_tags: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "contract": "review_dispatch_contract v0",
            "status": "requested",          # never "dispatched" — this module cannot dispatch
            "surface": self.surface,
            "slot_id": self.slot_id,
            "parent_variant_id": self.parent_variant_id,
            "workflow": self.workflow,
            "model": self.model,
            "prompt": self.prompt,
            "prompt_delta": self.prompt_delta,
            "defect_tags": list(self.defect_tags),
            "params": dict(self.params),
            "requested_by": self.requested_by,
            "at": self.at,
        }


def build_request(
    fm: dict[str, Any],
    *,
    requested_by: str,
    at: str,
) -> RerenderRequest:
    """Derive a re-render request from one tuning sidecar's collected frontmatter (**D1**).

    Raises :class:`RequestRefused` *before touching the filesystem* when the intent is not
    derivable — no parent variant, no workflow to re-run under, or no change asked for. The last
    of those is the one worth stating: a request that changes nothing is a re-roll nobody asked
    for, and spending on it is the failure mode D4 exists to prevent.
    """
    parent = str(fm.get("parent_variant_id") or "").strip()
    if not parent:
        raise RequestRefused("no parent_variant_id — a re-render is a re-roll of something (D3)")
    workflow = str(fm.get("workflow") or "").strip()
    if not workflow or workflow == ABSENT:
        raise RequestRefused(
            f"{parent}: no workflow recorded — a re-render must run under the same generation "
            "contract as its parent (D2), and that contract is unknown"
        )

    params = {
        name: fm[name] for name in TUNING_PARAMS
        if name != "prompt_delta" and fm.get(name) not in (None, "", [])
    }
    prompt_delta = str(fm.get("prompt_delta") or "").strip()
    if not params and not prompt_delta:
        raise RequestRefused(
            f"{parent}: no parameter changed and no prompt delta — nothing to re-render"
        )

    slot_id = str(fm.get("slot_id") or "")
    request_id = f"rr_{slot_id or 'slot'}_{parent}_{at[:19].replace(':', '').replace('-', '')}"
    return RerenderRequest(
        request_id=request_id,
        surface=str(fm.get("review_surface") or ""),
        slot_id=slot_id,
        parent_variant_id=parent,
        workflow=workflow,
        model=str(fm.get("model") or ABSENT),
        prompt=str(fm.get("prompt") or ""),
        requested_by=requested_by,
        at=at,
        params=params,
        prompt_delta=prompt_delta,
        defect_tags=tuple(str(tag) for tag in (fm.get("defect_tags") or [])),
    )


def write_request(
    request: RerenderRequest,
    *,
    request_dir: Path = DEFAULT_REQUEST_DIR,
    dry_run: bool = False,
) -> Path:
    """Persist a request record. Idempotent on ``request_id``; writes nothing on ``dry_run``."""
    target = Path(request_dir) / f"{request.request_id}.json"
    if dry_run or target.exists():
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(request.to_dict(), indent=2) + "\n", encoding="utf-8")
    return target


def collect_requests(
    sidecar_dir: str | Path,
    *,
    requested_by: str,
    at: str,
    request_dir: Path = DEFAULT_REQUEST_DIR,
    dry_run: bool = False,
) -> tuple[list[Path], list[str]]:
    """Turn every tuning sidecar that asked for a re-render into a request record.

    Returns ``(written, refused)``. **D5**: every sidecar is validated first and the batch writes
    nothing if any single one refuses — a refusal is file-count-invariant across the run, not
    "invariant except for the ones that got in before the bad one".
    """
    import yaml

    directory = Path(sidecar_dir)
    pending: list[RerenderRequest] = []
    refused: list[str] = []

    for path in sorted(directory.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        if not raw.startswith("---"):
            continue
        fm = yaml.safe_load(raw.split("---", 2)[1]) or {}
        if fm.get("type") != "tuning_sidecar" or not fm.get("re_render_requested"):
            continue
        try:
            pending.append(build_request(fm, requested_by=requested_by, at=at))
        except RequestRefused as exc:
            refused.append(f"{path.name}: {exc}")

    if refused:
        return [], refused
    return [write_request(r, request_dir=request_dir, dry_run=dry_run) for r in pending], []


# ================================================================================================
# The surface
# ================================================================================================

def _tuning_sidecar_frontmatter(
    variant: Variant,
    *,
    slot_id: str,
    surface: str,
    canvas_rel: str,
    prompt: str,
) -> dict[str, Any]:
    return {
        "type": "tuning_sidecar",
        "review_surface": surface,
        "review_canvas": canvas_rel,
        "slot_id": slot_id,
        "parent_variant_id": variant.variant_id,
        "workflow": variant.workflow,
        "model": variant.model,
        "prompt": prompt or variant.prompt,
        # Seeded EMPTY, never with the parent's values: a knob the operator did not move must be
        # absent from the request, not asserted at its old value (D1).
        "denoise": None,
        "steps": None,
        "cfg": None,
        "prompt_delta": "",
        "lora_strength": None,
        "defect_tags": [],
        "note": "",
        "re_render_requested": False,
        "requested_at": None,
        "request_id": None,
    }


def _tuning_sidecar_body(variant: Variant, slot_id: str) -> str:
    return f"""**Tune {variant.variant_id}** (slot `{slot_id}`)

Parent: `{variant.variant_id}` · model `{variant.model}` · workflow `{variant.workflow}`
· seed `{variant.seed}` · denoise `{variant.denoise}`

Leave a knob blank to keep the parent's value — a blank is *"unchanged"*, and it is left out of
the request rather than restated.

denoise: `INPUT[number:denoise]`
steps: `INPUT[number:steps]`
cfg: `INPUT[number:cfg]`
lora_strength: `INPUT[number:lora_strength]`

Prompt delta: `INPUT[textArea:prompt_delta]`
Note: `INPUT[textArea:note]`

```meta-bind-button
label: Request re-render (writes a request record — nothing dispatches)
style: primary
action:
  type: updateMetadata
  bindTarget: re_render_requested
  evaluate: false
  value: true
```

> This surface has no dispatcher behind it. Pressing the button marks an intent; running the
> collector turns it into a request record on disk. Whether anything renders is a separate,
> operator-gated decision (`review_dispatch_contract v0` D4).
"""


@dataclass(frozen=True)
class TuningPaths:
    canvas: Path
    sidecars: dict[str, Path]
    readme: Path


def build_tuning_surface(
    manifest_path: str | Path,
    out_dir: str | Path,
    *,
    variant_ids: tuple[str, ...] | None = None,
    vault_root: Path = _VAULT_ROOT,
    surface_name: str | None = None,
    force: bool = False,
) -> TuningPaths:
    """Build a tuning canvas over selected variants of a run (all of them when unfiltered)."""
    import yaml

    manifest = load_run_manifest(manifest_path)
    surface = surface_name or f"tuning_{manifest.run_id}"
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    sidecar_dir = out / "sidecars"
    sidecar_dir.mkdir(exist_ok=True)
    canvas_path = out / f"{surface}.canvas"
    try:
        canvas_rel = str(canvas_path.resolve().relative_to(vault_root.resolve()))
    except ValueError:
        canvas_rel = str(canvas_path)

    targets: list[tuple[str, Variant, str]] = [
        (slot.slot_id, variant, slot.prompt)
        for slot in manifest.slots for variant in slot.variants
        if variant_ids is None or variant.variant_id in variant_ids
    ]
    if not targets:
        raise ValueError(f"{manifest_path}: no variants matched {variant_ids!r}")

    sidecars: dict[str, Path] = {}
    for slot_id, variant, prompt in targets:
        path = sidecar_dir / f"{variant.variant_id}.md"
        if path.exists() and not force:
            existing = path.read_text(encoding="utf-8")
            if existing.startswith("---"):
                prior = yaml.safe_load(existing.split("---", 2)[1]) or {}
                if prior.get("re_render_requested"):
                    raise FileExistsError(
                        f"{path}: carries a re-render request — refusing to overwrite operator "
                        "signal (use force=True after collecting)"
                    )
        path.write_text(
            _dump_frontmatter(_tuning_sidecar_frontmatter(
                variant, slot_id=slot_id, surface=surface,
                canvas_rel=canvas_rel, prompt=prompt))
            + _tuning_sidecar_body(variant, slot_id),
            encoding="utf-8",
        )
        sidecars[variant.variant_id] = path

    builder = CanvasBuilder(name=surface, version="1.0.0")
    header = (
        f"{heading(f'Tuning — run {manifest.run_id}')}\n\n"
        f"{len(targets)} variant(s). Set the knobs you want changed, press **Request re-render**, "
        "save, then run the collector. Nothing dispatches from this surface."
    )
    header_w = 900
    header_h = fit_text_height(header, header_w)
    builder.add_text_node("tuning_header", header, x=0, y=-(header_h + 80),
                          width=header_w, height=header_h)

    component_types: dict[str, dict[str, Any]] = {
        "tuning_header": {"class": "text", "semantic_type": "instruction", "degrades_to": "text"},
    }
    affordances: dict[str, dict[str, Any]] = {}
    cursor_y = 0

    for slot_id, variant, _prompt in targets:
        img_w, img_h = (
            node_size(variant.width, variant.height, _PANEL_W, _IMG_MAX_H)
            if variant.width and variant.height else (_PANEL_W, _IMG_MAX_H)
        )
        title = heading(f"{variant.variant_id} — parent")
        title_h = fit_text_height(title, _PANEL_W)
        title_id = f"{variant.variant_id}_title"
        img_id = f"{variant.variant_id}_parent"
        knob_id = f"{variant.variant_id}_knobs"

        top = cursor_y + _PAD
        builder.add_text_node(title_id, title, x=_PAD, y=top, width=_PANEL_W, height=title_h)
        builder.add_file_node(img_id, _vault_relative(variant.path, vault_root),
                              x=_PAD, y=top + title_h + 20, width=img_w, height=img_h)
        builder.add_file_node(
            knob_id, _vault_relative(sidecars[variant.variant_id], vault_root),
            x=_PAD + _PANEL_W + 60, y=top, width=560, height=560,
        )
        builder.add_edge(f"{variant.variant_id}_tune_edge", img_id, knob_id,
                         from_side="right", to_side="left")

        component_types[title_id] = {
            "class": "text", "semantic_type": "title", "degrades_to": "text"}
        component_types[img_id] = {
            "class": "image", "semantic_type": "parent_variant", "degrades_to": "file",
            "qualities": {
                "substrate": "raster", "status": "rendered",
                "aspect_ratio": (aspect_label(variant.width, variant.height)
                                 if variant.width and variant.height else ABSENT),
                "model": variant.model, "workflow": variant.workflow,
                "seed": str(variant.seed), "denoise": str(variant.denoise),
                "source_backend": variant.source_backend,
            },
        }
        component_types[knob_id] = {
            "class": "embed", "semantic_type": "tuning_sidecar", "degrades_to": "file"}

        for param in TUNING_PARAMS:
            affordances[f"{variant.variant_id}.{param}"] = {
                "anchor": knob_id, "kind": "input",
                "prompt": f"{param} for a re-render of {variant.variant_id}", "required": False,
            }
        # Exactly one action affordance, and its response is a REQUEST — see the module docstring.
        affordances[f"{variant.variant_id}.re_render"] = {
            "anchor": knob_id, "kind": "action",
            "prompt": f"Request a re-render of {variant.variant_id} (records intent; dispatches nothing)",
            "required": False,
        }

        content_h = max(title_h + 20 + img_h, 560)
        group_w, group_h = fit_group_size(_PANEL_W + 60 + 560, content_h, _PAD)
        label = f"{variant.variant_id.upper()} · TUNE"
        _, needed = fit_group_label(label, group_w)
        builder.add_group(f"{variant.variant_id}_tune_group", label,
                          x=_PAD - MIN_EDGE_PAD, y=top - MIN_EDGE_PAD,
                          width=max(group_w, needed), height=group_h)
        cursor_y = top - MIN_EDGE_PAD + group_h + 100

    builder._reserved.update({
        "adna_version": "2.0.0",
        "conformance_level": "adna_native",
        "authority": "generator",
        "sync": {"sync_hash": builder.compute_sync_hash()},
        "component_types": component_types,
        "interaction": {
            "interaction_version": "1.0",
            "affordances": affordances,
            "responses": [],
            "state": {"turn": "t1", "open": []},
        },
    })
    doc = builder.build()
    report = validate_suite(doc, ConformanceLevel.ADNA_NATIVE)
    if report.level_reached is not ConformanceLevel.ADNA_NATIVE:
        raise ValueError(
            "tuning surface failed its own gate (adna_native): "
            + "; ".join(f["msg"] for f in report.failed)
        )
    canvas_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    readme = out / "README.md"
    readme.write_text(
        f"""# Tuning surface — `{surface}`

Run `{manifest.run_id}`, {len(targets)} variant(s). Spec: `spec_comfyui_canvas_emission` §1.2.

Set knobs, press **Request re-render**, save, then:

```bash
cd what/production
python -m canvas_core.rlhf.tuning_surface --collect {sidecar_dir.name} --requested-by <you>
```

**Nothing dispatches.** The collector writes request records under
`what/artifacts/rerender_requests/`. Whether any of them is ever run is a separate,
operator-gated decision — `review_dispatch_contract v0` ships no dispatcher (D4).
""",
        encoding="utf-8",
    )
    return TuningPaths(canvas=canvas_path, sidecars=sidecars, readme=readme)


def _main(argv: list[str] | None = None) -> int:
    from datetime import datetime, timezone

    ap = argparse.ArgumentParser(
        prog="python -m canvas_core.rlhf.tuning_surface",
        description="Build a tuning surface, or collect its re-render requests (records only).",
    )
    ap.add_argument("--manifest", type=Path, help="build mode: the run manifest")
    ap.add_argument("--out", type=Path, help="build mode: output directory")
    ap.add_argument("--variants", nargs="*", default=None, help="build mode: restrict to these ids")
    ap.add_argument("--collect", type=Path, help="collect mode: a tuning sidecars/ directory")
    ap.add_argument("--requested-by", default=None, help="collect mode: who is asking")
    ap.add_argument("--request-dir", type=Path, default=DEFAULT_REQUEST_DIR)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    if args.collect:
        if not args.requested_by:
            ap.error("--collect requires --requested-by (a request names who asked; D1)")
        written, refused = collect_requests(
            args.collect, requested_by=args.requested_by,
            at=datetime.now(timezone.utc).isoformat(),
            request_dir=args.request_dir, dry_run=args.dry_run,
        )
        for reason in refused:
            print(f"REFUSED {reason}")
        for path in written:
            print(f"request: {path}")
        print(f"{len(written)} request(s), {len(refused)} refused — nothing dispatched")
        return 1 if refused else 0

    if not args.manifest or not args.out:
        ap.error("build mode requires --manifest and --out")
    paths = build_tuning_surface(
        args.manifest, args.out,
        variant_ids=tuple(args.variants) if args.variants else None,
    )
    print(f"tuning surface: {paths.canvas}")
    print(f"sidecars: {len(paths.sidecars)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
