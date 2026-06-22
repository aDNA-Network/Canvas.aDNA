"""Conformance-suite harness over the golden corpus (Keystone E2.2).

Runs ``validate_suite`` against every manifest fixture and checks ``level_reached`` + ``ok`` against the declared
expectations — the canonical conformance corpus for the v2.0.0 reference impl.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from canvas_std import validate_suite
from canvas_std.validate import ConformanceLevel

FIXTURES = Path(__file__).parent / "fixtures"
MANIFEST = json.loads((FIXTURES / "manifest.json").read_text())["fixtures"]


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


@pytest.mark.parametrize("entry", MANIFEST, ids=lambda e: e["path"])
def test_validate_suite_outcome(entry):
    report = validate_suite(_load(entry["path"]), ConformanceLevel(entry["declared_level"]))

    expected_reached = entry["expected_level_reached"]
    actual_reached = report.level_reached.value if report.level_reached else None
    assert actual_reached == expected_reached, f"{entry['path']}: level_reached {actual_reached} != {expected_reached}"

    assert report.ok is entry["expected_ok"], f"{entry['path']}: ok {report.ok} != {entry['expected_ok']}"
    # a failing report carries structured failure records; a passing one carries none
    assert (report.failed == []) is entry["expected_valid"]
    assert report.standard_version == "2.0.2"


def test_degradation_only_for_adna_native():
    # validate_suite attaches a D-1..D-3 report only for an aDNA-Native declaration.
    adna = validate_suite(_load("adna_native.canvas"), ConformanceLevel.ADNA_NATIVE)
    assert set(adna.degradation) == {"D-1", "D-2", "D-3"} and all(adna.degradation.values())
    core = validate_suite(_load("core_minimal.canvas"), ConformanceLevel.CORE)
    assert core.degradation == {}
