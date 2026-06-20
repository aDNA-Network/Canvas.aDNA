"""Deterministic layout — the producer-side geometry for a deck.

Slides are laid out left-to-right in a single row (a deck is a linear sequence, so the ``sequence`` chain reads as a
straight line). Each slide is a 16:9 group; the ``deck_root`` group encloses them. All coordinates are **integers**
and a pure function of the input (reproducible). Interior placement is in ``slides.py`` (each slide type owns its
internal layout, like CanvasForge's slide builders).
"""

from __future__ import annotations

from dataclasses import dataclass

# Slide geometry (16:9), integer points.
SLIDE_W = 1280
SLIDE_H = 720
SLIDE_GAP = 96
DECK_PAD = 80
LABEL_BAND = 64    # room under the deck label, above the slide row
SLIDE_PAD = 56     # inner padding within a slide


@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int

    def as_node(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "width": self.w, "height": self.h}


def slide_box(idx: int) -> Box:
    """Geometry of the idx-th slide group (single horizontal row)."""
    x = DECK_PAD + idx * (SLIDE_W + SLIDE_GAP)
    y = DECK_PAD + LABEL_BAND
    return Box(x, y, SLIDE_W, SLIDE_H)


def deck_box(n_slides: int) -> Box:
    """Geometry of the enclosing deck_root group."""
    w = DECK_PAD * 2 + n_slides * SLIDE_W + (n_slides - 1) * SLIDE_GAP
    h = DECK_PAD * 2 + LABEL_BAND + SLIDE_H
    return Box(0, 0, w, h)


def content_rect(box: Box) -> Box:
    """The inner content area of a slide (inside SLIDE_PAD)."""
    return Box(box.x + SLIDE_PAD, box.y + SLIDE_PAD, box.w - 2 * SLIDE_PAD, box.h - 2 * SLIDE_PAD)


def est_text_height(text: str, *, wrap: int = 60, line_h: int = 30, pad: int = 24, min_h: int = 60) -> int:
    """Deterministic text-node height from a line-count estimate."""
    raw = text.split("\n") or [""]
    lines = sum(max(1, (len(ln) // wrap) + 1) for ln in raw)
    return max(min_h, lines * line_h + pad)
