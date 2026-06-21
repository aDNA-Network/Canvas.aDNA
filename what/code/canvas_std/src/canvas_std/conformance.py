"""Conformance harness — runs the suite and emits a report.

E2.1 implements ``validate_suite`` (spec_conformance_suite §1, §7): runs C-*/E-*/A-* at each level to find the
``level_reached``, records pass/fail at the declared level, and attaches the D-1..D-3 degradation report. The
``canvas-std`` CLI (``_cli``) is E2.3.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from importlib import resources
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


def json_schema() -> dict[str, Any]:
    """Return the published v2.0.1 JSON Schema (the structural contract; semantic checks are in the validator)."""
    text = resources.files("canvas_std").joinpath("data/adna_canvas_v2.schema.json").read_text()
    return json.loads(text)


def _report_dict(r: ConformanceReport) -> dict[str, Any]:
    d = asdict(r)
    d["declared_level"] = r.declared_level.value
    d["level_reached"] = r.level_reached.value if r.level_reached else None
    d["ok"] = r.ok
    return d


def _cli(argv: list[str] | None = None) -> int:
    """``canvas-std`` CLI (pyproject [project.scripts]). ``validate <file>`` + ``schema``."""
    import argparse
    from pathlib import Path

    p = argparse.ArgumentParser(prog="canvas-std", description="aDNA Canvas Standard v2.0.1 reference tooling")
    sub = p.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate", help="run the conformance suite on a .canvas file")
    v.add_argument("file")
    v.add_argument("--level", choices=[lvl.value for lvl in ConformanceLevel], default=None,
                   help="declared level (default: the doc's _reserved.conformance_level, else core)")
    v.add_argument("--json", action="store_true", dest="as_json", help="emit the report as JSON")
    sub.add_parser("schema", help="print the v2.0.1 JSON Schema")
    args = p.parse_args(argv)

    if args.cmd == "schema":
        print(json.dumps(json_schema(), indent=2))
        return 0

    doc = json.loads(Path(args.file).read_text())
    level = args.level or doc.get("metadata", {}).get("frontmatter", {}).get("_reserved", {}).get(
        "conformance_level", "core"
    )
    report = validate_suite(doc, ConformanceLevel(level))
    if args.as_json:
        print(json.dumps(_report_dict(report), indent=2))
    else:
        status = "OK" if report.ok else "FAIL"
        print(f"canvas-std {report.standard_version}: {args.file}")
        print(f"  declared={report.declared_level.value}  level_reached={report.level_reached.value if report.level_reached else None}  [{status}]")
        for f in report.failed:
            print(f"  - {f['msg']}")
        if report.degradation:
            print(f"  degradation: {report.degradation}")
    return 0 if report.ok else 1
