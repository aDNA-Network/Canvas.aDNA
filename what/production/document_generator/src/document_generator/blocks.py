"""Page builders — lay a page fragment's sections + blocks out vertically into canvas nodes.

``build_page`` walks the sections assigned to one canvas page (a ``layout.PageFragment``) top-to-bottom, emitting
interior nodes (in the ``canvas_std`` source-contract shape), their ``_reserved.component_types`` entries, a single
``reading_order`` chain through the page, and ``adjacency`` links from each section's prose to its citations. Component
classes come from the taxonomy in ``canvas_std.reserved.COMPONENT_CLASSES`` and every ``degrades_to`` is a baseline
node type (text/file/link/group).

The long-form element set: heading, body, figure (+caption), table, code, quote (+attribution), list, citation. E4.2
layers the per-asset **visual contract** (V1–V8) onto figure/caption ``qualities`` (the genre default, or a per-block
override) and marks an ``oversized`` section's heading with a layout diagnostic — both **additive**: with no genre the
output is byte-identical to E4.1. Geometry constants + the page-break planner live in ``layout.py`` (measure == emit).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from document_generator.layout import (
    ATTR_H,
    CAP_H,
    FIG_H,
    GAP,
    HEAD_H,
    SECTION_GAP,
    SRC_H,
    Box,
    PageFragment,
    content_rect,
    est_text_height,
    render_table,
)
from document_generator.model import AssetVisual


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


def _asset_quals(av: AssetVisual) -> dict[str, Any]:
    """The non-default per-asset visual-contract fields (V2–V8), as a figure ``qualities`` patch.

    Records intent only — nothing here renders (PT-P5). ``substrate`` (V1) is emitted from the node's own image type
    (raster/external), not from the contract, so it is excluded here; an all-default asset yields ``{}`` (E4.1-identical).
    """
    q: dict[str, Any] = {}
    if av.producer_tool:
        q["producer_tool"] = av.producer_tool          # V2
    if av.engine_route:
        q["engine_route"] = av.engine_route            # V3 (recorded, not invoked)
    if av.origin and av.origin != "generated":
        q["origin"] = av.origin                        # V4
    if av.scorecard:
        q["scorecard"] = {"criteria": list(av.scorecard), "n": len(av.scorecard)}  # V5 (shape only)
    if av.target_page_fraction:
        q["target_page_fraction"] = av.target_page_fraction  # V7
    if av.intent_class:
        q["intent_class"] = av.intent_class            # V8
    return q


def _emit_block(pb: PageBuild, blk, bid: str, c: Box, y: int, default_asset: AssetVisual) -> int:
    """Emit one block's node(s) at vertical cursor ``y``; return the new cursor."""
    if blk.type == "figure":
        av = blk.asset or default_asset                # per-figure override, else the genre default
        fbox = Box(c.x, y, c.w, FIG_H)
        if blk.image.startswith(("http://", "https://")):
            pb.nodes.append({"id": bid, "type": "link", "url": blk.image, **fbox.as_node()})
            quals = {"substrate": "external", **_asset_quals(av)}
            pb.component_types[bid] = _comp("image", "link", semantic="figure", qualities=quals)
        else:
            pb.nodes.append({"id": bid, "type": "file", "file": blk.image, **fbox.as_node()})
            quals = {"substrate": "raster", **_asset_quals(av)}
            pb.component_types[bid] = _comp("image", "file", semantic="figure", qualities=quals)
        pb.reading.append(bid)
        y += FIG_H + GAP
        if blk.caption:
            cid = f"{bid}_cap"
            pb.nodes.append(_text(cid, blk.caption, Box(c.x, y, c.w, CAP_H)))
            cap_q = {"caption_form": av.caption_form} if av.caption_form != "descriptive" else None  # V6
            pb.component_types[cid] = _comp("caption", "text", qualities=cap_q)
            pb.reading.append(cid)
            y += CAP_H + GAP
        return y
    if blk.type == "table":
        md, n_rows, n_cols = render_table(blk.table)
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


def build_page(fragment: PageFragment, pid: str, box: Box, default_asset: AssetVisual) -> PageBuild:
    """Lay one canvas page's sections out vertically; return interior nodes + component_types + reading/adjacency.

    ``fragment`` is the set of (whole) sections reflow assigned to this page. Node ids are ``{pid}_s{li}_…`` where
    ``li`` is the section's index *within this page* — so a non-overflowing document (one fragment per model page)
    reproduces the E4.1 id scheme + geometry exactly.
    """
    c = content_rect(box)
    pb = PageBuild(nodes=[], component_types={})
    y = c.y
    for li, sf in enumerate(fragment.fragments):
        sec = sf.section
        hid = f"{pid}_s{li}_head"
        head_q = {"layout_note": "oversized_overflow"} if sf.oversized else None  # CANVAS-L-002 residual, traced not silent
        pb.nodes.append(_text(hid, f"## {sec.heading}", Box(c.x, y, c.w, HEAD_H)))
        pb.component_types[hid] = _comp("typography_run", "text", semantic="heading", qualities=head_q)
        pb.reading.append(hid)
        pb.headings.append(hid)
        y += HEAD_H + GAP
        anchor = hid  # adjacency origin for citations (the body if present, else the heading)

        if sec.body:
            bid = f"{pid}_s{li}_body"
            bh = est_text_height(sec.body)
            pb.nodes.append(_text(bid, sec.body, Box(c.x, y, c.w, bh)))
            pb.component_types[bid] = _comp("text", "text")
            pb.reading.append(bid)
            y += bh + GAP
            anchor = bid

        for bi, blk in enumerate(sec.blocks):
            y = _emit_block(pb, blk, f"{pid}_s{li}_b{bi}", Box(c.x, y, c.w, 0), y, default_asset)

        for ci, src in enumerate(sec.sources):
            sid = f"{pid}_s{li}_src{ci}"
            pb.nodes.append({"id": sid, "type": "link", "url": src.url, **Box(c.x, y, c.w, SRC_H).as_node()})
            pb.component_types[sid] = _comp("link", "link", semantic="citation")
            pb.adjacency.append((anchor, sid))
            y += SRC_H + GAP

        y += SECTION_GAP - GAP
    return pb
