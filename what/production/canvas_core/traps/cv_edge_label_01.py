"""CV-EDGE-LABEL-01 — edge-label length and collision geometry.

The first trap to evaluate **edges** geometrically (every prior trap operates
on ``type == "text"`` / ``"group"`` nodes only). An Obsidian edge label
(``.canvas-path-label``) is **opaque**, anchored to the edge's bezier
midpoint, and **cannot be repositioned**; it wraps at ~33 chars into a box up
to 838x214 canvas-px — bigger than most nodes — and covers whatever sits
beneath it.

Conditions:
  (a) **label_too_long** — > 30 chars: wraps into a large opaque box (high).
  (b) **label_may_wrap** — 21-30 chars: may wrap to two lines (medium).
  (c) **label_collision** — the label's opaque box overlaps a node that is
      not one of the edge's endpoints, or a group's label band (high).
      Length alone says nothing about whether the box lands on something.

Authoring rule: **edge labels <= 20 chars, or omit** — 83% of fleet edges
carry no label at all; the practice already exists, now documented.

Constants are Obsidian-CSS-derived (Kennedy coord 2026-08-03; see
``canvas_core.text_metrics``). Bezier midpoint model: cubic with control
points extended from the anchor sides by ``clamp(dist/3, 80, 200)`` px,
evaluated at t=0.5.

New in Halftone HV (2026-08-03). Substrate-neutral — zero application imports.
"""

from __future__ import annotations

import math

from ..text_metrics import (
    OBSIDIAN_EDGE_LABEL_CPL,
    OBSIDIAN_EDGE_LABEL_FAIL,
    OBSIDIAN_EDGE_LABEL_LINE,
    OBSIDIAN_EDGE_LABEL_MAXW,
    OBSIDIAN_EDGE_LABEL_PAD,
    OBSIDIAN_EDGE_LABEL_PX_PER_CHAR,
    OBSIDIAN_EDGE_LABEL_WARN,
    OBSIDIAN_GROUP_LABEL_BAND,
    OBSIDIAN_GROUP_LABEL_PX_PER_CHAR,
)
from ..spatial import bounding_box
from . import TrapFinding

TRAP_ID = "CV-EDGE-LABEL-01"

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]


def _escalate_severity(severity: str) -> str:
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[min(idx + 1, len(_SEVERITY_ORDER) - 1)]


def _anchor(node: dict, side: str) -> tuple[float, float]:
    x0, y0, x1, y1 = bounding_box(node)
    return {
        "top": ((x0 + x1) / 2, y0),
        "bottom": ((x0 + x1) / 2, y1),
        "left": (x0, (y0 + y1) / 2),
        "right": (x1, (y0 + y1) / 2),
    }.get(side, ((x0 + x1) / 2, (y0 + y1) / 2))


def _ctrl(pt: tuple[float, float], side: str, d: float) -> tuple[float, float]:
    x, y = pt
    return {
        "top": (x, y - d),
        "bottom": (x, y + d),
        "left": (x - d, y),
        "right": (x + d, y),
    }.get(side, (x, y))


def edge_label_box(edge: dict, nodes_by_id: dict[str, dict]) -> tuple[float, float, float, float] | None:
    """Centre + size of an edge label's opaque box, or None if unlabelled."""
    label = edge.get("label", "")
    if not label:
        return None
    a = nodes_by_id.get(edge.get("fromNode"))
    b = nodes_by_id.get(edge.get("toNode"))
    if not a or not b:
        return None

    from_side = edge.get("fromSide", "right")
    to_side = edge.get("toSide", "left")
    p0 = _anchor(a, from_side)
    p3 = _anchor(b, to_side)
    d = min(200.0, max(80.0, math.dist(p0, p3) / 3))
    p1 = _ctrl(p0, from_side, d)
    p2 = _ctrl(p3, to_side, d)
    mx = (p0[0] + 3 * p1[0] + 3 * p2[0] + p3[0]) / 8
    my = (p0[1] + 3 * p1[1] + 3 * p2[1] + p3[1]) / 8

    lines = math.ceil(len(label) / OBSIDIAN_EDGE_LABEL_CPL)
    if lines > 1:
        w = OBSIDIAN_EDGE_LABEL_MAXW
    else:
        w = min(
            OBSIDIAN_EDGE_LABEL_MAXW,
            len(label) * OBSIDIAN_EDGE_LABEL_PX_PER_CHAR + OBSIDIAN_EDGE_LABEL_PAD,
        )
    h = lines * OBSIDIAN_EDGE_LABEL_LINE + OBSIDIAN_EDGE_LABEL_PAD
    return (mx - w / 2, my - h / 2, mx + w / 2, my + h / 2)


