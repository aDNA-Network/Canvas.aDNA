"""Generator for ``review_request.source.json`` — the authoritative SOURCE paired with ``interaction_review.canvas``.

Builds a ``.lattice``-shaped source (the ``canvas_std.roundtrip`` source contract + the ``spec_roundtrip_protocol_v2``
§6 source-only fields) whose **topology matches the view fixture**, so ``compute_sync_hash(source)`` equals the view's
stored ``_reserved.sync.sync_hash`` — the staleness gate's baseline (Armature P1). The source carries the source-only
§6 fields (``execution`` / ``fair`` / ``federation`` / per-node ``config``) that the canvas view drops. The topology is
**derived from the view** so the two can never drift. Re-run to regenerate (provenance, the producer way):

    PYTHONPATH=<canvas_std>/src:<canvas_context>/src <canvas_std>/.venv/bin/python _build_review_source.py
"""

from __future__ import annotations

import json
from pathlib import Path

from canvas_std import compute_sync_hash

HERE = Path(__file__).resolve().parent
VIEW = HERE / "interaction_review.canvas"
OUT = HERE / "review_request.source.json"

# §6 source-only per-node config — NOT recoverable from the canvas view; the reverse merge MUST restore it.
# (No custom semantic_type here: the view carries no color/shape that round-trips to one, so a custom value would
# read as a three-way-merge conflict — out of scope for the P1 happy path; conflict-flagging is merge()'s own contract.)
_CONFIG = {
    "decision_box": {"decision_policy": "operator_required"},
    "status_box": {"closes_turn": True},
}


def build(view: dict) -> dict:
    nodes = []
    for n in view.get("nodes", []):
        node: dict = {"id": n["id"], "type": n.get("type", "text")}
        if "text" in n:
            node["text"] = n["text"]
        if n["id"] in _CONFIG:
            node["config"] = _CONFIG[n["id"]]
        nodes.append(node)
    edges = [
        {"id": e["id"], "fromNode": e["fromNode"], "toNode": e["toNode"]}
        for e in view.get("edges", [])
        if isinstance(e, dict)
    ]
    return {
        "name": "review_request",
        "version": "0.1.0",
        "lattice_type": "context_graph",
        "execution": {"mode": "workflow", "runtime": "local", "tier": "L1"},  # §6 lossy (source-only)
        "nodes": nodes,
        "edges": edges,
        "fair": {  # §6 lossy (source-only)
            "license": "MIT",
            "creators": ["Canvas.aDNA / Mondrian"],
            "keywords": ["canvas", "interaction", "review", "armature"],
            "provenance": "Authoritative source paired with interaction_review.canvas — Operation Armature P1.",
        },
        "federation": {  # §6 lossy (source-only)
            "source_vault": "Canvas.aDNA",
            "version": "2.0.2",
            "version_policy": "minor",
        },
    }


def main() -> None:
    view = json.loads(VIEW.read_text(encoding="utf-8"))
    source = build(view)
    stored = view["metadata"]["frontmatter"]["_reserved"]["sync"]["sync_hash"]
    got = compute_sync_hash(source)
    assert got == stored, f"source topology hash {got} != view stored {stored} (topology must match for the gate)"
    OUT.write_text(json.dumps(source, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT.name} — sync_hash {got} matches the view (staleness baseline aligned)")


if __name__ == "__main__":
    main()
