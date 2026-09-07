"""Deterministic integer geometry — a vertical stack of post cards (copy + optional image) for a single post or thread.

All coordinates are integers and a pure function of the input (no randomness, no wall-clock) so the round-trip sync hash
is stable. Geometry only needs to be deterministic + roughly non-overlapping; overlap/render scoring is PT-P5-gated.

⛩ **P2c (2026-09-07):** card heights come from ``canvas_core.layout_fit`` rather than ``WRAP=60 / LINE_H=22``. The
guess understated: the single-post example showed **~72%** of its copy in Obsidian — on a producer whose entire output
*is* the copy. A ``####`` title card was added for ``CV-HIERARCHY-01``'s title slot.
"""

from __future__ import annotations

from dataclasses import dataclass

from canvas_core.layout_fit import fit_group_label, fit_group_size, fit_text_height, heading

CARD_W = 600
PAD = 48
GAP_Y = 32          # gap between consecutive panels
TEXT_PAD = 18
LINE_H = 22
IMG_H = 320         # fixed image-card height
GAP_IMG = 12        # gap between a post's copy and its image
INNER_W = CARD_W - 2 * PAD
TEXT_MIN_H = TEXT_PAD * 2 + LINE_H   # floor: a one-line card


@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int

    def as_node(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "width": self.w, "height": self.h}


def text_h(text: str) -> int:
    """A copy card's height — measured, so the whole post renders. Deterministic."""
    return fit_text_height(text, INNER_W, min_height=TEXT_MIN_H)


def title_text(title: str) -> str:
    """The thread's title card — ``#### <title>`` (CV-HIERARCHY-01 title slot; 42.6px lead)."""
    return heading(title)


def stack(panels, title: str = "") -> tuple[list[tuple[Box, Box | None]], Box, Box | None]:
    """Lay out the panels top-to-bottom; return (per-panel (post_box, img_box|None), post_root, title box)."""
    boxes: list[tuple[Box, Box | None]] = []
    y = PAD
    top = y

    title_box: Box | None = None
    if title:
        title_box = Box(PAD, y, INNER_W, fit_text_height(title_text(title), INNER_W, min_height=TEXT_MIN_H))
        y += title_box.h + GAP_Y

    for panel in panels:
        post_box = Box(PAD, y, INNER_W, text_h(panel.text))
        y += post_box.h
        img_box: Box | None = None
        if panel.image_prompt:
            y += GAP_IMG
            img_box = Box(PAD, y, INNER_W, IMG_H)
            y += IMG_H
        boxes.append((post_box, img_box))
        y += GAP_Y

    content_h = (y - GAP_Y) - top if (boxes or title_box) else 0
    w, _ = fit_group_size(INNER_W, content_h, PAD)
    w = max(w, CARD_W)
    if title:
        _, min_w = fit_group_label(title, w)
        w = max(w, min_w)
    bottom = (top + content_h + PAD) if content_h else (PAD * 2)
    root = Box(0, 0, w, bottom)
    return boxes, root, title_box
