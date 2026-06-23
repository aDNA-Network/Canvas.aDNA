"""Generator for ``interaction_review.canvas`` — the Salon P4 interaction-bearing golden fixture.

Builds a small, valid aDNA-Native canvas (a "review request") carrying a ``_reserved.interaction`` overlay that
declares **one affordance of each of the four kinds** (input / choice / annotation / action), anchored to real node
ids — one via a ``panel_link.anchors`` label (exercising both binding forms + ``validate_anchors``). It computes the
real topology ``sync_hash``, asserts ``canvas_std`` aDNA-Native validity **and** I-1/I-2/I-3 conformance, then writes
the golden. Re-run to regenerate (provenance, the way producers emit their examples):

    PYTHONPATH=<canvas_std>/src:<canvas_context>/src <canvas_std>/.venv/bin/python _build_interaction_review.py
"""

from __future__ import annotations

import json
from pathlib import Path

from canvas_std import ConformanceLevel, compute_sync_hash, validate

from canvas_context.interaction import validate_interaction_block

OUT = Path(__file__).resolve().parent / "interaction_review.canvas"


def _text(nid: str, x: int, y: int, h: int, text: str, *, start: bool = False) -> dict:
    node = {"id": nid, "type": "text", "x": x, "y": y, "width": 560, "height": h, "text": text}
    if start:
        node["isStartNode"] = True
    return node


def _ro_edge(eid: str, frm: str, to: str) -> dict:
    return {"id": eid, "fromNode": frm, "fromSide": "bottom", "toNode": to, "toSide": "top", "toEnd": "arrow"}


def build() -> dict:
    nodes = [
        {"id": "review_root", "type": "group", "x": 0, "y": 0, "width": 600, "height": 520, "label": "Review"},
        _text("summary_box", 20, 20, 80, "Summary: (pending)", start=True),
        _text("decision_box", 20, 120, 80, "Decision: pending"),
        _text("body", 20, 220, 140, "Draft body under review. See [[spec_interface_surface]]."),
        _text("status_box", 20, 380, 80, "Status: open"),
    ]
    edges = [
        _ro_edge("e1", "summary_box", "decision_box"),
        _ro_edge("e2", "decision_box", "body"),
        _ro_edge("e3", "body", "status_box"),
    ]
    doc = {
        "nodes": nodes,
        "edges": edges,
        "metadata": {
            "frontmatter": {
                "_reserved": {
                    "adna_version": "2.0.2",
                    "conformance_level": "adna_native",
                    "sync": {"sync_hash": "0" * 16},  # patched below
                    "component_types": {
                        "review_root": {"class": "panel", "degrades_to": "group"},
                        "summary_box": {"class": "text", "degrades_to": "text"},
                        "decision_box": {"class": "text", "degrades_to": "text"},
                        "body": {"class": "text", "degrades_to": "text"},
                        "status_box": {"class": "text", "degrades_to": "text"},
                    },
                    "panel_link": {
                        "regions": {"review_root": {"flow": "vertical", "pagination": "none"}},
                        "edges": {
                            "e1": {"kind": "reading_order"},
                            "e2": {"kind": "reading_order"},
                            "e3": {"kind": "reading_order"},
                        },
                        "surfaces": [{"id": "review_root", "role": "canonical", "surface": "review"}],
                        # a label -> node-id anchor map; 'status_marker' is the label-form binding for the action.
                        "anchors": {"status_marker": "status_box"},
                    },
                    "context_object": {
                        "id": "urn:adna:canvas:review:salon-p4-demo",
                        "version": "0.1.0",
                        "summary": "A canvas review request — the Operation Salon P4 interaction-loop POC fixture.",
                        "refs": [],
                    },
                    # leg-3 additive overlay: one affordance of each kind; turn t1 open on the two required ones.
                    "interaction": {
                        "interaction_version": "1.0",
                        "affordances": {
                            "summarize": {
                                "anchor": "summary_box",
                                "kind": "input",
                                "prompt": "Summarize this surface in one line.",
                                "required": True,
                            },
                            "approve": {
                                "anchor": "decision_box",
                                "kind": "choice",
                                "prompt": "Approve, revise, or reject?",
                                "options": ["approve", "revise", "reject"],
                                "required": True,
                            },
                            "margin_note": {
                                "anchor": "body",
                                "kind": "annotation",
                                "prompt": "Add a margin note on the body.",
                                "required": False,
                            },
                            "mark_reviewed": {
                                "anchor": "status_marker",  # label form -> status_box (panel_link.anchors)
                                "kind": "action",
                                "prompt": "Mark this surface reviewed.",
                                "required": False,
                            },
                        },
                        "responses": [],
                        "state": {"turn": "t1", "open": ["summarize", "approve"]},
                    },
                }
            }
        },
    }
    doc["metadata"]["frontmatter"]["_reserved"]["sync"]["sync_hash"] = compute_sync_hash(doc)
    return doc


def main() -> None:
    doc = build()
    core_errors = validate(doc, ConformanceLevel.ADNA_NATIVE)
    assert core_errors == [], f"fixture is not aDNA-Native valid: {core_errors}"
    ix_errors = validate_interaction_block(doc)
    assert ix_errors == [], f"fixture interaction layer not I-1/I-2/I-3 conformant: {ix_errors}"
    OUT.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} — adna_native [OK], interaction conformant, sync_hash "
          f"{doc['metadata']['frontmatter']['_reserved']['sync']['sync_hash']}")


if __name__ == "__main__":
    main()
