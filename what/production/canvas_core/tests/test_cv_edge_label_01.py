"""Tests for canvas_core.traps.cv_edge_label_01 (Halftone HV O1)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cv_edge_label_01 import check, edge_label_box


def _node(id: str, x: float, y: float, w: float = 200, h: float = 100,
          ntype: str = "text") -> dict:
    n = {"id": id, "type": ntype, "x": x, "y": y, "width": w, "height": h}
    if ntype == "text":
        n["text"] = "body"
    return n


def _edge(id: str, a: str, b: str, label: str = "",
          from_side: str = "right", to_side: str = "left") -> dict:
    e = {"id": id, "fromNode": a, "fromSide": from_side,
         "toNode": b, "toSide": to_side}
    if label:
        e["label"] = label
    return e


def _canvas(nodes: list[dict], edges: list[dict]) -> dict:
    return {"nodes": nodes, "edges": edges}


class TestLabelLength:
    def test_over_30_fails_high(self):
        canvas = _canvas(
            [_node("a", 0, 0), _node("b", 1000, 0)],
            [_edge("e1", "a", "b", "this label is far far too long to stay on one line")],
        )
        findings = [f for f in check(canvas) if f.condition == "label_too_long"]
        assert len(findings) == 1
        assert findings[0].severity == "high"

    def test_21_to_30_warns_medium(self):
        canvas = _canvas(
            [_node("a", 0, 0), _node("b", 2000, 0)],
            [_edge("e1", "a", "b", "twenty-five characters!!")],  # 24 chars
        )
        findings = [f for f in check(canvas) if f.condition == "label_may_wrap"]
        assert len(findings) == 1
        assert findings[0].severity == "medium"

    def test_20_or_under_clean(self):
        canvas = _canvas(
            [_node("a", 0, 0), _node("b", 2000, 0)],
            [_edge("e1", "a", "b", "composes"), _edge("e2", "b", "a")],
        )
        length_findings = [
            f for f in check(canvas)
            if f.condition in ("label_too_long", "label_may_wrap")
        ]
        assert length_findings == []


class TestLabelCollision:
    def test_label_over_third_node_fires(self):
        """A labelled edge whose midpoint box sits on an unrelated node."""
        canvas = _canvas(
            [
                _node("a", 0, 0),
                _node("b", 1000, 0),
                _node("victim", 450, -40, 220, 120),  # sits at the midpoint
            ],
            [_edge("e1", "a", "b", "spans the gap")],
        )
        findings = [f for f in check(canvas) if f.condition == "label_collision"]
        assert len(findings) == 1
        assert findings[0].severity == "high"
        assert "victim" in findings[0].node_ids

    def test_endpoints_never_count_as_collision(self):
        canvas = _canvas(
            [_node("a", 0, 0), _node("b", 220, 0)],  # close together
            [_edge("e1", "a", "b", "tight label")],
        )
        findings = [f for f in check(canvas) if f.condition == "label_collision"]
        for f in findings:
            assert "a" not in f.node_ids[1:] or "b" not in f.node_ids[1:]

    def test_unlabelled_edges_ignored(self):
        canvas = _canvas(
            [_node("a", 0, 0), _node("b", 1000, 0), _node("c", 450, -40)],
            [_edge("e1", "a", "b")],
        )
        assert check(canvas) == []

    def test_no_edges_returns_empty(self):
        assert check(_canvas([_node("a", 0, 0)], [])) == []


class TestEdgeLabelBox:
    def test_box_none_without_label(self):
        nodes = {n["id"]: n for n in [_node("a", 0, 0), _node("b", 500, 0)]}
        assert edge_label_box(_edge("e1", "a", "b"), nodes) is None

    def test_box_wider_for_longer_label(self):
        nodes = {n["id"]: n for n in [_node("a", 0, 0), _node("b", 500, 0)]}
        small = edge_label_box(_edge("e1", "a", "b", "hi"), nodes)
        large = edge_label_box(_edge("e2", "a", "b", "a much longer label"), nodes)
        assert (small[2] - small[0]) < (large[2] - large[0])

    def test_dangling_endpoint_returns_none(self):
        nodes = {n["id"]: n for n in [_node("a", 0, 0)]}
        assert edge_label_box(_edge("e1", "a", "missing", "x"), nodes) is None
