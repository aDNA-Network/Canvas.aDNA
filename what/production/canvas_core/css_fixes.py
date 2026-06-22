"""CSS fix registry for the visual quality improvement loop.

Each fix is a named CSS rule set targeting specific theme/slide-type
combinations. Fixes are applied after base CSS generation, allowing
iterative visual quality improvement without modifying the core renderer.

M05 creates the registry with seed fixes. M11 fills it to 35+.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CSSFix:
    """A named CSS fix targeting specific theme/slide-type combinations."""

    id: str
    description: str
    slide_types: list[str] | None = None  # None = all types
    theme_names: list[str] | None = None  # None = all themes
    vr_criteria: list[str] = field(default_factory=list)
    css_rules: str = ""
    priority: int = 0  # Higher = applied later (overrides)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

CSS_FIX_REGISTRY: dict[str, CSSFix] = {}

_LIGHT_THEMES = ["lattice_light", "scientific", "academic"]
_DARK_THEMES = ["tokyo_night", "lattice_dark", "lattice_brand", "science_stanley"]


def register_fix(fix: CSSFix) -> None:
    """Register a CSS fix in the global registry."""
    CSS_FIX_REGISTRY[fix.id] = fix


def get_fixes_for(slide_type: str, theme_name: str) -> list[CSSFix]:
    """Get all fixes applicable to a given slide type and theme.

    Returns fixes sorted by priority (lowest first).
    """
    applicable: list[CSSFix] = []
    for fix in CSS_FIX_REGISTRY.values():
        type_match = fix.slide_types is None or slide_type in fix.slide_types
        theme_match = fix.theme_names is None or theme_name in fix.theme_names
        if type_match and theme_match:
            applicable.append(fix)
    return sorted(applicable, key=lambda f: f.priority)


def apply_fixes(base_css: str, slide_type: str, theme_name: str) -> str:
    """Append applicable fix CSS rules to base CSS.

    Returns the combined CSS string.
    """
    fixes = get_fixes_for(slide_type, theme_name)
    if not fixes:
        return base_css
    parts = [base_css, "\n/* --- CSS Fix Registry --- */"]
    for fix in fixes:
        parts.append(f"/* {fix.id}: {fix.description} */")
        parts.append(fix.css_rules)
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Seed Fixes — M04 deferred items + M03 VR findings
# ---------------------------------------------------------------------------

register_fix(CSSFix(
    id="FIX-LIGHT-HERO-CONTRAST",
    description="Light themes: hero title uses text color + accent underline for contrast",
    slide_types=["title"],
    theme_names=_LIGHT_THEMES,
    vr_criteria=["VR1", "VR4"],
    css_rules="""
    .slide-type-title .hero h1 {
        color: var(--cl-text);
        border-bottom: 3px solid var(--cl-primary);
        display: inline-block;
        padding-bottom: 8px;
    }
    """,
    priority=10,
))

register_fix(CSSFix(
    id="FIX-CONTENT-LINE-LENGTH",
    description="Constrain content text width for optimal line length (~65 chars)",
    slide_types=["content"],
    theme_names=None,
    vr_criteria=["VR1", "VR3"],
    css_rules="""
    .slide-type-content .slide-node.text-node {
        max-width: 960px;
    }
    """,
    priority=0,
))

register_fix(CSSFix(
    id="FIX-CONTENT-HEAVY-TYPOGRAPHY",
    description="Dense content slides: larger body text for readability",
    slide_types=["content"],
    theme_names=None,
    vr_criteria=["VR1", "VR2"],
    css_rules="""
    .slide-type-content.flow-top .slide-node.text-node p {
        font-size: 20px;
        line-height: 1.3;
    }
    """,
    priority=0,
))

register_fix(CSSFix(
    id="FIX-CONTENT-BOLD-ACCENT",
    description="Bold text uses primary color for visual interest",
    slide_types=["content"],
    theme_names=None,
    vr_criteria=["VR4", "VR5"],
    css_rules="""
    .slide-type-content .slide-node.text-node strong {
        color: var(--cl-primary);
    }
    """,
    priority=0,
))

register_fix(CSSFix(
    id="FIX-CONTENT-ACCENT-BORDER",
    description="Content-heavy slides get accent border-top for structure",
    slide_types=["content"],
    theme_names=None,
    vr_criteria=["VR2", "VR5"],
    css_rules="""
    .slide-type-content.flow-top .slide-node.text-node:not(.heading-node) {
        border-top: 2px solid var(--cl-primary);
        padding-top: 24px;
    }
    """,
    priority=0,
))

register_fix(CSSFix(
    id="FIX-COMPARISON-WHITESPACE",
    description="Comparison slides: tighter padding to reduce 58% whitespace",
    slide_types=["comparison"],
    theme_names=None,
    vr_criteria=["VR3"],
    css_rules="""
    .slide-type-comparison .flow-row .slide-node {
        padding: 16px 20px;
    }
    """,
    priority=0,
))

register_fix(CSSFix(
    id="FIX-TITLE-SUBTITLE-SIZE",
    description="Subtitle text bumped from h3 to h2 size",
    slide_types=["title"],
    theme_names=None,
    vr_criteria=["VR1", "VR2"],
    css_rules="""
    .slide-group.flow-layout > .slide-node.subtitle-node p {
        font-size: 31px;
    }
    """,
    priority=0,
))
