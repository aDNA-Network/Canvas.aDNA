"""Conformance harness — runs the suite and emits a report.

E0.1: signatures frozen; bodies raise NotImplementedError (E2.1). The CLI entry point
(``canvas-std``) is wired in pyproject and implemented at E2.3.
Spec: spec_conformance_suite §1, §7.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from canvas_std.validate import ConformanceLevel


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


def validate_suite(doc: dict[str, Any], declared: ConformanceLevel) -> ConformanceReport:
    """Run C-*/E-*/A-* + degradation D-1..D-3; return a ConformanceReport. Implemented at E2.1."""
    raise NotImplementedError("validate_suite(): implemented at Keystone E2.1")


def _cli(argv: list[str] | None = None) -> int:
    """``canvas-std`` CLI entry point (pyproject [project.scripts]). Implemented at E2.3."""
    raise NotImplementedError("canvas-std CLI: implemented at Keystone E2.3")
