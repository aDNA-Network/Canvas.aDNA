"""Components: image panels degrade to file/link/text + carry degrades_to; the comic profile is declared."""

from __future__ import annotations

from canvas_std.reserved import BASELINE_TYPES, COMPONENT_CLASSES

from comic_generator.model import PANEL_TYPES


def _comps(doc):
    return doc["metadata"]["frontmatter"]["_reserved"]["component_types"]


def test_comic_root_is_panel_degrading_to_group(doc):
    by_id = {n["id"]: n for n in doc["nodes"]}
    entry = _comps(doc)["comic_root"]
    assert entry["class"] == "panel"
    assert entry["semantic_type"] == "comic"
    assert entry["degrades_to"] == "group"
    assert by_id["comic_root"]["type"] == "group"


def test_spread_and_page_groups_are_panels(doc):
    comps = _comps(doc)
    spreads = {nid: e for nid, e in comps.items() if e.get("semantic_type") == "spread"}
    pages = {nid: e for nid, e in comps.items() if e.get("semantic_type") == "page"}
    assert spreads and pages
    for e in {**spreads, **pages}.values():
        assert e["class"] == "panel"
        assert e["degrades_to"] == "group"


def test_image_panels_carry_qualities_and_degrade(doc):
    by_id = {n["id"]: n for n in doc["nodes"]}
    images = {nid: e for nid, e in _comps(doc).items() if e["class"] == "image"}
    assert images, "expected at least one image panel"
    for nid, e in images.items():
        assert e["degrades_to"] in BASELINE_TYPES
        assert e["degrades_to"] in ("file", "text")
        assert e["semantic_type"] in PANEL_TYPES
        q = e["qualities"]
        assert q["substrate"] == "raster"
        assert q["image_prompt"]              # the assembled 6-layer prompt rides here
        assert q["aspect_ratio"]
        assert q["status"] in ("rendered", "prompt_only")
        # the baseline node matches the degrades_to + the rendered/prompt status
        node = by_id[nid]
        if q["status"] == "rendered":
            assert node["type"] == "file" and "file" in node
        else:
            assert node["type"] == "text" and "**Panel" in node["text"]


def test_rendered_panel_is_file_node(doc):
    """The conftest comic includes a panel with image_path -> it must be a file node, status rendered."""
    by_id = {n["id"]: n for n in doc["nodes"]}
    rendered = [
        nid for nid, e in _comps(doc).items()
        if e["class"] == "image" and e["qualities"].get("status") == "rendered"
    ]
    assert rendered, "expected at least one rendered (file) panel"
    for nid in rendered:
        assert by_id[nid]["type"] == "file"


def test_spatial_layout_panel_carries_qualities(doc):
    """The conftest comic includes a panel with a spatial_layout -> qualities.spatial_layout present + dual_prompt PART 2."""
    images = [e for e in _comps(doc).values() if e["class"] == "image"]
    with_layout = [e for e in images if "spatial_layout" in e["qualities"]]
    assert with_layout, "expected a panel with a spatial_layout"
    for e in with_layout:
        assert "graph TB" in e["qualities"]["spatial_layout"]
        assert e["qualities"]["dual_prompt"].count("[PART 2: SPATIAL LAYOUT]") == 2


def test_comic_profile_declared(doc):
    assert doc["metadata"]["frontmatter"]["_reserved"]["semantic_bindings"] == {"profile": "comic"}


def test_all_component_classes_and_degrades_are_valid(doc):
    for nid, entry in _comps(doc).items():
        assert entry["class"] in COMPONENT_CLASSES, f"{nid}: bad class {entry['class']}"
        assert entry["degrades_to"] in BASELINE_TYPES, f"{nid}: bad degrades_to {entry['degrades_to']}"
