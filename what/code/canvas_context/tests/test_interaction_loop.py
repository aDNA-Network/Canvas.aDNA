"""The leg-3 POC proof (spec_interface_surface.md §10.2): the minimal ``read -> act -> re-read`` loop.

An operator-annotated canvas is read as context (leg-2 load, no rendering), an agent responds, and the re-read
surface state advances — the loop closes onto leg 2. When this passes with ``canvas_std`` untouched, leg 3
(interface surface) is *proven by POC*, not just ratified.
"""

from __future__ import annotations

import sys
from pathlib import Path

from canvas_context import apply_response, load_interaction_surface

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "interaction_review.canvas"


def test_read_act_reread_closes_the_loop():
    # --- READ (the surface as context — a leg-2 load, no rendering) ---
    surf = load_interaction_surface(FIXTURE)
    assert surf.graph.identity()["id"] == "urn:adna:canvas:review:salon-p4-demo"
    assert len(surf.affordances()) == 4

    state0 = surf.surface_state()
    assert state0.turn == "t1"
    assert set(state0.open) == {"summarize", "approve"}  # the two required affordances are open
    assert surf.turn_complete() is False

    # --- ACT (an agent responds — a pure append-only fold; the input doc is never mutated) ---
    doc = apply_response(surf, "summarize", "A canvas review request, used as the P4 interaction POC.")
    doc = apply_response(doc, "approve", "approve")                  # choice ∈ options
    doc = apply_response(doc, "margin_note", "Tighten the second paragraph.")
    doc = apply_response(doc, "mark_reviewed", None, participant={"kind": "ai", "id": "mondrian"})  # action ⇒ null

    # the original fixture object is untouched (append-only / view-only)
    assert load_interaction_surface(FIXTURE).responses() == []

    # --- RE-READ (the advanced surface state — itself a valid leg-2 load) ---
    surf2 = load_interaction_surface(doc)
    assert surf2.validate_interaction() == []                       # still I-1/I-2/I-3 conformant
    state1 = surf2.surface_state()
    assert state1.turn == "t1"
    assert state1.open == []                                        # all required affordances answered
    assert surf2.turn_complete() is True                            # the turn completed — the loop closed
    assert {r.affordance for r in surf2.responses()} == {"summarize", "approve", "margin_note", "mark_reviewed"}
    # the re-read is a valid leg-2 graph (the loop closes onto leg 2)
    assert surf2.graph.reading_order()


def test_loop_imports_no_render_libraries():
    """IX4 — the read/act/re-read loop touches no rasterizer (the same firewall the leg-2 pilot asserts)."""
    surf = load_interaction_surface(FIXTURE)
    doc = apply_response(surf, "summarize", "x")
    load_interaction_surface(doc).surface_state()
    assert "PIL" not in sys.modules
    assert "cairosvg" not in sys.modules


def test_apply_response_rejects_nonconformant_act():
    import pytest

    surf = load_interaction_surface(FIXTURE)
    with pytest.raises(ValueError):
        apply_response(surf, "ghost", "x")                          # undeclared affordance (IX5)
    with pytest.raises(ValueError):
        apply_response(surf, "approve", "maybe")                    # choice value ∉ options (IX5)
    with pytest.raises(ValueError):
        apply_response(surf, "mark_reviewed", "done")               # action must carry no value (IX5)


def test_response_log_is_append_only():
    surf = load_interaction_surface(FIXTURE)
    doc1 = apply_response(surf, "summarize", "first")
    doc2 = apply_response(doc1, "approve", "revise")
    log = doc2["metadata"]["frontmatter"]["_reserved"]["interaction"]["responses"]
    # the earlier entry is preserved verbatim — appended-to, never mutated
    assert log[0] == {"affordance": "summarize", "value": "first", "turn": "t1"}
    assert len(log) == 2
