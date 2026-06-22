"""Domain coverage: the letter carries all supplied blocks as nodes, is one page, and is reading-order chained."""

from __future__ import annotations

from letter_generator.consume import ROOT_ID, build_letter
from letter_generator.model import Letter


def test_all_supplied_blocks_present(doc, letter):
    node_ids = {n["id"] for n in doc["nodes"]}
    assert ROOT_ID in node_ids
    for expected in ("letterhead", "date", "recipient", "salutation", "closing", "signature"):
        assert expected in node_ids, expected
    for i in range(len(letter.body)):
        assert f"body{i}" in node_ids


def test_one_page(doc):
    region = doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]["regions"][ROOT_ID]
    assert region["pagination"] == "paged"
    assert region["extent"] == {"unit": "pages", "max": 1}


def test_body_paragraph_count_matches(doc, letter):
    body_nodes = [n for n in doc["nodes"] if n["id"].startswith("body")]
    assert len(body_nodes) == len(letter.body)


def test_blocks_are_reading_order_chained(doc):
    edges = doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]["edges"]
    assert edges, "expected reading_order edges chaining the blocks"
    assert {e["kind"] for e in edges.values()} == {"reading_order"}


def test_empty_optional_blocks_are_dropped():
    minimal = Letter(title="Bare", id="urn:adna:canvas:letter:bare", salutation="Hi,", body=("One line.",))
    node_ids = {n["id"] for n in build_letter(minimal)["nodes"]}
    assert "letterhead" not in node_ids  # not supplied -> dropped
    assert "date" not in node_ids
    assert {"letter_root", "salutation", "body0"} <= node_ids
