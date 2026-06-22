"""Tests for canvas_core.traps.cv_dimension_visibility_01 (M-R3-01a)."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cv_dimension_visibility_01 import check
from canvas_core.traps import TrapFinding


def _canvas(nodes: list[dict], **extras) -> dict:
    out = {"nodes": nodes, "edges": []}
    out.update(extras)
    return out


def _group(id: str, x: float = 0, y: float = 0,
           w: float = 1200, h: float = 1100) -> dict:
    return {"id": id, "type": "group", "x": x, "y": y, "width": w, "height": h}


def _text(id: str, text: str, x: float = 10, y: float = 10,
          w: float = 200, h: float = 50,
          style: dict | None = None) -> dict:
    n = {"id": id, "type": "text", "text": text,
         "x": x, "y": y, "width": w, "height": h}
    if style is not None:
        n["styleAttributes"] = style
    return n


# ---------------------------------------------------------------------------
# (a) aspect_ratio_missing
# ---------------------------------------------------------------------------


class TestAspectRatioMissing:
    def test_no_metadata_fires(self):
        """Canvas with no aspect-ratio metadata anywhere."""
        canvas = _canvas([_group("g1")])
        findings = check(canvas)
        misses = [f for f in findings if f.condition == "aspect_ratio_missing"]
        assert len(misses) == 1
        assert misses[0].severity == "medium"

    def test_top_level_aspect_ratio_no_fire(self):
        """Top-level 'aspect_ratio' key satisfies the metadata check."""
        canvas = _canvas([_group("g1")], aspect_ratio="16:9")
        findings = check(canvas)
        misses = [f for f in findings if f.condition == "aspect_ratio_missing"]
        assert len(misses) == 0

    def test_nested_metadata_aspect_no_fire(self):
        """Recursive search finds aspect_ratio under metadata.frontmatter."""
        canvas = _canvas([_group("g1")],
                         metadata={"frontmatter": {"aspect_ratio": "16:9"}})
        findings = check(canvas)
        misses = [f for f in findings if f.condition == "aspect_ratio_missing"]
        assert len(misses) == 0

    def test_viewport_alias_no_fire(self):
        """'viewport' key is also accepted."""
        canvas = _canvas([_group("g1")], viewport={"width": 1920, "height": 1080})
        findings = check(canvas)
        misses = [f for f in findings if f.condition == "aspect_ratio_missing"]
        assert len(misses) == 0


# ---------------------------------------------------------------------------
# (b) frame_dimension_hidden
# ---------------------------------------------------------------------------


class TestFrameDimensionHidden:
    def test_uniform_groups_no_affordance_fires(self):
        """Multiple uniform groups but no node carries dimension info."""
        canvas = _canvas([
            _group("g1", x=0),
            _group("g2", x=1500),
            _group("g3", x=3000),
        ], aspect_ratio="16:9")  # avoid aspect_ratio_missing fire
        findings = check(canvas)
        hidden = [f for f in findings if f.condition == "frame_dimension_hidden"]
        assert len(hidden) == 1
        assert set(hidden[0].node_ids) == {"g1", "g2", "g3"}
        assert "1200" in hidden[0].message and "1100" in hidden[0].message

    def test_text_pattern_satisfies_affordance(self):
        """A text node containing '16:9' counts as a visible dimension cue."""
        canvas = _canvas([
            _group("g1", x=0),
            _group("g2", x=1500),
            _text("t1", "Format: 16:9", x=10, y=10),
        ], aspect_ratio="16:9")
        findings = check(canvas)
        hidden = [f for f in findings if f.condition == "frame_dimension_hidden"]
        assert len(hidden) == 0

    def test_frame_node_satisfies_affordance(self):
        """A type:frame node counts as a visible affordance."""
        canvas = _canvas([
            _group("g1", x=0),
            _group("g2", x=1500),
            {"id": "f1", "type": "frame", "x": 0, "y": 0,
             "width": 1200, "height": 1100},
        ], aspect_ratio="16:9")
        findings = check(canvas)
        hidden = [f for f in findings if f.condition == "frame_dimension_hidden"]
        assert len(hidden) == 0

    def test_styleattr_aspect_ratio_satisfies(self):
        """A node with styleAttributes containing aspect_ratio key satisfies."""
        canvas = _canvas([
            _group("g1", x=0),
            _group("g2", x=1500),
            _text("t1", "body", style={"aspect_ratio": "16:9"}),
        ], aspect_ratio="16:9")
        findings = check(canvas)
        hidden = [f for f in findings if f.condition == "frame_dimension_hidden"]
        assert len(hidden) == 0

    def test_non_uniform_dims_no_fire(self):
        """Groups with varied dimensions — no implied uniform frame."""
        canvas = _canvas([
            _group("g1", x=0, w=1200, h=1100),
            _group("g2", x=1500, w=800, h=600),
        ], aspect_ratio="16:9")
        findings = check(canvas)
        hidden = [f for f in findings if f.condition == "frame_dimension_hidden"]
        assert len(hidden) == 0

    def test_no_groups_no_fire(self):
        """Canvas with no groups — frame_dimension_hidden does not apply."""
        canvas = _canvas([], aspect_ratio="16:9")
        findings = check(canvas)
        hidden = [f for f in findings if f.condition == "frame_dimension_hidden"]
        assert len(hidden) == 0


# ---------------------------------------------------------------------------
# Integration: both conditions fire when both apply
# ---------------------------------------------------------------------------


class TestBothConditions:
    def test_both_fire_on_bare_canvas(self):
        """Bare canvas: no metadata + uniform groups + no affordance — both fire."""
        canvas = _canvas([
            _group("g1", x=0),
            _group("g2", x=1500),
            _group("g3", x=3000),
        ])  # no aspect_ratio at top level
        findings = check(canvas)
        conditions = {f.condition for f in findings}
        assert "aspect_ratio_missing" in conditions
        assert "frame_dimension_hidden" in conditions


# ---------------------------------------------------------------------------
# R11 escalation
# ---------------------------------------------------------------------------


class TestR11Escalation:
    def test_frame_hidden_escalated(self):
        """frame_dimension_hidden bumps medium -> high when group is R11."""
        canvas = _canvas([
            _group("g1", x=0),
            _group("g2", x=1500),
        ], aspect_ratio="16:9")
        findings = check(canvas, r11_node_ids={"g1"})
        hidden = [f for f in findings if f.condition == "frame_dimension_hidden"]
        assert len(hidden) == 1
        assert hidden[0].severity == "high"


# ---------------------------------------------------------------------------
# Wilhelm + Issue 01 baselines (mission Exit Gate criterion 5)
# ---------------------------------------------------------------------------


class TestWilhelmBaseline:
    def test_wilhelm_fires_aspect_ratio_missing(self):
        """Wilhelm baseline has no aspect-ratio key — both conditions fire."""
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
        conditions = {f.condition for f in findings}
        # Wilhelm has no top-level or metadata aspect_ratio
        assert "aspect_ratio_missing" in conditions, (
            f"Expected aspect_ratio_missing on Wilhelm baseline, got {conditions}"
        )


class TestComicBaseline:
    def test_comic_fires_aspect_ratio_missing(self):
        """Comic baseline has no aspect-ratio key — fires."""
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
        conditions = {f.condition for f in findings}
        assert "aspect_ratio_missing" in conditions
