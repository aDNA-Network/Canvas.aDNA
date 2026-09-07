"""CV-LEAD-COST-01 — avoidable heading lead cost in canvas text nodes.

Obsidian canvas text nodes render in a ``display:flex; flex-direction:column``
content box, so margins DO NOT COLLAPSE: a ``##`` lead costs **98.9px** of
vertical space before a single body character renders (``###`` 74.8px, ``#``
56.7px) against **42.6px** for a ``####`` lead that still reads as a title — a
saving of more than two body lines per node.

The headline authoring rule (see ``what/docs/canvas_authoring_guidance.md``):
**never use ``#``/``##``/``###`` to title a canvas text node.**

Warn-class trap (severity ``medium``): a heading lead is not itself broken —
it is the single largest avoidable cause of CV-TEXT-BOUNDS-01 overflow, and
was the root cause of the Oration M-R5 incident (Kennedy coord, 2026-08-03).

⛩ **Fix hint corrected 2026-09-07 (F-P2-9, Blueprint P2c): ``**bold**`` →
``####``.** This trap shipped advising *"use a `**bold**` lead (40.0px)"*, and
that advice **produces a canvas that fails a sibling trap in the same pack, in
the same run**: ``**bold**`` carries no markdown heading marker, so a node
following the hint trips ``CV-HIERARCHY-01/title_slot_missing``. Measured
across every lead form at P2 (F-P2-3): ``h1/h2/h3`` pass hierarchy and trip
this trap · ``**bold**`` does the reverse · ``#####``/``######`` pass both only
by classifying as ``plain`` — a green check for the wrong reason · **``####``
alone passes both honestly.** The 2.6px bold saves is not worth the sibling
failure it causes.

F-P2-3 reported that contradiction as one *between two checks* and repaired the
producer. It was also live here, **in a fix hint** — which is worse, because a
failing check tells you something is wrong while a fix hint tells you what to
do, and is believed. ⇒ *When two traps in one pack constrain the same property,
their fix hints are part of the contradiction surface and must be re-derived
together.* The canonical lead is now :data:`canvas_core.layout_fit.LEAD_MARKER`.

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
                f"before any body text — use a `####` lead "
                f"({OBSIDIAN_LEAD_COST['h4']:.1f}px) instead; it is the only "
                f"form that also clears CV-HIERARCHY-01's title slot"
            ),
        ))

    if r11:
        for finding in findings:
            if any(nid in r11 for nid in finding.node_ids):
                finding.severity = _escalate_severity(finding.severity)

    return findings
