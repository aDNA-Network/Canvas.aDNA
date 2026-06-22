"""The comic generator: ``ComicInput`` -> a v2.0.0-conformant, aDNA-Native multi-page ``.canvas``.

Structurally the ``document_generator`` (multi-page) with a 2D panel-grid interior. The canvas model:

  * ``comic_root`` — one ``group`` node = the single canonical surface (``class: panel``, ``semantic_type: comic``);
  * one ``group`` per **spread** (``semantic_type: spread``) carrying a ``region`` (``flow: horizontal``,
    ``pagination: paged``, ``extent: {unit: pages, max: 2}``) — a spread holds its 1–2 pages side by side;
  * one ``group`` per **page** (``semantic_type: page``) carrying a ``region`` (``extent: {unit: pages, max: 1}``);
  * one baseline node per **panel** inside its page (``class: image`` — a ``file`` if rendered, else a ``text``
    placeholder; the assembled 6-layer image PROMPT rides in ``component_types[*].qualities.image_prompt``).

Edges (respecting the A-5 acyclicity check — only ``sequence`` is checked):
  * ``sequence`` over the pages in reading order (a linear, acyclic chain; ``isStartNode`` on page 0 post-to_canvas);
  * ``reading_order`` within a page (the panel Z-path — the grid read top-to-bottom, left-to-right);
  * ``adjacency`` for gutter-neighbour panels (spatial neighbours without order).

Pipeline (mirrors ``document_generator.consume`` / ``diagram_generator.consume``):
  1. group pages into spreads + lay out integer geometry (``layout``);
  2. assemble the ``canvas_std`` **source contract** — ``{name, version, nodes, edges}``;
  3. ``canvas_std.to_canvas`` (sets explicit ``toEnd`` + ``_reserved.sync``), then ``isStartNode`` on page 0;
  4. **enrich ``_reserved`` to aDNA-Native** — component_types / semantic_bindings (the bare ``comic`` profile) /
     panel_link (regions + edge kinds + exactly one canonical surface) / context_object.

``canvas_std`` is the only substrate dependency and is never mutated (substrate-neutrality / ADR-004 two-shelf
firewall). NEVER renders pixels — the panel image directives are PROMPTS in ``_reserved`` metadata only.
"""

from __future__ import annotations

from typing import Any

from canvas_std import to_canvas

from comic_generator import layout, panels
from comic_generator.model import ComicInput

ADNA_VERSION = "2.0.0"
COMIC_ID = "comic_root"


def _reading_path(panel_ids: list[str], page: Any) -> list[str]:
    """Panel ids in reading order (the page Z-path): top-to-bottom by grid row, then left-to-right by column.

    ``page.panels`` is parallel to ``panel_ids``; sort indices by (row, col) for a stable Z-path. Ties (same cell)
    keep declaration order (Python's sort is stable)."""
    order = sorted(range(len(panel_ids)), key=lambda i: (page.panels[i].row, page.panels[i].col))
    return [panel_ids[i] for i in order]


def _adjacency_pairs(panel_ids: list[str], page: Any) -> list[tuple[str, str]]:
    """Gutter-neighbour panel pairs (spatial adjacency, unordered): same-row horizontal neighbours +
    same-column vertical neighbours, by grid coordinates. Deterministic; each pair emitted once."""
    by_cell: dict[tuple[int, int], str] = {}
    for nid, panel in zip(panel_ids, page.panels):
        by_cell.setdefault((panel.row, panel.col), nid)  # first panel wins a cell (stable)
    pairs: list[tuple[str, str]] = []
    for (row, col), nid in by_cell.items():
        right = by_cell.get((row, col + 1))
        if right:
            pairs.append((nid, right))
        down = by_cell.get((row + 1, col))
        if down:
            pairs.append((nid, down))
    return pairs


