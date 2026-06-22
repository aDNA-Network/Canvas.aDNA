"""Deterministic layout — the producer-side print geometry for a comic, as INTEGER canvas boxes.

Print-spec constants are PORTED from the CanvasForge quarry (ComixWellspring standard; the quarry used 1" = 100
canvas units, floats). Here they become **integers** (canvas_std C-2 requires integer x/y/width/height) and pages
stack **top-to-bottom** in a single column (a comic reads page-by-page downward, like the document_generator), so the
page ``sequence`` chain reads straight down. The ``comic_root`` group encloses everything (the single canonical
surface); each spread is a group enclosing its page(s); each page is a group carrying a 2D panel grid.

All coordinates are integers and a pure function of the input (reproducible). Geometry is not scored here — it only
needs to be deterministic and roughly non-overlapping. This module is substrate-neutral (no ``canvas_std`` import); it
imports only the producer-side domain model.

Source (KEEP-reference, NOT a dependency): ``Archive.aDNA/CanvasForge.aDNA/what/code/canvas_comic/comic.py``
(``TRIM_*``/``SAFE_*``/``BLEED_*``/``PANEL_GUTTER`` + ``_grid_to_coords``).
"""

from __future__ import annotations

from dataclasses import dataclass

from comic_generator.model import Page

# Print-spec page geometry (ported from the quarry, rounded to integers; ComixWellspring trim/safe/bleed).
TRIM_W = 663
TRIM_H = 1025
SAFE_W = 638
SAFE_H = 1000
SAFE_ORIGIN_X = 25
SAFE_ORIGIN_Y = 13
PANEL_GUTTER = 10
BLEED_W = 688
BLEED_H = 1050

# Standard interior grid (2 columns × 3 rows) within the safe area — the quarry's default page grid.
GRID_COLS = 2
GRID_ROWS = 3

# Enclosure geometry.
COMIC_PAD = 80       # padding inside comic_root, around the spread column
SPREAD_PAD = 40      # padding inside a spread group, around its page(s)
SPREAD_LABEL_BAND = 56
PAGE_GAP = 96        # vertical gutter between spreads
SPREAD_PAGE_GAP = 48  # horizontal gutter between the two pages of a spread


@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int

    def as_node(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "width": self.w, "height": self.h}


def _col_row_size() -> tuple[int, int]:
    """The (col_width, row_height) of one standard grid cell within the safe area (integers)."""
    col_w = (SAFE_W - (GRID_COLS - 1) * PANEL_GUTTER) // GRID_COLS
    row_h = (SAFE_H - (GRID_ROWS - 1) * PANEL_GUTTER) // GRID_ROWS
    return col_w, row_h


def panel_box_in_page(row: int, col: int, span_rows: int, span_cols: int, layout_type: str) -> Box:
    """Geometry of one panel WITHIN its page's local coordinate space (origin at the page's top-left).

    A splash page or a full-bleed multi-cell panel fills the page; otherwise the panel occupies its grid cells within
    the safe area. Ported from the quarry's ``_grid_to_coords`` (integerized).
    """
    if layout_type == "splash" or (span_rows >= GRID_ROWS and span_cols >= GRID_COLS):
        return Box(0, 0, TRIM_W, TRIM_H)
    col_w, row_h = _col_row_size()
    x = SAFE_ORIGIN_X + col * (col_w + PANEL_GUTTER)
    y = SAFE_ORIGIN_Y + row * (row_h + PANEL_GUTTER)
    w = col_w * span_cols + PANEL_GUTTER * (span_cols - 1)
    h = row_h * span_rows + PANEL_GUTTER * (span_rows - 1)
    return Box(x, y, w, h)


def page_box_in_spread(page_index_in_spread: int) -> Box:
    """Geometry of a page group WITHIN its spread's local coordinate space (origin at the spread's top-left)."""
    x = SPREAD_PAD + page_index_in_spread * (TRIM_W + SPREAD_PAGE_GAP)
    y = SPREAD_PAD + SPREAD_LABEL_BAND
    return Box(x, y, TRIM_W, TRIM_H)


def spread_box(spread_index: int, n_pages_in_spread: int) -> Box:
    """Geometry of a spread group (top-to-bottom column inside comic_root)."""
    w = SPREAD_PAD * 2 + n_pages_in_spread * TRIM_W + (n_pages_in_spread - 1) * SPREAD_PAGE_GAP
    h = SPREAD_PAD * 2 + SPREAD_LABEL_BAND + TRIM_H
    x = COMIC_PAD
    y = COMIC_PAD + spread_index * (h + PAGE_GAP)
    return Box(x, y, w, h)


def comic_box(spread_boxes: list[Box]) -> Box:
    """Geometry of the enclosing comic_root group over all spread boxes."""
    if not spread_boxes:
        return Box(0, 0, COMIC_PAD * 2 + TRIM_W, COMIC_PAD * 2 + TRIM_H)
    max_right = max(b.x + b.w for b in spread_boxes)
    max_bottom = max(b.y + b.h for b in spread_boxes)
    return Box(0, 0, max_right + COMIC_PAD, max_bottom + COMIC_PAD)


def absolute(inner: Box, *parents: Box) -> Box:
    """Translate a Box given in a parent's local space into absolute canvas coordinates by summing parent origins."""
    ox = sum(p.x for p in parents)
    oy = sum(p.y for p in parents)
    return Box(inner.x + ox, inner.y + oy, inner.w, inner.h)


def assign_spreads(pages: tuple[Page, ...]) -> list[list[Page]]:
    """Group pages into spreads by their ``spread_number`` (declaration order preserved).

    Pages sharing a ``spread_number`` land in one spread group (in page order); a page with no ``spread_number`` is its
    own singleton spread. Deterministic: spreads are emitted in first-appearance order of their pages.
    """
    groups: list[list[Page]] = []
    by_spread: dict[int, list[Page]] = {}
    order: list[object] = []  # spread_number (int) or a unique singleton marker, in first-appearance order
    singleton_seq = 0
    for pg in pages:
        if pg.spread_number is None:
            groups.append([pg])
            order.append(("__singleton__", singleton_seq))
            singleton_seq += 1
        else:
            if pg.spread_number not in by_spread:
                by_spread[pg.spread_number] = []
                order.append(pg.spread_number)
            by_spread[pg.spread_number].append(pg)

    # Re-emit in first-appearance order, interleaving singletons and grouped spreads.
    result: list[list[Page]] = []
    singleton_iter = iter(groups)
    for key in order:
        if isinstance(key, tuple):  # singleton marker
            result.append(next(singleton_iter))
        else:
            result.append(by_spread[key])
    return result
