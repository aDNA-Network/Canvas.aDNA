"""Conformance: the comic validates at aDNA-Native; one canonical surface; one region per page; pages extent."""

from __future__ import annotations

from pathlib import Path

from canvas_std import ConformanceLevel, validate, validate_suite

from comic_generator.consume import build_comic
from comic_generator.model import load_comic


def test_validates_adna_native(doc):
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []


def test_suite_meets_declared_adna_native(doc):
    report = validate_suite(doc, ConformanceLevel.ADNA_NATIVE)
    assert report.failed == []
    assert report.meets_declared is True
    assert report.level_reached == ConformanceLevel.ADNA_NATIVE
    assert report.ok is True


def test_one_canonical_surface(doc):
    pl = doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]
    canonical = [s for s in pl["surfaces"] if s.get("role") == "canonical"]
    assert len(canonical) == 1  # the A-5 load-bearing constraint
    assert canonical[0]["id"] == "comic_root"


def test_one_region_per_page(doc):
    """Every page group has exactly one region entry (a page is a panel that carries a region)."""
    by_id = {n["id"]: n for n in doc["nodes"]}
    regions = doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]["regions"]
    page_ids = [nid for nid, e in _comps(doc).items()
                if e.get("semantic_type") == "page" and by_id[nid]["type"] == "group"]
    assert page_ids
    for pid in page_ids:
        assert pid in regions, f"page {pid} has no region"
        assert regions[pid]["extent"]["unit"] == "pages"
        assert regions[pid]["extent"]["max"] == 1


def test_extent_unit_is_pages_everywhere(doc):
    """No `panels` extent unit exists in the Standard — comics paginate in `pages` (PL_EXTENT_UNITS)."""
    regions = doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]["regions"]
    for gid, r in regions.items():
        unit = (r.get("extent") or {}).get("unit")
        if unit is not None:
            assert unit == "pages", f"region {gid} extent.unit {unit!r} should be 'pages'"


def test_component_types_keys_subset_of_node_ids(doc):
    node_ids = {n["id"] for n in doc["nodes"]}
    assert set(_comps(doc)).issubset(node_ids)


def test_example_yaml_builds_and_conforms():
    example = Path(__file__).resolve().parents[1] / "examples" / "science_stanley_mini_issue.yaml"
    doc = build_comic(load_comic(example))
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []
    groups = [n for n in doc["nodes"] if n["type"] == "group" and n["id"] == "comic_root"]
    assert len(groups) == 1


def _comps(doc):
    return doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
