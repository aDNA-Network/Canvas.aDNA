"""CV-IMAGE-ASPECT-RATIO-01 — image aspect drift + hero-slot under-fill trap.

Catches the "image looks wrong" failure mode that CV-CONTRAST-01 +
CV-COHERENCE-01 miss because both check pixels-as-displayed; this trap
checks pixels-as-displayed vs. dimensions-as-allocated.

Sub-conditions:
  (a) **aspect_drift** — source asset aspect ratio differs from rendered
      slot aspect ratio by > 5%. Source dimensions are resolved via
      ``PIL.Image.open(asset_root / file).size`` when ``asset_root`` is
      supplied and the file is readable; falls back silently otherwise.
  (b) **slot_underfill** — rendered image area is < 20% of its parent
      slot area AND the slot is hero-sized (heuristic: slot area > 25%
      of the largest container in the canvas).

Severity:
  (a) >0.05 medium / >0.15 high / >0.30 critical
  (b) medium (escalated to high under R11)

Design note (M-V1-2-G-02 D2): the trap-card spec mentions
``references.manifest.json`` as the source-dimension oracle, but that
file lives consumer-side (e.g. ``ScienceStanley.aDNA/what/visual_dna/.../
references/``) not in CanvasForge substrate. PIL fallback keeps the trap
substrate-resident and consumer-agnostic.

Per ``lattice-labs/who/coordination/coord_2026_04_16_forge_split.md``
re-merge rationale, image-dimension resolution is substrate-resident at
``canvas_core/``; the trap is symmetric to existing image-pipeline
checks.

New in M-V1-2-G-02 (Phase 3-extended — III loop implementation).
"""

from __future__ import annotations

from pathlib import Path

from ..spatial import bounding_box
from . import TrapFinding

TRAP_ID = "CV-IMAGE-ASPECT-RATIO-01"

ASPECT_DRIFT_MIN = 0.05
ASPECT_DRIFT_HIGH = 0.15
ASPECT_DRIFT_CRITICAL = 0.30

SLOT_UNDERFILL_MAX = 0.20
HERO_SLOT_FRACTION = 0.25

_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".bmp", ".tiff", ".tif"}
_SEVERITY_ORDER = ["low", "medium", "high", "critical"]


def _escalate_severity(severity: str) -> str:
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[min(idx + 1, len(_SEVERITY_ORDER) - 1)]


def _is_image_node(node: dict) -> bool:
    ntype = node.get("type")
    if ntype == "image":
        return True
    if ntype == "file":
        f = node.get("file") or node.get("filePath") or ""
        if isinstance(f, str):
            ext = Path(f).suffix.lower()
            return ext in _IMAGE_EXTS
    return False


def _resolve_source_dims(
    node: dict,
    asset_root: Path | None,
) -> tuple[float, float] | None:
    """Return (source_w, source_h) via PIL or ``None`` if unresolvable."""
    if asset_root is None:
        return None
    f = node.get("file") or node.get("filePath")
    if not isinstance(f, str) or not f:
        return None
    candidate = Path(asset_root) / f
    if not candidate.is_file():
        return None
    try:
        from PIL import Image

        with Image.open(candidate) as img:
            return (float(img.size[0]), float(img.size[1]))
    except Exception:
        return None


def _find_parent_group(node: dict, groups: list[dict]) -> dict | None:
    """Return the smallest group whose bounds contain *node*'s origin."""
    nx = node.get("x", 0.0)
    ny = node.get("y", 0.0)
    best: dict | None = None
    best_area = float("inf")
    for g in groups:
        if g.get("id") == node.get("id"):
            continue
        gx1, gy1, gx2, gy2 = bounding_box(g)
        if gx1 <= nx <= gx2 and gy1 <= ny <= gy2:
            area = (gx2 - gx1) * (gy2 - gy1)
            if area < best_area:
                best = g
                best_area = area
    return best


