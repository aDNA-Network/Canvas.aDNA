"""L1–L7 load-pipeline tests (spec_canvas_context_loading §4) against the canvas_std golden fixtures."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import canvas_std
import pytest

from canvas_context import CoreValidationError, load_context_graph

HERE = Path(__file__).resolve().parent
STD_FIXTURES = HERE.parent.parent / "canvas_std" / "tests" / "fixtures"
ADNA_NATIVE = STD_FIXTURES / "adna_native.canvas"


def _adna_native_doc() -> dict:
    return json.loads(ADNA_NATIVE.read_text())


# --- L1: parse & validate; refuse Core-invalid -------------------------------------------------


def test_l1_refuses_core_invalid_document():
    """A dangling edge endpoint is a Core (C-3) failure → the loader MUST refuse (spec §4 L1)."""
    bad = {
        "nodes": [],
        "edges": [{"id": "e1", "fromNode": "x", "toNode": "y", "fromSide": "bottom", "toSide": "top", "toEnd": "arrow"}],
    }
    with pytest.raises(CoreValidationError):
        load_context_graph(bad)


def test_l1_records_declared_and_reached_levels():
    g = load_context_graph(_adna_native_doc())
    c = g.conformance()
    assert c["declared"] == "adna_native"
    assert c["reached"] == "adna_native"


# --- L2 / §8: baseline graph + degradation on a _reserved-stripped canvas -----------------------


def test_l2_baseline_loads_on_stripped_canvas():
    """Strip _reserved → a plain baseline canvas still loads (L2 must succeed; §8 degradation)."""
    bare = canvas_std.strip(_adna_native_doc())
    g = load_context_graph(bare)
    assert g.identity()["id"] is None  # no context_object after strip — identity is null, never fabricated (L4)
    assert len(g.components()) == 4
    assert any(r.id == "intro_body" for r in g.relations())
    # baseline payload + advisory geometry survive
    intro = g.component("intro")
    assert intro.payload.get("text") == "# Greeting"
    assert intro.geometry.get("width") == 280


# --- L3: additive _reserved overlay ------------------------------------------------------------


def test_l3_overlays_reserved_semantics():
    g = load_context_graph(_adna_native_doc())
    intro = g.component("intro")
    assert intro.component_class == "typography_run"
    assert intro.semantic_type == "heading"
    assert intro.degrades_to == "text"
    # panel region overlay
    page1 = g.panel("page1")
    assert page1 is not None
    assert page1.flow == "vertical"
    assert page1.pagination == "paged"
    assert page1.surface == "letter"
    # edge kind overlay
    rel = next(r for r in g.relations() if r.id == "intro_body")
    assert rel.kind == "reading_order"


def test_l3_unannotated_nodes_keep_baseline_stub():
    """A node without a component_types entry MUST retain its L2 baseline (no silent drop, §4 L3)."""
    g = load_context_graph(_adna_native_doc())
    meta = g.component("_lattice_meta")  # not in component_types
    assert meta is not None
    assert meta.node_type == "group"
    assert meta.component_class is None


# --- L4: context identity ----------------------------------------------------------------------


def test_l4_resolves_context_identity():
    g = load_context_graph(_adna_native_doc())
    assert g.identity() == {"id": "urn:adna:canvas:example_doc", "version": "0.1.0"}
    assert g.summary() is None  # absent in the fixture — exposed as null, gracefully


# --- L5: classify & expose references ----------------------------------------------------------


def test_l5_classifies_refs_wikilink_and_federation():
    doc = {
        "nodes": [],
        "edges": [],
        "metadata": {
            "frontmatter": {
                "_reserved": {
                    "context_object": {"id": "urn:x", "refs": ["lattice://inst/lat", "[[foo]]"]}
                }
            }
        },
    }
    g = load_context_graph(doc, validate=False)
    forms = {(r.form, r.target) for r in g.refs()}
    assert ("federation_ref", "lattice://inst/lat") in forms
    assert ("wikilink", "[[foo]]") in forms


def test_l5_discovers_inline_wikilinks_in_text():
    doc = {
        "nodes": [{"id": "n1", "type": "text", "text": "see [[other_spec]] and [[third]]"}],
        "edges": [],
        "metadata": {"frontmatter": {"_reserved": {"context_object": {"id": "urn:x", "refs": []}}}},
    }
    g = load_context_graph(doc, validate=False)
    targets = {r.target for r in g.refs()}
    assert "[[other_spec]]" in targets
    assert "[[third]]" in targets


# --- L6: advisory staleness --------------------------------------------------------------------


def test_l6_flags_stale_when_hash_mismatches():
    """The golden fixture carries a placeholder sync_hash → recompute mismatches → stale flag set (advisory)."""
    g = load_context_graph(_adna_native_doc())
    assert g.conformance()["stale"] is True


def test_l6_not_stale_when_hash_matches():
    doc = _adna_native_doc()
    doc["metadata"]["frontmatter"]["_reserved"]["sync"]["sync_hash"] = canvas_std.compute_sync_hash(doc)
    g = load_context_graph(doc)
    assert g.conformance()["stale"] is False


def test_l6_no_sync_block_is_not_stale():
    bare = canvas_std.strip(_adna_native_doc())  # no _reserved → no sync → not stale
    assert load_context_graph(bare).conformance()["stale"] is False


# --- L7: no rendering --------------------------------------------------------------------------


def test_l7_no_rendering_libraries_imported():
    import sys

    load_context_graph(_adna_native_doc())
    assert "PIL" not in sys.modules
    assert "cairosvg" not in sys.modules


# --- accepts a parsed dict or a path -----------------------------------------------------------


def test_loads_from_path_and_from_dict_equivalently():
    from_path = load_context_graph(ADNA_NATIVE)
    from_dict = load_context_graph(_adna_native_doc())
    assert from_path.identity() == from_dict.identity()
    assert len(from_path.components()) == len(from_dict.components())


def test_load_does_not_mutate_source_dict():
    doc = _adna_native_doc()
    before = copy.deepcopy(doc)
    load_context_graph(doc, validate=False)
    assert doc == before  # read-only — no mutation of the source (§6)
