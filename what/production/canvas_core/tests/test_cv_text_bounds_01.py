"""Tests for canvas_core.traps.cv_text_bounds_01 (M-1-07 O2/O4)."""

from __future__ import annotations

import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cv_text_bounds_01 import check
from canvas_core.traps import TrapFinding


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "cv_text_bounds_01")


def _canvas(nodes: list[dict]) -> dict:
    """Build a minimal canvas dict."""
    return {"nodes": nodes, "edges": []}


def _text_node(
    id: str,
    text: str,
    x: float,
    y: float,
    width: float,
    height: float,
) -> dict:
    return {"id": id, "type": "text", "text": text,
            "x": x, "y": y, "width": width, "height": height}


def _group_node(
    id: str,
    x: float,
    y: float,
    width: float,
    height: float,
    label: str = "",
) -> dict:
    return {"id": id, "type": "group", "label": label,
            "x": x, "y": y, "width": width, "height": height}


# ---------------------------------------------------------------------------
# (a) Overflow
# ---------------------------------------------------------------------------


class TestOverflow:
    def test_overflow_detected(self):
        """Long text in a tiny box triggers overflow."""
        canvas = _canvas([
            _group_node("g1", 0, 0, 400, 400, "Page"),
            _text_node("t1", "This is a very long title that should definitely overflow", 10, 10, 80, 20),
        ])
        findings = check(canvas)
        overflow = [f for f in findings if f.condition == "overflow"]
        assert len(overflow) >= 1
        assert "t1" in overflow[0].node_ids
        assert overflow[0].severity == "medium"

    def test_no_overflow_short_text(self):
        """Short text in a big box — no overflow."""
        canvas = _canvas([
            _group_node("g1", 0, 0, 400, 400),
            _text_node("t1", "Hi", 10, 10, 200, 100),
        ])
        findings = check(canvas)
        overflow = [f for f in findings if f.condition == "overflow"]
        assert len(overflow) == 0

    def test_overflow_empty_text_ignored(self):
        """Empty text nodes should not fire."""
        canvas = _canvas([
            _text_node("t1", "", 10, 10, 80, 20),
        ])
        findings = check(canvas)
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# (b) Overlap
# ---------------------------------------------------------------------------


class TestOverlap:
    def test_overlap_detected(self):
        """Two text nodes at the same position overlap."""
        canvas = _canvas([
            _group_node("g1", 0, 0, 800, 800),
            _text_node("t1", "Hello", 100, 100, 200, 50),
            _text_node("t2", "World", 100, 100, 200, 50),
        ])
        findings = check(canvas)
        overlaps = [f for f in findings if f.condition == "overlap"]
        assert len(overlaps) >= 1
        assert set(overlaps[0].node_ids) == {"t1", "t2"}
        assert overlaps[0].severity == "high"

    def test_no_overlap_separated(self):
        """Two far-apart text nodes — no overlap."""
        canvas = _canvas([
            _group_node("g1", 0, 0, 800, 800),
            _text_node("t1", "Hello", 0, 0, 100, 50),
            _text_node("t2", "World", 500, 500, 100, 50),
        ])
        findings = check(canvas)
        overlaps = [f for f in findings if f.condition == "overlap"]
        assert len(overlaps) == 0


# ---------------------------------------------------------------------------
# (c) Group exit
# ---------------------------------------------------------------------------


class TestGroupExit:
    def test_group_exit_detected(self):
        """Text node extends well beyond parent group."""
        canvas = _canvas([
            _group_node("g1", 0, 0, 400, 400, "Panel"),
            _text_node("t1", "Escaped text", 380, 380, 100, 100),
        ])
        findings = check(canvas)
        exits = [f for f in findings if f.condition == "group_exit"]
        assert len(exits) >= 1
        assert "t1" in exits[0].node_ids
        assert exits[0].severity == "high"
        assert "Panel" in exits[0].message

    def test_no_group_exit_contained(self):
        """Text node fully within group bounds — no exit."""
        canvas = _canvas([
            _group_node("g1", 0, 0, 400, 400),
            _text_node("t1", "Safe text", 10, 10, 100, 50),
        ])
        findings = check(canvas)
        exits = [f for f in findings if f.condition == "group_exit"]
        assert len(exits) == 0

    def test_top_level_text_no_exit(self):
        """Text node with no parent group should not fire group_exit."""
        canvas = _canvas([
            _text_node("t1", "Orphan text", 0, 0, 100, 50),
        ])
        findings = check(canvas)
        exits = [f for f in findings if f.condition == "group_exit"]
        assert len(exits) == 0


