"""The load pipeline (spec_canvas_context_loading §4) — ``load_context_graph``.

Executes the normative L1–L7 steps in order: parse & validate (refuse Core-invalid) → build the baseline graph →
overlay the ``_reserved`` semantic layer (additive) → resolve context identity → classify & expose references →
detect staleness (advisory) → **no rendering**. Reads ``canvas_std``'s public API only (D6 firewall — one-way
dependency; ``canvas_std`` is never mutated).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from canvas_std import ConformanceLevel, compute_sync_hash, validate_suite

from canvas_context.model import (
    Component,
    Conformance,
    ContextGraph,
    Panel,
    Ref,
    Relation,
    Surface,
)

# Inline wikilinks discoverable inside text payloads (spec §4 L5).
_WIKILINK = re.compile(r"\[\[([^\]]+)\]\]")
_PAYLOAD_KEYS = ("text", "file", "url", "label")
_GEOMETRY_KEYS = ("x", "y", "width", "height")


class CoreValidationError(ValueError):
    """Raised when a document fails **Core** validation — the loader refuses to produce a graph (spec §4 L1)."""

    def __init__(self, failures: list[dict[str, Any]]) -> None:
        self.failures = failures
        msgs = "; ".join(f.get("msg", str(f)) for f in failures) or "core validation failed"
        super().__init__(f"refusing to load a Core-invalid canvas: {msgs}")


def load_context_graph(
    source: str | Path | dict[str, Any],
    *,
    resolver: Any | None = None,
    validate: bool = True,
    _seen: dict[str, ContextGraph] | None = None,
) -> ContextGraph:
    """Load a ``.canvas`` into a :class:`~canvas_context.model.ContextGraph` **without rendering** (spec §4).

    ``source`` is a path (``str``/``Path``) or an already-parsed canvas ``dict``. ``resolver`` is unused at load time
    (references are exposed lazily, §4 L5; pass one to ``ContextGraph.resolve``). ``_seen`` (keyed by context-object
    ``id``) makes recursive multi-canvas resolution cycle-safe (§5.2): a re-encountered id returns the existing graph.
    """
    doc = _read_doc(source)  # L1 (parse)
    reserved = _reserved_block(doc)

    # cycle-safe recursive resolution (§5.2): re-encountering a loaded id returns the existing graph
    co_early = reserved.get("context_object")
    early_id = co_early.get("id") if isinstance(co_early, dict) else None
    if _seen is not None and isinstance(early_id, str) and early_id in _seen:
        return _seen[early_id]

    declared = _declared_level(reserved)

    # L1 — validate; refuse a Core-invalid document
    reached: str | None = None
    if validate:
        report = validate_suite(doc, declared)
        reached = report.level_reached.value if report.level_reached else None
        if ConformanceLevel.CORE.value not in report.passed:
            raise CoreValidationError(report.failed)

    # L2 — build the baseline graph (MUST succeed on a _reserved-stripped canvas)
    components, panels = _build_nodes(doc)
    relations = _build_edges(doc)
    _assign_panel_children(components, panels)

    # L3 — overlay the _reserved semantic layer (additive; no silent drop of un-annotated nodes/edges)
    _overlay_reserved(reserved, components, panels, relations)
    anchors, surfaces = _anchors_and_surfaces(reserved)

    # L4 — resolve context identity (absent ⇒ pure output artifact; never fabricate)
    node_id, version, summary, raw_refs = _context_identity(reserved)

    # L5 — classify & expose references (declared + inline wikilinks); resolution is lazy/delegated
    refs = _classify_refs(raw_refs, components)

    # L6 — detect staleness (advisory; never blocks)
    stale = _detect_staleness(doc, reserved)

    # L7 — no rendering: nothing is rasterized/decoded; media rides by reference in Component.payload
    conformance = Conformance(declared=declared.value, reached=reached, stale=stale)
    graph = ContextGraph(
        id=node_id,
        version=version,
        summary=summary,
        conformance=conformance,
        panels=list(panels.values()),
        components=list(components.values()),
        relations=relations,
        refs=refs,
        anchors=anchors,
        surfaces=surfaces,
    )
    if _seen is not None and isinstance(node_id, str):
        _seen[node_id] = graph
    return graph


# --- L1 helpers ---------------------------------------------------------------------------------


def _read_doc(source: str | Path | dict[str, Any]) -> dict[str, Any]:
    if isinstance(source, dict):
        return source
    text = Path(source).read_text(encoding="utf-8")
    doc = json.loads(text)
    if not isinstance(doc, dict):
        raise CoreValidationError([{"id": "C-1", "msg": "document is not a JSON object"}])
    return doc


def _reserved_block(doc: dict[str, Any]) -> dict[str, Any]:
    """``_reserved`` lives at ``metadata.frontmatter._reserved`` (canvas_std validate/CLI convention)."""
    block = doc.get("metadata", {}).get("frontmatter", {}).get("_reserved", {})
    return block if isinstance(block, dict) else {}


def _declared_level(reserved: dict[str, Any]) -> ConformanceLevel:
    """The declared level from ``_reserved.conformance_level``; else inferred to the Core floor (spec §4 L1)."""
    declared = reserved.get("conformance_level")
    try:
        return ConformanceLevel(declared)
    except ValueError:
        return ConformanceLevel.CORE


# --- L2 helpers ---------------------------------------------------------------------------------


def _build_nodes(doc: dict[str, Any]) -> tuple[dict[str, Component], dict[str, Panel]]:
    components: dict[str, Component] = {}
    panels: dict[str, Panel] = {}
    for n in doc.get("nodes", []):
        if not isinstance(n, dict) or "id" not in n:
            continue
        nid = n["id"]
        payload = {k: n[k] for k in _PAYLOAD_KEYS if k in n}
        geometry = {k: n[k] for k in _GEOMETRY_KEYS if k in n}
        components[nid] = Component(
            id=nid,
            node_type=n.get("type"),
            payload=payload,
            geometry=geometry,
            is_start=bool(n.get("isStartNode", False)),
        )
        if n.get("type") == "group":
            panels[nid] = Panel(id=nid)
    return components, panels


def _build_edges(doc: dict[str, Any]) -> list[Relation]:
    relations: list[Relation] = []
    for e in doc.get("edges", []):
        if not isinstance(e, dict) or "id" not in e:
            continue
        directed = e.get("toEnd") == "arrow" or e.get("fromEnd") == "arrow"
        relations.append(
            Relation(
                id=e["id"],
                source=e.get("fromNode"),
                target=e.get("toNode"),
                directed=directed,
                label=e.get("label"),
            )
        )
    return relations


def _assign_panel_children(components: dict[str, Component], panels: dict[str, Panel]) -> None:
    """Assign each node to its *nearest* (smallest) geometrically-containing panel (spec §3 Panel.children)."""
    boxes = {pid: _box(components[pid].geometry) for pid in panels if pid in components}
    for cid, comp in components.items():
        cbox = _box(comp.geometry)
        if cbox is None:
            continue
        containers = [
            pid for pid, pbox in boxes.items() if pid != cid and pbox is not None and _contains(pbox, cbox)
        ]
        if not containers:
            continue
        nearest = min(containers, key=lambda pid: _area(boxes[pid]))
        panels[nearest].children.append(cid)


def _box(geometry: dict[str, Any]) -> tuple[int, int, int, int] | None:
    if not all(k in geometry for k in _GEOMETRY_KEYS):
        return None
    try:
        return (int(geometry["x"]), int(geometry["y"]), int(geometry["width"]), int(geometry["height"]))
    except (TypeError, ValueError):
        return None


def _contains(outer: tuple[int, int, int, int], inner: tuple[int, int, int, int]) -> bool:
    ox, oy, ow, oh = outer
    ix, iy, iw, ih = inner
    return ix >= ox and iy >= oy and ix + iw <= ox + ow and iy + ih <= oy + oh


def _area(box: tuple[int, int, int, int]) -> int:
    return box[2] * box[3]


# --- L3 helpers ---------------------------------------------------------------------------------


def _overlay_reserved(
    reserved: dict[str, Any],
    components: dict[str, Component],
    panels: dict[str, Panel],
    relations: list[Relation],
) -> None:
    ct = reserved.get("component_types")
    if isinstance(ct, dict):
        for nid, entry in ct.items():
            comp = components.get(nid)
            if comp is None or not isinstance(entry, dict):
                continue
            comp.component_class = entry.get("class")
            comp.semantic_type = entry.get("semantic_type")
            if isinstance(entry.get("qualities"), dict):
                comp.qualities = entry["qualities"]
            comp.degrades_to = entry.get("degrades_to")

    pl = reserved.get("panel_link")
    if not isinstance(pl, dict):
        return

    regions = pl.get("regions")
    if isinstance(regions, dict):
        for gid, region in regions.items():
            if not isinstance(region, dict):
                continue
            panel = panels.get(gid)
            if panel is None:
                panel = Panel(id=gid)
                panels[gid] = panel
            panel.flow = region.get("flow")
            panel.pagination = region.get("pagination")
            panel.extent = region.get("extent")
            panel.surface = region.get("surface")

    edges_meta = pl.get("edges")
    if isinstance(edges_meta, dict):
        by_id = {r.id: r for r in relations}
        for eid, meta in edges_meta.items():
            r = by_id.get(eid)
            if r is not None and isinstance(meta, dict):
                r.kind = meta.get("kind")


def _anchors_and_surfaces(reserved: dict[str, Any]) -> tuple[dict[str, str], list[Surface]]:
    pl = reserved.get("panel_link")
    pl = pl if isinstance(pl, dict) else {}
    anchors = pl.get("anchors")
    anchors = dict(anchors) if isinstance(anchors, dict) else {}
    surfaces: list[Surface] = []
    for s in pl.get("surfaces") or []:
        if isinstance(s, dict):
            extra = {k: v for k, v in s.items() if k not in ("id", "role", "surface")}
            surfaces.append(Surface(id=s.get("id"), role=s.get("role"), surface=s.get("surface"), extra=extra))
    return anchors, surfaces


# --- L4 / L5 / L6 helpers -----------------------------------------------------------------------


def _context_identity(reserved: dict[str, Any]) -> tuple[str | None, str | None, str | None, list[Any]]:
    co = reserved.get("context_object")
    if not isinstance(co, dict):
        return None, None, None, []
    raw_refs = co.get("refs")
    raw_refs = raw_refs if isinstance(raw_refs, list) else []
    return co.get("id"), co.get("version"), co.get("summary"), raw_refs


def _classify_refs(raw_refs: list[Any], components: dict[str, Component]) -> list[Ref]:
    refs: list[Ref] = []
    seen: set[tuple[str, str]] = set()

    def add(form: str, target: str) -> None:
        key = (form, target)
        if key not in seen:
            seen.add(key)
            refs.append(Ref(form=form, target=target))

    for raw in raw_refs:
        target = _ref_target(raw)
        if target:
            add(_classify(target), target)

    # inline wikilinks discovered in text payloads (spec §4 L5)
    for comp in components.values():
        text = comp.payload.get("text")
        if isinstance(text, str):
            for inner in _WIKILINK.findall(text):
                add("wikilink", f"[[{inner}]]")
    return refs


def _ref_target(raw: Any) -> str | None:
    if isinstance(raw, str):
        return raw
    if isinstance(raw, dict):
        for key in ("target", "ref", "federation_ref", "uri"):
            if isinstance(raw.get(key), str):
                return raw[key]
    return None


def _classify(target: str) -> str:
    return "federation_ref" if target.startswith("lattice://") else "wikilink"


def _detect_staleness(doc: dict[str, Any], reserved: dict[str, Any]) -> bool:
    """Advisory: recompute the topology hash and compare to ``_reserved.sync.sync_hash`` (spec §4 L6)."""
    sync = reserved.get("sync")
    stored = sync.get("sync_hash") if isinstance(sync, dict) else None
    if not isinstance(stored, str):
        return False
    try:
        return compute_sync_hash(doc) != stored
    except Exception:
        return False
