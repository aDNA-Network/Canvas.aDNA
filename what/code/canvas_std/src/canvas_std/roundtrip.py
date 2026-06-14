"""Round-trip Protocol v2 — authoritative-source <-> view.

E1.2 implements ``compute_sync_hash``, ``to_canvas`` (=legacy ``build``, forward source->view), and
``from_canvas`` (=legacy ``read_back``, advisory view->source draft). ``diff``/``merge`` are E1.3.

Authority model (spec_roundtrip_protocol_v2 §2): the source owns topology + semantics; the view owns positions +
visual styling. Forward is deterministic; reverse is **advisory** (produces a draft for human review). **Layout is
producer-side** (inventory §B) — ``to_canvas`` emits default geometry, not a real layout.

Source contract (minimal): ``{name?, version?, nodes:[{id, semantic_type?, type?, text?/file?/url?/label?,
x?,y?,width?,height?}], edges:[{id, fromNode, toNode, fromSide?, toSide?, semantic_type?}]}``.
"""

from __future__ import annotations

import hashlib
from typing import Any

from canvas_std import schema

DEFAULT_WIDTH = 240
DEFAULT_HEIGHT = 80

# Reverse of the lattice node profile {color,shape,node_type} -> semantic_type (best-effort, for from_canvas).
_LATTICE_REVERSE = {
    (v["color"], v["shape"], v["node_type"]): k for k, v in schema.TYPE_MAPPING.items()
}


def compute_sync_hash(doc: dict[str, Any]) -> str:
    """16-hex SHA-256 over the topology: sorted node ids + sorted ``fromNode->toNode`` pairs (spec §3)."""
    node_ids = sorted(str(n["id"]) for n in doc.get("nodes", []) if isinstance(n, dict) and "id" in n)
    edges = sorted(
        f"{e.get('fromNode')}->{e.get('toNode')}" for e in doc.get("edges", []) if isinstance(e, dict)
    )
    payload = "".join(node_ids) + "" + "".join(edges)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def to_canvas(source: dict[str, Any]) -> dict[str, Any]:
    """Forward: build a conformant ``.canvas`` view from an authoritative source (deterministic).

    Applies the ``lattice`` semantic profile (color/shape/node_type), sets explicit ``toEnd``, injects
    ``_reserved.sync``. Geometry defaults (real layout is producer-side). (legacy: ``build``)
    """
    nodes: list[dict[str, Any]] = []
    for sn in source.get("nodes", []):
        st = sn.get("semantic_type")
        prof = schema.TYPE_MAPPING.get(st, {}) if st else {}
        node_type = sn.get("type") or prof.get("node_type") or "text"
        node: dict[str, Any] = {
            "id": sn["id"],
            "type": node_type,
            "x": int(sn.get("x", 0)),
            "y": int(sn.get("y", 0)),
            "width": int(sn.get("width", DEFAULT_WIDTH)),
            "height": int(sn.get("height", DEFAULT_HEIGHT)),
        }
        for payload_key in ("text", "file", "url", "label"):
            if payload_key in sn:
                node[payload_key] = sn[payload_key]
        if prof.get("color") is not None:
            node["color"] = prof["color"]
        if prof.get("shape") is not None:
            node["styleAttributes"] = {"shape": prof["shape"]}
        nodes.append(node)

    edges: list[dict[str, Any]] = []
    for se in source.get("edges", []):
        st = se.get("semantic_type")
        eprof = schema.EDGE_TYPE_MAPPING.get(st, {}) if st else {}
        edge: dict[str, Any] = {
            "id": se["id"],
            "fromNode": se["fromNode"],
            "fromSide": se.get("fromSide", "bottom"),
            "toNode": se["toNode"],
            "toSide": se.get("toSide", "top"),
            "toEnd": eprof.get("to_end", "arrow") or "arrow",
        }
        if eprof.get("from_end") is not None:
            edge["fromEnd"] = eprof["from_end"]
        sa = {}
        if eprof.get("path_style") is not None:
            sa["path"] = eprof["path_style"]
        if eprof.get("arrow") is not None:
            sa["arrow"] = eprof["arrow"]
        if sa:
            edge["styleAttributes"] = sa
        edges.append(edge)

    canvas: dict[str, Any] = {"nodes": nodes, "edges": edges}
    canvas["metadata"] = {
        "frontmatter": {
            "_reserved": {
                "sync": {
                    "sync_hash": compute_sync_hash(source),
                    "source_name": source.get("name"),
                    "source_version": source.get("version"),
                }
            }
        }
    }
    return canvas


