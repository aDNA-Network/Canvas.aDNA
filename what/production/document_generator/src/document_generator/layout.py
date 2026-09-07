"""Deterministic layout + reflow — the producer-side geometry for a long-form document.

Pages are stacked **top-to-bottom** in a single column (a document reads vertically, unlike the deck's left-to-right
row), so the page ``sequence`` chain reads straight down. Each page is a US-Letter group (816x1056 @ 96dpi); the
``doc_root`` group encloses them. All coordinates are **integers** and a pure function of the input (reproducible).

E4.2 adds **reflow / auto-pagination** (closing ``CANVAS-L-002``): a model page whose content exceeds one canvas
page's usable height is split, at **section** granularity, across as many canvas pages as it needs. Measurement and
emission share one source of truth — the ``*_height`` functions here are exactly what ``blocks.py`` advances its
cursor by — so a document that does **not** overflow is laid out byte-identically to E4.1. Interior node placement is
in ``blocks.py``; this module owns geometry, the per-unit heights, and the page-break planner.

This module is substrate-neutral (no ``canvas_std`` import). ⛩ **P2c (2026-09-07):** it now imports
``canvas_core.layout_fit`` — the shared engine-shelf fitter (``adr_004``) — so that node heights are the same number
``CV-TEXT-BOUNDS-01`` computes rather than a parallel guess. The former ``est_text_height(text, wrap=88, line_h=24,
pad=20)`` charged 24px a line and wrapped at a fixed 88 characters; the trap measures the Obsidian flex box, where
paragraph margins do not collapse and a ``##`` lead costs 98.9px before a body character renders. The two models
disagreed on **26 findings per shipped example**, all in the same direction. Measure == emit still holds: the
``*_height`` functions here remain exactly what ``blocks.py`` advances its cursor by.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from canvas_core.layout_fit import (
    fit_group_label,
    fit_group_size,
    fit_image_box,
    fit_text_height,
    heading,
)

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
CONTENT_W = PAGE_W - 2 * PAGE_PAD   # 672 — the width every interior text node is emitted at

# Interior block geometry (shared by measurement here + emission in blocks.py — single source of truth).
# HEAD_H / CAP_H / ATTR_H are now FLOORS, not answers: a heading or caption that wraps is measured
# through `fit_text_height` and grows past them. A fixed height is what let a `## …` heading — 98.9px
# of lead cost — ship in a 48px box (P2c).
HEAD_H = 48
CAP_H = 44
ATTR_H = 40
SRC_H = 40    # a link node renders a bare URL, not measured markdown
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


def page_box(idx: int, doc_w: int = DOC_PAD * 2 + PAGE_W) -> Box:
    """Geometry of the idx-th *emitted* page group (single vertical column).

    ``doc_w`` centres the column when ``doc_root`` was widened to fit its label.
    """
    x = page_column_x(doc_w)
    y = DOC_PAD + LABEL_BAND + idx * (PAGE_H + PAGE_GAP)
    return Box(x, y, PAGE_W, PAGE_H)


def doc_box(n_pages: int, label: str = "") -> Box:
    """Geometry of the enclosing doc_root group (over the *emitted* page count).

    Sized through :func:`canvas_core.layout_fit.fit_group_size` so the page column clears
    ``CV-GROUP-PADDING-01``'s 90% fill ceiling however many pages the document reflows to (it read
    95.27% at four pages), and widened to :func:`fit_group_label`'s minimum so the title does not
    ellipsise — a frame group is free to be wider than its content, and the label is the only thing
    a reader sees when zoomed out.
    """
    pages_h = n_pages * PAGE_H + (n_pages - 1) * PAGE_GAP
    w, ratio_h = fit_group_size(PAGE_W, pages_h, DOC_PAD)
    # The page column starts below the label band, so the container needs that band on top of the
    # ratio-derived height — a fill ceiling and an asymmetric offset are two different constraints.
    h = max(DOC_PAD + LABEL_BAND + pages_h + DOC_PAD, ratio_h)
    if label:
        _, min_w = fit_group_label(label, w)
        w = max(w, min_w)
    return Box(0, 0, w, h)


def page_column_x(doc_w: int) -> int:
    """Left edge of the page column, centred inside a doc_root that may be wider than a page."""
    return max(DOC_PAD, (doc_w - PAGE_W) // 2)


def content_rect(box: Box) -> Box:
    """The inner content area of a page (inside PAGE_PAD)."""
    return Box(box.x + PAGE_PAD, box.y + PAGE_PAD, box.w - 2 * PAGE_PAD, box.h - 2 * PAGE_PAD)


def est_text_height(text: str, *, width: int = CONTENT_W, min_h: int = 44) -> int:
    """Deterministic text-node height — the height ``CV-TEXT-BOUNDS-01`` will require.

    ⛩ P2c: was a character-count estimate (``wrap=88``, ``line_h=24``, ``pad=20``). Those keywords
    are gone rather than deprecated — they described a model nothing else in the vault used, and
    callers passing ``wrap=200`` for a table were tuning a guess against a measurement they could
    have made. Delegates to :func:`canvas_core.layout_fit.fit_text_height`.
    """
    return fit_text_height(text, width, min_height=min_h)


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

def heading_text(head: str) -> str:
    """The emitted form of a section heading — ``#### <head>``.

    Was ``## <head>``, which cost 98.9px of non-collapsing lead margin inside a 48px node: the
    single largest contributor to this producer's overflow findings, and 10 ``CV-LEAD-COST-01``
    findings in its own right. ``####`` costs 42.6px and remains a real markdown heading, so
    ``CV-HIERARCHY-01``'s title slot still sees it (F-P2-3/F-P2-9).
    """
    return heading(head)


def heading_height(head: str = "") -> int:
    """Height a section heading consumes, incl. its trailing gap. ``HEAD_H`` is a floor."""
    if not head:
        return HEAD_H + GAP
    return est_text_height(heading_text(head), min_h=HEAD_H) + GAP


def figure_height(image: str) -> int:
    """Height a figure node needs to preserve its asset's aspect at ``CONTENT_W``.

    ``FIG_H`` is the fallback for a remote or unresolvable image. A fixed height distorts any
    asset whose aspect differs — CV-IMAGE-ASPECT-RATIO-01, which could not fire at all while the
    example PNGs were missing (P2c).
    """
    box = fit_image_box(image, CONTENT_W, CONTENT_H)
    return box[1] if box else FIG_H


def figure_width(image: str) -> int:
    """Width a figure node takes — narrower than the column when the page height binds."""
    box = fit_image_box(image, CONTENT_W, CONTENT_H)
    return box[0] if box else CONTENT_W


def caption_height(caption: str) -> int:
    return est_text_height(caption, min_h=CAP_H)


def attribution_height(attribution: str) -> int:
    return est_text_height(f"— {attribution}", min_h=ATTR_H)


def body_height(body: str) -> int:
    return est_text_height(body) + GAP if body else 0


def source_height() -> int:
    return SRC_H + GAP


def section_trailing_gap() -> int:
    return SECTION_GAP - GAP


def block_height(blk: Block) -> int:
    """Total vertical space (incl. trailing GAP) one block consumes — mirrors ``blocks._emit_block`` exactly."""
    if blk.type == "figure":
        h = figure_height(blk.image) + GAP
        if blk.caption:
            h += caption_height(blk.caption) + GAP
        return h
    if blk.type == "table":
        md, _rows, _cols = render_table(blk.table)
        return est_text_height(md, min_h=100) + GAP
    if blk.type == "code":
        return est_text_height(code_text(blk), min_h=80) + GAP
    if blk.type == "quote":
        h = est_text_height(f"> {blk.text}", min_h=72) + GAP
        if blk.attribution:
            h += attribution_height(blk.attribution) + GAP
        return h
    if blk.type == "list":
        text = "\n".join(f"- {it}" for it in blk.items)
        return est_text_height(text, min_h=56) + GAP
    raise ValueError(f"unknown block type {blk.type!r}")


def code_text(blk: Block) -> str:
    """The emitted form of a code block — the fenced text, which is what renders and is measured."""
    return f"```{blk.lang}\n{blk.code}\n```" if blk.lang else f"```\n{blk.code}\n```"


def section_height(sec: Section) -> int:
    """Total height one section consumes when laid out (heading + body + blocks + sources + trailing gap)."""
    h = heading_height(sec.heading) + body_height(sec.body)
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
