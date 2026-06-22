"""Tests for the visual inspection pipeline.

Covers: screenshot preparation, review report building,
comparison reports, and the visual_inspect orchestration.

Migrated from `lattice-protocol/extensions/canvas/tests/test_visual_inspector.py`
under M-R5-01a (campaign_canvasforge_review). Pure substrate — no
canvas_presentation / canvas_comic imports. Substrate target:
`canvas_core/visual_inspector.py` (540 LOC).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import json
from pathlib import Path

import pytest

from canvas_core.visual_inspector import (
    ScreenshotBatch,
    ScreenshotResult,
    automated_vr_score,
    batch_score,
    build_automated_report,
    build_review_report,
    compare_reviews,
    multi_theme_render,
    prepare_screenshots,
    save_review_report,
    slide_urls,
    visual_inspect,
)
from canvas_core.visual_review import (
    CanvasVisualScore,
    VisualCriterionScore,
    VisualReviewReport,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def minimal_canvas():
    return {
        "nodes": [
            {
                "id": "g1",
                "type": "group",
                "x": 0,
                "y": 0,
                "width": 1200,
                "height": 1100,
                "color": "6",
                "label": "Title Slide",
            },
            {
                "id": "n1",
                "type": "text",
                "x": 60,
                "y": 40,
                "width": 1080,
                "height": 200,
                "text": "# Hello",
                "styleAttributes": {"textAlign": "center", "cssclasses": "hero"},
            },
        ],
        "edges": [],
        "metadata": {"startNode": "g1"},
    }


@pytest.fixture
def canvas_file(minimal_canvas, tmp_path):
    p = tmp_path / "test_deck.canvas"
    p.write_text(json.dumps(minimal_canvas))
    return p


# ---------------------------------------------------------------------------
# Screenshot Preparation
# ---------------------------------------------------------------------------


class TestPrepareScreenshots:
    def test_creates_directories(self, canvas_file, tmp_path):
        output = tmp_path / "output"
        prepare_screenshots(canvas_file, output)
        assert (output / "html").is_dir()
        assert (output / "screenshots").is_dir()

    def test_returns_batch(self, canvas_file, tmp_path):
        batch = prepare_screenshots(canvas_file, tmp_path / "output")
        assert isinstance(batch, ScreenshotBatch)
        assert batch.title == "test_deck"
        assert len(batch.slides) == 1

    def test_html_files_created(self, canvas_file, tmp_path):
        output = tmp_path / "output"
        batch = prepare_screenshots(canvas_file, output)
        for slide in batch.slides:
            assert slide.html_path.exists()
            content = slide.html_path.read_text()
            assert "<!DOCTYPE html>" in content

    def test_screenshot_paths_set(self, canvas_file, tmp_path):
        batch = prepare_screenshots(canvas_file, tmp_path / "output")
        for slide in batch.slides:
            assert slide.screenshot_path is not None
            assert str(slide.screenshot_path).endswith(".png")

    def test_slide_metadata(self, canvas_file, tmp_path):
        batch = prepare_screenshots(canvas_file, tmp_path / "output")
        slide = batch.slides[0]
        assert slide.slide_title == "Title Slide"
        assert slide.slide_index == 0


class TestScreenshotBatch:
    def test_success_count(self):
        batch = ScreenshotBatch(title="test", output_dir=Path("/tmp"))
        batch.slides = [
            ScreenshotResult(0, "A", "title", Path("a.html"), screenshot_path=Path("a.png")),
            ScreenshotResult(
                1, "B", "content", Path("b.html"), screenshot_path=None, error="failed"
            ),
        ]
        assert batch.success_count == 1

    def test_screenshot_paths(self):
        batch = ScreenshotBatch(title="test", output_dir=Path("/tmp"))
        batch.slides = [
            ScreenshotResult(0, "A", "title", Path("a.html"), screenshot_path=Path("a.png")),
            ScreenshotResult(1, "B", "content", Path("b.html"), screenshot_path=Path("b.png")),
        ]
        assert len(batch.screenshot_paths) == 2


# ---------------------------------------------------------------------------
# Slide URLs
# ---------------------------------------------------------------------------


class TestSlideUrls:
    def test_generates_urls(self, canvas_file, tmp_path):
        batch = prepare_screenshots(canvas_file, tmp_path / "output")
        urls = slide_urls(batch, port=9999)
        assert len(urls) == 1
        assert urls[0]["url"].startswith("http://127.0.0.1:9999/")
        assert urls[0]["title"] == "Title Slide"

    def test_custom_port(self, canvas_file, tmp_path):
        batch = prepare_screenshots(canvas_file, tmp_path / "output")
        urls = slide_urls(batch, port=3000)
        assert "3000" in urls[0]["url"]


# ---------------------------------------------------------------------------
# Visual Inspect Orchestration
# ---------------------------------------------------------------------------


class TestVisualInspect:
    def test_returns_package(self, canvas_file, tmp_path):
        output = tmp_path / "output"
        result = visual_inspect(canvas_file, output)

        assert result["title"] == "test_deck"
        assert result["slide_count"] == 1
        assert len(result["slides"]) == 1
        assert len(result["prompts"]) == 1

    def test_prompts_contain_criteria(self, canvas_file, tmp_path):
        result = visual_inspect(canvas_file, tmp_path / "output")
        prompt = result["prompts"][0]["prompt"]
        assert "VR1" in prompt or "Text Readability" in prompt

    def test_output_paths(self, canvas_file, tmp_path):
        output = tmp_path / "output"
        result = visual_inspect(canvas_file, output)
        assert result["report_path"].endswith("_visual_review.md")
        assert result["json_path"].endswith("_visual_review.json")


# ---------------------------------------------------------------------------
# Review Report Building
# ---------------------------------------------------------------------------


class TestBuildReviewReport:
    def test_basic_build(self):
        scores = [
            {
                "slide_index": 1,
                "slide_title": "Title",
                "slide_type": "title",
                "scores": {
                    "VR1": {"name": "Text Readability", "score": 8.0, "notes": "Good"},
                    "VR2": {"name": "Visual Hierarchy", "score": 7.0, "notes": "OK"},
                    "VR3": {"name": "Whitespace Quality", "score": 9.0, "notes": "Great"},
                    "VR4": {"name": "Color Harmony", "score": 7.5, "notes": "Fine"},
                    "VR5": {"name": "Professional Appearance", "score": 8.0, "notes": "Clean"},
                },
            },
        ]
        report = build_review_report("Test Deck", scores)
        assert len(report.node_scores) == 1
        assert report.aggregate_score > 7.0
        assert report.review_method == "playwright_visual"

    def test_json_string_scores(self):
        json_str = json.dumps(
            {
                "VR1": {"score": 8.0, "notes": "ok"},
                "VR2": {"score": 7.0, "notes": "ok"},
                "VR3": {"score": 9.0, "notes": "ok"},
                "VR4": {"score": 7.5, "notes": "ok"},
                "VR5": {"score": 8.0, "notes": "ok"},
            }
        )
        scores = [
            {
                "slide_index": 1,
                "slide_title": "Test",
                "slide_type": "content",
                "scores": json_str,
            }
        ]
        report = build_review_report("Test", scores)
        assert len(report.node_scores) == 1
        assert report.node_scores[0].criteria[0].score == 8.0


# ---------------------------------------------------------------------------
# Save Report
# ---------------------------------------------------------------------------


class TestSaveReport:
    def test_saves_files(self, tmp_path):
        report = VisualReviewReport(title="Test Deck")
        s1 = CanvasVisualScore(1, "Slide", "content")
        s1.criteria = [
            VisualCriterionScore("VR1", "A", 8.0, 0.25),
        ]
        report.node_scores = [s1]

        md_path, json_path = save_review_report(report, tmp_path)
        assert md_path.exists()
        assert json_path.exists()
        assert "Visual Quality Report" in md_path.read_text()

        data = json.loads(json_path.read_text())
        assert data["title"] == "Test Deck"


# ---------------------------------------------------------------------------
# Compare Reviews
# ---------------------------------------------------------------------------


class TestCompareReviews:
    def _make_report(self, score: float) -> VisualReviewReport:
        r = VisualReviewReport(title="Test")
        s = CanvasVisualScore(1, "Slide", "content")
        s.criteria = [
            VisualCriterionScore("VR1", "A", score, 0.25),
            VisualCriterionScore("VR2", "B", score, 0.25),
            VisualCriterionScore("VR3", "C", score, 0.20),
            VisualCriterionScore("VR4", "D", score, 0.15),
            VisualCriterionScore("VR5", "E", score, 0.15),
        ]
        r.node_scores = [s]
        return r

    def test_improvement(self):
        before = self._make_report(5.0)
        after = self._make_report(8.0)
        result = compare_reviews(before, after)
        assert result["aggregate_change"] == 3.0
        assert result["after_passes"] is True
        assert result["before_passes"] is False

    def test_no_change(self):
        report = self._make_report(7.0)
        result = compare_reviews(report, report)
        assert result["aggregate_change"] == 0.0

    def test_per_slide_deltas(self):
        before = self._make_report(6.0)
        after = self._make_report(9.0)
        result = compare_reviews(before, after)
        assert len(result["slides"]) == 1
        assert result["slides"][0]["change"] == 3.0
        assert result["slides"][0]["criteria"]["VR1"] == 3.0


# ---------------------------------------------------------------------------
# Automated VR Scoring
# ---------------------------------------------------------------------------


class TestAutomatedVrScore:
    """Verify automated scoring request preparation."""

    def test_returns_prompt_and_path(self, tmp_path):
        screenshot = tmp_path / "slide.png"
        screenshot.write_bytes(b"fake-png")
        result = automated_vr_score(screenshot, "Title Slide", "title")
        assert result["screenshot_path"] == str(screenshot)
        assert "VR1" in result["prompt"] or "Text Readability" in result["prompt"]
        assert result["slide_title"] == "Title Slide"
        assert result["slide_type"] == "title"

    def test_default_slide_type(self, tmp_path):
        screenshot = tmp_path / "slide.png"
        screenshot.write_bytes(b"fake-png")
        result = automated_vr_score(screenshot)
        assert result["slide_type"] == "content"


class TestBatchScore:
    """Verify batch scoring request generation."""

    def test_generates_requests_for_existing_screenshots(self, tmp_path):
        batch = ScreenshotBatch(title="test", output_dir=tmp_path)
        # Create a real screenshot file
        ss_path = tmp_path / "slide_01.png"
        ss_path.write_bytes(b"fake-png")
        batch.slides = [
            ScreenshotResult(0, "Title", "title", Path("a.html"), screenshot_path=ss_path),
            ScreenshotResult(
                1, "Content", "content", Path("b.html"), screenshot_path=tmp_path / "missing.png"
            ),
        ]
        requests = batch_score(batch)
        assert len(requests) == 1  # Only existing screenshot
        assert requests[0]["slide_index"] == 0
        assert "prompt" in requests[0]

    def test_empty_batch(self):
        batch = ScreenshotBatch(title="empty", output_dir=Path("/tmp"))
        requests = batch_score(batch)
        assert requests == []


class TestBuildAutomatedReport:
    """Verify automated report construction from Gemini responses."""

    def test_builds_report_from_json_responses(self):
        responses = [
            {
                "slide_index": 1,
                "slide_title": "Title",
                "slide_type": "title",
                "response": json.dumps(
                    {
                        "VR1": {"score": 8.5, "notes": "Clear text"},
                        "VR2": {"score": 8.0, "notes": "Good hierarchy"},
                        "VR3": {"score": 9.0, "notes": "Nice spacing"},
                        "VR4": {"score": 7.5, "notes": "Harmonious"},
                        "VR5": {"score": 8.0, "notes": "Professional"},
                    }
                ),
            },
        ]
        report = build_automated_report("Test Deck", responses)
        assert report.review_method == "gemini_automated"
        assert len(report.node_scores) == 1
        assert report.aggregate_score > 7.5

    def test_handles_malformed_response(self):
        responses = [
            {
                "slide_index": 1,
                "slide_title": "Bad",
                "slide_type": "content",
                "response": "not valid json",
            },
        ]
        report = build_automated_report("Test", responses)
        assert len(report.node_scores) == 1
        # Should fallback to default scores (5.0)
        assert report.node_scores[0].weighted_score == 5.0


# ---------------------------------------------------------------------------
# Multi-Theme Render
# ---------------------------------------------------------------------------


class TestMultiThemeRender:
    """Verify multi-theme rendering produces batches for all themes."""

    def test_renders_all_themes(self, canvas_file, tmp_path):
        output = tmp_path / "multi_theme"
        results = multi_theme_render(canvas_file, output)
        assert len(results) == 8  # All 8 themes
        for _name, batch in results.items():
            assert isinstance(batch, ScreenshotBatch)
            assert len(batch.slides) == 1

    def test_renders_subset_of_themes(self, canvas_file, tmp_path):
        output = tmp_path / "multi_theme"
        results = multi_theme_render(
            canvas_file,
            output,
            theme_names=["tokyo_night", "lattice_light"],
        )
        assert len(results) == 2
        assert "tokyo_night" in results
        assert "lattice_light" in results

    def test_theme_directories_created(self, canvas_file, tmp_path):
        output = tmp_path / "multi_theme"
        multi_theme_render(
            canvas_file,
            output,
            theme_names=["tokyo_night"],
        )
        assert (output / "tokyo_night" / "html").is_dir()