def _max_container_area(groups: list[dict]) -> float:
    best = 0.0
    for g in groups:
        gx1, gy1, gx2, gy2 = bounding_box(g)
        a = (gx2 - gx1) * (gy2 - gy1)
        if a > best:
            best = a
    return best


def check(
    canvas_data: dict,
    *,
    r11_node_ids: set[str] | None = None,
    asset_root: Path | str | None = None,
) -> list[TrapFinding]:
    """Run CV-IMAGE-ASPECT-RATIO-01 against a canvas.

    Args:
        canvas_data: Parsed canvas JSON (must have ``"nodes"`` key).
        r11_node_ids: Optional set of node IDs under R11 gating.
        asset_root: Optional directory root to resolve image ``file``
            attributes against. When ``None`` or unresolvable, the
            aspect_drift sub-condition is silently skipped for that node
            (slot_underfill still fires using declared dimensions).

    Returns:
        List of :class:`TrapFinding` (may be empty).
    """
    nodes = canvas_data.get("nodes", [])
    image_nodes = [n for n in nodes if _is_image_node(n)]
    if not image_nodes:
        return []

    groups = [n for n in nodes if n.get("type") == "group"]
    max_container = _max_container_area(groups)

    if isinstance(asset_root, str):
        asset_root_p: Path | None = Path(asset_root)
    else:
        asset_root_p = asset_root

    findings: list[TrapFinding] = []
    r11 = r11_node_ids or set()

    for img in image_nodes:
        img_id = img.get("id", "<unknown>")
        rendered_w = float(img.get("width", 0.0))
        rendered_h = float(img.get("height", 0.0))

        # --- (a) Aspect drift ---
        source = _resolve_source_dims(img, asset_root_p)
        if source is not None and rendered_w > 0 and rendered_h > 0:
            sw, sh = source
            if sw > 0 and sh > 0:
                source_aspect = sw / sh
                rendered_aspect = rendered_w / rendered_h
                drift = abs(source_aspect - rendered_aspect) / source_aspect
                if drift > ASPECT_DRIFT_MIN:
                    if drift > ASPECT_DRIFT_CRITICAL:
                        sev = "critical"
                    elif drift > ASPECT_DRIFT_HIGH:
                        sev = "high"
                    else:
                        sev = "medium"
                    findings.append(TrapFinding(
                        trap_id=TRAP_ID,
                        condition="aspect_drift",
                        node_ids=[img_id],
                        severity=sev,
                        message=(
                            f"Image aspect drift {drift:.2%} "
                            f"(source {sw:.0f}x{sh:.0f} aspect "
                            f"{source_aspect:.3f}; rendered "
                            f"{rendered_w:.0f}x{rendered_h:.0f} aspect "
                            f"{rendered_aspect:.3f})"
                        ),
                    ))

        # --- (b) Slot under-fill ---
        if rendered_w > 0 and rendered_h > 0 and max_container > 0:
            parent = _find_parent_group(img, groups)
            if parent is not None:
                px1, py1, px2, py2 = bounding_box(parent)
                slot_area = (px2 - px1) * (py2 - py1)
                if slot_area > 0:
                    rendered_area = rendered_w * rendered_h
                    slot_fill = rendered_area / slot_area
                    is_hero = slot_area > HERO_SLOT_FRACTION * max_container
                    if slot_fill < SLOT_UNDERFILL_MAX and is_hero:
                        parent_label = parent.get("label", parent.get("id", "<unknown>"))
                        findings.append(TrapFinding(
                            trap_id=TRAP_ID,
                            condition="slot_underfill",
                            node_ids=[img_id],
                            severity="medium",
                            message=(
                                f"Hero slot '{parent_label}' under-filled: "
                                f"slot_fill={slot_fill:.2%} "
                                f"(image {rendered_w:.0f}x{rendered_h:.0f}, "
                                f"slot {px2 - px1:.0f}x{py2 - py1:.0f})"
                            ),
                        ))

    if r11:
        for f in findings:
            if any(nid in r11 for nid in f.node_ids):
                f.severity = _escalate_severity(f.severity)

    return findings
