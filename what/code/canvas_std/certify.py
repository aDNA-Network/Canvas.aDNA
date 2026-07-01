#!/usr/bin/env python3
"""Conformance certification runner for the aDNA Canvas Standard.

Runs a validator over the golden conformance corpus (``tests/fixtures/``) and checks that every fixture reaches
the ``level_reached`` / ``ok`` outcome recorded in ``manifest.json``. Exit 0 if the implementation agrees with
the corpus on every fixture (a passing self-attestation), 1 otherwise.

    python certify.py            # certify the installed canvas_std reference implementation
    python certify.py --json     # machine-readable report

An external implementation certifies itself by running its own validator over the same fixtures and matching
each manifest entry's ``expected_level_reached`` + ``expected_ok``. See CERTIFICATION.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from canvas_std import validate_suite
from canvas_std.validate import ConformanceLevel

FIXTURES = Path(__file__).parent / "tests" / "fixtures"
LEVELS = ["core", "extended", "adna_native"]


def run() -> tuple[list[dict], str]:
    """Validate every corpus fixture; return (per-fixture results, standard_version)."""
    manifest = json.loads((FIXTURES / "manifest.json").read_text())["fixtures"]
    results: list[dict] = []
    standard_version = "?"
    for e in manifest:
        doc = json.loads((FIXTURES / e["path"]).read_text())
        report = validate_suite(doc, ConformanceLevel(e["declared_level"]))
        standard_version = report.standard_version
        reached = report.level_reached.value if report.level_reached else None
        agree = reached == e["expected_level_reached"] and report.ok == e["expected_ok"]
        results.append(
            {
                "fixture": e["path"],
                "declared": e["declared_level"],
                "expected": {"level_reached": e["expected_level_reached"], "ok": e["expected_ok"]},
                "actual": {"level_reached": reached, "ok": report.ok},
                "agree": agree,
                "note": e["note"],
            }
        )
    return results, standard_version


def _attestation(results: list[dict]) -> dict[str, dict]:
    """Per-level self-attestation: how many corpus fixtures exercise each level, and how many agree."""
    attest = {}
    for lvl in LEVELS:
        subset = [r for r in results if r["expected"]["level_reached"] == lvl]
        attest[lvl] = {"fixtures": len(subset), "agree": sum(r["agree"] for r in subset)}
    return attest


def main(argv: list[str]) -> int:
    results, standard_version = run()
    passed = sum(r["agree"] for r in results)
    total = len(results)
    attest = _attestation(results)
    ok = passed == total

    if "--json" in argv:
        print(
            json.dumps(
                {
                    "standard_version": standard_version,
                    "certified": ok,
                    "passed": passed,
                    "total": total,
                    "attestation": attest,
                    "results": results,
                },
                indent=2,
            )
        )
        return 0 if ok else 1

    print(f"aDNA Canvas Standard — conformance certification (Standard v{standard_version})")
    print(f"corpus: {total} golden fixtures ({FIXTURES})\n")
    for r in results:
        mark = "PASS" if r["agree"] else "FAIL"
        print(
            f"  [{mark}] {r['fixture']:<26} declared={r['declared']:<12} "
            f"reached={str(r['actual']['level_reached']):<12} ok={r['actual']['ok']}"
        )
    print("\n  self-attestation by conformance level:")
    for lvl in LEVELS:
        a = attest[lvl]
        print(f"    {lvl:<12} {a['agree']}/{a['fixtures']} fixtures agree")
    print(f"\n{'CERTIFIED' if ok else 'NOT CERTIFIED'}: {passed}/{total} fixtures agree with the corpus.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
