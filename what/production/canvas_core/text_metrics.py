"""Text extent measurement for canvas text nodes.

Provides ``measure_text_extent()`` — the primary helper consumed by the
III trap pack (CV-TEXT-BOUNDS-01) to detect overflow of text content
beyond its declared canvas-node dimensions.

Two measurement paths:
  1. **Pillow** — ``ImageDraw.textbbox()`` with a resolved system font.
     Accurate, but requires a font file on disk.
  2. **Heuristic** — character-count estimation with configurable width
     factor.  Always available; used as fallback when Pillow font
     resolution fails (CI, minimal containers, missing fonts).

The third return value of ``measure_text_extent()`` records which path
fired (``"pillow"`` or ``"heuristic"``) so downstream consumers can
assess confidence.

New in M-1-07 (Phase 1 — Substrate Extraction).  Pure substrate — zero
application imports.
"""

from __future__ import annotations

import logging
import math
import os
import re
from pathlib import Path

_log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Markdown stripping
# ---------------------------------------------------------------------------

_MD_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"!\[.*?\]\(.*?\)"), ""),          # images
    (re.compile(r"\[([^\]]+)\]\(.*?\)"), r"\1"),   # links -> text
    (re.compile(r"\*\*(.+?)\*\*"), r"\1"),         # bold
    (re.compile(r"\*(.+?)\*"), r"\1"),             # italic
    (re.compile(r"__(.+?)__"), r"\1"),             # bold alt
    (re.compile(r"_(.+?)_"), r"\1"),               # italic alt
    (re.compile(r"~~(.+?)~~"), r"\1"),             # strikethrough
    (re.compile(r"`(.+?)`"), r"\1"),               # inline code
    (re.compile(r"^#{1,6}\s+", re.MULTILINE), ""), # headings
    (re.compile(r"^[-*+]\s+", re.MULTILINE), ""),  # bullets
    (re.compile(r"^\d+\.\s+", re.MULTILINE), ""),  # numbered lists
    (re.compile(r"^>\s+", re.MULTILINE), ""),      # blockquotes
]


def _strip_markdown(text: str) -> str:
    """Remove common markdown decorators for accurate character counting."""
    result = text
    for pattern, replacement in _MD_PATTERNS:
        result = pattern.sub(replacement, result)
    return result


# ---------------------------------------------------------------------------
# Font resolution (Pillow path)
# ---------------------------------------------------------------------------

_SYSTEM_FONT_DIRS: list[str] = [
    "/System/Library/Fonts/Supplemental",  # macOS
    "/System/Library/Fonts",               # macOS
    "/Library/Fonts",                      # macOS user
    "/usr/share/fonts/truetype",           # Linux (Debian/Ubuntu)
    "/usr/share/fonts",                    # Linux (generic)
]

_FAMILY_MAP: dict[str, list[str]] = {
    "sans-serif": ["Arial.ttf", "Helvetica.ttf", "DejaVuSans.ttf",
                   "LiberationSans-Regular.ttf", "FreeSans.ttf"],
    "serif": ["Times New Roman.ttf", "TimesNewRoman.ttf",
              "DejaVuSerif.ttf", "LiberationSerif-Regular.ttf"],
    "monospace": ["Courier New.ttf", "CourierNew.ttf",
                  "DejaVuSansMono.ttf", "LiberationMono-Regular.ttf"],
}

# Line-height multiplier (CSS-like 1.4 default).
_LINE_HEIGHT_FACTOR = 1.4


def _resolve_font(
    font_family: str | None,
    font_size: float,
) -> tuple[object | None, str]:
    """Attempt to load a Pillow ImageFont.

    Returns ``(font_object_or_None, path_description)``.
    """
    try:
        from PIL import ImageFont  # noqa: F811
    except ImportError:
        return None, "pillow-unavailable"

    candidates: list[str] = []
    if font_family:
        key = font_family.lower().strip()
        candidates = _FAMILY_MAP.get(key, [key + ".ttf", key + ".otf"])

    # Also try common defaults.
    candidates.extend(_FAMILY_MAP.get("sans-serif", []))

    for directory in _SYSTEM_FONT_DIRS:
        if not os.path.isdir(directory):
            continue
        for name in candidates:
            path = os.path.join(directory, name)
            if os.path.isfile(path):
                try:
                    font = ImageFont.truetype(path, size=int(font_size))
                    return font, path
                except Exception:
                    continue

    # Last resort: Pillow's built-in bitmap font (very inaccurate but real).
    try:
        return ImageFont.load_default(), "pillow-default"
    except Exception:
        return None, "pillow-failed"


