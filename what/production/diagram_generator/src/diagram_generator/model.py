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

from canvas_std.reserved import AUTHORITY_VALUES, PRODUCTION_VALUES

# The five diagram types ported from CanvasForge's MermaidGenerator (the rest are P5/engine concerns).
DIAGRAM_TYPES: frozenset[str] = frozenset(
    {"flowchart", "sequence", "class_diagram", "state_diagram", "gantt"}
)

# Flow directions (Mermaid vocab) — validated on flowchart/state diagrams; advisory elsewhere.
DIRECTIONS: frozenset[str] = frozenset({"TD", "LR", "RL", "BT"})

# Node shapes — Mermaid vocab (NOT the canvas VALID_SHAPES enum; carried only in _reserved qualities.shape).
NODE_SHAPES: frozenset[str] = frozenset({"rect", "round", "diamond", "stadium", "circle"})

# The diagrammatic-context axes. Declared in `_reserved.authority` / `_reserved.production`; `""`
# means undeclared on either, which stays legal so every pre-existing spec keeps building unchanged.
#
# ⛩ SPLIT 2026-09-11 (aDNA.aDNA HAUSSMANN R1, `pattern_diagrammatic_context`), on Canvas's own offer
# as amended by our erratum E2. `generator` was REMOVED from the authority axis — it never answered
# "who owns the meaning", it answered "how is the picture made". The two questions now have a field
# each. ⭐ The "never hand-edit; regenerate" discipline attaches to `production: generated` and to NO
# authority value, which is the whole reason the axes are split: this very producer's own two output
# canvases are `dual_channel` AND machine-generated at once, so under the old single enum a reader
# following the table literally received no instruction not to hand-edit them.
#
# ⛩ DE-DUPLICATED 2026-09-11 (Gridline). This comment used to read: *"`canvas_std` STILL does not know
# either key (F-B1-2), so `authority: "veiw"` passes `canvas-std validate` silently. These two
# frozensets and `canvas_core.conform` are the ONLY places a typo is caught anywhere."* **All of that
# is now false** — LIP-0010 was ratified and `canvas_std` validates both keys as **A-8** at Standard
# **v2.4.0**. The values are therefore imported from the Standard rather than restated here; this
# module keeps only the *early* raise, which still earns its place (a spec error caught at
# `__post_init__` never reaches a file). ⇒ one definition, two enforcement points, no drift possible.
AUTHORITY_MODELS: frozenset[str] = AUTHORITY_VALUES
PRODUCTION_MODES: frozenset[str] = PRODUCTION_VALUES


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
    # Diagrammatic-context fields (optional; all default off so existing specs are unaffected).
    authority: str = ""       # "" | dual_channel | view          -> _reserved.authority
    production: str = ""      # "" | hand_authored | generated    -> _reserved.production
    prose: str = ""           # vault-relative path of the prose channel; appended to context_object.refs

    def __post_init__(self) -> None:
        if self.authority and self.authority not in AUTHORITY_MODELS:
            hint = (
                " — `generator` was REMOVED from this axis on 2026-09-11; it answers *how is the "
                "picture made*, so declare production: generated instead"
                if self.authority == "generator"
                else ""
            )
            raise ValueError(
                f"unknown authority {self.authority!r}; expected one of {sorted(AUTHORITY_MODELS)}{hint}"
            )
        if self.production and self.production not in PRODUCTION_MODES:
            raise ValueError(
                f"unknown production {self.production!r}; expected one of {sorted(PRODUCTION_MODES)}"
            )
        if self.prose and self.authority != "dual_channel":
            # A prose channel is what `dual_channel` MEANS. Declaring one under `view` (or with no
            # authority at all) is a spec error, not a harmless extra: it would emit a canvas
            # asserting a sync obligation its declared authority does not carry.
            raise ValueError(
                f"prose channel declared with authority {self.authority or '(none)'!r}; "
                "a prose pair requires authority: dual_channel"
            )
        # ⛩ A-8, Standard v2.4.0 (Gridline P1) — LAST of the axis checks, deliberately. A spec that is
        # both contradictory (prose under `view`) and incomplete (no `production`) should hear about
        # the contradiction first: it is the more specific fault and fixing it may change what
        # `production` should say. The Standard now REJECTS `authority` without `production`, so
        # emitting that pair would build a canvas `canvas-std validate` refuses — and refusing here
        # beats failing after it is in someone's file, this module's standing discipline. The converse
        # is deliberately allowed: `production` alone is correct for a diagram no other channel owns.
        if self.authority and not self.production:
            raise ValueError(
                f"authority {self.authority!r} declared without production — A-8 (Standard v2.4.0) "
                "requires `production` whenever `authority` is present: declaring that another "
                "channel owns this diagram's meaning while leaving unsaid how it is made omits the "
                "field carrying 'never hand-edit; regenerate'. Add production: generated "
                "(diagram_generator output always is)."
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
            production=str(d.get("production", "")),
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
