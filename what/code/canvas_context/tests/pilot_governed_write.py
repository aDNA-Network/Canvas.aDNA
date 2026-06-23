"""On-disk demo of the leg-3 GOVERNED write loop (Operation Armature P1).

The runtime narrative against real files: an operator-annotated canvas (the **view**) is *read* as context (a leg-2
load, no rendering), an agent *acts* (responds), and each act is *reconciled* to the authoritative source (the
``.lattice.yaml``, here its parsed ``.source.json`` pair) via the **advisory** reverse path — emitting a **reviewed
source DRAFT**, never a silent write. Unlike the Salon P4 POC (a thin ``json.dump`` of the folded view), this closes
the governed write: a draft + a response review-payload + a staleness verdict, with the authoritative source left
**byte-unchanged** (``spec_roundtrip_protocol_v2`` §1.2).

    PYTHONPATH=<canvas_std>/src:<canvas_context>/src <canvas_std>/.venv/bin/python pilot_governed_write.py
"""

from __future__ import annotations

import json
from pathlib import Path

from canvas_context import governed_apply, load_interaction_surface, write_source_draft

HERE = Path(__file__).resolve().parent
VIEW = HERE / "fixtures" / "interaction_review.canvas"
SOURCE = HERE / "fixtures" / "review_request.source.json"
DRAFT = HERE / "fixtures" / "review_request.source.draft.json"


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    source_bytes = SOURCE.read_bytes()  # the authoritative source, before — must be untouched at the end

    # 1. READ — the operator-annotated view, as context (leg-2 load, no rendering)
    surf = load_interaction_surface(VIEW)
    print(f"READ   {VIEW.name}: id={surf.graph.identity()['id']} — {len(surf.affordances())} affordances")
    print(f"       authoritative source: {SOURCE.name} ({len(source['nodes'])} nodes, {len(source['edges'])} edges)")

    # 2. ACT — the agent responds; each act is GOVERNED (advance the view, append-only, THEN reconcile to a draft)
    view = json.loads(VIEW.read_text(encoding="utf-8"))
    recon = None
    for aff, val in (
        ("summarize", "A canvas review request — the Armature P1 governed-write demo."),
        ("approve", "approve"),
    ):
        view, recon = governed_apply(view, source, aff, val)
        print(f"ACT    {aff} = {val!r}  ->  reconciled (stale={recon.stale}, conflicts={len(recon.conflicts)})")

    # 3. WRITE — the reviewed source DRAFT to a SEPARATE artifact; the authoritative source is never written
    path = write_source_draft(recon, DRAFT, reviewed_by="stanley")
    print(f"DRAFT  wrote {path.name} — _draft + requires_review + reviewed_by=stanley; "
          f"{len(recon.responses)} responses surfaced for review (not written into the source)")

    # 4. PROVE — the authoritative source is byte-for-byte unchanged (§1.2 — the governed write stays advisory)
    assert SOURCE.read_bytes() == source_bytes, "the authoritative source must never be written by the runtime"
    print(f"OK     authoritative {SOURCE.name} byte-unchanged; the governed write stayed advisory. canvas_std untouched.")


if __name__ == "__main__":
    main()
