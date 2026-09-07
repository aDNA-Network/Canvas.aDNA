"""Slide builders — map each slide type to interior canvas nodes (a lean KEEP subset of CanvasForge's 16 types).

Each builder returns a ``SlideBuild`` (interior nodes in the ``canvas_std`` source-contract shape, their
``_reserved.component_types`` entries, and within-slide ``reading_order`` edge pairs). Geometry is absolute (placed
inside the slide's content rect). Component classes come from the taxonomy in ``canvas_std.reserved.COMPONENT_CLASSES``
and every ``degrades_to`` is a baseline node type (text/file/link/group).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from canvas_core.layout_fit import fit_image_box

from deck_generator.layout import Box, content_rect, est_text_height, heading_height, heading_text


@dataclass
class SlideBuild:
    nodes: list[dict[str, Any]]
    component_types: dict[str, dict[str, Any]]
    edges: list[tuple[str, str]] = field(default_factory=list)  # within-slide reading_order pairs


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


def _title(slide, sid, box) -> SlideBuild:
    c = content_rect(box)
    nodes, comps, edges = [], {}, []
    tid = f"{sid}_title"
    th = heading_height(slide.title, width=c.w, min_h=160)
    ty = c.y + c.h // 3
    nodes.append(_text(tid, heading_text(slide.title), Box(c.x, ty, c.w, th)))
    comps[tid] = _comp("typography_run", "text", semantic="title")
    if slide.subtitle:
        stid = f"{sid}_subtitle"
        nodes.append(_text(stid, slide.subtitle, Box(c.x, ty + th + 24, c.w,
                                                    est_text_height(slide.subtitle, width=c.w, min_h=96))))
        comps[stid] = _comp("text", "text", semantic="subtitle")
        edges.append((tid, stid))
    return SlideBuild(nodes, comps, edges)


def _section(slide, sid, box) -> SlideBuild:
    c = content_rect(box)
    hid = f"{sid}_heading"
    sh = heading_height(slide.title, width=c.w, min_h=160)
    node = _text(hid, heading_text(slide.title), Box(c.x, c.y + c.h // 2 - sh // 2, c.w, sh))
    return SlideBuild([node], {hid: _comp("typography_run", "text", semantic="section")})


def _content(slide, sid, box) -> SlideBuild:
    c = content_rect(box)
    nodes, comps, edges = [], {}, []
    hid = f"{sid}_heading"
    hh = heading_height(slide.title, width=c.w, min_h=90)
    nodes.append(_text(hid, heading_text(slide.title), Box(c.x, c.y, c.w, hh)))
    comps[hid] = _comp("typography_run", "text", semantic="heading")
    prev, y = hid, c.y + hh + 20
    if slide.body:
        bid = f"{sid}_body"
        bh = est_text_height(slide.body, width=c.w)
        nodes.append(_text(bid, slide.body, Box(c.x, y, c.w, bh)))
        comps[bid] = _comp("text", "text")
        edges.append((prev, bid))
        prev, y = bid, y + bh + 24
    if slide.bullets:
        lid = f"{sid}_bullets"
        text = "\n".join(f"- {b}" for b in slide.bullets)
        lh = est_text_height(text, width=c.w)
        nodes.append(_text(lid, text, Box(c.x, y, c.w, lh)))
        comps[lid] = _comp("text", "text", semantic="list")
        edges.append((prev, lid))
    return SlideBuild(nodes, comps, edges)


def _image(slide, sid, box) -> SlideBuild:
    c = content_rect(box)
    nodes, comps, edges = [], {}, []
    hid = f"{sid}_heading"
    hh = heading_height(slide.title, width=c.w, min_h=80)
    nodes.append(_text(hid, heading_text(slide.title), Box(c.x, c.y, c.w, hh)))
    comps[hid] = _comp("typography_run", "text", semantic="heading")
    iid = f"{sid}_image"
    cap_h = est_text_height(slide.caption, width=c.w, min_h=56) if slide.caption else 0
    avail_h = c.h - (hh + 20) - (cap_h + 16 if cap_h else 0)
    # A slide's height is FIXED (16:9 is the format), so an asset taller than the space left must
    # narrow rather than squash — fit both axes and centre (CV-IMAGE-ASPECT-RATIO-01). Falls back to
    # filling the column for a remote or unresolvable image.
    img_w, img_h = fit_image_box(slide.image, c.w, avail_h) or (c.w, avail_h)
    img_box = Box(c.x + (c.w - img_w) // 2, c.y + hh + 20, img_w, img_h)
    if slide.image.startswith(("http://", "https://")):
        nodes.append({"id": iid, "type": "link", "url": slide.image, **img_box.as_node()})
        comps[iid] = _comp("image", "link", semantic="figure", qualities={"substrate": "external"})
    else:
        nodes.append({"id": iid, "type": "file", "file": slide.image, **img_box.as_node()})
        comps[iid] = _comp("image", "file", semantic="figure", qualities={"substrate": "raster"})
    edges.append((hid, iid))
    if slide.caption:
        cid = f"{sid}_caption"
        nodes.append(_text(cid, slide.caption, Box(c.x, c.y + c.h - cap_h, c.w, cap_h)))
        comps[cid] = _comp("caption", "text")
        edges.append((iid, cid))
    return SlideBuild(nodes, comps, edges)


def _table(slide, sid, box) -> SlideBuild:
    c = content_rect(box)
    nodes, comps, edges = [], {}, []
    hid = f"{sid}_heading"
    hh = heading_height(slide.title, width=c.w, min_h=80)
    nodes.append(_text(hid, heading_text(slide.title), Box(c.x, c.y, c.w, hh)))
    comps[hid] = _comp("typography_run", "text", semantic="heading")
    md, n_rows, n_cols = _render_table(slide.table)
    tid = f"{sid}_table"
    th = est_text_height(md, width=c.w, min_h=120)
    nodes.append(_text(tid, md, Box(c.x, c.y + hh + 20, c.w, th)))
    comps[tid] = _comp("table", "text", qualities={"row_count": n_rows, "col_count": n_cols})
    edges.append((hid, tid))
    return SlideBuild(nodes, comps, edges)


def _quote(slide, sid, box) -> SlideBuild:
    c = content_rect(box)
    nodes, comps, edges = [], {}, []
    qid = f"{sid}_quote"
    quoted = f"> {slide.body or slide.title}"
    qh = est_text_height(quoted, width=c.w, min_h=200)
    nodes.append(_text(qid, quoted, Box(c.x, c.y + c.h // 3, c.w, qh)))
    comps[qid] = _comp("text", "text", semantic="quote")
    if slide.attribution:
        aid = f"{sid}_attribution"
        attr = f"— {slide.attribution}"
        nodes.append(_text(aid, attr, Box(c.x, c.y + c.h // 3 + qh + 20, c.w,
                                          est_text_height(attr, width=c.w, min_h=60))))
        comps[aid] = _comp("text", "text", semantic="attribution")
        edges.append((qid, aid))
    return SlideBuild(nodes, comps, edges)


_BUILDERS = {
    "title": _title,
    "section": _section,
    "content": _content,
    "image": _image,
    "table": _table,
    "quote": _quote,
}


def build_slide(slide, sid: str, box: Box) -> SlideBuild:
    return _BUILDERS[slide.type](slide, sid, box)
