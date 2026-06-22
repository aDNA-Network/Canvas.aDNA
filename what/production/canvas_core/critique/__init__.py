"""Agent-autonomous canvas critique pipeline.

Renders canvas artifacts, captures screenshots via headless Chrome
(Playwright), runs vision-model analysis, and emits CV-* trap findings.
Complements HITL review — does not replace it.

New in M-1-08 (Phase 1 — Substrate Extraction).  Pure substrate.

Pipeline:
    canvas → html_renderer → Playwright PNG → vision model → findings
    → agent_observations.md + III trap registry
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class CritiqueFinding:
    """A single finding from agent critique (vision or rule-based)."""

    trap_id: str        # CV-* trap ID
    node_refs: list[str]  # canvas node IDs referenced
    severity: str       # "low" | "medium" | "high" | "critical"
    observation: str    # human-readable observation
    source: str = "agent_critique"  # "agent_critique" | "rule_based_fallback"


@dataclass
class CritiqueResult:
    """Full result from a critique pipeline run."""

    findings: list[CritiqueFinding] = field(default_factory=list)
    rendered_html_path: Path | None = None
    screenshots: dict[str, Path] = field(default_factory=dict)
    cost_usd: float = 0.0
    duration_s: float = 0.0
    vision_model: str = ""
    fallback_used: bool = False


from .agent_critique import run_critique  # noqa: E402

__all__ = [
    "CritiqueFinding",
    "CritiqueResult",
    "run_critique",
]
