"""Deterministic layout — the producer-side geometry.

``canvas_std.to_canvas`` emits *default* geometry by design (real layout is producer-side). The brief consumer owns a
simple, deterministic vertical-stack layout: a single page region (the canonical surface) enclosing per-section
heading / body / source blocks. All coordinates are **integers** (Core requires integer ``x/y/width/height``), and the
layout is a pure function of the input (no randomness, no time) so the generated ``.canvas`` is reproducible.

⛩ **P2c (2026-09-07):** heights come from ``canvas_core.layout_fit`` — the shared engine-shelf fitter (``adr_004``) —
instead of the local ``_WRAP=84 / _LINE_H=22`` heuristic. That heuristic disagreed with what ``CV-TEXT-BOUNDS-01``
actually measures on **10 of this producer's 17 findings**, the worst node showing ~43% of its text in Obsidian.
"""

from __future__ import annotations

from dataclasses import dataclass

from canvas_core.layout_fit import fit_group_label, fit_group_size, fit_text_height, heading

# --- Layout constants (integer points) ---------------------------------------------------------
PAGE_X = 0
PAGE_Y = 0
PAD = 40          # page inner padding
TITLE_BAND = 56   # room under the page label before the first block
CONTENT_W = 620   # block width
HEADING_H = 56    # FLOOR, not the answer — a wrapping heading is measured and grows past it
SOURCE_H = 40     # a link node renders a bare URL, not measured markdown
GAP = 20          # gap between blocks within a section
SECTION_GAP = 48  # gap between sections


@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int


def heading_text(head: str) -> str:
    """The emitted form of a section heading — ``#### <head>``.

    Was ``## <head>``: 98.9px of non-collapsing lead margin in a 56px node, and 5 of this
    producer's ``CV-LEAD-COST-01`` findings. ``####`` costs 42.6px and stays a real heading, so
    ``CV-HIERARCHY-01``'s title slot still sees it (F-P2-3/F-P2-9).
    """
    return heading(head)


def heading_height(head: str) -> int:
    return fit_text_height(heading_text(head), CONTENT_W, min_height=HEADING_H)


def body_height(text: str) -> int:
    """A deterministic body-node height — the height ``CV-TEXT-BOUNDS-01`` will require."""
    return fit_text_height(text, CONTENT_W, min_height=88)


def stack(blocks: list[tuple[str, int, int]], label: str = "") -> tuple[Box, dict[str, Box]]:
    """Lay ordered ``(node_id, height, gap_after)`` blocks into a single vertical column.

    Returns the enclosing page ``Box`` (the canonical surface) and per-node ``Box`` geometry. The
    page is sized through :func:`canvas_core.layout_fit.fit_group_size` so the column clears
    ``CV-GROUP-PADDING-01``'s fill ceiling (it read 90.75% — *barely*, which is what made a scaling
    defect look like a one-off), and widened to hold *label* without ellipsis.
    """
    boxes: dict[str, Box] = {}
    x = PAGE_X + PAD
    y = PAGE_Y + PAD + TITLE_BAND
    top = y
    for nid, height, gap_after in blocks:
        boxes[nid] = Box(x, y, CONTENT_W, int(height))
        y += int(height) + int(gap_after)
        last_gap = int(gap_after)
    content_h = (y - last_gap) - top if blocks else 0
    w, ratio_h = fit_group_size(CONTENT_W, content_h, PAD)
    # The column starts below the title band; a fill ceiling and an asymmetric top offset are two
    # different constraints, so satisfy both rather than assuming symmetric padding.
    h = max(top + content_h + PAD, ratio_h)
    if label:
        _, min_w = fit_group_label(label, w)
        w = max(w, min_w)
    # Re-centre the column inside a page that may have widened for its label.
    if w > CONTENT_W + 2 * PAD:
        x = (w - CONTENT_W) // 2
        for box in boxes.values():
            box.x = x
    page = Box(PAGE_X, PAGE_Y, w, h)
    return page, boxes
