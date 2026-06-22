"""Rule-based fallback critique when vision model is unavailable.

Runs the III trap pack structurally (no image analysis) against the
canvas data.  Findings are prefixed ``[rule-based fallback]`` and
severity drops one level per ADR 004 § Consequences Negative.

New in M-1-08.  Pure substrate.

M-V1-05 (F-26 fix): routes through ``run_all_traps()`` to cover all 6
implemented traps (CV-COHERENCE-01, CV-AUDIENCE-01, CV-HIERARCHY-01,
CV-DIMENSION-VISIBILITY-01, CV-PENDING-01, CV-TEXT-BOUNDS-01) instead of
calling CV-TEXT-BOUNDS-01 directly.
"""

from __future__ import annotations

import logging

from . import CritiqueFinding
from ..traps import TrapFinding
from ..traps.runner import run_all_traps

_log = logging.getLogger(__name__)

_SEVERITY_ORDER = ["low", "medium", "high", "critical"]


def _degrade_severity(severity: str) -> str:
    """Drop severity one level (quality-degradation for fallback)."""
    idx = _SEVERITY_ORDER.index(severity)
    return _SEVERITY_ORDER[max(idx - 1, 0)]


def run_fallback(
    canvas_data: dict,
    *,
    r11_node_ids: set[str] | None = None,
) -> list[CritiqueFinding]:
    """Run structural trap-pack checks as fallback critique.

    Returns findings with ``source='rule_based_fallback'``,
    severity degraded one level, and observation prefixed.
    """
    findings: list[CritiqueFinding] = []

    # Run all implemented + graduated traps via runner (F-26 fix at M-V1-05).
    trap_findings = run_all_traps(canvas_data, r11_node_ids=r11_node_ids)

    for tf in trap_findings:
        findings.append(CritiqueFinding(
            trap_id=tf.trap_id,
            node_refs=tf.node_ids,
            severity=_degrade_severity(tf.severity),
            observation=f"[rule-based fallback] {tf.message}",
            source="rule_based_fallback",
        ))

    _log.info(
        "Rule-based fallback produced %d findings (severity degraded -1)",
        len(findings),
    )
    return findings
