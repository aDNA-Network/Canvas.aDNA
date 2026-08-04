"""Halftone HR — collector tests (`canvas_core.rlhf.review_collect`): the three-sink fan-out + idempotency.

All runs use ``participant_kind="ai"`` (`{kind: ai}` attribution) — agent-simulated verdicts are never forged
as human signal. Tmp dataset root + tmp III store; the live corpus and store are untouched.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.rlhf import iii_bridge, review_collect
from canvas_core.rlhf.selection import SelectionRecord, validate_selection_record
from canvas_std import validate_interaction

from conftest import build_review as _build


def _set_fm(sidecar: Path, **updates) -> None:
    """Edit sidecar frontmatter the way Meta Bind would (values only; body untouched)."""
    import yaml

    text = sidecar.read_text(encoding="utf-8")
    _, fm_text, body = text.split("---", 2)
    fm = yaml.safe_load(fm_text)
    fm.update(updates)
    sidecar.write_text(
        "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000) + "---" + body,
        encoding="utf-8",
    )


def _fm(sidecar: Path) -> dict:
    import yaml

    return yaml.safe_load(sidecar.read_text(encoding="utf-8").split("---", 2)[1])


def _collect(root, paths, tmp_path, **kw):
    return review_collect.collect(
        paths.canvas,
        approver="test_agent",
        participant_kind="ai",
        dataset_root=tmp_path / "dataset",
        store_path=tmp_path / "store.jsonl",
        **kw,
    )


def _reviewed(vault_fixture, tmp_path):
    root, paths = _build(vault_fixture)
    _set_fm(paths.sidecars["var_1"], verdict="approve", rating=4, defect_tags=["slop"], note="keep it")
    _set_fm(paths.sidecars["var_2"], verdict="reject", note="off model", regenerate_requested=True)
    return root, paths


def test_three_sink_fan_out(vault, tmp_path):
    root, paths = _reviewed(vault, tmp_path)
    counts = _collect(root, paths, tmp_path)
    # var_1: verdict+rating+defect+note = 4 · var_2: verdict+note+regenerate = 3
    assert counts == {"variants": 2, "responses": 7, "selections": 1, "iii_lines": 1, "skipped": 0}

    doc = json.loads(paths.canvas.read_text(encoding="utf-8"))
    reserved = doc["metadata"]["frontmatter"]["_reserved"]
    assert validate_interaction(reserved, doc) == []
    responses = doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["responses"]
    assert len(responses) == 7
    assert all(r["participant"] == {"kind": "ai", "id": "test_agent"} for r in responses)
    regen = next(r for r in responses if r["affordance"] == "var_2.regenerate")
    assert regen["value"] is None  # action value is null (I-3)

    # Schema-A: one F-36-clean record for the approval, in the timestamp month, pick_index = var_1.
    records = list((tmp_path / "dataset").rglob("sel_*.json"))
    assert len(records) == 1
    sel = SelectionRecord.from_dict(json.loads(records[0].read_text(encoding="utf-8")))
    assert validate_selection_record(sel) == []
    assert sel.pick_index == 0 and len(sel.variants) == 2
    assert sel.vr_scores == {"overall": 4.0}
    assert "verdict=approve" in sel.pick_reason and "slop" in sel.pick_reason

    # III: exactly one line, carrying the same selection_id.
    lines = (tmp_path / "store.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["rlhf_reviewer_persona"] == "test_agent"

    # Ledger written last: collected_at + selection_id + review_turn stamped.
    fm1 = _fm(paths.sidecars["var_1"])
    assert fm1["collected_at"] and fm1["selection_id"] == sel.selection_id and fm1["review_turn"] == "t1"
    # The Meta Bind body survived the ledger rewrite byte-verbatim.
    assert "INPUT[inlineSelect" in paths.sidecars["var_1"].read_text(encoding="utf-8")


def test_rerun_is_a_no_op(vault, tmp_path):
    root, paths = _reviewed(vault, tmp_path)
    _collect(root, paths, tmp_path)
    counts = _collect(root, paths, tmp_path)
    assert counts["variants"] == 0 and counts["skipped"] == 2
    assert counts["responses"] == counts["selections"] == counts["iii_lines"] == 0
    doc = json.loads(paths.canvas.read_text(encoding="utf-8"))
    assert len(doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["responses"]) == 7
    assert len(list((tmp_path / "dataset").rglob("sel_*.json"))) == 1
    assert len((tmp_path / "store.jsonl").read_text(encoding="utf-8").strip().splitlines()) == 1


def test_ledger_loss_replay_self_heals(vault, tmp_path):
    """Clearing collected_at (lost ledger) must not duplicate responses, records, or III lines —
    the canvas response `at` is the fallback clock for the deterministic selection_id."""
    root, paths = _reviewed(vault, tmp_path)
    _collect(root, paths, tmp_path)
    _set_fm(paths.sidecars["var_1"], collected_at=None, selection_id=None, review_turn=None)
    counts = _collect(root, paths, tmp_path, force=True)
    assert counts["responses"] == 0            # layer-2 dedup
    assert counts["selections"] == 0           # layer-3: same stamp (from canvas) → same id → exists
    assert counts["iii_lines"] == 0            # layer-4: native accumulate dedup
    assert len(list((tmp_path / "dataset").rglob("sel_*.json"))) == 1
    assert len((tmp_path / "store.jsonl").read_text(encoding="utf-8").strip().splitlines()) == 1


def test_dry_run_writes_nothing(vault, tmp_path):
    root, paths = _reviewed(vault, tmp_path)

    def state() -> str:
        h = hashlib.sha256()
        for p in sorted([paths.canvas, *paths.sidecars.values()]):
            h.update(p.read_bytes())
        h.update(str(sorted((tmp_path / "dataset").rglob("*"))).encode())
        h.update(b"store" + ((tmp_path / "store.jsonl").read_bytes() if (tmp_path / "store.jsonl").exists() else b""))
        return h.hexdigest()

    before = state()
    counts = _collect(root, paths, tmp_path, dry_run=True)
    assert state() == before                     # byte-identical everywhere
    assert counts["variants"] == 2 and counts["responses"] == 7
    assert counts["selections"] == 1 and counts["iii_lines"] == 1  # would-writes reported


def test_reject_only_session_appends_responses_only(vault, tmp_path):
    root, paths = _build(vault)
    _set_fm(paths.sidecars["var_2"], verdict="reject", defect_tags=["off-model", "composition"])
    counts = _collect(root, paths, tmp_path)
    assert counts == {"variants": 1, "responses": 3, "selections": 0, "iii_lines": 0, "skipped": 1}
    assert not (tmp_path / "dataset").exists() or not list((tmp_path / "dataset").rglob("sel_*.json"))
    assert not (tmp_path / "store.jsonl").exists()
    doc = json.loads(paths.canvas.read_text(encoding="utf-8"))
    tags = [
        r["value"]
        for r in doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["responses"]
        if r["affordance"] == "var_2.defect"
    ]
    assert sorted(tags) == ["composition", "off-model"]  # multi-tag = one response per tag


def test_unknown_defect_tag_hard_fails(vault, tmp_path):
    root, paths = _build(vault)
    _set_fm(paths.sidecars["var_1"], verdict="approve", defect_tags=["not-in-vocab"])
    with pytest.raises(ValueError, match="not-in-vocab|IX5|options"):
        _collect(root, paths, tmp_path)


def test_missing_approver_refused(vault, tmp_path):
    root, paths = _reviewed(vault, tmp_path)
    with pytest.raises(ValueError, match="approver"):
        review_collect.collect(paths.canvas, approver="", participant_kind="ai")


def test_default_learning_store_repointed_to_live_name():
    """HR regression: the stale pre-merge `canvasforge_…` default is gone; the default points at the live store."""
    assert iii_bridge.DEFAULT_LEARNING_STORE.name == "canvas_iii_learning_store.jsonl"
    assert iii_bridge.DEFAULT_LEARNING_STORE.exists()  # the live store (3+ lines) resolves via the iii symlink
