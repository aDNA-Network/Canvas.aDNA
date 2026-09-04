"""Input model — a structured diagram spec (a typed graph).

A substrate-free producer-side domain model: a human/agent authors a diagram (a title + a diagram type + nodes +
edges), and the consumer (``consume.py``) maps it onto the aDNA Canvas Standard (the whole diagram → one ``group``
node = the single canonical surface; each diagram node → an interior baseline node; each edge → a baseline edge with a
panel-link ``kind``; plus one derived ``code`` node carrying the generated Mermaid source). No ``canvas_std`` import
here.

Lineage (KEEP reference, not a dependency): ``Archive.aDNA/CanvasForge.aDNA/what/code/canvas_core/mermaid.py`` —
``MermaidNode``/``MermaidEdge`` retyped here as substrate-free frozen dataclasses (theme coupling dropped).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# The five diagram types ported from CanvasForge's MermaidGenerator (the rest are P5/engine concerns).
DIAGRAM_TYPES: frozenset[str] = frozenset(
    {"flowchart", "sequence", "class_diagram", "state_diagram", "gantt"}
)

# Flow directions (Mermaid vocab) — validated on flowchart/state diagrams; advisory elsewhere.
DIRECTIONS: frozenset[str] = frozenset({"TD", "LR", "RL", "BT"})

# Node shapes — Mermaid vocab (NOT the canvas VALID_SHAPES enum; carried only in _reserved qualities.shape).
NODE_SHAPES: frozenset[str] = frozenset({"rect", "round", "diamond", "stadium", "circle"})

# Authority models — the diagrammatic-context authority axis (Blueprint P1 draft pattern; adr_011 rules
# the `view` row). Declared in `_reserved.authority`; `""` means undeclared, which stays legal here so
# every pre-existing spec keeps building unchanged.
#
# ⚠ `canvas_std` does NOT know this key (F-B1-2, 2026-08-24): it is normative in the doctrine and
# unvalidated by the Standard, so `authority: "veiw"` passes `canvas-std validate` silently. The
# validated-enum fix is LIP-0010 Option B, deferred by design pending Rosetta's ruling on the pattern.
# Until then this frozenset is the ONLY place a typo is caught — producer-side, which is why the check
# lives here rather than being left to the validator that cannot perform it.
AUTHORITY_MODELS: frozenset[str] = frozenset({"dual_channel", "generator", "view"})


@dataclass(frozen=True)
class DiagramNode:
    """A node in the diagram graph. ``members`` carries class-diagram attributes (ignored by other types)."""

    id: str
    label: str = ""
    shape: str = "rect"
    members: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("DiagramNode.id must be non-empty")
        if self.shape not in NODE_SHAPES:
            raise ValueError(
                f"unknown node shape {self.shape!r}; expected one of {sorted(NODE_SHAPES)}"
            )


@dataclass(frozen=True)
class DiagramEdge:
    """An edge between two diagram nodes. ``relation`` is the domain relation; the canvas panel-link ``kind`` is
    derived in ``consume.py`` (gantt task-order -> ``sequence``; all others -> ``dependency``)."""

    from_id: str
    to_id: str
    label: str = ""
    relation: str = "flow"  # flow | dependency | inherits | composition | aggregation | message | transition

    def __post_init__(self) -> None:
        if not self.from_id or not self.to_id:
            raise ValueError("DiagramEdge requires both from_id and to_id")


@dataclass(frozen=True)
class DiagramInput:
    title: str
    id: str
    version: str
    diagram_type: str
    nodes: tuple[DiagramNode, ...]
    edges: tuple[DiagramEdge, ...] = ()
    direction: str = "TD"
    refs: tuple[str, ...] = ()
    # Diagrammatic-context fields (optional; both default off so existing specs are unaffected).
    authority: str = ""       # "" | dual_channel | generator | view  -> _reserved.authority
    prose: str = ""           # vault-relative path of the prose channel; appended to context_object.refs

    def __post_init__(self) -> None:
        if self.authority and self.authority not in AUTHORITY_MODELS:
            raise ValueError(
                f"unknown authority {self.authority!r}; expected one of {sorted(AUTHORITY_MODELS)}"
            )
        if self.prose and self.authority != "dual_channel":
            # A prose channel is what `dual_channel` MEANS. Declaring one under `generator`/`view`
            # (or with no authority at all) is a spec error, not a harmless extra: it would emit a
            # canvas asserting a sync obligation its declared authority does not carry.
            raise ValueError(
                f"prose channel declared with authority {self.authority or '(none)'!r}; "
                "a prose pair requires authority: dual_channel"
            )
        if self.diagram_type not in DIAGRAM_TYPES:
            raise ValueError(
                f"unknown diagram_type {self.diagram_type!r}; expected one of {sorted(DIAGRAM_TYPES)}"
            )
        if self.direction not in DIRECTIONS:
            raise ValueError(
                f"unknown direction {self.direction!r}; expected one of {sorted(DIRECTIONS)}"
            )
        if not self.nodes:
            raise ValueError("diagram has no nodes")
        ids = [n.id for n in self.nodes]
        if len(ids) != len(set(ids)):
            raise ValueError("duplicate node id in diagram")
        known = set(ids)
        for e in self.edges:
            if e.from_id not in known:
                raise ValueError(f"edge from_id {e.from_id!r} not a declared node")
            if e.to_id not in known:
                raise ValueError(f"edge to_id {e.to_id!r} not a declared node")

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> DiagramInput:
        nodes = tuple(
            DiagramNode(
                id=str(n["id"]),
                label=str(n.get("label", n["id"])),
                shape=str(n.get("shape", "rect")),
                members=tuple(str(m) for m in n.get("members", [])),
            )
            for n in d.get("nodes", [])
        )
        edges = tuple(
            DiagramEdge(
                from_id=str(e["from"]) if "from" in e else str(e["from_id"]),
                to_id=str(e["to"]) if "to" in e else str(e["to_id"]),
                label=str(e.get("label", "")),
                relation=str(e.get("relation", "flow")),
            )
            for e in d.get("edges", [])
        )
        return cls(
            title=str(d["title"]),
            id=str(d["id"]),
            version=str(d.get("version", "0.1.0")),
            diagram_type=str(d["diagram_type"]),
            direction=str(d.get("direction", "TD")),
            refs=tuple(str(r) for r in d.get("refs", [])),
            authority=str(d.get("authority", "")),
            prose=str(d.get("prose", "")),
            nodes=nodes,
            edges=edges,
        )


def load_diagram(path: str | Path) -> DiagramInput:
    """Load a diagram from ``.yaml``/``.yml`` (PyYAML) or ``.json``."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in (".yaml", ".yml"):
        import yaml

        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"diagram input {p} did not parse to a mapping")
    return DiagramInput.from_dict(data)
