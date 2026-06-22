"""Deterministic integer geometry — a single vertical stack for a one-page letter.

The whole letter is one ``letter_root`` group enclosing a top-to-bottom column of block boxes (letterhead, date,
recipient, salutation, one box per body paragraph, closing, signature). Each box is a fixed-width band; its height
scales with the number of text lines so longer blocks roughly fit. All coordinates are **integers** and a pure
function of the input (no randomness, no wall-clock) so the round-trip sync hash is stable across rebuilds. Geometry is
not scored here — it only needs to be deterministic and roughly non-overlapping (overlap/containment scoring is
PT-P5-gated).
"""

from __future__ import annotations

from dataclasses import dataclass

# Page + band geometry, integer points (roughly US-Letter-ish proportions; not scored, only deterministic).
PAGE_W = 800          # the writable column width
PAD = 64              # padding inside the letter_root group, around the column
LABEL_BAND = 48       # room under the group label
LINE_H = 24           # vertical room per text line within a band
BAND_PAD = 20         # vertical padding inside a band
GAP_Y = 28            # vertical gap between consecutive bands
BLOCK_W = PAGE_W - 2 * PAD  # the band width inside the padded column


@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int

    def as_node(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "width": self.w, "height": self.h}


def _band_height(line_count: int) -> int:
    """A band's height = padding + one line-height per text line (min one line)."""
    return BAND_PAD * 2 + max(1, line_count) * LINE_H


def stack(line_counts: list[int]) -> tuple[list[Box], Box]:
    """Lay out ``len(line_counts)`` bands top-to-bottom; return (per-block boxes in order, the letter_root box).

    ``line_counts[i]`` is the number of text lines in block ``i`` (drives that band's height). Deterministic.
    """
    boxes: list[Box] = []
    y = PAD + LABEL_BAND
    for n_lines in line_counts:
        h = _band_height(n_lines)
        boxes.append(Box(PAD, y, BLOCK_W, h))
        y += h + GAP_Y

    # The group encloses the whole column (drop the trailing gap, add the bottom pad).
    bottom = (y - GAP_Y + PAD) if boxes else (PAD + LABEL_BAND + PAD)
    root = Box(0, 0, PAGE_W, bottom)
    return boxes, root
