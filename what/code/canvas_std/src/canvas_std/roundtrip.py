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


def diff(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    """Structured topology/position diff for the advisory reverse path. Spec §5 — E1.3."""
    raise NotImplementedError("diff(): implemented at Keystone E1.3")


def merge(source: dict[str, Any], canvas: dict[str, Any], *, strategy: str = "yaml_wins") -> dict[str, Any]:
    """Three-way merge (source semantics win; canvas positions win; conflicts flagged). Spec §5 — E1.3."""
    raise NotImplementedError("merge(): implemented at Keystone E1.3")
