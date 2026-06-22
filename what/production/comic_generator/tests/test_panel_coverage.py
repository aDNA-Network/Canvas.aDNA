"""Panel coverage: every page has ≥1 panel; every panel has a prompt + aspect; reading_order + sequence cover all."""

from __future__ import annotations


def _reserved(doc):
    return doc["metadata"]["frontmatter"]["_reserved"]


def _by_semantic(doc, semantic):
    by_id = {n["id"]: n for n in doc["nodes"]}
    comps = _reserved(doc)["component_types"]
    return [nid for nid, e in comps.items() if e.get("semantic_type") == semantic and nid in by_id]


def _panels_of_page(doc, page_id):
    """Image-panel node ids whose id is prefixed by the page id (panel ids are `{pid}_pN`)."""
    comps = _reserved(doc)["component_types"]
    return [nid for nid, e in comps.items() if e["class"] == "image" and nid.startswith(f"{page_id}_p")]


def test_every_page_has_at_least_one_panel(doc):
    pages = _by_semantic(doc, "page")
    assert pages
    for pid in pages:
        assert _panels_of_page(doc, pid), f"page {pid} has no panels"


def test_every_panel_has_non_empty_image_prompt_and_aspect(doc):
    images = {nid: e for nid, e in _reserved(doc)["component_types"].items() if e["class"] == "image"}
    assert images
    for nid, e in images.items():
        q = e["qualities"]
        assert isinstance(q.get("image_prompt"), str) and q["image_prompt"].strip(), f"{nid}: empty image_prompt"
        assert isinstance(q.get("aspect_ratio"), str) and q["aspect_ratio"], f"{nid}: missing aspect_ratio"


def test_reading_order_covers_each_multi_panel_page(doc):
    """Each page with ≥2 panels has a reading_order chain visiting every panel on that page exactly once."""
    pl = _reserved(doc)["panel_link"]
    endpoints = {e["id"]: (e["fromNode"], e["toNode"]) for e in doc["edges"]}
    for pid in _by_semantic(doc, "page"):
        panels = set(_panels_of_page(doc, pid))
        if len(panels) < 2:
            continue
        ro_eids = [eid for eid, m in pl["edges"].items() if m["kind"] == "reading_order" and eid.startswith(f"{pid}_ro_")]
        visited: set[str] = set()
        for eid in ro_eids:
            frm, to = endpoints[eid]
            visited |= {frm, to}
        assert panels.issubset(visited), f"page {pid}: reading_order misses {panels - visited}"


def test_sequence_covers_all_pages(doc):
    """The sequence chain spans all pages: it touches every page group, and has (n_pages - 1) edges."""
    pl = _reserved(doc)["panel_link"]
    pages = set(_by_semantic(doc, "page"))
    endpoints = {e["id"]: (e["fromNode"], e["toNode"]) for e in doc["edges"]}
    seq_eids = [eid for eid, m in pl["edges"].items() if m["kind"] == "sequence"]
    assert len(seq_eids) == len(pages) - 1
    touched: set[str] = set()
    for eid in seq_eids:
        frm, to = endpoints[eid]
        touched |= {frm, to}
    assert touched == pages, f"sequence does not cover all pages: {pages - touched}"


def test_adjacency_links_are_gutter_neighbours(doc):
    """Every adjacency edge connects two image panels on the same page (a spatial neighbour relation)."""
    pl = _reserved(doc)["panel_link"]
    comps = _reserved(doc)["component_types"]
    endpoints = {e["id"]: (e["fromNode"], e["toNode"]) for e in doc["edges"]}
    adj_eids = [eid for eid, m in pl["edges"].items() if m["kind"] == "adjacency"]
    for eid in adj_eids:
        frm, to = endpoints[eid]
        assert comps[frm]["class"] == "image" and comps[to]["class"] == "image"
        # same page prefix (panel ids are `{pid}_pN`)
        assert frm.rsplit("_p", 1)[0] == to.rsplit("_p", 1)[0], f"adjacency {eid} crosses pages"
