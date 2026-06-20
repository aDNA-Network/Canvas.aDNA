"""E4.2 reflow / auto-pagination (CANVAS-L-002): a content-heavy model page paginates across canvas pages; a
non-overflowing, no-genre document stays byte-identical to E4.1; an unsplittable section is flagged, not silent."""

from __future__ import annotations

import json
from pathlib import Path

from document_generator import layout
from document_generator.consume import build_document
from document_generator.model import Document, Page, Section, load_document

HERE = Path(__file__).resolve().parent
GOLDEN = HERE / "golden"
EXAMPLES = HERE.parent / "examples"


def _reserved(doc):
    return doc["metadata"]["frontmatter"]["_reserved"]


def _pages(doc):
    return [n["id"] for n in doc["nodes"] if n["type"] == "group" and n["id"].startswith("page")]


def test_long_model_page_splits_across_canvas_pages(grant_doc):
    d = load_document(EXAMPLES / "grant_proposal.yaml")
    assert len(d.pages) == 1               # a single model page...
    assert len(_pages(grant_doc)) >= 3     # ...reflowed across several canvas pages (CANVAS-L-002 closed)


def test_no_emitted_page_overflows_content_height():
    d = load_document(EXAMPLES / "grant_proposal.yaml")
    for pf in (pf for pg in d.pages for pf in layout.paginate(pg)):
        used = sum(layout.section_height(sf.section) for sf in pf.fragments)
        assert used <= layout.CONTENT_H or any(sf.oversized for sf in pf.fragments)


def test_non_overflowing_doc_byte_identical_to_e41_golden():
    # The strongest regression guard: reflow + conditional emission must leave a non-overflowing, no-genre document
    # byte-identical to the E4.1 layout (the golden was captured from pre-E4.2 code).
    built = build_document(load_document(GOLDEN / "document_small.yaml"))
    golden = json.loads((GOLDEN / "document_small.canvas").read_text())
    assert built == golden


def test_reading_order_is_page_scoped(grant_doc):
    pl = _reserved(grant_doc)["panel_link"]
    ro = [eid for eid, m in pl["edges"].items() if m["kind"] == "reading_order"]
    assert ro and all(eid.startswith("page") for eid in ro)  # sections stay atomic -> no cross-page reading_order


def test_oversized_section_is_flagged_not_silent():
    big = " ".join(["overflow"] * 4000)  # a single section taller than a whole page
    d = Document(title="big", id="urn:adna:canvas:doc:big", version="0.1.0",
                 pages=[Page(sections=[Section(heading="Huge", body=big)])])
    doc = build_document(d)
    assert any(e.get("qualities", {}).get("layout_note") == "oversized_overflow"
               for e in _reserved(doc)["component_types"].values())
