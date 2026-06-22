"""Design tokens for the presentation system.

Provides a systematic spacing scale, typography scale, color proportion
rules, and vertical rhythm system. Replaces hardcoded constants in
canvas_presentation.py with a coherent design token system.

Part of campaign_presentation_excellence M16 (Visual Quality Engine).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .typography import TypographyToken

# ---------------------------------------------------------------------------
# Spacing Scale — 4px base grid
# ---------------------------------------------------------------------------

SPACE_BASE = 4

# Named spacing tokens (geometric progression from 4px base)
SPACE_2XS = SPACE_BASE  # 4px
SPACE_XS = SPACE_BASE * 2  # 8px
SPACE_SM = SPACE_BASE * 3  # 12px
SPACE_MD = SPACE_BASE * 4  # 16px
SPACE_LG = SPACE_BASE * 6  # 24px
SPACE_XL = SPACE_BASE * 8  # 32px
SPACE_2XL = SPACE_BASE * 12  # 48px
SPACE_3XL = SPACE_BASE * 16  # 64px
SPACE_4XL = SPACE_BASE * 24  # 96px

# Full spacing scale as a list (for programmatic access)
SPACING_SCALE = [
    SPACE_2XS,
    SPACE_XS,
    SPACE_SM,
    SPACE_MD,
    SPACE_LG,
    SPACE_XL,
    SPACE_2XL,
    SPACE_3XL,
    SPACE_4XL,
]

# Named mapping for CSS export
SPACING_TOKENS: dict[str, int] = {
    "2xs": SPACE_2XS,
    "xs": SPACE_XS,
    "sm": SPACE_SM,
    "md": SPACE_MD,
    "lg": SPACE_LG,
    "xl": SPACE_XL,
    "2xl": SPACE_2XL,
    "3xl": SPACE_3XL,
    "4xl": SPACE_4XL,
}


# ---------------------------------------------------------------------------
# Typography Scale — Major Third (1.250)
# ---------------------------------------------------------------------------

TYPE_SCALE_RATIO = 1.250  # Major third
TYPE_BASE_SIZE = 16  # Base font size in px

# Computed scale steps (base × ratio^n)
# n: -2=label, -1=caption, 0=body, 1=h4, 2=h3, 3=h2, 4=h1, 5=display
TYPE_SCALE_STEPS = {
    "label": TYPE_BASE_SIZE / (TYPE_SCALE_RATIO**2),  # ~10.24px
    "caption": TYPE_BASE_SIZE / TYPE_SCALE_RATIO,  # ~12.80px
    "body": TYPE_BASE_SIZE,  # 16.00px
    "h4": TYPE_BASE_SIZE * TYPE_SCALE_RATIO,  # 20.00px
    "h3": TYPE_BASE_SIZE * TYPE_SCALE_RATIO**2,  # 25.00px
    "h2": TYPE_BASE_SIZE * TYPE_SCALE_RATIO**3,  # 31.25px
    "h1": TYPE_BASE_SIZE * TYPE_SCALE_RATIO**4,  # 39.06px
    "display": TYPE_BASE_SIZE * TYPE_SCALE_RATIO**5,  # 48.83px
}

# Rounded values for practical use
TYPE_SIZES: dict[str, int] = {k: round(v) for k, v in TYPE_SCALE_STEPS.items()}

# Line height ratios per element type
LINE_HEIGHTS: dict[str, float] = {
    "display": 1.1,
    "h1": 1.15,
    "h2": 1.2,
    "h3": 1.25,
    "h4": 1.3,
    "body": 1.5,
    "caption": 1.3,
    "label": 1.2,
}

# Letter-spacing in em
LETTER_SPACING: dict[str, float] = {
    "display": -0.02,
    "h1": -0.015,
    "h2": -0.01,
    "h3": -0.005,
    "h4": 0.0,
    "body": 0.0,
    "caption": 0.01,
    "label": 0.04,
}


# ---------------------------------------------------------------------------
# Typography Token Contract (ADR-009; M-V1-2-B-01 S1 2026-05-27; Pillar B)
#
# Opt-in fine-grained typography surface (tracking, kerning, line-height
# multipliers, optical sizing, per-element weight variants, font-family +
# weight tokenization). All consumer-facing surfaces default to None and
# preserve V1 behavior verbatim — see Memory A
# `feedback_substrate_additive_opt_in_gated_pattern.md` (4-session Pillar F
# precedent). Re-baseline gate Q5 non-fire by construction at S1.
#
# Re-merge rationale (CR7+SO7):
# `lattice-labs/who/coordination/coord_2026_04_16_forge_split.md`
# ---------------------------------------------------------------------------

# Sentinel default — preserves V1 CSS path when consumers don't opt in.
TYPOGRAPHY_TOKENS_DEFAULT: TypographyToken | None = None

# Opt-in publication-grade preset. Demonstrates the contract for downstream
# callers (LP 3-5 pager / Pillar A in LPWhitepaper; SS / CC wrappers).
# NOT wired into any built-in theme at S1 — baseline themes consume
# TYPOGRAPHY_TOKENS_DEFAULT (i.e. None) and remain on the V1 path.
TYPOGRAPHY_TOKENS_PUBLICATION: TypographyToken = TypographyToken(
    kerning="normal",
    optical_sizing="auto",
    tracking_em={
        "h1": -0.02,
        "h2": -0.015,
        "h3": -0.01,
        "body": 0.005,
    },
    line_height_multiplier={
        "h1": 1.0,
        "h2": 1.0,
        "body": 1.0,
    },
)


# Per-theme opt-in presets (M-V1-2-B-01 S2 — 2026-05-28; ADR-009 §D5).
# Each preset captures theme-flavored typography refinements as a single
# importable name; callers wire by passing to `PresentationTheme(
# typography_tokens=...)`. Both presets are family-agnostic — the host
# `theme.font_suggestion` (Wilhelm: Charter/serif; Issue 01: JetBrains
# Mono) continues to drive font-family unless caller also opts into
# `font_family_*` overrides.
#
# NOT wired into THEME_WILHELM_FOUNDATION or THEME_SCIENCE_STANLEY at S2 —
# baseline themes consume TYPOGRAPHY_TOKENS_DEFAULT (None) and remain on
# the V1 CSS path. Wilhelm 8.80 + Issue 01 8.43 parity baselines (SHA
# `3ce4d341a727…`) preserved by construction; re-baseline gate Q5 non-fire.
# Memory A `feedback_substrate_additive_opt_in_gated_pattern.md` discipline.

# Wilhelm-deck-flavored refinements for serif/academic publication.
# Charter/Georgia/Cambria serif benefits from tightened display + h1
# tracking and a lifted h1 weight to balance Charter's tall x-height.
TYPOGRAPHY_TOKENS_WILHELM: TypographyToken = TypographyToken(
    kerning="normal",
    optical_sizing="auto",
    tracking_em={
        "display": -0.025,
        "h1": -0.02,
        "h2": -0.015,
        "h3": -0.01,
        "body": 0.005,
        "caption": 0.015,
        "label": 0.05,
    },
    line_height_multiplier={
        "h1": 0.95,
        "h2": 0.98,
        "body": 1.0,
    },
    weight_h1=600,
    weight_strong=600,
)

# Issue-01-comic-flavored refinements for JetBrains Mono / monospace.
# Mono already carries even horizontal rhythm — tracking shifts are smaller;
# the gain is at hierarchy (heavier h1/h2 for impact) and at comic-density
# body line-height (tighter than narrative deck body).
TYPOGRAPHY_TOKENS_ISSUE_01: TypographyToken = TypographyToken(
    kerning="normal",
    optical_sizing="auto",
    tracking_em={
        "h1": -0.01,
        "h2": -0.005,
        "body": 0.0,
        "caption": 0.01,
        "label": 0.03,
    },
    line_height_multiplier={
        "h1": 1.0,
        "body": 0.95,
        "caption": 0.95,
    },
    weight_h1=800,
)


# ---------------------------------------------------------------------------
# Color Proportion — 60/30/10 Rule
# ---------------------------------------------------------------------------

COLOR_DOMINANT_RATIO = 0.60  # Background, base canvas
COLOR_SECONDARY_RATIO = 0.30  # Structure, containers, content borders
COLOR_ACCENT_RATIO = 0.10  # Highlights, CTAs, emphasis


@dataclass
class ColorProportionResult:
    """Result of color proportion analysis."""

    dominant_ratio: float
    secondary_ratio: float
    accent_ratio: float
    passes: bool
    issues: list[str] = field(default_factory=list)


def check_color_proportion(
    dominant_area: float,
    secondary_area: float,
    accent_area: float,
    *,
    tolerance: float = 0.15,
) -> ColorProportionResult:
    """Check if color distribution follows the 60/30/10 rule.

    Args:
        dominant_area: Area fraction used by dominant color (0-1).
        secondary_area: Area fraction used by secondary color (0-1).
        accent_area: Area fraction used by accent color (0-1).
        tolerance: Acceptable deviation from ideal ratios.

    Returns:
        ColorProportionResult with pass/fail and issues.
    """
    total = dominant_area + secondary_area + accent_area
    if total <= 0:
        return ColorProportionResult(0, 0, 0, True)

    d = dominant_area / total
    s = secondary_area / total
    a = accent_area / total
    issues: list[str] = []

    if abs(d - COLOR_DOMINANT_RATIO) > tolerance:
        issues.append(f"Dominant color at {d:.0%} (target {COLOR_DOMINANT_RATIO:.0%})")
    if abs(s - COLOR_SECONDARY_RATIO) > tolerance:
        issues.append(f"Secondary color at {s:.0%} (target {COLOR_SECONDARY_RATIO:.0%})")
    if abs(a - COLOR_ACCENT_RATIO) > tolerance:
        issues.append(f"Accent color at {a:.0%} (target {COLOR_ACCENT_RATIO:.0%})")

    return ColorProportionResult(
        dominant_ratio=round(d, 3),
        secondary_ratio=round(s, 3),
        accent_ratio=round(a, 3),
        passes=len(issues) == 0,
        issues=issues,
    )


# ---------------------------------------------------------------------------
# Vertical Rhythm
# ---------------------------------------------------------------------------


def rhythm_unit(base_size: int = TYPE_BASE_SIZE, line_height: float = 1.5) -> int:
    """Compute the vertical rhythm unit.

    The rhythm unit is the baseline grid interval: font-size × line-height,
    snapped to a 4px grid boundary.
    """
    raw = base_size * line_height
    return max(SPACE_BASE, round(raw / SPACE_BASE) * SPACE_BASE)


def rhythm_multiples(count: int, base_size: int = TYPE_BASE_SIZE) -> list[int]:
    """Generate rhythm-aligned spacing values.

    Returns ``count`` multiples of the rhythm unit starting from 1×.
    """
    unit = rhythm_unit(base_size)
    return [unit * (i + 1) for i in range(count)]


# ---------------------------------------------------------------------------
# Slide-Type Token Profiles
# ---------------------------------------------------------------------------


@dataclass
class SlideTypeTokens:
    """Design token profile for a specific slide type.

    Controls whitespace targets, typography choices, and spacing behavior.
    """

    slide_type: str

    # Whitespace targets (fraction of slide area)
    whitespace_min: float = 0.40
    whitespace_target: float = 0.55
    whitespace_max: float = 0.75

    # Content sizing
    min_height: int = 600
    max_height: int = 1600
    heading_height: int = 120

    # Margins (from spacing scale)
    margin_top: int = SPACE_2XL  # 48px
    margin_side: int = SPACE_3XL  # 64px
    margin_bottom: int = SPACE_2XL  # 48px

    # Gaps
    heading_body_gap: int = SPACE_LG  # 24px

    # Typography level for heading
    heading_level: str = "h2"

    # Content height estimation: words per 100px at body size
    words_per_100px: int = 15

    # Per-type height padding (extra space for visual breathing room)
    height_padding: int = SPACE_3XL  # 64px

    # Per-slide-type typography override (ADR-009; opt-in; default None).
    # When None, the slide consumes theme-level typography_tokens (if any)
    # OR the V1 hardcoded CSS path. When set, composes with theme-level
    # tokens via `typography.merge(theme.typography_tokens, slide_tokens)`.
    typography_tokens: TypographyToken | None = None


# Default profiles per slide type
_SLIDE_TYPE_DEFAULTS: dict[str, dict[str, Any]] = {
    "title": {
        "whitespace_min": 0.65,
        "whitespace_target": 0.75,
        "whitespace_max": 0.85,
        "heading_height": 200,
        "heading_level": "h1",
        "margin_top": SPACE_3XL,
        "margin_side": SPACE_3XL,
        "heading_body_gap": SPACE_XL,
        "height_padding": SPACE_4XL,
    },
    "content": {
        "whitespace_min": 0.40,
        "whitespace_target": 0.50,
        "whitespace_max": 0.60,
        "heading_body_gap": SPACE_LG,
    },
    "comparison": {
        "whitespace_min": 0.35,
        "whitespace_target": 0.45,
        "whitespace_max": 0.55,
    },
    "quote": {
        "whitespace_min": 0.60,
        "whitespace_target": 0.70,
        "whitespace_max": 0.80,
        "heading_height": 100,
        "heading_body_gap": SPACE_XL,
        "height_padding": SPACE_4XL,
    },
    "stats": {
        "whitespace_min": 0.50,
        "whitespace_target": 0.60,
        "whitespace_max": 0.70,
        "heading_body_gap": SPACE_XL,
    },
    "section_divider": {
        "whitespace_min": 0.70,
        "whitespace_target": 0.80,
        "whitespace_max": 0.90,
        "heading_height": 200,
        "heading_level": "h1",
        "margin_top": SPACE_4XL,
        "height_padding": SPACE_4XL,
    },
    "diagram": {
        "whitespace_min": 0.30,
        "whitespace_target": 0.40,
        "whitespace_max": 0.55,
    },
    "image": {
        "whitespace_min": 0.25,
        "whitespace_target": 0.35,
        "whitespace_max": 0.50,
    },
    "timeline": {
        "whitespace_min": 0.35,
        "whitespace_target": 0.45,
        "whitespace_max": 0.55,
    },
    "process": {
        "whitespace_min": 0.35,
        "whitespace_target": 0.45,
        "whitespace_max": 0.55,
    },
    "three_column": {
        "whitespace_min": 0.35,
        "whitespace_target": 0.45,
        "whitespace_max": 0.55,
    },
    "key_value": {
        "whitespace_min": 0.40,
        "whitespace_target": 0.50,
        "whitespace_max": 0.60,
    },
    "matrix": {
        "whitespace_min": 0.30,
        "whitespace_target": 0.40,
        "whitespace_max": 0.50,
    },
    "collage": {
        "whitespace_min": 0.20,
        "whitespace_target": 0.30,
        "whitespace_max": 0.45,
    },
    "video": {
        "whitespace_min": 0.35,
        "whitespace_target": 0.45,
        "whitespace_max": 0.55,
    },
    "team": {
        "whitespace_min": 0.40,
        "whitespace_target": 0.50,
        "whitespace_max": 0.60,
    },
}


def get_slide_tokens(slide_type: str) -> SlideTypeTokens:
    """Get the design token profile for a slide type.

    Falls back to the default SlideTypeTokens for unknown types.
    """
    overrides = _SLIDE_TYPE_DEFAULTS.get(slide_type, {})
    return SlideTypeTokens(slide_type=slide_type, **overrides)


# ---------------------------------------------------------------------------
# Content-Adaptive Height Estimation
# ---------------------------------------------------------------------------


def estimate_content_height(
    text: str,
    slide_type: str,
    width: int = 1080,
) -> int:
    """Estimate the rendered height needed for text content.

    Uses word count and line estimation to approximate how much vertical
    space the content needs at body font size.

    Args:
        text: The text content (may include markdown).
        slide_type: Slide type for per-type token lookup.
        width: Available content width in pixels.

    Returns:
        Estimated height in pixels, clamped to type-specific min/max.
    """
    tokens = get_slide_tokens(slide_type)

    if not text.strip():
        return tokens.min_height

    # Count content elements
    lines = text.strip().split("\n")
    non_empty_lines = [ln for ln in lines if ln.strip()]
    bullet_count = sum(1 for ln in non_empty_lines if ln.lstrip().startswith(("- ", "* ", "1.")))
    heading_count = sum(1 for ln in non_empty_lines if ln.lstrip().startswith("#"))

    # Estimate characters per line at body size
    # At 16px body size, ~60 chars fit in 1080px width
    chars_per_line = max(1, width // TYPE_SIZES["body"])

    # Estimate total rendered lines
    total_chars = len(text)
    text_lines = max(len(non_empty_lines), total_chars // chars_per_line)

    # Height estimation
    body_rhythm = rhythm_unit()
    heading_rhythm = rhythm_unit(TYPE_SIZES["h2"], LINE_HEIGHTS["h2"])

    text_height = text_lines * body_rhythm
    bullet_extra = bullet_count * SPACE_XS  # extra spacing between bullets
    heading_extra = heading_count * heading_rhythm

    # Compose total height
    content_height = text_height + bullet_extra + heading_extra
    total_height = (
        tokens.margin_top
        + tokens.heading_height
        + tokens.heading_body_gap
        + content_height
        + tokens.margin_bottom
        + tokens.height_padding
    )

    return max(tokens.min_height, min(int(total_height), tokens.max_height))


def estimate_node_height(
    text: str,
    width: int,
    slide_type: str,
) -> int:
    """Estimate height for a single interior node based on its content.

    Unlike ``estimate_content_height`` which estimates the full slide,
    this estimates a single body node's height.

    Args:
        text: Node text content.
        width: Node width in pixels.
        slide_type: Parent slide type for token lookup.

    Returns:
        Estimated node height in pixels.
    """
    if not text.strip():
        return 100

    tokens = get_slide_tokens(slide_type)
    lines = text.strip().split("\n")
    non_empty = [ln for ln in lines if ln.strip()]
    word_count = len(text.split())

    # Words per 100px at the given width (scaled from default 1080px)
    scale_factor = width / 1080.0
    effective_wpp = max(5, int(tokens.words_per_100px * scale_factor))

    # Height from word count
    text_height = (word_count / effective_wpp) * 100

    # Add space for bullets and headings
    bullet_count = sum(1 for ln in non_empty if ln.lstrip().startswith(("- ", "* ")))
    heading_count = sum(1 for ln in non_empty if ln.lstrip().startswith("#"))

    extra = bullet_count * SPACE_2XS + heading_count * SPACE_MD

    # Minimum based on line count
    line_min = len(non_empty) * rhythm_unit()

    raw = max(text_height + extra, line_min)

    # Clamp: minimum 80px, maximum 800px for a single node
    return max(80, min(int(raw), 800))


# ---------------------------------------------------------------------------
# CSS Custom Property Export
# ---------------------------------------------------------------------------


def export_css_custom_properties() -> str:
    """Generate CSS custom property declarations for design tokens.

    Returns a string of CSS that can be injected into a :root {} block
    or used to verify alignment between Python tokens and CSS variables.
    """
    lines: list[str] = []
    lines.append("/* Design tokens — auto-generated from canvas_design_tokens.py */")
    lines.append("")

    # Spacing
    lines.append("/* Spacing scale */")
    for name, value in SPACING_TOKENS.items():
        lines.append(f"--cl-space-{name}: {value}px;")
    lines.append("")

    # Typography
    lines.append("/* Typography scale (major third 1.250) */")
    for name, value in TYPE_SIZES.items():
        lines.append(f"--cl-type-{name}: {value}px;")
    lines.append("")

    # Line heights
    lines.append("/* Line heights */")
    for name, value in LINE_HEIGHTS.items():
        lines.append(f"--cl-lh-{name}: {value};")
    lines.append("")

    # Letter spacing
    lines.append("/* Letter spacing */")
    for name, value in LETTER_SPACING.items():
        lines.append(f"--cl-ls-{name}: {value}em;")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Backward Compatibility — Legacy Constant Mapping
# ---------------------------------------------------------------------------

# These map the old hardcoded constants to token-based values.
# Used by canvas_presentation.py during the transition.

# ---------------------------------------------------------------------------
# WCAG 2.1 Contrast Utilities
# ---------------------------------------------------------------------------
# Pure-Python implementation of the WCAG 2.1 relative luminance and contrast
# ratio algorithms. Used by canvas_scoring.py (A4 accessibility criterion)
# and tests. Replaces symbols deleted in the canvas_presentation refactor
# (_contrast_ratio, _hex_to_rgb from the old PE M13 audit).


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert ``#RRGGBB`` hex string to an (R, G, B) tuple."""
    h = hex_color.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"Expected 6-character hex color, got {hex_color!r}")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _srgb_to_linear(channel: int) -> float:
    """Convert an 8-bit sRGB channel value to linear RGB per WCAG 2.1."""
    s = channel / 255.0
    return s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_color: str) -> float:
    """WCAG 2.1 relative luminance of a hex color (0.0 = black, 1.0 = white)."""
    r, g, b = hex_to_rgb(hex_color)
    return 0.2126 * _srgb_to_linear(r) + 0.7152 * _srgb_to_linear(g) + 0.0722 * _srgb_to_linear(b)


