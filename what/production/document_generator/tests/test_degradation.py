"""Degradation: stripping _reserved yields a valid baseline (Obsidian) canvas — incl. isStartNode + heading color."""

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


def test_start_node_survives_strip(doc):
    bare = strip(doc)
    start = [n for n in bare["nodes"] if n.get("isStartNode") is True]
    assert len(start) == 1 and start[0]["id"] == "page0"  # Extended field, valid post-strip
