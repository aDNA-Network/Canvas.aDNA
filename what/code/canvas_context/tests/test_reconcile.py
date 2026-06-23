"""Tests for the leg-3 governed advisory-reverse write runtime (Operation Armature P1).

The headline property: a logged response advances the view, ``reconcile`` produces a **reviewed source draft**, and
the authoritative source is **never written** (``spec_roundtrip_protocol_v2`` §1.2). The runtime reuses
``canvas_std.roundtrip`` (firewall held — ``canvas_std`` is imported read-only, never mutated).
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from canvas_context import (
    governed_apply,
    is_round_trip_safe,
    reconcile,
    write_source_draft,
)

HERE = Path(__file__).resolve().parent
VIEW = HERE / "fixtures" / "interaction_review.canvas"
SOURCE = HERE / "fixtures" / "review_request.source.json"


def _view() -> dict:
    return json.loads(VIEW.read_text(encoding="utf-8"))


def _source() -> dict:
    return json.loads(SOURCE.read_text(encoding="utf-8"))


# --- the reconcile contract ---------------------------------------------------------------------


def test_reconcile_emits_advisory_draft_not_a_write():
    recon = reconcile(_view(), _source())
    # the draft is marked as a draft requiring review — never an authoritative write (§1.2)
    assert recon.draft["_draft"] is True
    assert recon.draft.get("_merged") is True
    assert recon.requires_review is True
    # topology matches the source, so the view is not stale (the gate's baseline aligns, §3.2)
    assert recon.stale is False
    # the draft preserves the source identity + topology
    assert recon.draft["name"] == "review_request"
    assert {n["id"] for n in recon.draft["nodes"]} == {n["id"] for n in _source()["nodes"]}


def test_reconcile_restores_lossy_source_only_fields():
    """§6 — source-only fields not recoverable from the view MUST be restored from source onto the draft."""
    recon = reconcile(_view(), _source())
    draft = recon.draft
    assert draft.get("fair", {}).get("license") == "MIT"            # top-level §6 (merge() drops these)
    assert draft.get("federation", {}).get("source_vault") == "Canvas.aDNA"
    assert draft.get("execution", {}).get("mode") == "workflow"
    # per-node config survives (decision_box carries an operator policy that the canvas view never holds)
    decision = next(n for n in draft["nodes"] if n["id"] == "decision_box")
    assert decision.get("config", {}).get("decision_policy") == "operator_required"


def test_reconcile_is_pure_mutates_no_input():
    view, source = _view(), _source()
    view_before, source_before = copy.deepcopy(view), copy.deepcopy(source)
    reconcile(view, source)
    assert view == view_before
    assert source == source_before


# --- the governed act ---------------------------------------------------------------------------


def test_governed_apply_advances_view_and_surfaces_the_response():
    advanced, recon = governed_apply(_view(), _source(), "summarize", "A review request used as the P1 demo.")
    # the view advanced (append-only): one response now logged
    log = advanced["metadata"]["frontmatter"]["_reserved"]["interaction"]["responses"]
    assert len(log) == 1 and log[0]["affordance"] == "summarize"
    # the reconciliation surfaces the response for review — but it is NOT written into the draft source
    assert recon.responses and recon.responses[0]["affordance"] == "summarize"
    assert "interaction" not in recon.draft  # the source draft carries no interaction layer (responses stay a payload)
    assert "responses" not in recon.draft


def test_governed_write_never_touches_the_authoritative_source(tmp_path):
    """The headline guarantee: the on-disk authoritative source is byte-for-byte unchanged after the full loop."""
    source_bytes_before = SOURCE.read_bytes()

    advanced, recon = governed_apply(_view(), _source(), "approve", "approve")
    draft_path = write_source_draft(recon, tmp_path / "review_request.source.draft.json", reviewed_by="stanley")

    # the authoritative source file is untouched — the runtime never wrote it
    assert SOURCE.read_bytes() == source_bytes_before
    # the draft landed in a SEPARATE artifact, marked for review + stamped with the reviewer
    assert draft_path.exists() and draft_path != SOURCE
    written = json.loads(draft_path.read_text(encoding="utf-8"))
    assert written["_draft"] is True
    assert written["requires_review"] is True
    assert written["reviewed_by"] == "stanley"


# --- the staleness gate (§3.2) ------------------------------------------------------------------


def test_staleness_gate_flags_a_changed_source():
    """If the source topology changed since the view was generated, the reverse is flagged stale (§3.2)."""
    fresh = reconcile(_view(), _source())
    assert fresh.stale is False

    changed = _source()
    changed["nodes"].append({"id": "new_section", "type": "text", "text": "added on the source since generation"})
    stale = reconcile(_view(), changed)
    assert stale.stale is True  # the view's stored sync_hash no longer matches the source's topology


# --- round-trip-to-baseline (the additive guarantee holds) --------------------------------------


def test_round_trip_to_baseline_still_holds():
    """The governed write does not disturb the additive guarantee: strip the view → a valid Core canvas."""
    assert is_round_trip_safe(_view()) is True


def test_reconcile_rejects_unknown_merge_strategy():
    with pytest.raises(ValueError):
        reconcile(_view(), _source(), strategy="nonsense")