# ---------------------------------------------------------------------------
# R11 escalation
# ---------------------------------------------------------------------------


class TestR11Escalation:
    def test_overflow_escalated(self):
        """Overflow on R11 node bumps severity medium -> high."""
        canvas = _canvas([
            _group_node("g1", 0, 0, 400, 400),
            _text_node("t1", "Very long text that overflows its tiny box easily", 10, 10, 80, 20),
        ])
        findings = check(canvas, r11_node_ids={"t1"})
        overflow = [f for f in findings if f.condition == "overflow"]
        assert len(overflow) >= 1
        assert overflow[0].severity == "high"  # escalated from medium

    def test_overlap_escalated_to_critical(self):
        """Overlap (default high) on R11 node bumps to critical."""
        canvas = _canvas([
            _group_node("g1", 0, 0, 800, 800),
            _text_node("t1", "Hello", 100, 100, 200, 50),
            _text_node("t2", "World", 100, 100, 200, 50),
        ])
        findings = check(canvas, r11_node_ids={"t1"})
        overlaps = [f for f in findings if f.condition == "overlap"]
        assert len(overlaps) >= 1
        assert overlaps[0].severity == "critical"  # escalated from high

    def test_no_escalation_without_r11(self):
        """Non-R11 nodes keep default severity."""
        canvas = _canvas([
            _group_node("g1", 0, 0, 400, 400),
            _text_node("t1", "Very long text that overflows its tiny box easily", 10, 10, 80, 20),
        ])
        findings = check(canvas, r11_node_ids={"other_node"})
        overflow = [f for f in findings if f.condition == "overflow"]
        assert len(overflow) >= 1
        assert overflow[0].severity == "medium"  # not escalated


# ---------------------------------------------------------------------------
# M-1-06 compatibility
# ---------------------------------------------------------------------------


class TestViewportCompatibility:
    def test_comic_dims_no_false_fire(self):
        """Comic page at 1988x3075 — text fitting real dims must not fire."""
        canvas = _canvas([
            _group_node("g1", 0, 0, 1988, 3075, "Comic Page"),
            # Text that fits comfortably in a 400x200 box at this page size.
            _text_node("t1", "Short", 100, 100, 400, 200),
        ])
        findings = check(canvas)
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# Fixture test (O4)
# ---------------------------------------------------------------------------


class TestIssue01Fixture:
    def test_issue_01_p1_fires(self):
        """SS Issue 01 page 1 fixture must fire at least one finding.

        The page 1 text nodes (e.g. '**SCIENCE STANLEY**' in a 200x40 box)
        have text content that overflows their declared dimensions at any
        reasonable font size.  This test validates that the CV-TEXT-BOUNDS-01
        trap machinery is wired and detects the known M01 failure mode.

        Phase 1 exit gate criterion 6 (ADR 004).
        """
        fixture_path = os.path.join(FIXTURES_DIR, "issue_01_p1.canvas")
        assert os.path.isfile(fixture_path), f"Fixture missing: {fixture_path}"

        with open(fixture_path) as f:
            canvas_data = json.load(f)

        findings = check(canvas_data)
        assert len(findings) >= 1, (
            f"Expected >=1 finding on Issue 01 page 1 fixture, got {len(findings)}"
        )
        # Gate criterion: trap fires at all on the known-failure case.
        # Text node at y=1002 with height=40 escapes group (ends y=1025)
        # by 17px — group_exit should fire.  Overflow may also fire
        # depending on font resolution (Pillow vs heuristic path).
        conditions = {f.condition for f in findings}
        assert len(conditions) >= 1, (
            f"Expected at least one condition type, got: {conditions}"
        )
