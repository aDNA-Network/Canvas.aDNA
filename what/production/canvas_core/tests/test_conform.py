"""Conformance-repair tests (`canvas_core.conform`) — the C-4 normalizer and the `_reserved` uplift.

The fixtures below reproduce the **exact defect signature** the P2b census measured in two other
vaults (`campaign_canvas_blueprint/artifacts/p2b_conversion_census_20260907.md`), rather than
copying anyone's files in: three Operations projection copies that had lost 100% of their explicit
`toEnd` keys, one of them additionally carrying an edge pointing at a node id that is not in the
file, and five ScienceStanley boards with the same `toEnd` omission.

Reproducing the signature rather than the file is deliberate — the projection copy is **gitignored
by its owner**, and Canvas.aDNA is a public repo (`adr_012`, publication boundary).
"""

from __future__ import annotations

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core import conform
from canvas_std import ConformanceLevel, validate


def _obsidian_resaved() -> dict:
    """A canvas as Obsidian leaves it: renders fine, no explicit `toEnd` anywhere."""
    return {
        "nodes": [
            {"id": "pkg", "type": "text", "x": 0, "y": 0, "width": 220, "height": 100, "text": "#### package"},
            {"id": "lease", "type": "text", "x": 300, "y": 0, "width": 220, "height": 100, "text": "lease"},
            {"id": "expires", "type": "text", "x": 600, "y": 0, "width": 220, "height": 100, "text": "expires_at"},
        ],
        "edges": [
            {"id": "e1", "fromNode": "pkg", "fromSide": "right", "toNode": "lease", "toSide": "left"},
            {"id": "e2", "fromNode": "lease", "fromSide": "right", "toNode": "expires", "toSide": "left"},
        ],
    }


def test_normalize_edges_adds_explicit_to_end_and_counts_repairs():
    doc, repaired = conform.normalize_edges(_obsidian_resaved())
    assert repaired == 2
    assert [e["toEnd"] for e in doc["edges"]] == ["arrow", "arrow"]


def test_normalize_edges_clears_c4_in_the_validator_that_reported_it():
    """The point of the module: run the real validator before and after, not a proxy assertion."""
    doc = _obsidian_resaved()
    before = [e for e in validate(doc) if e.startswith("C-4")]
    assert len(before) == 2

    conform.normalize_edges(doc)
    errors = validate(doc)
    assert [e for e in errors if e.startswith("C-4")] == []
    assert errors == []


def test_normalize_edges_leaves_a_deliberate_undirected_edge_alone():
    """`toEnd: "none"` is a permitted undirected edge — already explicit, so not ours to overwrite."""
    doc = _obsidian_resaved()
    doc["edges"][0]["toEnd"] = "none"
    doc, repaired = conform.normalize_edges(doc)
    assert repaired == 1
    assert doc["edges"][0]["toEnd"] == "none"


def test_normalize_edges_is_idempotent():
    doc, first = conform.normalize_edges(_obsidian_resaved())
    _, second = conform.normalize_edges(doc)
    assert (first, second) == (2, 0)


def test_normalize_edges_changes_no_node():
    doc = _obsidian_resaved()
    before = [dict(n) for n in doc["nodes"]]
    conform.normalize_edges(doc)
    assert doc["nodes"] == before


def test_unresolved_edges_reports_the_dangling_reference_and_does_not_repair_it():
    """The census's one real defect: an edge off `expires_at` at a target that is not in the file."""
    doc = _obsidian_resaved()
    doc["edges"].append(
        {"id": "8f003ea", "fromNode": "expires", "fromSide": "bottom",
         "toNode": "269b75cbca9331d4", "toSide": "top"}
    )
    assert conform.unresolved_edges(doc) == [("8f003ea", "toNode", "269b75cbca9331d4")]

    # Normalizing does not quietly drop it — repairing a dangling edge needs judgement, and a
    # normalizer that deleted edges would be the most dangerous tool in the vault.
    conform.normalize_edges(doc)
    assert len(doc["edges"]) == 3
    assert conform.unresolved_edges(doc) == [("8f003ea", "toNode", "269b75cbca9331d4")]
    assert any(e.startswith("C-3") for e in validate(doc))


def test_unresolved_edges_empty_on_a_sound_canvas():
    assert conform.unresolved_edges(_obsidian_resaved()) == []


def test_uplift_writes_the_canonical_path_not_the_legacy_one():
    """F-B1-1: a block at `metadata._reserved` reads green at `core` while no tool can see it."""
    doc = conform.uplift_to_adna_native(
        _obsidian_resaved(), source_name="c08_dispatch_package_anatomy", authority="view"
    )
    assert "_reserved" in doc["metadata"]["frontmatter"]
    assert "_reserved" not in doc["metadata"]


def test_uplift_recomputes_a_16_hex_sync_hash():
    doc = conform.uplift_to_adna_native(_obsidian_resaved(), source_name="src", authority="view")
    sync = doc["metadata"]["frontmatter"]["_reserved"]["sync"]
    assert len(sync["sync_hash"]) == 16
    assert all(c in "0123456789abcdef" for c in sync["sync_hash"])
    assert sync["source_name"] == "src"


