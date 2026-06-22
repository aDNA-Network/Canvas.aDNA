"""The context-graph record shapes (spec_canvas_context_loading §3) + the read-only ``ContextGraph``.

A ``ContextGraph`` is what a loader produces from a ``.canvas``: a navigable, read-only structure carrying the
baseline JSON-Canvas topology (panels / components / relations) plus the additive ``_reserved`` semantic overlay
(component classes, panel-link kinds, context-object identity, refs, anchors, surfaces). The §6 traversal primitives
are exposed as methods; graph-walking lives in ``traversal.py`` (imported lazily to avoid an import cycle).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class _Unresolved:
    """Falsy singleton sentinel for an unresolved ``Ref`` (distinct from a legitimately-``None`` handle, spec §5)."""

    __slots__ = ()

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return "UNRESOLVED"

    def __bool__(self) -> bool:
        return False


UNRESOLVED = _Unresolved()


@dataclass
class Conformance:
    """``{declared, reached, stale}`` (spec §3 / §4 L1, L6)."""

    declared: str | None
    reached: str | None
    stale: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {"declared": self.declared, "reached": self.reached, "stale": self.stale}


@dataclass
class Component:
    """One per ``nodes[]`` entry (spec §3). ``_reserved`` enrichment is additive (L3); absence is valid (§8)."""

    id: str
    node_type: str | None                         # baseline JSON Canvas type: text | file | group | link
    component_class: str | None = None            # _reserved.component_types[id].class (14-class taxonomy)
    semantic_type: str | None = None              # e.g. heading, figure, quote, footnote
    qualities: dict[str, Any] = field(default_factory=dict)
    payload: dict[str, Any] = field(default_factory=dict)   # text? | file? | url? | label? (media by reference)
    degrades_to: str | None = None                # baseline fallback type
    geometry: dict[str, Any] = field(default_factory=dict)  # x, y, width, height — advisory (layout, not semantics)
    is_start: bool = False                        # node.isStartNode — the reading-order entry point


@dataclass
class Panel:
    """A Component with class ∈ {panel, group, region} — a layout-bearing region (spec §3)."""

    id: str
    flow: str | None = None                       # none | vertical | horizontal | columns
    pagination: str | None = None                 # none | paged | continuous
    extent: dict[str, Any] | None = None          # {unit, max} | None
    surface: str | None = None                    # print_page | slide | web | letter | …
    children: list[str] = field(default_factory=list)   # nodes geometrically/semantically contained


@dataclass
class Relation:
    """One per ``edges[]`` entry (spec §3)."""

    id: str
    source: str | None                            # edge.fromNode
    target: str | None                            # edge.toNode
    directed: bool = False                        # from toEnd/fromEnd
    kind: str | None = None                       # _reserved.panel_link.edges[id].kind
    label: str | None = None


@dataclass
class Ref:
    """An outbound context reference (spec §3). ``resolved`` is set only by a resolver (§5)."""

    form: str                                     # wikilink | federation_ref
    target: str                                   # "[[path]]" | "lattice://instance/lattice[/node]"
    resolved: Any = UNRESOLVED


@dataclass
class Surface:
    """A canonical/derived surface declaration (spec §3, from _reserved.panel_link.surfaces[])."""

    id: str | None
    role: str | None = None                       # canonical | derived
    surface: str | None = None                    # free-form, producer-defined (AT-2)
    extra: dict[str, Any] = field(default_factory=dict)   # aspect_ratio, round_trip, … (retained, not interpreted)


class ContextGraph:
    """The read-only context graph (spec §3) with the §6 traversal primitives.

    Construct via :func:`canvas_context.loader.load_context_graph`. All primitives are side-effect-free reads; none
    mutate the source document. ``id``/``version`` are ``None`` for a pure output artifact (no ``context_object``, §8).
    """

    def __init__(
        self,
        *,
        id: str | None,
        version: str | None,
        summary: str | None,
        conformance: Conformance,
        panels: list[Panel],
        components: list[Component],
        relations: list[Relation],
        refs: list[Ref],
        anchors: dict[str, str],
        surfaces: list[Surface],
    ) -> None:
        self.id = id
        self.version = version
        self._summary = summary
        self._conformance = conformance
        self._panels: dict[str, Panel] = {p.id: p for p in panels}
        self._components: dict[str, Component] = {c.id: c for c in components}
        self._relations: list[Relation] = list(relations)
        self._refs: list[Ref] = list(refs)
        self._anchors: dict[str, str] = dict(anchors)
        self._surfaces: list[Surface] = list(surfaces)

    # --- §6 read-only traversal primitives (names illustrative; semantics binding) ---

    def identity(self) -> dict[str, str | None]:
        return {"id": self.id, "version": self.version}

    def summary(self) -> str | None:
        return self._summary

    def conformance(self) -> dict[str, Any]:
        return self._conformance.as_dict()

    def panels(self) -> list[Panel]:
        return list(self._panels.values())

    def panel(self, panel_id: str) -> Panel | None:
        return self._panels.get(panel_id)

    def children(self, panel_id: str) -> list[str]:
        p = self._panels.get(panel_id)
        return list(p.children) if p else []

    def components(self) -> list[Component]:
        return list(self._components.values())

    def component(self, node_id: str) -> Component | None:
        return self._components.get(node_id)

    def relations(self) -> list[Relation]:
        return list(self._relations)

    def neighbors(self, node_id: str, kind: str | None = None) -> list[str]:
        from canvas_context import traversal

        return traversal.neighbors(self._relations, node_id, kind)

    def reading_order(self, panel_id: str | None = None) -> list[str]:
        from canvas_context import traversal

        return traversal.reading_order(self, panel_id)

    def refs(self) -> list[Ref]:
        return list(self._refs)

    def resolve(self, ref: Ref, resolver: Any) -> Any:
        """Resolve one ``Ref`` via a caller-supplied resolver (§5). The loader never transports content itself."""
        return resolver.resolve(ref)

    def anchors(self) -> dict[str, str]:
        return dict(self._anchors)

    def surfaces(self) -> list[Surface]:
        return list(self._surfaces)
