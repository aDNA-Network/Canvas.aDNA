"""E4.2: the first consumer use of the `region` component class (derived-surface markers + the surface_subclass region)."""

from __future__ import annotations

from canvas_std import ConformanceLevel, strip, validate


def _reserved(doc):
    return doc["metadata"]["frontmatter"]["_reserved"]


def test_region_class_first_use(whitepaper_doc):
    regions = {nid: e for nid, e in _reserved(whitepaper_doc)["component_types"].items() if e["class"] == "region"}
    assert regions, "E4.2 is the first consumer to exercise the `region` class"
    assert all(e["degrades_to"] == "group" for e in regions.values())


def test_surface_subclass_region(whitepaper_doc):
    r = _reserved(whitepaper_doc)
    assert r["component_types"]["rgn_subclass"]["class"] == "region"
    assert r["component_types"]["rgn_subclass"]["qualities"]["surface_subclass"] == "print_page"
    assert r["panel_link"]["regions"]["rgn_subclass"]["surface"] == "print_page"


def test_no_genre_has_no_region_class(doc):
    assert not any(e["class"] == "region" for e in _reserved(doc)["component_types"].values())


def test_region_nodes_degrade_clean(whitepaper_doc):
    bare = strip(whitepaper_doc)
    assert validate(bare, ConformanceLevel.CORE) == []
    assert validate(bare, ConformanceLevel.EXTENDED) == []
    by_id = {n["id"]: n for n in bare["nodes"]}
    region_ids = [nid for nid, e in _reserved(whitepaper_doc)["component_types"].items() if e["class"] == "region"]
    assert region_ids and all(by_id[rid]["type"] == "group" for rid in region_ids)
