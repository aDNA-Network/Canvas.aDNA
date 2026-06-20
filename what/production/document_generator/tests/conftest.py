"""Shared fixtures — a deterministic 2-page document exercising every block type + its built canvas doc, plus the
two E4.2 worked examples (whitepaper genre + the reflow-forcing grant)."""

from __future__ import annotations

from pathlib import Path

import pytest

from document_generator.consume import build_document
from document_generator.model import Block, Document, Page, Section, Source, load_document

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


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
def n_pages(doc: dict) -> int:
    # The count of *emitted* canvas pages (>= model pages once E4.2 reflow paginates an overflowing model page).
    return sum(1 for n in doc["nodes"] if n["type"] == "group" and n["id"].startswith("page"))


@pytest.fixture
def whitepaper_doc() -> dict:
    """The whitepaper example (genre: whitepaper) — the contract-bearing dog-food document."""
    return build_document(load_document(EXAMPLES / "canvas_standard_whitepaper.yaml"))


@pytest.fixture
def grant_doc() -> dict:
    """The grant example (genre: grant) — one content-heavy model page that reflows across several canvas pages."""
    return build_document(load_document(EXAMPLES / "grant_proposal.yaml"))
