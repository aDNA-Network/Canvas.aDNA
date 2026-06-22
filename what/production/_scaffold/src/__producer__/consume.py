"""__producer__: ``ProducerInput`` -> a v2.0.0-conformant, aDNA-Native ``.canvas`` (a plain dict).

The canonical 4-step producer contract (mirrors ``deck_generator`` / ``diagram_generator`` / ``document_generator``):

  1. assemble the ``canvas_std`` **source contract** ``{name, version, nodes, edges}`` — a containing ``group`` node
     is the single canonical surface; interior nodes are baseline types (text/file/group/link);
  2. ``doc = to_canvas(source)`` — sets explicit edge ``toEnd`` + ``_reserved.sync``;
  3. **enrich** ``doc["metadata"]["frontmatter"]["_reserved"]`` to aDNA-Native (component_types / semantic_bindings /
     panel_link / context_object).

``canvas_std`` is the ONLY substrate dependency and is NEVER mutated (C8 — the two-shelf firewall).
"""

from __future__ import annotations

from typing import Any

from canvas_std import to_canvas

from __producer__.model import ProducerInput

ADNA_VERSION = "2.0.0"
ROOT_ID = "root"        # TODO(clone): the canonical-surface group id (e.g. "letter_root", "post_root")
PROFILE = "document"    # TODO(clone): your producer-side profile name (bare; NEVER registered in canvas_std.schema)


def build(inp: ProducerInput) -> dict[str, Any]:
    """Map a ``ProducerInput`` to a v2.0.0 aDNA-Native ``.canvas`` document (a plain dict)."""
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    component_types: dict[str, dict[str, Any]] = {}
    panel_link_edges: dict[str, dict[str, str]] = {}

    # 1) The single canonical surface: one group enclosing the artifact.
    #    TODO(clone): real geometry via layout.py; deterministic so round-trip hashes stay stable.
    nodes.append({"id": ROOT_ID, "type": "group", "label": inp.title,
                  "x": 0, "y": 0, "width": 800, "height": 1000})
    component_types[ROOT_ID] = {"class": "panel", "semantic_type": PROFILE, "degrades_to": "group"}

    # TODO(clone): append interior BASELINE nodes (type in {text,file,group,link}) + their component_types entries;
    #              append baseline edges + panel_link_edges[eid] = {"kind": ...}.
    #   Edge-kind discipline: only "sequence" is acyclicity-checked — use it for strictly linear chains
    #   (page/slide/thread order); use "dependency"/"reading_order"/"adjacency" for anything that may cycle.

    # 2) To the substrate.
    source = {"name": inp.id, "version": inp.version, "nodes": nodes, "edges": edges}
    doc = to_canvas(source)

    # 3) Enrich _reserved -> aDNA-Native.
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    reserved["adna_version"] = ADNA_VERSION
    reserved["conformance_level"] = "adna_native"
    reserved["component_types"] = component_types
    reserved["semantic_bindings"] = {"profile": PROFILE}
    reserved["panel_link"] = {
        "edges": panel_link_edges,
        # TODO(clone): per-region {flow, pagination, extent?, surface?}. Omit `extent` if no unit fits
        #   (PL_EXTENT_UNITS = {words, pages, slides}); a non-paginated region uses pagination: "none".
        "regions": {ROOT_ID: {"flow": "vertical", "pagination": "none"}},
        # A-5: exactly ONE canonical surface, and its id MUST resolve to a node above.
        "surfaces": [{"id": ROOT_ID, "role": "canonical"}],
    }
    reserved["context_object"] = {"id": inp.id, "version": inp.version, "refs": list(inp.refs)}
    return doc
