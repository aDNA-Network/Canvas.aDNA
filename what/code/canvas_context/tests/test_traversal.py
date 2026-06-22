"""Traversal-primitive tests (spec_canvas_context_loading §6) — reading order, neighbors, cycle-safety, fallback.

These use hand-built docs loaded with ``validate=False`` to isolate the graph-walk semantics from validation.
"""

from __future__ import annotations

from canvas_context import load_context_graph


def _doc(nodes, edges, pl_edges=None):
    reserved = {"panel_link": {"edges": pl_edges}} if pl_edges else {}
    return {
        "nodes": nodes,
        "edges": edges,
        "metadata": {"frontmatter": {"_reserved": reserved}},
    }


def test_reading_order_follows_order_edges_from_start_node():
    doc = _doc(
        nodes=[
            {"id": "n1", "type": "text", "x": 0, "y": 0, "width": 10, "height": 10, "isStartNode": True},
            {"id": "n2", "type": "text", "x": 0, "y": 20, "width": 10, "height": 10},
            {"id": "n3", "type": "text", "x": 0, "y": 40, "width": 10, "height": 10},
        ],
        edges=[
            {"id": "e1", "fromNode": "n1", "toNode": "n2", "toEnd": "arrow"},
            {"id": "e2", "fromNode": "n2", "toNode": "n3", "toEnd": "arrow"},
        ],
        pl_edges={"e1": {"kind": "reading_order"}, "e2": {"kind": "sequence"}},
    )
    g = load_context_graph(doc, validate=False)
    assert g.reading_order() == ["n1", "n2", "n3"]


def test_neighbors_directed_and_kind_filtered():
    doc = _doc(
        nodes=[{"id": "a", "type": "text"}, {"id": "b", "type": "text"}, {"id": "c", "type": "text"}],
        edges=[
            {"id": "e1", "fromNode": "a", "toNode": "b", "toEnd": "arrow"},
            {"id": "e2", "fromNode": "a", "toNode": "c", "toEnd": "arrow"},
        ],
        pl_edges={"e1": {"kind": "reading_order"}, "e2": {"kind": "adjacency"}},
    )
    g = load_context_graph(doc, validate=False)
    assert sorted(g.neighbors("a")) == ["b", "c"]
    assert g.neighbors("a", "reading_order") == ["b"]
    assert g.neighbors("a", "adjacency") == ["c"]


def test_neighbors_undirected_is_bidirectional():
    doc = _doc(
        nodes=[{"id": "a", "type": "text"}, {"id": "b", "type": "text"}],
        edges=[{"id": "e1", "fromNode": "a", "toNode": "b", "toEnd": "none"}],
        pl_edges={"e1": {"kind": "adjacency"}},
    )
    g = load_context_graph(doc, validate=False)
    assert g.neighbors("b") == ["a"]  # undirected edge → reachable from either end


def test_reading_order_is_cycle_safe():
    doc = _doc(
        nodes=[{"id": "a", "type": "text", "isStartNode": True}, {"id": "b", "type": "text"}],
        edges=[
            {"id": "e1", "fromNode": "a", "toNode": "b", "toEnd": "arrow"},
            {"id": "e2", "fromNode": "b", "toNode": "a", "toEnd": "arrow"},
        ],
        pl_edges={"e1": {"kind": "reading_order"}, "e2": {"kind": "reading_order"}},
    )
    g = load_context_graph(doc, validate=False)
    assert g.reading_order() == ["a", "b"]  # terminates; a re-encountered node is not revisited (§5.2)


def test_reading_order_geometry_fallback_when_no_order_edges():
    doc = _doc(
        nodes=[
            {"id": "low", "type": "text", "x": 0, "y": 100, "width": 10, "height": 10},
            {"id": "high", "type": "text", "x": 0, "y": 0, "width": 10, "height": 10},
            {"id": "mid", "type": "text", "x": 0, "y": 50, "width": 10, "height": 10},
        ],
        edges=[],
    )
    g = load_context_graph(doc, validate=False)
    assert g.reading_order() == ["high", "mid", "low"]  # top-to-bottom (y, then x)


def test_panels_children_assigned_by_geometric_containment():
    doc = _doc(
        nodes=[
            {"id": "page", "type": "group", "x": 0, "y": 0, "width": 100, "height": 100},
            {"id": "inside", "type": "text", "x": 10, "y": 10, "width": 10, "height": 10},
            {"id": "outside", "type": "text", "x": 200, "y": 200, "width": 10, "height": 10},
        ],
        edges=[],
    )
    g = load_context_graph(doc, validate=False)
    assert g.children("page") == ["inside"]
