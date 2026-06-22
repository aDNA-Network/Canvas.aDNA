"""Deterministic integer geometry — a vertical stack of post cards (copy + optional image) for a single post or thread.

All coordinates are integers and a pure function of the input (no randomness, no wall-clock) so the round-trip sync hash
is stable. Geometry only needs to be deterministic + roughly non-overlapping; overlap/render scoring is PT-P5-gated.
"""

from __future__ import annotations

from dataclasses import dataclass

CARD_W = 600
PAD = 48
GAP_Y = 32          # gap between consecutive panels
TEXT_PAD = 18
LINE_H = 22
IMG_H = 320         # fixed image-card height
GAP_IMG = 12        # gap between a post's copy and its image
WRAP = 60           # rough chars-per-line for height estimation
INNER_W = CARD_W - 2 * PAD


@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int

    def as_node(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "width": self.w, "height": self.h}


def _text_h(text: str) -> int:
    """A copy card's height: padding + one line-height per (wrapped) line. Deterministic."""
    lines = max(1, text.count("\n") + 1 + len(text) // WRAP)
    return TEXT_PAD * 2 + lines * LINE_H


def stack(panels) -> tuple[list[tuple[Box, Box | None]], Box]:
    """Lay out the panels top-to-bottom; return (per-panel (post_box, img_box|None) in order, the post_root box)."""
    boxes: list[tuple[Box, Box | None]] = []
    y = PAD
    for panel in panels:
        post_box = Box(PAD, y, INNER_W, _text_h(panel.text))
        y += post_box.h
        img_box: Box | None = None
        if panel.image_prompt:
            y += GAP_IMG
            img_box = Box(PAD, y, INNER_W, IMG_H)
            y += IMG_H
        boxes.append((post_box, img_box))
        y += GAP_Y

    bottom = (y - GAP_Y + PAD) if boxes else (PAD * 2)
    root = Box(0, 0, CARD_W, bottom)
    return boxes, root
