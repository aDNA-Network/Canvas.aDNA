"""B2 — long-form ride-on-text semantic_types (spec_component_model §4.4).

Quote and footnote roles ride on ``class: text`` via canonical ``semantic_type`` values rather than dedicated
taxonomy classes. Verifies the long-form fixture validates aDNA-Native, that the registered value set is exactly
what the spec documents, and that a footnote anchor ref still gets teeth from B1's ``validate_anchors``. Added with
the v2.0.1 errata (LIP queue B2).
"""

from __future__ import annotations

import json
from pathlib import Path

from canvas_std import validate
from canvas_std.reserved import LONGFORM_SEMANTIC_TYPES
from canvas_std.validate import ConformanceLevel

FIXTURES = Path(__file__).parent / "fixtures"


def _longform() -> dict:
    return json.loads((FIXTURES / "adna_longform_quote.canvas").read_text())


def test_longform_fixture_valid_end_to_end():
    assert validate(_longform(), ConformanceLevel.ADNA_NATIVE) == []


def test_registered_longform_values():
    assert LONGFORM_SEMANTIC_TYPES == frozenset({"quote", "block_quote", "footnote", "attribution"})
    # every long-form role used in the fixture is a registered value (ride-on-text, not a new class)
    comp = _longform()["metadata"]["frontmatter"]["_reserved"]["component_types"]
    used = {e["semantic_type"] for e in comp.values() if "semantic_type" in e}
    assert used == LONGFORM_SEMANTIC_TYPES
    # and they all ride on the baseline `text` class — no taxonomy growth
    assert all(e["class"] == "text" for e in comp.values() if e.get("semantic_type") in LONGFORM_SEMANTIC_TYPES)


def test_footnote_orphan_ref_fails():
    # a footnote whose qualities.ref points nowhere is a no-orphaned-anchor (A-5) violation — B1 gives it teeth
    doc = _longform()
    doc["metadata"]["frontmatter"]["_reserved"]["component_types"]["fn1"]["qualities"]["ref"] = "ghost"
    errs = validate(doc, ConformanceLevel.ADNA_NATIVE)
    assert any("missing anchor" in e for e in errs), errs
