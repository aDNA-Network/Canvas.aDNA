"""Components: image + table classes (which brief_consumer didn't exercise) carry + degrade faithfully."""

from __future__ import annotations

from canvas_std.reserved import BASELINE_TYPES, COMPONENT_CLASSES


def _comps(doc):
    return doc["metadata"]["frontmatter"]["_reserved"]["component_types"]


def test_image_components_degrade(doc):
    by_id = {n["id"]: n for n in doc["nodes"]}
    images = {nid: e for nid, e in _comps(doc).items() if e["class"] == "image"}
    assert images, "expected at least one image component"
    seen_file = seen_link = False
    for nid, entry in images.items():
        node = by_id[nid]
        if entry["degrades_to"] == "file":
            assert node["type"] == "file" and "file" in node
            seen_file = True
        else:
            assert entry["degrades_to"] == "link" and node["type"] == "link" and "url" in node
            seen_link = True
    assert seen_file and seen_link  # the fixture covers both a vault-path and an external-url image


def test_table_component_degrades(doc):
    by_id = {n["id"]: n for n in doc["nodes"]}
    tables = {nid: e for nid, e in _comps(doc).items() if e["class"] == "table"}
    assert tables, "expected a table component"
    for nid, entry in tables.items():
        assert entry["degrades_to"] == "text"
        assert by_id[nid]["type"] == "text"
        assert "|" in by_id[nid]["text"]  # rendered markdown table
        assert entry["qualities"]["col_count"] >= 1


def test_all_component_classes_and_degrades_are_valid(doc):
    for nid, entry in _comps(doc).items():
        assert entry["class"] in COMPONENT_CLASSES, f"{nid}: bad class {entry['class']}"
        assert entry["degrades_to"] in BASELINE_TYPES, f"{nid}: bad degrades_to {entry['degrades_to']}"
