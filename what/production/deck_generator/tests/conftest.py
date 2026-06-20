"""Shared fixtures — a deterministic deck exercising every slide type + its built canvas doc."""

from __future__ import annotations

import pytest

from deck_generator.consume import build_deck
from deck_generator.model import DeckInput, Slide


@pytest.fixture
def deck() -> DeckInput:
    return DeckInput(
        title="Test Deck",
        id="urn:adna:canvas:deck:test",
        version="0.1.0",
        refs=["[[spec_adna_canvas_standard]]"],
        slides=[
            Slide(type="title", title="Hello", subtitle="A test deck"),
            Slide(type="content", title="Points", body="Some body text.", bullets=["one", "two", "three"]),
            Slide(type="section", title="Part II"),
            Slide(type="image", title="A figure", image="assets/fig.png", caption="A caption."),
            Slide(type="image", title="External", image="https://example.org/x.png"),
            Slide(type="table", title="Data", table={"headers": ["A", "B"], "rows": [["1", "2"], ["3", "4"]]}),
            Slide(type="quote", title="End", body="Be lean.", attribution="Mondrian"),
        ],
    )


@pytest.fixture
def doc(deck: DeckInput) -> dict:
    return build_deck(deck)


@pytest.fixture
def n_slides(deck: DeckInput) -> int:
    return len(deck.slides)
