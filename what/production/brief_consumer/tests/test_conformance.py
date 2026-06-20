"""Conformance: the consumer's output validates at aDNA-Native (canvas_std A-* checks)."""

from __future__ import annotations

from pathlib import Path

from canvas_std import ConformanceLevel, validate, validate_suite

from brief_consumer.consume import build_brief
from brief_consumer.model import load_brief


def test_validates_adna_native(doc):
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_suite_meets_declared_adna_native(doc):
    report = validate_suite(doc, ConformanceLevel.ADNA_NATIVE)
    assert report.failed == []
    assert report.meets_declared is True
    assert report.level_reached == ConformanceLevel.ADNA_NATIVE
    assert report.ok is True


def test_reserved_block_well_formed(doc):
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    assert reserved["adna_version"] == "2.0.0"
    assert reserved["conformance_level"] == "adna_native"

    # exactly one canonical surface, resolving to a node
    node_ids = {n["id"] for n in doc["nodes"]}
    canonical = [s for s in reserved["panel_link"]["surfaces"] if s.get("role") == "canonical"]
    assert len(canonical) == 1
    assert canonical[0]["id"] in node_ids

    # every component_types key resolves to a node
    assert set(reserved["component_types"]).issubset(node_ids)


def test_example_yaml_builds_and_conforms():
    """The shipped self-referential dog-food input builds + conforms at aDNA-Native."""
    example = Path(__file__).resolve().parents[1] / "examples" / "canvas_standard_brief.yaml"
    doc = build_brief(load_brief(example))
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []
    # 5 sections -> 5 headings + 5 bodies + 3 sources + 1 page = 14 nodes
    assert len(doc["nodes"]) == 14
