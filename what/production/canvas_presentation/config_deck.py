"""Deck-specific configuration — themes, palettes, audiences, arcs, layout constants.

Migrated from lattice-protocol/extensions/canvas/canvas_config.py (deck-specific
symbols only).  Substrate-eligible symbols (VALID_ROLES, ImageFormat, PendingImage)
remain in canvas_core.config_substrate per ADR 001 § canvas_config Split.

Populated in M-2a-01 (Phase 2a — Deck Application Extraction).
"""

from __future__ import annotations

from dataclasses import dataclass

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------

SLIDE_WIDTH = 1200
SLIDE_HEIGHT = 1100
GRID_COLUMNS = 2
ROW_GAP = 200

HEADING_TOP_MARGIN = 40
HEADING_HEIGHT = 120
BODY_TOP_GAP = 20
CONTENT_SIDE_MARGIN = 60
CONTENT_WIDTH = SLIDE_WIDTH - 2 * CONTENT_SIDE_MARGIN  # 1080

MIN_SLIDES = 3
MAX_SLIDES = 15
MAX_WORDS_PER_NODE = 100

WORDS_TITLE = 30
WORDS_CONTENT = 100
WORDS_COMPARISON = 80
WORDS_QUOTE = 80
WORDS_STATS = 50
WORDS_SECTION_DIVIDER = 20
WORDS_VIDEO = 30

_WORDS_BY_TYPE: dict[str, int] = {
    "title": WORDS_TITLE,
    "content": WORDS_CONTENT,
    "comparison": WORDS_COMPARISON,
    "quote": WORDS_QUOTE,
    "stats": WORDS_STATS,
    "section_divider": WORDS_SECTION_DIVIDER,
    "video": WORDS_VIDEO,
    "image": WORDS_CONTENT,
    "diagram": WORDS_CONTENT,
    "timeline": WORDS_CONTENT,
    "process": WORDS_CONTENT,
    "three_column": WORDS_COMPARISON,
    "key_value": WORDS_CONTENT,
    "matrix": 60,
    "collage": 30,
}

# ---------------------------------------------------------------------------
# Density profiles
# ---------------------------------------------------------------------------

_DENSITY_MULTIPLIERS: dict[str, float] = {
    "sparse": 0.5,
    "balanced": 1.0,
    "dense": 1.5,
}

_WHITESPACE_TARGETS: dict[str, tuple[float, float]] = {
    "title": (0.60, 0.80),
    "section_divider": (0.70, 0.90),
    "content": (0.35, 0.55),
    "comparison": (0.25, 0.45),
    "stats": (0.40, 0.60),
    "quote": (0.55, 0.75),
    "image": (0.15, 0.45),
    "diagram": (0.15, 0.45),
    "video": (0.20, 0.50),
    "timeline": (0.25, 0.50),
    "process": (0.25, 0.50),
    "three_column": (0.25, 0.45),
    "key_value": (0.30, 0.55),
    "matrix": (0.20, 0.40),
    "collage": (0.10, 0.35),
}

# ---------------------------------------------------------------------------
# Audience Context System
# ---------------------------------------------------------------------------


@dataclass
class AudienceContext:
    """Configures density, word limits, and layout for a target audience."""

    name: str
    density_profile: str
    word_range: tuple[int, int]
    preferred_layout: str
    slide_range: tuple[int, int] = (5, 15)
    content_fill_target: float = 0.5


_AUDIENCE_CONTEXTS: dict[str, AudienceContext] = {
    "keynote": AudienceContext("keynote", "sparse", (10, 25), "grid_1col", (8, 20), 0.30),
    "pitch": AudienceContext("pitch", "balanced", (20, 50), "grid_2col", (6, 12), 0.45),
    "meeting": AudienceContext("meeting", "balanced", (40, 80), "grid_2col", (4, 10), 0.50),
    "async": AudienceContext("async", "dense", (60, 120), "grid_2col", (5, 15), 0.55),
    "reference": AudienceContext("reference", "dense", (80, 150), "grid_3col", (8, 25), 0.60),
}

# ---------------------------------------------------------------------------
# Theme System
# ---------------------------------------------------------------------------


@dataclass
class PresentationTheme:
    """Visual theme for presentations."""

    name: str
    primary_color: str
    secondary_color: str
    accent_color: str
    background_style: str = "default"
    font_suggestion: str = ""
    logo_path: str | None = None


