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
    # emit_rejects=True explicitly, so these tests stay pinned to the behaviour they assert rather
    # than to whatever the module default happens to be.
    # ⛩ 2026-09-07: this used to read "(not in production)" — true only until the S-4 gate was
    # ruled. Argus ruled reading (b) and the production default is now True as well, so the
    # parenthetical was stale, not wrong-at-the-time. The override stays for explicitness.
    kw.setdefault("emit_rejects", True)
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
    # S-3 (2026-08-09): iii_lines is now 2, not 1 — the approval routes via Schema-A and the
    # rejection routes via responses[]. Before the seam ruling the reject produced nothing.
    assert counts == {
        "variants": 2, "responses": 7, "selections": 1,
        "rejects": 1, "rejects_held": 0, "iii_lines": 2, "skipped": 0,
        # F-HR-1 (2026-09-08): the counts dict gained two conformance fields. Both are zero on a
        # healthy surface — asserted rather than omitted, so a normalization that started firing
        # here (i.e. our own builder emitting non-conformant edges) would fail this test loudly.
        "edges_normalized": 0, "edges_unresolved": 0,
    }

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

    # III: two lines — one per verdict, distinguishable by signal type and by which dedup key
    # they carry (selection_id for the accept, response_id for the reject).
    lines = [json.loads(x) for x in
             (tmp_path / "store.jsonl").read_text(encoding="utf-8").strip().splitlines()]
    assert len(lines) == 2
    assert all(x["rlhf_reviewer_persona"] == "test_agent" for x in lines)
    by_type = {x["rlhf_signal_type"]: x for x in lines}
    assert set(by_type) == {"accept", "reject"}
    accept_ns = by_type["accept"]["rlhf_consumer_namespace"]["canvasforge"]["image_generation"]
    reject_ns = by_type["reject"]["rlhf_consumer_namespace"]["canvasforge"]["image_generation"]
    assert accept_ns["selection_id"] == sel.selection_id and "response_id" not in accept_ns
    assert reject_ns["response_id"].startswith("rej_") and "selection_id" not in reject_ns
    # The rejection's CONTENT is what makes it learnable (§4.5) — the note travels with it.
    assert reject_ns["note"] == "off model"
    assert "off model" in by_type["reject"]["example"]
    assert by_type["reject"]["trap"] == "image_generation_variant_reject"

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
    assert counts["rejects"] == 0
    doc = json.loads(paths.canvas.read_text(encoding="utf-8"))
    assert len(doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["responses"]) == 7
    assert len(list((tmp_path / "dataset").rglob("sel_*.json"))) == 1
    # 2 lines, not 1: the reject signal is subject to the same dedup as the accept (S-2).
    assert len((tmp_path / "store.jsonl").read_text(encoding="utf-8").strip().splitlines()) == 2


def test_ledger_loss_replay_self_heals(vault, tmp_path):
    """Clearing collected_at (lost ledger) must not duplicate responses, records, or III lines —
    the canvas response `at` is the fallback clock for the deterministic selection_id."""
    root, paths = _reviewed(vault, tmp_path)
    _collect(root, paths, tmp_path)
    _set_fm(paths.sidecars["var_1"], collected_at=None, selection_id=None, review_turn=None)
    counts = _collect(root, paths, tmp_path, force=True)
    assert counts["responses"] == 0            # layer-2 dedup
    assert counts["selections"] == 0           # layer-3: same stamp (from canvas) → same id → exists
    assert counts["iii_lines"] == 0            # layer-4: native accumulate dedup, BOTH key families
    assert len(list((tmp_path / "dataset").rglob("sel_*.json"))) == 1
    assert len((tmp_path / "store.jsonl").read_text(encoding="utf-8").strip().splitlines()) == 2


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
    assert counts["selections"] == 1 and counts["iii_lines"] == 2  # would-writes: accept + reject
    assert counts["rejects"] == 1


