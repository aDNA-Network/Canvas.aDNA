"""Substrate configuration — symbols shared across all canvas applications.

Split from lattice-protocol/extensions/canvas/canvas_config.py per ADR 001
§ canvas_config Split. Substrate gets: VALID_ROLES, ImageFormat, PendingImage.
Deck-specific symbols (themes, palettes, arcs, audience contexts, layout
constants, word limits, density profiles) migrate to canvas_presentation/
in Wave 2.
"""

from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Semantic Roles (canvas node role classification)
# ---------------------------------------------------------------------------

VALID_ROLES = frozenset({"stage", "io", "metadata", "decision", "critical"})


# ---------------------------------------------------------------------------
# Image Format System
# ---------------------------------------------------------------------------


class ImageFormat:
    """Image format presets for canvas images (substrate-neutral)."""

    LANDSCAPE_16_9 = (1000, 563)
    LANDSCAPE_4_3 = (1000, 750)
    SQUARE = (800, 800)
    PORTRAIT_3_4 = (750, 1000)
    HERO_BANNER = (1100, 400)

    _FORMATS: dict[str, tuple[int, int]] = {
        "landscape_16_9": LANDSCAPE_16_9,
        "landscape_4_3": LANDSCAPE_4_3,
        "square": SQUARE,
        "portrait_3_4": PORTRAIT_3_4,
        "hero_banner": HERO_BANNER,
    }

    @classmethod
    def get(cls, name: str) -> tuple[int, int]:
        """Get (width, height) for a named format."""
        if name not in cls._FORMATS:
            raise ValueError(
                f"Unknown image format {name!r}. Available: {sorted(cls._FORMATS)}"
            )
        return cls._FORMATS[name]

    @classmethod
    def list_formats(cls) -> list[str]:
        return sorted(cls._FORMATS.keys())


# ---------------------------------------------------------------------------
# Pending Image Tracking
# ---------------------------------------------------------------------------


@dataclass
class PendingImage:
    """Tracks a generative image request decoupled from MCP.

    Used by both deck and comic applications — substrate-neutral.
    """

    id: str
    prompt: str
    target_path: str
    slide_id: str  # or panel_id for comics — field name preserved for compat
    status: str = "pending"  # pending | resolved | failed
    format: str = "landscape_16_9"
