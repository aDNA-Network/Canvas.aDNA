"""Diagram builders — map each diagram type to interior canvas nodes (the ``slides.py`` analog).

Hybrid, native-primary mapping (Operation Atelier A1):
  * each ``DiagramNode`` -> an interior baseline ``text`` node carrying its label; in ``_reserved.component_types`` it
    is ``{class: "shape", semantic_type: <role>, qualities: {shape: <mermaid shape>}, degrades_to: "text"}``. The
    Mermaid shape rides ONLY in ``qualities.shape`` — we NEVER set baseline ``styleAttributes.shape`` (the canvas
    ``VALID_SHAPES`` enum lacks rect/round/stadium, so setting it would fail E-2/D-2).
  * the per-type builder owns how a node's text reads (e.g. class_diagram folds ``members`` into the label).

Component classes come from ``canvas_std.reserved.COMPONENT_CLASSES`` and every ``degrades_to`` is a baseline node type
(text/file/link/group). Geometry is supplied by ``layout.py``; this module only fills text + the component entries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from diagram_generator.layout import Box
from diagram_generator.model import DiagramInput, DiagramNode

# Mermaid shape -> the node's semantic role (a hint for an iii/ review lens; informational, not validated).
_SHAPE_ROLE: dict[str, str] = {
    "rect": "process",
    "round": "event",
    "stadium": "terminal",
    "diamond": "decision",
    "circle": "state",
}


@dataclass
class DiagramBuild:
    nodes: list[dict[str, Any]]
    component_types: dict[str, dict[str, Any]] = field(default_factory=dict)


def _text(nid: str, text: str, box: Box) -> dict[str, Any]:
    return {"id": nid, "type": "text", "text": text, **box.as_node()}


def _shape_comp(node: DiagramNode) -> dict[str, Any]:
    """The ``_reserved.component_types`` entry for a diagram node: a ``shape`` carrying the Mermaid shape in
    ``qualities`` (never on the baseline node), degrading to ``text``."""
    return {
        "class": "shape",
        "semantic_type": _SHAPE_ROLE.get(node.shape, "node"),
        "degrades_to": "text",
        "qualities": {"shape": node.shape},
    }


def _node_text(node: DiagramNode, diagram_type: str) -> str:
    """The interior text for a node, by diagram type."""
    label = node.label or node.id
    if diagram_type == "class_diagram" and node.members:
        body = "\n".join(f"- {m}" for m in node.members)
        return f"**{label}**\n{body}"
    if diagram_type == "gantt":
        # gantt node label carries the duration; show task id + duration in the panel.
        return f"{node.id}: {label}"
    if diagram_type == "sequence":
        return f"**{label}**"  # a participant
    return label


def build_nodes(d: DiagramInput, boxes: dict[str, Box]) -> DiagramBuild:
    """Build the interior baseline nodes (one per ``DiagramNode``) + their ``shape`` component entries."""
    nodes: list[dict[str, Any]] = []
    comps: dict[str, dict[str, Any]] = {}
    for dn in d.nodes:
        nodes.append(_text(dn.id, _node_text(dn, d.diagram_type), boxes[dn.id]))
        comps[dn.id] = _shape_comp(dn)
    return DiagramBuild(nodes, comps)
