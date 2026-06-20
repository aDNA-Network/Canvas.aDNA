"""Components: the long-form element set — incl. the `code` class (first consumer to exercise it) — degrades faithfully."""

from __future__ import annotations

from canvas_std.reserved import BASELINE_TYPES, COMPONENT_CLASSES


def _comps(doc):
    return doc["metadata"]["frontmatter"]["_reserved"]["component_types"]


def test_code_component_degrades(doc):
    by_id = {n["id"]: n for n in doc["nodes"]}
    codes = {nid: e for nid, e in _comps(doc).items() if e["class"] == "code"}
    assert codes, "expected a code component (E4.1 is the first consumer to exercise `code`)"
    for nid, entry in codes.items():
        assert entry["degrades_to"] == "text"
        assert by_id[nid]["type"] == "text"
        assert "```" in by_id[nid]["text"]  # rendered as a fenced code block


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
    assert seen_file and seen_link  # the fixture covers both a vault-path and an external-url figure


def test_table_component_degrades(doc):
    by_id = {n["id"]: n for n in doc["nodes"]}
    tables = {nid: e for nid, e in _comps(doc).items() if e["class"] == "table"}
    assert tables, "expected a table component"
    for nid, entry in tables.items():
        assert entry["degrades_to"] == "text"
        assert by_id[nid]["type"] == "text"
        assert "|" in by_id[nid]["text"]  # rendered markdown table
        assert entry["qualities"]["col_count"] >= 1


def test_long_form_classes_and_semantics_present(doc):
    comps = _comps(doc)
    classes = {e["class"] for e in comps.values()}
    assert {"panel", "typography_run", "caption", "table", "code", "link", "image"}.issubset(classes)
    # blockquote + list ride on a `text` node carrying a semantic_type (no dedicated class — see erratum note)
    semantics = {e.get("semantic_type") for e in comps.values()}
    assert {"document", "page", "heading", "figure", "quote", "list", "citation"}.issubset(semantics)


def test_all_component_classes_and_degrades_are_valid(doc):
    for nid, entry in _comps(doc).items():
        assert entry["class"] in COMPONENT_CLASSES, f"{nid}: bad class {entry['class']}"
        assert entry["degrades_to"] in BASELINE_TYPES, f"{nid}: bad degrades_to {entry['degrades_to']}"
