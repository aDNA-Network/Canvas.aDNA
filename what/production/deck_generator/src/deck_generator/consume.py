"""The deck generator: ``DeckInput`` -> a v2.0.0-conformant, aDNA-Native deck ``.canvas``.

Each slide is a **group** node nested in a ``deck_root`` group (the single canonical surface). Pipeline:
  1. assemble the ``canvas_std`` **source contract** — deck_root group + per-slide group + interior nodes (from
     ``slides.build_slide``); a ``sequence`` chain across slides + ``reading_order`` within each slide;
  2. ``canvas_std.to_canvas`` (sets ``toEnd`` + ``_reserved.sync``);
  3. set ``isStartNode`` on slide 0 (Extended; ``to_canvas`` carries only text/file/url/label payloads);
  4. **enrich ``_reserved`` to aDNA-Native** — component_types (deck/slide panels + interior classes incl
     image/table) / semantic_bindings / panel_link (regions per slide, **exactly one canonical surface**, sequence +
     reading_order edges) / context_object.

``canvas_std`` is the only substrate dependency and is never mutated (C8).
"""

from __future__ import annotations

from typing import Any

from canvas_std import to_canvas

from deck_generator import layout
from deck_generator.model import DeckInput
from deck_generator.slides import build_slide

ADNA_VERSION = "2.0.0"
DECK_ID = "deck_root"


def build_deck(deck: DeckInput) -> dict[str, Any]:
    """Map a ``DeckInput`` to a v2.0.0 aDNA-Native deck ``.canvas`` document (a plain dict)."""
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    component_types: dict[str, dict[str, Any]] = {}
    panel_link_edges: dict[str, dict[str, str]] = {}
    regions: dict[str, dict[str, Any]] = {}

    deck_box = layout.deck_box(len(deck.slides))
    nodes.append({"id": DECK_ID, "type": "group", "label": deck.title, **deck_box.as_node()})
    component_types[DECK_ID] = {"class": "panel", "semantic_type": "deck", "degrades_to": "group"}

    slide_ids: list[str] = []
    for i, slide in enumerate(deck.slides):
        sid = f"slide{i}"
        sbox = layout.slide_box(i)
        nodes.append({"id": sid, "type": "group", "label": slide.title or slide.type, **sbox.as_node()})
        component_types[sid] = {"class": "panel", "semantic_type": "slide", "degrades_to": "group"}
        regions[sid] = {"flow": "vertical", "pagination": "paged",
                        "extent": {"unit": "slides", "max": 1}, "surface": slide.type}
        slide_ids.append(sid)

        build = build_slide(slide, sid, sbox)
        nodes.extend(build.nodes)
        component_types.update(build.component_types)
        for k, (a, b) in enumerate(build.edges):
            eid = f"{sid}_flow_{k}"
            edges.append({"id": eid, "fromNode": a, "toNode": b, "fromSide": "bottom", "toSide": "top"})
            panel_link_edges[eid] = {"kind": "reading_order"}

    for i in range(len(slide_ids) - 1):
        eid = f"seq_{i}"
        edges.append({"id": eid, "fromNode": slide_ids[i], "toNode": slide_ids[i + 1],
                      "fromSide": "right", "toSide": "left"})
        panel_link_edges[eid] = {"kind": "sequence"}

    source = {"name": deck.id, "version": deck.version, "nodes": nodes, "edges": edges}
    doc = to_canvas(source)

    # isStartNode: an Advanced Canvas field to_canvas doesn't carry from source — set it post-hoc (Extended; KEEP).
    by_id = {n["id"]: n for n in doc["nodes"]}
    by_id[slide_ids[0]]["isStartNode"] = True

    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    reserved["adna_version"] = ADNA_VERSION
    reserved["conformance_level"] = "adna_native"
    reserved["component_types"] = component_types
    reserved["semantic_bindings"] = {"profile": "deck"}
    reserved["panel_link"] = {
        "edges": panel_link_edges,
        "regions": regions,
        "surfaces": [{"id": DECK_ID, "role": "canonical"}],
    }
    reserved["context_object"] = {"id": deck.id, "version": deck.version, "refs": list(deck.refs)}
    return doc
