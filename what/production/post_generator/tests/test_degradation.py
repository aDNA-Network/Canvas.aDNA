"""Degradation: stripping _reserved yields a valid baseline (Obsidian) canvas at CORE + EXTENDED."""

from __future__ import annotations

from canvas_std import ConformanceLevel, degradation_report, strip, validate


def test_degradation_report_all_pass(doc):
    assert degradation_report(doc) == {"D-1": True, "D-2": True, "D-3": True}


def test_strip_is_core_and_extended_valid(doc):
    bare = strip(doc)
    assert validate(bare, ConformanceLevel.CORE) == []
    assert validate(bare, ConformanceLevel.EXTENDED) == []


def test_strip_removes_reserved(doc):
    bare = strip(doc)
    assert "_reserved" not in bare.get("metadata", {}).get("frontmatter", {})


def test_baseline_node_types_valid(doc):
    """Every node is a baseline type — the image node degrades to text (no out-of-enum baseline leaked)."""
    baseline = {"text", "file", "group", "link"}
    for n in doc["nodes"]:
        assert n["type"] in baseline, f"node {n['id']} has non-baseline type {n['type']!r}"
