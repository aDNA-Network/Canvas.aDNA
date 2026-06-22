"""Scoring substrate — criterion scores, category scores, and quality reports.

Generic scoring data structures consumed by both deck and comic applications.
Application-specific scoring logic (e.g., PresentationScoringMixin with its
24 criterion scorers) lives in the application packages (canvas_presentation/
scoring.py in Wave 2).

Migrated from lattice-protocol/extensions/canvas/canvas_scoring.py lines 1-182
(M-1-01 session 2, O4). PresentationReport name kept for provenance — future
rename to CanvasReport is a MINOR if needed (recorded in M-1-01 AAR).

Review Ordering Contract (M-1-04, G6 parity-gate blocker):
    Any application-level review() implementation MUST call structural fixes
    before scoring criteria. The substrate dataclasses (CriterionScore,
    CategoryScore, PresentationReport) assume post-fix state. Without this
    ordering, whitespace/layout scores produce false negatives (Wilhelm
    pre-fix 0.535 vs post-fix 0.965).

    Upstream fix: canvas_scoring.py:1298-1300 (prefix pattern — review()
    calls _apply_structural_fixes() before the 24 criterion scorers).
    Wave 2 extraction (M-2a-03) must preserve this ordering.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# M-1-04 G6: Review ordering contract. Application-level review() must call
# structural fixes before scoring. See module docstring for full rationale.
REVIEW_ORDERING_CONTRACT = (
    "structural_fixes_before_scoring: "
    "upstream canvas_scoring.py:1298-1300 prefix pattern; "
    "Wave 2 M-2a-03 must preserve"
)


@dataclass
class CriterionScore:
    """Score for a single review criterion."""

    id: str  # e.g. "S1", "C3", "T5"
    name: str  # e.g. "Slide Count Appropriateness"
    score: float  # 0.0-1.0 continuous
    weight: float  # within-category weight
    status: str = ""  # "pass" (>=0.8), "warn" (>=0.6), "fail" (<0.6)
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.status:
            if self.score >= 0.8:
                self.status = "pass"
            elif self.score >= 0.6:
                self.status = "warn"
            else:
                self.status = "fail"


@dataclass
class CategoryScore:
    """Per-category review score."""

    name: str
    criteria: list[CriterionScore] = field(default_factory=list)
    # Legacy fields kept for backward compatibility
    _passed: int | None = field(default=None, repr=False)
    _total: int | None = field(default=None, repr=False)
    issues: list[str] = field(default_factory=list)

    @property
    def passed(self) -> int:
        if self._passed is not None:
            return self._passed
        return sum(1 for c in self.criteria if c.status == "pass")

    @passed.setter
    def passed(self, value: int) -> None:
        self._passed = value

    @property
    def total(self) -> int:
        if self._total is not None:
            return self._total
        return len(self.criteria)

    @total.setter
    def total(self, value: int) -> None:
        self._total = value

    @property
    def weighted_score(self) -> float:
        if not self.criteria:
            return self.passed / self.total if self.total > 0 else 1.0
        total_weight = sum(c.weight for c in self.criteria)
        if total_weight <= 0:
            return 1.0
        return sum(c.score * c.weight for c in self.criteria) / total_weight

    @property
    def score(self) -> float:
        return self.weighted_score


_GRADE_THRESHOLDS = [
    (0.90, "A"),
    (0.80, "B"),
    (0.70, "C"),
    (0.60, "D"),
]


def _score_to_grade(score: float) -> str:
    """Convert a 0.0-1.0 score to a letter grade."""
    for threshold, grade in _GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return "F"


@dataclass
class PresentationReport:
    """Scored quality report from review().

    Name kept as PresentationReport for provenance continuity with upstream
    lattice-protocol/extensions/canvas/canvas_scoring.py. Future rename to
    CanvasReport is a semver-MINOR if needed.
    """

    score: float  # 0.0-1.0
    issues: list[str] = field(default_factory=list)
    pass_threshold: float = 0.85
    categories: dict[str, CategoryScore] = field(default_factory=dict)
    suggestions: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.score >= self.pass_threshold

    @property
    def grade(self) -> str:
        return _score_to_grade(self.score)

    @property
    def criterion_scores(self) -> list[CriterionScore]:
        """Flat list of all criterion scores across categories."""
        result: list[CriterionScore] = []
        for cat in self.categories.values():
            result.extend(cat.criteria)
        return result

    def to_dict(self) -> dict[str, Any]:
        """JSON-serializable dict."""
        return {
            "score": self.score,
            "passed": self.passed,
            "grade": self.grade,
            "issues": self.issues,
            "suggestions": self.suggestions,
            "categories": {
                k: {
                    "score": round(v.score, 2),
                    "passed": v.passed,
                    "total": v.total,
                    "issues": v.issues,
                    "criteria": [
                        {
                            "id": c.id,
                            "name": c.name,
                            "score": round(c.score, 2),
                            "weight": c.weight,
                            "status": c.status,
                            "issues": c.issues,
                            "suggestions": c.suggestions,
                        }
                        for c in v.criteria
                    ],
                }
                for k, v in self.categories.items()
            },
        }

    def to_markdown(self) -> str:
        """Render as markdown summary with criterion-level breakdown."""
        lines = [
            f"# Presentation Review: {self.grade} ({self.score:.0%})",
            "",
        ]
        for name, cat in self.categories.items():
            lines.append(f"## {name.title()} ({cat.score:.0%})")
            for c in cat.criteria:
                status_icon = {"pass": "+", "warn": "~", "fail": "-"}
                icon = status_icon.get(c.status, "?")
                lines.append(f"  [{icon}] {c.id} {c.name}: {c.score:.0%}")
                for issue in c.issues:
                    lines.append(f"      - {issue}")
            if not cat.criteria and not cat.issues:
                lines.append("- All checks passed")
            lines.append("")
        if self.suggestions:
            lines.append("## Suggestions")
            for s in self.suggestions:
                lines.append(f"- {s}")
        return "\n".join(lines)
