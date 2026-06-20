"""Round-trip: topology (incl. the slide sequence) is stable across to_canvas/from_canvas."""

from __future__ import annotations

from canvas_std import compute_sync_hash, diff, from_canvas, to_canvas


def test_sync_hash_matches_reserved(doc):
    assert compute_sync_hash(doc) == doc["metadata"]["frontmatter"]["_reserved"]["sync"]["sync_hash"]


def test_roundtrip_topology_stable(doc):
    redrawn = to_canvas(from_canvas(doc))
    assert compute_sync_hash(redrawn) == compute_sync_hash(doc)
    assert diff(doc, redrawn)["topology_changed"] is False


def test_from_canvas_recovers_all_ids(doc):
    draft = from_canvas(doc)
    assert {n["id"] for n in draft["nodes"]} == {n["id"] for n in doc["nodes"]}
    assert {e["id"] for e in draft["edges"]} == {e["id"] for e in doc["edges"]}


def test_sequence_chain_is_linear(doc, n_slides):
    pl = doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]
    seq = [eid for eid, m in pl["edges"].items() if m["kind"] == "sequence"]
    assert len(seq) == n_slides - 1  # a single chain across the slides (acyclicity enforced by validate at A-5)
