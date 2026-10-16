"""LIP-0011 — sync semantics (Standard v2.5.0; Operation Vernier P2b, firewall touch #7).

Signed 2026-10-15 at ``how/gates/lip_0011_signature_20261015`` (4/4 approve; **D-1 = (i)**). What is defended here:

* §1.1 — ``sync_hash`` byte for byte, by its **test vector**, so the Standard is checkable without our code; and the
  F-V-13 trap (separators written as literal control bytes, which render as nothing) cannot come back unseen.
* §2 / §3.1 — ``sync.source_sha256``: 64 lowercase hex, **hard** at ``extended`` and ``adna_native``.
* §4 / §3.2 — ``sync.generator``: a non-empty string, **hard** at both tiers; the top-level key stays legal.
* §3.3 — topology consistency for ``production: generated`` is an **advisory** at both tiers (D-1 (i)), never an error.
* §5 — A-8 runs at ``extended`` when the block **declares** ``extended``; ``core`` and undeclared canvases are untouched.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from canvas_std import advisories, compute_source_sha256, compute_sync_hash, validate, validate_suite
from canvas_std.validate import ConformanceLevel

FIXTURES = Path(__file__).parent / "fixtures"
SRC = Path(__file__).parent.parent / "src" / "canvas_std"
EXT, NATIVE, CORE = ConformanceLevel.EXTENDED, ConformanceLevel.ADNA_NATIVE, ConformanceLevel.CORE


def _doc(level: str = "extended", **reserved) -> dict:
    doc = {
        "nodes": [{"id": "a", "type": "text", "text": "a", "x": 0, "y": 0, "width": 100, "height": 50},
                  {"id": "b", "type": "text", "text": "b", "x": 0, "y": 100, "width": 100, "height": 50}],
        "edges": [{"id": "e", "fromNode": "a", "fromSide": "bottom", "toNode": "b", "toSide": "top", "toEnd": "arrow"}],
    }
    block = {"adna_version": "2.5.0", "conformance_level": level, "sync": {"sync_hash": compute_sync_hash(doc)}}
    block.update(reserved)
    doc["metadata"] = {"frontmatter": {"_reserved": block}}
    return doc


def _level(doc: dict) -> ConformanceLevel:
    return ConformanceLevel(doc["metadata"]["frontmatter"]["_reserved"]["conformance_level"])


# --- §1.1 the definition, byte for byte -----------------------------------------------------------
def test_the_normative_test_vector():
    doc = {"nodes": [{"id": "a"}, {"id": "b"}], "edges": [{"fromNode": "a", "toNode": "b"}]}
    assert compute_sync_hash(doc) == "097164175d271fb8"
    payload = "a\x01b\x02a->b"  # U+0001 between items, U+0002 between the lists, ASCII "->"
    assert hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16] == "097164175d271fb8"
    # The misreading F-V-13 recorded: the separators read as empty strings.
    assert hashlib.sha256(b"aba->b").hexdigest()[:16] == "5d3a8a0c81db08d9" != compute_sync_hash(doc)


def test_order_independence_and_the_lists_do_not_bleed():
    doc = {"nodes": [{"id": "b"}, {"id": "a"}], "edges": [{"fromNode": "a", "toNode": "b"}]}
    assert compute_sync_hash(doc) == "097164175d271fb8"
    # Without U+0002 these two would hash the same payload; with it they cannot.
    assert compute_sync_hash({"nodes": [{"id": "x->y"}], "edges": []}) != compute_sync_hash(
        {"nodes": [], "edges": [{"fromNode": "x", "toNode": "y"}]})


def test_no_literal_control_bytes_in_the_reference_source():
    # F-V-13: the separators were literal U+0001/U+0002 in roundtrip.py and printed as nothing.
    raw = (SRC / "roundtrip.py").read_bytes()
    assert b"\x01" not in raw and b"\x02" not in raw


# --- §2 source_sha256 ---------------------------------------------------------------------------
def test_compute_source_sha256_is_the_raw_byte_digest(tmp_path):
    f = tmp_path / "src.md"
    f.write_bytes(b"line\r\nno normalisation\n")
    assert compute_source_sha256(f) == hashlib.sha256(b"line\r\nno normalisation\n").hexdigest()
    assert compute_source_sha256(str(f)) == compute_source_sha256(f)


def test_the_city_twin_fixture_is_verifiable_from_its_source_file():
    entry = next(e for e in json.loads((FIXTURES / "manifest.json").read_text())["fixtures"]
                 if e["path"] == "adna_city_twin_shape.canvas")
    doc = json.loads((FIXTURES / entry["path"]).read_text())
    sync = doc["metadata"]["frontmatter"]["_reserved"]["sync"]
    assert sync["source_sha256"] == compute_source_sha256(FIXTURES / entry["source_file"])
    assert sync["sync_hash"] == compute_sync_hash(doc)


@pytest.mark.parametrize("level", ["extended", "adna_native"])
@pytest.mark.parametrize("bad", ["ABC", "f" * 63, "F" * 64, 42, None])
def test_source_sha256_is_hard_at_both_tiers(level, bad):
    doc = _doc(level)
    doc["metadata"]["frontmatter"]["_reserved"]["sync"]["source_sha256"] = bad
    assert any("source_sha256" in e for e in validate(doc, _level(doc)))


@pytest.mark.parametrize("level", ["extended", "adna_native"])
def test_well_formed_source_sha256_passes(level):
    doc = _doc(level)
    doc["metadata"]["frontmatter"]["_reserved"]["sync"]["source_sha256"] = "0" * 64
    assert validate(doc, _level(doc)) == []


# --- §4 generator ---------------------------------------------------------------------------------
@pytest.mark.parametrize("level", ["extended", "adna_native"])
@pytest.mark.parametrize("bad", ["", "   ", 7, None, ["x"]])
def test_sync_generator_is_hard_at_both_tiers(level, bad):
    doc = _doc(level)
    doc["metadata"]["frontmatter"]["_reserved"]["sync"]["generator"] = bad
    assert any("sync.generator" in e for e in validate(doc, _level(doc)))


@pytest.mark.parametrize("level", ["extended", "adna_native"])
def test_sync_generator_and_the_deprecated_top_level_key_are_both_legal(level):
    doc = _doc(level, generator="what/canvas/build_canvases.py")  # top-level: deprecated, not invalid (§4.2)
    doc["metadata"]["frontmatter"]["_reserved"]["sync"]["generator"] = "canvas_presentation.PresentationBuilder"
    assert validate(doc, _level(doc)) == []


# --- §5 A-8 at extended ---------------------------------------------------------------------------
def test_a8_now_runs_at_extended():
    doc = _doc("extended", authority="view")  # authority without production — the PercySleep shape
    assert any(e.startswith("A-8") for e in validate(doc, EXT))
    assert any(e.startswith("A-8") for e in validate(_doc("extended", production="handmade"), EXT))
    assert validate(_doc("extended", authority="view", production="generated"), EXT) == []


@pytest.mark.parametrize("declared", [None, "core"])
def test_core_and_undeclared_blocks_are_untouched_at_every_level(declared):
    # The 414 template-legacy `authority: view` canvases (ADR-011's view row): no _reserved check at core, and
    # validate_suite walking them through EXTENDED must not move level_reached (§5.2).
    doc = _doc("extended", authority="view")
    block = doc["metadata"]["frontmatter"]["_reserved"]
    if declared is None:
        del block["conformance_level"]
    else:
        block["conformance_level"] = declared
    assert validate(doc, CORE) == [] and validate(doc, EXT) == []
    assert validate_suite(doc, CORE).level_reached is EXT


def test_an_adna_native_block_is_not_checked_twice_on_the_way_through_extended():
    doc = _doc("adna_native", authority="view")  # fails A-8 at adna_native — as before v2.5.0
    assert validate(doc, EXT) == []
    assert validate_suite(doc, NATIVE).level_reached is EXT


# --- §3.3 topology consistency: advisory at both tiers (D-1 (i)) ----------------------------------
@pytest.mark.parametrize("level", ["extended", "adna_native"])
def test_a_stale_generated_canvas_warns_and_does_not_fail(level):
    doc = _doc(level, production="generated")
    doc["metadata"]["frontmatter"]["_reserved"]["sync"]["sync_hash"] = "0123456789abcdef"
    assert validate(doc, _level(doc)) == []
    (adv,) = advisories(doc, _level(doc))
    assert adv.startswith("A-6 (advisory)") and compute_sync_hash(doc) in adv


@pytest.mark.parametrize("production", [None, "hand_authored"])
def test_only_generated_canvases_get_the_topology_advisory(production):
    doc = _doc("adna_native", **({"production": production} if production else {}))
    doc["metadata"]["frontmatter"]["_reserved"]["sync"]["sync_hash"] = "0123456789abcdef"
    assert advisories(doc, NATIVE) == []


def test_no_advisories_at_core_or_for_a_fresh_canvas():
    stale = _doc("extended", production="generated")
    stale["metadata"]["frontmatter"]["_reserved"]["sync"]["sync_hash"] = "0123456789abcdef"
    assert advisories(stale, CORE) == []
    assert advisories(_doc("adna_native", production="generated"), NATIVE) == []
    assert advisories({"nodes": [], "edges": []}, NATIVE) == [] and advisories("not a doc", NATIVE) == []


def test_the_terminal_shape_is_source_bytes_and_therefore_stale():
    doc = json.loads((FIXTURES / "extended_terminal_shape.canvas").read_text())
    sync = doc["metadata"]["frontmatter"]["_reserved"]["sync"]
    assert sync["sync_hash"] == compute_source_sha256(FIXTURES / "extended_terminal_shape.source.md")[:16]
    assert validate(doc, EXT) == [] and len(advisories(doc, EXT)) == 1
    fresh = copy.deepcopy(doc)
    fresh["metadata"]["frontmatter"]["_reserved"]["sync"]["sync_hash"] = compute_sync_hash(doc)
    assert advisories(fresh, EXT) == []  # the one regeneration LIP-0011 §6 asks of Terminal
