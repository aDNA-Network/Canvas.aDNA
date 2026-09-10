"""The leg-2 proof (spec_canvas_context_loading §9.1).

Loads a real producer ``.canvas`` (a ``document_generator`` whitepaper, aDNA-Native) as a navigable context
graph **without rendering** and walks its document order. When this passes with ``canvas_std`` untouched,
leg 2 — *canvas as a first-class context object* — is proven.

⚠ **The fixture is generated, so its size is not a fact about the loader** (F-P5-3, Blueprint P5). This test
pinned the whitepaper's literal node/edge/panel counts (32/23/8) from Salon. Blueprint P2c legitimately
regenerated the example — section-atomic pagination split it 5 pages → 6, taking it to 35/25/9 — and the
assertions went stale the same day. Nobody noticed for two days across three phase closes, because
``canvas_context`` had quietly dropped out of the standing gate set and every one of those closes reported
green without running it.

So the structural counts below are now **derived from the file**: they assert what is actually a claim about
the loader — that it exposes *every* node and edge, losing nothing — and they survive the next regeneration.
The document order stays a literal, because that one *is* the leg-2 claim and a change to it should fail.
"""

from __future__ import annotations

import json
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

    # baseline topology (L2) — derived from the file, so a regenerated example cannot rot this
    # into a false red (or, worse, a false green). The claim is that the loader is lossless.
    doc = json.loads(WHITEPAPER.read_text(encoding="utf-8"))
    assert len(g.components()) == len(doc["nodes"])
    assert len(g.relations()) == len(doc["edges"])
    assert len(g.panels()) == sum(1 for n in doc["nodes"] if n.get("type") == "group")

    # *** the core leg-2 capability: document order recovered WITHOUT rendering (L7 / §6.1) ***
    # Literal on purpose — this is the leg-2 claim itself, not a property of the fixture's size.
    # (P2c's pagination split took this from 5 pages to 6; a further change should fail here.)
    assert g.reading_order() == ["page0", "page1", "page2", "page3", "page4", "page5"]

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
