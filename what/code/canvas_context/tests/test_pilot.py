"""The leg-2 proof (spec_canvas_context_loading §9.1).

Loads a real producer ``.canvas`` (a ``document_generator`` whitepaper, 32 nodes / 23 edges, aDNA-Native) as a
navigable context graph **without rendering** and walks its document order. When this passes with ``canvas_std``
untouched, leg 2 — *canvas as a first-class context object* — is proven.
"""

from __future__ import annotations

import sys
from pathlib import Path

from canvas_context import load_context_graph

HERE = Path(__file__).resolve().parent
PRODUCER = HERE.parent.parent.parent / "production" / "document_generator" / "examples"
WHITEPAPER = PRODUCER / "canvas_standard_whitepaper.canvas"
GRANT = PRODUCER / "grant_proposal.canvas"


def test_pilot_loads_producer_canvas_as_context_without_rendering():
    g = load_context_graph(WHITEPAPER)

    # identity (L4) — resolved from _reserved.context_object; summary absent → exposed as null
    assert g.identity() == {"id": "urn:adna:canvas:whitepaper:canvas-standard", "version": "0.1.0"}
    assert g.summary() is None

    # conformance (L1/L6) — validated at its declared level; the producer's real sync_hash is current
    assert g.conformance() == {"declared": "adna_native", "reached": "adna_native", "stale": False}

    # baseline topology (L2)
    assert len(g.components()) == 32
    assert len(g.relations()) == 23
    assert len(g.panels()) == 8

    # *** the core leg-2 capability: document order recovered WITHOUT rendering (L7 / §6.1) ***
    assert g.reading_order() == ["page0", "page1", "page2", "page3", "page4"]

    # references exposed (L5) — all four are in-vault wikilinks, none transported
    refs = g.refs()
    assert len(refs) == 4
    assert all(r.form == "wikilink" for r in refs)
    assert {r.target for r in refs} == {
        "[[spec_adna_canvas_standard]]",
        "[[spec_component_model]]",
        "[[spec_panel_link_semantics]]",
        "[[adr_003_standard_governance]]",
    }

    # _reserved semantic overlay (L3)
    doc_root = g.component("doc_root")
    assert doc_root.component_class == "panel"
    assert doc_root.semantic_type == "document"

    # surfaces — exactly one canonical (the print/LaTeX face), plus a derived html face
    canonical = [s for s in g.surfaces() if s.role == "canonical"]
    assert len(canonical) == 1 and canonical[0].id == "doc_root"

    # L7 — the file component rides by *reference* (no decoded bytes), and no render libs were imported
    files = [c for c in g.components() if c.node_type == "file"]
    assert files and isinstance(files[0].payload.get("file"), str)
    assert "PIL" not in sys.modules
    assert "cairosvg" not in sys.modules


def test_pilot_second_producer_also_loads_as_context():
    """A second producer output (grant proposal) loads the same way — the loader is not whitepaper-specific."""
    g = load_context_graph(GRANT)
    assert g.identity()["id"] == "urn:adna:canvas:grant:adna-harness-r01"
    assert g.conformance()["reached"] == "adna_native"
    assert g.reading_order()  # non-empty document order
    assert all(r.form == "wikilink" for r in g.refs())


def test_pilot_reading_order_within_a_page_panel():
    """Panel-scoped reading order walks a page's content (the §6 children + reading_order contract)."""
    g = load_context_graph(WHITEPAPER)
    # page1..page4 are content pages; their panel-scoped reading order should be a non-empty ordered walk
    order = g.reading_order("page1")
    assert order  # non-empty
    assert order[0] in {c for c in g.children("page1")} or order[0] == "page1"
