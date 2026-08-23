"""Tests for ComicPageBuilder.review() — M07 structural scoring.

Migrated from `lattice-protocol/extensions/canvas/tests/test_comic_review.py`
under M-R5-01a (campaign_canvasforge_review). Complementary to canonical
`canvas_comic/tests/test_comic_builder.py::test_review_scoring` — that test
covers a single happy-path review() call; this file covers empty-comic, structural,
panel-variety, idempotent, grade boundaries, and M08 variant-selection flow.
"""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import shutil
import tempfile
import unittest
from pathlib import Path

from canvas_comic.comic import ComicPageBuilder, ComicReport, ContextPack


def _make_test_context_pack(tmp_dir: Path) -> ContextPack:
    """Create 5 sentinel files in tmp_dir and return a ContextPack."""
    fields = (
        "storyboard_canvas",
        "character_bible",
        "color_theory",
        "prompt_engineering",
        "voice_foundations",
    )
    kwargs: dict[str, Path] = {}
    for f in fields:
        p = tmp_dir / f"{f}.md"
        p.write_text(f"# Sentinel {f}\n")
        kwargs[f] = p
    return ContextPack(**kwargs)


class TestComicReviewEmpty(unittest.TestCase):
    """review() on an empty comic."""

    def test_empty_comic_fails(self):
        cpb = ComicPageBuilder("empty", "1.0", 662.5, 1025.0, "pixel_art_ghibli")
        report = cpb.review()
        self.assertIsInstance(report, ComicReport)
        self.assertEqual(report.score, 0.0)
        self.assertEqual(report.grade, "F")
        self.assertFalse(report.passed)
        self.assertEqual(report.page_count, 0)
        self.assertEqual(report.panel_count, 0)


