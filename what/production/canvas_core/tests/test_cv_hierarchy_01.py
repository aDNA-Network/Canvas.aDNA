"""Tests for canvas_core.traps.cv_hierarchy_01 (M-R3-01a)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cv_hierarchy_01 import check, _heading_level
from canvas_core.traps import TrapFinding


def _canvas(nodes: list[dict]) -> dict:
    return {"nodes": nodes, "edges": []}


def _group(id: str, x: float = 0, y: float = 0,
           w: float = 1000, h: float = 1000,
           label: str | None = None) -> dict:
    g = {"id": id, "type": "group", "x": x, "y": y, "width": w, "height": h}
    if label is not None:
        g["label"] = label
    return g


def _text(id: str, text: str, y: float = 50,
          x: float = 10, w: float = 800, h: float = 100) -> dict:
    return {"id": id, "type": "text", "text": text,
            "x": x, "y": y, "width": w, "height": h}


# ---------------------------------------------------------------------------
# Heading-level parser
# ---------------------------------------------------------------------------


class TestHeadingLevelParser:
    def test_h1(self):
        assert _heading_level("# Title") == 1

    def test_h2(self):
        assert _heading_level("## Subtitle") == 2

    def test_h6(self):
        assert _heading_level("###### Sub") == 6

    def test_no_heading(self):
        assert _heading_level("Body text without prefix") is None

    def test_empty(self):
        assert _heading_level("") is None

    def test_no_space_after_hash(self):
        assert _heading_level("#NotAHeading") is None  # no space

    def test_first_line_only(self):
        assert _heading_level("# Title\nBody") == 1

    def test_leading_whitespace_ok(self):
        assert _heading_level("  ## Indented") == 2

    def test_too_many_hashes(self):
        assert _heading_level("####### NotAHeading") is None  # 7+ hashes


# ---------------------------------------------------------------------------
# (a) title_slot_missing
# ---------------------------------------------------------------------------


class TestTitleSlotMissing:
    def test_no_heading_fires(self):
        """Group with body-only text — no markdown heading anywhere."""
        canvas = _canvas([
            _group("g1", h=1000, label="bad slide"),
            _text("t1", "Just body text", y=50),
            _text("t2", "More body text", y=200),
        ])
        findings = check(canvas)
        misses = [f for f in findings if f.condition == "title_slot_missing"]
        assert len(misses) == 1
        assert misses[0].node_ids == ["g1"]
        assert "bad slide" in misses[0].message

    def test_heading_in_top_region_no_fire(self):
        """Heading sits in the top 40% — title slot satisfied."""
        canvas = _canvas([
            _group("g1", h=1000),
            _text("t1", "# Hello", y=50),  # well within top 40% (y < 400)
            _text("t2", "Body text below", y=600),
        ])
        findings = check(canvas)
        misses = [f for f in findings if f.condition == "title_slot_missing"]
        assert len(misses) == 0

    def test_heading_below_title_region_fires(self):
        """Heading is too low in the group to count as title."""
        canvas = _canvas([
            _group("g1", h=1000),
            _text("t1", "Body text on top", y=50),
            _text("t2", "# Title at bottom", y=800),  # below 0.4 * 1000 = 400
        ])
        findings = check(canvas)
        misses = [f for f in findings if f.condition == "title_slot_missing"]
        assert len(misses) == 1

    def test_no_text_nodes_no_fire(self):
        """Group with no text children — nothing to check."""
        canvas = _canvas([
            _group("g1", h=1000),
        ])
        findings = check(canvas)
        assert len(findings) == 0


# ---------------------------------------------------------------------------
# (b) hierarchy_ratio_collapse — multiple H1s
# ---------------------------------------------------------------------------


class TestHierarchyRatioCollapse:
    def test_two_h1_fires(self):
        """Two competing H1 headings in one group."""
        canvas = _canvas([
            _group("g1", h=1000),
            _text("t1", "# First Title", y=50),
            _text("t2", "# Second Title", y=150),
        ])
        findings = check(canvas)
        collapses = [f for f in findings if f.condition == "hierarchy_ratio_collapse"]
        assert len(collapses) == 1
        assert set(collapses[0].node_ids) == {"t1", "t2"}

    def test_h1_plus_h2_no_fire(self):
        """H1 + H2 is normal hierarchy."""
        canvas = _canvas([
            _group("g1", h=1000),
            _text("t1", "# Title", y=50),
            _text("t2", "## Subtitle", y=150),
        ])
        findings = check(canvas)
        collapses = [f for f in findings if f.condition == "hierarchy_ratio_collapse"]
        assert len(collapses) == 0

    def test_three_h1_fires(self):
        """Three H1s — even worse collapse."""
        canvas = _canvas([
            _group("g1", h=1000),
            _text("t1", "# A", y=50),
            _text("t2", "# B", y=150),
            _text("t3", "# C", y=250),
        ])
        findings = check(canvas)
        collapses = [f for f in findings if f.condition == "hierarchy_ratio_collapse"]
        assert len(collapses) == 1
        assert len(collapses[0].node_ids) == 3


# ---------------------------------------------------------------------------
# R11 escalation
# ---------------------------------------------------------------------------


class TestR11Escalation:
    def test_title_slot_missing_escalated(self):
        """title_slot_missing on R11 group bumps medium -> high."""
        canvas = _canvas([
            _group("g1", h=1000),
            _text("t1", "Body only", y=50),
        ])
        findings = check(canvas, r11_node_ids={"g1"})
        misses = [f for f in findings if f.condition == "title_slot_missing"]
        assert len(misses) == 1
        assert misses[0].severity == "high"


# ---------------------------------------------------------------------------
# Wilhelm baseline sanity (mission Exit Gate criterion 5)
# ---------------------------------------------------------------------------


class TestWilhelmBaseline:
    def test_wilhelm_runs_clean(self):
        """Wilhelm parity baseline runs without error.

        Wilhelm slides all carry markdown heading prefixes, so
        title_slot_missing should not fire across the full deck.
        Real audit interpretation deferred to M-R3-01.
        """
        import json
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "..",
            "what", "artifacts", "parity_deck", "wilhelm_parity.canvas"
        )
        path = os.path.normpath(path)
        if not os.path.isfile(path):
            import pytest
            pytest.skip(f"Wilhelm baseline missing: {path}")

        with open(path) as f:
            canvas_data = json.load(f)

        findings = check(canvas_data)
        for f in findings:
            assert f.trap_id == "CV-HIERARCHY-01"
            assert f.severity in ("medium", "high", "critical")


class TestComicBaseline:
    def test_comic_fires(self):
        """Issue 01 parity comic — comic pages contain panel-dialogue body
        text without markdown headings, so title_slot_missing should fire
        on at least one page.
        """
        import json
        path = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "..",
            "what", "artifacts", "parity_comic", "comic_parity.canvas"
        )
        path = os.path.normpath(path)
        if not os.path.isfile(path):
            import pytest
            pytest.skip(f"Comic baseline missing: {path}")

        with open(path) as f:
            canvas_data = json.load(f)

        findings = check(canvas_data)
        misses = [f for f in findings if f.condition == "title_slot_missing"]
        assert len(misses) >= 1, (
            f"Expected >=1 title_slot_missing on comic baseline (panel-only "
            f"text without headings), got {len(misses)}"
        )