THEME_TOKYO_NIGHT = PresentationTheme("tokyo_night", "6", "5", "4", font_suggestion="JetBrains Mono, Fira Code, Menlo, Consolas, monospace")
THEME_LATTICE_BRAND = PresentationTheme("lattice_brand", "6", "4", "1", font_suggestion="Space Grotesk, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif")
THEME_SCIENTIFIC = PresentationTheme("scientific", "5", "3", "2", font_suggestion="Charter, Georgia, Cambria, Times New Roman, serif")
THEME_LATTICE_DARK = PresentationTheme("lattice_dark", "6", "4", "1", font_suggestion="Inter, -apple-system, BlinkMacSystemFont, sans-serif")
THEME_LATTICE_LIGHT = PresentationTheme("lattice_light", "5", "3", "1", font_suggestion="Inter, -apple-system, BlinkMacSystemFont, sans-serif")
THEME_SCIENCE_STANLEY = PresentationTheme("science_stanley", "6", "5", "4", font_suggestion="JetBrains Mono, Fira Code, Menlo, monospace")
THEME_ACADEMIC = PresentationTheme("academic", "5", "3", "2", font_suggestion="Charter, Georgia, Cambria, serif")

PRESENTATION_THEMES: dict[str, PresentationTheme] = {
    "tokyo_night": THEME_TOKYO_NIGHT,
    "lattice_brand": THEME_LATTICE_BRAND,
    "scientific": THEME_SCIENTIFIC,
    "lattice_dark": THEME_LATTICE_DARK,
    "lattice_light": THEME_LATTICE_LIGHT,
    "science_stanley": THEME_SCIENCE_STANLEY,
    "academic": THEME_ACADEMIC,
}


@dataclass
class ThemePalette:
    """Background, text, and border colors for HTML rendering."""

    bg: str
    bg_lighter: str
    text: str
    text_dim: str
    border: str


THEME_PALETTES: dict[str, ThemePalette] = {
    "tokyo_night": ThemePalette("#1a1b26", "#24283b", "#c0caf5", "#6272a4", "#3b4261"),
    "lattice_dark": ThemePalette("#1e1e2e", "#2a2a3e", "#cdd6f4", "#6c7086", "#45475a"),
    "lattice_brand": ThemePalette("#1a1b26", "#24283b", "#c0caf5", "#6272a4", "#3b4261"),
    "science_stanley": ThemePalette("#1a1b26", "#24283b", "#c0caf5", "#6272a4", "#3b4261"),
    "lattice_light": ThemePalette("#ffffff", "#f5f5f7", "#1d1d1f", "#6e6e73", "#d2d2d7"),
    "scientific": ThemePalette("#fafaf8", "#f0f0ec", "#2c2c2c", "#6b6b6b", "#d4d4cc"),
    "academic": ThemePalette("#fffef9", "#f8f6f0", "#2d2926", "#7a7267", "#d6cfc4"),
}

DEFAULT_PALETTE = THEME_PALETTES["tokyo_night"]

# ---------------------------------------------------------------------------
# Narrative Arc Framework
# ---------------------------------------------------------------------------


@dataclass
class ArcSection:
    """A section within a narrative arc."""

    name: str
    slide_types: list[str]
    description: str


@dataclass
class NarrativeArc:
    """Storytelling structure for presentations."""

    name: str
    sections: list[ArcSection]
    description: str = ""

    @property
    def section_names(self) -> list[str]:
        return [s.name for s in self.sections]

    def expected_types(self) -> list[str]:
        types: list[str] = []
        for section in self.sections:
            types.extend(section.slide_types)
        return types

    @classmethod
    def from_brief(cls, brief: str, arc_name: str = "problem_solution") -> list[dict[str, str]]:
        arc = NARRATIVE_ARCS.get(arc_name)
        if not arc:
            raise ValueError(f"Unknown arc {arc_name!r}. Available: {sorted(NARRATIVE_ARCS)}")
        outline: list[dict[str, str]] = []
        for section in arc.sections:
            for stype in section.slide_types:
                outline.append({
                    "type": stype,
                    "title": f"{section.name}: {stype.replace('_', ' ').title()}",
                    "section": section.name,
                    "brief": brief,
                })
        return outline


