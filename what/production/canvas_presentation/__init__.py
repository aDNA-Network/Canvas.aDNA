"""canvas_presentation — deck application package for CanvasForge.

Imports canvas_core (substrate), never canvas_comic.
Populated in Phase 2a (M-2a-01..03) per ADR 001 § Directory Shape.
"""

# --- Deck configuration ---
from .config_deck import (
    PRESENTATION_THEMES,
    THEME_PALETTES,
    NARRATIVE_ARCS,
    DEFAULT_PALETTE,
    _AUDIENCE_CONTEXTS,
    _DENSITY_MULTIPLIERS,
    _WHITESPACE_TARGETS,
    _WORDS_BY_TYPE,
    ArcSection,
    AudienceContext,
    NarrativeArc,
    PresentationTheme,
    ThemePalette,
    SLIDE_WIDTH,
    SLIDE_HEIGHT,
    CONTENT_WIDTH,
    MAX_SLIDES,
    MIN_SLIDES,
    MAX_WORDS_PER_NODE,
)

# --- Deck layout ---
from .layout import (
    LAYOUT_GRID_1COL,
    LAYOUT_GRID_2COL,
    LAYOUT_GRID_3COL,
    LAYOUT_PRESETS,
    LayoutStrategy,
    NodePlacement,
    SlideLayout,
    auto_select_layout,
    compute_dynamic_height,
    get_layout,
    slide_layout_for_strategy,
)

# --- Slide builders (16 types) ---
from .slide_builders import SlideBuilderMixin

# --- PresentationBuilder ---
from .presentation import PresentationBuilder

__all__ = [
    # Config
    "PRESENTATION_THEMES",
    "THEME_PALETTES",
    "NARRATIVE_ARCS",
    "DEFAULT_PALETTE",
    "_AUDIENCE_CONTEXTS",
    "_DENSITY_MULTIPLIERS",
    "_WHITESPACE_TARGETS",
    "ArcSection",
    "AudienceContext",
    "NarrativeArc",
    "PresentationTheme",
    "ThemePalette",
    # Layout
    "LayoutStrategy",
    "SlideLayout",
    "NodePlacement",
    "LAYOUT_GRID_2COL",
    "LAYOUT_GRID_1COL",
    "LAYOUT_GRID_3COL",
    "LAYOUT_PRESETS",
    "auto_select_layout",
    "slide_layout_for_strategy",
    "compute_dynamic_height",
    "get_layout",
    # Builders
    "SlideBuilderMixin",
    "PresentationBuilder",
]
