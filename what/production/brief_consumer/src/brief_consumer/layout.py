"""Deterministic layout — the producer-side geometry.

``canvas_std.to_canvas`` emits *default* geometry by design (real layout is producer-side). The brief consumer owns a
simple, deterministic vertical-stack layout: a single page region (the canonical surface) enclosing per-section
heading / body / source blocks. All coordinates are **integers** (Core requires integer ``x/y/width/height``), and the
layout is a pure function of the input (no randomness, no time) so the generated ``.canvas`` is reproducible.
"""

from __future__ import annotations

from dataclasses import dataclass

# --- Layout constants (integer points) ---------------------------------------------------------
PAGE_X = 0
PAGE_Y = 0
PAD = 40          # page inner padding
TITLE_BAND = 56   # room under the page label before the first block
CONTENT_W = 620   # block width
HEADING_H = 56
SOURCE_H = 40
GAP = 20          # gap between blocks within a section
SECTION_GAP = 48  # gap between sections

# Body height heuristic (deterministic): wrap at ~84 chars, ~22 pt/line, min 88.
_WRAP = 84
_LINE_H = 22
_BODY_MIN_H = 88


@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int


def body_height(text: str) -> int:
    """A deterministic body-node height from the text (line count, wrapped)."""
    raw_lines = text.split("\n") or [""]
    wrapped = sum(max(1, (len(ln) // _WRAP) + 1) for ln in raw_lines)
    return max(_BODY_MIN_H, wrapped * _LINE_H + 24)


def stack(blocks: list[tuple[str, int, int]]) -> tuple[Box, dict[str, Box]]:
    """Lay ordered ``(node_id, height, gap_after)`` blocks into a single vertical column.

    Returns the enclosing page ``Box`` (the canonical surface) and per-node ``Box`` geometry.
    """
    boxes: dict[str, Box] = {}
    x = PAGE_X + PAD
    y = PAGE_Y + PAD + TITLE_BAND
    last_gap = 0
    for nid, height, gap_after in blocks:
        boxes[nid] = Box(x, y, CONTENT_W, int(height))
        y += int(height) + int(gap_after)
        last_gap = int(gap_after)
    bottom = y - last_gap + PAD
    page = Box(PAGE_X, PAGE_Y, CONTENT_W + 2 * PAD, bottom - PAGE_Y)
    return page, boxes
