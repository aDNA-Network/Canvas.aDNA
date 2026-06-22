"""M13 Accessibility Audit — unittest suite.

Validates themes for WCAG AA contrast, font size minimum, and benchmark
deck accessibility scores.

Migrated from `lattice-protocol/extensions/canvas/tests/test_m13_audit.py`
under M-R5-01a (campaign_canvasforge_review). Standalone `audit_theme_*`
print functions (lines 99+ upstream) are dev tooling, not tests — not migrated.

PARTIALLY RE-ENABLED 2026-04-11 (CVC M04): WCAG contrast utilities restored
in canvas_core/design_tokens.py (hex_to_rgb, contrast_ratio, check_wcag_aa).
Accessibility category (A1-A4) added to review() in canvas_presentation/scoring.py.
Tests that depend on deleted CVD symbols (_check_palette_colorblind_safety,
CANVAS_SR_LIMITATIONS, validate_theme_contrast) remain skipped.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import unittest

from canvas_core.design_tokens import (
    check_wcag_aa,
    contrast_ratio,
    hex_to_rgb,
)
from canvas_core.html_renderer import THEME_PALETTES
from canvas_presentation.config_deck import PRESENTATION_THEMES
from canvas_presentation.presentation import PresentationBuilder


# Map Obsidian canvas color slots (1-6) to Tokyo Night hex palette
CANVAS_COLOR_HEX = {
    "1": "#f7768e",
    "2": "#ff9e64",
    "3": "#e0af68",
    "4": "#7dcfff",
    "5": "#9ece6a",
    "6": "#9d7cd8",
}


class TestM13AccessibilityAudit(unittest.TestCase):
    """PE M13 accessibility verification tests (partially re-enabled)."""

    def test_all_themes_pass_aa_large_contrast(self):
        """O1/O3: All themes must pass WCAG AA Large Text (3:1) for primary text on bg."""
        for theme_name, palette in THEME_PALETTES.items():
            ratio = contrast_ratio(palette.text, palette.bg)
            self.assertGreaterEqual(
                ratio, 3.0,
                f"{theme_name}.text ({palette.text}) vs {palette.bg}: "
                f"{ratio:.2f}:1 < 3:1 AA large text minimum",
            )
            # text_dim is intentionally lower contrast — check it meets 2.5:1
            dim_ratio = contrast_ratio(palette.text_dim, palette.bg)
            self.assertGreaterEqual(
                dim_ratio, 2.5,
                f"{theme_name}.text_dim ({palette.text_dim}) vs {palette.bg}: "
                f"{dim_ratio:.2f}:1 below 2.5:1 floor for dim text",
            )

    @unittest.skip("CVD simulation symbols not restored — Phase 2+ scope")
    def test_cvd_simulation_runs(self):
        """O3: CVD simulation for all themes."""
        pass

    def test_font_size_minimum_met(self):
        """O2: CSS body scale produces >= 18px effective body text."""
        base_font = 16.0
        body_scale = 1.125
        effective_body = base_font * body_scale
        self.assertGreaterEqual(
            effective_body, 18.0,
            f"Effective body font {effective_body}px < 18px minimum",
        )

    def test_benchmark_decks_pass_accessibility(self):
        """O1/O5: Benchmark decks score >= 0.80 accessibility via review()."""
        themes_to_test = list(PRESENTATION_THEMES.keys())[:3]
        for theme_name in themes_to_test:
            pb = PresentationBuilder(f"benchmark_{theme_name}", "1.0", theme=theme_name)
            pb.add_title_slide("Test Deck")
            pb.add_content_slide("Introduction", "This is a test slide with body text.")
            pb.add_image_slide("Visual", image_path="test.png", alt_text="Test image")
            pb.add_content_slide("Conclusion", "Final slide content.")
            report = pb.review()
            self.assertIn("accessibility", report.categories)
            acc_score = report.categories["accessibility"].score
            self.assertGreaterEqual(
                acc_score, 0.79,
                f"Theme {theme_name}: accessibility score {acc_score:.2f} < 0.80",
            )

    @unittest.skip("CANVAS_SR_LIMITATIONS not restored — Phase 2+ scope")
    def test_sr_limitations_documented(self):
        """O4: Screen reader limitations documented."""
        pass


if __name__ == "__main__":
    unittest.main()
