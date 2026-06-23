"""I-1 / I-2 / I-3 conformance for the leg-3 interaction overlay (spec_interface_surface §9.1).

Wired into the aDNA-Native ``validate()`` path at Operation Armature P2 (``adr_007`` — the first leg-3 touch of the
harness). Covers: the interaction golden validates natively and degrades to a Core baseline (D-1, additive layer);
I-1/I-2/I-3 fail the right way through ``validate()``; the anchor substrate is not double-validated (R1); and the
``canvas-std`` CLI validates an interaction-bearing canvas (``adr_007`` Positive #1).
"""

from __future__ import annotations

import json
from pathlib import Path

from canvas_std import strip, validate, validate_interaction
from canvas_std.conformance import _cli
from canvas_std.reserved import AFFORDANCE_KINDS
from canvas_std.validate import ConformanceLevel

FIXTURES = Path(__file__).parent / "fixtures"


def _golden() -> dict:
    return json.loads((FIXTURES / "adna_interaction.canvas").read_text())


def _interaction(doc: dict) -> dict:
    return doc["metadata"]["frontmatter"]["_reserved"]["interaction"]


def _affordances(doc: dict) -> dict:
    return _interaction(doc)["affordances"]


def _with_response(doc: dict, **fields) -> dict:
    _interaction(doc)["responses"].append(fields)
    return doc


# --- the golden validates natively + degrades to baseline ----------------------------------------
def test_kinds_are_the_closed_set():
    assert AFFORDANCE_KINDS == ("input", "choice", "annotation", "action")


def test_golden_is_valid_adna_native_end_to_end():
    # I-* now rides the aDNA-Native validate() path — the golden validates with no consumer code, and its
    # label-form affordance (mark_reviewed -> "status_marker") resolves via panel_link.anchors (the doc path).
    assert validate(_golden(), ConformanceLevel.ADNA_NATIVE) == []
    assert {a["kind"] for a in _affordances(_golden()).values()} == set(AFFORDANCE_KINDS)


def test_golden_degrades_to_core_baseline():
    # D-1 (spec_interface_surface §8.2): strip removes the whole _reserved incl. interaction -> valid Core canvas.
    assert validate(strip(_golden()), ConformanceLevel.CORE) == []


# --- I-1: well-formed overlay --------------------------------------------------------------------
def test_i1_non_interactive_is_vacuously_conformant():
    doc = _golden()
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    reserved.pop("interaction")
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []  # a non-interactive surface is still valid
    assert validate_interaction(reserved, doc) == []


def test_i1_interaction_version_must_be_semver():
    doc = _golden()
    _interaction(doc)["interaction_version"] = 123
    assert any("I-1" in e and "semver" in e for e in validate(doc, ConformanceLevel.ADNA_NATIVE))


def test_i1_two_part_interaction_version_is_accepted():
    # 2-part-tolerant ("1.0") — distinct from the 3-part adna_version semver (R3).
    doc = _golden()
    _interaction(doc)["interaction_version"] = "1.0"
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_i1_responses_must_be_a_list():
    doc = _golden()
    _interaction(doc)["responses"] = {}
    assert any("responses must be a list" in e for e in validate(doc, ConformanceLevel.ADNA_NATIVE))


# --- I-2: anchor resolution + kind + options -----------------------------------------------------
def test_i2_orphaned_affordance_rejected():
    doc = _golden()
    _affordances(doc)["summarize"]["anchor"] = "no_such_node"
    assert any("I-2" in e and "orphaned affordance" in e for e in validate(doc, ConformanceLevel.ADNA_NATIVE))


def test_i2_kind_must_be_in_enum():
    doc = _golden()
    _affordances(doc)["summarize"]["kind"] = "freeform"
    assert any("I-2" in e and "kind" in e for e in validate(doc, ConformanceLevel.ADNA_NATIVE))


def test_i2_choice_must_declare_options():
    doc = _golden()
    _affordances(doc)["approve"].pop("options")
    assert any("I-2" in e and "options" in e for e in validate(doc, ConformanceLevel.ADNA_NATIVE))


# --- I-3: response references + value kind-consistency --------------------------------------------
def test_i3_response_must_reference_declared_affordance():
    errs = validate(_with_response(_golden(), affordance="ghost", value="x", turn="t1"), ConformanceLevel.ADNA_NATIVE)
    assert any("I-3" in e and "undeclared affordance" in e for e in errs)


def test_i3_action_value_must_be_null():
    errs = validate(_with_response(_golden(), affordance="mark_reviewed", value="done", turn="t1"), ConformanceLevel.ADNA_NATIVE)
    assert any("I-3" in e and "must carry no value" in e for e in errs)


def test_i3_valid_responses_pass():
    doc = _golden()
    _with_response(doc, affordance="summarize", value="A one-line summary.", turn="t1")
    _with_response(doc, affordance="approve", value="approve", turn="t1")
    _with_response(doc, affordance="mark_reviewed", value=None, turn="t1")
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


# --- R1: the anchor substrate is not double-validated --------------------------------------------
def test_anchor_orphan_emits_a_single_a5_not_duplicated():
    # validate_interaction must NOT re-run validate_anchors (validate_reserved already does). A malformed anchor
    # registry entry yields exactly one A-5 through the full path, never two.
    doc = _golden()
    doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]["anchors"]["status_marker"] = "ghost_node"
    a5 = [e for e in validate(doc, ConformanceLevel.ADNA_NATIVE) if "A-5" in e and "ghost_node" in e]
    assert len(a5) == 1, a5


# --- the canvas-std CLI validates an interaction-bearing canvas (adr_007 Positive #1) -------------
def test_cli_validates_the_interaction_golden():
    assert _cli(["validate", str(FIXTURES / "adna_interaction.canvas")]) == 0


def test_cli_rejects_an_orphaned_affordance(tmp_path):
    doc = _golden()
    _affordances(doc)["summarize"]["anchor"] = "no_such_node"
    bad = tmp_path / "orphan_interaction.canvas"
    bad.write_text(json.dumps(doc))
    assert _cli(["validate", str(bad), "--level", "adna_native"]) == 1
