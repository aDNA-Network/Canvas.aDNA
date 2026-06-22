"""Tests for canvas_presentation (M-2a-01)."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_presentation import (
    PresentationBuilder,
    PRESENTATION_THEMES,
    NARRATIVE_ARCS,
    LayoutStrategy,
    SlideLayout,
    auto_select_layout,
    NarrativeArc,
)


class TestPresentationBuilder:
    def test_basic_build(self):
        pb = PresentationBuilder(name="test")
        pb.add_title_slide("Title", "Subtitle")
        pb.add_content_slide("Content", "Body text")
        canvas = pb.build()
        assert len(canvas["nodes"]) >= 4  # 2 groups + interior nodes
        assert len(pb.slides) == 2

    def test_all_16_slide_types(self):
        pb = PresentationBuilder(name="all_types")
        pb.add_title_slide("Title")
        pb.add_content_slide("Content", "body")
        pb.add_comparison_slide("Compare", "A", "Left", "B", "Right")
        pb.add_diagram_slide("Diagram", mermaid="graph TD\n  A-->B")
        pb.add_image_slide("Image", prompt="test")
        pb.add_quote_slide("Quote", "Test quote", "Author")
        pb.add_section_divider("Section")
        pb.add_stats_slide("Stats", [("42%", "Accuracy"), ("99%", "Uptime")])
        pb.add_video_slide("Video", "https://youtube.com/watch?v=test")
        pb.add_timeline_slide("Timeline", [("2024", "Start"), ("2025", "Mid")])
        pb.add_process_slide("Process", ["Step 1", "Step 2", "Step 3"])
        pb.add_three_column_slide("Columns", [("A", "a"), ("B", "b"), ("C", "c")])
        pb.add_key_value_slide("KV", [("Key1", "Val1"), ("Key2", "Val2")])
        pb.add_matrix_slide("Matrix", ["R1"], ["C1", "C2"], [["1", "2"]])
        pb.add_collage_slide("Collage", "hero.png", ["t1.png", "t2.png"])
        pb.add_media_slide("Media", source="test.png")
        assert len(pb.slides) == 16

    def test_theme_application(self):
        pb = PresentationBuilder(name="themed", theme="tokyo_night")
        pb.add_title_slide("Title")
        pb.add_content_slide("Content", "body")
        canvas = pb.build()
        # Title slide should get primary color (6)
        title_group = next(n for n in canvas["nodes"] if n.get("type") == "group" and n.get("isStartNode"))
        assert title_group.get("color") == "6"

    def test_audience_context(self):
        pb = PresentationBuilder(name="keynote", audience="keynote")
        assert pb._density_profile == "sparse"

    def test_narrative_arc(self):
        pb = PresentationBuilder(name="arc", arc="problem_solution")
        assert pb._arc is not None
        assert pb._arc.name == "problem_solution"

    def test_markdown_parser(self):
        md = "# My Deck\nSubtitle\n\n## Slide 1\nContent here\n\n## Slide 2\nMore content"
        pb = PresentationBuilder.from_markdown(md, name="parsed")
        assert len(pb.slides) == 3  # title + 2 content

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            pb = PresentationBuilder(name="save_test")
            pb.add_title_slide("Title")
            path = pb.save(Path(tmpdir) / "test.canvas")
            assert path.exists()
            with open(path) as f:
                data = json.load(f)
            assert "nodes" in data
            assert "edges" in data

    def test_navigation_edges(self):
        pb = PresentationBuilder(name="nav")
        pb.add_title_slide("Title")
        pb.add_content_slide("A", "a")
        pb.add_content_slide("B", "b")
        canvas = pb.build()
        assert len(canvas["edges"]) == 2  # title->A, A->B

    def test_review_24_criteria(self):
        pb = PresentationBuilder(name="review", theme="tokyo_night")
        pb.add_title_slide("Title", "Sub")
        pb.add_content_slide("Content", "Body text here with enough words")
        pb.add_stats_slide("Metrics", [("42%", "Growth")])
        report = pb.review()
        assert 0.0 <= report.score <= 1.0
        assert len(report.categories) == 5
        total_criteria = sum(len(cat.criteria) for cat in report.categories.values())
        assert total_criteria == 24
        assert report.grade in ("A", "B", "C", "D", "F")


class TestConfig:
    def test_themes_count(self):
        assert len(PRESENTATION_THEMES) == 7

    def test_arcs_count(self):
        assert len(NARRATIVE_ARCS) == 8

    def test_arc_from_brief(self):
        outline = NarrativeArc.from_brief("Test topic", "problem_solution")
        assert len(outline) >= 5
        assert outline[0]["type"] == "title"


class TestLayout:
    def test_auto_select_sparse(self):
        layout = auto_select_layout(3, "sparse")
        assert layout.columns == 1

    def test_auto_select_dense(self):
        layout = auto_select_layout(10, "dense")
        assert layout.columns == 3

    def test_slide_layout_content_width(self):
        sl = SlideLayout(name="test", slide_width=1200, margin_side=60)
        assert sl.content_width == 1080
