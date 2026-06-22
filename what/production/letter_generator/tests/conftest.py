"""Shared fixtures — a realistic ``Letter`` + the default built canvas doc (mirrors diagram_generator's conftest)."""

from __future__ import annotations

import pytest

from letter_generator.consume import build_letter
from letter_generator.model import Letter


@pytest.fixture
def letter() -> Letter:
    return Letter(
        title="Cover letter — Canvas.aDNA",
        id="urn:adna:canvas:letter:cover",
        version="0.1.0",
        refs=("[[spec_adna_canvas_standard]]", "[[adr_004_production_code_layout]]"),
        sender=("Piet Mondrian", "aDNA Labs", "mondrian@adna.example"),
        date="2026-06-22",
        recipient=("Hiring Committee", "Bauhaus Foundation", "Dessau, Germany"),
        salutation="Dear Committee,",
        body=(
            "I write to apply for the role of standard-bearer for two-dimensional output.",
            "My method reduces any page to a disciplined grid of typed components on a canvas.",
            "I would welcome the chance to discuss how that grammar serves your archive.",
        ),
        closing="Sincerely,",
        signature=("Piet Mondrian", "Standard-bearer"),
    )


@pytest.fixture
def doc(letter: Letter) -> dict:
    return build_letter(letter)
