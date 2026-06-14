"""Validators for the additive ``_reserved`` block (the aDNA-Native A-* checks).

E1.4 implements ``validate_reserved`` + the ``component_types`` and ``panel_link`` sub-validators
(spec_conformance_suite §4; spec_component_model §7; spec_panel_link_semantics §6; spec_context_object §4).

Spec: spec_adna_canvas_standard §7.
"""

from __future__ import annotations

import re
from typing import Any

from canvas_std import schema

# The reserved-key namespace (spec_adna_canvas_standard §7.2).
RESERVED_KEYS: tuple[str, ...] = (
    "adna_version",
    "conformance_level",
    "sync",
    "component_types",
    "semantic_bindings",
    "brand_style_pack_ref",
    "panel_link",
    "context_object",
)

# Component taxonomy (spec_component_model §2) and the baseline degradation types.
COMPONENT_CLASSES: frozenset[str] = frozenset(
    {"text", "typography_run", "image", "video", "shape", "embed", "group", "panel",
     "link", "edge", "table", "code", "caption", "region"}
)
BASELINE_TYPES: frozenset[str] = frozenset({"text", "file", "group", "link"})

# Panel/link vocabularies (spec_panel_link_semantics §3–§4).
PL_EDGE_KINDS: frozenset[str] = frozenset({"sequence", "reading_order", "adjacency", "dependency"})
PL_FLOW: frozenset[str] = frozenset({"none", "vertical", "horizontal", "columns"})
PL_PAGINATION: frozenset[str] = frozenset({"none", "paged", "continuous"})
PL_EXTENT_UNITS: frozenset[str] = frozenset({"words", "pages", "slides"})

_SEMVER = re.compile(r"^\d+\.\d+\.\d+")
_HEX16 = re.compile(r"^[0-9a-f]{16}$")


def validate_reserved(reserved: dict[str, Any], doc: dict[str, Any]) -> list[str]:
    """Validate a ``_reserved`` block (A-* checks). ``doc`` supplies node/edge ids for resolution."""
    errors: list[str] = []
    if not isinstance(reserved, dict):
        return ["A-2: _reserved is not an object"]
    node_ids = {n["id"] for n in doc.get("nodes", []) if isinstance(n, dict) and "id" in n}
    edge_ids = {e["id"] for e in doc.get("edges", []) if isinstance(e, dict) and "id" in e}

    # A-2
    av = reserved.get("adna_version")
    if not (isinstance(av, str) and _SEMVER.match(av)):
        errors.append(f"A-2: adna_version {av!r} missing or not semver")
    cl = reserved.get("conformance_level")
    if cl != "adna_native":
        errors.append(f"A-2: conformance_level {cl!r} must be 'adna_native' for an aDNA-Native canvas")

    # A-6 (structural — hash↔source match is checked by the round-trip layer)
    sync = reserved.get("sync")
    if not isinstance(sync, dict):
        errors.append("A-6: _reserved.sync missing")
    else:
        sh = sync.get("sync_hash")
        if not (isinstance(sh, str) and _HEX16.match(sh)):
            errors.append(f"A-6: sync.sync_hash {sh!r} is not 16 hex chars")

    # A-3 / A-5 / A-7
    if "component_types" in reserved:
        errors += validate_component_types(reserved["component_types"], node_ids)
    if "semantic_bindings" in reserved:
        errors += _validate_semantic_bindings(reserved["semantic_bindings"])
    if "panel_link" in reserved:
        errors += validate_panel_link(reserved["panel_link"], node_ids, doc.get("edges", []), edge_ids)
    if "context_object" in reserved:
        errors += _validate_context_object(reserved["context_object"])
    return errors


def validate_component_types(block: dict[str, Any], node_ids: set[str]) -> list[str]:
    """spec_component_model §7 — each key resolves to a node/edge id; class ∈ taxonomy; degrades_to ∈ baseline."""
    errors: list[str] = []
    if not isinstance(block, dict):
        return ["A-3: component_types is not an object"]
    for nid, entry in block.items():
        if nid not in node_ids:
            errors.append(f"A-3: component_types key {nid!r} does not resolve to a node")
        if not isinstance(entry, dict):
            errors.append(f"A-3: component_types[{nid!r}] is not an object")
            continue
        if entry.get("class") not in COMPONENT_CLASSES:
            errors.append(f"A-3: component {nid!r} class {entry.get('class')!r} not in taxonomy")
        dt = entry.get("degrades_to")
        if dt is not None and dt not in BASELINE_TYPES:
            errors.append(f"A-3: component {nid!r} degrades_to {dt!r} not in {sorted(BASELINE_TYPES)}")
    return errors


