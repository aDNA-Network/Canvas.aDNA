"""Domain coverage: single vs thread shape, sequence chaining, image-as-metadata, platform profile."""

from __future__ import annotations

from post_generator.consume import ROOT_ID, build_post


def _pl(doc):
    return doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]


def _seq_edges(doc):
    return {eid: e for eid, e in _pl(doc)["edges"].items() if e["kind"] == "sequence"}


def test_single_post_has_no_sequence_edges(single_post):
    doc = build_post(single_post)
    post_nodes = [n for n in doc["nodes"] if n["id"].startswith("post") and n["id"] != ROOT_ID]
    assert len(post_nodes) == 1
    assert _seq_edges(doc) == {}


def test_thread_is_sequence_chained_and_acyclic(thread):
    doc = build_post(thread)
    post_nodes = [n for n in doc["nodes"] if n["id"].startswith("post") and n["id"] != ROOT_ID]
    assert len(post_nodes) == len(thread.panels)
    seq = _seq_edges(doc)
    assert len(seq) == len(thread.panels) - 1  # a linear chain
    # acyclic + linear: each post is the source of at most one sequence edge, and no edge loops back to post0
    canvas_edges = {e["id"]: e for e in doc["edges"]}
    sources = [canvas_edges[eid]["fromNode"] for eid in seq]
    assert len(sources) == len(set(sources))  # no node starts two sequence hops
    assert all(canvas_edges[eid]["toNode"] != "post0" for eid in seq)  # nothing points back to the start


def test_first_panel_is_start_node(thread):
    doc = build_post(thread)
    post0 = next(n for n in doc["nodes"] if n["id"] == "post0")
    assert post0.get("isStartNode") is True


def test_image_panel_carries_prompt_as_metadata_no_render(thread):
    doc = build_post(thread)
    img_nodes = [n for n in doc["nodes"] if n["id"].startswith("img")]
    assert img_nodes, "the thread fixture has an image panel"
    cts = doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
    for n in img_nodes:
        assert n["type"] == "text"  # a placeholder node — NO rendered file, NO image bytes (ComfyUI renders)
        assert "file" not in n
        assert cts[n["id"]]["class"] == "image"
        assert cts[n["id"]]["qualities"]["image_prompt"]
    # each image is tied to its post by an adjacency edge
    kinds = {e["kind"] for e in _pl(doc)["edges"].values()}
    assert "adjacency" in kinds


def test_platform_profile_applied(single_post, thread):
    single = build_post(single_post)["metadata"]["frontmatter"]["_reserved"]["component_types"][ROOT_ID]["qualities"]
    assert single["platform"] == "twitter" and single["char_budget"] == 280 and single["thread"] is False
    th = build_post(thread)["metadata"]["frontmatter"]["_reserved"]["component_types"][ROOT_ID]["qualities"]
    assert th["platform"] == "linkedin" and th["char_budget"] == 3000 and th["thread"] is True