NARRATIVE_ARCS: dict[str, NarrativeArc] = {
    "problem_solution": NarrativeArc(name="problem_solution", description="Challenge \u2192 Approach \u2192 Evidence \u2192 Result \u2192 Ask", sections=[
        ArcSection("Opening", ["title"], "Set the stage"),
        ArcSection("Challenge", ["content", "stats"], "Define the problem"),
        ArcSection("Approach", ["content", "process"], "Present the solution"),
        ArcSection("Evidence", ["stats", "image"], "Show proof"),
        ArcSection("Result", ["content", "key_value"], "Summarize outcomes"),
        ArcSection("Ask", ["content"], "Call to action"),
    ]),
    "journey": NarrativeArc(name="journey", description="Where we were \u2192 What changed \u2192 Where we are", sections=[
        ArcSection("Opening", ["title"], "Set context"),
        ArcSection("Origin", ["content", "timeline"], "Starting point"),
        ArcSection("Transformation", ["content", "process"], "What changed"),
        ArcSection("Current State", ["stats", "key_value"], "Where we are"),
        ArcSection("Future", ["content"], "Vision ahead"),
    ]),
    "comparison": NarrativeArc(name="comparison", description="Option A \u2192 Option B \u2192 Recommendation", sections=[
        ArcSection("Opening", ["title"], "Frame the decision"),
        ArcSection("Context", ["content"], "Background"),
        ArcSection("Option A", ["content", "stats"], "First option"),
        ArcSection("Option B", ["content", "stats"], "Second option"),
        ArcSection("Analysis", ["comparison", "three_column", "matrix"], "Side by side"),
        ArcSection("Recommendation", ["content"], "Final verdict"),
    ]),
    "demonstration": NarrativeArc(name="demonstration", description="Context \u2192 Demo \u2192 Impact", sections=[
        ArcSection("Opening", ["title"], "Introduction"),
        ArcSection("Context", ["content"], "Why this matters"),
        ArcSection("Demo", ["image", "process", "collage"], "Show it working"),
        ArcSection("Impact", ["stats", "key_value"], "Measure results"),
        ArcSection("Next Steps", ["content"], "What's next"),
    ]),
    "educational": NarrativeArc(name="educational", description="Topic \u2192 Concepts \u2192 Examples \u2192 Summary", sections=[
        ArcSection("Opening", ["title"], "Topic introduction"),
        ArcSection("Concepts", ["content", "content"], "Core ideas"),
        ArcSection("Examples", ["content", "diagram"], "Illustrations"),
        ArcSection("Practice", ["content", "key_value"], "Apply the knowledge"),
        ArcSection("Summary", ["content"], "Key takeaways"),
    ]),
    "workshop": NarrativeArc(name="workshop", description="Welcome \u2192 Context \u2192 Activities \u2192 Takeaways", sections=[
        ArcSection("Welcome", ["title"], "Set the tone"),
        ArcSection("Context", ["content", "stats"], "Why we're here"),
        ArcSection("Activity 1", ["content", "process", "diagram"], "First exercise"),
        ArcSection("Debrief 1", ["content", "key_value"], "Reflect on activity 1"),
        ArcSection("Activity 2", ["content", "process", "diagram"], "Second exercise"),
        ArcSection("Debrief 2", ["content", "key_value"], "Reflect on activity 2"),
        ArcSection("Takeaways", ["content", "stats"], "Key learnings"),
    ]),
    "quarterly_review": NarrativeArc(name="quarterly_review", description="Title \u2192 Summary \u2192 Metrics \u2192 Next Quarter \u2192 Ask", sections=[
        ArcSection("Title", ["title"], "Quarter identification"),
        ArcSection("Executive Summary", ["content"], "High-level overview"),
        ArcSection("Metrics", ["stats", "key_value"], "Quantitative results"),
        ArcSection("Highlights", ["content", "image"], "Key wins"),
        ArcSection("Challenges", ["content", "comparison"], "Issues and risks"),
        ArcSection("Next Quarter", ["content", "timeline"], "Forward plan"),
        ArcSection("Ask", ["content"], "Resource requests"),
    ]),
    "research_defense": NarrativeArc(name="research_defense", description="Title \u2192 Background \u2192 Methods \u2192 Results \u2192 Conclusion", sections=[
        ArcSection("Title", ["title"], "Research identification"),
        ArcSection("Background", ["content"], "Prior work and context"),
        ArcSection("Hypothesis", ["content", "quote"], "Research question"),
        ArcSection("Methods", ["content", "process", "diagram"], "Experimental approach"),
        ArcSection("Results", ["stats", "image", "key_value"], "Data and findings"),
        ArcSection("Discussion", ["content", "comparison"], "Interpretation"),
        ArcSection("Conclusion", ["content"], "Summary of contributions"),
        ArcSection("References", ["content"], "Citations and acknowledgments"),
    ]),
}
