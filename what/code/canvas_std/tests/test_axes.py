"""A-8 conformance for the diagrammatic-context axes (Standard v2.4.0; LIP-0010 Option D).

Two keys on ``_reserved``, both optional, both validated only if present, **two keys or neither**:

- ``authority``  — *who owns the meaning?*   ``dual_channel`` | ``view``
- ``production`` — *how is the picture made?* ``hand_authored`` | ``generated``

Landed at Operation Gridline P1 under the §7.7 signature on LIP-0010 (2026-09-11), which bounds the
firewall touch to Option D's four-file table.

**What these tests are really defending.** Before v2.4.0 the enum was enforced in exactly two places,
both of them Canvas's own producers, and both said so in their error text: *"canvas_std does not
validate this key, so it is checked here or nowhere."* Every other producer in the fleet, and every
hand-authored canvas in 15+ wrapper vaults, could write ``authority: "veiw"`` and get a green ``[OK]``.
The suite below is the difference between a doctrine two modules happen to police and one the Standard
knows.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from canvas_std import strip, validate
from canvas_std.conformance import json_schema, validate_suite
from canvas_std.reserved import AUTHORITY_VALUES, PRODUCTION_VALUES, RESERVED_KEYS
from canvas_std.validate import ConformanceLevel

FIXTURES = Path(__file__).parent / "fixtures"


def _golden() -> dict:
    """The axes golden: ``dual_channel`` AND ``generated`` at once — the state the superseded
    three-value enum could not express, and the reason the axis was split."""
    return json.loads((FIXTURES / "adna_axes.canvas").read_text())


def _plain() -> dict:
    """An aDNA-Native canvas carrying neither key. MUST stay conformant (the majority case:
    21 of 25 in-vault aDNA-Native canvases were in this state when v2.4.0 was cut)."""
    return json.loads((FIXTURES / "adna_native.canvas").read_text())


def _reserved(doc: dict) -> dict:
    return doc["metadata"]["frontmatter"]["_reserved"]


def _native(doc: dict) -> list[str]:
    return validate(doc, ConformanceLevel.ADNA_NATIVE)


def _a8(doc: dict) -> list[str]:
    return [e for e in _native(doc) if e.startswith("A-8")]


# --- the closed sets are the ruled sets -----------------------------------------------------------
def test_the_sets_are_exactly_what_the_ruling_says():
    # Guards against a well-meaning widening. `pattern_diagrammatic_context` (aDNA.aDNA, ruled
    # 2026-09-11) fixes both cells; changing either is a Standard change, not an edit.
    assert AUTHORITY_VALUES == frozenset({"dual_channel", "view"})
    assert PRODUCTION_VALUES == frozenset({"hand_authored", "generated"})


def test_generator_is_not_an_authority_value():
    # The removal IS the ruling. Asserted separately from the set equality above so that a future
    # widening of the authority axis cannot quietly re-admit it.
    assert "generator" not in AUTHORITY_VALUES


def test_both_keys_are_registered_in_the_reserved_namespace():
    # ⚠ RESERVED_KEYS has no consumer (F-GL-1) — this assertion is currently the ONLY thing in the
    # package that reads it. That is deliberate: the append LIP-0010 required is otherwise inert, and
    # an inert list drifts (`interaction` has been missing from it since v2.2.0 for exactly that
    # reason). If the P1 gate question gives the tuple a real consumer, this test stops being its
    # only reader and becomes a redundant-but-cheap belt.
    assert "authority" in RESERVED_KEYS
    assert "production" in RESERVED_KEYS


# --- absent: conformant, and this is the majority case --------------------------------------------
def test_neither_key_is_conformant():
    assert _native(_plain()) == []


def test_neither_key_is_conformant_through_validate_suite():
    # Belt and braces at the level a consumer actually calls: the harness, not just the validator.
    report = validate_suite(_plain())
    assert report.ok
    assert report.level_reached == "adna_native"


# --- present and valid: conformant ----------------------------------------------------------------
def test_the_golden_validates_natively():
    assert _native(_golden()) == []


def test_the_golden_says_dual_channel_and_generated_at_once():
    # The whole point of two axes. Under the superseded single enum this canvas could declare only
    # `dual_channel`, so a reader following the table received no instruction not to hand-edit it.
    r = _reserved(_golden())
    assert r["authority"] == "dual_channel"
    assert r["production"] == "generated"


@pytest.mark.parametrize("authority", sorted(AUTHORITY_VALUES))
@pytest.mark.parametrize("production", sorted(PRODUCTION_VALUES))
def test_every_combination_of_the_two_axes_is_valid(authority: str, production: str):
    # The axes are INDEPENDENT — that independence is the reason there are two of them, so all four
    # cells must pass. A `view` canvas can be hand-authored; a `dual_channel` one can be generated.
    doc = _plain()
    _reserved(doc).update(authority=authority, production=production)
    assert _native(doc) == []


def test_the_axes_are_additive_and_degrade_away():
    # D-1: stripping `_reserved` yields a valid baseline canvas. The axes must not break degradation,
    # which is the round-trip promise the whole fork rests on.
    assert validate(strip(_golden()), ConformanceLevel.CORE) == []


# --- present and invalid: rejected ----------------------------------------------------------------
def test_a_misspelled_authority_is_rejected():
    doc = _golden()
    _reserved(doc)["authority"] = "veiw"
    errors = _a8(doc)
    assert len(errors) == 1
    assert "veiw" in errors[0]


def test_a_misspelled_production_is_rejected():
    doc = _golden()
    _reserved(doc)["production"] = "genarated"
    errors = _a8(doc)
    assert len(errors) == 1
    assert "genarated" in errors[0]


def test_generator_as_authority_is_rejected_and_says_where_it_went():
    """The migration case: 2 of Canvas's own 4 carriers were in this state before Plumbline P1.

    A bare "not in [...]" would be technically correct and useless — the reader's next question is
    always *then where does my value go?*, and the answer is a different key, not a different spelling.
    """
    doc = _golden()
    _reserved(doc)["authority"] = "generator"
    errors = _a8(doc)
    assert len(errors) == 1
    assert "production" in errors[0] and "generated" in errors[0]


# --- the ASYMMETRIC cross-key rule ----------------------------------------------------------------
# ⛩ These four tests were written symmetric ("two keys or neither") and corrected at the Gridline P1
# exit gate (F-GL-5, operator ruling 2026-09-11). The symmetric reading came from LIP-0010's table
# citing "both become binding together" — a sentence about VALIDATION SCOPE, not per-document
# co-presence. It made this vault's own emitters unable to produce a conformant canvas.
def test_authority_alone_is_rejected():
    """⛔ The direction that stops v2.4.0 re-creating the defect it exists to fix.

    A validated `authority` with no `production` would let a canvas be *validly* `dual_channel` while
    omitting the only field that says *do not hand-edit me* — exactly the state the three-value enum
    blessed, and the one thing the cross-key rule is FOR.
    """
    doc = _plain()
    _reserved(doc)["authority"] = "dual_channel"
    errors = _a8(doc)
    assert len(errors) == 1
    assert "REQUIRES" in errors[0]
    assert "production" in errors[0]


def test_production_alone_is_LEGAL():
    """⭐ The converse is conformant, and this test is the whole reason the rule is asymmetric.

    `variant_board.py` and `tuning_surface.py` emit exactly this block — `production: generated` with
    `authority` ABSENT — because a board built from a run manifest has no prose twin and no
    `.lattice.yaml`, so the authority question does not arise. A symmetric rule made their output
    nonconformant and unfixable by regeneration: the only remedy would have been to invent an
    authority value, which `conform.py` names as "passing a value to make a number go green".
    """
    doc = _plain()
    _reserved(doc)["production"] = "generated"
    assert _a8(doc) == []
    assert _native(doc) == []


@pytest.mark.parametrize("production", sorted(PRODUCTION_VALUES))
def test_production_alone_is_legal_for_either_value(production: str):
    # `hand_authored` alone is the documented honest block for a hand-authored primary artifact;
    # `generated` alone is what the two rlhf emitters write. Both must pass.
    doc = _plain()
    _reserved(doc)["production"] = production
    assert _native(doc) == []


def test_authority_alone_AND_misspelled_reports_both_faults():
    # Two independent rules, so two errors — not a short-circuit. A validator that stopped at the
    # first would send the author round the loop twice for one edit.
    doc = _plain()
    _reserved(doc)["authority"] = "veiw"
    errors = _a8(doc)
    assert len(errors) == 2
    assert any("REQUIRES" in e for e in errors)
    assert any("veiw" in e for e in errors)


def test_a_misspelled_production_alone_is_still_caught():
    # Legal SHAPE, illegal VALUE. The asymmetry relaxes the co-presence rule, not membership.
    doc = _plain()
    _reserved(doc)["production"] = "genarated"
    errors = _a8(doc)
    assert len(errors) == 1
    assert "genarated" in errors[0]


# --- the namespace record (F-GL-1) ----------------------------------------------------------------
def test_interaction_is_registered_in_all_the_places_that_list_the_namespace():
    """F-GL-1: `interaction` shipped at v2.2.0 and was missing from all THREE hand-maintained copies
    of the `_reserved` namespace for three months, because nothing read any of them. Back-filled by
    operator ruling 2026-09-11. This test is the reader that stops it happening a fourth time here —
    the spec's §7.2 prose copy has no test and is covered by the dated note in the spec itself."""
    assert "interaction" in RESERVED_KEYS
    assert "interaction" in json_schema()["$defs"]["reserved"]["properties"]


# --- the schema half ------------------------------------------------------------------------------
def test_the_schema_carries_both_enums_and_tracks_2_4_0():
    schema = json_schema()
    reserved = schema["$defs"]["reserved"]["properties"]
    assert reserved["authority"]["enum"] == ["dual_channel", "view"]
    assert reserved["production"]["enum"] == ["hand_authored", "generated"]
    assert schema["x-standard-version"] == "2.4.0"


def test_the_schema_stays_additive_so_older_documents_keep_validating():
    # F-GL-3, asserted rather than remembered: $defs.reserved sets no additionalProperties:false, so
    # adding properties CANNOT invalidate an existing canvas. This is why the $id stays pinned to the
    # v2.0.0 path — the canonical URL keeps its promise. If someone ever closes this object, that is a
    # MAJOR bump and this test is where they find out.
    assert json_schema()["$defs"]["reserved"].get("additionalProperties") is not False
