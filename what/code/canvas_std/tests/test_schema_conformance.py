"""The published JSON Schema is exercised against real documents — and its coverage is published.

Operation Datum **P4b** (2026-09-15), firewall touch #6, under the operator ruling *"build the test,
and publish its coverage on its face."*

## Why this file exists (F-DT-7, Datum P3)

``canvas_std`` carries each baseline vocabulary **twice**: as a Python constant the reference
validator reads, and as an ``enum`` in ``data/adna_canvas_v2.schema.json``. The ``certification``
gate (12/12) exercises the **validator's verdicts**. Until this file, *nothing exercised the schema.*

That mattered because the schema's consumers are **outside this repository** — a fork, a
``pip install adna-canvas-std``, any external validator of a public Standard. Inside the package every
reader of :func:`json_schema` reads ``$defs.reserved`` only. P3 measured the consequence: gutting the
schema's ``fromSide``/``toSide`` enums from four values to one left **all ten vault gates green**,
while ``jsonschema`` correctly rejected an ordinary canvas.

P3 closed the *existence* half — every constant now declares ``SCHEMA-TWIN``/``VALIDATOR-ONLY`` and
the claim is checked against a derivation (see ``test_registry_consistency.py``). This file closes a
different half: **does the schema actually work on a real document.**

## ⚠ The honest limit, stated on the face of the result rather than discovered later

**The corpus is the coverage, and this corpus is thin.** Measured when this file was written: the 12
fixtures exercise **12 of 40** declared enum values across the eleven non-``reserved`` enums, and two
enums — ``edge.styleAttributes.arrow`` (0/7) and ``edge.fromEnd`` (0/2) — are exercised **not at
all**.

⚠ **The plan for this file predicted it would NOT have caught the F-DT-7 perturbation. Measured, that
prediction was wrong — and the truth is sharper.** Derivations D13a/D13b, Datum P4b:

===============================  ==========================================================
D13a  the *actual* F-DT-7 edit   **CAUGHT** — 5+ fixtures fail. The corpus uses ``"bottom"``
      (``fromSide`` AND                for ``fromSide``, so reducing that enum to ``["top"]``
      ``toSide`` → ``["top"]``)        breaks them.
D13b  ``toSide`` alone →         **NOT caught — 14 passed.** The corpus uses ``"top"`` for
      ``["top"]``                      ``toSide``, its only value there.
===============================  ==========================================================

So the blind spot is real and live, but narrower and more arbitrary than predicted: **which
single-value perturbations are invisible depends on which value the corpus happens to use.**
``fromSide`` is accidentally guarded; ``toSide`` is not; the two zero-coverage enums could be
**deleted outright** and nothing here would notice.

    ⇒ a test that looks like coverage is worse than no test, unless somebody measures what it covers.

⛔ **Do not read the D13a pass as reassurance.** It is a coincidence of fixture authorship, not a
property of this suite, and it would evaporate the moment a fixture changed a side.

That is F-DT-7's own lesson one layer out, which is why :func:`test_enum_coverage_is_published`
exists and why it **prints the figure and names the zero-coverage enums** rather than returning a
bare green. The real guard against an enum vanishing remains P3's declared-state check, because that
one does not depend on the corpus at all.

⚠ ``jsonschema`` is a **dev-only** dependency (``pyproject.toml`` ``[project.optional-dependencies]``).
The zero-runtime-dependency promise of the Standard floor is unchanged — nothing under ``src/``
imports it. It is imported **hard** here, deliberately: a :func:`pytest.importorskip` would make this
suite vanish silently in an environment missing the dependency, which is the F-P2-11 family (*a check
that cannot run is not a check that passes*) in the one place this campaign could least defend it.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema  # hard import — see the module docstring; NEVER importorskip this
import pytest

from canvas_std.conformance import json_schema

FIXTURES = Path(__file__).resolve().parent / "fixtures"

# Fixtures that MUST fail schema validation, and the substring their first error must contain.
# ⛩ The reason is asserted, not merely the failure. A fixture that starts failing for a NEW reason
# (say, because the schema acquired a bad `required`) would otherwise keep this table green while
# meaning something entirely different — the F-DT-6 family: a check that observes correctly and
# reports the wrong cause.
EXPECTED_SCHEMA_FAILURES: dict[str, str] = {
    "core_only_bad_shape.canvas": "'hexagon' is not one of",
    "invalid_missing_arrow.canvas": "'toEnd' is a required property",
}

# Enum-value coverage ratchet. Coverage may RISE freely; a DROP fails.
#
# Not a correctness assertion — it is a review trigger, the same shape as
# KNOWN_DYNAMIC_DISPATCH_SITES in test_registry_consistency.py. A fixture removed or narrowed silently
# shrinks what this suite actually exercises, and nobody would otherwise be told.
#
# ⛔ Do NOT raise this to match a drop. A drop is a finding to investigate.
KNOWN_ENUM_VALUE_COVERAGE = 12

# ⛩ And the ratchet above needs a second half, found by derivation D13c rather than by reasoning.
#
# Deleting BOTH zero-coverage enums outright (`edge.fromEnd`, `edge.styleAttributes.arrow`) left this
# suite at **14 passed**. The coverage ratchet cannot see it: those enums contribute 0 to `covered`,
# so removing them changes nothing it measures. A ratchet on the covered count is blind to the loss of
# exactly the vocabularies it was already failing to exercise — *the blind spot compounds itself.*
#
# So the DECLARED total is pinned too. Adding an enum raises it freely; losing one fails.
KNOWN_DECLARED_ENUM_VALUES = 40
KNOWN_DECLARED_ENUMS = 11


def _fixtures() -> list[Path]:
    found = sorted(FIXTURES.glob("*.canvas"))
    # A glob that finds nothing would make every parametrized test below vacuously absent — pytest
    # reports "no tests ran" for that id rather than a failure, which reads as success in a summary.
    assert len(found) >= 12, f"expected the fixture corpus, found {len(found)} at {FIXTURES}"
    return found


def _validator() -> jsonschema.protocols.Validator:
    return jsonschema.Draft202012Validator(json_schema())


def _enum_pointers(obj: Any, pointer: str = "") -> list[tuple[str, frozenset]]:
    """Every ``enum`` node in the schema, by JSON pointer. Traversed, never listed."""
    out: list[tuple[str, frozenset]] = []
    if isinstance(obj, dict):
        if isinstance(obj.get("enum"), list):
            out.append((pointer or "/", frozenset(v for v in obj["enum"] if v is not None)))
        for k, v in obj.items():
            out += _enum_pointers(v, f"{pointer}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += _enum_pointers(v, f"{pointer}/{i}")
    return out


def _values_used_by_corpus() -> dict[str, set]:
    """What the fixture corpus actually puts on the wire, keyed by the same pointers.

    ⚠ This walk is written against the baseline document shape (``nodes``/``edges`` and their
    ``styleAttributes``), so it covers the eleven non-``reserved`` enums and deliberately not the
    ``_reserved`` ones — those are guarded by the A-* validators and by
    ``test_registry_consistency.py``.
    """
    used: dict[str, set] = {}

    def note(pointer: str, value: Any) -> None:
        if value is not None:
            used.setdefault(pointer, set()).add(value)

    for path in _fixtures():
        doc = json.loads(path.read_text(encoding="utf-8"))
        for n in doc.get("nodes", []):
            note("/$defs/node/properties/type", n.get("type"))
            sa = n.get("styleAttributes") or {}
            for key in ("shape", "border", "textAlign"):
                note(f"/$defs/node/properties/styleAttributes/properties/{key}", sa.get(key))
        for e in doc.get("edges", []):
            for key in ("fromSide", "toSide", "toEnd", "fromEnd"):
                note(f"/$defs/edge/properties/{key}", e.get(key))
            sa = e.get("styleAttributes") or {}
            for key in ("path", "arrow", "pathfindingMethod"):
                note(f"/$defs/edge/properties/styleAttributes/properties/{key}", sa.get(key))
    return used


@pytest.mark.parametrize("fixture", _fixtures(), ids=lambda p: p.name)
def test_fixture_matches_the_published_schema(fixture: Path) -> None:
    """Every fixture validates against the schema — except the ones that must not.

    This is the assertion nothing in the package made before P4b: the schema is not merely *present
    and internally consistent*, it **accepts the documents the Standard says are valid**.
    """
    doc = json.loads(fixture.read_text(encoding="utf-8"))
    errors = sorted(_validator().iter_errors(doc), key=lambda e: list(e.absolute_path))
    expected = EXPECTED_SCHEMA_FAILURES.get(fixture.name)

    if expected is None:
        assert not errors, (
            f"{fixture.name} is a VALID fixture but the published JSON Schema rejects it: "
            f"{[e.message for e in errors]}. Either the schema drifted from the reference validator "
            "(they are two independent copies of one vocabulary — F-DT-7) or this fixture belongs in "
            "EXPECTED_SCHEMA_FAILURES with its reason."
        )
        return

    assert errors, (
        f"{fixture.name} is listed in EXPECTED_SCHEMA_FAILURES as {expected!r} but the schema now "
        "ACCEPTS it. If the fixture was deliberately repaired, remove it from that table; if the "
        "schema was loosened, that is the finding — a constraint the Standard relies on has gone."
    )
    assert any(expected in e.message for e in errors), (
        f"{fixture.name} fails schema validation, but not for its recorded reason. "
        f"expected a message containing {expected!r}; got {[e.message for e in errors]}. "
        "A fixture failing for a NEW reason keeps this table green while meaning something else."
    )


def test_enum_coverage_is_published(capsys: pytest.CaptureFixture[str]) -> None:
    """Publish what this suite actually covers — and ratchet it so it cannot quietly shrink.

    ⛔ **This test passing does not mean the eleven enums are guarded.** It means the corpus did not
    get thinner. The figure below is the honest description of this file's reach, and it is printed
    rather than merely asserted so that a reader of the test output sees the limit next to the pass.
    """
    declared = {
        ptr: members
        for ptr, members in _enum_pointers(json_schema())
        if members and "/$defs/reserved/" not in ptr
    }
    used = _values_used_by_corpus()

    covered = 0
    total = 0
    zero: list[str] = []
    lines: list[str] = []
    for ptr in sorted(declared):
        exercised = declared[ptr] & used.get(ptr, set())
        covered += len(exercised)
        total += len(declared[ptr])
        short = ptr.replace("/$defs/", "").replace("/properties/", ".")
        if not exercised:
            zero.append(short)
        lines.append(f"    {short:<44} {len(exercised):>2}/{len(declared[ptr]):<2} "
                     f"unused={sorted(declared[ptr] - exercised)}")

    with capsys.disabled():
        print(f"\n  schema enum-value coverage by the fixture corpus: {covered}/{total}")
        print("\n".join(lines))
        if zero:
            print(f"    ⛔ ZERO coverage: {zero} — these enums are declared and never exercised")
        print("    ⇒ the corpus IS the coverage. This suite does not guard what it does not use;\n"
              "      the declared-state check in test_registry_consistency.py is what does (F-DT-7).")

    assert covered >= KNOWN_ENUM_VALUE_COVERAGE, (
        f"fixture-corpus enum coverage DROPPED: {covered} < {KNOWN_ENUM_VALUE_COVERAGE}. A fixture "
        "was removed or narrowed, so this suite now exercises less of the schema than it did. "
        "⛔ Do not raise KNOWN_ENUM_VALUE_COVERAGE to match — find out which values were lost. "
        f"currently unexercised-entirely: {zero}"
    )

    # D13c's half: the schema itself must not lose an enum. The coverage number above cannot see this.
    assert len(declared) >= KNOWN_DECLARED_ENUMS and total >= KNOWN_DECLARED_ENUM_VALUES, (
        f"the published JSON Schema has LOST enum constraints: {len(declared)} enums / {total} values, "
        f"was {KNOWN_DECLARED_ENUMS} / {KNOWN_DECLARED_ENUM_VALUES}. Present: {sorted(declared)}. "
        "⛔ This is the F-DT-7 failure mode in its purest form — an enum deleted from a schema whose "
        "consumers are outside this repository. The coverage ratchet above is BLIND to it (a "
        "zero-coverage enum contributes nothing to `covered`, so deleting it changes nothing there), "
        "which is why this assertion exists separately. Do not lower the constants to match."
    )


def test_the_schema_is_not_vacuously_permissive() -> None:
    """Guard the guard: a schema that accepts everything would make every test above pass.

    The fixture table is an argument from examples, and examples cannot distinguish "the schema is
    correct" from "the schema constrains nothing". So: construct a document that is structurally fine
    and carries one illegal enum value, and require the schema to reject it. If `$defs.edge` ever
    loses its `fromSide` enum — F-DT-7's exact failure — this fails even though the corpus, which
    only ever uses "top", would not notice.
    """
    doc = {
        "nodes": [
            {"id": "a", "type": "text", "text": "x", "x": 0, "y": 0, "width": 10, "height": 10},
            {"id": "b", "type": "text", "text": "y", "x": 50, "y": 0, "width": 10, "height": 10},
        ],
        "edges": [
            {"id": "e", "fromNode": "a", "fromSide": "NOT_A_SIDE", "toNode": "b",
             "toSide": "top", "toEnd": "arrow"}
        ],
    }
    errors = [e.message for e in _validator().iter_errors(doc)]
    assert any("NOT_A_SIDE" in m for m in errors), (
        "the published JSON Schema ACCEPTED an illegal `fromSide` value. Either `$defs.edge` lost its "
        f"`fromSide` enum or the enum was widened. Errors reported: {errors}. This is the F-DT-7 "
        "failure mode directly: the schema's consumers are outside this repository, and the fixture "
        "corpus exercises only one of the four legal sides, so nothing else here would catch it."
    )
