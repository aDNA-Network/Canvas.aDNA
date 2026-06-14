"""Golden-canvas fixture harness (Keystone E0.3).

What runs NOW (E0.3): each fixture parses as JSON, has the baseline node/edge shape, every node/edge
carries its required fields, and the declared level is coherent. These guard the fixtures themselves.

What is XFAIL until E1: the ``validate()`` / ``strip()`` assertions — the behavior is stubbed
(``NotImplementedError``) until E1.1 (Core/Extended), E1.4 (``_reserved``), E1.5 (degradation). The xfail
is non-strict, so these tests flip to PASS automatically when E1 lands (a built-in E1 acceptance signal).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from canvas_std import schema, strip, validate
from canvas_std.validate import ConformanceLevel

FIXTURES = Path(__file__).parent / "fixtures"
MANIFEST = json.loads((FIXTURES / "manifest.json").read_text())["fixtures"]
LEVELS = {lvl.value for lvl in ConformanceLevel}


def _load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


@pytest.mark.parametrize("entry", MANIFEST, ids=lambda e: e["path"])
class TestFixtures:
    # --- runs now: the fixtures are well-formed and coherent --------------------------------
    def test_parses_and_baseline_shape(self, entry):
        doc = _load(entry["path"])
        assert isinstance(doc.get("nodes"), list) and doc["nodes"], entry["path"]
        assert isinstance(doc.get("edges"), list), entry["path"]

    def test_declared_level_is_known(self, entry):
        assert entry["declared_level"] in LEVELS

    def test_nodes_and_edges_have_required_fields(self, entry):
        doc = _load(entry["path"])
        for n in doc["nodes"]:
            for f in schema.NODE_REQUIRED_FIELDS:
                assert f in n, f"{entry['path']}: node {n.get('id')!r} missing {f}"
        for e in doc["edges"]:
            for f in schema.EDGE_REQUIRED_FIELDS:
                assert f in e, f"{entry['path']}: edge {e.get('id')!r} missing {f}"

    def test_adna_native_declares_level_in_reserved(self, entry):
        if entry["declared_level"] != "adna_native":
            pytest.skip("only aDNA-Native carries _reserved.conformance_level")
        doc = _load(entry["path"])
        assert doc["metadata"]["frontmatter"]["_reserved"]["conformance_level"] == "adna_native"

    # --- behavior assertions: implemented across E1.1–E1.5 (xfail markers retired) ----------
    def test_validate_matches_expectation(self, entry):
        doc = _load(entry["path"])
        level = ConformanceLevel(entry["declared_level"])
        errors = validate(doc, level)
        assert (errors == []) is entry["expected_valid"], errors

    def test_degradation(self, entry):
        if not entry["degrades_to"] or not entry["expected_valid"]:
            pytest.skip("no degradation target")
        doc = _load(entry["path"])
        bare = strip(doc)
        assert "metadata" not in bare or "_reserved" not in bare.get("metadata", {}).get("frontmatter", {})
        assert validate(bare, ConformanceLevel(entry["degrades_to"])) == []
