"""Tests for the design token system.

Covers: spacing scale, typography scale, color proportions, vertical rhythm,
slide-type token profiles, content-adaptive height estimation, and CSS export.

Migrated from `lattice-protocol/extensions/canvas/tests/test_design_tokens.py`
under M-R5-01a (campaign_canvasforge_review). Pure substrate — no
canvas_presentation / canvas_comic imports. Substrate target:
`canvas_core/design_tokens.py` (582 LOC).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.design_tokens import (
    COLOR_ACCENT_RATIO,
    COLOR_DOMINANT_RATIO,
    COLOR_SECONDARY_RATIO,
    LEGACY_CONTENT_SIDE_MARGIN,
    LEGACY_CONTENT_WIDTH,
    LEGACY_SLIDE_HEIGHT,
    LEGACY_SLIDE_WIDTH,
    LETTER_SPACING,
    LINE_HEIGHTS,
    SPACE_2XL,
    SPACE_2XS,
    SPACE_3XL,
    SPACE_4XL,
    SPACE_BASE,
    SPACE_LG,
    SPACE_MD,
    SPACE_SM,
    SPACE_XL,
    SPACE_XS,
    SPACING_SCALE,
    SPACING_TOKENS,
    TYPE_BASE_SIZE,
    TYPE_SCALE_RATIO,
    TYPE_SCALE_STEPS,
    TYPE_SIZES,
    SlideTypeTokens,
    check_color_proportion,
    estimate_content_height,
    estimate_node_height,
    export_css_custom_properties,
    get_slide_tokens,
    rhythm_multiples,
    rhythm_unit,
)

# ---------------------------------------------------------------------------
# Spacing Scale
# ---------------------------------------------------------------------------


class TestSpacingScale:
    def test_base_unit(self):
        assert SPACE_BASE == 4

    def test_all_multiples_of_base(self):
        for val in SPACING_SCALE:
            assert val % SPACE_BASE == 0, f"{val} is not a multiple of {SPACE_BASE}"

    def test_monotonic_increase(self):
        for i in range(1, len(SPACING_SCALE)):
            assert SPACING_SCALE[i] > SPACING_SCALE[i - 1]

    def test_named_tokens_match_scale(self):
        assert SPACE_2XS == 4
        assert SPACE_XS == 8
        assert SPACE_SM == 12
        assert SPACE_MD == 16
        assert SPACE_LG == 24
        assert SPACE_XL == 32
        assert SPACE_2XL == 48
        assert SPACE_3XL == 64
        assert SPACE_4XL == 96

    def test_token_dict_completeness(self):
        assert len(SPACING_TOKENS) == 9
        assert set(SPACING_TOKENS.values()) == set(SPACING_SCALE)

    def test_scale_length(self):
        assert len(SPACING_SCALE) == 9


# ---------------------------------------------------------------------------
# Typography Scale
# ---------------------------------------------------------------------------


class TestTypographyScale:
    def test_base_size(self):
        assert TYPE_BASE_SIZE == 16

    def test_scale_ratio(self):
        assert TYPE_SCALE_RATIO == 1.250

    def test_body_equals_base(self):
        assert TYPE_SCALE_STEPS["body"] == TYPE_BASE_SIZE

    def test_h1_larger_than_body(self):
        assert TYPE_SCALE_STEPS["h1"] > TYPE_SCALE_STEPS["body"] * 2

    def test_caption_smaller_than_body(self):
        assert TYPE_SCALE_STEPS["caption"] < TYPE_SCALE_STEPS["body"]

    def test_scale_monotonic(self):
        order = ["label", "caption", "body", "h4", "h3", "h2", "h1", "display"]
        for i in range(1, len(order)):
            assert TYPE_SCALE_STEPS[order[i]] > TYPE_SCALE_STEPS[order[i - 1]]

    def test_rounded_sizes_reasonable(self):
        assert TYPE_SIZES["body"] == 16
        assert 18 <= TYPE_SIZES["h4"] <= 22
        assert 23 <= TYPE_SIZES["h3"] <= 27
        assert 29 <= TYPE_SIZES["h2"] <= 33
        assert 37 <= TYPE_SIZES["h1"] <= 41
        assert 46 <= TYPE_SIZES["display"] <= 52

    def test_line_heights_all_present(self):
        for key in TYPE_SCALE_STEPS:
            assert key in LINE_HEIGHTS

    def test_heading_line_heights_tighter(self):
        assert LINE_HEIGHTS["h1"] < LINE_HEIGHTS["body"]
        assert LINE_HEIGHTS["display"] < LINE_HEIGHTS["h1"]

    def test_body_line_height_range(self):
        assert 1.4 <= LINE_HEIGHTS["body"] <= 1.6

    def test_letter_spacing_all_present(self):
        for key in TYPE_SCALE_STEPS:
            assert key in LETTER_SPACING

    def test_heading_letter_spacing_tight(self):
        assert LETTER_SPACING["display"] < 0
        assert LETTER_SPACING["h1"] < 0

    def test_body_letter_spacing_normal(self):
        assert LETTER_SPACING["body"] == 0.0

    def test_label_letter_spacing_wide(self):
        assert LETTER_SPACING["label"] > 0


# ---------------------------------------------------------------------------
# Color Proportion
# ---------------------------------------------------------------------------


class TestColorProportion:
    def test_ideal_ratios(self):
        result = check_color_proportion(0.60, 0.30, 0.10)
        assert result.passes
        assert len(result.issues) == 0

    def test_off_balance(self):
        result = check_color_proportion(0.40, 0.40, 0.20)
        assert not result.passes
        assert len(result.issues) > 0

    def test_within_tolerance(self):
        result = check_color_proportion(0.55, 0.32, 0.13, tolerance=0.15)
        assert result.passes

    def test_all_zero(self):
        result = check_color_proportion(0.0, 0.0, 0.0)
        assert result.passes

    def test_ratios_sum_to_one(self):
        result = check_color_proportion(0.60, 0.30, 0.10)
        total = result.dominant_ratio + result.secondary_ratio + result.accent_ratio
        assert abs(total - 1.0) < 0.01

    def test_ratios_constants(self):
        assert COLOR_DOMINANT_RATIO == 0.60
        assert COLOR_SECONDARY_RATIO == 0.30
        assert COLOR_ACCENT_RATIO == 0.10


# ---------------------------------------------------------------------------
# Vertical Rhythm
# ---------------------------------------------------------------------------


class TestVerticalRhythm:
    def test_default_rhythm_unit(self):
        unit = rhythm_unit()
        # 16px × 1.5 = 24px
        assert unit == 24

    def test_snaps_to_4px_grid(self):
        unit = rhythm_unit(17, 1.5)  # 25.5 → 24
        assert unit % SPACE_BASE == 0

    def test_minimum_is_base(self):
        unit = rhythm_unit(1, 0.1)
        assert unit >= SPACE_BASE

    def test_multiples(self):
        multiples = rhythm_multiples(4)
        assert len(multiples) == 4
        assert multiples[0] == 24
        assert multiples[1] == 48
        assert multiples[2] == 72
        assert multiples[3] == 96

    def test_multiples_are_multiples_of_unit(self):
        unit = rhythm_unit()
        for m in rhythm_multiples(5):
            assert m % unit == 0


# ---------------------------------------------------------------------------
# Slide Type Tokens
# ---------------------------------------------------------------------------


class TestSlideTypeTokens:
    def test_default_profile(self):
        tokens = SlideTypeTokens(slide_type="unknown")
        assert tokens.whitespace_target == 0.55
        assert tokens.min_height == 600
        assert tokens.max_height == 1600

    def test_title_profile(self):
        tokens = get_slide_tokens("title")
        assert tokens.whitespace_target > 0.70
        assert tokens.heading_level == "h1"

    def test_content_profile(self):
        tokens = get_slide_tokens("content")
        assert tokens.whitespace_target < 0.60

    def test_quote_profile(self):
        tokens = get_slide_tokens("quote")
        assert tokens.whitespace_target > 0.65

    def test_section_divider_profile(self):
        tokens = get_slide_tokens("section_divider")
        assert tokens.whitespace_target > 0.75
        assert tokens.heading_level == "h1"

    def test_all_types_covered(self):
        known_types = [
            "title",
            "content",
            "comparison",
            "quote",
            "stats",
            "section_divider",
            "diagram",
            "image",
            "timeline",
            "process",
            "three_column",
            "key_value",
            "matrix",
            "collage",
            "video",
            "team",
        ]
        for stype in known_types:
            tokens = get_slide_tokens(stype)
            assert tokens.slide_type == stype

    def test_unknown_type_gets_defaults(self):
        tokens = get_slide_tokens("nonexistent")
        assert tokens.slide_type == "nonexistent"
        assert tokens.whitespace_target == 0.55

    def test_margins_from_spacing_scale(self):
        tokens = get_slide_tokens("content")
        assert tokens.margin_top in SPACING_SCALE
        assert tokens.margin_side in SPACING_SCALE
        assert tokens.margin_bottom in SPACING_SCALE

    def test_whitespace_range_valid(self):
        for stype in ["title", "content", "quote", "stats"]:
            tokens = get_slide_tokens(stype)
            assert tokens.whitespace_min < tokens.whitespace_target
            assert tokens.whitespace_target < tokens.whitespace_max


# ---------------------------------------------------------------------------
# Content-Adaptive Height
# ---------------------------------------------------------------------------


class TestContentAdaptiveHeight:
    def test_empty_text_returns_min(self):
        height = estimate_content_height("", "content")
        assert height == get_slide_tokens("content").min_height

    def test_short_text_smaller_than_long(self):
        short = estimate_content_height("Hello world", "content")
        long_text = "Word " * 200
        tall = estimate_content_height(long_text, "content")
        assert tall > short

    def test_clamped_to_max(self):
        huge = "Word " * 2000
        height = estimate_content_height(huge, "content")
        assert height <= get_slide_tokens("content").max_height

    def test_clamped_to_min(self):
        height = estimate_content_height("tiny", "content")
        assert height >= get_slide_tokens("content").min_height

    def test_bullets_add_height(self):
        plain = "Line one\nLine two\nLine three"
        bullets = "- Bullet one\n- Bullet two\n- Bullet three"
        h_plain = estimate_content_height(plain, "content")
        h_bullets = estimate_content_height(bullets, "content")
        # Bullets should add at least a small amount
        assert h_bullets >= h_plain

    def test_different_types_different_heights(self):
        text = "A moderate amount of content for testing."
        h_title = estimate_content_height(text, "title")
        h_content = estimate_content_height(text, "content")
        # Both should be valid
        assert 600 <= h_title <= 1600
        assert 600 <= h_content <= 1600


class TestNodeHeightEstimation:
    def test_empty_returns_minimum(self):
        h = estimate_node_height("", 1080, "content")
        assert h == 100

    def test_short_text(self):
        h = estimate_node_height("Hello world", 1080, "content")
        assert 80 <= h <= 800

    def test_long_text_taller(self):
        short_h = estimate_node_height("Short text", 1080, "content")
        long_h = estimate_node_height("Word " * 100, 1080, "content")
        assert long_h > short_h

    def test_clamped_to_max(self):
        h = estimate_node_height("Word " * 1000, 1080, "content")
        assert h <= 800

    def test_narrow_width_scales(self):
        h_wide = estimate_node_height("Some text here", 1080, "content")
        h_narrow = estimate_node_height("Some text here", 400, "content")
        # Narrower width should generally produce taller estimates
        # (but not necessarily — depends on content length)
        assert h_wide >= 80
        assert h_narrow >= 80


# ---------------------------------------------------------------------------
# CSS Export
# ---------------------------------------------------------------------------


class TestCSSExport:
    def test_produces_string(self):
        css = export_css_custom_properties()
        assert isinstance(css, str)
        assert len(css) > 100

    def test_spacing_properties(self):
        css = export_css_custom_properties()
        assert "--cl-space-md: 16px;" in css
        assert "--cl-space-xl: 32px;" in css

    def test_typography_properties(self):
        css = export_css_custom_properties()
        assert "--cl-type-body: 16px;" in css
        assert "--cl-type-h1:" in css

    def test_line_height_properties(self):
        css = export_css_custom_properties()
        assert "--cl-lh-body:" in css

    def test_letter_spacing_properties(self):
        css = export_css_custom_properties()
        assert "--cl-ls-body:" in css


# ---------------------------------------------------------------------------
# Legacy Compatibility
# ---------------------------------------------------------------------------


class TestLegacyCompatibility:
    def test_slide_dimensions_preserved(self):
        assert LEGACY_SLIDE_WIDTH == 1200
        assert LEGACY_SLIDE_HEIGHT == 1100

    def test_content_width_computed(self):
        expected = LEGACY_SLIDE_WIDTH - 2 * LEGACY_CONTENT_SIDE_MARGIN
        assert LEGACY_CONTENT_WIDTH == expected

    def test_margins_are_close_to_originals(self):
        # Original was 40px top margin, now 48px (SPACE_2XL)
        # Close enough for backward compat
        assert 40 <= SPACE_2XL <= 64
        # Original side margin was 60px, now 64px (SPACE_3XL)
        assert 56 <= SPACE_3XL <= 72


# ---------------------------------------------------------------------------
# Typography Token Contract (ADR-009; M-V1-2-B-01 S1 2026-05-27)
# Substrate-additive opt-in surface per Memory A
# (`feedback_substrate_additive_opt_in_gated_pattern.md`).
# ---------------------------------------------------------------------------


class TestTypographyTokensModule:
    def test_default_sentinel_is_none(self):
        """TYPOGRAPHY_TOKENS_DEFAULT must be None — V1 path preserved."""
        from canvas_core.design_tokens import TYPOGRAPHY_TOKENS_DEFAULT

        assert TYPOGRAPHY_TOKENS_DEFAULT is None

    def test_publication_preset_is_typography_token(self):
        """TYPOGRAPHY_TOKENS_PUBLICATION must be a TypographyToken instance."""
        from canvas_core.design_tokens import TYPOGRAPHY_TOKENS_PUBLICATION
        from canvas_core.typography import TypographyToken

        assert isinstance(TYPOGRAPHY_TOKENS_PUBLICATION, TypographyToken)

    def test_publication_preset_carries_kerning_and_optical_sizing(self):
        from canvas_core.design_tokens import TYPOGRAPHY_TOKENS_PUBLICATION

        assert TYPOGRAPHY_TOKENS_PUBLICATION.kerning == "normal"
        assert TYPOGRAPHY_TOKENS_PUBLICATION.optical_sizing == "auto"

    def test_publication_preset_does_not_pin_font_family(self):
        """Preset is family-agnostic — caller's theme font_suggestion still wins
        unless caller explicitly sets font_family_body."""
        from canvas_core.design_tokens import TYPOGRAPHY_TOKENS_PUBLICATION

        assert TYPOGRAPHY_TOKENS_PUBLICATION.font_family_body is None
        assert TYPOGRAPHY_TOKENS_PUBLICATION.font_family_heading is None
        assert TYPOGRAPHY_TOKENS_PUBLICATION.font_family_code is None

    def test_slide_type_tokens_typography_default_is_none(self):
        """SlideTypeTokens().typography_tokens must default to None."""
        from canvas_core.design_tokens import SlideTypeTokens

        assert SlideTypeTokens(slide_type="content").typography_tokens is None

    def test_get_slide_tokens_typography_default_is_none(self):
        """get_slide_tokens() for any known slide type returns typography_tokens=None."""
        from canvas_core.design_tokens import get_slide_tokens

        for slide_type in ("title", "content", "comparison", "quote", "stats"):
            assert get_slide_tokens(slide_type).typography_tokens is None

    def test_typography_token_re_exported_via_design_tokens(self):
        """`from canvas_core.design_tokens import TypographyToken` must work."""
        from canvas_core.design_tokens import TypographyToken
        from canvas_core.typography import TypographyToken as Canonical

        assert TypographyToken is Canonical


# ---------------------------------------------------------------------------
# Per-theme typography presets (ADR-009 §D5; M-V1-2-B-01 S2 — 2026-05-28).
#
# Two named presets land at S2 as opt-in pathways for Wilhelm and Issue-01-
# flavored typography. The presets are NOT wired into the corresponding
# baseline themes (THEME_WILHELM_FOUNDATION / THEME_SCIENCE_STANLEY); both
# themes consume TYPOGRAPHY_TOKENS_DEFAULT (None) and remain on the V1 CSS
# path. Memory A `feedback_substrate_additive_opt_in_gated_pattern.md`
# discipline preserves Wilhelm 8.80 + Issue 01 8.43 parity baselines
# (SHA `3ce4d341a727…`) by construction.
#
# Re-merge rationale (CR7+SO7):
# `lattice-labs/who/coordination/coord_2026_04_16_forge_split.md`
# ---------------------------------------------------------------------------


class TestPerThemeTypographyPresets:
    def test_typography_tokens_wilhelm_is_non_none_token(self):
        """TYPOGRAPHY_TOKENS_WILHELM must be a non-None TypographyToken."""
        from canvas_core.design_tokens import TYPOGRAPHY_TOKENS_WILHELM
        from canvas_core.typography import TypographyToken

        assert TYPOGRAPHY_TOKENS_WILHELM is not None
        assert isinstance(TYPOGRAPHY_TOKENS_WILHELM, TypographyToken)
        # Family-agnostic — caller's theme font_suggestion still drives family.
        assert TYPOGRAPHY_TOKENS_WILHELM.font_family_body is None
        assert TYPOGRAPHY_TOKENS_WILHELM.font_family_heading is None

    def test_typography_tokens_issue_01_is_non_none_token(self):
        """TYPOGRAPHY_TOKENS_ISSUE_01 must be a non-None TypographyToken."""
        from canvas_core.design_tokens import TYPOGRAPHY_TOKENS_ISSUE_01
        from canvas_core.typography import TypographyToken

        assert TYPOGRAPHY_TOKENS_ISSUE_01 is not None
        assert isinstance(TYPOGRAPHY_TOKENS_ISSUE_01, TypographyToken)
        # Family-agnostic — caller's theme font_suggestion still drives family.
        assert TYPOGRAPHY_TOKENS_ISSUE_01.font_family_body is None
        assert TYPOGRAPHY_TOKENS_ISSUE_01.font_family_code is None

    def test_per_theme_presets_not_wired_into_baseline_themes(self):
        """Baseline THEME_WILHELM_FOUNDATION + THEME_SCIENCE_STANLEY must
        carry typography_tokens=None — V1 path preserved by construction;
        re-baseline gate Q5 non-fire (Memory A discipline)."""
        from canvas_core.html_renderer import (
            THEME_SCIENCE_STANLEY,
            THEME_WILHELM_FOUNDATION,
        )

        assert THEME_WILHELM_FOUNDATION.typography_tokens is None
        assert THEME_SCIENCE_STANLEY.typography_tokens is None

    def test_per_theme_presets_opt_in_pathway_emits_v2_css(self):
        """Caller opting in via PresentationTheme(typography_tokens=...) must
        flip the renderer onto the V2 path — `_generate_base_css` appends a
        non-empty typography fragment when the preset is non-None."""
        from dataclasses import replace

        from canvas_core.design_tokens import (
            TYPOGRAPHY_TOKENS_ISSUE_01,
            TYPOGRAPHY_TOKENS_WILHELM,
        )
        from canvas_core.html_renderer import (
            THEME_SCIENCE_STANLEY,
            THEME_WILHELM_FOUNDATION,
            _generate_base_css,
        )

        wilhelm_v1 = _generate_base_css(THEME_WILHELM_FOUNDATION)
        wilhelm_v2 = _generate_base_css(
            replace(THEME_WILHELM_FOUNDATION, typography_tokens=TYPOGRAPHY_TOKENS_WILHELM)
        )
        assert len(wilhelm_v2) > len(wilhelm_v1), (
            "Wilhelm V2 path must append opt-in typography CSS"
        )

        ss_v1 = _generate_base_css(THEME_SCIENCE_STANLEY)
        ss_v2 = _generate_base_css(
            replace(THEME_SCIENCE_STANLEY, typography_tokens=TYPOGRAPHY_TOKENS_ISSUE_01)
        )
        assert len(ss_v2) > len(ss_v1), (
            "Issue 01 V2 path must append opt-in typography CSS"
        )
