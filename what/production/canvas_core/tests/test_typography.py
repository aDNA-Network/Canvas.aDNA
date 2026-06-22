"""Tests for the typography token contract (ADR-009).

Covers: TypographyToken default-None inertness, to_css_fragment(None) → "",
merge() field-wise override semantics, opt-in CSS fragment emission for body /
heading / code / strong selectors + per-element tracking + line-height
multipliers + variable-font weight-axis.

Authored at M-V1-2-B-01 S1 (2026-05-27) per Pillar B charter. Substrate target:
`canvas_core/typography.py` (NEW at this session).

Re-merge rationale (CR7+SO7):
`lattice-labs/who/coordination/coord_2026_04_16_forge_split.md`
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.typography import (
    ELEMENTS,
    TypographyToken,
    merge,
    to_css_fragment,
)


# ---------------------------------------------------------------------------
# TypographyToken — default-None inertness (Memory A discipline)
# ---------------------------------------------------------------------------


def test_typography_token_all_fields_default_none():
    """Every field on a fresh TypographyToken must be None.

    Memory A `feedback_substrate_additive_opt_in_gated_pattern.md`: V1 path
    preserved when caller doesn't opt in to any override.
    """
    t = TypographyToken()
    assert t.font_family_body is None
    assert t.font_family_heading is None
    assert t.font_family_code is None
    assert t.weight_h1 is None
    assert t.weight_h2 is None
    assert t.weight_h3 is None
    assert t.weight_h4 is None
    assert t.weight_body is None
    assert t.weight_strong is None
    assert t.tracking_em is None
    assert t.line_height_multiplier is None
    assert t.kerning is None
    assert t.optical_sizing is None
    assert t.weight_axis is None


def test_typography_token_is_frozen():
    """TypographyToken is frozen — assignment after construction must raise."""
    t = TypographyToken()
    try:
        t.weight_h1 = 800  # type: ignore[misc]
    except Exception as exc:
        assert "frozen" in str(exc).lower() or "FrozenInstance" in type(exc).__name__
        return
    raise AssertionError("expected FrozenInstanceError on assignment to frozen dataclass")


def test_elements_tuple_contains_expected_keys():
    assert "h1" in ELEMENTS
    assert "body" in ELEMENTS
    assert "strong" in ELEMENTS
    assert "display" in ELEMENTS
    assert "caption" in ELEMENTS
    assert "label" in ELEMENTS


# ---------------------------------------------------------------------------
# to_css_fragment — V1 path preservation
# ---------------------------------------------------------------------------


def test_to_css_fragment_none_returns_empty_string():
    """to_css_fragment(None) must return '' so callers can append unconditionally.

    This is the V1 path guarantee — re-baseline gate Q5 NON-FIRE by construction.
    """
    assert to_css_fragment(None) == ""


def test_to_css_fragment_all_none_token_returns_empty_string():
    """A constructed-but-all-None TypographyToken also emits no CSS."""
    assert to_css_fragment(TypographyToken()) == ""


# ---------------------------------------------------------------------------
# to_css_fragment — V2 path opt-in emission
# ---------------------------------------------------------------------------


def test_to_css_fragment_body_font_family_emits_body_rule():
    t = TypographyToken(font_family_body="Charter, Georgia, serif")
    css = to_css_fragment(t)
    assert "/* Typography token overrides (ADR-009) */" in css
    assert "body { font-family: Charter, Georgia, serif; }" in css


def test_to_css_fragment_heading_family_emits_grouped_rule():
    t = TypographyToken(font_family_heading="Inter, sans-serif")
    css = to_css_fragment(t)
    assert "h1, h2, h3, h4 { font-family: Inter, sans-serif; }" in css


def test_to_css_fragment_code_family_emits_code_rule():
    t = TypographyToken(font_family_code="Fira Code, monospace")
    css = to_css_fragment(t)
    assert "code { font-family: Fira Code, monospace; }" in css


def test_to_css_fragment_per_element_weights():
    t = TypographyToken(weight_h1=800, weight_h2=600, weight_strong=700)
    css = to_css_fragment(t)
    assert "h1 { font-weight: 800; }" in css
    assert "h2 { font-weight: 600; }" in css
    assert "strong { font-weight: 700; }" in css


def test_to_css_fragment_kerning_and_optical_sizing_emit_on_body():
    t = TypographyToken(kerning="normal", optical_sizing="auto")
    css = to_css_fragment(t)
    assert "font-kerning: normal" in css
    assert "font-optical-sizing: auto" in css


def test_to_css_fragment_per_element_tracking():
    t = TypographyToken(tracking_em={"h1": -0.02, "body": 0.005})
    css = to_css_fragment(t)
    assert "letter-spacing: -0.02em" in css
    assert "letter-spacing: 0.005em" in css


def test_to_css_fragment_per_element_line_height_multiplier_uses_var():
    t = TypographyToken(line_height_multiplier={"h1": 1.05})
    css = to_css_fragment(t)
    assert "calc(var(--cl-lh-h1) * 1.05)" in css


def test_to_css_fragment_weight_axis_emits_font_variation_settings():
    t = TypographyToken(weight_axis={"h1": 750, "body": 400})
    css = to_css_fragment(t)
    assert "font-variation-settings: 'wght' 750" in css
    assert "font-variation-settings: 'wght' 400" in css


# ---------------------------------------------------------------------------
# merge — field-wise override semantics
# ---------------------------------------------------------------------------


def test_merge_both_none_returns_none():
    assert merge(None, None) is None


def test_merge_base_only_returns_base():
    base = TypographyToken(weight_h1=800)
    assert merge(base, None) is base


def test_merge_override_only_returns_override():
    override = TypographyToken(weight_h1=900)
    assert merge(None, override) is override


def test_merge_override_sets_only_non_none_fields():
    """None fields in override must NOT clobber non-None fields in base."""
    base = TypographyToken(weight_h1=800, weight_h2=600, kerning="normal")
    override = TypographyToken(weight_h1=900)  # only weight_h1 set
    result = merge(base, override)
    assert result is not None
    assert result.weight_h1 == 900  # overridden
    assert result.weight_h2 == 600  # preserved from base
    assert result.kerning == "normal"  # preserved from base


def test_merge_no_op_when_override_is_all_none():
    base = TypographyToken(weight_h1=800, kerning="normal")
    result = merge(base, TypographyToken())
    assert result is base  # no updates → original returned


def test_merge_dict_field_replaced_not_per_key_merged():
    """Dict-field override fully replaces base dict (documented behavior)."""
    base = TypographyToken(tracking_em={"h1": -0.02, "h2": -0.01})
    override = TypographyToken(tracking_em={"h3": -0.005})
    result = merge(base, override)
    assert result is not None
    assert result.tracking_em == {"h3": -0.005}  # FULL replace, not per-key merge


# ---------------------------------------------------------------------------
# Smoke: real-world composition pattern (theme-level + slide-type-level)
# ---------------------------------------------------------------------------


def test_realistic_theme_plus_slide_composition_yields_expected_css():
    theme_level = TypographyToken(
        font_family_body="Charter, serif",
        kerning="normal",
        optical_sizing="auto",
    )
    slide_level = TypographyToken(
        weight_h1=800,  # override hardcoded 700 for hero
        tracking_em={"h1": -0.025},
    )
    composed = merge(theme_level, slide_level)
    assert composed is not None
    css = to_css_fragment(composed)
    assert "Charter, serif" in css
    assert "font-kerning: normal" in css
    assert "font-optical-sizing: auto" in css
    assert "h1 { font-weight: 800;" in css
    assert "letter-spacing: -0.025em" in css