def contrast_ratio(fg_hex: str, bg_hex: str) -> float:
    """WCAG 2.1 contrast ratio between two hex colors. Always >= 1.0."""
    l1 = relative_luminance(fg_hex)
    l2 = relative_luminance(bg_hex)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def check_wcag_aa(fg_hex: str, bg_hex: str, large_text: bool = True) -> bool:
    """Check if a foreground/background pair passes WCAG AA.

    Large text (>= 18pt or >= 14pt bold): 3:1 minimum.
    Normal text: 4.5:1 minimum.
    """
    ratio = contrast_ratio(fg_hex, bg_hex)
    threshold = 3.0 if large_text else 4.5
    return ratio >= threshold


def validate_theme_palette(palette: Any) -> list[str]:
    """Validate a ThemePalette for WCAG AA compliance.

    Checks:
      - text on bg >= 4.5:1 (WCAG AA normal text)
      - text_dim on bg >= 3.0:1 (WCAG AA large text)
      - bg_lighter distinct from bg

    Returns a list of issues (empty = all checks pass).
    """
    issues: list[str] = []
    text_bg = contrast_ratio(palette.text, palette.bg)
    if text_bg < 4.5:
        issues.append(f"text/bg contrast {text_bg:.2f}:1 below AA normal (4.5:1)")
    dim_bg = contrast_ratio(palette.text_dim, palette.bg)
    if dim_bg < 3.0:
        issues.append(f"text_dim/bg contrast {dim_bg:.2f}:1 below AA large (3.0:1)")
    if palette.bg == palette.bg_lighter:
        issues.append("bg and bg_lighter are identical")
    return issues


LEGACY_SLIDE_WIDTH = 1200
LEGACY_SLIDE_HEIGHT = 1100
LEGACY_HEADING_TOP_MARGIN = SPACE_2XL  # was 40 → now 48
LEGACY_HEADING_HEIGHT = 120  # preserved
LEGACY_BODY_TOP_GAP = SPACE_LG  # was 20 → now 24
LEGACY_CONTENT_SIDE_MARGIN = SPACE_3XL  # was 60 → now 64
LEGACY_CONTENT_WIDTH = LEGACY_SLIDE_WIDTH - 2 * LEGACY_CONTENT_SIDE_MARGIN  # 1072