def _rects_overlap(r: tuple[float, ...], s: tuple[float, ...]) -> bool:
    return r[0] < s[2] and s[0] < r[2] and r[1] < s[3] and s[1] < r[3]


def check(
    canvas_data: dict,
    *,
    r11_node_ids: set[str] | None = None,
) -> list[TrapFinding]:
    """Run CV-EDGE-LABEL-01 against a canvas.

    Args:
        canvas_data: Parsed canvas JSON (``"nodes"`` + ``"edges"`` keys).
        r11_node_ids: Optional set of node IDs under R11 gating — findings
            whose collision hits include an R11 node get severity +1.

    Returns:
        List of :class:`TrapFinding` instances (may be empty).
    """
    nodes = canvas_data.get("nodes", [])
    edges = canvas_data.get("edges", [])
    if not edges:
        return []

    nodes_by_id = {n.get("id"): n for n in nodes}
    findings: list[TrapFinding] = []
    r11 = r11_node_ids or set()

    # --- (a)/(b) label length ---
    for edge in edges:
        label = edge.get("label", "")
        if not label:
            continue
        n = len(label)
        edge_id = edge.get("id", "<unknown>")
        if n > OBSIDIAN_EDGE_LABEL_FAIL:
            findings.append(TrapFinding(
                trap_id=TRAP_ID,
                condition="label_too_long",
                node_ids=[edge_id],
                severity="high",
                message=(
                    f"Edge label is {n} chars — wraps into a large opaque box "
                    f"that covers nodes beneath it. Cap {OBSIDIAN_EDGE_LABEL_WARN}; "
                    f"move detail into a node, or drop the label"
                ),
            ))
        elif n > OBSIDIAN_EDGE_LABEL_WARN:
            findings.append(TrapFinding(
                trap_id=TRAP_ID,
                condition="label_may_wrap",
                node_ids=[edge_id],
                severity="medium",
                message=(
                    f"Edge label is {n} chars — may wrap to two lines "
                    f"(cap {OBSIDIAN_EDGE_LABEL_WARN})"
                ),
            ))

    # --- (c) label collision ---
    obstacles: list[tuple[str, tuple[float, float, float, float]]] = [
        (n.get("id", "<unknown>"), bounding_box(n))
        for n in nodes
        if n.get("type") != "group"
    ]
    for g in nodes:
        if g.get("type") == "group" and g.get("label"):
            gx, gy, gx1, _ = bounding_box(g)
            lw = min(gx1 - gx, len(g["label"]) * OBSIDIAN_GROUP_LABEL_PX_PER_CHAR)
            obstacles.append((
                f"{g.get('id', '<unknown>')}:label",
                (gx, gy - OBSIDIAN_GROUP_LABEL_BAND, gx + lw, gy),
            ))

    for edge in edges:
        box = edge_label_box(edge, nodes_by_id)
        if box is None:
            continue
        edge_id = edge.get("id", "<unknown>")
        endpoints = (edge.get("fromNode"), edge.get("toNode"))
        hits = [
            oid for oid, ob in obstacles
            if oid not in endpoints and _rects_overlap(box, ob)
        ]
        if hits:
            shown = ", ".join(hits[:4]) + ("…" if len(hits) > 4 else "")
            findings.append(TrapFinding(
                trap_id=TRAP_ID,
                condition="label_collision",
                node_ids=[edge_id, *hits],
                severity="high",
                message=(
                    f"Edge label \"{edge.get('label', '')}\" renders an opaque box "
                    f"covering {shown}. Labels cannot be repositioned — shorten, "
                    f"or drop the label"
                ),
            ))

    if r11:
        for finding in findings:
            if any(nid in r11 for nid in finding.node_ids):
                finding.severity = _escalate_severity(finding.severity)

    return findings
