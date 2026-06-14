"""Validation + the degradation strip.

E1.1 implements the **Core (C-*)** and **Extended (E-*)** checks (spec_conformance_suite §2–§3) against the
KEEP-floor enums (``schema``). aDNA-Native (A-*) delegates to ``reserved`` (NotImplementedError until E1.4);
``strip`` is E1.5. Conformance is monotone: aDNA-Native ⊃ Extended ⊃ Core.

Spec: spec_adna_canvas_standard §4–§6, §10 · spec_conformance_suite §2–§5.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from canvas_std import schema


class ConformanceLevel(str, Enum):
    CORE = "core"
    EXTENDED = "extended"
    ADNA_NATIVE = "adna_native"


class ValidationError(Exception):
    """Raised (or collected) when a document fails its declared conformance level."""


def _is_int(v: Any) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _color_ok(c: Any) -> bool:
    return c in schema.VALID_COLORS or (isinstance(c, str) and c.startswith("#"))


def _core_checks(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    nodes = doc.get("nodes")
    edges = doc.get("edges")
    # C-1
    if not isinstance(nodes, list):
        errors.append("C-1: top-level 'nodes' array missing")
        nodes = []
    if not isinstance(edges, list):
        errors.append("C-1: top-level 'edges' array missing")
        edges = []

    # C-2 (nodes)
    node_ids: set[str] = set()
    for i, n in enumerate(nodes):
        if not isinstance(n, dict):
            errors.append(f"C-2: node[{i}] is not an object")
            continue
        nid = n.get("id")
        for f in schema.NODE_REQUIRED_FIELDS:
            if f not in n:
                errors.append(f"C-2: node {nid!r} missing required field '{f}'")
        if isinstance(nid, str):
            if nid in node_ids:
                errors.append(f"C-2: duplicate node id {nid!r}")
            node_ids.add(nid)
        if n.get("type") not in schema.VALID_NODE_TYPES:
            errors.append(f"C-2: node {nid!r} type {n.get('type')!r} not in {sorted(schema.VALID_NODE_TYPES)}")
        for f in ("x", "y", "width", "height"):
            if f in n and not _is_int(n[f]):
                errors.append(f"C-2: node {nid!r} field '{f}' must be an integer")
        # C-5 (color)
        if "color" in n and not _color_ok(n["color"]):
            errors.append(f"C-2/C-5: node {nid!r} color {n['color']!r} not a valid slot or #-hex")

    # C-3 / C-4 (edges)
    edge_ids: set[str] = set()
    for i, e in enumerate(edges):
        if not isinstance(e, dict):
            errors.append(f"C-3: edge[{i}] is not an object")
            continue
        eid = e.get("id")
        for f in schema.EDGE_REQUIRED_FIELDS:
            if f not in e:
                errors.append(f"C-3: edge {eid!r} missing required field '{f}'")
        if isinstance(eid, str):
            if eid in edge_ids:
                errors.append(f"C-3: duplicate edge id {eid!r}")
            edge_ids.add(eid)
        if e.get("fromSide") not in schema.VALID_SIDES:
            errors.append(f"C-3: edge {eid!r} fromSide {e.get('fromSide')!r} invalid")
        if e.get("toSide") not in schema.VALID_SIDES:
            errors.append(f"C-3: edge {eid!r} toSide {e.get('toSide')!r} invalid")
        for endpoint in ("fromNode", "toNode"):
            ref = e.get(endpoint)
            if ref is not None and ref not in node_ids:
                errors.append(f"C-3: edge {eid!r} {endpoint} {ref!r} does not resolve to a node")
        # C-4 — every edge MUST carry an explicit top-level toEnd ∈ VALID_ENDS.
        # (v1.0.0 "always include toEnd:arrow" + I4; an omitted toEnd is the bug the negative fixture encodes.
        #  An explicit toEnd:"none" is a permitted undirected edge.)
        if "toEnd" not in e:
            errors.append(f"C-4: edge {eid!r} missing explicit top-level 'toEnd' (use \"arrow\")")
        elif e["toEnd"] not in schema.VALID_ENDS:
            errors.append(f"C-4: edge {eid!r} toEnd {e['toEnd']!r} not in {sorted(schema.VALID_ENDS)}")
        if "fromEnd" in e and e["fromEnd"] not in schema.VALID_ENDS:
            errors.append(f"C-4: edge {eid!r} fromEnd {e['fromEnd']!r} not in {sorted(schema.VALID_ENDS)}")
    return errors


def _extended_checks(doc: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for n in doc.get("nodes", []):
        if not isinstance(n, dict):
            continue
        nid = n.get("id")
        sa = n.get("styleAttributes")
        if isinstance(sa, dict):
            if sa.get("shape") not in schema.VALID_SHAPES:
                errors.append(f"E-2: node {nid!r} shape {sa.get('shape')!r} invalid")
            if "border" in sa and sa["border"] not in schema.VALID_BORDERS:
                errors.append(f"E-2: node {nid!r} border {sa['border']!r} invalid")
            if "textAlign" in sa and sa["textAlign"] not in schema.VALID_TEXT_ALIGN:
                errors.append(f"E-2: node {nid!r} textAlign {sa['textAlign']!r} invalid")
        for flag in ("isStartNode", "collapsed"):
            if flag in n and not isinstance(n[flag], bool):
                errors.append(f"E-4: node {nid!r} '{flag}' must be boolean")
    for e in doc.get("edges", []):
        if not isinstance(e, dict):
            continue
        eid = e.get("id")
        sa = e.get("styleAttributes")
        if isinstance(sa, dict):
            if "path" in sa and sa["path"] not in schema.VALID_PATH_STYLES:
                errors.append(f"E-3: edge {eid!r} path {sa['path']!r} invalid")
            if "arrow" in sa and sa["arrow"] not in schema.VALID_ARROWS:
                errors.append(f"E-3: edge {eid!r} arrow {sa['arrow']!r} invalid")
            if "pathfindingMethod" in sa and sa["pathfindingMethod"] not in schema.VALID_PATHFINDING:
                errors.append(f"E-3: edge {eid!r} pathfindingMethod {sa['pathfindingMethod']!r} invalid")
    return errors


def validate(doc: dict[str, Any], level: ConformanceLevel = ConformanceLevel.CORE) -> list[str]:
    """Return a list of human-readable errors ([] == valid at ``level``).

    Core (C-*) always; Extended (E-*) for Extended/aDNA-Native; aDNA-Native (A-*) for aDNA-Native.
    The A-* (``_reserved``) layer is implemented at E1.4 — until then aDNA-Native validation raises.
    """
    if not isinstance(doc, dict):
        return ["C-1: document is not a JSON object"]
    errors = _core_checks(doc)
    if level in (ConformanceLevel.EXTENDED, ConformanceLevel.ADNA_NATIVE):
        errors += _extended_checks(doc)
    if level is ConformanceLevel.ADNA_NATIVE:
        from canvas_std import reserved  # A-* checks (spec_conformance_suite §4)

        reserved_block = doc.get("metadata", {}).get("frontmatter", {}).get("_reserved", {})
        errors += reserved.validate_reserved(reserved_block)  # NotImplementedError until E1.4
    return errors


def strip(doc: dict[str, Any]) -> dict[str, Any]:
    """Return ``doc`` with ``metadata.frontmatter._reserved`` removed (the C4 degradation op). E1.5."""
    raise NotImplementedError("strip(): implemented at Keystone E1.5")
