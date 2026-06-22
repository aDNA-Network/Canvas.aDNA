"""CV-NODE-DENSITY-01 — aggregate content-to-container fill-ratio trap.

Direct counterpart to CV-TEXT-BOUNDS-01: that trap catches a single text
node escaping its node bounds; this trap catches the aggregate-density
problem where every child technically fits but the container as a whole
is over-stuffed.

Closes operator complaint 2026-05-25 ("too much text/images for the size
of the panel they were placed on"). Per container (slide / comic panel /
canvas group), sums rendered child content area against container area
and compares fill_ratio against a per-container-type threshold.

Sub-condition:
  (a) **fill_ratio** — child content area / container area exceeds the
      configured per-type threshold (defaults: title=0.40, content=0.75,
      dense_data=0.85, comic_panel=0.80, unknown=0.75).

Severity ladder (independent of threshold ladder):
  - fill > threshold: medium
  - fill > 0.90:      high
  - fill > 0.95:      critical

Consumes:
  - ``canvas_core.text_metrics.measure_text_extent`` (text area)
  - ``canvas_core.spatial.bounding_box`` (container + child geometry)

Substrate-neutral — zero application imports. Per
``lattice-labs/who/coordination/coord_2026_04_16_forge_split.md``
re-merge rationale, this trap is canvas-substrate-resident; any future
canvas application (topology diagrams, sequence diagrams, comparison
matrices) consumes it without modification.

New in M-V1-2-G-02 (Phase 3-extended — III loop implementation).
"""

from __future__ import annotations

from ..spatial import bounding_box
from ..text_metrics import measure_text_extent
from . import TrapFinding

TRAP_ID = "CV-NODE-DENSITY-01"

FILL_THRESHOLDS: dict[str, float] = {
    "title": 0.40,
    "content": 0.75,
    "dense_data": 0.85,
    "comic_panel": 0.80,
}
DEFAULT_THRESHOLD = 0.75

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]


def _escalate_severity(severity: str) -> str:
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[min(idx + 1, len(_SEVERITY_ORDER) - 1)]


def _container_type(container: dict) -> str:
    """Resolve the container's threshold-lookup type.

    Reads ``slide_type`` then ``panel_type`` then ``type`` markers; falls
    back to ``"content"`` (default threshold).
    """
    for key in ("slide_type", "panel_type"):
        v = container.get(key)
        if isinstance(v, str) and v in FILL_THRESHOLDS:
            return v
    return "content"


def _is_direct_child(child: dict, container: dict) -> bool:
    """True if *child*'s origin lies inside *container*'s bounds.

    Uses origin (not full extent) for parentage so that escaping children
    still count as children of the container they originated in.
    """
    if child.get("id") == container.get("id"):
        return False
    cx1, cy1, cx2, cy2 = bounding_box(container)
    nx = child.get("x", 0.0)
    ny = child.get("y", 0.0)
    return cx1 <= nx <= cx2 and cy1 <= ny <= cy2


def _innermost_parent(child: dict, containers: list[dict]) -> dict | None:
    """Return the smallest container whose bounds contain *child*'s origin."""
    best: dict | None = None
    best_area = float("inf")
    for c in containers:
        if not _is_direct_child(child, c):
            continue
        cx1, cy1, cx2, cy2 = bounding_box(c)
        area = (cx2 - cx1) * (cy2 - cy1)
        if area < best_area:
            best = c
            best_area = area
    return best


def _child_content_area(
    child: dict,
    *,
    font_size: float,
    font_family: str | None,
) -> float:
    """Rendered content area for a single child node.

    Text nodes measure via Pillow / heuristic path; non-text nodes use
    declared ``width × height``.
    """
    if child.get("type") == "text":
        text = child.get("text", "")
        declared_w = float(child.get("width", 0.0))
        if not text.strip() or declared_w <= 0:
            return 0.0
        mw, mh, _ = measure_text_extent(
            text,
            font_family=font_family,
            font_size=font_size,
            max_width=declared_w,
        )
        return float(mw) * float(mh)
    w = float(child.get("width", 0.0))
    h = float(child.get("height", 0.0))
    return max(w * h, 0.0)


def check(
    canvas_data: dict,
    *,
    r11_node_ids: set[str] | None = None,
    font_size: float = 16.0,
    font_family: str | None = None,
) -> list[TrapFinding]:
    """Run CV-NODE-DENSITY-01 against a canvas.

    Args:
        canvas_data: Parsed canvas JSON (must have ``"nodes"`` key).
        r11_node_ids: Optional set of node IDs under R11 gating; findings
            whose container OR any direct child is R11-gated get
            severity +1.
        font_size: Default font size for text measurement (px).
        font_family: Default font family for text measurement.

    Returns:
        List of :class:`TrapFinding` instances (may be empty).
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
        container_area = container_w * container_h
        if container_area <= 0:
            continue

        direct_children = [
            n for n in nodes
            if n.get("id") != container.get("id")
            and _innermost_parent(n, containers) is container
        ]
        if not direct_children:
            continue

        sum_child_area = 0.0
        for ch in direct_children:
            sum_child_area += _child_content_area(
                ch,
                font_size=font_size,
                font_family=font_family,
            )

        fill_ratio = sum_child_area / container_area
        ctype = _container_type(container)
        threshold = FILL_THRESHOLDS.get(ctype, DEFAULT_THRESHOLD)

        if fill_ratio <= threshold:
            continue

        if fill_ratio > 0.95:
            sev = "critical"
        elif fill_ratio > 0.90:
            sev = "high"
        else:
            sev = "medium"

        container_id = container.get("id", "<unknown>")
        container_label = container.get("label", container_id)
        child_ids = [c.get("id", "<unknown>") for c in direct_children]
        msg = (
            f"Container '{container_label}' ({ctype}) fill_ratio="
            f"{fill_ratio:.2f} exceeds threshold {threshold:.2f} "
            f"({len(child_ids)} children)"
        )

        finding = TrapFinding(
            trap_id=TRAP_ID,
            condition="fill_ratio",
            node_ids=[container_id] + child_ids,
            severity=sev,
            message=msg,
        )

        if r11 and (container_id in r11 or any(cid in r11 for cid in child_ids)):
            finding.severity = _escalate_severity(finding.severity)

        findings.append(finding)

    return findings
