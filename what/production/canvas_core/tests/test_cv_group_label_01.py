"""Tests for canvas_core.traps.cv_group_label_01 (Halftone HV O1)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cv_group_label_01 import check, label_budget


def _canvas(nodes: list[dict]) -> dict:
    return {"nodes": nodes, "edges": []}


def _group(id: str, label: str, w: float, h: float = 400) -> dict:
    return {"id": id, "type": "group", "label": label,
            "x": 0, "y": 0, "width": w, "height": h}


class TestLabelBudget:
    def test_caps_budget_tighter_than_mixed(self):
        assert label_budget(500, "ALL CAPS LABEL") < label_budget(500, "Mixed case label")

    def test_oration_shape_fires(self):
        """`02 · THE AUTHENTIC ...` — a long CAPS label on a narrow group."""
        label = "02 · THE AUTHENTIC VOICE OF THE SPEAKER IN FULL"
        canvas = _canvas([_group("g1", label, 400)])
        findings = check(canvas)
        assert len(findings) == 1
        assert findings[0].condition == "label_truncates"
        assert findings[0].severity == "high"
        assert "widen the group" in findings[0].message

    def test_short_label_clean(self):
        canvas = _canvas([_group("g1", "02 · VOICE", 400)])
        assert check(canvas) == []

    def test_unlabelled_and_non_group_ignored(self):
        canvas = _canvas([
            _group("g1", "", 100),
            {"id": "t1", "type": "text", "text": "a very long text indeed here",
             "x": 0, "y": 0, "width": 100, "height": 50},
        ])
        assert check(canvas) == []

    def test_zero_width_ignored(self):
        canvas = _canvas([_group("g1", "Label", 0)])
        assert check(canvas) == []


class TestR11Escalation:
    def test_r11_bumps_to_critical(self):
        label = "A VERY LONG ALL CAPS LABEL THAT CANNOT POSSIBLY FIT"
        canvas = _canvas([_group("g1", label, 300)])
        findings = check(canvas, r11_node_ids={"g1"})
        assert findings[0].severity == "critical"
