"""Tests for the accessibility scoring category (A1-A4) in PresentationBuilder.review().

Mission: campaign_canvas_visual_command / mission_cvc_m04 (upstream).
Migrated from `lattice-protocol/extensions/canvas/tests/test_canvas_accessibility.py`
under M-R5-01a (campaign_canvasforge_review). The substrate WCAG-utility slice
(TestWCAGContrastUtilities) is at `canvas_core/tests/test_wcag_utilities.py`;
this file holds the deck-application slice (TestAccessibilityCategoryInReview)
which uses PresentationBuilder.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import unittest

from canvas_presentation.presentation import PresentationBuilder


class TestAccessibilityCategoryInReview(unittest.TestCase):
    """Verify A1-A4 criteria appear in review() output."""

    def _make_builder(self, **kwargs):
        defaults = dict(name="test", version="1.0", theme="scientific", audience="pitch")
        defaults.update(kwargs)
        pb = PresentationBuilder(**defaults)
        pb.add_title_slide("Test Title")
        pb.add_content_slide("Body", "Some content here for testing.")
        return pb

    def test_review_includes_accessibility_category(self):
        pb = self._make_builder()
        report = pb.review()
        self.assertIn("accessibility", report.categories)
        cat = report.categories["accessibility"]
        ids = [c.id for c in cat.criteria]
        self.assertEqual(ids, ["A1", "A2", "A3", "A4"])

    def test_a1_alt_text_missing_lowers_score(self):
        pb = self._make_builder()
        pb.add_image_slide("Visual", image_path="test.png")  # no alt_text
        report = pb.review()
        a1 = next(c for c in report.categories["accessibility"].criteria if c.id == "A1")
        self.assertLess(a1.score, 1.0)
        self.assertTrue(any("alt text" in i.lower() for i in a1.issues))

    def test_a1_alt_text_present_passes(self):
        pb = self._make_builder()
        pb.add_image_slide("Visual", image_path="test.png", alt_text="A test image")
        report = pb.review()
        a1 = next(c for c in report.categories["accessibility"].criteria if c.id == "A1")
        self.assertEqual(a1.score, 1.0)
        self.assertEqual(a1.issues, [])

    def test_a4_contrast_passes_for_scientific_theme(self):
        pb = self._make_builder(theme="scientific")
        report = pb.review()
        a4 = next(c for c in report.categories["accessibility"].criteria if c.id == "A4")
        self.assertEqual(a4.score, 1.0)

    def test_a2_heading_hierarchy_passes_clean_deck(self):
        pb = self._make_builder()
        report = pb.review()
        a2 = next(c for c in report.categories["accessibility"].criteria if c.id == "A2")
        self.assertEqual(a2.score, 1.0)

    def test_accessibility_category_does_not_break_aggregate(self):
        """Adding accessibility as 5th category should not crash or produce NaN."""
        pb = self._make_builder()
        report = pb.review()
        self.assertGreater(report.score, 0.0)
        self.assertLessEqual(report.score, 1.0)
        self.assertEqual(len(report.categories), 5)


if __name__ == "__main__":
    unittest.main()
