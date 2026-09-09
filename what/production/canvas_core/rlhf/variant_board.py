"""Variant-selection board — a ComfyUI run manifest -> an interaction-bearing selection canvas.

Canvas's half of `spec_comfyui_canvas_emission` §1.1 (Blueprint P4). One aDNA-Native ``.canvas``
per generation run: each slot becomes a group of ``file`` nodes (one per variant, plus a caption
carrying that variant's provenance) beside a **slot sidecar** whose Meta Bind control captures the
operator's pick. ``review_collect`` fans the result into the same three sinks as the HR pilot.

**How this differs from** ``review_canvas.py``, and why. The HR pilot asks *"what do you make of
this variant?"* — one verdict affordance per variant. A selection board asks *"which of these?"* —
**one choice affordance per slot, options = the slot's variant ids** — because that choice **is**
ComfyUI's SO-5 human gate (spec §5), not a rating of independent images. The two shapes share one
pipeline: ``review_collect.decisions_of`` translates a pick into the variant-keyed decisions the
sinks already consume, so idempotency, Schema-A, the III routing and the S-4 reject gate are
inherited rather than reimplemented.

**Provenance is a floor, not a nicety** (§1.1). Each variant node carries ``workflow · model ·
seed · denoise · lora_refs · source_backend`` in ``component_types[...].qualities``, and a gap is
rendered as an explicit ``<absent>`` — never back-filled from a sibling. The ``SelectionRecord``
this board feeds outlives the board; a variant silently attributed to the wrong model poisons the
corpus quietly.

**Geometry passes by construction, not by luck** (P2c): every node is sized through
``canvas_core.layout_fit``, group boxes through ``fit_group_size``, labels through
``fit_group_label``, leads through ``heading``/``fit_lead``, and image boxes through
``image_probe.node_size`` at the asset's exact aspect. The builder then self-gates on
``validate_suite(ADNA_NATIVE)`` before it writes, exactly as ``review_canvas`` does.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
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
from canvas_core.rlhf.review_canvas import DEFECT_VOCAB, _dump_frontmatter
from canvas_core.rlhf.run_manifest import ABSENT, RunManifest, Variant, load_run_manifest
from canvas_std import ConformanceLevel, validate_suite

_VAULT_ROOT = Path(__file__).resolve().parents[4]

DEFAULT_REGISTER = "comfyui_variants"

# Layout constants. Widths are chosen so the label budget (width/25 for CAPS — CV-GROUP-LABEL-01)
# accommodates a slot label, and the image fit-box keeps a variant cell well above the 20% slot
# fill floor (CV-IMAGE-ASPECT-RATIO-01).
_CELL_W, _IMG_MAX_H = 420, 420
_CAPTION_W = _CELL_W
_SIDECAR_W = 560
#: Slot sidecar node height. Inherited from the HR pilot and **kept deliberately**, after being
#: changed twice and changed back.
#:
#: ⛩ F-P4-4 — a false positive found by sight, and caught by sight. The first agent-confirmed
#: render showed this embed with a scrollbar and its lower controls below the fold; that was
#: written up as a clipping defect of exactly the class P2c removed from six producers (a guessed
#: constant), and "fixed" by deriving the height from ``fit_text_height(body)`` ≈ 1580px. The next
#: render refuted it on three counts:
#:
#: 1. A canvas embed **scrolls** — nothing was unreachable, so there was no defect to fix.
#: 2. ``fit_text_height`` measures **raw markdown**; Meta Bind renders those fences as compact
#:    widgets, so 1580 was never the required height either.
#: 3. The taller node grew the board past the point where zoom-to-fit stays above Obsidian's LOD
#:    threshold, so **every caption on the board** reverted to placeholder bars. A cosmetic
#:    non-problem was traded for a whole-surface legibility one. 900 failed the same way.
#:
#: ⇒ ***the sight gate produces false positives too, and the discipline that catches them is the
#: same one that catches the true ones: render again after the fix and compare.*** Had this been
#: "fixed" and shipped on the strength of one look, the board would have been strictly worse and
#: the record would have called it a repair.
_SIDECAR_H = 520
_GUTTER, _PAD = 60, 48
_SLOT_GAP = 120


def _vault_relative(path: Path, vault_root: Path) -> str:
    """A node's ``file`` value, vault-relative when possible.

    Obsidian and ``canvas-visual-check --vault-root`` both resolve a file node against the vault
    root, **not** against the canvas or the manifest. The manifest's own ``path`` is relative to
    the manifest (that is the seam's contract, §3), so writing it straight into a node produces a
    canvas whose images resolve for the builder's cwd and nowhere else — and, worse, one whose
    file-resolution traps *skip* rather than fail, reporting green for checks that never ran
    (F-P2-11).
    """
    try:
        return str(path.resolve().relative_to(vault_root.resolve()))
    except ValueError:
        return str(path.resolve())


@dataclass(frozen=True)
class BoardPaths:
    canvas: Path
    sidecars: dict[str, Path]        # slot_id -> sidecar path
    readme: Path


# ================================================================================================
# Sidecars — one per SLOT (the pick is a slot-level question)
# ================================================================================================

def _slot_sidecar_frontmatter(
    slot_id: str,
    variants: tuple[Variant, ...],
    *,
    surface: str,
    canvas_rel: str,
    prompt: str,
    vault_root: Path,
) -> dict[str, Any]:
    return {
        "type": "selection_sidecar",
        "review_surface": surface,
        "review_canvas": canvas_rel,
        "slot_id": slot_id,
        "options": [v.variant_id for v in variants],
        # Vault-relative, like the node paths — this is what reaches Schema-A's `variants[]` and
        # outlives the board.
        "option_images": {v.variant_id: _vault_relative(v.path, vault_root) for v in variants},
        "option_models": {v.variant_id: v.model for v in variants},
        "prompt": prompt,
        "reviewer": None,
        "pick": None,
        "rejected": [],
        "rating": None,
        "defect_tags": [],
        "note": "",
        "prompt_edit": "",
        "regenerate_requested": False,
        "pin_requested": False,
        "escalate": False,
        "collected_at": None,
        "selection_id": None,
        "review_turn": None,
    }


def _slot_sidecar_body(slot_id: str, variants: tuple[Variant, ...], prompt: str) -> str:
    """Meta Bind controls — JS-less, and `multiSelect` emitted as a fenced block.

    Inline ``INPUT[multiSelect(...)]`` renders ``[META_BIND_ERROR]`` in Meta Bind 1.4.x; it is
    block-only. Learned by agent-confirmed render on 2026-08-04 and inherited here rather than
    rediscovered.
    """
    pick_options = ", ".join(f"option({v.variant_id})" for v in variants)
    reject_options = ", ".join(f"option({v.variant_id})" for v in variants)
    defect_options = ", ".join(f"option({tag})" for tag in DEFECT_VOCAB)
    roster = "\n".join(
        f"- `{v.variant_id}` — {v.model} · seed `{v.seed}` · denoise `{v.denoise}`"
        + (f" · lora {list(v.lora_refs)}" if v.lora_refs and v.lora_refs is not ABSENT else "")
        for v in variants
    )
    return f"""**{slot_id} — pick one** ({len(variants)} variants)

{prompt or "_no prompt recorded for this slot_"}

{roster}

Pick (required): `INPUT[inlineSelect({pick_options}):pick]`
Rating of the pick (1–5): `INPUT[inlineSelect(option(1), option(2), option(3), option(4), option(5)):rating]`

Explicitly reject variants (optional — not picking is a *skip*, not a reject):

```meta-bind
INPUT[multiSelect({reject_options}):rejected]
```

Defect tags (controlled vocabulary):

```meta-bind
INPUT[multiSelect({defect_options}):defect_tags]
```

Note: `INPUT[textArea:note]`
Prompt edit (whole-string delta): `INPUT[textArea:prompt_edit]`

Pin as reference: `INPUT[toggle:pin_requested]` · Escalate (#needs-human): `INPUT[toggle:escalate]`

```meta-bind-button
label: Request regenerate (intent flag — dispatch deferred)
style: primary
action:
  type: updateMetadata
  bindTarget: regenerate_requested
  evaluate: false
  value: true
```

> Saving this note IS the capture. Nothing dispatches from this surface —
> `review_dispatch_contract v0` ships no dispatcher (`spec_canvas_review_surface` §6).
"""


# ================================================================================================
# The canvas
# ================================================================================================

def _caption(variant: Variant) -> str:
    """A variant's provenance, rendered so a gap reads as a gap.

    Leads with ``####`` (``layout_fit.heading``) because the caption sits at the **top** of its
    variant cell and is that cell's title slot: ``CV-HIERARCHY-01`` wants a heading marker in a
    group's upper 40%, and ``CV-LEAD-COST-01`` forbids ``h1/h2/h3`` — ``####`` is the one lead
    that passes both honestly (F-P2-3/F-P2-6, encoded once in ``layout_fit``).
    """
    lines = [
        heading(variant.variant_id),
        f"model: `{variant.model}`",
        f"workflow: `{variant.workflow}`",
        f"seed: `{variant.seed}` · denoise: `{variant.denoise}`",
        f"backend: `{variant.source_backend}`",
    ]
    if variant.lora_refs is ABSENT:
        lines.append(f"lora: `{ABSENT}`")
    else:
        lines.append(f"lora: `{list(variant.lora_refs) or 'none'}`")
    return "\n\n".join(lines)


def _affordances_for_slot(
    slot_id: str,
    variants: tuple[Variant, ...],
    sidecar_node_id: str,
) -> dict[str, dict[str, Any]]:
    """The slot's declared interaction surface (v2.2.0 grammar, `interaction_version 1.0`)."""
    affordances: dict[str, dict[str, Any]] = {
        f"{slot_id}.pick": {
            "anchor": sidecar_node_id,
            "kind": "choice",
            "options": [v.variant_id for v in variants],
            "prompt": f"Which variant for {slot_id}?",
            "required": True,
        },
        f"{slot_id}.rating": {
            "anchor": sidecar_node_id, "kind": "choice",
            "options": ["1", "2", "3", "4", "5"],
            "prompt": f"Rating of the pick for {slot_id}", "required": False,
        },
        f"{slot_id}.defect": {
            "anchor": sidecar_node_id, "kind": "choice", "options": list(DEFECT_VOCAB),
            "prompt": f"Defect tags for {slot_id} (one response per tag)", "required": False,
        },
        f"{slot_id}.note": {
            "anchor": sidecar_node_id, "kind": "annotation",
            "prompt": f"Free note on {slot_id}", "required": False,
        },
        f"{slot_id}.prompt_edit": {
            "anchor": sidecar_node_id, "kind": "input",
            "prompt": f"Prompt delta for {slot_id}", "required": False,
        },
    }
    for action in ("regenerate", "pin", "escalate"):
        affordances[f"{slot_id}.{action}"] = {
            "anchor": sidecar_node_id, "kind": "action",
            "prompt": f"{action} intent for {slot_id}", "required": False,
        }
    # The reject channel is per-VARIANT and deliberately not part of the pick. Not picking a
    # variant is a skip; rejecting it is a distinct judgement that carries defect tags into the
    # III store through the S-4 gate, and the signal is only derivable when it is attributed to
    # the variant rather than the slot.
    for variant in variants:
        affordances[f"{variant.variant_id}.verdict"] = {
            "anchor": sidecar_node_id, "kind": "choice", "options": ["reject"],
            "prompt": f"Explicitly reject {variant.variant_id}", "required": False,
        }
    return affordances


def build_variant_board(
    manifest_path: str | Path,
    out_dir: str | Path,
    *,
    vault_root: Path = _VAULT_ROOT,
    surface_name: str | None = None,
    register: str = DEFAULT_REGISTER,
    force: bool = False,
) -> BoardPaths:
    """Build the board canvas + slot sidecars + README under ``out_dir``.

    Refuses to overwrite a sidecar that already carries a pick unless ``force`` — the same
    never-destroy-operator-signal guard the HR pilot ships.
    """
    import yaml

    manifest: RunManifest = load_run_manifest(manifest_path)
    surface = surface_name or f"board_{manifest.run_id}"
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    sidecar_dir = out / "sidecars"
    sidecar_dir.mkdir(exist_ok=True)
    canvas_path = out / f"{surface}.canvas"
    try:
        canvas_rel = str(canvas_path.resolve().relative_to(vault_root))
    except ValueError:
        canvas_rel = str(canvas_path)

    # --- sidecars -------------------------------------------------------------------------------
    sidecars: dict[str, Path] = {}
    for slot in manifest.slots:
        path = sidecar_dir / f"{slot.slot_id}.md"
        if path.exists() and not force:
            existing = path.read_text(encoding="utf-8")
            if existing.startswith("---"):
                prior = yaml.safe_load(existing.split("---", 2)[1]) or {}
                if prior.get("pick"):
                    raise FileExistsError(
                        f"{path}: carries a pick ({prior['pick']!r}) — refusing to overwrite "
                        "operator signal (use force=True after collecting)"
                    )
        frontmatter = _slot_sidecar_frontmatter(
            slot.slot_id, slot.variants,
            surface=surface, canvas_rel=canvas_rel, prompt=slot.prompt, vault_root=vault_root,
        )
        body = _slot_sidecar_body(slot.slot_id, slot.variants, slot.prompt)
        path.write_text(_dump_frontmatter(frontmatter) + body, encoding="utf-8")
        sidecars[slot.slot_id] = path

    # --- canvas ---------------------------------------------------------------------------------
    builder = CanvasBuilder(name=surface, version="1.0.0")
    header_text = (
        f"{heading(f'Variant selection — run {manifest.run_id}')}\n\n"
        f"Driver `{manifest.driver}` · {len(manifest.slots)} slot(s) · "
        f"{manifest.variant_count} variant(s). Open each slot's sidecar, set **pick**, save — "
        "then run the collector (README). Not picking a variant is a skip, not a reject."
    )
    if manifest.provenance_gaps:
        header_text += (
            f"\n\n⚠ {len(manifest.provenance_gaps)} variant(s) arrived with an incomplete "
            "provenance floor; the gaps are shown as `<absent>` and were not inferred."
        )
    header_w = 900
    builder.add_text_node(
        "board_header", header_text, x=0, y=-(fit_text_height(header_text, header_w) + 80),
        width=header_w, height=fit_text_height(header_text, header_w),
    )

    component_types: dict[str, dict[str, Any]] = {
        "board_header": {"class": "text", "semantic_type": "instruction", "degrades_to": "text"},
    }
    affordances: dict[str, dict[str, Any]] = {}
    cursor_y = 0

    for slot in manifest.slots:
        cell_ids: list[str] = []
        child_boxes: list[tuple[int, int, int, int]] = []
        x = _PAD
        tallest_cell = 0

        # A slot's title node — its own heading, so CV-HIERARCHY-01's title slot is filled by a
        # real title rather than by whichever child text node happens to sit highest.
        slot_title = heading(slot.label or slot.slot_id)
        title_w = _CELL_W * 2
        title_h = fit_text_height(slot_title, title_w)
        title_id = f"{slot.slot_id}_title"
        builder.add_text_node(title_id, slot_title,
                              x=_PAD, y=cursor_y + _PAD, width=title_w, height=title_h)
        component_types[title_id] = {
            "class": "text", "semantic_type": "title", "degrades_to": "text",
        }
        child_boxes.append((_PAD, cursor_y + _PAD, title_w, title_h))
        cell_top = cursor_y + _PAD + title_h + 32

        for variant in slot.variants:
            img_w, img_h = (
                node_size(variant.width, variant.height, _CELL_W, _IMG_MAX_H)
                if variant.width and variant.height
                else (_CELL_W, _IMG_MAX_H)
            )
            caption = _caption(variant)
            cap_h = fit_text_height(caption, _CAPTION_W)
            img_id = f"{variant.variant_id}_image"
            cap_id = f"{variant.variant_id}_caption"

            # Caption ABOVE the image: it is the cell's title slot, and CV-HIERARCHY-01 measures
            # the group's upper 40%.
            cap_y = cell_top + _PAD
            img_y = cap_y + cap_h + 20
            builder.add_text_node(cap_id, caption,
                                  x=x, y=cap_y, width=_CAPTION_W, height=cap_h)
            builder.add_file_node(img_id, _vault_relative(variant.path, vault_root),
                                  x=x, y=img_y, width=img_w, height=img_h)
            builder.add_edge(f"{variant.variant_id}_edge", cap_id, img_id,
                             from_side="bottom", to_side="top")

            # Each variant is its own CELL GROUP. Not decoration: CV-IMAGE-ASPECT-RATIO-01 measures
            # an image's fill against its **smallest enclosing group**, so N competing variants
            # sharing one slot container each read as ~10% under-fill — a hero-slot model applied
            # to a surface that has no hero by construction. Grouping the cell states the real
            # containment instead of arguing with the trap about it.
            cell_h = cap_h + 20 + img_h
            cell_w, cell_box_h = fit_group_size(_CELL_W, cell_h, MIN_EDGE_PAD)
            builder.add_group(f"{variant.variant_id}_cell", "",
                              x=x - MIN_EDGE_PAD, y=cap_y - MIN_EDGE_PAD,
                              width=cell_w, height=cell_box_h)

            child_boxes.append((x - MIN_EDGE_PAD, cap_y - MIN_EDGE_PAD, cell_w, cell_box_h))
            tallest_cell = max(tallest_cell, cell_box_h)
            cell_ids.append(img_id)

            component_types[img_id] = {
                "class": "image", "semantic_type": "variant", "degrades_to": "file",
                "qualities": {
                    "substrate": "raster", "status": "rendered",
                    "aspect_ratio": (aspect_label(variant.width, variant.height)
                                     if variant.width and variant.height else ABSENT),
                    # The §1.1 provenance floor, carried on the node itself.
                    "model": variant.model,
                    "workflow": variant.workflow,
                    "seed": str(variant.seed),
                    "denoise": str(variant.denoise),
                    "lora_refs": (ABSENT if variant.lora_refs is ABSENT
                                  else list(variant.lora_refs)),
                    "source_backend": variant.source_backend,
                },
            }
            component_types[cap_id] = {
                "class": "text", "semantic_type": "provenance", "degrades_to": "text",
            }
            x += _CELL_W + _GUTTER

        sidecar_id = f"{slot.slot_id}_sidecar"
        sidecar_rel = str(sidecars[slot.slot_id].resolve())
        try:
            sidecar_rel = str(sidecars[slot.slot_id].resolve().relative_to(vault_root))
        except ValueError:
            pass
        sidecar_h = _SIDECAR_H
        builder.add_file_node(sidecar_id, sidecar_rel,
                              x=x, y=cell_top + _PAD, width=_SIDECAR_W, height=sidecar_h)
        child_boxes.append((x, cell_top + _PAD, _SIDECAR_W, sidecar_h))
        component_types[sidecar_id] = {
            "class": "embed", "semantic_type": "selection_sidecar", "degrades_to": "file",
        }
        for cell_id in cell_ids:
            builder.add_edge(f"{cell_id}_to_sidecar", cell_id, sidecar_id,
                             from_side="right", to_side="left")

        left = min(box[0] for box in child_boxes)
        top = min(box[1] for box in child_boxes)
        bbox_w = max(box[0] + box[2] for box in child_boxes) - left
        bbox_h = max(box[1] + box[3] for box in child_boxes) - top
        group_w, group_h = fit_group_size(bbox_w, bbox_h, _PAD)

        label = f"{slot.slot_id.upper()}"
        if slot.label:
            label = f"{label} · {slot.label.upper()}"
        _, needed = fit_group_label(label, group_w)
        group_w = max(group_w, needed)

        builder.add_group(f"{slot.slot_id}_group", label,
                          x=left - _PAD, y=top - _PAD, width=group_w, height=group_h)
        affordances.update(_affordances_for_slot(slot.slot_id, slot.variants, sidecar_id))
        cursor_y = top - _PAD + group_h + _SLOT_GAP

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
            "state": {
                "turn": "t1",
                "open": [f"{slot.slot_id}.pick" for slot in manifest.slots],
            },
        },
    })
    doc = builder.build()

    report = validate_suite(doc, ConformanceLevel.ADNA_NATIVE)
    if report.level_reached is not ConformanceLevel.ADNA_NATIVE:
        raise ValueError(
            "variant board failed its own gate (adna_native): "
            + "; ".join(f["msg"] for f in report.failed)
        )
    canvas_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    readme = out / "README.md"
    readme.write_text(
        f"""# Variant-selection board — `{surface}`

Run `{manifest.run_id}` (driver `{manifest.driver}`), {len(manifest.slots)} slot(s),
{manifest.variant_count} variant(s). Spec: `what/specs/spec_comfyui_canvas_emission.md` §1.1.

## Review

1. Open `{surface}.canvas` in Obsidian (Advanced Canvas + Meta Bind ≥1.4).
2. In each slot's sidecar set **pick** (required); optionally rating / rejected / defect tags /
   note / prompt edit. Saving the note IS the capture.

**Not picking a variant is a skip, not a reject.** Use `rejected` to say a variant was actively
bad — that is the judgement that carries defect tags into the III store.

## Collect

```bash
cd what/production
python -m canvas_core.rlhf.review_collect {canvas_path.name} --approver <you> --register {register}
```

Same collector as the HR pilot: canvas -> Schema-A -> III -> ledger, layered idempotency,
`--dry-run` writes nothing. Agent plumbing runs MUST pass `--participant-kind ai`.

{"⚠ Provenance gaps in this run: " + json.dumps(manifest.provenance_gaps) if manifest.provenance_gaps else ""}
{"⚠ Skipped by the loader: " + "; ".join(manifest.skipped) if manifest.skipped else ""}
""",
        encoding="utf-8",
    )
    return BoardPaths(canvas=canvas_path, sidecars=sidecars, readme=readme)


def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python -m canvas_core.rlhf.variant_board",
        description="Build a variant-selection board from a run manifest (spec §1.1/§3).",
    )
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--surface-name", default=None)
    ap.add_argument("--register", default=DEFAULT_REGISTER)
    ap.add_argument("--force", action="store_true",
                    help="overwrite sidecars even if they carry a pick (destroys operator signal!)")
    args = ap.parse_args(argv)
    paths = build_variant_board(args.manifest, args.out, surface_name=args.surface_name,
                                register=args.register, force=args.force)
    print(f"board: {paths.canvas}")
    print(f"sidecars: {len(paths.sidecars)} under {paths.canvas.parent / 'sidecars'}")
    print(f"README: {paths.readme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
