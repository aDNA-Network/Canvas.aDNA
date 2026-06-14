"""Conformance harness — runs the suite and emits a report.

E2.1 implements ``validate_suite`` (spec_conformance_suite §1, §7): runs C-*/E-*/A-* at each level to find the
``level_reached``, records pass/fail at the declared level, and attaches the D-1..D-3 degradation report. The
``canvas-std`` CLI (``_cli``) is E2.3.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from canvas_std.validate import ConformanceLevel, degradation_report, validate

_ORDER = [ConformanceLevel.CORE, ConformanceLevel.EXTENDED, ConformanceLevel.ADNA_NATIVE]


@dataclass
class ConformanceReport:
    """The §7 report shape."""

    standard_version: str
    declared_level: ConformanceLevel
    level_reached: ConformanceLevel | None = None
    passed: list[str] = field(default_factory=list)
    failed: list[dict[str, Any]] = field(default_factory=list)
    degradation: dict[str, bool] = field(default_factory=dict)  # D-1, D-2, D-3

    @property
    def ok(self) -> bool:
        return not self.failed and self.level_reached is not None

    @property
    def meets_declared(self) -> bool:
        """True iff the doc actually satisfies its declared level."""
        return not self.failed


def validate_suite(doc: dict[str, Any], declared: ConformanceLevel = ConformanceLevel.CORE) -> ConformanceReport:
    """Run the conformance suite. ``level_reached`` = the highest level whose checks all pass (monotone)."""
    from canvas_std import STANDARD_VERSION  # lazy: avoids an import cycle during package init

    level_reached: ConformanceLevel | None = None
    passed: list[str] = []
    declared_errors: list[str] = []
    for lvl in _ORDER:
        errs = validate(doc, lvl)
        if lvl is declared:
            declared_errors = errs
        if errs == []:
            passed.append(lvl.value)
            level_reached = lvl

    report = ConformanceReport(
        standard_version=STANDARD_VERSION,
        declared_level=declared,
        level_reached=level_reached,
        passed=passed,
        failed=[{"id": e.split(":", 1)[0], "msg": e} for e in declared_errors],
    )
    if declared is ConformanceLevel.ADNA_NATIVE:
        report.degradation = degradation_report(doc)
    return report


def _cli(argv: list[str] | None = None) -> int:
    """``canvas-std`` CLI entry point (pyproject [project.scripts]). Implemented at E2.3."""
    raise NotImplementedError("canvas-std CLI: implemented at Keystone E2.3")
