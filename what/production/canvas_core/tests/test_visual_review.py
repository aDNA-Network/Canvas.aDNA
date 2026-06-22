"""Tests for the visual review pipeline.

Covers: visual quality rubric, structural estimation, score parsing,
review prompt generation, and report output.

Migrated from `lattice-protocol/extensions/canvas/tests/test_visual_review.py`
under M-R5-01a (campaign_canvasforge_review). Pure substrate — no
canvas_presentation / canvas_comic imports. Substrate target:
`canvas_core/visual_review.py` (566 LOC).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import json

from canvas_core.visual_review import (
    VISUAL_CRITERIA,
    CanvasVisualScore,
    SlideVisualScore,
    VisualCriterionScore,
    VisualReviewReport,
    estimate_visual_scores,
    generate_review_prompt,
    parse_visual_review_response,
)

# ---------------------------------------------------------------------------
# Visual Criteria
# ---------------------------------------------------------------------------


class TestVisualCriteria:
    def test_five_criteria(self):
        assert len(VISUAL_CRITERIA) == 5

    def test_weights_sum_to_one(self):
        total = sum(c["weight"] for c in VISUAL_CRITERIA)
        assert abs(total - 1.0) < 0.01

    def test_all_have_ids(self):
        ids = {c["id"] for c in VISUAL_CRITERIA}
        assert ids == {"VR1", "VR2", "VR3", "VR4", "VR5"}

    def test_all_have_descriptions(self):
        for c in VISUAL_CRITERIA:
            assert len(c["description"]) > 20


# ---------------------------------------------------------------------------
# Score Data Types
# ---------------------------------------------------------------------------


class TestVisualCriterionScore:
    def test_basic(self):
        score = VisualCriterionScore(
            id="VR1",
            name="Text Readability",
            score=8.0,
            weight=0.25,
        )
        assert score.score == 8.0
        assert score.weight == 0.25


class TestCanvasVisualScore:
    def test_weighted_score(self):
        sv = CanvasVisualScore(node_index=1, node_label="Test", node_type="content")
        sv.criteria = [
            VisualCriterionScore("VR1", "A", 10.0, 0.5),
            VisualCriterionScore("VR2", "B", 6.0, 0.5),
        ]
        assert sv.weighted_score == 8.0

    def test_empty_score(self):
        sv = CanvasVisualScore(node_index=1, node_label="Test", node_type="content")
        assert sv.weighted_score == 0.0

    def test_min_criterion(self):
        sv = CanvasVisualScore(node_index=1, node_label="Test", node_type="content")
        sv.criteria = [
            VisualCriterionScore("VR1", "A", 9.0, 0.5),
            VisualCriterionScore("VR2", "B", 5.0, 0.5),
        ]
        assert sv.min_criterion == 5.0


class TestCanvasVisualScoreAlias:
    """M-V1-06 S1+S2: legacy class-name alias contract.

    S1 renamed `SlideVisualScore` → `CanvasVisualScore` and added the
    `SlideVisualScore = CanvasVisualScore` alias. S2 cascaded the field
    renames (slide_index/title/type → node_index/label/type) and shipped
    the topology-aware `_estimate_hierarchy()` plus application-pluggable
    `generate_review_prompt()`. The class-name alias still resolves; the
    legacy `slide_*` field/kwarg surface no longer exists.
    """

    def test_legacy_alias_resolves(self):
        # Legacy import path keeps working
        from canvas_core.visual_review import SlideVisualScore as Legacy
        from canvas_core.visual_review import CanvasVisualScore as Canonical
        assert Legacy is Canonical

    def test_legacy_class_name_constructs_via_new_kwargs(self):
        # Legacy class name still constructs — but only via canonical
        # node_* kwargs (S2 field rename means slide_* kwargs no longer exist).
        sv = SlideVisualScore(node_index=1, node_label="Test", node_type="content")
        assert sv.node_index == 1
        assert sv.node_label == "Test"
        assert sv.node_type == "content"


class TestVisualReviewReport:
    def test_aggregate_score(self):
        report = VisualReviewReport(title="Test")
        s1 = CanvasVisualScore(1, "A", "content")
        s1.criteria = [VisualCriterionScore("VR1", "A", 8.0, 1.0)]
        s2 = CanvasVisualScore(2, "B", "content")
        s2.criteria = [VisualCriterionScore("VR1", "A", 6.0, 1.0)]
        report.node_scores = [s1, s2]
        assert report.aggregate_score == 7.0

    def test_passes_threshold(self):
        report = VisualReviewReport(title="Test")
        s1 = CanvasVisualScore(1, "A", "content")
        s1.criteria = [VisualCriterionScore("VR1", "A", 8.0, 1.0)]
        report.node_scores = [s1]
        assert report.passes  # 8.0 >= 7.5

    def test_fails_threshold(self):
        report = VisualReviewReport(title="Test")
        s1 = CanvasVisualScore(1, "A", "content")
        s1.criteria = [VisualCriterionScore("VR1", "A", 5.0, 1.0)]
        report.node_scores = [s1]
        assert not report.passes  # 5.0 < 7.5

    def test_weakest_criterion(self):
        report = VisualReviewReport(title="Test")
        s1 = CanvasVisualScore(1, "A", "content")
        s1.criteria = [
            VisualCriterionScore("VR1", "Readability", 9.0, 0.5),
            VisualCriterionScore("VR2", "Hierarchy", 5.0, 0.5),
        ]
        report.node_scores = [s1]
        assert report.weakest_criterion == "Hierarchy"

    def test_to_markdown(self):
        report = VisualReviewReport(title="Test Deck")
        s1 = CanvasVisualScore(1, "Title Slide", "title")
        s1.criteria = [
            VisualCriterionScore("VR1", "Readability", 8.0, 0.25),
            VisualCriterionScore("VR2", "Hierarchy", 7.0, 0.25),
            VisualCriterionScore("VR3", "Whitespace", 9.0, 0.20),
            VisualCriterionScore("VR4", "Color", 7.5, 0.15),
            VisualCriterionScore("VR5", "Professional", 8.0, 0.15),
        ]
        report.node_scores = [s1]
        md = report.to_markdown()
        assert "Visual Quality Report" in md
        assert "Title Slide" in md

    def test_to_dict(self):
        report = VisualReviewReport(title="Test")
        s1 = CanvasVisualScore(1, "Slide", "content")
        s1.criteria = [VisualCriterionScore("VR1", "A", 7.0, 1.0)]
        report.node_scores = [s1]
        d = report.to_dict()
        # Output schema preserved at v1.0 ("slides"/"slide_count" top-level
        # keys + inner "title") for consumer-side backward compatibility.
        assert d["title"] == "Test"
        assert len(d["slides"]) == 1
        assert d["slides"][0]["weighted_score"] == 7.0
        assert d["slide_count"] == 1

    def test_empty_report(self):
        report = VisualReviewReport(title="Empty")
        assert report.aggregate_score == 0.0
        assert report.min_slide_score == 0.0


# ---------------------------------------------------------------------------
# Structural Visual Estimation
# ---------------------------------------------------------------------------


class TestStructuralEstimation:
    def test_basic_estimation(self):
        slides = [
            {"id": "s1", "type": "title", "title": "Hello", "node_ids": ["n1"]},
        ]
        canvas = {
            "nodes": [
                {"id": "s1", "type": "group", "x": 0, "y": 0, "width": 1200, "height": 1100},
                {
                    "id": "n1",
                    "type": "text",
                    "text": "Hello World",
                    "x": 60,
                    "y": 40,
                    "width": 1080,
                    "height": 200,
                },
            ],
        }
        report = estimate_visual_scores(slides, canvas)
        assert len(report.node_scores) == 1
        assert report.node_scores[0].weighted_score > 0

    def test_multiple_slides(self):
        slides = [
            {"id": "s1", "type": "title", "title": "T", "node_ids": ["n1"]},
            {"id": "s2", "type": "content", "title": "C", "node_ids": ["n2"]},
        ]
        canvas = {
            "nodes": [
                {"id": "s1", "type": "group", "width": 1200, "height": 1100, "x": 0, "y": 0},
                {
                    "id": "n1",
                    "type": "text",
                    "text": "Title",
                    "x": 60,
                    "y": 40,
                    "width": 1080,
                    "height": 200,
                },
                {"id": "s2", "type": "group", "width": 1200, "height": 1100, "x": 1400, "y": 0},
                {
                    "id": "n2",
                    "type": "text",
                    "text": "Body content here",
                    "x": 1460,
                    "y": 180,
                    "width": 1080,
                    "height": 600,
                },
            ],
        }
        report = estimate_visual_scores(slides, canvas)
        assert len(report.node_scores) == 2

    def test_no_canvas_data(self):
        slides = [
            {"id": "s1", "type": "content", "title": "Test", "node_ids": []},
        ]
        report = estimate_visual_scores(slides)
        assert len(report.node_scores) == 1
        # Should still produce scores using defaults
        assert report.node_scores[0].weighted_score > 0

    def test_review_method(self):
        report = estimate_visual_scores(
            [
                {"id": "s1", "type": "title", "title": "T", "node_ids": []},
            ]
        )
        assert report.review_method == "structural_estimate"

    def test_custom_hierarchy_hints(self):
        """Application-supplied hierarchy_hints override the deck-canonical defaults."""
        slides = [
            {"id": "p1", "type": "comic_cover", "title": "Cover", "node_ids": ["n1"]},
        ]
        canvas = {
            "nodes": [
                {"id": "p1", "type": "group", "x": 0, "y": 0, "width": 1200, "height": 1100},
                {"id": "n1", "type": "text", "text": "Cover Art",
                 "x": 60, "y": 40, "width": 1080, "height": 200},
            ],
        }
        report = estimate_visual_scores(
            slides, canvas,
            hierarchy_hints={"comic_cover": 9.5},
        )
        # VR2 score for the cover node should reflect the custom hint.
        vr2 = next(c for c in report.node_scores[0].criteria if c.id == "VR2")
        assert vr2.score == 9.5

    def test_unknown_type_falls_back_to_ratio(self):
        """Node type with no hint registered falls through to ratio-based estimation."""
        slides = [
            {"id": "x", "type": "topology_node", "title": "Net", "node_ids": ["a", "b"]},
        ]
        canvas = {
            "nodes": [
                {"id": "x", "type": "group", "width": 1200, "height": 1100, "x": 0, "y": 0},
                {"id": "a", "type": "text", "text": "A",
                 "width": 1000, "height": 800, "x": 60, "y": 40},
                {"id": "b", "type": "text", "text": "B",
                 "width": 1000, "height": 100, "x": 60, "y": 900},
            ],
        }
        report = estimate_visual_scores(slides, canvas)  # no hints → DEFAULT_HIERARCHY_HINTS
        vr2 = next(c for c in report.node_scores[0].criteria if c.id == "VR2")
        # Ratio max(800)/min(100) = 8.0 → falls in the >= 2.0 band → 9.0.
        assert vr2.score == 9.0


# ---------------------------------------------------------------------------
# Review Prompt Generation
# ---------------------------------------------------------------------------


class TestReviewPrompt:
    def test_generates_prompt(self):
        prompt = generate_review_prompt("Title Slide", "title")
        assert "Title Slide" in prompt
        assert "title" in prompt
        assert "VR1" in prompt or "Text Readability" in prompt

    def test_includes_criteria(self):
        prompt = generate_review_prompt("Test", "content")
        assert "Visual Hierarchy" in prompt
        assert "Whitespace" in prompt
        assert "Professional" in prompt

    def test_includes_json_format(self):
        prompt = generate_review_prompt("Test", "content")
        assert "JSON" in prompt or "json" in prompt

    def test_application_pluggable_domain_noun(self):
        """domain_noun and item_label override deck-canonical language."""
        prompt = generate_review_prompt(
            "Cover Art", "comic_cover",
            domain_noun="comic page", item_label="Page",
        )
        assert "comic page" in prompt
        assert "**Page**" in prompt
        assert "presentation slide" not in prompt
        assert "Cover Art" in prompt

    def test_default_application_context_preserves_deck_language(self):
        """No application context → deck-canonical wording preserved."""
        prompt = generate_review_prompt("Title", "title")
        assert "presentation slide" in prompt
        assert "**Slide**" in prompt


# ---------------------------------------------------------------------------
# Response Parsing
# ---------------------------------------------------------------------------


class TestResponseParsing:
    def test_valid_json(self):
        response = json.dumps(
            {
                "VR1": {"score": 8.0, "notes": "Good readability"},
                "VR2": {"score": 7.0, "notes": "Clear hierarchy"},
                "VR3": {"score": 9.0, "notes": "Great whitespace"},
                "VR4": {"score": 7.5, "notes": "Colors work well"},
                "VR5": {"score": 8.0, "notes": "Professional look"},
            }
        )
        score = parse_visual_review_response(response, 1, "Test", "content")
        assert len(score.criteria) == 5
        assert score.criteria[0].score == 8.0

    def test_json_in_code_block(self):
        response = '```json\n{"VR1": {"score": 7.0, "notes": "ok"}}\n```'
        score = parse_visual_review_response(response, 1, "Test", "content")
        assert len(score.criteria) >= 1

    def test_invalid_json_fallback(self):
        response = "This is not JSON at all"
        score = parse_visual_review_response(response, 1, "Test", "content")
        assert len(score.criteria) == 5  # Falls back to defaults
        assert all(c.score == 5.0 for c in score.criteria)

    def test_scores_clamped(self):
        response = json.dumps(
            {
                "VR1": {"score": 15.0, "notes": "too high"},
                "VR2": {"score": -5.0, "notes": "too low"},
                "VR3": {"score": 7.0, "notes": "normal"},
                "VR4": {"score": 7.0, "notes": "normal"},
                "VR5": {"score": 7.0, "notes": "normal"},
            }
        )
        score = parse_visual_review_response(response, 1, "Test", "content")
        for c in score.criteria:
            assert 0.0 <= c.score <= 10.0
