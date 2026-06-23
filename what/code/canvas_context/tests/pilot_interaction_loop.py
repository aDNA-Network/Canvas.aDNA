"""On-disk demo of the leg-3 ``read -> act -> re-read`` loop (Operation Salon P4 POC).

Runs the literal campaign narrative end-to-end against a real file: an operator-annotated canvas is *read* as
context (a leg-2 load, no rendering), an agent *acts* (responds), and the advanced surface is *re-read* from disk.

    PYTHONPATH=<canvas_std>/src:<canvas_context>/src <canvas_std>/.venv/bin/python pilot_interaction_loop.py

This is a demonstration, **not** a runtime: the write-back is a thin ``json.dump`` of the folded view — it is not
the governed round-trip write against the authoritative ``.lattice.yaml`` (that is spec_roundtrip_protocol_v2's
job), and nothing here renders, captures input, or transports.
"""

from __future__ import annotations

import json
from pathlib import Path

from canvas_context import apply_response, load_interaction_surface

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "interaction_review.canvas"
AFTER = HERE / "fixtures" / "interaction_review_after.canvas"


def _state_line(surf) -> str:
    st = surf.surface_state()
    return f"turn={st.turn} open={st.open} complete={surf.turn_complete()}"


def main() -> None:
    # 1. READ — the operator-annotated canvas, loaded as context (no rendering)
    surf = load_interaction_surface(FIXTURE)
    print(f"READ  {FIXTURE.name}: id={surf.graph.identity()['id']}")
    print("      affordances an agent reads:")
    for a in surf.affordances():
        req = " (required)" if a.required else ""
        opts = f" options={a.options}" if a.options else ""
        print(f"        - {a.id}: {a.kind} @ {a.anchor}{opts}{req} — {a.prompt}")
    print(f"      state: {_state_line(surf)}")

    # 2. ACT — the agent responds (append-only fold over the view)
    doc = apply_response(surf, "summarize", "A canvas review request — the Salon P4 interaction POC.")
    doc = apply_response(doc, "approve", "approve")
    doc = apply_response(doc, "margin_note", "Tighten the second paragraph.")
    doc = apply_response(doc, "mark_reviewed", None, participant={"kind": "ai", "id": "mondrian"})
    AFTER.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"ACT   agent logged {len(doc['metadata']['frontmatter']['_reserved']['interaction']['responses'])} "
          f"responses -> wrote {AFTER.name}")

    # 3. RE-READ — load the advanced surface back from disk; the turn has completed
    surf2 = load_interaction_surface(AFTER)
    print(f"REREAD {AFTER.name}: state: {_state_line(surf2)}")
    for r in surf2.responses():
        who = (r.participant or {}).get("kind", "?")
        print(f"        - {r.affordance} = {r.value!r}  [{who}]")
    assert surf2.turn_complete(), "the turn should have completed"
    print("OK    read -> act -> re-read loop closed (turn complete); canvas_std untouched.")


if __name__ == "__main__":
    main()
