"""Tests for canvas_core.traps.cv_node_density_01 (M-V1-2-G-02 O4)."""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cv_node_density_01 import check, FILL_THRESHOLDS


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _canvas(nodes: list[dict]) -> dict:
    return {"nodes": nodes, "edges": []}


def _group_node(
    id: str,
    x: float,
    y: float,
    width: float,
    height: float,
    label: str = "",
    slide_type: str | None = None,
) -> dict:
    n = {"id": id, "type": "group", "label": label,
         "x": x, "y": y, "width": width, "height": height}
    if slide_type:
        n["slide_type"] = slide_type
    return n


def _box_node(
    id: str,
    x: float,
    y: float,
    width: float,
    height: float,
    ntype: str = "file",
) -> dict:
    """Non-text content node; area = width * height exactly."""
    return {"id": id, "type": ntype, "x": x, "y": y,
            "width": width, "height": height}


# ---------------------------------------------------------------------------
# Fill ratio detection
# ---------------------------------------------------------------------------


class TestFillRatioMedium:
    def test_fill_above_threshold_fires_medium(self):
        """Content area 80% of container > content threshold 0.75 → medium."""
        # Container 1000x1000 = 1_000_000 area; child 900x900 = 810_000 area = 0.81
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000, slide_type="content"),
            _box_node("b1", 10, 10, 900, 900),
        ])
        findings = check(canvas)
        density = [f for f in findings if f.condition == "fill_ratio"]
        assert len(density) == 1
        assert density[0].severity == "medium"
        assert "c1" in density[0].node_ids

    def test_fill_below_threshold_no_fire(self):
        """Content area 50% of container ≤ 0.75 threshold → no fire."""
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000, slide_type="content"),
            _box_node("b1", 10, 10, 700, 700),  # 0.49
        ])
        findings = check(canvas)
        density = [f for f in findings if f.condition == "fill_ratio"]
        assert len(density) == 0


# ---------------------------------------------------------------------------
# Severity escalation
# ---------------------------------------------------------------------------


class TestFillRatioEscalation:
    def test_fill_above_0_90_escalates_to_high(self):
        # 950x950 = 902_500 / 1_000_000 = 0.9025 → not > 0.90; need > 0.90
        # use 960x960 = 921_600 → 0.9216
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000, slide_type="content"),
            _box_node("b1", 10, 10, 960, 960),
        ])
        findings = check(canvas)
        density = [f for f in findings if f.condition == "fill_ratio"]
        assert len(density) == 1
        assert density[0].severity == "high"

    def test_fill_above_0_95_escalates_to_critical(self):
        # 990x990 = 980_100 / 1_000_000 = 0.9801 > 0.95
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000, slide_type="content"),
            _box_node("b1", 5, 5, 990, 990),
        ])
        findings = check(canvas)
        density = [f for f in findings if f.condition == "fill_ratio"]
        assert len(density) == 1
        assert density[0].severity == "critical"


# ---------------------------------------------------------------------------
# Per-container threshold
# ---------------------------------------------------------------------------


class TestContainerTypes:
    def test_title_slide_strict_threshold(self):
        """Title slide threshold = 0.40; fill 0.50 fires medium."""
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000, slide_type="title"),
            _box_node("b1", 10, 10, 710, 710),  # 504_100/1M = 0.504
        ])
        findings = check(canvas)
        density = [f for f in findings if f.condition == "fill_ratio"]
        assert len(density) == 1
        assert density[0].severity == "medium"

    def test_dense_data_lax_threshold(self):
        """Dense data slide threshold = 0.85; fill 0.80 does not fire."""
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000, slide_type="dense_data"),
            _box_node("b1", 10, 10, 900, 880),  # 792_000 / 1M = 0.792
        ])
        findings = check(canvas)
        density = [f for f in findings if f.condition == "fill_ratio"]
        assert len(density) == 0

    def test_comic_panel_threshold(self):
        """Comic panel threshold = 0.80; fill 0.82 fires medium."""
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000, slide_type="comic_panel"),
            _box_node("b1", 10, 10, 910, 910),  # 828_100 / 1M = 0.828
        ])
        findings = check(canvas)
        density = [f for f in findings if f.condition == "fill_ratio"]
        assert len(density) == 1
        assert density[0].severity == "medium"

    def test_unknown_slide_type_uses_default(self):
        """Unknown slide_type defaults to content threshold 0.75."""
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000, slide_type="weird_type"),
            _box_node("b1", 10, 10, 900, 900),  # 0.81 > 0.75
        ])
        findings = check(canvas)
        density = [f for f in findings if f.condition == "fill_ratio"]
        assert len(density) == 1


# ---------------------------------------------------------------------------
# R11 escalation
# ---------------------------------------------------------------------------


class TestR11Escalation:
    def test_r11_child_escalates_medium_to_high(self):
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000, slide_type="content"),
            _box_node("b1", 10, 10, 900, 900),  # 0.81 medium
        ])
        findings = check(canvas, r11_node_ids={"b1"})
        density = [f for f in findings if f.condition == "fill_ratio"]
        assert len(density) == 1
        assert density[0].severity == "high"

    def test_r11_container_escalates_high_to_critical(self):
        canvas = _canvas([
            _group_node("c1", 0, 0, 1000, 1000, slide_type="content"),
            _box_node("b1", 10, 10, 960, 960),  # 0.9216 high
        ])
        findings = check(canvas, r11_node_ids={"c1"})
        density = [f for f in findings if f.condition == "fill_ratio"]
        assert len(density) == 1
        assert density[0].severity == "critical"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_container_no_fire(self):
        canvas = _canvas([_group_node("c1", 0, 0, 1000, 1000)])
        findings = check(canvas)
        assert len(findings) == 0

    def test_zero_dimension_container_skipped(self):
        canvas = _canvas([
            _group_node("c1", 0, 0, 0, 0),
            _box_node("b1", 0, 0, 100, 100),
        ])
        findings = check(canvas)
        assert len(findings) == 0

    def test_canvas_without_groups_no_fire(self):
        """No groups means no containers to evaluate."""
        canvas = _canvas([
            _box_node("b1", 0, 0, 100, 100),
            _box_node("b2", 200, 0, 100, 100),
        ])
        findings = check(canvas)
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# Substrate neutrality
# ---------------------------------------------------------------------------


class TestSubstrateNeutrality:
    def test_zero_application_imports(self):
        """Trap file must not import canvas_presentation or canvas_comic."""
        trap_path = os.path.join(
            os.path.dirname(__file__), "..", "traps",
            "cv_node_density_01.py",
        )
        with open(trap_path) as f:
            src = f.read()
        assert "canvas_presentation" not in src
        assert "canvas_comic" not in src