# ---------------------------------------------------------------------------
# Heuristic path
# ---------------------------------------------------------------------------


def _estimate_text_extent_heuristic(
    text: str,
    font_size: float,
    max_width: float | None,
    monospace: bool = False,
) -> tuple[float, float, str]:
    """Character-count heuristic for text extent.

    Returns ``(width, height, "heuristic")``.
    """
    clean = _strip_markdown(text)
    if not clean.strip():
        return (0.0, 0.0, "heuristic")

    char_factor = 0.6 if monospace else 0.55
    lines = clean.split("\n")
    total_height = 0.0
    max_line_width = 0.0

    for line in lines:
        line_width = len(line) * char_factor * font_size
        max_line_width = max(max_line_width, line_width)
        if max_width and max_width > 0 and line_width > max_width:
            wrap_lines = math.ceil(line_width / max_width)
            total_height += wrap_lines * font_size * _LINE_HEIGHT_FACTOR
        else:
            total_height += font_size * _LINE_HEIGHT_FACTOR

    # If max_width supplied, effective width is capped.
    effective_width = min(max_line_width, max_width) if max_width else max_line_width

    return (effective_width, total_height, "heuristic")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def measure_text_extent(
    text: str,
    font_family: str | None = None,
    font_size: float = 16.0,
    max_width: float | None = None,
) -> tuple[float, float, str]:
    """Measure the rendered extent of text content.

    Args:
        text: Text content (may contain markdown decorators).
        font_family: CSS-style font family name (optional).
        font_size: Font size in pixels (default 16.0).
        max_width: Maximum width for text wrapping (optional).

    Returns:
        ``(measured_width, measured_height, path_name)`` where
        *path_name* is ``"pillow"`` or ``"heuristic"``.
    """
    if not text or not text.strip():
        return (0.0, 0.0, "heuristic")

    clean = _strip_markdown(text)
    is_mono = font_family and "mono" in font_family.lower()

    # --- Pillow path ---
    font, font_desc = _resolve_font(font_family, font_size)
    if font is not None:
        try:
            from PIL import Image, ImageDraw

            scratch = Image.new("L", (1, 1))
            draw = ImageDraw.Draw(scratch)

            # Pillow doesn't natively wrap at max_width, so we simulate.
            lines = clean.split("\n")
            total_height = 0.0
            max_line_width = 0.0

            for line in lines:
                if not line:
                    total_height += font_size * _LINE_HEIGHT_FACTOR
                    continue

                # Wrap long lines manually.
                if max_width and max_width > 0:
                    wrapped = _wrap_line_pillow(draw, font, line, max_width)
                else:
                    wrapped = [line]

                for wline in wrapped:
                    bbox = draw.textbbox((0, 0), wline, font=font)
                    w = bbox[2] - bbox[0]
                    h = bbox[3] - bbox[1]
                    max_line_width = max(max_line_width, w)
                    total_height += max(h, font_size) * _LINE_HEIGHT_FACTOR

            effective_width = (
                min(max_line_width, max_width) if max_width else max_line_width
            )
            return (float(effective_width), float(total_height), "pillow")

        except Exception as exc:
            _log.debug("Pillow measurement failed (%s), falling back to heuristic", exc)

    # --- Heuristic fallback ---
    return _estimate_text_extent_heuristic(
        text, font_size, max_width, monospace=bool(is_mono),
    )


def _wrap_line_pillow(
    draw: object,
    font: object,
    line: str,
    max_width: float,
) -> list[str]:
    """Word-wrap a single line using Pillow measurements."""
    words = line.split()
    if not words:
        return [line]

    wrapped: list[str] = []
    current = words[0]

    for word in words[1:]:
        test = current + " " + word
        bbox = draw.textbbox((0, 0), test, font=font)  # type: ignore[union-attr]
        if (bbox[2] - bbox[0]) <= max_width:
            current = test
        else:
            wrapped.append(current)
            current = word

    wrapped.append(current)
    return wrapped
