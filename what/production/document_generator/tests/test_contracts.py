"""E4.2: the LF format/visual contracts are emitted as declarative ``_reserved`` metadata (and only when declared)."""

from __future__ import annotations

import dataclasses
from pathlib import Path

from canvas_std import ConformanceLevel, validate
from canvas_std.reserved import PL_EXTENT_UNITS
from canvas_std.schema import VALID_COLORS

from document_generator.consume import build_document
from document_generator.model import (
    BrandStylePackRef,
    CrossAssetVisual,
    GenreProfile,
    VisualContract,
    load_document,
)

GOLDEN = Path(__file__).resolve().parent / "golden"


def _reserved(doc):
    return doc["metadata"]["frontmatter"]["_reserved"]


def test_no_genre_emits_no_contract_metadata(doc):
    # The bare (no-genre) fixture carries only the base profile — no genre/format/visual/brand keys (E4.1-identical).
    assert _reserved(doc)["semantic_bindings"] == {"profile": "long_document"}
    assert "brand_style_pack_ref" not in _reserved(doc)


def test_format_contract_in_semantic_bindings(whitepaper_doc):
    fmt = _reserved(whitepaper_doc)["semantic_bindings"]["format"]
    assert fmt["length_window"] == {"min": 5000, "max": 15000, "unit": "words"}   # F1
    assert fmt["length_window"]["unit"] in PL_EXTENT_UNITS
    assert fmt["round_trip_surface"] == "latex_source"                            # F5
    assert fmt["asset_conventions"]["table_form"] == "booktabs"                   # F4
    assert any(s["role"] == "canonical" for s in fmt["output_surfaces"])          # F3


def test_output_surfaces_one_canonical_plus_backed_derived(whitepaper_doc):
    pl = _reserved(whitepaper_doc)["panel_link"]
    node_ids = {n["id"] for n in whitepaper_doc["nodes"]}
    canonical = [s for s in pl["surfaces"] if s.get("role") == "canonical"]
    assert len(canonical) == 1 and canonical[0]["id"] == "doc_root"               # A-5
    assert all(s["id"] in node_ids for s in pl["surfaces"])                       # every surface id resolves to a node
    derived = [s for s in pl["surfaces"] if s.get("role") == "derived"]
    assert derived and all(s["id"].startswith("surface_") for s in derived)


def test_visual_per_asset_qualities_on_figures(whitepaper_doc):
    figs = [e.get("qualities", {}) for e in _reserved(whitepaper_doc)["component_types"].values()
            if e["class"] == "image"]
    assert figs
    # genre default: a generated canvas figure routes TikZ -> CanvasForge with the cycle-22 5-criteria scorecard
    assert any(q.get("producer_tool") == "TikZ" and q.get("engine_route") == "CanvasForge" for q in figs)
    assert any(q.get("scorecard", {}).get("n") == 5 for q in figs)
    # the per-figure override (Figure 2): a captured external social_card, not the genre canvas/generated default
    assert any(q.get("origin") == "captured" and q.get("intent_class") == "social_card" for q in figs)


def test_caption_form_override_emitted_only_when_non_default(whitepaper_doc):
    caps = [e.get("qualities") or {} for e in _reserved(whitepaper_doc)["component_types"].values()
            if e["class"] == "caption"]
    assert any(c.get("caption_form") == "claim_form" for c in caps)   # Figure 2 override (V6)
    assert any("caption_form" not in c for c in caps)                 # descriptive captions stay un-annotated


def test_visual_cross_asset_in_semantic_bindings(whitepaper_doc):
    vis = _reserved(whitepaper_doc)["semantic_bindings"]["visual"]
    assert vis["engine_map"]                                          # X1
    assert vis["orphan_detector"]["mode"] == "label_ref"             # X2
    assert vis["style_lock"]["kind"] == "internal"                   # X5
    assert "figure_text_coherence" in vis["visual_voices"]           # X10


def test_brand_style_pack_ref_present_when_set_else_omitted(whitepaper_doc):
    # Whitepaper uses an internal style-lock -> no brand pack -> dedicated reserved key omitted.
    assert "brand_style_pack_ref" not in _reserved(whitepaper_doc)
    # A genre that sets a brand pack (X3) -> emitted into the dedicated _reserved.brand_style_pack_ref key.
    branded = GenreProfile(name="branded", visual_spec=VisualContract(cross=CrossAssetVisual(
        brand_style_pack_ref=BrandStylePackRef(vault="ScienceStanley.aDNA", pack_id="ss_core", version="1.0.0"))))
    doc = build_document(dataclasses.replace(load_document(GOLDEN / "document_small.yaml"), genre=branded))
    assert _reserved(doc)["brand_style_pack_ref"] == {"vault": "ScienceStanley.aDNA", "pack_id": "ss_core",
                                                      "version": "1.0.0"}


def test_color_signal_vocabulary_recorded_but_never_applied_to_node_color():
    # PT-P5 guard: signal colors are recorded as a vocabulary in semantic_bindings, NEVER painted onto node `color`
    # (which must stay a valid slot / #-hex). A signal NAME like "amber" must not leak onto any node.
    signal = GenreProfile(name="signal", visual_spec=VisualContract(cross=CrossAssetVisual(
        color_signal_vocabulary={"ok": "green", "warn": "amber", "error": "red"})))
    doc = build_document(dataclasses.replace(load_document(GOLDEN / "document_small.yaml"), genre=signal))
    assert _reserved(doc)["semantic_bindings"]["visual"]["color_signal_vocabulary"]["warn"] == "amber"
    for n in doc["nodes"]:
        if "color" in n:
            assert n["color"] in VALID_COLORS or str(n["color"]).startswith("#")
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_grant_form_fill_exemption_and_template(grant_doc):
    sb = _reserved(grant_doc)["semantic_bindings"]
    assert sb["visual"]["form_fill_exemption"] is True                                   # X13
    assert sb["format"]["format_template_ref"] == {"owner": "funder", "template_id": "NIH-R01",
                                                   "resolver": "structured_form"}         # F6
    assert sb["format"]["asset_conventions"]["figure_placement"] == "n/a (form-bypass)"  # F4 (content-not-placement)
