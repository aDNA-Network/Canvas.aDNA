"""Conformance: the deck validates at aDNA-Native, with slides as regions under one canonical surface."""

from __future__ import annotations

from pathlib import Path

from canvas_std import ConformanceLevel, validate, validate_suite

from deck_generator.consume import build_deck
from deck_generator.model import load_deck


def test_validates_adna_native(doc):
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_suite_meets_declared_adna_native(doc):
    report = validate_suite(doc, ConformanceLevel.ADNA_NATIVE)
    assert report.failed == []
    assert report.meets_declared is True
    assert report.level_reached == ConformanceLevel.ADNA_NATIVE
    assert report.ok is True


def test_one_canonical_surface_and_regions_per_slide(doc, n_slides):
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    pl = reserved["panel_link"]
    canonical = [s for s in pl["surfaces"] if s.get("role") == "canonical"]
    assert len(canonical) == 1  # the A-5 load-bearing constraint
    assert canonical[0]["id"] == "deck_root"
    # one region per slide group
    slide_groups = [n["id"] for n in doc["nodes"]
                    if n["type"] == "group" and n["id"].startswith("slide")]
    assert len(slide_groups) == n_slides
    assert set(pl["regions"]) == set(slide_groups)
    assert all(r["extent"]["unit"] == "slides" for r in pl["regions"].values())


def test_component_types_resolve(doc):
    node_ids = {n["id"] for n in doc["nodes"]}
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    assert set(reserved["component_types"]).issubset(node_ids)


def test_example_yaml_builds_and_conforms():
    example = Path(__file__).resolve().parents[1] / "examples" / "canvas_standard_deck.yaml"
    doc = build_deck(load_deck(example))
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []
    slide_groups = [n for n in doc["nodes"] if n["type"] == "group" and n["id"].startswith("slide")]
    assert len(slide_groups) == 6
