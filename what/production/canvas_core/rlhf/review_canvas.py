"""HR review-surface builder — a variant manifest -> an interaction-bearing review canvas + Meta Bind sidecars.

Builds the operator RLHF review surface specified by ``what/specs/spec_canvas_review_surface.md`` (Halftone HR):
one aDNA-Native ``.canvas`` where each image variant is a ``file`` node paired with a **sidecar note** ``file``
node whose frontmatter carries the verdict controls (Meta Bind INPUT fields + an ``updateMetadata`` button —
JS-less; ``enableJs: false`` preserved). The canvas declares the affordances additively under
``_reserved.interaction`` (``interaction_version: 1.0``); ``review_collect.py`` fans collected verdicts into the
three sinks. This module is a **substrate capability of** ``canvas_core.rlhf`` — not a producer package: it
composes ``CanvasBuilder`` + the trap-derived authoring rules (``what/docs/canvas_authoring_guidance.md``) and is
reusable by producers later.

Geometry doctrine (visual gate, spec_federation_contract §4 Amendment 1): integer coords; image nodes at the
image's EXACT reduced aspect (CV-IMAGE-ASPECT-RATIO-01); ``**bold**`` leads, never ``#`` (CV-LEAD-COST-01); group
labels within the width/25 CAPS budget (CV-GROUP-LABEL-01); unlabeled edges (CV-EDGE-LABEL-01); sidecar
frontmatter requires ``propertiesInDocument: "hidden"`` for a clean CV-FILE-PROPS-01 (operator-consented).

Input manifest reality (``variations.manifest.json``): a partially-failed run record — some variants carry no
``output_path`` (generation errored, the file landed later) and one records ``success: false`` for a file that
exists. The builder therefore derives each variant's path (``output_path`` else the ``anchor_var_{id}_{label}``
pattern) and includes a variant **iff the image file exists on disk**.
"""

from __future__ import annotations

import argparse
import json
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# Bootstrap the canvas_core import surface when invoked as `python -m canvas_core.rlhf.review_canvas` from
# `what/production/` (the shelf convention — mirrors iii_bridge/_main usage; canvas_core is unpackaged).
from canvas_core.core import CanvasBuilder  # noqa: E402
from canvas_std import ConformanceLevel, validate_suite  # noqa: E402

_VAULT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_MANIFEST = (
    _VAULT_ROOT / "what/artifacts/style_registry/ss_character/canonical/variations.manifest.json"
)
DEFAULT_OUT_DIR = _VAULT_ROOT / "what/artifacts/review_surface_pilot"
DEFAULT_SURFACE_NAME = "ss_variant_review"
DEFAULT_REGISTER = "ss_character"

# The controlled defect vocabulary (Bearly spec_bearly_rlhf_canvas §3, adopted normatively by
# spec_canvas_review_surface §2) — options of the `defect` choice affordance.
DEFECT_VOCAB: tuple[str, ...] = (
    "off-model", "wrong-palette", "line-quality", "expression", "composition",
    "text-error", "tone", "safety", "provenance-gap", "slop",
)
VERDICT_OPTIONS: tuple[str, ...] = ("approve", "reject", "skip")
RATING_OPTIONS: tuple[str, ...] = ("1", "2", "3", "4", "5")

# Layout constants (ints; trap-derived — see module docstring). The numbers clear the measured gates:
# content bbox spans (sidecar_right − image_left) = 1280/1440 = 88.9% < CV-GROUP-PADDING-01's 90%; the image
# fit-box (640×460) keeps every variant's slot area ≥ 20% of the 1440×540 group (CV-IMAGE-ASPECT-RATIO-01).
_GROUP_W, _GROUP_H, _GUTTER = 1440, 540, 80
_PAD_X, _PAD_Y = 80, 40
_SIDECAR_W, _SIDECAR_H = 600, 460
_IMG_MAX_W, _IMG_MAX_H = 640, 460
_COLS = 2


@dataclass(frozen=True)
class VariantEntry:
    """One reviewable variant (manifest row + on-disk reality)."""

    variant_id: str          # "var_1"
    label: str
    axis: str
    image_vault_path: str    # vault-relative (F-36-clean)
    prompt: str
    model: str
    width: int
    height: int