def from_canvas(canvas: dict[str, Any]) -> dict[str, Any]:
    """Reverse (advisory): extract a source DRAFT from a view. Drops positions + visual styling (view-authority);
    recovers semantic types best-effort from the lattice profile. Marked ``_draft: True`` — human review required.
    (legacy: ``read_back``)
    """
    sync = canvas.get("metadata", {}).get("frontmatter", {}).get("_reserved", {}).get("sync", {})
    src_nodes: list[dict[str, Any]] = []
    for n in canvas.get("nodes", []):
        if not isinstance(n, dict):
            continue
        key = (n.get("color"), (n.get("styleAttributes") or {}).get("shape"), n.get("type"))
        st = _LATTICE_REVERSE.get(key)
        sn: dict[str, Any] = {"id": n.get("id"), "type": n.get("type")}
        if st:
            sn["semantic_type"] = st
        for payload_key in ("text", "file", "url", "label"):
            if payload_key in n:
                sn[payload_key] = n[payload_key]
        src_nodes.append(sn)

    src_edges = [
        {
            "id": e.get("id"),
            "fromNode": e.get("fromNode"),
            "fromSide": e.get("fromSide"),
            "toNode": e.get("toNode"),
            "toSide": e.get("toSide"),
        }
        for e in canvas.get("edges", [])
        if isinstance(e, dict)
    ]
    return {
        "_draft": True,
        "name": sync.get("source_name"),
        "version": sync.get("source_version"),
        "nodes": src_nodes,
        "edges": src_edges,
    }


def _by_id(items: list[Any]) -> dict[str, dict[str, Any]]:
    return {i["id"]: i for i in items if isinstance(i, dict) and "id" in i}


def _geom(n: dict[str, Any]) -> tuple:
    return (n.get("x"), n.get("y"), n.get("width"), n.get("height"))


def diff(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    """Structured topology/position diff a→b (spec §5). Keys: nodes_added/removed/modified, positions_changed,
    edges_added/removed, topology_changed (bool)."""
    an, bn = _by_id(a.get("nodes", [])), _by_id(b.get("nodes", []))
    ae, be = _by_id(a.get("edges", [])), _by_id(b.get("edges", []))
    common = an.keys() & bn.keys()
    nodes_added = sorted(bn.keys() - an.keys())
    nodes_removed = sorted(an.keys() - bn.keys())
    nodes_modified = sorted(i for i in common if an[i] != bn[i])
    positions_changed = sorted(i for i in common if _geom(an[i]) != _geom(bn[i]))
    edges_added = sorted(be.keys() - ae.keys())
    edges_removed = sorted(ae.keys() - be.keys())
    return {
        "nodes_added": nodes_added,
        "nodes_removed": nodes_removed,
        "nodes_modified": nodes_modified,
        "positions_changed": positions_changed,
        "edges_added": edges_added,
        "edges_removed": edges_removed,
        "topology_changed": bool(nodes_added or nodes_removed or edges_added or edges_removed),
    }


def preserve_positions(target: dict[str, Any], reference: dict[str, Any]) -> dict[str, Any]:
    """Copy x/y/width/height from ``reference`` onto matching node ids in ``target`` (G1). Mutates + returns
    ``target`` — used after forward regen so existing positions survive (spec §4)."""
    ref = _by_id(reference.get("nodes", []))
    for n in target.get("nodes", []):
        r = ref.get(n.get("id"))
        if r:
            for f in ("x", "y", "width", "height"):
                if f in r:
                    n[f] = r[f]
    return target


def merge(source: dict[str, Any], canvas: dict[str, Any], *, strategy: str = "yaml_wins") -> dict[str, Any]:
    """Three-way merge of an authoritative ``source`` with an edited ``canvas`` view (spec §5).

    The canvas defines the current topology (added/removed nodes + edges) and owns positions; the source owns
    semantics. ``yaml_wins`` (default): on a semantic conflict the source value is kept; ``canvas_wins``: the
    canvas value is kept. Either way the conflict is flagged. Returns a merged source draft (``_merged: true``).
    """
    if strategy not in ("yaml_wins", "canvas_wins"):
        raise ValueError(f"merge: unknown strategy {strategy!r}")
    src_nodes = _by_id(source.get("nodes", []))
    canvas_draft = from_canvas(canvas)  # canvas -> source-like topology + recovered semantics
    cv_nodes = {n["id"]: n for n in canvas_draft["nodes"] if n.get("id")}
    cv_pos = _by_id(canvas.get("nodes", []))

    merged_nodes: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    for nid, cv in cv_nodes.items():  # canvas node set is authoritative for topology
        if nid in src_nodes:
            node = dict(src_nodes[nid])
            s_st, c_st = src_nodes[nid].get("semantic_type"), cv.get("semantic_type")
            if s_st and c_st and s_st != c_st:
                conflicts.append({"id": nid, "field": "semantic_type", "source": s_st, "canvas": c_st})
                chosen = s_st if strategy == "yaml_wins" else c_st
            else:
                chosen = s_st or c_st
            if chosen:
                node["semantic_type"] = chosen
        else:
            node = dict(cv)  # new node introduced on the canvas → draft
        for f in ("x", "y", "width", "height"):  # positions: canvas authority
            if nid in cv_pos and f in cv_pos[nid]:
                node[f] = cv_pos[nid][f]
        merged_nodes.append(node)

    return {
        "_merged": True,
        "strategy": strategy,
        "name": source.get("name"),
        "version": source.get("version"),
        "nodes": merged_nodes,
        "edges": canvas_draft["edges"],
        "conflicts": conflicts,
    }
