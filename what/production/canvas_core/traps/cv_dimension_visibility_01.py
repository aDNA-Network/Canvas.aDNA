"""CV-DIMENSION-VISIBILITY-01 — slide/page dimensions hidden from reviewers.

Detects canvases where target aspect ratio is not declared in metadata
and no node surfaces it as a visible affordance.  Reviewers cannot
judge "does this fit a 16:9 slide?" if the canvas does not advertise
its target aspect anywhere.  Two conditions:

  (a) **aspect_ratio_missing** — no aspect-ratio key found in canvas
      top-level keys or metadata (recursive search for one of the
      ASPECT_KEYS tokens).
  (b) **frame_dimension_hidden** — groups share uniform dimensions
      (i.e., the canvas has a consistent slide/page frame), but no
      node-level affordance (frame-typed node, ``aspect_ratio`` style
      attribute, or text content matching an aspect-ratio pattern like
      ``16:9`` / ``1080×1080``) makes the dimensions visible to a
      reviewer.

A future canvas-topology-diagram application could reuse this check
unchanged — the detection is canvas-shape-agnostic.

New in M-R3-01a (Phase R3 — III scaffold-trap implementation).
"""

from __future__ import annotations

import re
from typing import Any

from . import TrapFinding

TRAP_ID = "CV-DIMENSION-VISIBILITY-01"

ASPECT_KEYS = frozenset({
    "aspect_ratio",
    "aspectratio",
    "viewport",
    "dimensions",
    "slide_dimensions",
    "frame_dimensions",
    "page_dimensions",
})

# Matches "16:9", "4:3", "1080x1080", "1080×1080" in text content.
ASPECT_PATTERN = re.compile(r"\b\d{1,5}\s*[:×x]\s*\d{1,5}\b")

SEVERITY_DEFAULTS: dict[str, str] = {
    "aspect_ratio_missing": "medium",
    "frame_dimension_hidden": "medium",
}

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]


def _escalate_severity(severity: str) -> str:
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[min(idx + 1, len(_SEVERITY_ORDER) - 1)]


def _key_matches_aspect(key: str) -> bool:
    return key.lower() in ASPECT_KEYS


def _has_aspect_metadata(canvas_data: dict) -> bool:
    """Recursively search canvas top-level + metadata for aspect-ratio keys."""
    # Top-level canvas dict
    for k in canvas_data.keys():
        if _key_matches_aspect(k):
            return True

    def walk(obj: Any) -> bool:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if _key_matches_aspect(k):
                    return True
                if walk(v):
                    return True
        elif isinstance(obj, list):
            for item in obj:
                if walk(item):
                    return True
        return False

    return walk(canvas_data.get("metadata", {}))


def _has_node_affordance(nodes: list[dict]) -> bool:
    """Return True if any node carries a visible dimension cue."""
    for n in nodes:
        if n.get("type") == "frame":
            return True
        text = n.get("text", "") or ""
        if ASPECT_PATTERN.search(text):
            return True
        style = n.get("styleAttributes") or {}
        if any(_key_matches_aspect(k) for k in style.keys()):
            return True
    return False


def check(
    canvas_data: dict,
    *,
    r11_node_ids: set[str] | None = None,
) -> list[TrapFinding]:
    """Run CV-DIMENSION-VISIBILITY-01 against a canvas.

    Args:
        canvas_data: Parsed canvas JSON.
        r11_node_ids: Optional set of node IDs under R11 gating.

    Returns:
        List of :class:`TrapFinding` instances (may be empty).
    """
    findings: list[TrapFinding] = []
    r11 = r11_node_ids or set()

    nodes = canvas_data.get("nodes", [])
    groups = [n for n in nodes if n.get("type") == "group"]

    has_meta = _has_aspect_metadata(canvas_data)
    has_affordance = _has_node_affordance(nodes)

    # --- (a) aspect_ratio_missing ---
    if not has_meta:
        findings.append(TrapFinding(
            trap_id=TRAP_ID,
            condition="aspect_ratio_missing",
            node_ids=[],
            severity=SEVERITY_DEFAULTS["aspect_ratio_missing"],
            message=(
                "Canvas declares no aspect-ratio metadata — searched top-level "
                f"keys + metadata for any of: {sorted(ASPECT_KEYS)}"
            ),
        ))

    # --- (b) frame_dimension_hidden — uniform frames + no affordance ---
    if groups and not has_affordance:
        dims = {(round(float(g.get("width", 0)), 2),
                 round(float(g.get("height", 0)), 2)) for g in groups}
        if len(dims) == 1:
            (w, h) = next(iter(dims))
            gids = [g.get("id", "<unknown>") for g in groups]
            findings.append(TrapFinding(
                trap_id=TRAP_ID,
                condition="frame_dimension_hidden",
                node_ids=gids,
                severity=SEVERITY_DEFAULTS["frame_dimension_hidden"],
                message=(
                    f"All {len(groups)} groups share dimensions {w:g}x{h:g} "
                    f"(implied aspect) but no node surfaces a dimension "
                    f"affordance to the reviewer"
                ),
            ))

    # --- R11 escalation ---
    if r11:
        for finding in findings:
            if any(nid in r11 for nid in finding.node_ids):
                finding.severity = _escalate_severity(finding.severity)

    return findings
