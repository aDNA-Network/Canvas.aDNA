#!/usr/bin/env python3
"""Operation Keystone E3.3 — deterministic parity check (Approach A).

Proves the E3.2 constants-only shim is OUTPUT-NEUTRAL for CanvasForge, with no LLM/API:

  1. Rebuilds the Wilhelm parity deck through the (shimmed) canvas_core generation path
     (PresentationBuilder -> CanvasBuilder, exercising TYPE_MAPPING / EDGE_TYPE_MAPPING / VALID_*),
     normalizes the random `secrets.token_hex` IDs to a canonical order, and SHA-256s the
     structural essence. Run shim-on vs shim-off => identical SHA proves the shim changes nothing.
  2. Loads the committed Issue-01 comic canvas and verifies every node value is accepted by the
     federated CanvasBuilder.VALID_* frozensets (exercises the federated floor on the comic path
     without invoking the comic build's Gemini image-gen).

Writes a JSON capture to argv[1]. Compare captures across runs; the load-bearing field is
`deck_norm_sha256`. NEVER touches baseline_vr_scores.json.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

CF_CODE = Path("/Users/stanley/aDNA/CanvasForge.aDNA/what/code")
PARITY_DECK = Path("/Users/stanley/aDNA/CanvasForge.aDNA/what/artifacts/parity_deck")
COMIC_CANVAS = Path("/Users/stanley/aDNA/CanvasForge.aDNA/what/artifacts/parity_comic/comic_parity.canvas")

sys.path.insert(0, str(CF_CODE))
sys.path.insert(0, str(PARITY_DECK))

from canvas_core.core import CanvasBuilder  # noqa: E402  (federated floor via the shim)
import build_wilhelm_parity as bwp  # noqa: E402


def normalize(canvas: dict) -> dict:
    """Canonicalize a canvas modulo random node/edge IDs and volatile top-level metadata.

    Keeps exactly what the federated floor affects: node type/geometry/color/styleAttributes and
    edge endpoints/sides/label/styleAttributes. Drops `id` (random) and all top-level keys
    (metadata, _reserved sync hashes, timestamps).
    """
    nodes = canvas.get("nodes", []) or []
    edges = canvas.get("edges", []) or []

    def node_body(n: dict) -> dict:
        return {k: v for k, v in n.items() if k != "id"}

    sorted_nodes = sorted(nodes, key=lambda n: json.dumps(node_body(n), sort_keys=True))
    idmap: dict[str, str] = {}
    norm_nodes = []
    for i, n in enumerate(sorted_nodes):
        idmap[n.get("id")] = f"n{i}"
        norm_nodes.append(node_body(n))

    def edge_body(e: dict) -> dict:
        body = {k: v for k, v in e.items() if k not in ("id", "fromNode", "toNode")}
        body["fromNode"] = idmap.get(e.get("fromNode"), e.get("fromNode"))
        body["toNode"] = idmap.get(e.get("toNode"), e.get("toNode"))
        return body

    norm_edges = sorted((edge_body(e) for e in edges), key=lambda b: json.dumps(b, sort_keys=True))
    return {"nodes": norm_nodes, "edges": norm_edges}


def fingerprint(canvas: dict) -> dict:
    colors, shapes, ntypes = set(), set(), set()
    for n in canvas.get("nodes", []) or []:
        ntypes.add(n.get("type"))
        if n.get("color") is not None:
            colors.add(str(n.get("color")))
        sa = n.get("styleAttributes") or {}
        if sa.get("shape") is not None:
            shapes.add(str(sa.get("shape")))
    return {
        "node_types": sorted(t for t in ntypes if t is not None),
        "colors": sorted(colors),
        "shapes": sorted(shapes),
    }


def federated_floor_rejects(canvas: dict) -> list:
    """Values the federated CanvasBuilder.VALID_* frozensets would reject (expect [])."""
    bad = []
    for n in canvas.get("nodes", []) or []:
        if n.get("type") not in CanvasBuilder.VALID_NODE_TYPES:
            bad.append(["node_type", n.get("id"), n.get("type")])
        c = n.get("color")
        if c is not None and c not in CanvasBuilder.VALID_COLORS:
            bad.append(["color", n.get("id"), c])
        sa = n.get("styleAttributes") or {}
        sh = sa.get("shape")
        if sh is not None and sh not in CanvasBuilder.VALID_SHAPES:
            bad.append(["shape", n.get("id"), sh])
    return bad


def main() -> None:
    out = Path(sys.argv[1])

    deck = bwp.build_wilhelm().build()  # full generation path (shimmed floor)
    deck_norm = normalize(deck)
    deck_sha = hashlib.sha256(json.dumps(deck_norm, sort_keys=True).encode()).hexdigest()

    comic = json.loads(COMIC_CANVAS.read_text())

    capture = {
        "deck_norm_sha256": deck_sha,
        "deck_nodes": len(deck.get("nodes", []) or []),
        "deck_edges": len(deck.get("edges", []) or []),
        "deck_fingerprint": fingerprint(deck),
        "deck_floor_rejects": federated_floor_rejects(deck),
        "comic_nodes": len(comic.get("nodes", []) or []),
        "comic_fingerprint": fingerprint(comic),
        "comic_floor_rejects": federated_floor_rejects(comic),
    }
    out.write_text(json.dumps(capture, indent=2, sort_keys=True))
    print(f"deck_norm_sha256={deck_sha}")
    print(f"deck nodes={capture['deck_nodes']} edges={capture['deck_edges']} "
          f"rejects={len(capture['deck_floor_rejects'])}")
    print(f"comic nodes={capture['comic_nodes']} rejects={len(capture['comic_floor_rejects'])}")


if __name__ == "__main__":
    main()
