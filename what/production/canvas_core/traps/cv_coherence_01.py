"""CV-COHERENCE-01 — visual consistency drift between slides/panels.

Detects style fingerprint divergence across sibling groups (slides for
deck canvases, pages/panels for comic canvases).  Two conditions:

  (a) **palette_drift** — a group's ``color`` token is unique (no other
      group on the canvas uses it).
  (b) **style_drift** — a cssclass token appears in only one group's
      child nodes (one-off style across the canvas).

Substrate-neutral — operates on the generic canvas dict shape (groups +
text/file children with optional ``styleAttributes.cssclasses``).
Calibration-cycle slice (re-running against known-defective canvases +
threshold tuning) is out of scope here per 2026-04-30 amendment — that
moves to the successor v1.1 hardening campaign.

New in M-R3-01a (Phase R3 — III scaffold-trap implementation).
"""

from __future__ import annotations

from ..spatial import bounding_box
from . import TrapFinding

TRAP_ID = "CV-COHERENCE-01"

SEVERITY_DEFAULTS: dict[str, str] = {
    "palette_drift": "medium",
    "style_drift": "medium",
}

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]


def _escalate_severity(severity: str) -> str:
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[min(idx + 1, len(_SEVERITY_ORDER) - 1)]


def _children_of(group: dict, nodes: list[dict]) -> list[dict]:
    """Return non-group nodes whose origin lies inside *group*'s bounds."""
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


def _cssclass_tokens(node: dict) -> set[str]:
    style = node.get("styleAttributes") or {}
    raw = style.get("cssclasses", "") or ""
    return {tok for tok in raw.split() if tok}


def check(
    canvas_data: dict,
    *,
    r11_node_ids: set[str] | None = None,
) -> list[TrapFinding]:
    """Run CV-COHERENCE-01 against a canvas.

    Args:
        canvas_data: Parsed canvas JSON (must have ``"nodes"`` key).
        r11_node_ids: Optional set of node IDs under R11 gating.

    Returns:
        List of :class:`TrapFinding` instances (may be empty).
    """
    nodes = canvas_data.get("nodes", [])
    groups = [n for n in nodes if n.get("type") == "group"]

    if len(groups) < 2:
        return []

    findings: list[TrapFinding] = []
    r11 = r11_node_ids or set()

    # --- Build per-group style fingerprints ---
    group_color: dict[str, str | None] = {}
    group_cssclasses: dict[str, set[str]] = {}
    for g in groups:
        gid = g.get("id", "<unknown>")
        group_color[gid] = g.get("color")
        children = _children_of(g, nodes)
        tokens: set[str] = set()
        for c in children:
            tokens |= _cssclass_tokens(c)
        group_cssclasses[gid] = tokens

    # --- (a) palette_drift — singleton color values ---
    color_counts: dict[str | None, int] = {}
    for col in group_color.values():
        if col is None:
            continue
        color_counts[col] = color_counts.get(col, 0) + 1

    for gid, col in group_color.items():
        if col is None:
            continue
        if color_counts.get(col, 0) == 1:
            findings.append(TrapFinding(
                trap_id=TRAP_ID,
                condition="palette_drift",
                node_ids=[gid],
                severity=SEVERITY_DEFAULTS["palette_drift"],
                message=(
                    f"Group {gid} uses palette color '{col}' that no other "
                    f"group on the canvas uses (singleton across {len(groups)} groups)"
                ),
            ))

    # --- (b) style_drift — singleton cssclass tokens ---
    token_groups: dict[str, list[str]] = {}
    for gid, tokens in group_cssclasses.items():
        for tok in tokens:
            token_groups.setdefault(tok, []).append(gid)

    seen_singleton_pairs: set[tuple[str, str]] = set()
    for tok, gids in token_groups.items():
        if len(gids) != 1:
            continue
        owning_gid = gids[0]
        key = (owning_gid, tok)
        if key in seen_singleton_pairs:
            continue
        seen_singleton_pairs.add(key)
        findings.append(TrapFinding(
            trap_id=TRAP_ID,
            condition="style_drift",
            node_ids=[owning_gid],
            severity=SEVERITY_DEFAULTS["style_drift"],
            message=(
                f"cssclass '{tok}' appears only in group {owning_gid} "
                f"(one-off style across {len(groups)} groups)"
            ),
        ))

    # --- R11 escalation ---
    if r11:
        for finding in findings:
            if any(nid in r11 for nid in finding.node_ids):
                finding.severity = _escalate_severity(finding.severity)

    return findings
