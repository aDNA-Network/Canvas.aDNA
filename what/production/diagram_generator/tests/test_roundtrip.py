"""Round-trip: topology is stable across to_canvas/from_canvas — including a flowchart WITH A CYCLE."""

from __future__ import annotations

from canvas_std import ConformanceLevel, compute_sync_hash, diff, from_canvas, to_canvas, validate

from diagram_generator.consume import build_diagram


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


def test_cyclic_flowchart_roundtrips_and_validates(flowchart):
    """The flowchart fixture has a cycle (c -> a). Its edges are `dependency` (not the acyclicity-checked
    `sequence`), so it must validate aDNA-Native AND survive a round-trip. Guards against mis-tagging edges."""
    doc = build_diagram(flowchart)
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []
    pl = doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]
    assert all(m["kind"] == "dependency" for m in pl["edges"].values())
    # and there genuinely is a cycle in the topology
    succ: dict[str, set[str]] = {}
    for e in doc["edges"]:
        succ.setdefault(e["fromNode"], set()).add(e["toNode"])
    assert "a" in succ.get("c", set()) and "b" in succ.get("a", set())  # c->a->b->c
    redrawn = to_canvas(from_canvas(doc))
    assert diff(doc, redrawn)["topology_changed"] is False


def test_gantt_sequence_chain_is_linear_and_acyclic(gantt):
    doc = build_diagram(gantt)
    assert validate(doc, ConformanceLevel.ADNA_NATIVE) == []
    pl = doc["metadata"]["frontmatter"]["_reserved"]["panel_link"]
    kinds = {m["kind"] for m in pl["edges"].values()}
    assert kinds == {"sequence"}
    assert len(pl["edges"]) == len(gantt.edges)  # a single chain across the tasks (A-5 enforces acyclicity)
