"""Deterministic integer geometry — a single vertical stack for a one-page letter.

The whole letter is one ``letter_root`` group enclosing a top-to-bottom column of block boxes (letterhead, date,
recipient, salutation, one box per body paragraph, closing, signature). Each box is a fixed-width band; its height
scales with the number of text lines so longer blocks roughly fit. All coordinates are **integers** and a pure
function of the input (no randomness, no wall-clock) so the round-trip sync hash is stable across rebuilds. Geometry is
not scored here — it only needs to be deterministic and roughly non-overlapping (overlap/containment scoring is
PT-P5-gated).

⛩ **P2c (2026-09-07):** band heights come from ``canvas_core.layout_fit`` rather than a line count × ``LINE_H``.
"Roughly fit" was the defect, not the design: four of this producer's five findings were nodes showing 75–95% of
their text. A ``####`` title band was added so the group satisfies ``CV-HIERARCHY-01``'s title slot — a letter's
subject line was previously carried only in the group label, which a reader zoomed out cannot fully read.
"""

from __future__ import annotations

from dataclasses import dataclass

from canvas_core.layout_fit import fit_group_label, fit_group_size, fit_text_height, heading

# Page + band geometry, integer points (roughly US-Letter-ish proportions; not scored, only deterministic).
PAGE_W = 800          # the writable column width
PAD = 64              # padding inside the letter_root group, around the column
LABEL_BAND = 48       # room under the group label
LINE_H = 24           # vertical room per text line within a band
BAND_PAD = 20         # vertical padding inside a band
GAP_Y = 28            # vertical gap between consecutive bands
BLOCK_W = PAGE_W - 2 * PAD  # the band width inside the padded column
BAND_MIN_H = BAND_PAD * 2 + LINE_H   # floor: a one-line band


@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int

    def as_node(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "width": self.w, "height": self.h}


def band_height(text: str) -> int:
    """A band's height — measured, so the whole block renders rather than roughly fitting."""
    return fit_text_height(text, BLOCK_W, min_height=BAND_MIN_H)


def title_text(title: str) -> str:
    """The letter's title band — ``#### <title>`` (CV-HIERARCHY-01 title slot; 42.6px lead)."""
    return heading(title)


def stack(texts: list[str], title: str = "") -> tuple[list[Box], Box, Box | None]:
    """Lay out one band per text top-to-bottom; return (per-block boxes in order, letter_root, title box).

    A non-empty *title* prepends a heading band, which is what puts a markdown heading in the
    group's upper 40% for ``CV-HIERARCHY-01``. Deterministic.
    """
    boxes: list[Box] = []
    y = PAD + LABEL_BAND
    top = y

    title_box: Box | None = None
    if title:
        title_box = Box(PAD, y, BLOCK_W, fit_text_height(title_text(title), BLOCK_W, min_height=BAND_MIN_H))
        y += title_box.h + GAP_Y

    for text in texts:
        h = band_height(text)
        boxes.append(Box(PAD, y, BLOCK_W, h))
        y += h + GAP_Y

    # The group encloses the whole column (drop the trailing gap, add the bottom pad).
    content_h = (y - GAP_Y) - top if (boxes or title_box) else 0
    w, _ = fit_group_size(BLOCK_W, content_h, PAD)
    w = max(w, PAGE_W)
    if title:
        _, min_w = fit_group_label(title, w)
        w = max(w, min_w)
    bottom = (top + content_h + PAD) if content_h else (PAD + LABEL_BAND + PAD)
    root = Box(0, 0, w, bottom)
    return boxes, root, title_box
