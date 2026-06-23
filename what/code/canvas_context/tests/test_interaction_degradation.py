"""I-D — round-trip-to-baseline (spec_interface_surface.md §8.2 / §9.1).

Stripping the interaction layer leaves a valid canvas: the full ``_reserved`` strip yields a Core-valid baseline
(I-D), and stripping *only* ``_reserved.interaction`` yields a still-aDNA-Native canvas carrying no affordances
(§8.2). Both hold before and after an agent has logged responses.
"""

from __future__ import annotations

import json
from pathlib import Path

from canvas_std import ConformanceLevel, validate

from canvas_context import (
    apply_response,
    is_round_trip_safe,
    load_interaction_surface,
    strip_interaction,
)

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixtures" / "interaction_review.canvas"


def _doc() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_id_full_strip_is_core_valid():
    assert is_round_trip_safe(_doc()) is True  # validate(strip(doc), CORE) == []


def test_strip_interaction_keeps_an_adna_native_canvas_with_no_affordances():
    bare = strip_interaction(_doc())
    # the rest of _reserved is intact → still aDNA-Native valid
    assert validate(bare, ConformanceLevel.ADNA_NATIVE) == []
    # ...but it is now a non-interactive surface (no affordances), still a valid leg-2 load
    surf = load_interaction_surface(bare)
    assert surf.is_interactive() is False
    assert surf.affordances() == []
    assert surf.graph.reading_order()  # leg-2 still works


def test_round_trip_safe_after_responses_logged():
    surf = load_interaction_surface(FIXTURE)
    doc = apply_response(surf, "summarize", "a summary")
    doc = apply_response(doc, "approve", "approve")
    # a fully-answered interactive canvas still degrades to a Core baseline
    assert is_round_trip_safe(doc) is True
    # and stripping only the interaction layer is still aDNA-Native valid
    assert validate(strip_interaction(doc), ConformanceLevel.ADNA_NATIVE) == []
