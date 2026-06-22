"""The diagram generator: ``DiagramInput`` -> a v2.0.0-conformant, aDNA-Native diagram ``.canvas``.

Hybrid, native-primary mapping. The whole diagram is ONE ``group`` node = ``diagram_root`` = the single canonical
surface; each ``DiagramNode`` is an interior baseline ``text`` node (its Mermaid shape rides in
``_reserved.component_types[*].qualities.shape``, never on the baseline node); each ``DiagramEdge`` is a baseline edge
with a panel-link ``kind``; PLUS one derived ``mermaid_src`` ``code`` node carrying the generated Mermaid source.

Pipeline (mirrors ``deck_generator.consume``):
  1. assemble the ``canvas_std`` **source contract** — ``{name, version, nodes, edges}`` (same keys as the deck);
  2. ``canvas_std.to_canvas`` (sets explicit ``toEnd`` + ``_reserved.sync``);
  3. **enrich ``_reserved`` to aDNA-Native** — component_types (shape nodes + the code node) / semantic_bindings (the
     bare ``diagram`` profile) / panel_link (one ``diagram_root`` region, exactly one canonical surface, edge kinds) /
     context_object.

Edge-kind mapping (respect the A-5 acyclicity check — only ``sequence`` is acyclicity-checked):
  * ``gantt`` task order -> ``sequence`` (a linear, acyclic chain);
  * ALL other types (flowchart / class_diagram / state_diagram / sequence-diagram messages) -> ``dependency`` (cycles
    allowed — a flowchart or state diagram WITH a cycle must still validate).

``canvas_std`` is the only substrate dependency and is never mutated (C8).
"""

from __future__ import annotations

from typing import Any

from canvas_std import to_canvas

from diagram_generator import layout
from diagram_generator.diagrams import build_nodes
from diagram_generator.mermaid import mermaid_for
from diagram_generator.model import DiagramInput

ADNA_VERSION = "2.0.0"
ROOT_ID = "diagram_root"
SRC_ID = "mermaid_src"

# Region flow per direction (panel_link PL_FLOW = none|vertical|horizontal|columns).
_FLOW_FOR = {"TD": "vertical", "BT": "vertical", "LR": "horizontal", "RL": "horizontal"}


def _edge_kind(diagram_type: str) -> str:
    """gantt -> ``sequence`` (acyclic chain); everything else -> ``dependency`` (cycles permitted)."""
    return "sequence" if diagram_type == "gantt" else "dependency"


def build_diagram(d: DiagramInput) -> dict[str, Any]:
    """Map a ``DiagramInput`` to a v2.0.0 aDNA-Native diagram ``.canvas`` document (a plain dict)."""
    boxes, group_box, src_box = layout.layout(d)

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    component_types: dict[str, dict[str, Any]] = {}
    panel_link_edges: dict[str, dict[str, str]] = {}

    # The single canonical surface: a group enclosing the whole diagram.
    nodes.append({"id": ROOT_ID, "type": "group", "label": d.title, **group_box.as_node()})
    component_types[ROOT_ID] = {"class": "panel", "semantic_type": "diagram", "degrades_to": "group"}

    # Interior nodes (one baseline text node per DiagramNode) + their shape component entries.
    build = build_nodes(d, boxes)
    nodes.extend(build.nodes)
    component_types.update(build.component_types)

    # The derived Mermaid source as a `code` node (degrades to text).
    mermaid = mermaid_for(d)
    nodes.append({"id": SRC_ID, "type": "text", "text": f"```mermaid\n{mermaid}\n```", **src_box.as_node()})
    component_types[SRC_ID] = {
        "class": "code",
        "semantic_type": "mermaid_source",
        "degrades_to": "text",
        "qualities": {"language": "mermaid"},
    }

    # Edges -> baseline edges + panel_link kinds.
    kind = _edge_kind(d.diagram_type)
    horizontal = d.direction in ("LR", "RL")
    from_side, to_side = ("right", "left") if horizontal else ("bottom", "top")
    for i, e in enumerate(d.edges):
        eid = f"edge{i}"
        edges.append({"id": eid, "fromNode": e.from_id, "toNode": e.to_id,
                      "fromSide": from_side, "toSide": to_side})
        panel_link_edges[eid] = {"kind": kind}

    source = {"name": d.id, "version": d.version, "nodes": nodes, "edges": edges}
    doc = to_canvas(source)

    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    reserved["adna_version"] = ADNA_VERSION
    reserved["conformance_level"] = "adna_native"
    reserved["component_types"] = component_types
    reserved["semantic_bindings"] = {"profile": "diagram"}
    reserved["panel_link"] = {
        "edges": panel_link_edges,
        "regions": {
            ROOT_ID: {
                "flow": _FLOW_FOR.get(d.direction, "vertical"),
                "pagination": "none",
                "surface": d.diagram_type,
            }
        },
        "surfaces": [{"id": ROOT_ID, "role": "canonical"}],
    }
    reserved["context_object"] = {"id": d.id, "version": d.version, "refs": list(d.refs)}
    return doc
