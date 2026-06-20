"""Shared fixtures — a small deterministic brief + its built canvas doc."""

from __future__ import annotations

import pytest

from brief_consumer.consume import build_brief
from brief_consumer.model import BriefInput, Section, Source


@pytest.fixture
def brief() -> BriefInput:
    return BriefInput(
        title="Test Brief",
        id="urn:adna:canvas:brief:test",
        version="0.1.0",
        refs=["[[spec_adna_canvas_standard]]"],
        sections=[
            Section(
                heading="Alpha",
                body="First section body text, long enough to wrap across a couple of estimated lines.",
                sources=[Source(label="JSON Canvas", url="https://jsoncanvas.org")],
            ),
            Section(heading="Beta", body="Second section body.\nWith an explicit second line.", sources=[]),
            Section(
                heading="Gamma",
                body="Third.",
                sources=[
                    Source(label="x", url="https://example.org/x"),
                    Source(label="y", url="https://example.org/y"),
                ],
            ),
        ],
    )


@pytest.fixture
def doc(brief: BriefInput) -> dict:
    return build_brief(brief)
