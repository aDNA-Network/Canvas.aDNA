"""Deterministic layout — the producer-side geometry for a deck.

Slides are laid out left-to-right in a single row (a deck is a linear sequence, so the ``sequence`` chain reads as a
straight line). Each slide is a 16:9 group; the ``deck_root`` group encloses them. All coordinates are **integers**
and a pure function of the input (reproducible). Interior placement is in ``slides.py`` (each slide type owns its
internal layout, like CanvasForge's slide builders).

⛩ **P2c (2026-09-07):** interior heights come from ``canvas_core.layout_fit``. The **slide box stays 16:9** — a deck's
frame is its format, not a variable, and the ``deck`` trap profile now says so (a slide is meant to be well-filled;
the knowledge-board fill/title aesthetics do not apply). What was wrong was the *interior*: fixed 80/90px heading
bands holding ``##`` leads that cost 98.9px before a character rendered.
"""

from __future__ import annotations

from dataclasses import dataclass

from canvas_core.layout_fit import fit_group_label, fit_text_height, heading

# Slide geometry (16:9), integer points. ASPECT is emitted as canvas metadata — a deck genuinely
# has an aspect ratio, and CV-DIMENSION-VISIBILITY-01 (admitted by the `deck` profile) asks for it.
SLIDE_W = 1280
SLIDE_H = 720
ASPECT_RATIO = "16:9"
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


def deck_box(n_slides: int, label: str = "") -> Box:
    """Geometry of the enclosing deck_root group.

    The frame is deliberately *not* ratio-scaled — a deck is a slide row, and the ``deck`` profile
    excludes the fill aesthetic. It is only widened when its label would otherwise ellipsise.
    """
    w = DECK_PAD * 2 + n_slides * SLIDE_W + (n_slides - 1) * SLIDE_GAP
    h = DECK_PAD * 2 + LABEL_BAND + SLIDE_H
    if label:
        _, min_w = fit_group_label(label, w)
        w = max(w, min_w)
    return Box(0, 0, w, h)


def content_rect(box: Box) -> Box:
    """The inner content area of a slide (inside SLIDE_PAD)."""
    return Box(box.x + SLIDE_PAD, box.y + SLIDE_PAD, box.w - 2 * SLIDE_PAD, box.h - 2 * SLIDE_PAD)


def est_text_height(text: str, *, width: int = SLIDE_W - 2 * SLIDE_PAD, min_h: int = 60) -> int:
    """Deterministic text-node height — the height ``CV-TEXT-BOUNDS-01`` will require.

    ⛩ P2c: was a character-count estimate (``wrap=60``, ``line_h=30``, ``pad=24``). Callers that
    passed ``wrap=200`` for a table were tuning a guess against a measurement they could have made.
    """
    return fit_text_height(text, width, min_height=min_h)


def heading_text(title: str) -> str:
    """A slide heading — ``#### <title>``.

    Was ``#`` (title/section slides) and ``##`` (content/image/table): 56.7px and 98.9px of
    non-collapsing lead before any body text, in bands fixed at 80–160px. All five of this
    producer's ``CV-LEAD-COST-01`` findings. ``####`` costs 42.6px (F-P2-3/F-P2-9).
    """
    return heading(title)


def heading_height(title: str, *, width: int = SLIDE_W - 2 * SLIDE_PAD, min_h: int = 80) -> int:
    return est_text_height(heading_text(title), width=width, min_h=min_h)
