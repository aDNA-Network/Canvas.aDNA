"""Components: shape nodes carry qualities.shape + degrade to text; mermaid_src is the code/text class."""

from __future__ import annotations

from canvas_std.reserved import BASELINE_TYPES, COMPONENT_CLASSES

from diagram_generator.model import NODE_SHAPES


def _comps(doc):
    return doc["metadata"]["frontmatter"]["_reserved"]["component_types"]


def test_shape_components_carry_qualities_and_degrade(doc):
    by_id = {n["id"]: n for n in doc["nodes"]}
    shapes = {nid: e for nid, e in _comps(doc).items() if e["class"] == "shape"}
    assert shapes, "expected at least one shape component"
    for nid, entry in shapes.items():
        assert entry["degrades_to"] == "text"
        assert by_id[nid]["type"] == "text"  # the baseline node degrades to text
        assert entry["qualities"]["shape"] in NODE_SHAPES  # the Mermaid shape rides in qualities
        assert "shape" not in by_id[nid].get("styleAttributes", {})  # never on the baseline node


def test_mermaid_src_is_code_class(doc):
    by_id = {n["id"]: n for n in doc["nodes"]}
    entry = _comps(doc)["mermaid_src"]
    assert entry["class"] == "code"
    assert entry["degrades_to"] == "text"
    assert entry["qualities"]["language"] == "mermaid"
    node = by_id["mermaid_src"]
    assert node["type"] == "text"  # a code node degrades to a text node
    assert "```mermaid" in node["text"]  # carries the generated Mermaid source


def test_root_is_panel_degrading_to_group(doc):
    by_id = {n["id"]: n for n in doc["nodes"]}
    entry = _comps(doc)["diagram_root"]
    assert entry["class"] == "panel"
    assert entry["degrades_to"] == "group"
    assert by_id["diagram_root"]["type"] == "group"


def test_all_component_classes_and_degrades_are_valid(doc):
    for nid, entry in _comps(doc).items():
        assert entry["class"] in COMPONENT_CLASSES, f"{nid}: bad class {entry['class']}"
        assert entry["degrades_to"] in BASELINE_TYPES, f"{nid}: bad degrades_to {entry['degrades_to']}"
