"""Conformance: the diagram validates at aDNA-Native, the whole graph as one region under one canonical surface."""

from __future__ import annotations

from pathlib import Path

from canvas_std import ConformanceLevel, validate, validate_suite

from diagram_generator.consume import build_diagram
from diagram_generator.model import load_diagram


def test_validates_adna_native(doc):
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_suite_meets_declared_adna_native(doc):
    report = validate_suite(doc, ConformanceLevel.ADNA_NATIVE)
    assert report.failed == []
    assert report.meets_declared is True
    assert report.level_reached == ConformanceLevel.ADNA_NATIVE
    assert report.ok is True


def test_one_canonical_surface_and_single_region(doc):
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    pl = reserved["panel_link"]
    canonical = [s for s in pl["surfaces"] if s.get("role") == "canonical"]
    assert len(canonical) == 1  # the A-5 load-bearing constraint
    assert canonical[0]["id"] == "diagram_root"
    # exactly one region — the diagram_root group (the whole diagram is one surface)
    assert set(pl["regions"]) == {"diagram_root"}
    assert pl["regions"]["diagram_root"]["flow"] in ("vertical", "horizontal")


def test_component_types_resolve(doc):
    node_ids = {n["id"] for n in doc["nodes"]}
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    assert set(reserved["component_types"]).issubset(node_ids)


def test_example_yaml_builds_and_conforms():
    example = Path(__file__).resolve().parents[1] / "examples" / "canvas_standard_flow.yaml"
    doc = build_diagram(load_diagram(example))
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []
    # the canonical surface group is present
    groups = [n for n in doc["nodes"] if n["type"] == "group" and n["id"] == "diagram_root"]
    assert len(groups) == 1
