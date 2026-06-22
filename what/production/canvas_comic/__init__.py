"""canvas_comic — comic application package for CanvasForge.

Imports canvas_core (substrate), never canvas_presentation.
Populated in Phase 2b (M-2b-01..05) per ADR 001 § Directory Shape.
"""

from .comic import (
    ComicPageBuilder,
    ComicProductionAdapter,
    ComicReport,
    Page,
    Panel,
    PendingPanel,
    ActInfo,
    CharacterState,
    StoryState,
    SpreadColorScript,
    PanelTypeTemplate,
    StageResult,
    TRIM_WIDTH,
    TRIM_HEIGHT,
    BLEED_WIDTH,
    BLEED_HEIGHT,
    TOTAL_PAGES,
    TOTAL_SPREADS,
    ASPECT_RATIOS,
    PANEL_TYPE_TEMPLATES,
    CHARACTER_STANLEY,
    CHARACTER_AGENT_STANLEY,
    CHARACTER_HELIX,
    STYLE_GHIBLI,
    STYLE_PIXEL,
    STYLE_TRANSITION,
)

__all__ = [
    "ComicPageBuilder",
    "ComicProductionAdapter",
    "ComicReport",
    "Page",
    "Panel",
    "PendingPanel",
    "ActInfo",
    "CharacterState",
    "StoryState",
    "SpreadColorScript",
    "PanelTypeTemplate",
    "StageResult",
]
