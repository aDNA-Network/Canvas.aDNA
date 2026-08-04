"""CV-GROUP-LABEL-01 — group label truncation against group width.

Obsidian group labels never wrap: they hard-ellipsise at the group's width
(``02 · THE AUTHENTIC ...``). Worse, because of ``--zoom-multiplier`` the
label **scales up as you zoom out**, so fewer characters fit the further back
you stand — exactly the view an operator uses to survey a large canvas.

Budget model (Obsidian-CSS-derived, Kennedy coord 2026-08-03):
``chars <= width / 25`` for ALL-CAPS labels (~15% wider glyphs), or
``width / 22`` for mixed case.

CV-GROUP-PADDING-01 measures *children* against the group frame; nothing
before this trap measured the *label string* against the group's width.

New in Halftone HV (2026-08-03). Substrate-neutral — zero application imports.
"""

from __future__ import annotations

import math

from ..text_metrics import (
    OBSIDIAN_GROUP_LABEL_DIVISOR_CAPS,
    OBSIDIAN_GROUP_LABEL_DIVISOR_MIXED,
)
from . import TrapFinding

TRAP_ID = "CV-GROUP-LABEL-01"

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]


def _escalate_severity(severity: str) -> str:
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[min(idx + 1, len(_SEVERITY_ORDER) - 1)]


def label_budget(width: float, label: str) -> int:
    """Character budget for a group label at the given group width."""
    caps = label == label.upper()
    divisor = (
        OBSIDIAN_GROUP_LABEL_DIVISOR_CAPS if caps
        else OBSIDIAN_GROUP_LABEL_DIVISOR_MIXED
    )
    return int(width / divisor)


def check(
    canvas_data: dict,
    *,
    r11_node_ids: set[str] | None = None,
) -> list[TrapFinding]:
    """Flag group labels that exceed their width's character budget.

    Args:
        canvas_data: Parsed canvas JSON (must have ``"nodes"`` key).
        r11_node_ids: Optional set of node IDs under R11 gating (severity +1).

    Returns:
        List of :class:`TrapFinding` instances (may be empty).
    """
    findings: list[TrapFinding] = []
    r11 = r11_node_ids or set()

    for node in canvas_data.get("nodes", []):
        if node.get("type") != "group":
            continue
        label = node.get("label", "")
        if not label:
            continue
        width = float(node.get("width", 0))
        if width <= 0:
            continue
        budget = label_budget(width, label)
        if len(label) > budget:
            caps = label == label.upper()
            divisor = (
                OBSIDIAN_GROUP_LABEL_DIVISOR_CAPS if caps
                else OBSIDIAN_GROUP_LABEL_DIVISOR_MIXED
            )
            findings.append(TrapFinding(
                trap_id=TRAP_ID,
                condition="label_truncates",
                node_ids=[node.get("id", "<unknown>")],
                severity="high",
                message=(
                    f"Label is {len(label)} chars, budget {budget} at width "
                    f"{width:.0f} — truncates with an ellipsis (and worsens as "
                    f"you zoom out). Shorten the label, or widen the group to "
                    f">= {math.ceil(len(label) * divisor)}"
                ),
            ))

    if r11:
        for finding in findings:
            if any(nid in r11 for nid in finding.node_ids):
                finding.severity = _escalate_severity(finding.severity)

    return findings
