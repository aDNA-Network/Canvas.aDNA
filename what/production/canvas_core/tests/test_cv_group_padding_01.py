"""Tests for canvas_core.traps.cv_group_padding_01 (M-V1-2-G-02 O4)."""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cv_group_padding_01 import check, PADDING_MIN_PX


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _canvas(nodes: list[dict]) -> dict:
    return {"nodes": nodes, "edges": []}


def _group_node(
    id: str,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str = "",
    slide_type: str | None = None,
) -> dict:
    n = {"id": id, "type": "group", "label": label,
         "x": x, "y": y, "width": w, "height": h}
    if slide_type:
        n["slide_type"] = slide_type
    return n


def _box_node(
    id: str,
    x: float,
    y: float,
    w: float,
    h: float,
    ntype: str = "file",
) -> dict:
    return {"id": id, "type": ntype, "x": x, "y": y, "width": w, "height": h}


# ---------------------------------------------------------------------------
# Aggregate width fill (a)
# ---------------------------------------------------------------------------


class TestAggregateWidthFill:
    def test_width_fill_above_0_90_fires_medium(self):
        # Container 1000 wide; child spans x=40..960 = 920/1000 = 0.92
        # Edges 40 each side > padding_min=24 so only aggregate_fill fires.
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000),
            _box_node("b1", 40, 100, 920, 100),
        ])
        findings = check(canvas)
        agg = [f for f in findings if f.condition == "aggregate_fill"]
        assert len(agg) == 1
        assert agg[0].severity == "medium"
        assert "width" in agg[0].message.lower()

    def test_width_fill_above_0_95_fires_high(self):
        # 970/1000 = 0.97
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000),
            _box_node("b1", 15, 100, 970, 100),
        ])
        findings = check(canvas)
        agg = [f for f in findings if f.condition == "aggregate_fill"]
        assert len(agg) == 1
        assert agg[0].severity == "high"


# ---------------------------------------------------------------------------
# Aggregate height fill (a)
# ---------------------------------------------------------------------------


class TestAggregateHeightFill:
    def test_height_fill_above_0_90_fires_medium(self):
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000),
            _box_node("b1", 100, 40, 100, 920),
        ])
        findings = check(canvas)
        agg = [f for f in findings if f.condition == "aggregate_fill"]
        assert len(agg) == 1
        assert agg[0].severity == "medium"
        assert "height" in agg[0].message.lower()

    def test_height_fill_below_0_90_no_fire(self):
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000),
            _box_node("b1", 100, 100, 100, 800),
        ])
        findings = check(canvas)
        agg = [f for f in findings if f.condition == "aggregate_fill"]
        assert len(agg) == 0


# ---------------------------------------------------------------------------
# Per-node padding (b)
# ---------------------------------------------------------------------------


class TestPerNodePadding:
    def test_edge_distance_below_min_fires(self):
        """Child left edge 8px from container left; padding_min=24 → fires."""
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000),
            _box_node("b1", 8, 100, 100, 100),
        ])
        findings = check(canvas)
        viol = [f for f in findings if f.condition == "edge_violation"]
        assert len(viol) >= 1
        # 8 < 0.5 * 24 = 12 → critical
        assert viol[0].severity == "critical"

    def test_edge_distance_high_severity_band(self):
        """Child left 20px from container; padding_min=24; 20 < 24 but > 18 (0.75*24)
        → medium per ladder (>= 0.75*padding_min)."""
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000),
            _box_node("b1", 20, 100, 100, 100),
        ])
        findings = check(canvas)
        viol = [f for f in findings if f.condition == "edge_violation"]
        assert len(viol) >= 1
        assert viol[0].severity == "medium"

    def test_edge_distance_safe_no_fire(self):
        """Child 30px from container edge; padding_min=24 → no fire."""
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000),
            _box_node("b1", 30, 30, 100, 100),
        ])
        findings = check(canvas)
        viol = [f for f in findings if f.condition == "edge_violation"]
        assert len(viol) == 0


# ---------------------------------------------------------------------------
# Slide-type tokens
# ---------------------------------------------------------------------------


class TestSlideTypeTokens:
    def test_title_slide_uses_token_padding(self):
        """Title slide tokens override margin_side (3xl=64); child 30px → fires."""
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000, slide_type="title"),
            _box_node("b1", 30, 100, 100, 100),  # 30 < 64
        ])
        findings = check(canvas)
        viol = [f for f in findings if f.condition == "edge_violation"]
        assert len(viol) >= 1

    def test_unknown_slide_type_uses_constant(self):
        """Unknown slide_type falls back to 24px constant; 30px is safe."""
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000, slide_type="bogus_type"),
            _box_node("b1", 30, 30, 100, 100),
        ])
        findings = check(canvas)
        viol = [f for f in findings if f.condition == "edge_violation"]
        assert len(viol) == 0


# ---------------------------------------------------------------------------
# R11 escalation
# ---------------------------------------------------------------------------


class TestR11Escalation:
    def test_r11_aggregate_escalates(self):
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000),
            _box_node("b1", 40, 100, 920, 100),  # 0.92 medium
        ])
        findings = check(canvas, r11_node_ids={"b1"})
        agg = [f for f in findings if f.condition == "aggregate_fill"]
        assert len(agg) == 1
        assert agg[0].severity == "high"

    def test_r11_edge_violation_escalates_critical(self):
        """8px violation already critical; R11 on container keeps critical (cap)."""
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000),
            _box_node("b1", 8, 100, 100, 100),
        ])
        findings = check(canvas, r11_node_ids={"c1"})
        viol = [f for f in findings if f.condition == "edge_violation"]
        assert len(viol) >= 1
        assert viol[0].severity == "critical"  # capped


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_container_no_fire(self):
        canvas = _canvas([_group_node("c1", 0, 0, 1000, 1000)])
        findings = check(canvas)
        assert len(findings) == 0

    def test_canvas_without_groups_no_fire(self):
        canvas = _canvas([_box_node("b1", 0, 0, 100, 100)])
        findings = check(canvas)
        assert len(findings) == 0

    def test_zero_dimension_container_skipped(self):
        canvas = _canvas([
            _group_node("c1", 0, 0, 0, 0),
            _box_node("b1", 0, 0, 100, 100),
        ])
        findings = check(canvas)
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# Substrate neutrality
# ---------------------------------------------------------------------------


class TestSubstrateNeutrality:
    def test_zero_application_imports(self):
        trap_path = os.path.join(
            os.path.dirname(__file__), "..", "traps",
            "cv_group_padding_01.py",
        )
        with open(trap_path) as f:
            src = f.read()
        assert "canvas_presentation" not in src
        assert "canvas_comic" not in src
