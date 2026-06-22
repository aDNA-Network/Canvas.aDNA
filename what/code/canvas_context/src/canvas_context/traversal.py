"""Graph-walking behind the §6 traversal primitives (spec_canvas_context_loading §6).

``reading_order`` gives an agent the *document order* of a non-DAG output (a deck's slides, a paper's sections)
**without rendering** — the core leg-2 capability. It walks ``kind ∈ {reading_order, sequence}`` edges from the
start node (``isStartNode``) / canonical surface, falling back to geometry only when no such edges exist
(spec §6.1). All walks are **cycle-safe** (a re-encountered node is not revisited, spec §5.2 / §9).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # avoid an import cycle at runtime — model imports this module lazily
    from canvas_context.model import ContextGraph, Relation

# The edge kinds that define linear document order (spec_panel_link_semantics §3–§4).
ORDER_KINDS = frozenset({"reading_order", "sequence"})


def neighbors(relations: list[Relation], node_id: str, kind: str | None = None) -> list[str]:
    """Adjacent node ids of ``node_id`` (spec §6), optionally filtered by relation ``kind``.

    Outgoing for directed relations; both directions for an undirected relation (``directed is False``).
    """
    out: list[str] = []
    for r in relations:
        if kind is not None and r.kind != kind:
            continue
        if r.source == node_id and r.target is not None:
            out.append(r.target)
        elif not r.directed and r.target == node_id and r.source is not None:
            out.append(r.source)
    return out


def reading_order(graph: ContextGraph, panel_id: str | None = None) -> list[str]:
    """An ordered node-id walk in document order (spec §6.1).

    Follows ``reading_order``/``sequence`` edges from the start node(s); cycle-safe. When no order-bearing edges
    exist, falls back to a geometry sort (top-to-bottom, then left-to-right). When ``panel_id`` is given, the walk
    starts within that panel's children.
    """
    relations = graph.relations()
    components = {c.id: c for c in graph.components()}

    # Geometry fallback — only when there are NO order-bearing edges at all (spec §6.1).
    if not any(r.kind in ORDER_KINDS for r in relations):
        scope = set(graph.children(panel_id)) if panel_id is not None else set(components)
        ordered = sorted(
            (c for c in components.values() if c.id in scope),
            key=lambda c: (c.geometry.get("y", 0), c.geometry.get("x", 0)),
        )
        return [c.id for c in ordered]

    # Adjacency over order-bearing edges, preserving relation order (insertion order of edges[]).
    adj: dict[str, list[str]] = {}
    for r in relations:
        if r.kind in ORDER_KINDS and r.source is not None and r.target is not None:
            adj.setdefault(r.source, []).append(r.target)

    starts = _start_nodes(graph, components, panel_id)

    order: list[str] = []
    seen: set[str] = set()

    def visit(n: str) -> None:
        if n in seen:  # cycle-safe — a re-encountered node is not revisited (§5.2)
            return
        seen.add(n)
        order.append(n)
        for m in adj.get(n, []):
            visit(m)

    for s in starts:
        visit(s)
    return order


def _start_nodes(graph: ContextGraph, components: dict, panel_id: str | None) -> list[str]:
    """The reading-order entry point(s): isStartNode → canonical surface → first node (spec §6.1)."""
    if panel_id is not None:
        children = graph.children(panel_id)
        flagged = [c for c in children if components.get(c) and components[c].is_start]
        if flagged:
            return flagged
        return children[:1] or [panel_id]

    flagged = [c.id for c in graph.components() if c.is_start]
    if flagged:
        return flagged
    canonical = [s.id for s in graph.surfaces() if s.role == "canonical" and s.id]
    if canonical:
        return canonical
    all_components = graph.components()
    return [all_components[0].id] if all_components else []
