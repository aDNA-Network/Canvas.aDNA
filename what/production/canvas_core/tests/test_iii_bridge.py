"""Tests for canvas_core.rlhf.iii_bridge (Pillar E HITL RLHF bridge).

Covers the selection-record → ADR-005 §2 signal mapping + the local-store
ACCUMULATE writer. Single-vault start per ``campaign_canvasforge_v1_2``
mission M-V1-2-E-01; no canonical-store touches.

Re-merge rationale (CR7+SO7):
``lattice-labs/who/coordination/coord_2026_04_16_forge_split.md``.

Created in M-V1-2-E-01 S1.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.rlhf import iii_bridge
from canvas_core.rlhf.iii_bridge import (
    ENTRY_ID_PREFIX,
    RLHF_SIGNAL_TYPE_ACCEPT,
    TRAP_IMAGE_GENERATION_VARIANT_PICK,
    _derive_entry_id,
    _derive_pattern,
    _normalize_iso8601_utc,
    accumulate,
    accumulate_directory,
    selection_to_iii_signal,
)
from canvas_core.rlhf.selection import SelectionRecord, VariantInfo

# Five Schema-A fixture records ship under what/artifacts/image_gen_dataset/2026-05/.
# Use the canonical Wilhelm cover record as the primary smoke fixture.
_CORPUS_DIR = iii_bridge.DEFAULT_CORPUS_DIR
_FIXTURE_PATH = _CORPUS_DIR / "sel_20260514_064421_814d.json"

# ADR-005 §2 required-min field names.
_REQUIRED_MIN = {"rlhf_signal_type", "rlhf_session_id", "rlhf_captured_at"}

# ADR-005 §2 ISO 8601 Z-suffixed UTC pattern.
_ISO_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


def _load_fixture(name: str = "sel_20260514_064421_814d.json") -> SelectionRecord:
    return SelectionRecord.from_dict(json.loads((_CORPUS_DIR / name).read_text()))


def _make_min_record(**overrides) -> SelectionRecord:
    base = dict(
        prompt="Editorial illustration",
        register="R1",
        variants=[
            VariantInfo(image_path="what/artifacts/test/v1.png"),
            VariantInfo(image_path="what/artifacts/test/v2.png"),
        ],
        pick_index=0,
        pick_reason="Composition wins on first pass",
        approver_id="stanley",
        selection_id="sel_20260101_000000_abcd",
        timestamp="2026-01-01T00:00:00+00:00",
    )
    base.update(overrides)
    return SelectionRecord(**base)


# ---------------------------------------------------------------------------
# Mapper — ADR-005 §2 conformance
# ---------------------------------------------------------------------------


class TestMapperRequiredMin:
    """ADR-005 §2 required-minimum field set."""

    def test_smoke_all_three_required_min_present(self):
        sel = _load_fixture()
        sig = selection_to_iii_signal(sel, session_id="session_test")
        assert _REQUIRED_MIN.issubset(sig.keys())

    def test_rlhf_signal_type_is_accept(self):
        sig = selection_to_iii_signal(_make_min_record(), session_id="session_test")
        assert sig["rlhf_signal_type"] == RLHF_SIGNAL_TYPE_ACCEPT
        assert sig["rlhf_signal_type"] == "accept"

    def test_rlhf_session_id_is_passthrough(self):
        sig = selection_to_iii_signal(_make_min_record(), session_id="session_alpha")
        assert sig["rlhf_session_id"] == "session_alpha"

    def test_rlhf_captured_at_iso8601_z_suffix(self):
        sig = selection_to_iii_signal(_make_min_record(), session_id="session_test")
        assert _ISO_Z.match(sig["rlhf_captured_at"]), sig["rlhf_captured_at"]


class TestMapperOptionalOpen:
    """ADR-005 §2 optional-open fields."""

    def test_reviewer_persona_populated_from_approver_id(self):
        sel = _make_min_record(approver_id="herb")
        sig = selection_to_iii_signal(sel, session_id="session_test")
        assert sig["rlhf_reviewer_persona"] == "herb"


class TestMapperConsumerNamespace:
    """ADR-005 §3 consumer-namespace boundary — vault-local fields stay nested."""

    def test_consumer_namespace_is_nested_object(self):
        sig = selection_to_iii_signal(_make_min_record(), session_id="s")
        cns = sig["rlhf_consumer_namespace"]
        assert isinstance(cns, dict)
        assert "canvasforge" in cns
        assert "image_generation" in cns["canvasforge"]
        assert isinstance(cns["canvasforge"]["image_generation"], dict)

    def test_no_dotted_consumer_namespace_keys_at_top_level(self):
        """ADR-005 §3 rule 5 boundary: nested-object form, never flat dotted keys at top level."""
        sig = selection_to_iii_signal(_make_min_record(), session_id="s")
        for key in sig:
            assert not key.startswith("rlhf_consumer_namespace."), key

    def test_no_consumer_namespace_leak_into_top_level_rlhf(self):
        """ADR-005 §3 rule 5: namespace data lives only under rlhf_consumer_namespace."""
        sel = _load_fixture()
        sig = selection_to_iii_signal(sel, session_id="s")
        # The full sel projection lives under the namespace; verify it does NOT
        # also appear as top-level rlhf_* keys.
        ig = sig["rlhf_consumer_namespace"]["canvasforge"]["image_generation"]
        assert ig["selection_id"] == sel.selection_id
        assert ig["pick_reason"] == sel.pick_reason
        assert "selection_id" not in sig  # no top-level leak
        assert "pick_reason" not in sig
        assert "vr_scores" not in sig
        assert "prompt" not in sig

    def test_consumer_namespace_carries_full_projection(self):
        sel = _load_fixture()
        sig = selection_to_iii_signal(sel, session_id="s")
        ig = sig["rlhf_consumer_namespace"]["canvasforge"]["image_generation"]
        # Spot-check the rich data made it through unmodified.
        assert ig["prompt"] == sel.prompt
        assert ig["register"] == sel.register
        assert ig["pick_index"] == sel.pick_index
        assert ig["pick_reason"] == sel.pick_reason
        assert ig["vr_scores"] == sel.vr_scores
        assert ig["selected_variant_path"] == sel.variants[sel.pick_index].image_path


# ---------------------------------------------------------------------------
# Mapper — ADR-003 §4 base correction fields
# ---------------------------------------------------------------------------


class TestMapperBaseFields:
    """ADR-003 §4 base correction fields populated on every emitted entry."""

    def test_id_prefix_and_selection_id(self):
        sel = _make_min_record(selection_id="sel_20260101_000000_abcd")
        sig = selection_to_iii_signal(sel, session_id="s")
        assert sig["id"] == f"{ENTRY_ID_PREFIX}sel_20260101_000000_abcd"
        # Idempotency precondition: same selection_id → same entry id.
        assert _derive_entry_id(sel.selection_id) == sig["id"]

    def test_trap_is_vault_local_image_gen_pick(self):
        sig = selection_to_iii_signal(_make_min_record(), session_id="s")
        assert sig["trap"] == TRAP_IMAGE_GENERATION_VARIANT_PICK
        assert sig["trap"] == "image_generation_variant_pick"

    def test_pattern_deterministic(self):
        sig1 = selection_to_iii_signal(_make_min_record(), session_id="s")
        sig2 = selection_to_iii_signal(_make_min_record(), session_id="s")
        assert sig1["pattern"] == sig2["pattern"]
        # Pattern surface shape: snake_case, starts with image_gen_pick_.
        assert sig1["pattern"].startswith("image_gen_pick_")
        assert re.match(r"^[a-z0-9_]+$", sig1["pattern"])

    def test_pattern_distinguishes_registers(self):
        a = _make_min_record(register="R1", pick_reason="cover-grade composition")
        b = _make_min_record(register="R3", pick_reason="cover-grade composition")
        sig_a = selection_to_iii_signal(a, session_id="s")
        sig_b = selection_to_iii_signal(b, session_id="s")
        assert sig_a["pattern"] != sig_b["pattern"]

    def test_pattern_collapses_by_register_equivalence_class(self):
        # ADR-007 §3 footnote + M-V1-2-F-01 S2 F-E-01.S2.B: ``pattern`` is the
        # register-equivalence-class identifier. Picks within the same register
        # collapse to one pattern by design, even when pick_reason text
        # differs. Per-pick uniqueness lives on ``id`` (selection_id-derived;
        # see ``test_id_prefix_and_selection_id``).
        a = _make_min_record(register="R1", pick_reason="cover-grade composition")
        c = _make_min_record(register="R1", pick_reason="contrast-clarity wins")
        sig_a = selection_to_iii_signal(a, session_id="s")
        sig_c = selection_to_iii_signal(c, session_id="s")
        assert sig_a["pattern"] == sig_c["pattern"]

    def test_frequency_and_accepted(self):
        sig = selection_to_iii_signal(_make_min_record(), session_id="s")
        assert sig["frequency"] == 1
        assert sig["accepted"] is True

    def test_created_is_yyyy_mm_dd(self):
        sig = selection_to_iii_signal(_make_min_record(), session_id="s")
        assert re.match(r"^\d{4}-\d{2}-\d{2}$", sig["created"])


# ---------------------------------------------------------------------------
# Mapper — schema discipline
# ---------------------------------------------------------------------------


class TestMapperValidation:
    """Schema-violation discipline — hard-fail per selection.py doctrine."""

    def test_raises_on_invalid_record(self):
        bad = _make_min_record(approver_id="")  # validate_selection_record flags this
        with pytest.raises(ValueError, match="schema violations"):
            selection_to_iii_signal(bad, session_id="s")

    def test_raises_on_out_of_range_pick_index(self):
        # Two variants; pick_index 5 is out of range.
        bad = _make_min_record(pick_index=5)
        with pytest.raises(ValueError, match="pick_index"):
            selection_to_iii_signal(bad, session_id="s")


# ---------------------------------------------------------------------------
# Mapper — top-level key envelope
# ---------------------------------------------------------------------------


class TestMapperTopLevelEnvelope:
    """Top-level keys are exactly the expected set — guard against drift."""

    def test_expected_top_level_keys_only(self):
        sel = _load_fixture()  # has approver_id → rlhf_reviewer_persona present
        sig = selection_to_iii_signal(sel, session_id="s")
        expected = {
            # ADR-003 §4 base
            "id", "trap", "pattern", "description", "example",
            "source_review", "source_finding", "frequency", "accepted", "created",
            # ADR-005 §2 required-min
            "rlhf_signal_type", "rlhf_session_id", "rlhf_captured_at",
            # ADR-005 §2 optional-open (only present when approver_id is)
            "rlhf_reviewer_persona",
            # ADR-005 §3 namespace
            "rlhf_consumer_namespace",
        }
        assert set(sig.keys()) == expected


# ---------------------------------------------------------------------------
# Accumulate — append-only writer with idempotency
# ---------------------------------------------------------------------------


class TestAccumulate:
    """ACCUMULATE writes to the local learning store; idempotent on selection_id."""

    def test_first_write_appends_line(self, tmp_path: Path):
        store = tmp_path / "store.jsonl"
        sig = selection_to_iii_signal(_make_min_record(), session_id="s")
        wrote = accumulate(sig, store_path=store)
        assert wrote is True
        assert store.exists()
        lines = store.read_text().strip().splitlines()
        assert len(lines) == 1
        roundtrip = json.loads(lines[0])
        assert roundtrip == sig

    def test_second_write_idempotent_no_new_line(self, tmp_path: Path):
        store = tmp_path / "store.jsonl"
        sig = selection_to_iii_signal(_make_min_record(), session_id="s")
        assert accumulate(sig, store_path=store) is True
        assert accumulate(sig, store_path=store) is False
        assert len(store.read_text().strip().splitlines()) == 1

    def test_raises_when_signal_lacks_selection_id(self, tmp_path: Path):
        store = tmp_path / "store.jsonl"
        bad = {"rlhf_signal_type": "accept", "rlhf_session_id": "s", "rlhf_captured_at": "2026-01-01T00:00:00Z"}
        with pytest.raises(ValueError, match="selection_id"):
            accumulate(bad, store_path=store)
        assert not store.exists()

    def test_appends_alongside_pre_existing_legacy_entries(self, tmp_path: Path):
        """G-01 F3-migrated entries don't carry consumer-namespace selection_id;
        accumulate skips them for idempotency but still appends new entries."""
        store = tmp_path / "store.jsonl"
        legacy = {
            "id": "C-NEW-2026-05-23-A",
            "title": "Pre-existing legacy entry",
            "rlhf_signal_type": "accept_with_modification",
            "rlhf_session_id": "session_g_01",
            "rlhf_captured_at": "2026-05-23T12:00:00Z",
            "rlhf_consumer_namespace": {"canvasforge": {"original_type": "check"}},
        }
        store.write_text(json.dumps(legacy) + "\n")
        sig = selection_to_iii_signal(_make_min_record(), session_id="s")
        assert accumulate(sig, store_path=store) is True
        lines = store.read_text().strip().splitlines()
        assert len(lines) == 2


# ---------------------------------------------------------------------------
# accumulate_directory — fixture-corpus end-to-end
# ---------------------------------------------------------------------------


class TestAccumulateDirectory:
    """End-to-end scan of the M-V1-VAL-01 corpus."""

    def test_scans_five_schema_a_records_skips_two_schema_c(self, tmp_path: Path):
        store = tmp_path / "store.jsonl"
        report = accumulate_directory(
            _CORPUS_DIR, session_id="session_test", store_path=store
        )
        assert len(report["accumulated"]) == 5, report
        assert len(report["skipped_duplicate"]) == 0, report
        # Two SS character-round records are Schema-C (visual-style RLHF
        # runner shape) and are correctly skipped.
        assert len(report["skipped_non_schema_a"]) == 2, report
        for name in report["skipped_non_schema_a"]:
            assert name.startswith("sel_ss_character_round_"), name

    def test_second_run_is_idempotent(self, tmp_path: Path):
        store = tmp_path / "store.jsonl"
        first = accumulate_directory(
            _CORPUS_DIR, session_id="session_test", store_path=store
        )
        before = len(store.read_text().strip().splitlines())
        second = accumulate_directory(
            _CORPUS_DIR, session_id="session_test_redux", store_path=store
        )
        after = len(store.read_text().strip().splitlines())
        assert before == after, (before, after)
        assert len(second["accumulated"]) == 0
        assert len(second["skipped_duplicate"]) == len(first["accumulated"])


# ---------------------------------------------------------------------------
# Helper coverage — timestamp + id derivation primitives
# ---------------------------------------------------------------------------


class TestHelpers:
    """Low-level helper invariants."""

    def test_normalize_iso8601_z_strips_microseconds_and_offset(self):
        assert _normalize_iso8601_utc("2026-05-14T06:44:21.502227+00:00") == "2026-05-14T06:44:21Z"

    def test_normalize_iso8601_z_handles_naive_as_utc(self):
        # Naive timestamp is treated as UTC (matches selection.py default).
        assert _normalize_iso8601_utc("2026-05-14T06:44:21") == "2026-05-14T06:44:21Z"

    def test_normalize_iso8601_z_converts_non_utc_offsets(self):
        # PDT = UTC-7; 13:44 PDT == 20:44 UTC.
        assert _normalize_iso8601_utc("2026-05-14T13:44:21-07:00") == "2026-05-14T20:44:21Z"

    def test_derive_pattern_normalizes_register_punctuation(self):
        # The Wilhelm cover register carries '+' which must become '_'.
        p = _derive_pattern("R1+R3_implied_no_R11_on_cover")
        assert "+" not in p
        assert " " not in p
        # Equivalence-class semantics (ADR-007 §3 footnote): no per-pick suffix.
        assert p == "image_gen_pick_r1_r3_implied_no_r11_on_cover"
