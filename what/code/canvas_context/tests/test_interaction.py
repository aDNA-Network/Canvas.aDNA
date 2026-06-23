"""I-1 / I-2 / I-3 conformance (spec_interface_surface.md §9.1) for the leg-3 interaction overlay.

Negative cases call ``validate_interaction_block`` directly on a mutated doc (graph=None path) — a bad affordance
anchor / kind / value does not break Core validity, so the checks are exercised in isolation.
"""

from __future__ import annotations

import json
from pathlib import Path

from canvas_context import (
    AFFORDANCE_KINDS,
    load_interaction_surface,
    validate_interaction_block,
)

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "interaction_review.canvas"


def _doc() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def _affordances(doc: dict) -> dict:
    return doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["affordances"]


# --- the golden fixture is conformant ---------------------------------------------------------


def test_fixture_loads_and_is_conformant():
    surf = load_interaction_surface(FIXTURE)
    assert surf.is_interactive()
    assert surf.interaction_version == "1.0"
    assert {a.id for a in surf.affordances()} == {"summarize", "approve", "margin_note", "mark_reviewed"}
    # one affordance of each of the four kinds
    assert {a.kind for a in surf.affordances()} == set(AFFORDANCE_KINDS)
    assert surf.validate_interaction() == []


def test_kinds_are_the_closed_set():
    assert AFFORDANCE_KINDS == ("input", "choice", "annotation", "action")


# --- I-1: well-formed overlay ------------------------------------------------------------------


def test_i1_non_interactive_is_vacuously_conformant():
    doc = _doc()
    doc["metadata"]["frontmatter"]["_reserved"].pop("interaction")
    assert validate_interaction_block(doc) == []  # absent interaction == conformant (non-interactive surface)


def test_i1_interaction_version_must_be_semver():
    doc = _doc()
    doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["interaction_version"] = 123
    errs = validate_interaction_block(doc)
    assert any("I-1" in e and "semver" in e for e in errs)


def test_i1_responses_must_be_a_list():
    doc = _doc()
    doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["responses"] = {}
    errs = validate_interaction_block(doc)
    assert any("I-1" in e and "responses must be a list" in e for e in errs)


# --- I-2: anchor resolution + kind + options ---------------------------------------------------


def test_i2_anchor_resolves_both_forms():
    # node-id form (summarize -> summary_box) and label form (mark_reviewed -> status_marker -> status_box)
    surf = load_interaction_surface(FIXTURE)
    assert surf.affordance("summarize").anchor == "summary_box"
    assert surf.affordance("mark_reviewed").anchor == "status_marker"
    assert surf.validate_interaction() == []  # both resolve


def test_i2_orphaned_affordance_rejected():
    doc = _doc()
    _affordances(doc)["summarize"]["anchor"] = "no_such_node"
    errs = validate_interaction_block(doc)
    assert any("I-2" in e and "orphaned affordance" in e for e in errs)


def test_i2_kind_must_be_in_enum():
    doc = _doc()
    _affordances(doc)["summarize"]["kind"] = "freeform"
    errs = validate_interaction_block(doc)
    assert any("I-2" in e and "kind" in e for e in errs)


def test_i2_choice_must_declare_options():
    doc = _doc()
    _affordances(doc)["approve"].pop("options")
    errs = validate_interaction_block(doc)
    assert any("I-2" in e and "options" in e for e in errs)


def test_i2_non_choice_must_not_declare_options():
    doc = _doc()
    _affordances(doc)["margin_note"]["options"] = ["a", "b"]
    errs = validate_interaction_block(doc)
    assert any("I-2" in e and "must not declare options" in e for e in errs)


# --- I-3: response references + value kind-consistency ------------------------------------------


def _with_response(doc: dict, **fields) -> dict:
    doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["responses"].append(fields)
    return doc


def test_i3_response_must_reference_declared_affordance():
    errs = validate_interaction_block(_with_response(_doc(), affordance="ghost", value="x", turn="t1"))
    assert any("I-3" in e and "undeclared affordance" in e for e in errs)


def test_i3_choice_value_must_be_in_options():
    errs = validate_interaction_block(_with_response(_doc(), affordance="approve", value="maybe", turn="t1"))
    assert any("I-3" in e and "not in declared options" in e for e in errs)


def test_i3_action_value_must_be_null():
    errs = validate_interaction_block(_with_response(_doc(), affordance="mark_reviewed", value="done", turn="t1"))
    assert any("I-3" in e and "must carry no value" in e for e in errs)


def test_i3_input_value_must_not_be_null():
    errs = validate_interaction_block(_with_response(_doc(), affordance="summarize", value=None, turn="t1"))
    assert any("I-3" in e and "must not be null" in e for e in errs)


def test_i3_valid_responses_pass():
    doc = _doc()
    _with_response(doc, affordance="summarize", value="A one-line summary.", turn="t1")
    _with_response(doc, affordance="approve", value="approve", turn="t1")
    _with_response(doc, affordance="mark_reviewed", value=None, turn="t1")
    assert validate_interaction_block(doc) == []
