"""Conformance: the letter validates at aDNA-Native — the whole letter is one region under one canonical surface."""

from __future__ import annotations

from pathlib import Path

from canvas_std import ConformanceLevel, validate, validate_suite

from letter_generator.consume import ROOT_ID, build_letter
from letter_generator.model import load_letter


def test_validates_adna_native(doc):
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_suite_meets_declared_adna_native(doc):
    report = validate_suite(doc, ConformanceLevel.ADNA_NATIVE)
    assert report.failed == []
    assert report.meets_declared is True
    assert report.level_reached == ConformanceLevel.ADNA_NATIVE
    assert report.ok is True


def test_one_canonical_surface_and_single_region(doc):
    pl = doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]
    canonical = [s for s in pl["surfaces"] if s.get("role") == "canonical"]
    assert len(canonical) == 1  # the A-5 load-bearing constraint
    assert canonical[0]["id"] == ROOT_ID
    assert set(pl["regions"]) == {ROOT_ID}  # the whole letter is one surface
    assert pl["regions"][ROOT_ID]["flow"] == "vertical"


def test_component_types_resolve(doc):
    node_ids = {n["id"] for n in doc["nodes"]}
    assert set(doc["metadata"]["frontmatter"]["_reserved"]["component_types"]).issubset(node_ids)


def test_example_yaml_builds_and_conforms():
    example = Path(__file__).resolve().parents[1] / "examples" / "example_letter.yaml"
    doc = build_letter(load_letter(example))
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []
    groups = [n for n in doc["nodes"] if n["type"] == "group" and n["id"] == ROOT_ID]
    assert len(groups) == 1
