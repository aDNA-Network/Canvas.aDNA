"""Degradation: stripping _reserved yields a valid baseline (Obsidian) canvas — and NO shape-enum overload."""

from __future__ import annotations

from canvas_std import ConformanceLevel, degradation_report, strip, validate

from diagram_generator.consume import build_diagram


def test_degradation_report_all_pass(doc):
    assert degradation_report(doc) == {"D-1": True, "D-2": True, "D-3": True}


def test_strip_is_core_and_extended_valid(doc):
    bare = strip(doc)
    assert validate(bare, ConformanceLevel.CORE) == []
    assert validate(bare, ConformanceLevel.EXTENDED) == []


def test_strip_removes_reserved(doc):
    bare = strip(doc)
    assert "_reserved" not in bare.get("metadata", {}).get("frontmatter", {})


def test_no_out_of_enum_shape_attribute(doc):
    """The shape-enum trap: the Mermaid shape rides ONLY in _reserved.qualities.shape — NO baseline node may carry a
    styleAttributes.shape (the canvas VALID_SHAPES enum lacks rect/round/stadium; setting it fails E-2/D-2)."""
    for n in doc["nodes"]:
        assert "shape" not in n.get("styleAttributes", {}), f"node {n['id']} leaked a styleAttributes.shape"


def test_no_shape_attribute_across_all_types(all_types):
    for name, d in all_types.items():
        doc = build_diagram(d)
        for n in doc["nodes"]:
            assert "shape" not in n.get("styleAttributes", {}), f"{name}: node {n['id']} leaked styleAttributes.shape"
        assert degradation_report(doc) == {"D-1": True, "D-2": True, "D-3": True}, name
