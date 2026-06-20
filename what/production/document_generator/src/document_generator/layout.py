"""Deterministic layout — the producer-side geometry for a long-form document.

Pages are stacked **top-to-bottom** in a single column (a document reads vertically, unlike the deck's left-to-right
row), so the page ``sequence`` chain reads straight down. Each page is a US-Letter group (816x1056 @ 96dpi); the
``doc_root`` group encloses them. All coordinates are **integers** and a pure function of the input (reproducible).
Interior placement (sections + blocks) is in ``blocks.py``.
"""

from __future__ import annotations

from dataclasses import dataclass

# Page geometry (US Letter @ 96dpi), integer points.
PAGE_W = 816
PAGE_H = 1056
PAGE_GAP = 96       # vertical gutter between pages
DOC_PAD = 80        # padding around the page column inside doc_root
LABEL_BAND = 64     # room under the doc_root label, above the first page
PAGE_PAD = 72       # inner page margin (~0.75in)


@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int

    def as_node(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "width": self.w, "height": self.h}


def page_box(idx: int) -> Box:
    """Geometry of the idx-th page group (single vertical column)."""
    x = DOC_PAD
    y = DOC_PAD + LABEL_BAND + idx * (PAGE_H + PAGE_GAP)
    return Box(x, y, PAGE_W, PAGE_H)


def doc_box(n_pages: int) -> Box:
    """Geometry of the enclosing doc_root group."""
    w = DOC_PAD * 2 + PAGE_W
    h = DOC_PAD * 2 + LABEL_BAND + n_pages * PAGE_H + (n_pages - 1) * PAGE_GAP
    return Box(0, 0, w, h)


def content_rect(box: Box) -> Box:
    """The inner content area of a page (inside PAGE_PAD)."""
    return Box(box.x + PAGE_PAD, box.y + PAGE_PAD, box.w - 2 * PAGE_PAD, box.h - 2 * PAGE_PAD)


def est_text_height(text: str, *, wrap: int = 88, line_h: int = 24, pad: int = 20, min_h: int = 44) -> int:
    """Deterministic text-node height from a line-count estimate."""
    raw = text.split("\n") or [""]
    lines = sum(max(1, (len(ln) // wrap) + 1) for ln in raw)
    return max(min_h, lines * line_h + pad)
