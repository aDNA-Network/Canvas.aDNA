"""CV-LEAD-COST-01 — avoidable heading lead cost in canvas text nodes.

Obsidian canvas text nodes render in a ``display:flex; flex-direction:column``
content box, so margins DO NOT COLLAPSE: a ``##`` lead costs **98.9px** of
vertical space before a single body character renders (``###`` 74.8px, ``#``
56.7px) against **40.0px** for a ``**bold**`` lead that still reads as a
title — a saving of more than two body lines per node.

The headline authoring rule (see ``what/docs/canvas_authoring_guidance.md``):
**never use ``#``/``##``/``###`` to title a canvas text node.**

Warn-class trap (severity ``medium``): a heading lead is not itself broken —
it is the single largest avoidable cause of CV-TEXT-BOUNDS-01 overflow, and
was the root cause of the Oration M-R5 incident (Kennedy coord, 2026-08-03).

New in Halftone HV (2026-08-03). Substrate-neutral — zero application imports.
"""

from __future__ import annotations

from ..text_metrics import OBSIDIAN_LEAD_COST, classify_lead_block
from . import TrapFinding

TRAP_ID = "CV-LEAD-COST-01"

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]
_FLAGGED_KINDS = ("h1", "h2", "h3")


def _escalate_severity(severity: str) -> str:
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[min(idx + 1, len(_SEVERITY_ORDER) - 1)]


def check(
    canvas_data: dict,
    *,
    r11_node_ids: set[str] | None = None,
) -> list[TrapFinding]:
    """Flag text nodes whose first block is an ``h1``/``h2``/``h3`` heading.

    Args:
        canvas_data: Parsed canvas JSON (must have ``"nodes"`` key).
        r11_node_ids: Optional set of node IDs under R11 gating (severity +1).

    Returns:
        List of :class:`TrapFinding` instances (may be empty).
    """
    findings: list[TrapFinding] = []
    r11 = r11_node_ids or set()

    for node in canvas_data.get("nodes", []):
        if node.get("type") != "text":
            continue
        text = node.get("text", "")
        blocks = [b for b in text.split("\n") if b.strip()]
        if not blocks:
            continue
        kind = classify_lead_block(blocks[0])
        if kind not in _FLAGGED_KINDS:
            continue
        marker = "#" * int(kind[1])
        findings.append(TrapFinding(
            trap_id=TRAP_ID,
            condition="heading_lead",
            node_ids=[node.get("id", "<unknown>")],
            severity="medium",
            message=(
                f"Leads with `{marker}` costing {OBSIDIAN_LEAD_COST[kind]:.1f}px "
                f"before any body text — use a **bold** lead "
                f"({OBSIDIAN_LEAD_COST['bold']:.1f}px) instead"
            ),
        ))

    if r11:
        for finding in findings:
            if any(nid in r11 for nid in finding.node_ids):
                finding.severity = _escalate_severity(finding.severity)

    return findings
