"""Page builders — lay a page's sections + blocks out vertically into canvas nodes.

``build_page`` walks a page's sections top-to-bottom, emitting interior nodes (in the ``canvas_std`` source-contract
shape), their ``_reserved.component_types`` entries, a single ``reading_order`` chain through the page, and
``adjacency`` links from each section's prose to its citations. Component classes come from the taxonomy in
``canvas_std.reserved.COMPONENT_CLASSES`` and every ``degrades_to`` is a baseline node type (text/file/link/group).

This is the producer-side rendering of the long-form element set: heading, body, figure (+caption), table, code,
quote (+attribution), list, citation. The ``code`` class is exercised here for the first time across the consumers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from document_generator.layout import Box, content_rect, est_text_height

HEAD_H = 48
CAP_H = 44
ATTR_H = 40
SRC_H = 40
FIG_H = 320
GAP = 20
SECTION_GAP = 44


@dataclass
class PageBuild:
    nodes: list[dict[str, Any]]
    component_types: dict[str, dict[str, Any]]
    reading: list[str] = field(default_factory=list)               # ordered ids -> reading_order chain
    adjacency: list[tuple[str, str]] = field(default_factory=list)  # (prose_id, citation_id) -> adjacency
    headings: list[str] = field(default_factory=list)              # heading node ids (for styling)


def _text(nid: str, text: str, box: Box) -> dict[str, Any]:
    return {"id": nid, "type": "text", "text": text, **box.as_node()}


def _comp(cls: str, degrades: str, *, semantic: str | None = None,
          qualities: dict[str, Any] | None = None) -> dict[str, Any]:
    entry: dict[str, Any] = {"class": cls, "degrades_to": degrades}
    if semantic:
        entry["semantic_type"] = semantic
    if qualities:
        entry["qualities"] = qualities
    return entry


def _render_table(table: Any) -> tuple[str, int, int]:
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


def _emit_block(pb: PageBuild, blk, bid: str, c: Box, y: int) -> int:
    """Emit one block's node(s) at vertical cursor ``y``; return the new cursor."""
    if blk.type == "figure":
        fbox = Box(c.x, y, c.w, FIG_H)
        if blk.image.startswith(("http://", "https://")):
            pb.nodes.append({"id": bid, "type": "link", "url": blk.image, **fbox.as_node()})
            pb.component_types[bid] = _comp("image", "link", semantic="figure", qualities={"substrate": "external"})
        else:
            pb.nodes.append({"id": bid, "type": "file", "file": blk.image, **fbox.as_node()})
            pb.component_types[bid] = _comp("image", "file", semantic="figure", qualities={"substrate": "raster"})
        pb.reading.append(bid)
        y += FIG_H + GAP
        if blk.caption:
            cid = f"{bid}_cap"
            pb.nodes.append(_text(cid, blk.caption, Box(c.x, y, c.w, CAP_H)))
            pb.component_types[cid] = _comp("caption", "text")
            pb.reading.append(cid)
            y += CAP_H + GAP
        return y
    if blk.type == "table":
        md, n_rows, n_cols = _render_table(blk.table)
        th = est_text_height(md, wrap=200, line_h=26, pad=24, min_h=100)
        pb.nodes.append(_text(bid, md, Box(c.x, y, c.w, th)))
        pb.component_types[bid] = _comp("table", "text", qualities={"row_count": n_rows, "col_count": n_cols})
        pb.reading.append(bid)
        return y + th + GAP
    if blk.type == "code":
        fenced = f"```{blk.lang}\n{blk.code}\n```" if blk.lang else f"```\n{blk.code}\n```"
        ch = est_text_height(blk.code, wrap=100, line_h=22, pad=28, min_h=80)
        pb.nodes.append(_text(bid, fenced, Box(c.x, y, c.w, ch)))
        pb.component_types[bid] = _comp("code", "text", qualities={"lang": blk.lang} if blk.lang else None)
        pb.reading.append(bid)
        return y + ch + GAP
    if blk.type == "quote":
        qh = est_text_height(blk.text, min_h=72)
        pb.nodes.append(_text(bid, f"> {blk.text}", Box(c.x, y, c.w, qh)))
        pb.component_types[bid] = _comp("text", "text", semantic="quote")
        pb.reading.append(bid)
        y += qh + GAP
        if blk.attribution:
            aid = f"{bid}_attr"
            pb.nodes.append(_text(aid, f"— {blk.attribution}", Box(c.x, y, c.w, ATTR_H)))
            pb.component_types[aid] = _comp("text", "text", semantic="attribution")
            pb.reading.append(aid)
            y += ATTR_H + GAP
        return y
    if blk.type == "list":
        text = "\n".join(f"- {it}" for it in blk.items)
        lh = est_text_height(text, min_h=56)
        pb.nodes.append(_text(bid, text, Box(c.x, y, c.w, lh)))
        pb.component_types[bid] = _comp("text", "text", semantic="list")
        pb.reading.append(bid)
        return y + lh + GAP
    raise ValueError(f"unknown block type {blk.type!r}")


def build_page(page, pid: str, box: Box) -> PageBuild:
    """Lay a page's sections out vertically; return interior nodes + component_types + reading/adjacency edges."""
    c = content_rect(box)
    pb = PageBuild(nodes=[], component_types={})
    y = c.y
    for si, sec in enumerate(page.sections):
        hid = f"{pid}_s{si}_head"
        pb.nodes.append(_text(hid, f"## {sec.heading}", Box(c.x, y, c.w, HEAD_H)))
        pb.component_types[hid] = _comp("typography_run", "text", semantic="heading")
        pb.reading.append(hid)
        pb.headings.append(hid)
        y += HEAD_H + GAP
        anchor = hid  # adjacency origin for citations (the body if present, else the heading)

        if sec.body:
            bid = f"{pid}_s{si}_body"
            bh = est_text_height(sec.body)
            pb.nodes.append(_text(bid, sec.body, Box(c.x, y, c.w, bh)))
            pb.component_types[bid] = _comp("text", "text")
            pb.reading.append(bid)
            y += bh + GAP
            anchor = bid

        for bi, blk in enumerate(sec.blocks):
            y = _emit_block(pb, blk, f"{pid}_s{si}_b{bi}", Box(c.x, y, c.w, 0), y)

        for ci, src in enumerate(sec.sources):
            sid = f"{pid}_s{si}_src{ci}"
            pb.nodes.append({"id": sid, "type": "link", "url": src.url, **Box(c.x, y, c.w, SRC_H).as_node()})
            pb.component_types[sid] = _comp("link", "link", semantic="citation")
            pb.adjacency.append((anchor, sid))
            y += SRC_H + GAP

        y += SECTION_GAP - GAP
    return pb
