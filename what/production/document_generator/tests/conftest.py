"""Shared fixtures — a deterministic 2-page document exercising every block type + its built canvas doc."""

from __future__ import annotations

import pytest

from document_generator.consume import build_document
from document_generator.model import Block, Document, Page, Section, Source


@pytest.fixture
def document() -> Document:
    return Document(
        title="Test Whitepaper",
        id="urn:adna:canvas:doc:test",
        version="0.1.0",
        refs=["[[spec_adna_canvas_standard]]"],
        pages=[
            Page(sections=[
                Section(
                    heading="Abstract",
                    body="A short abstract about the Standard.",
                    blocks=[Block(type="quote", text="Be lean.", attribution="Mondrian")],
                    sources=[Source(label="JSON Canvas", url="https://jsoncanvas.org/spec/1.0/")],
                ),
                Section(
                    heading="Grammar",
                    body="The component grammar and conformance levels.",
                    blocks=[
                        Block(type="table", table={"headers": ["Level", "Adds"],
                                                   "rows": [["Core", "KEEP"], ["Extended", "style"]]}),
                        Block(type="figure", image="assets/fig.png", caption="A local figure."),
                    ],
                ),
            ]),
            Page(sections=[
                Section(
                    heading="Practice",
                    body="The reference library in practice.",
                    blocks=[
                        Block(type="code", lang="python", code="assert validate(doc, ADNA_NATIVE) == []"),
                        Block(type="figure", image="https://example.org/x.png", caption="An external figure."),
                    ],
                    sources=[Source(label="ref", url="https://example.org/ref")],
                ),
                Section(
                    heading="Governance",
                    body="The LIP process on a semver line.",
                    blocks=[Block(type="list", items=["MAJOR", "MINOR", "PATCH"])],
                ),
            ]),
        ],
    )


@pytest.fixture
def doc(document: Document) -> dict:
    return build_document(document)


@pytest.fixture
def n_pages(document: Document) -> int:
    return len(document.pages)
