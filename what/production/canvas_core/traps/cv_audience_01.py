"""CV-AUDIENCE-01 — audience-presentation fit ambiguity (live vs async).

Detects deck-wide variance in slide content load that signals an
unclear audience target (sparse live-pitch slides next to dense async-
read slides, etc.).  Two conditions:

  (a) **audience_variance** — words-per-slide variance σ > THRESHOLD_CV × μ
      across the deck.  Fires per outlier slide (|count - μ| > σ).
  (b) **complexity_variance** — average-word-length variance σ > THRESHOLD_CV × μ.
      Fires per outlier slide whose word-length distance from the deck
      mean exceeds 1σ.

Registered as ``deck-specific`` scope in TRAP_PACK_REGISTRY but the
implementation lives in ``canvas_core/traps/`` per ADR 001 — the
detection logic is canvas-shape-agnostic; only the calibration is
deck-tuned.  A future canvas-topology-diagram application could reuse
the same statistical method without code changes.

New in M-R3-01a (Phase R3 — III scaffold-trap implementation).
"""

from __future__ import annotations

import re
from statistics import mean, pstdev

from ..spatial import bounding_box
from . import TrapFinding

TRAP_ID = "CV-AUDIENCE-01"
THRESHOLD_CV = 0.5  # σ > 0.5 × μ is the variance trigger (per mission Objective 2)
MIN_GROUPS = 3       # variance is meaningless on < 3 samples

SEVERITY_DEFAULTS: dict[str, str] = {
    "audience_variance": "high",
    "complexity_variance": "high",
}

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]
_WORD_RE = re.compile(r"\w+")


def _escalate_severity(severity: str) -> str:
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[min(idx + 1, len(_SEVERITY_ORDER) - 1)]


def _children_text(group: dict, nodes: list[dict]) -> str:
    """Concatenate text content of non-group nodes whose origin is inside *group*."""
    gx1, gy1, gx2, gy2 = bounding_box(group)
    parts: list[str] = []
    for n in nodes:
        if n is group or n.get("type") != "text":
            continue
        nx = n.get("x", 0.0)
        ny = n.get("y", 0.0)
        if gx1 <= nx <= gx2 and gy1 <= ny <= gy2:
            parts.append(n.get("text", "") or "")
    return " ".join(parts)


def check(
    canvas_data: dict,
    *,
    r11_node_ids: set[str] | None = None,
    threshold_cv: float = THRESHOLD_CV,
) -> list[TrapFinding]:
    """Run CV-AUDIENCE-01 against a canvas.

    Args:
        canvas_data: Parsed canvas JSON (must have ``"nodes"`` key).
        r11_node_ids: Optional set of node IDs under R11 gating.
        threshold_cv: Coefficient-of-variation trigger.  Default 0.5
            (σ > 0.5 × μ).  Calibration cycle in successor v1.1 campaign.

    Returns:
        List of :class:`TrapFinding` instances (may be empty).
    """
    nodes = canvas_data.get("nodes", [])
    groups = [n for n in nodes if n.get("type") == "group"]

    if len(groups) < MIN_GROUPS:
        return []

    findings: list[TrapFinding] = []
    r11 = r11_node_ids or set()

    word_counts: list[int] = []
    complexities: list[float] = []
    for g in groups:
        text = _children_text(g, nodes)
        words = _WORD_RE.findall(text)
        wc = len(words)
        avg_len = (sum(len(w) for w in words) / wc) if wc else 0.0
        word_counts.append(wc)
        complexities.append(avg_len)

    # --- (a) audience_variance ---
    mu_wc = mean(word_counts)
    sigma_wc = pstdev(word_counts)
    if mu_wc > 0 and sigma_wc > threshold_cv * mu_wc:
        for g, wc in zip(groups, word_counts):
            if abs(wc - mu_wc) > 0.7 * sigma_wc:
                gid = g.get("id", "<unknown>")
                label = g.get("label", gid)
                findings.append(TrapFinding(
                    trap_id=TRAP_ID,
                    condition="audience_variance",
                    node_ids=[gid],
                    severity=SEVERITY_DEFAULTS["audience_variance"],
                    message=(
                        f"Slide '{label}' has {wc} words; deck mean {mu_wc:.0f} "
                        f"σ {sigma_wc:.0f} (CV {sigma_wc/mu_wc:.2f} > {threshold_cv:.2f})"
                    ),
                ))

    # --- (b) complexity_variance ---
    mu_cx = mean(complexities)
    sigma_cx = pstdev(complexities)
    if mu_cx > 0 and sigma_cx > threshold_cv * mu_cx:
        for g, cx in zip(groups, complexities):
            if abs(cx - mu_cx) > 0.7 * sigma_cx:
                gid = g.get("id", "<unknown>")
                label = g.get("label", gid)
                findings.append(TrapFinding(
                    trap_id=TRAP_ID,
                    condition="complexity_variance",
                    node_ids=[gid],
                    severity=SEVERITY_DEFAULTS["complexity_variance"],
                    message=(
                        f"Slide '{label}' avg word-length {cx:.1f}; deck mean "
                        f"{mu_cx:.1f} σ {sigma_cx:.1f} (CV {sigma_cx/mu_cx:.2f} > {threshold_cv:.2f})"
                    ),
                ))

    # --- R11 escalation ---
    if r11:
        for finding in findings:
            if any(nid in r11 for nid in finding.node_ids):
                finding.severity = _escalate_severity(finding.severity)

    return findings
