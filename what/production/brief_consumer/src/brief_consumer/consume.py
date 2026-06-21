"""The brief consumer: ``BriefInput`` -> a v2.0.0-conformant, aDNA-Native ``.canvas``.

Pipeline:
  1. assemble the ``canvas_std`` **source contract** — a group *page* (the canonical surface) enclosing per-section
     heading (``text``) + body (``text``) + source (``link``) nodes, plus a ``reading_order`` flow chain and
     ``adjacency`` edges from each body to its sources;
  2. ``canvas_std.to_canvas(source)`` — the forward round-trip (sets explicit ``toEnd`` + injects ``_reserved.sync``);
  3. **enrich ``metadata.frontmatter._reserved`` to aDNA-Native** — ``adna_version`` / ``conformance_level`` /
     ``component_types`` / ``semantic_bindings`` / ``panel_link`` (exactly one canonical surface) / ``context_object``.

``canvas_std`` is the only substrate dependency, and it is never mutated (substrate-neutrality / C8).
"""

from __future__ import annotations

from typing import Any

from canvas_std import to_canvas

from brief_consumer import layout
from brief_consumer.model import BriefInput

ADNA_VERSION = "2.0.0"
PAGE_ID = "brief_page"
HEADING_COLOR = "5"  # a valid color slot — visual distinction for headings; degrades cleanly (Core/Extended-valid)


def build_brief(brief: BriefInput) -> dict[str, Any]:
    """Map a ``BriefInput`` to a v2.0.0 aDNA-Native ``.canvas`` document (a plain dict)."""
    blocks: list[tuple[str, int, int]] = []          # (id, height, gap_after) for layout
    payloads: dict[str, dict[str, Any]] = {}         # id -> {type, text|url}
    component_types: dict[str, dict[str, Any]] = {}  # id -> _reserved.component_types entry
    heading_ids: list[str] = []
    reading_chain: list[str] = []                    # ordered ids -> reading_order edges
    ref_pairs: list[tuple[str, str]] = []            # (body_id, source_id) -> adjacency edges

    for i, sec in enumerate(brief.sections):
        head_id, body_id = f"sec{i}_head", f"sec{i}_body"

        payloads[head_id] = {"type": "text", "text": f"## {sec.heading}"}
        component_types[head_id] = {"class": "typography_run", "semantic_type": "heading", "degrades_to": "text"}
        heading_ids.append(head_id)
        reading_chain.append(head_id)
        blocks.append((head_id, layout.HEADING_H, layout.GAP))

        payloads[body_id] = {"type": "text", "text": sec.body}
        component_types[body_id] = {"class": "text", "degrades_to": "text"}
        reading_chain.append(body_id)
        body_gap = layout.GAP if sec.sources else layout.SECTION_GAP
        blocks.append((body_id, layout.body_height(sec.body), body_gap))

        for j, src in enumerate(sec.sources):
            sid = f"sec{i}_src{j}"
            payloads[sid] = {"type": "link", "url": src.url}
            # CANVAS-L-001 carry: baseline link nodes have no anchor-text slot; keep the authored label in the
            # metadata layer so provenance survives the degrade-to-bare-URL (do not force it into the link node).
            component_types[sid] = {"class": "link", "semantic_type": "citation", "degrades_to": "link"}
            if src.label:
                component_types[sid]["qualities"] = {"label": src.label}
            last = j == len(sec.sources) - 1
            blocks.append((sid, layout.SOURCE_H, layout.SECTION_GAP if last else layout.GAP))
            ref_pairs.append((body_id, sid))

    page_box, boxes = layout.stack(blocks)

    # --- source contract (spec_roundtrip_protocol_v2 §; roundtrip.py docstring) ---
    nodes: list[dict[str, Any]] = [
        {"id": PAGE_ID, "type": "group", "label": brief.title,
         "x": page_box.x, "y": page_box.y, "width": page_box.w, "height": page_box.h}
    ]
    for nid, payload in payloads.items():
        b = boxes[nid]
        nodes.append({"id": nid, **payload, "x": b.x, "y": b.y, "width": b.w, "height": b.h})

    edges: list[dict[str, Any]] = []
    panel_link_edges: dict[str, dict[str, str]] = {}
    for k in range(len(reading_chain) - 1):
        eid = f"flow_{k}"
        edges.append({"id": eid, "fromNode": reading_chain[k], "toNode": reading_chain[k + 1],
                      "fromSide": "bottom", "toSide": "top"})
        panel_link_edges[eid] = {"kind": "reading_order"}
    for n, (body_id, sid) in enumerate(ref_pairs):
        eid = f"ref_{n}"
        edges.append({"id": eid, "fromNode": body_id, "toNode": sid, "fromSide": "right", "toSide": "left"})
        panel_link_edges[eid] = {"kind": "adjacency"}

    source = {"name": brief.id, "version": brief.version, "nodes": nodes, "edges": edges}

    # --- forward to a conformant view (sets toEnd + _reserved.sync) ---
    doc = to_canvas(source)

    # subtle, valid styling: headings get a color slot (proven Core/Extended-valid by the degradation tests)
    by_id = {n["id"]: n for n in doc["nodes"]}
    for hid in heading_ids:
        by_id[hid]["color"] = HEADING_COLOR

    # --- enrich _reserved -> aDNA-Native (A-* checks; reserved.py) ---
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    reserved["adna_version"] = ADNA_VERSION
    reserved["conformance_level"] = "adna_native"
    reserved["component_types"] = {
        PAGE_ID: {"class": "panel", "semantic_type": "page", "degrades_to": "group"},
        **component_types,
    }
    reserved["semantic_bindings"] = {"profile": "document"}
    reserved["panel_link"] = {
        "edges": panel_link_edges,
        "regions": {
            PAGE_ID: {"flow": "vertical", "pagination": "paged",
                      "extent": {"unit": "pages", "max": 1}, "surface": "letter"}
        },
        "surfaces": [{"id": PAGE_ID, "role": "canonical"}],
    }
    reserved["context_object"] = {"id": brief.id, "version": brief.version, "refs": list(brief.refs)}
    return doc
