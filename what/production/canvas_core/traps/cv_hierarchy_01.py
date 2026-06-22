"""CV-HIERARCHY-01 — visual hierarchy inconsistency (heading weight collapse).

Detects per-group hierarchy failures using markdown heading markers as
the structural signal (Obsidian-Canvas text nodes carry markdown
content; ``# Title`` ≡ H1, ``## Subtitle`` ≡ H2, etc.).  Two conditions:

  (a) **title_slot_missing** — group has 1+ text nodes but no text node
      both (i) starts with a heading marker (``# ``, ``## ``, …) and
      (ii) sits in the upper TITLE_REGION_FRACTION (default 0.4) of the
      group's height.  A slide with no title-positioned heading reads
      as orphaned body text.
  (b) **hierarchy_ratio_collapse** — group contains 2+ text nodes that
      start with H1 (``# ``) markers, signalling competing titles.
      Multiple H1s in a single slide is a heading-weight collapse.

Box-area is intentionally not used as a font-size proxy: in the
Obsidian-Canvas model, text-node ``width × height`` reflects the
container, not the rendered text size, so a long body text can have a
larger box than a hero heading.  Markdown markers + position give a
substrate-neutral signal that does not require parsing CSS.

New in M-R3-01a (Phase R3 — III scaffold-trap implementation).
"""

from __future__ import annotations

import re

from ..spatial import bounding_box
from . import TrapFinding

TRAP_ID = "CV-HIERARCHY-01"
TITLE_REGION_FRACTION = 0.4  # title must sit within the top 40% of group height

SEVERITY_DEFAULTS: dict[str, str] = {
    "title_slot_missing": "medium",
    "hierarchy_ratio_collapse": "medium",
}

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]
_HEADING_RE = re.compile(r"^\s*(#{1,6})\s+\S")


def _escalate_severity(severity: str) -> str:
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[min(idx + 1, len(_SEVERITY_ORDER) - 1)]


def _heading_level(text: str) -> int | None:
    """Return heading level (1..6) or None for body / non-heading text."""
    if not text:
        return None
    first_line = text.lstrip().split("\n", 1)[0]
    m = _HEADING_RE.match(first_line)
    if m is None:
        return None
    return len(m.group(1))


def _children_of(group: dict, nodes: list[dict]) -> list[dict]:
    gx1, gy1, gx2, gy2 = bounding_box(group)
    out: list[dict] = []
    for n in nodes:
        if n is group or n.get("type") == "group":
            continue
        nx = n.get("x", 0.0)
        ny = n.get("y", 0.0)
        if gx1 <= nx <= gx2 and gy1 <= ny <= gy2:
            out.append(n)
    return out


def check(
    canvas_data: dict,
    *,
    r11_node_ids: set[str] | None = None,
    title_region_fraction: float = TITLE_REGION_FRACTION,
) -> list[TrapFinding]:
    """Run CV-HIERARCHY-01 against a canvas.

    Args:
        canvas_data: Parsed canvas JSON (must have ``"nodes"`` key).
        r11_node_ids: Optional set of node IDs under R11 gating.
        title_region_fraction: Upper-region fraction in which a title
            heading must sit.  Default 0.4 (top 40% of group height).

    Returns:
        List of :class:`TrapFinding` instances (may be empty).
    """
    nodes = canvas_data.get("nodes", [])
    groups = [n for n in nodes if n.get("type") == "group"]

    if not groups:
        return []

    findings: list[TrapFinding] = []
    r11 = r11_node_ids or set()

    for g in groups:
        gid = g.get("id", "<unknown>")
        gx, gy = g.get("x", 0.0), g.get("y", 0.0)
        gh = float(g.get("height", 0.0))
        if gh <= 0:
            continue
        title_y_max = gy + title_region_fraction * gh

        children = _children_of(g, nodes)
        text_children = [c for c in children if c.get("type") == "text"]
        if not text_children:
            continue  # nothing to check

        # Find title candidates: heading-marker text in the upper region.
        h1_nodes: list[dict] = []
        title_in_slot: list[dict] = []
        any_heading_in_slot = False
        for tn in text_children:
            level = _heading_level(tn.get("text", ""))
            if level is None:
                continue
            ny = tn.get("y", 0.0)
            in_slot = ny <= title_y_max
            if level == 1:
                h1_nodes.append(tn)
            if in_slot:
                title_in_slot.append(tn)
                any_heading_in_slot = True

        # --- (a) title_slot_missing ---
        if not any_heading_in_slot:
            label = g.get("label", gid)
            findings.append(TrapFinding(
                trap_id=TRAP_ID,
                condition="title_slot_missing",
                node_ids=[gid],
                severity=SEVERITY_DEFAULTS["title_slot_missing"],
                message=(
                    f"Group '{label}' has {len(text_children)} text node(s) but "
                    f"no markdown heading positioned in the upper "
                    f"{title_region_fraction:.0%} of the group"
                ),
            ))

        # --- (b) hierarchy_ratio_collapse — multiple H1s ---
        if len(h1_nodes) >= 2:
            ids = [n.get("id", "<unknown>") for n in h1_nodes]
            label = g.get("label", gid)
            findings.append(TrapFinding(
                trap_id=TRAP_ID,
                condition="hierarchy_ratio_collapse",
                node_ids=ids,
                severity=SEVERITY_DEFAULTS["hierarchy_ratio_collapse"],
                message=(
                    f"Group '{label}' has {len(h1_nodes)} H1 headings "
                    f"competing for the title slot"
                ),
            ))

    # --- R11 escalation ---
    if r11:
        for finding in findings:
            if any(nid in r11 for nid in finding.node_ids):
                finding.severity = _escalate_severity(finding.severity)

    return findings
