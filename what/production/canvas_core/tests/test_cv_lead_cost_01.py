"""Tests for canvas_core.traps.cv_lead_cost_01 (Halftone HV O1)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cv_lead_cost_01 import check


def _canvas(nodes: list[dict]) -> dict:
    return {"nodes": nodes, "edges": []}


def _text_node(id: str, text: str, w: float = 320, h: float = 110) -> dict:
    return {"id": id, "type": "text", "text": text,
            "x": 0, "y": 0, "width": w, "height": h}


class TestHeadingLead:
    def test_h2_lead_fires(self):
        """The Oration failure shape: a `##` lead costs 98.9px."""
        canvas = _canvas([_text_node("t1", "## Stage One\nBody text here.")])
        findings = check(canvas)
        assert len(findings) == 1
        assert findings[0].condition == "heading_lead"
        assert findings[0].severity == "medium"
        assert "98.9" in findings[0].message
        assert "bold" in findings[0].message

    def test_h3_lead_fires(self):
        canvas = _canvas([_text_node("t1", "### Sub-stage\nBody.")])
        findings = check(canvas)
        assert len(findings) == 1
        assert "74.8" in findings[0].message

    def test_h1_lead_fires(self):
        canvas = _canvas([_text_node("t1", "# Title\nBody.")])
        assert len(check(canvas)) == 1

    def test_bold_lead_clean(self):
        """The recommended pattern: a **bold** lead does not fire."""
        canvas = _canvas([_text_node("t1", "**Stage One**\nBody text here.")])
        assert check(canvas) == []

    def test_plain_and_h4_clean(self):
        canvas = _canvas([
            _text_node("t1", "Plain body text."),
            _text_node("t2", "#### Minor heading\nBody."),
        ])
        assert check(canvas) == []

    def test_heading_mid_node_not_flagged(self):
        """Only the LEAD block is the avoidable cost this trap names."""
        canvas = _canvas([_text_node("t1", "**Lead**\n## Later heading\nBody.")])
        assert check(canvas) == []

    def test_non_text_and_empty_ignored(self):
        canvas = _canvas([
            {"id": "g1", "type": "group", "label": "## G", "x": 0, "y": 0,
             "width": 100, "height": 100},
            _text_node("t1", ""),
        ])
        assert check(canvas) == []


class TestR11Escalation:
    def test_r11_bumps_severity(self):
        canvas = _canvas([_text_node("t1", "## Gate\nBody.")])
        findings = check(canvas, r11_node_ids={"t1"})
        assert findings[0].severity == "high"