def test_reject_only_session_now_emits_a_signal(vault, tmp_path):
    """INVERTED at S-3 (2026-08-09). This test previously asserted the *bug*.

    Its old name — ``..._appends_responses_only`` — and its old assertion ``not (tmp_path /
    "store.jsonl").exists()`` encoded the exact loss the seam ruling fixed: a reject-only pass
    wrote a durable record into ``responses[]`` and produced **no learning signal at all**. It is
    inverted rather than deleted so the regression stays legible: Schema-A must still write
    nothing (it structurally requires a pick), and III must now receive the rejection.
    """
    root, paths = _build(vault)
    _set_fm(paths.sidecars["var_2"], verdict="reject", defect_tags=["off-model", "composition"])
    counts = _collect(root, paths, tmp_path)
    assert counts == {
        "variants": 1, "responses": 3, "selections": 0,
        "rejects": 1, "rejects_held": 0, "iii_lines": 1, "skipped": 1,
        "edges_normalized": 0, "edges_unresolved": 0,   # F-HR-1 fields, zero on a healthy surface
    }

    # Schema-A stays approval-only — unchanged by the ruling, and that is the point.
    assert not (tmp_path / "dataset").exists() or not list((tmp_path / "dataset").rglob("sel_*.json"))

    # III now has exactly the signal that used to be dropped.
    lines = (tmp_path / "store.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    signal = json.loads(lines[0])
    assert signal["rlhf_signal_type"] == iii_bridge.RLHF_SIGNAL_TYPE_REJECT
    ns = signal["rlhf_consumer_namespace"]["canvasforge"]["image_generation"]
    assert ns["derived_from"] == "interaction.responses"
    # Both tags survive the fold, even though each was logged as its own response row.
    assert sorted(ns["defect_tags"]) == ["composition", "off-model"]
    assert "off-model" in signal["example"] and "composition" in signal["example"]

    doc = json.loads(paths.canvas.read_text(encoding="utf-8"))
    tags = [
        r["value"]
        for r in doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["responses"]
        if r["affordance"] == "var_2.defect"
    ]
    assert sorted(tags) == ["composition", "off-model"]  # multi-tag = one response per tag


def test_a_reject_with_no_tags_or_note_says_so(vault, tmp_path):
    """A bare "no" is still worth recording — but the signal must admit it carries no reason,
    rather than presenting an empty rationale as if the reviewer had given one."""
    root, paths = _build(vault)
    _set_fm(paths.sidecars["var_2"], verdict="reject")
    _collect(root, paths, tmp_path)
    signal = json.loads((tmp_path / "store.jsonl").read_text(encoding="utf-8").strip())
    assert signal["rlhf_signal_type"] == "reject"
    assert "not captured" in signal["example"]


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


def test_s4_gate_emits_rejects_by_default_after_the_ruling(vault, tmp_path):
    """⛩ INVERTED 2026-09-07, not deleted — this test asserted the OPPOSITE until the S-4 ruling.

    As written 2026-08-09 it asserted ``rejects_held == 1``, ``iii_lines == 0`` and that no store
    file was created, because spec_rlhf_seam §5 S-4 required ADR-005 vocabulary confirmation with
    Argus **before first emission** — the signal shape is III's, not ours. That default had to
    actually hold rather than merely be documented as intended, so it was asserted.

    Argus ruled on 2026-09-07 (reading (b), ``accepted`` = the reviewer's verdict) and said "emit
    when ready". The gate opened, so the assertion inverts: the reject now reaches the store. The
    invariant that did NOT change is the last one — the capture substrate never depended on the
    gate, which is why holding the III write lost nothing while it was closed.
    """
    _root, paths = _build(vault)
    _set_fm(paths.sidecars["var_2"], verdict="reject", note="off model")
    counts = review_collect.collect(          # NOTE: not _collect — no emit_rejects override
        paths.canvas,
        approver="test_agent",
        participant_kind="ai",
        dataset_root=tmp_path / "dataset",
        store_path=tmp_path / "store.jsonl",
    )
    assert counts["rejects"] == 1            # built
    assert counts["rejects_held"] == 0       # and no longer held
    assert counts["iii_lines"] == 1
    assert (tmp_path / "store.jsonl").exists()

    # The capture substrate is unaffected — it never was gate-dependent.
    doc = json.loads(paths.canvas.read_text(encoding="utf-8"))
    verdicts = [
        r["value"] for r in doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["responses"]
        if r["affordance"] == "var_2.verdict"
    ]
    assert verdicts == ["reject"]


def test_s4_gate_default_tracks_the_bridge_constant(vault):
    """The gate is one constant, flipped in one place when Argus replies."""
    assert review_collect.REJECT_VOCABULARY_CONFIRMED is iii_bridge.REJECT_VOCABULARY_CONFIRMED


def test_accepted_is_the_reviewers_verdict_not_store_admission(vault, tmp_path):
    """The S-4 ruling, pinned by a test rather than by a comment (Argus 2026-09-07, reading (b)).

    ``accepted`` is the reviewer's verdict: ``False`` on a reject, ``True`` on a pick. Both halves
    are asserted in one place, because the whole content of the ruling is the *asymmetry* — a
    future reader finding one ``True`` and one ``False`` would otherwise be tempted to harmonise
    them, which would re-introduce exactly the bug ADR-003 §3's graduation gate is scored against
    (refusals accumulating toward "this register is working").
    """
    _root, paths = _build(vault)
    # One of each verdict in a single pass, so both entries land in the same store and the
    # asymmetry is visible in one file rather than inferred across two runs.
    _set_fm(paths.sidecars["var_1"], verdict="approve", rating=4, note="keep it")
    _set_fm(paths.sidecars["var_2"], verdict="reject", note="off model")
    store = tmp_path / "store.jsonl"
    review_collect.collect(
        paths.canvas,
        approver="test_agent",
        participant_kind="ai",
        dataset_root=tmp_path / "dataset",
        store_path=store,
    )
    entries = [json.loads(line) for line in store.read_text().splitlines() if line.strip()]
    by_type = {e["rlhf_signal_type"]: e for e in entries}

    assert by_type[iii_bridge.RLHF_SIGNAL_TYPE_REJECT]["accepted"] is False
    assert by_type[iii_bridge.RLHF_SIGNAL_TYPE_ACCEPT]["accepted"] is True
    # The two channels stay orthogonal: rlhf_signal_type = what the signal IS; accepted = what the
    # reviewer RULED. Neither is derivable from the other.
    assert (
        by_type[iii_bridge.RLHF_SIGNAL_TYPE_REJECT]["trap"]
        != by_type[iii_bridge.RLHF_SIGNAL_TYPE_ACCEPT]["trap"]
    )


# ================================================================================================
# F-HR-1 — normalize-on-collect (Blueprint P3, 2026-09-08)
#
# The defect this closes is not hypothetical and is not ours alone. A review surface is handed to a
# human in Obsidian; Obsidian's re-save rewrites the `edges` block WITHOUT the explicit `toEnd`
# keys; the canvas still renders perfectly and now fails C-4. Measured 2026-09-08 across 106
# authored canvases in 18 peer vaults: 464 such errors, 95% of all conformance errors once one
# float-coordinate outlier vault is excluded. In a peer's history the signature has a named commit
# (f00bf04, 2026-07-22, "canvas: layout adjustments … in Obsidian") that stripped every explicit
# toEnd in one file in one act.
#
# The re-save is reproduced HERE as a fixture mutation. No peer's file is copied into this repo:
# Canvas.aDNA is public and the vault where it was first measured gitignores its copy (adr_012).
# ================================================================================================

def _obsidian_resave(canvas_path: Path) -> int:
    """Drop every explicit top-level ``toEnd``, as an Obsidian re-save does. Returns how many went."""
    doc = json.loads(canvas_path.read_text(encoding="utf-8"))
    dropped = 0
    for edge in doc.get("edges", []):
        if "toEnd" in edge:
            del edge["toEnd"]
            dropped += 1
    canvas_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return dropped


def _core_errors(canvas_path: Path) -> list[str]:
    from canvas_std.conformance import ConformanceLevel, validate_suite

    doc = json.loads(canvas_path.read_text(encoding="utf-8"))
    return [f["id"] for f in validate_suite(doc, ConformanceLevel.CORE).failed]


def test_the_resave_really_does_un_conform_the_surface(vault, tmp_path):
    """The premise, asserted rather than assumed: without the fix, C-4 appears from a pure re-save."""
    _root, paths = _build(vault)
    assert _core_errors(paths.canvas) == [], "the surface should start conformant"
    dropped = _obsidian_resave(paths.canvas)
    assert dropped > 0, "fixture must have explicit toEnd keys to drop, or it proves nothing"
    assert set(_core_errors(paths.canvas)) == {"C-4"}


def test_collect_repairs_the_resave_in_the_write_back(vault, tmp_path):
    """The fix: collecting a verdict restores conformance in the same act that records it."""
    root, paths = _reviewed(vault, tmp_path)
    dropped = _obsidian_resave(paths.canvas)
    counts = _collect(root, paths, tmp_path)
    assert counts["edges_normalized"] == dropped
    assert _core_errors(paths.canvas) == []
    # and the verdicts still landed — the repair is not instead of the collection
    assert counts["variants"] == 2 and counts["responses"] > 0


def test_normalization_is_reported_but_not_persisted_when_nothing_is_collected(vault, tmp_path):
    """⚠ The idempotency property is load-bearing: a pass with nothing to collect writes nothing.

    An un-conformed surface with no pending verdicts is REPORTED, not silently rewritten. Per
    Berthier's Operations ruling (2026-09-07), a hand-maintained canvas wants its normalize pass
    before publish, not as a side effect of somebody else's read.
    """
    root, paths = _build(vault)  # no verdicts set
    dropped = _obsidian_resave(paths.canvas)
    before = paths.canvas.read_bytes()
    counts = _collect(root, paths, tmp_path)
    assert counts["variants"] == 0
    assert counts["edges_normalized"] == dropped     # seen and said
    assert paths.canvas.read_bytes() == before       # and not written
    assert set(_core_errors(paths.canvas)) == {"C-4"}


def test_rerun_after_repair_is_still_a_no_op(vault, tmp_path):
    """The repair converges: it happens once, and the second pass changes nothing on disk."""
    root, paths = _reviewed(vault, tmp_path)
    _obsidian_resave(paths.canvas)
    _collect(root, paths, tmp_path)
    after_first = paths.canvas.read_bytes()
    counts = _collect(root, paths, tmp_path)
    assert counts["edges_normalized"] == 0
    assert paths.canvas.read_bytes() == after_first


def test_deliberate_undirected_edge_survives_normalization(vault, tmp_path):
    """``toEnd: "none"`` is already explicit — a normalizer that "fixed" it would change meaning."""
    root, paths = _reviewed(vault, tmp_path)
    doc = json.loads(paths.canvas.read_text(encoding="utf-8"))
    assert doc.get("edges"), "fixture needs at least one edge"
    doc["edges"][0]["toEnd"] = "none"
    paths.canvas.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    _collect(root, paths, tmp_path)
    out = json.loads(paths.canvas.read_text(encoding="utf-8"))
    assert out["edges"][0]["toEnd"] == "none"


def test_no_normalize_opt_out_leaves_the_surface_alone(vault, tmp_path):
    """--no-normalize is an audit mode: it must not quietly repair what it is measuring."""
    root, paths = _reviewed(vault, tmp_path)
    _obsidian_resave(paths.canvas)
    counts = _collect(root, paths, tmp_path, normalize=False)
    assert counts["edges_normalized"] == 0
    assert set(_core_errors(paths.canvas)) == {"C-4"}


def test_dangling_edges_are_reported_and_never_repaired(vault, tmp_path):
    """⛔ The one class the collector must NOT touch.

    The single genuinely-unresolved edge found across 106 peer canvases took a history walk in
    another vault to rule on (its target had never existed as a node in any committed revision).
    No normalizer could have known that, which is exactly why this one reports and stops.
    """
    root, paths = _reviewed(vault, tmp_path)
    doc = json.loads(paths.canvas.read_text(encoding="utf-8"))
    doc["edges"].append({
        "id": "dangler", "fromNode": doc["nodes"][0]["id"], "toNode": "node_that_never_existed",
        "fromSide": "right", "toSide": "left", "toEnd": "arrow",
    })
    paths.canvas.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = _collect(root, paths, tmp_path)
    assert counts["edges_unresolved"] == 1
    out = json.loads(paths.canvas.read_text(encoding="utf-8"))
    assert any(e["id"] == "dangler" for e in out["edges"]), "the edge must survive — reported, not removed"