def test_uplift_rejects_an_authority_canvas_std_would_accept_silently():
    """F-B1-2: `canvas_std` does not know this key, so an invented value passes validation."""
    with pytest.raises(ValueError, match="authority"):
        conform.uplift_to_adna_native(_obsidian_resaved(), source_name="s", authority="veiw")


def test_uplift_changes_no_node_or_edge():
    doc = _obsidian_resaved()
    nodes_before = [dict(n) for n in doc["nodes"]]
    edges_before = [dict(e) for e in doc["edges"]]
    conform.uplift_to_adna_native(doc, source_name="s", authority="view")
    assert doc["nodes"] == nodes_before
    assert doc["edges"] == edges_before


def test_full_repair_reaches_adna_native():
    """End to end, the way a consumer would run it: normalize, then uplift, then validate."""
    doc = _obsidian_resaved()
    conform.normalize_edges(doc)
    conform.uplift_to_adna_native(
        doc,
        source_name="c08_dispatch_package_anatomy",
        authority="view",
        context_object={"id": "urn:adna:canvas:ops:c08_dispatch_package_anatomy",
                        "version": "1.0.0", "refs": []},
    )
    errors = validate(doc, level=ConformanceLevel.ADNA_NATIVE)
    assert errors == [], errors


def test_uplift_refuses_a_context_object_without_an_id():
    """A-7 wants a non-empty id; refusing at build time beats failing after it is in someone's file."""
    with pytest.raises(ValueError, match="context_object"):
        conform.uplift_to_adna_native(
            _obsidian_resaved(), source_name="s", authority="view", context_object={"refs": []}
        )


# ---------------------------------------------------------------------------------------------
# The 2026-09-11 axis split (aDNA.aDNA HAUSSMANN R1 / Operation Plumbline P1).
# `authority` answers *who owns the meaning*; `production` answers *how is the picture made*.
# ---------------------------------------------------------------------------------------------


def test_generator_is_no_longer_an_authority_value():
    """The removed cell. It never answered "who owns the meaning" — it answered the other question.

    This is the one change that can break a caller, so it is pinned: a caller who passes the old
    third value gets a `ValueError` naming the replacement, not a silently-written wrong key.
    """
    with pytest.raises(ValueError, match="production='generated'"):
        conform.uplift_to_adna_native(_obsidian_resaved(), source_name="s", authority="generator")


def test_production_is_checked_here_because_canvas_std_will_not():
    """F-B1-2 applies to the new key exactly as it applied to the old one."""
    with pytest.raises(ValueError, match="production"):
        conform.uplift_to_adna_native(
            _obsidian_resaved(), source_name="s", production="hand-authored"  # hyphen, not underscore
        )


def test_dual_channel_and_generated_can_finally_both_be_said():
    """E2's defect, now expressible.

    Canvas's own first two dual-channel canvases are `dual_channel` AND machine-generated at once.
    Under the single three-value enum they declared `dual_channel`, so a reader following the table
    literally received no instruction not to hand-edit them. Both facts now fit in the block.
    """
    doc = conform.uplift_to_adna_native(
        _obsidian_resaved(), source_name="s", authority="dual_channel", production="generated"
    )
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    assert reserved["authority"] == "dual_channel"
    assert reserved["production"] == "generated"


def test_a_hand_authored_primary_artifact_needs_no_authority_at_all():
    """P2b's population — and the reason the offer was blocked for four days on the wrong cause.

    A hand-authored teaching diagram or review board has no prose twin and no `.lattice.yaml`: it
    owns its own meaning, so the authority question does not arise. It is outside the scope of
    `pattern_diagrammatic_context`, which governs a `.canvas` *beside a document*. The ruled pattern
    declines to call an undeclared canvas nonconformant, so this must reach `adna_native` with the
    key absent — **absent, not empty, not a placeholder.**
    """
    doc = _obsidian_resaved()
    conform.normalize_edges(doc)
    conform.uplift_to_adna_native(doc, source_name="c08_teaching_diagram", production="hand_authored")
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    assert "authority" not in reserved
    assert reserved["production"] == "hand_authored"
    assert validate(doc, level=ConformanceLevel.ADNA_NATIVE) == []


def test_both_axis_keys_may_be_omitted_entirely():
    """Backward compatibility for every caller that predates the split, stated as a test.

    `authority` was a *required* argument until 2026-09-11 because Canvas's own draft said a canvas
    without one was nonconformant. The ruling declined that mandate; requiring it here would be this
    function inventing a rule the doctrine refused to make.
    """
    doc = _obsidian_resaved()
    conform.normalize_edges(doc)
    conform.uplift_to_adna_native(doc, source_name="s")
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    assert "authority" not in reserved and "production" not in reserved
    assert validate(doc, level=ConformanceLevel.ADNA_NATIVE) == []