def _validate_semantic_bindings(block: Any) -> list[str]:
    """spec_component_model §4 — inline bindings use only §6 tokens; the built-in 'lattice' profile is unmodified."""
    errors: list[str] = []
    if not isinstance(block, dict):
        return ["A-4: semantic_bindings is not an object"]
    if block.get("profile") == "lattice" and "bindings" not in block:
        return errors  # naming the built-in profile is fine
    for name, binding in block.get("bindings", {}).items():
        if not isinstance(binding, dict):
            continue
        if "shape" in binding and binding["shape"] not in schema.VALID_SHAPES:
            errors.append(f"A-4: semantic_bindings[{name!r}] shape {binding['shape']!r} not in enum")
        if "color" in binding and binding["color"] is not None and binding["color"] not in schema.VALID_COLORS:
            errors.append(f"A-4: semantic_bindings[{name!r}] color {binding['color']!r} not in enum")
    return errors


def validate_panel_link(block: dict[str, Any], node_ids: set[str], edges: list[Any], edge_ids: set[str]) -> list[str]:
    """spec_panel_link_semantics §6 — kinds/ids resolve, sequence acyclic, exactly one canonical surface."""
    errors: list[str] = []
    if not isinstance(block, dict):
        return ["A-5: panel_link is not an object"]

    edge_endpoints = {e["id"]: (e.get("fromNode"), e.get("toNode")) for e in edges if isinstance(e, dict) and "id" in e}
    seq_graph: dict[str, list[str]] = {}
    for eid, meta in block.get("edges", {}).items():
        if eid not in edge_ids:
            errors.append(f"A-5: panel_link.edges key {eid!r} does not resolve to an edge")
        kind = meta.get("kind") if isinstance(meta, dict) else None
        if kind not in PL_EDGE_KINDS:
            errors.append(f"A-5: panel_link edge {eid!r} kind {kind!r} not in {sorted(PL_EDGE_KINDS)}")
        if kind == "sequence" and eid in edge_endpoints:
            frm, to = edge_endpoints[eid]
            seq_graph.setdefault(frm, []).append(to)
    if _has_cycle(seq_graph):
        errors.append("A-5: panel_link 'sequence' chain has a cycle")

    for gid, region in block.get("regions", {}).items():
        if gid not in node_ids:
            errors.append(f"A-5: panel_link.regions key {gid!r} does not resolve to a node/group")
        if not isinstance(region, dict):
            continue
        if "flow" in region and region["flow"] not in PL_FLOW:
            errors.append(f"A-5: region {gid!r} flow {region['flow']!r} invalid")
        if "pagination" in region and region["pagination"] not in PL_PAGINATION:
            errors.append(f"A-5: region {gid!r} pagination {region['pagination']!r} invalid")
        unit = (region.get("extent") or {}).get("unit")
        if unit is not None and unit not in PL_EXTENT_UNITS:
            errors.append(f"A-5: region {gid!r} extent.unit {unit!r} invalid")

    surfaces = block.get("surfaces")
    if surfaces is not None:
        canonical = [s for s in surfaces if isinstance(s, dict) and s.get("role") == "canonical"]
        if len(canonical) != 1:
            errors.append(f"A-5: panel_link must have exactly one canonical surface (found {len(canonical)})")
        for s in surfaces:
            if isinstance(s, dict) and s.get("id") not in node_ids:
                errors.append(f"A-5: surface id {s.get('id')!r} does not resolve to a node/group")
    return errors


def _has_cycle(graph: dict[str, list[str]]) -> bool:
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {}

    def visit(u: str) -> bool:
        color[u] = GRAY
        for v in graph.get(u, []):
            if color.get(v, WHITE) == GRAY:
                return True
            if color.get(v, WHITE) == WHITE and visit(v):
                return True
        color[u] = BLACK
        return False

    return any(color.get(n, WHITE) == WHITE and visit(n) for n in list(graph))


def _validate_context_object(block: Any) -> list[str]:
    """spec_context_object §4 — stable id; semver version; well-formed refs."""
    errors: list[str] = []
    if not isinstance(block, dict):
        return ["A-7: context_object is not an object"]
    if not isinstance(block.get("id"), str) or not block["id"]:
        errors.append("A-7: context_object.id missing")
    v = block.get("version")
    if v is not None and not (isinstance(v, str) and _SEMVER.match(v)):
        errors.append(f"A-7: context_object.version {v!r} not semver")
    refs = block.get("refs", [])
    if not isinstance(refs, list):
        errors.append("A-7: context_object.refs must be a list")
    return errors
