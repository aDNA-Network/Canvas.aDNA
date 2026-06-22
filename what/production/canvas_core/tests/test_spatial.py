"""LOC-heavy substrate smoke for `canvas_core/spatial.py` (291 LOC).

Authored under M-R5-01a S2 Phase 4 (`campaign_canvasforge_review`) to
provide minimum-viable test coverage for the pure-geometry spatial-analysis
module not covered by inherited Phase 1 migrations. Goal: prevent silent
breakage on Phase 7 cleanup-mission file moves; not full unit coverage.

Exercises the public surface — bounding_box, overlaps, detect_overlaps,
alignment_score, containment_check, spacing_analysis, structural_summary.
Pure substrate; zero application assumptions.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.spatial import (
    alignment_score,
    bounding_box,
    containment_check,
    detect_overlaps,
    overlaps,
    spacing_analysis,
    structural_summary,
)


class TestBoundingBox:
    """Smoke: bounding_box extracts (x1, y1, x2, y2) from node dicts."""

    def test_basic(self):
        node = {"x": 10, "y": 20, "width": 100, "height": 200}
        assert bounding_box(node) == (10, 20, 110, 220)

    def test_origin(self):
        node = {"x": 0, "y": 0, "width": 50, "height": 50}
        assert bounding_box(node) == (0, 0, 50, 50)

    def test_missing_fields_default_zero(self):
        # Node missing fields uses defaults; result is (0, 0, 0, 0)
        node = {}
        assert bounding_box(node) == (0.0, 0.0, 0.0, 0.0)


class TestOverlaps:
    """Smoke: overlaps returns True/False for disjoint vs intersecting nodes."""

    def test_disjoint_nodes(self):
        a = {"x": 0, "y": 0, "width": 50, "height": 50}
        b = {"x": 100, "y": 100, "width": 50, "height": 50}
        assert overlaps(a, b) is False

    def test_overlapping_nodes(self):
        a = {"x": 0, "y": 0, "width": 100, "height": 100}
        b = {"x": 50, "y": 50, "width": 100, "height": 100}
        assert overlaps(a, b) is True

    def test_edge_touch_with_default_tolerance_does_not_overlap(self):
        # Edge-touching nodes within 5px tolerance are NOT overlapping
        a = {"x": 0, "y": 0, "width": 100, "height": 100}
        b = {"x": 100, "y": 0, "width": 100, "height": 100}
        assert overlaps(a, b) is False


class TestDetectOverlaps:
    """Smoke: detect_overlaps returns a list of overlapping pairs."""

    def test_no_overlaps(self):
        nodes = [
            {"id": "a", "x": 0, "y": 0, "width": 50, "height": 50},
            {"id": "b", "x": 100, "y": 0, "width": 50, "height": 50},
        ]
        result = detect_overlaps(nodes)
        assert result == []

    def test_one_overlap(self):
        nodes = [
            {"id": "a", "x": 0, "y": 0, "width": 100, "height": 100},
            {"id": "b", "x": 50, "y": 50, "width": 100, "height": 100},
        ]
        result = detect_overlaps(nodes)
        assert len(result) == 1


class TestAlignmentScore:
    """Smoke: alignment_score returns a float in [0, 1] (or similar bounded range)."""

    def test_perfectly_aligned(self):
        nodes = [
            {"x": 0, "y": 0, "width": 100, "height": 100},
            {"x": 0, "y": 200, "width": 100, "height": 100},  # same x — aligned
            {"x": 0, "y": 400, "width": 100, "height": 100},
        ]
        score = alignment_score(nodes)
        assert isinstance(score, float)
        # Alignment of 3 left-edge-aligned nodes should be high
        assert 0.0 <= score <= 1.0

    def test_misaligned(self):
        nodes = [
            {"x": 0, "y": 0, "width": 100, "height": 100},
            {"x": 37, "y": 200, "width": 100, "height": 100},
            {"x": 91, "y": 400, "width": 100, "height": 100},
        ]
        score = alignment_score(nodes)
        assert isinstance(score, float)
        assert 0.0 <= score <= 1.0

    def test_empty_nodes(self):
        # Empty / single-element input must not crash
        score = alignment_score([])
        assert isinstance(score, float)


class TestContainmentCheck:
    """Smoke: containment_check returns IDs of children outside parent bounds."""

    def test_child_inside_parent(self):
        parent = {"id": "g1", "x": 0, "y": 0, "width": 1200, "height": 1100}
        children = [{"id": "n1", "x": 60, "y": 40, "width": 100, "height": 100}]
        outside_ids = containment_check(parent, children)
        assert outside_ids == []

    def test_child_outside_parent(self):
        parent = {"id": "g1", "x": 0, "y": 0, "width": 100, "height": 100}
        children = [{"id": "n1", "x": 500, "y": 500, "width": 50, "height": 50}]
        outside_ids = containment_check(parent, children)
        assert outside_ids == ["n1"]


class TestSpacingAnalysis:
    """Smoke: spacing_analysis returns a dict of metrics."""

    def test_returns_dict(self):
        nodes = [
            {"x": 0, "y": 0, "width": 100, "height": 100},
            {"x": 200, "y": 0, "width": 100, "height": 100},
            {"x": 400, "y": 0, "width": 100, "height": 100},
        ]
        result = spacing_analysis(nodes)
        assert isinstance(result, dict)


class TestStructuralSummary:
    """Smoke: structural_summary returns a dict combining the spatial metrics."""

    def test_returns_dict_with_keys(self):
        canvas = {
            "nodes": [
                {"id": "g1", "type": "group", "x": 0, "y": 0, "width": 1200, "height": 1100},
                {"id": "n1", "type": "text", "x": 60, "y": 40, "width": 100, "height": 100},
            ],
            "edges": [],
        }
        summary = structural_summary(canvas)
        assert isinstance(summary, dict)
        # Summary should be non-empty
        assert len(summary) > 0
