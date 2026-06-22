"""B1 — anchor-layer validator (spec_panel_link_semantics §5.3/§6).

Direct unit coverage of ``validate_anchors`` (the well-formedness + reference-resolution branches the golden
fixtures don't each exercise) plus end-to-end checks that the new check rides the aDNA-Native ``validate`` path.
Added with the v2.0.1 errata (LIP queue B1).
"""

from __future__ import annotations

import json
from pathlib import Path

from canvas_std import validate
from canvas_std.reserved import validate_anchors, validate_panel_link
from canvas_std.validate import ConformanceLevel

FIXTURES = Path(__file__).parent / "fixtures"


def _anchored() -> dict:
    return json.loads((FIXTURES / "adna_anchored.canvas").read_text())


# --- well-formed declarations pass -----------------------------------------------------------------
def test_well_formed_anchor_layer_is_clean():
    reserved = {
        "semantic_bindings": {
            "format": {"naming_convention": {"label_form": "legacy", "migration_rule": "x -> y"}},
            "visual": {"orphan_detector": {"mode": "src_cited", "threshold": 0.1}},
        },
        "panel_link": {"anchors": {"Fig 1": "n1"}},
        "component_types": {"cap": {"class": "caption", "qualities": {"ref": "n1"}}},
    }
    assert validate_anchors(reserved, {"n1", "cap"}) == []


def test_empty_and_anchorless_reserved_is_clean():
    assert validate_anchors({}, set()) == []
    assert validate_anchors({"component_types": {"a": {"class": "text"}}}, {"a"}) == []


# --- naming_convention / orphan_detector well-formedness -------------------------------------------
def test_bad_label_form_flagged():
    errs = validate_anchors({"panel_link": {"naming_convention": {"label_form": "fancy"}}}, set())
    assert errs and "label_form" in errs[0]


def test_non_string_migration_rule_flagged():
    errs = validate_anchors({"semantic_bindings": {"format": {"naming_convention": {"migration_rule": 7}}}}, set())
    assert errs and "migration_rule" in errs[0]


def test_bad_orphan_mode_flagged():
    errs = validate_anchors({"semantic_bindings": {"visual": {"orphan_detector": {"mode": "guess"}}}}, set())
    assert errs and "orphan_detector.mode" in errs[0]


def test_threshold_out_of_range_flagged():
    errs = validate_anchors({"semantic_bindings": {"visual": {"orphan_detector": {"threshold": 5}}}}, set())
    assert errs and "threshold" in errs[0]


def test_bool_threshold_rejected():
    # a JSON bool must not slip through the numeric [0,1] check
    assert validate_anchors({"semantic_bindings": {"visual": {"orphan_detector": {"threshold": True}}}}, set())


# --- orphan resolution -----------------------------------------------------------------------------
def test_orphan_component_ref_flagged():
    errs = validate_anchors({"component_types": {"cap": {"class": "caption", "qualities": {"ref": "nope"}}}}, {"cap"})
    assert errs and "missing anchor" in errs[0] and "nope" in errs[0]


def test_component_ref_resolves_against_anchor_label():
    # an explicit reference may point at a declared anchor label, not only a node id
    reserved = {
        "panel_link": {"anchors": {"Fig 1": "n1"}},
        "component_types": {"cap": {"class": "caption", "qualities": {"cites": "Fig 1"}}},
    }
    assert validate_anchors(reserved, {"n1", "cap"}) == []


def test_orphan_anchor_registry_entry_flagged():
    errs = validate_anchors({"panel_link": {"anchors": {"Fig 9": "ghost"}}}, set())
    assert errs and "anchors" in errs[0] and "ghost" in errs[0]


# --- end-to-end: the check rides the aDNA-Native validate() path -----------------------------------
def test_anchored_fixture_valid_end_to_end():
    assert validate(_anchored(), ConformanceLevel.ADNA_NATIVE) == []


def test_orphan_fixture_fails_end_to_end():
    doc = _anchored()
    doc["metadata"]["frontmatter"]["_reserved"]["component_types"]["cap1"]["qualities"]["ref"] = "ghost"
    errs = validate(doc, ConformanceLevel.ADNA_NATIVE)
    assert any("missing anchor" in e for e in errs), errs


# --- AT-1 / AT-2 errata (v2.0.2): extent is optional; surface label is an open vocabulary ----------
# Lock the clarified contract from spec_panel_link_semantics §4/§5.2/§6 (surfaced building the Atelier
# producers). Both pass against current code — they guard against an accidental future tightening.
def test_at1_extent_optional_for_nonpaginated_region():
    # AT-1: a non-paginated single-surface region (e.g. a diagram, pagination: none) omits extent → conformant.
    ok = {"regions": {"g": {"flow": "vertical", "pagination": "none"}}}
    assert validate_panel_link(ok, {"g"}, [], set()) == []
    # optionality is about *absence*, not laxity: a present extent.unit outside the enum still fails.
    bad = {"regions": {"g": {"extent": {"unit": "graphs"}}}}
    assert any("extent.unit" in e for e in validate_panel_link(bad, {"g"}, [], set()))


def test_at2_surface_label_is_open_vocabulary():
    # AT-2: the `surface` subclass label (region surface + surfaces[].surface) is free-form; novel
    # producer tokens (a diagram-type name, "comic_page") must not be rejected.
    block = {
        "regions": {"g": {"surface": "flowchart"}},
        "surfaces": [{"id": "g", "role": "canonical", "surface": "comic_page"}],
    }
    assert validate_panel_link(block, {"g"}, [], set()) == []