class TestComicReviewStructural(unittest.TestCase):
    """Structural scoring invariants."""

    def setUp(self):
        self.cpb = ComicPageBuilder("test_issue", "1.0", 662.5, 1025.0, "pixel_art_ghibli")

    def test_pages_without_panels_flagged(self):
        self.cpb.add_page(1, 1)
        self.cpb.add_page(2, 1)
        report = self.cpb.review()
        panel_issues = [i for i in report.issues if "no panels" in i]
        self.assertEqual(len(panel_issues), 2)

    def test_missing_scene_descriptions_flagged(self):
        p1 = self.cpb.add_page(1, 1)
        self.cpb.standard_grid(p1, 2, 2, "action")
        report = self.cpb.review()
        desc_issues = [i for i in report.issues if "missing scene descriptions" in i]
        self.assertTrue(len(desc_issues) > 0)

    def test_full_issue_scores_higher(self):
        # Build a 30-page issue with content
        for i in range(1, 31):
            pid = self.cpb.add_page(i, (i + 1) // 2)
            panels = self.cpb.standard_grid(pid, 2, 2, "action" if i % 2 else "dialogue")
            for panel_id in panels:
                self.cpb.set_panel_content(
                    panel_id,
                    f"Scene {i} test description",
                    "medium_shot",
                    characters=["Stanley"],
                    mood="calm",
                )
        report = self.cpb.review()
        self.assertGreater(report.score, 0.5)
        self.assertEqual(report.page_count, 30)
        self.assertEqual(report.panel_count, 120)
        # Page count in range (28-34) should give s1=1.0
        self.assertGreaterEqual(report.structural_score, 0.9)

    def test_panel_type_variety_rewards_diversity(self):
        p1 = self.cpb.add_page(1, 1)
        self.cpb.add_panel(p1, 0, 0, 1, 1, False, "action")
        self.cpb.add_panel(p1, 0, 1, 1, 1, False, "dialogue")
        self.cpb.add_panel(p1, 1, 0, 1, 1, False, "establishing")
        self.cpb.add_panel(p1, 1, 1, 1, 1, False, "close_up")
        report = self.cpb.review()
        # 4+ types should give s3=1.0
        self.assertGreaterEqual(report.structural_score, 0.5)


class TestComicReviewIdempotent(unittest.TestCase):
    """review() is idempotent — calling it twice gives same result."""

    def test_review_idempotent(self):
        cpb = ComicPageBuilder("test", "1.0", 662.5, 1025.0, "pixel_art_ghibli")
        p1 = cpb.add_page(1, 1)
        cpb.standard_grid(p1, 2, 2, "action")
        r1 = cpb.review()
        r2 = cpb.review()
        self.assertEqual(r1.score, r2.score)
        self.assertEqual(r1.issues, r2.issues)
        self.assertEqual(r1.grade, r2.grade)


class TestComicReportGrades(unittest.TestCase):
    """Grade boundaries."""

    def test_grade_a(self):
        r = ComicReport(score=0.92)
        self.assertEqual(r.grade, "A")
        self.assertTrue(r.passed)

    def test_grade_b(self):
        r = ComicReport(score=0.85)
        self.assertEqual(r.grade, "B")
        self.assertTrue(r.passed)

    def test_grade_c(self):
        r = ComicReport(score=0.75)
        self.assertEqual(r.grade, "C")
        self.assertFalse(r.passed)

    def test_grade_f(self):
        r = ComicReport(score=0.3)
        self.assertEqual(r.grade, "F")
        self.assertFalse(r.passed)


class TestComicVariantSelection(unittest.TestCase):
    """M08: Variant selection flow integration tests."""

    def setUp(self):
        self._tmp_dir = Path(tempfile.mkdtemp(prefix="canvasforge_review_"))
        self._ctx_pack = _make_test_context_pack(self._tmp_dir)
        self.cpb = ComicPageBuilder(
            "variant_test", "1.0", 662.5, 1025.0, "pixel_art_ghibli",
            context_pack=self._ctx_pack,
        )
        p1 = self.cpb.add_page(1, 1)
        panels = self.cpb.standard_grid(p1, 2, 2, "action")
        self.panel_id = panels[0]
        self.cpb.set_panel_content(
            self.panel_id, "A hero shot of Stanley in the lab", "wide_shot",
            characters=["Stanley"], mood="determined",
        )

    def tearDown(self):
        shutil.rmtree(self._tmp_dir, ignore_errors=True)

    def test_prepare_panel_generation(self):
        pending = self.cpb.prepare_panel_generation(self.panel_id)
        self.assertEqual(pending.panel_id, self.panel_id)
        self.assertEqual(pending.status, "pending")
        self.assertIn("hero shot", pending.prompt)
        self.assertIn(pending, self.cpb.pending_panels)

    def test_resolve_panel_clears_pending(self):
        self.cpb.prepare_panel_generation(self.panel_id)
        self.cpb.resolve_panel(self.panel_id, "/tmp/fake_panel.png")
        panel = self.cpb.get_panel(self.panel_id)
        self.assertEqual(panel.image_path, "/tmp/fake_panel.png")
        self.assertEqual(len(self.cpb.pending_panels), 0)

    def test_generate_panel_variants_returns_canvas(self):
        from canvas_core import CanvasBuilder
        board = self.cpb.generate_panel_variants(
            self.panel_id,
            ["/tmp/v1.png", "/tmp/v2.png", "/tmp/v3.png"],
            ["Variant A", "Variant B", "Variant C"],
        )
        self.assertIsInstance(board, CanvasBuilder)

    def test_regenerate_panel_resets_state(self):
        self.cpb.prepare_panel_generation(self.panel_id)
        self.cpb.resolve_panel(self.panel_id, "/tmp/old.png")
        pending = self.cpb.regenerate_panel(self.panel_id)
        self.assertEqual(pending.status, "pending")
        panel = self.cpb.get_panel(self.panel_id)
        self.assertIsNone(panel.image_path)

    def test_full_variant_flow(self):
        """End-to-end: prepare → variants → resolve → review scores production."""
        pending = self.cpb.prepare_panel_generation(self.panel_id)
        self.assertEqual(pending.status, "pending")

        variant_paths = ["/tmp/v1.png", "/tmp/v2.png", "/tmp/v3.png"]
        board = self.cpb.generate_panel_variants(self.panel_id, variant_paths)
        self.assertIsNotNone(board)

        self.cpb.resolve_panel(self.panel_id, "/tmp/v2.png")
        panel = self.cpb.get_panel(self.panel_id)
        self.assertEqual(panel.image_path, "/tmp/v2.png")

        report = self.cpb.review()
        self.assertGreater(report.production_score, 0.0)


if __name__ == "__main__":
    unittest.main()