def build_comic(comic: ComicInput) -> dict[str, Any]:
    """Map a ``ComicInput`` to a v2.0.0 aDNA-Native multi-page ``.canvas`` document (a plain dict)."""
    bible = comic.character_bible()
    spreads = layout.assign_spreads(comic.pages)

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    component_types: dict[str, dict[str, Any]] = {}
    panel_link_edges: dict[str, dict[str, str]] = {}
    regions: dict[str, dict[str, Any]] = {}

    # --- comic_root (the single canonical surface) ---------------------------------------------------------
    spread_boxes = [layout.spread_box(si, len(pages)) for si, pages in enumerate(spreads)]
    cbox = layout.comic_box(spread_boxes)
    nodes.append({"id": COMIC_ID, "type": "group", "label": comic.title, **cbox.as_node()})
    component_types[COMIC_ID] = {"class": "panel", "semantic_type": "comic", "degrades_to": "group"}
    regions[COMIC_ID] = {
        "flow": "vertical",
        "pagination": "paged",
        "extent": {"unit": "pages", "max": comic.page_count()},
        "surface": "comic_page",
    }

    page_ids: list[str] = []  # in reading order, for the sequence chain
    for si, pages in enumerate(spreads):
        sbox = spread_boxes[si]
        sid = f"spread{si}"
        nodes.append({"id": sid, "type": "group", "label": f"Spread {si + 1}", **sbox.as_node()})
        component_types[sid] = {"class": "panel", "semantic_type": "spread", "degrades_to": "group"}
        regions[sid] = {
            "flow": "horizontal",
            "pagination": "paged",
            "extent": {"unit": "pages", "max": 2},
            "surface": "comic_page",
        }

        for pi, page in enumerate(pages):
            pid = f"spread{si}_page{pi}"
            pbox_local = layout.page_box_in_spread(pi)
            pbox_abs = layout.Box(pbox_local.x + sbox.x, pbox_local.y + sbox.y, pbox_local.w, pbox_local.h)
            nodes.append({"id": pid, "type": "group", "label": f"Page {page.number}", **pbox_abs.as_node()})
            component_types[pid] = {"class": "panel", "semantic_type": "page", "degrades_to": "group"}
            regions[pid] = {
                "flow": "columns",
                "pagination": "paged",
                "extent": {"unit": "pages", "max": 1},
                "surface": "comic_page",
            }
            page_ids.append(pid)

            # Panel boxes in page-local space, then build interior nodes + image component entries.
            panel_boxes = [
                layout.panel_box_in_page(p.row, p.col, p.span_rows, p.span_cols, page.layout_type)
                for p in page.panels
            ]
            build = panels.build_panels(
                page,
                pid,
                pbox_abs,
                panel_boxes,
                character_bible=bible,
                color_script=comic.color_script_for(page.spread_number),
                story_state=comic.story_state_for(page.spread_number),
                comic_default_style=comic.art_style,
            )
            nodes.extend(build.nodes)
            component_types.update(build.component_types)

            # reading_order within the page (the panel Z-path)
            read = _reading_path(build.panel_ids, page)
            for k in range(len(read) - 1):
                eid = f"{pid}_ro_{k}"
                edges.append({"id": eid, "fromNode": read[k], "toNode": read[k + 1],
                              "fromSide": "bottom", "toSide": "top"})
                panel_link_edges[eid] = {"kind": "reading_order"}

            # adjacency for gutter neighbours
            for j, (a, b) in enumerate(_adjacency_pairs(build.panel_ids, page)):
                eid = f"{pid}_adj_{j}"
                edges.append({"id": eid, "fromNode": a, "toNode": b, "fromSide": "right", "toSide": "left"})
                panel_link_edges[eid] = {"kind": "adjacency"}

    # --- sequence chain across all pages (acyclic) --------------------------------------------------------
    for i in range(len(page_ids) - 1):
        eid = f"seq_{i}"
        edges.append({"id": eid, "fromNode": page_ids[i], "toNode": page_ids[i + 1],
                      "fromSide": "bottom", "toSide": "top"})
        panel_link_edges[eid] = {"kind": "sequence"}

    # --- forward + enrich ---------------------------------------------------------------------------------
    source = {"name": comic.id, "version": comic.version, "nodes": nodes, "edges": edges}
    doc = to_canvas(source)

    # isStartNode on the first page (Advanced Canvas / Extended field to_canvas doesn't carry — set post-hoc).
    by_id = {n["id"]: n for n in doc["nodes"]}
    if page_ids:
        by_id[page_ids[0]]["isStartNode"] = True

    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    reserved["adna_version"] = ADNA_VERSION
    reserved["conformance_level"] = "adna_native"
    reserved["component_types"] = component_types
    reserved["semantic_bindings"] = {"profile": "comic"}
    reserved["panel_link"] = {
        "edges": panel_link_edges,
        "regions": regions,
        "surfaces": [{"id": COMIC_ID, "role": "canonical", "surface": "comic_page"}],
    }
    reserved["context_object"] = {"id": comic.id, "version": comic.version, "refs": list(comic.refs)}
    return doc
