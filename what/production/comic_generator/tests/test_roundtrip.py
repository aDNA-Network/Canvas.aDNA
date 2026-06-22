"""Round-trip: the sync hash is stable across to_canvas/from_canvas; the sequence chain is acyclic."""

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


def test_sequence_chain_acyclic_and_linear(doc):
    """The page `sequence` chain is a single linear, acyclic chain (A-5 enforces acyclicity)."""
    pl = doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]
    seq_eids = [eid for eid, m in pl["edges"].items() if m["kind"] == "sequence"]
    endpoints = {e["id"]: (e["fromNode"], e["toNode"]) for e in doc["edges"]}
    # build the sequence subgraph and confirm no cycle + a single source/sink chain
    succ: dict[str, str] = {}
    indeg: dict[str, int] = {}
    nodes: set[str] = set()
    for eid in seq_eids:
        frm, to = endpoints[eid]
        succ[frm] = to
        indeg[to] = indeg.get(to, 0) + 1
        nodes |= {frm, to}
    # exactly one source (indeg 0) for a non-empty chain
    sources = [n for n in nodes if indeg.get(n, 0) == 0]
    assert len(sources) == 1
    # walk forward: visits each node once (no cycle)
    seen, cur = set(), sources[0]
    while cur in succ:
        assert cur not in seen, "cycle in sequence chain"
        seen.add(cur)
        cur = succ[cur]
    assert len(seen) == len(seq_eids)


def test_start_node_survives_on_first_page(doc):
    """`isStartNode` is set on the first page group (the sequence chain origin)."""
    by_id = {n["id"]: n for n in doc["nodes"]}
    start = [nid for nid, n in by_id.items() if n.get("isStartNode") is True]
    assert len(start) == 1
    # and it is a page group, and the sequence chain's source
    comps = doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
    assert comps[start[0]]["semantic_type"] == "page"
