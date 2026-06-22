"""Conformance: the post validates at aDNA-Native — the whole post/thread is one region under one canonical surface."""

from __future__ import annotations

from pathlib import Path

from canvas_std import ConformanceLevel, validate, validate_suite

from post_generator.consume import ROOT_ID, build_post
from post_generator.model import load_post


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
    assert set(pl["regions"]) == {ROOT_ID}


def test_component_types_resolve(doc):
    node_ids = {n["id"] for n in doc["nodes"]}
    assert set(doc["metadata"]["frontmatter"]["_reserved"]["component_types"]).issubset(node_ids)


def test_single_post_conforms(single_post):
    assert validate(build_post(single_post), ConformanceLevel.ADNA_NATIVE) == []


def test_examples_build_and_conform():
    examples = Path(__file__).resolve().parents[1] / "examples"
    for name in ("example_post_single.yaml", "example_post_thread.yaml"):
        doc = build_post(load_post(examples / name))
        assert validate(doc, ConformanceLevel.ADNA_NATIVE) == [], name
