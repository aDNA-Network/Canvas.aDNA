"""Tests for WCAG contrast utilities (substrate slice).

Covers `canvas_core.design_tokens`: hex_to_rgb, relative_luminance,
contrast_ratio, check_wcag_aa.

Migrated from `lattice-protocol/extensions/canvas/tests/test_canvas_accessibility.py`
under M-R5-01a (campaign_canvasforge_review). The substrate slice (TestWCAGContrastUtilities)
lives here; the deck-application slice (TestAccessibilityCategoryInReview, which uses
PresentationBuilder) is migrated to `canvas_presentation/tests/test_accessibility_category.py`
to preserve substrate-neutrality (canvas_core/tests/ MUST NOT import canvas_presentation).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import unittest

from canvas_core.design_tokens import (
    check_wcag_aa,
    contrast_ratio,
    hex_to_rgb,
    relative_luminance,
)


class TestWCAGContrastUtilities(unittest.TestCase):
    """Verify WCAG 2.1 contrast ratio calculations against known reference values."""

    def test_hex_to_rgb_basic(self):
        self.assertEqual(hex_to_rgb("#000000"), (0, 0, 0))
        self.assertEqual(hex_to_rgb("#ffffff"), (255, 255, 255))
        self.assertEqual(hex_to_rgb("#ff0000"), (255, 0, 0))

    def test_hex_to_rgb_rejects_invalid(self):
        with self.assertRaises(ValueError):
            hex_to_rgb("#fff")
        with self.assertRaises(ValueError):
            hex_to_rgb("red")

    def test_relative_luminance_extremes(self):
        self.assertAlmostEqual(relative_luminance("#000000"), 0.0, places=4)
        self.assertAlmostEqual(relative_luminance("#ffffff"), 1.0, places=4)

    def test_contrast_ratio_black_white(self):
        ratio = contrast_ratio("#000000", "#ffffff")
        self.assertAlmostEqual(ratio, 21.0, delta=0.1)

    def test_contrast_ratio_same_color(self):
        ratio = contrast_ratio("#abcdef", "#abcdef")
        self.assertAlmostEqual(ratio, 1.0, delta=0.01)

    def test_contrast_ratio_is_symmetric(self):
        r1 = contrast_ratio("#2c2c2c", "#fafaf8")
        r2 = contrast_ratio("#fafaf8", "#2c2c2c")
        self.assertAlmostEqual(r1, r2, places=4)

    def test_contrast_ratio_always_gte_one(self):
        ratio = contrast_ratio("#888888", "#999999")
        self.assertGreaterEqual(ratio, 1.0)

    def test_check_wcag_aa_large_text_threshold(self):
        """AA large text requires 3:1."""
        self.assertTrue(check_wcag_aa("#ffffff", "#555555", large_text=True))
        self.assertFalse(check_wcag_aa("#eeeeee", "#ffffff", large_text=True))

    def test_check_wcag_aa_normal_text_threshold(self):
        """AA normal text requires 4.5:1."""
        self.assertTrue(check_wcag_aa("#2c2c2c", "#fafaf8", large_text=False))
        self.assertFalse(check_wcag_aa("#999999", "#ffffff", large_text=False))

    def test_scientific_theme_text_passes_aa(self):
        """Scientific theme: #2c2c2c on #fafaf8 should pass both AA levels."""
        ratio = contrast_ratio("#2c2c2c", "#fafaf8")
        self.assertGreater(ratio, 4.5, f"Scientific theme text contrast {ratio:.1f}:1 < 4.5:1")
        self.assertTrue(check_wcag_aa("#2c2c2c", "#fafaf8", large_text=False))
        self.assertTrue(check_wcag_aa("#2c2c2c", "#fafaf8", large_text=True))

    def test_scientific_theme_dim_text_passes_aa_large(self):
        """Scientific theme dim text: #6b6b6b on #fafaf8 should pass AA large."""
        self.assertTrue(check_wcag_aa("#6b6b6b", "#fafaf8", large_text=True))


if __name__ == "__main__":
    unittest.main()