def _png_dimensions(path: Path) -> tuple[int, int]:
    """Read PNG IHDR width/height (pure Python — no PIL on this shelf outside canvas_core.print)."""
    with path.open("rb") as fh:
        header = fh.read(26)
    if len(header) < 26 or header[:8] != b"\x89PNG\r\n\x1a\n" or header[12:16] != b"IHDR":
        raise ValueError(f"{path}: not a PNG (cannot size the review node)")
    width, height = struct.unpack(">II", header[16:24])
    return int(width), int(height)


def _reduced_aspect(width: int, height: int) -> tuple[int, int]:
    from math import gcd

    g = gcd(width, height) or 1
    return width // g, height // g


def _node_size(width: int, height: int) -> tuple[int, int]:
    """Largest integer node size at the image's EXACT aspect that fits the fit-box (CV-IMAGE-ASPECT-RATIO-01:
    exact ratio kills drift; maximizing within the box keeps slot fill above the 20% floor)."""
    rw, rh = _reduced_aspect(width, height)
    k = max(1, min(_IMG_MAX_W // rw, _IMG_MAX_H // rh))
    return rw * k, rh * k


def load_variants(manifest_path: Path, *, vault_root: Path) -> list[VariantEntry]:
    """Manifest rows -> reviewable variants (path derived when the run record lacks one; must exist on disk)."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    base_rel = manifest_path.parent.relative_to(vault_root)
    out: list[VariantEntry] = []
    for row in manifest.get("variants", []):
        vid = row.get("id")
        label = str(row.get("label", "") or f"variant_{vid}")
        rel = row.get("output_path") or str(base_rel / "variations" / f"anchor_var_{vid}_{label}.png")
        image = vault_root / rel
        if not image.exists():
            continue
        width, height = _png_dimensions(image)
        model = (row.get("result_summary") or {}).get("model") or str(row.get("method", "") or "unknown")
        out.append(
            VariantEntry(
                variant_id=f"var_{vid}",
                label=label,
                axis=str(row.get("axis", "") or ""),
                image_vault_path=str(rel),
                prompt=str(row.get("prompt_or_instruction", "") or ""),
                model=model,
                width=width,
                height=height,
            )
        )
    if not out:
        raise ValueError(f"{manifest_path}: no variant images found on disk")
    return out


# ============================================================================================================
# Sidecar notes (the Meta Bind capture surface).
# ============================================================================================================

def _sidecar_frontmatter(v: VariantEntry, surface: str, canvas_rel: str) -> dict[str, Any]:
    """The spec §3 sidecar schema — identity + controls (pre-seeded empty) + the collector's ledger keys."""
    return {
        "type": "review_sidecar",
        "review_surface": surface,
        "review_canvas": canvas_rel,
        "variant_id": v.variant_id,
        "variant_label": v.label,
        "image_path": v.image_vault_path,
        "model": v.model,
        "prompt": v.prompt,
        "reviewer": None,
        "verdict": None,
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


def _sidecar_body(v: VariantEntry) -> str:
    """Meta Bind controls — JS-less (INPUT fields + one `updateMetadata` button; `enableJs: false` holds).

    multiSelect is block-only in Meta Bind (1.4.x): inline `INPUT[multiSelect(...)]` renders
    [META_BIND_ERROR]; it must be emitted as a fenced ```meta-bind block (agent-confirmed render,
    2026-08-04).
    """
    verdict_opts = ", ".join(f"option({o})" for o in VERDICT_OPTIONS)
    rating_opts = ", ".join(f"option({o})" for o in RATING_OPTIONS)
    defect_opts = ", ".join(f"option({t})" for t in DEFECT_VOCAB)
    return f"""**{v.variant_id} — {v.label}** (axis: {v.axis or "n/a"} · {v.width}×{v.height})

Verdict (required): `INPUT[inlineSelect({verdict_opts}):verdict]`
Rating (1–5): `INPUT[inlineSelect({rating_opts}):rating]`

Defect tags (controlled vocabulary):

```meta-bind
INPUT[multiSelect({defect_opts}):defect_tags]
```

Note: `INPUT[textArea:note]`
Prompt edit (whole-string delta, v1.0): `INPUT[textArea:prompt_edit]`

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

> Save the note, then run the collector (see the pilot README). Nothing dispatches from this surface —
> `regenerate` is an intent flag under `review_dispatch_contract v0` (spec §6).
"""


def _dump_frontmatter(fm: dict[str, Any]) -> str:
    import yaml

    return "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n\n"


# ============================================================================================================
# The canvas.
# ============================================================================================================

def _affordances_for(v: VariantEntry, sidecar_node_id: str) -> dict[str, dict[str, Any]]:
    a = {
        f"{v.variant_id}.verdict": {
            "anchor": sidecar_node_id, "kind": "choice", "options": list(VERDICT_OPTIONS),
            "prompt": f"Verdict for {v.variant_id} ({v.label})", "required": True,
        },
        f"{v.variant_id}.rating": {
            "anchor": sidecar_node_id, "kind": "choice", "options": list(RATING_OPTIONS),
            "prompt": f"Overall rating for {v.variant_id}", "required": False,
        },
        f"{v.variant_id}.defect": {
            "anchor": sidecar_node_id, "kind": "choice", "options": list(DEFECT_VOCAB),
            "prompt": f"Defect tags for {v.variant_id} (one response per tag)", "required": False,
        },
        f"{v.variant_id}.note": {
            "anchor": sidecar_node_id, "kind": "annotation",
            "prompt": f"Free note on {v.variant_id}", "required": False,
        },
        f"{v.variant_id}.prompt_edit": {
            "anchor": sidecar_node_id, "kind": "input",
            "prompt": f"Prompt delta for {v.variant_id}", "required": False,
        },
    }
    for action in ("regenerate", "pin", "escalate"):
        a[f"{v.variant_id}.{action}"] = {
            "anchor": sidecar_node_id, "kind": "action",
            "prompt": f"{action} intent for {v.variant_id}", "required": False,
        }
    return a


@dataclass(frozen=True)
class ReviewSurfacePaths:
    canvas: Path
    sidecars: dict[str, Path]  # variant_id -> sidecar path
    readme: Path


def build_review_surface(
    manifest_path: Path = DEFAULT_MANIFEST,
    out_dir: Path = DEFAULT_OUT_DIR,
    *,
    vault_root: Path = _VAULT_ROOT,
    surface_name: str = DEFAULT_SURFACE_NAME,
    register: str = DEFAULT_REGISTER,
    force: bool = False,
) -> ReviewSurfacePaths:
    """Build the review canvas + sidecars + README under ``out_dir``. Never destroys operator signal:
    refuses to overwrite a sidecar whose ``verdict`` is set unless ``force``."""
    import yaml

    variants = load_variants(manifest_path, vault_root=vault_root)
    out_dir.mkdir(parents=True, exist_ok=True)
    sidecar_dir = out_dir / "sidecars"
    sidecar_dir.mkdir(exist_ok=True)
    canvas_path = out_dir / f"{surface_name}.canvas"
    canvas_rel = str(canvas_path.relative_to(vault_root))

    # --- sidecars ------------------------------------------------------------------------------------------
    sidecars: dict[str, Path] = {}
    for v in variants:
        sp = sidecar_dir / f"{v.variant_id}.md"
        if sp.exists() and not force:
            existing = sp.read_text(encoding="utf-8")
            if existing.startswith("---"):
                fm = yaml.safe_load(existing.split("---", 2)[1]) or {}
                if fm.get("verdict"):
                    raise FileExistsError(
                        f"{sp}: carries a verdict ({fm['verdict']!r}) — refusing to overwrite operator "
                        "signal (use force=True after collecting)"
                    )
        sp.write_text(
            _dump_frontmatter(_sidecar_frontmatter(v, surface_name, canvas_rel)) + _sidecar_body(v),
            encoding="utf-8",
        )
        sidecars[v.variant_id] = sp

    # --- canvas --------------------------------------------------------------------------------------------
    cb = CanvasBuilder(name=surface_name, version="1.0.0")
    header = (
        "**Science-Stanley variant review — HR pilot**\n\n"
        f"Register `{register}` · {len(variants)} variants. Open each sidecar, set the verdict controls, "
        "save — then run the collector (README). Regenerate/pin/escalate are intent flags; nothing dispatches."
    )
    cb.add_text_node("header", header, x=0, y=-200, width=_GROUP_W, height=140)

    component_types: dict[str, dict[str, Any]] = {
        "header": {"class": "text", "semantic_type": "instruction", "degrades_to": "text"},
    }
    affordances: dict[str, dict[str, Any]] = {}
    for i, v in enumerate(variants):
        row, col = divmod(i, _COLS)
        gx = col * (_GROUP_W + _GUTTER)
        gy = row * (_GROUP_H + _GUTTER)
        gid = f"{v.variant_id}_group"
        img_id = f"{v.variant_id}_image"
        side_id = f"{v.variant_id}_sidecar"
        label = f"{v.variant_id.upper()} · {v.label.replace('_', ' ').upper()}"[: _GROUP_W // 25]
        cb.add_group(gid, label, x=gx, y=gy, width=_GROUP_W, height=_GROUP_H)

        iw, ih = _node_size(v.width, v.height)
        cb.add_file_node(
            img_id, v.image_vault_path,
            x=gx + _PAD_X, y=gy + _PAD_Y + (_SIDECAR_H - ih) // 2, width=iw, height=ih,
        )
        sidecar_rel = str(sidecars[v.variant_id].relative_to(vault_root))
        cb.add_file_node(
            side_id, sidecar_rel,
            x=gx + _GROUP_W - _PAD_X - _SIDECAR_W, y=gy + _PAD_Y, width=_SIDECAR_W, height=_SIDECAR_H,
        )
        cb.add_edge(f"{v.variant_id}_edge", img_id, side_id, from_side="right", to_side="left")

        rw, rh = _reduced_aspect(v.width, v.height)
        component_types[img_id] = {
            "class": "image", "semantic_type": "variant", "degrades_to": "file",
            "qualities": {"substrate": "raster", "aspect_ratio": f"{rw}:{rh}", "status": "rendered",
                          "model": v.model},
        }
        component_types[side_id] = {
            "class": "embed", "semantic_type": "review_sidecar", "degrades_to": "file",
        }
        affordances.update(_affordances_for(v, side_id))

    cb._reserved.update(
        {
            "adna_version": "2.0.0",
            "conformance_level": "adna_native",
            "sync": {"sync_hash": cb.compute_sync_hash()},
            "component_types": component_types,
            "interaction": {
                "interaction_version": "1.0",
                "affordances": affordances,
                "responses": [],
                "state": {"turn": "t1", "open": [f"{v.variant_id}.verdict" for v in variants]},
            },
        }
    )
    doc = cb.build()

    report = validate_suite(doc, ConformanceLevel.ADNA_NATIVE)
    if report.level_reached is not ConformanceLevel.ADNA_NATIVE:
        raise ValueError(
            "review canvas failed its own gate (adna_native): "
            + "; ".join(f["msg"] for f in report.failed)
        )

    canvas_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    readme = out_dir / "README.md"
    readme.write_text(
        f"""# HR review-surface pilot — `{surface_name}`

Operator RLHF review surface over the `{register}` variant set (Halftone HR;
spec: `what/specs/spec_canvas_review_surface.md`). `enableJs: false` throughout.

## Review

1. Open `{surface_name}.canvas` in Obsidian (Advanced Canvas + Meta Bind ≥1.4).
2. In each variant's sidecar: set **verdict** (required), optionally rating / defect tags / note /
   prompt edit / intent toggles. Saving the note IS the capture — verdicts live in sidecar frontmatter.

## Collect (fan out to the three sinks)

```bash
cd what/production
canvas_core/.venv/bin/python -m canvas_core.rlhf.review_collect \\
    ../artifacts/review_surface_pilot/{surface_name}.canvas --approver <you>
```

Appends `_reserved.interaction.responses[]` (append-only), writes Schema-A `SelectionRecord`s for approvals
into `what/artifacts/image_gen_dataset/`, and accumulates III signals into the live learning store.
Re-runs are no-ops (`collected_at` ledger + response dedup + deterministic selection ids). `--dry-run` reports
without writing; re-review a variant by clearing its `collected_at`/`verdict` or passing `--turn t2`.

Regenerate/pin/escalate are captured as **intent flags** only — dispatch is `review_dispatch_contract v0`
(spec §6), deferred pending Bearly P5 evidence.
""",
        encoding="utf-8",
    )
    return ReviewSurfacePaths(canvas=canvas_path, sidecars=sidecars, readme=readme)


def _main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="python -m canvas_core.rlhf.review_canvas",
        description="Build the HR review-surface pilot (canvas + Meta Bind sidecars + README).",
    )
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--surface-name", default=DEFAULT_SURFACE_NAME)
    ap.add_argument("--register", default=DEFAULT_REGISTER)
    ap.add_argument("--force", action="store_true",
                    help="overwrite sidecars even if they carry verdicts (destroys operator signal!)")
    args = ap.parse_args(argv)
    paths = build_review_surface(
        args.manifest, args.out, surface_name=args.surface_name, register=args.register, force=args.force
    )
    print(f"review surface: {paths.canvas}")
    print(f"sidecars: {len(paths.sidecars)} under {paths.canvas.parent / 'sidecars'}")
    print(f"README: {paths.readme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
