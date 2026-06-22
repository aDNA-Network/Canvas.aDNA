"""CV-TEXT-BOUNDS-01 — text overflow, overlap, and group-exit trap.

First implemented III trap in the canvas visual trap pack.  Checks three
conditions on canvas text nodes per ADR 004 D2:

  (a) **overflow** — text extent exceeds declared node dimensions (+5 px).
  (b) **overlap** — two text nodes overlap beyond 5 px tolerance.
  (c) **group_exit** — text node escapes parent group bounds by > 5 px.

Consumes:
  - ``canvas_core.text_metrics.measure_text_extent`` (O1)
  - ``canvas_core.spatial.overlaps`` / ``detect_overlaps`` (M-1-02)
  - ``canvas_core.spatial.bounding_box`` (M-1-02)

Substrate-neutral — zero application imports.

New in M-1-07 (Phase 1 — Substrate Extraction).
"""

from __future__ import annotations

from ..text_metrics import measure_text_extent
from ..spatial import bounding_box, detect_overlaps
from . import TrapFinding

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TRAP_ID = "CV-TEXT-BOUNDS-01"
TOLERANCE_PX = 5.0

SEVERITY_DEFAULTS: dict[str, str] = {
    "overflow": "medium",
    "overlap": "high",
    "group_exit": "high",
}

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _escalate_severity(severity: str) -> str:
    """Bump severity one level for R11 escalation.  Caps at critical."""
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[min(idx + 1, len(_SEVERITY_ORDER) - 1)]


def _find_parent_group(
    node: dict,
    groups: list[dict],
) -> dict | None:
    """Return the innermost group whose bounds contain *node*'s origin.

    Uses the node's top-left corner (x, y) — not its full extent — to
    determine parentage.  A node that escapes its group still has its
    origin inside the group, which is exactly the group_exit condition.

    When multiple groups contain the origin, picks the smallest by area.
    Returns ``None`` if no containing group is found.
    """
    nx = node.get("x", 0.0)
    ny = node.get("y", 0.0)
    best: dict | None = None
    best_area = float("inf")

    for grp in groups:
        gx1, gy1, gx2, gy2 = bounding_box(grp)
        if gx1 <= nx <= gx2 and gy1 <= ny <= gy2:
            area = (gx2 - gx1) * (gy2 - gy1)
            if area < best_area:
                best = grp
                best_area = area

    return best


def _check_group_exit(
    node: dict,
    group: dict,
) -> bool:
    """Return True if *node* escapes *group* by more than TOLERANCE_PX."""
    nx1, ny1, nx2, ny2 = bounding_box(node)
    gx1, gy1, gx2, gy2 = bounding_box(group)
    return (
        nx1 < gx1 - TOLERANCE_PX
        or ny1 < gy1 - TOLERANCE_PX
        or nx2 > gx2 + TOLERANCE_PX
        or ny2 > gy2 + TOLERANCE_PX
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def check(
    canvas_data: dict,
    *,
    r11_node_ids: set[str] | None = None,
    font_size: float = 16.0,
    font_family: str | None = None,
) -> list[TrapFinding]:
    """Run CV-TEXT-BOUNDS-01 against a canvas.

    Args:
        canvas_data: Parsed canvas JSON (must have ``"nodes"`` key).
        r11_node_ids: Optional set of node IDs under R11 gating.
            Findings involving R11 nodes get severity +1.
        font_size: Default font size for text measurement (px).
        font_family: Default font family for text measurement.

    Returns:
        List of :class:`TrapFinding` instances (may be empty).
    """
    nodes = canvas_data.get("nodes", [])
    groups = [n for n in nodes if n.get("type") == "group"]
    text_nodes = [n for n in nodes if n.get("type") == "text"]

    if not text_nodes:
        return []

    findings: list[TrapFinding] = []
    r11 = r11_node_ids or set()

    # --- (a) Overflow ---
    for tn in text_nodes:
        text = tn.get("text", "")
        declared_w = float(tn.get("width", 0))
        declared_h = float(tn.get("height", 0))
        node_id = tn.get("id", "<unknown>")

        if not text.strip() or declared_w <= 0 or declared_h <= 0:
            continue

        mw, mh, path = measure_text_extent(
            text,
            font_family=font_family,
            font_size=font_size,
            max_width=declared_w,
        )

        if mh > declared_h + TOLERANCE_PX or mw > declared_w + TOLERANCE_PX:
            sev = SEVERITY_DEFAULTS["overflow"]
            msg = (
                f"Text overflows declared {declared_w:.0f}x{declared_h:.0f} "
                f"(measured {mw:.0f}x{mh:.0f}, path={path})"
            )
            findings.append(TrapFinding(
                trap_id=TRAP_ID,
                condition="overflow",
                node_ids=[node_id],
                severity=sev,
                message=msg,
            ))

    # --- (b) Overlap ---
    overlap_pairs = detect_overlaps(text_nodes, tolerance=TOLERANCE_PX)
    for id_a, id_b in overlap_pairs:
        sev = SEVERITY_DEFAULTS["overlap"]
        findings.append(TrapFinding(
            trap_id=TRAP_ID,
            condition="overlap",
            node_ids=[id_a, id_b],
            severity=sev,
            message=f"Text nodes {id_a} and {id_b} overlap beyond {TOLERANCE_PX}px tolerance",
        ))

    # --- (c) Group exit ---
    for tn in text_nodes:
        node_id = tn.get("id", "<unknown>")
        parent = _find_parent_group(tn, groups)
        if parent is None:
            continue  # top-level text node — no group to escape from

        if _check_group_exit(tn, parent):
            sev = SEVERITY_DEFAULTS["group_exit"]
            parent_label = parent.get("label", parent.get("id", "<unknown>"))
            findings.append(TrapFinding(
                trap_id=TRAP_ID,
                condition="group_exit",
                node_ids=[node_id],
                severity=sev,
                message=f"Text node escapes parent group '{parent_label}' by >{TOLERANCE_PX}px",
            ))

    # --- R11 escalation ---
    if r11:
        for finding in findings:
            if any(nid in r11 for nid in finding.node_ids):
                finding.severity = _escalate_severity(finding.severity)

    return findings
