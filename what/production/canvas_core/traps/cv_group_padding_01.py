"""CV-GROUP-PADDING-01 — content bleeds to container frame edge trap.

Complements CV-NODE-DENSITY-01 (density) and CV-DIMENSION-VISIBILITY-01
(frame visibility): this trap catches the bleed-to-edge failure mode
that's a spatial-discipline problem rather than aggregate density or
frame metadata.

Sub-conditions:
  (a) **aggregate_fill** — combined content bounding box exceeds 90% of
      container width OR height (no breathing room). Severity medium;
      escalates to high at > 0.95.
  (b) **edge_violation** — any individual content node's edge distance
      from the container edge is less than the design-token-defined
      minimum padding (default ``PADDING_MIN_PX = 24``; resolved per
      slide-type via ``design_tokens.get_slide_tokens(slide_type)
      .margin_side`` when slide_type is detectable). Severity medium;
      escalates to high when distance < padding_min but > 0; critical
      when distance < 50% of padding_min (dangerously close to edge).

Per ``lattice-labs/who/coordination/coord_2026_04_16_forge_split.md``
re-merge rationale, design-token resolution is substrate-resident at
``canvas_core/``; the trap is substrate-neutral and consumable by any
future canvas application without modification.

New in M-V1-2-G-02 (Phase 3-extended — III loop implementation).
"""

from __future__ import annotations

from ..design_tokens import _SLIDE_TYPE_DEFAULTS, get_slide_tokens
from ..spatial import bounding_box
from . import TrapFinding

TRAP_ID = "CV-GROUP-PADDING-01"

AGGREGATE_FILL_MEDIUM = 0.90
AGGREGATE_FILL_HIGH = 0.95

PADDING_MIN_PX = 24.0

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]


def _escalate_severity(severity: str) -> str:
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[min(idx + 1, len(_SEVERITY_ORDER) - 1)]


def _is_direct_child(child: dict, container: dict, all_containers: list[dict]) -> bool:
    """True if *container* is the innermost group whose bounds contain *child*'s origin."""
    if child.get("id") == container.get("id"):
        return False
    cx1, cy1, cx2, cy2 = bounding_box(container)
    nx = child.get("x", 0.0)
    ny = child.get("y", 0.0)
    if not (cx1 <= nx <= cx2 and cy1 <= ny <= cy2):
        return False
    container_area = (cx2 - cx1) * (cy2 - cy1)
    for g in all_containers:
        if g.get("id") in (container.get("id"), child.get("id")):
            continue
        gx1, gy1, gx2, gy2 = bounding_box(g)
        if not (gx1 <= nx <= gx2 and gy1 <= ny <= gy2):
            continue
        gx_area = (gx2 - gx1) * (gy2 - gy1)
        if gx_area < container_area:
            return False
    return True


def _bbox_of_children(children: list[dict]) -> tuple[float, float, float, float] | None:
    if not children:
        return None
    xs1 = []
    ys1 = []
    xs2 = []
    ys2 = []
    for ch in children:
        x1, y1, x2, y2 = bounding_box(ch)
        xs1.append(x1)
        ys1.append(y1)
        xs2.append(x2)
        ys2.append(y2)
    return (min(xs1), min(ys1), max(xs2), max(ys2))


def _resolve_padding_min(container: dict) -> float:
    """Resolve the per-container padding minimum.

    Tries ``container['slide_type']`` then ``container['panel_type']``;
    when detectable looks up ``get_slide_tokens(slide_type).margin_side``.
    Falls back to ``PADDING_MIN_PX`` (24).
    """
    for key in ("slide_type", "panel_type"):
        slide_type = container.get(key)
        if isinstance(slide_type, str) and slide_type in _SLIDE_TYPE_DEFAULTS:
            try:
                tokens = get_slide_tokens(slide_type)
                side = float(getattr(tokens, "margin_side", PADDING_MIN_PX))
                if side > 0:
                    return side
            except Exception:
                continue
    return PADDING_MIN_PX


