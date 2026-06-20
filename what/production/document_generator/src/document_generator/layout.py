"""Deterministic layout + reflow — the producer-side geometry for a long-form document.

Pages are stacked **top-to-bottom** in a single column (a document reads vertically, unlike the deck's left-to-right
row), so the page ``sequence`` chain reads straight down. Each page is a US-Letter group (816x1056 @ 96dpi); the
``doc_root`` group encloses them. All coordinates are **integers** and a pure function of the input (reproducible).

E4.2 adds **reflow / auto-pagination** (closing ``CANVAS-L-002``): a model page whose content exceeds one canvas
page's usable height is split, at **section** granularity, across as many canvas pages as it needs. Measurement and
emission share one source of truth — the ``*_height`` functions here are exactly what ``blocks.py`` advances its
cursor by — so a document that does **not** overflow is laid out byte-identically to E4.1. Interior node placement is
in ``blocks.py``; this module owns geometry, the per-unit heights, and the page-break planner.

This module is substrate-neutral (no ``canvas_std`` import); it imports only the producer-side domain model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from document_generator.model import Block, Page, Section

# Page geometry (US Letter @ 96dpi), integer points.
PAGE_W = 816
PAGE_H = 1056
PAGE_GAP = 96       # vertical gutter between pages
DOC_PAD = 80        # padding around the page column inside doc_root
LABEL_BAND = 64     # room under the doc_root label, above the first page
PAGE_PAD = 72       # inner page margin (~0.75in)

# Usable content height inside one page (between the top + bottom margins). A page's laid-out content must fit here;
# reflow (paginate) breaks a model page that would exceed it. (E1.5/E4.1 had no such bound — the CANVAS-L-002 defect.)
CONTENT_H = PAGE_H - 2 * PAGE_PAD   # 912

# Interior block geometry (shared by measurement here + emission in blocks.py — single source of truth).
HEAD_H = 48
CAP_H = 44
ATTR_H = 40
SRC_H = 40
FIG_H = 320
GAP = 20
SECTION_GAP = 44


@dataclass
class Box:
    x: int
    y: int
    w: int
    h: int

    def as_node(self) -> dict[str, int]:
        return {"x": self.x, "y": self.y, "width": self.w, "height": self.h}


def page_box(idx: int) -> Box:
    """Geometry of the idx-th *emitted* page group (single vertical column)."""
    x = DOC_PAD
    y = DOC_PAD + LABEL_BAND + idx * (PAGE_H + PAGE_GAP)
    return Box(x, y, PAGE_W, PAGE_H)


def doc_box(n_pages: int) -> Box:
    """Geometry of the enclosing doc_root group (over the *emitted* page count)."""
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


def render_table(table: Any) -> tuple[str, int, int]:
    """Return (markdown, row_count, col_count) for a markdown string or a {headers, rows} dict."""
    if isinstance(table, str):
        lines = [ln for ln in table.strip().splitlines() if ln.strip()]
        seps = [ln for ln in lines if set(ln) <= set("|-: ")]
        data_rows = max(0, len(lines) - len(seps) - 1)  # minus header
        cols = max(0, lines[0].count("|") - 1) if lines else 0
        return table.strip(), data_rows, cols
    if isinstance(table, dict):
        headers = [str(h) for h in table.get("headers", [])]
        rows = [[str(c) for c in r] for r in table.get("rows", [])]
        head = "| " + " | ".join(headers) + " |"
        sep = "| " + " | ".join("---" for _ in headers) + " |"
        body = "\n".join("| " + " | ".join(r) + " |" for r in rows)
        md = "\n".join([head, sep, body]) if body else "\n".join([head, sep])
        return md, len(rows), len(headers)
    raise ValueError("table must be a markdown string or a {headers, rows} object")


# --- Per-unit heights (MUST equal what blocks.py advances its cursor by; measure == emit) -------------------

def heading_height() -> int:
    return HEAD_H + GAP


def body_height(body: str) -> int:
    return est_text_height(body) + GAP if body else 0


def source_height() -> int:
    return SRC_H + GAP


def section_trailing_gap() -> int:
    return SECTION_GAP - GAP


def block_height(blk: Block) -> int:
    """Total vertical space (incl. trailing GAP) one block consumes — mirrors ``blocks._emit_block`` exactly."""
    if blk.type == "figure":
        h = FIG_H + GAP
        if blk.caption:
            h += CAP_H + GAP
        return h
    if blk.type == "table":
        md, _rows, _cols = render_table(blk.table)
        return est_text_height(md, wrap=200, line_h=26, pad=24, min_h=100) + GAP
    if blk.type == "code":
        return est_text_height(blk.code, wrap=100, line_h=22, pad=28, min_h=80) + GAP
    if blk.type == "quote":
        h = est_text_height(blk.text, min_h=72) + GAP
        if blk.attribution:
            h += ATTR_H + GAP
        return h
    if blk.type == "list":
        text = "\n".join(f"- {it}" for it in blk.items)
        return est_text_height(text, min_h=56) + GAP
    raise ValueError(f"unknown block type {blk.type!r}")


def section_height(sec: Section) -> int:
    """Total height one section consumes when laid out (heading + body + blocks + sources + trailing gap)."""
    h = heading_height() + body_height(sec.body)
    for blk in sec.blocks:
        h += block_height(blk)
    h += source_height() * len(sec.sources)
    h += section_trailing_gap()
    return h


# --- Reflow / auto-pagination (section-level; CANVAS-L-002) -------------------------------------------------

@dataclass
class SectionFragment:
    """One whole section assigned to one canvas page. ``oversized`` flags a section taller than a page (own page,
    intentional overflow + a diagnostic — the documented CANVAS-L-002 residual; intra-section pagination is PT-P5)."""

    section: Section
    oversized: bool = False


@dataclass
class PageFragment:
    """The sections (in order) that land on one canvas page."""

    fragments: list[SectionFragment] = field(default_factory=list)


def paginate(page: Page) -> list[PageFragment]:
    """Distribute a model page's sections across one-or-more canvas pages (a model page never *merges* with the next).

    Greedy, section-atomic, deterministic (integer heights): a section that does not fit in the remaining page space
    starts a new page; a section taller than a whole page gets its own page (``oversized=True``) and is allowed to
    overflow. Returns ≥1 fragment for any non-empty model page; a non-overflowing page yields exactly one fragment
    carrying all its sections in order (so E4.2 output is byte-identical to E4.1 when nothing overflows).
    """
    pages: list[PageFragment] = []
    cur: list[SectionFragment] = []
    used = 0
    for sec in page.sections:
        h = section_height(sec)
        if h > CONTENT_H:
            if cur:
                pages.append(PageFragment(cur))
                cur, used = [], 0
            pages.append(PageFragment([SectionFragment(sec, oversized=True)]))
            continue
        if cur and used + h > CONTENT_H:
            pages.append(PageFragment(cur))
            cur, used = [], 0
        cur.append(SectionFragment(sec))
        used += h
    if cur:
        pages.append(PageFragment(cur))
    return pages
