"""Conformance: the document validates at aDNA-Native, with pages as regions under one canonical surface."""

from __future__ import annotations

from pathlib import Path

from canvas_std import ConformanceLevel, validate, validate_suite

from document_generator.consume import build_document
from document_generator.model import load_document


def test_validates_adna_native(doc):
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_suite_meets_declared_adna_native(doc):
    report = validate_suite(doc, ConformanceLevel.ADNA_NATIVE)
    assert report.failed == []
    assert report.meets_declared is True
    assert report.level_reached == ConformanceLevel.ADNA_NATIVE
    assert report.ok is True


def test_one_canonical_surface_and_region_per_page(doc, n_pages):
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    pl = reserved["panel_link"]
    canonical = [s for s in pl["surfaces"] if s.get("role") == "canonical"]
    assert len(canonical) == 1  # the A-5 load-bearing constraint
    assert canonical[0]["id"] == "doc_root"
    page_groups = [n["id"] for n in doc["nodes"] if n["type"] == "group" and n["id"].startswith("page")]
    assert len(page_groups) == n_pages
    # every page has its own region (extent in pages); the doc_root region carries the document words-extent
    assert set(page_groups).issubset(set(pl["regions"]))
    assert all(pl["regions"][pid]["extent"]["unit"] == "pages" for pid in page_groups)
    assert pl["regions"]["doc_root"]["extent"]["unit"] == "words"


def test_component_types_resolve(doc):
    node_ids = {n["id"] for n in doc["nodes"]}
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    assert set(reserved["component_types"]).issubset(node_ids)


def test_example_yaml_builds_and_conforms():
    example = Path(__file__).resolve().parents[1] / "examples" / "canvas_standard_whitepaper.yaml"
    doc = build_document(load_document(example))
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []
    page_groups = [n for n in doc["nodes"] if n["type"] == "group" and n["id"].startswith("page")]
    assert len(page_groups) == 2