def check(
    canvas_data: dict,
    *,
    r11_node_ids: set[str] | None = None,
) -> list[TrapFinding]:
    """Run CV-GROUP-PADDING-01 against a canvas.

    Args:
        canvas_data: Parsed canvas JSON (must have ``"nodes"`` key).
        r11_node_ids: Optional set of node IDs under R11 gating.

    Returns:
        List of :class:`TrapFinding` (may be empty).
    """
    nodes = canvas_data.get("nodes", [])
    containers = [n for n in nodes if n.get("type") == "group"]
    if not containers:
        return []

    findings: list[TrapFinding] = []
    r11 = r11_node_ids or set()

    for container in containers:
        cx1, cy1, cx2, cy2 = bounding_box(container)
        container_w = cx2 - cx1
        container_h = cy2 - cy1
        if container_w <= 0 or container_h <= 0:
            continue

        direct_children = [
            n for n in nodes
            if _is_direct_child(n, container, containers)
        ]
        if not direct_children:
            continue

        container_id = container.get("id", "<unknown>")
        container_label = container.get("label", container_id)

        # --- (a) Aggregate width/height fill ---
        bbox = _bbox_of_children(direct_children)
        if bbox is not None:
            bx1, by1, bx2, by2 = bbox
            bb_w = bx2 - bx1
            bb_h = by2 - by1
            width_fill = bb_w / container_w if container_w > 0 else 0.0
            height_fill = bb_h / container_h if container_h > 0 else 0.0
            max_fill = max(width_fill, height_fill)
            if max_fill > AGGREGATE_FILL_MEDIUM:
                sev = "high" if max_fill > AGGREGATE_FILL_HIGH else "medium"
                axis = "width" if width_fill >= height_fill else "height"
                child_ids = [c.get("id", "<unknown>") for c in direct_children]
                f = TrapFinding(
                    trap_id=TRAP_ID,
                    condition="aggregate_fill",
                    node_ids=[container_id] + child_ids,
                    severity=sev,
                    message=(
                        f"Container '{container_label}' {axis}_fill="
                        f"{max_fill:.2%} exceeds {AGGREGATE_FILL_MEDIUM:.0%} "
                        f"(no breathing room)"
                    ),
                )
                if r11 and (container_id in r11 or any(cid in r11 for cid in child_ids)):
                    f.severity = _escalate_severity(f.severity)
                findings.append(f)

        # --- (b) Per-node edge violation ---
        padding_min = _resolve_padding_min(container)
        critical_threshold = padding_min * 0.5
        for ch in direct_children:
            chx1, chy1, chx2, chy2 = bounding_box(ch)
            dist_left = chx1 - cx1
            dist_top = chy1 - cy1
            dist_right = cx2 - chx2
            dist_bottom = cy2 - chy2
            min_dist = min(dist_left, dist_top, dist_right, dist_bottom)
            if min_dist >= padding_min:
                continue
            if min_dist < critical_threshold:
                sev = "critical"
            else:
                sev = "high" if min_dist < padding_min * 0.75 else "medium"
            ch_id = ch.get("id", "<unknown>")
            edges = []
            if dist_left < padding_min:
                edges.append(f"left={dist_left:.0f}")
            if dist_top < padding_min:
                edges.append(f"top={dist_top:.0f}")
            if dist_right < padding_min:
                edges.append(f"right={dist_right:.0f}")
            if dist_bottom < padding_min:
                edges.append(f"bottom={dist_bottom:.0f}")
            f = TrapFinding(
                trap_id=TRAP_ID,
                condition="edge_violation",
                node_ids=[ch_id],
                severity=sev,
                message=(
                    f"Node {ch_id} violates padding_min={padding_min:.0f}px "
                    f"in '{container_label}': "
                    + ", ".join(edges)
                ),
            )
            if r11 and (ch_id in r11 or container_id in r11):
                f.severity = _escalate_severity(f.severity)
            findings.append(f)

    return findings
