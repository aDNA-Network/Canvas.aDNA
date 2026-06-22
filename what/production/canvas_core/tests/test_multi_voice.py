"""Tests for canvas_core.multi_voice productionization wire-up (M-V1-06 S3).

Covers the run_multi_voice_review() top-level entry-point, FakeVisionClient
deterministic mock, build_review_prompts() application-pluggable kwargs
(domain_noun + item_label per BV-3 S2 convention), r11_node_ids kwarg
threading per M-V1-05 uniform contract, severity aggregation, and end-to-end
SelectionRecord write via write_selection_record().

All tests use FakeVisionClient — no real LLM calls; CI-safe.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import json

import pytest

from canvas_core.multi_voice import (
    CANONICAL_VOICES,
    DEFAULT_SEVERITY_TO_SCORE,
    FakeVisionClient,
    MultiVoiceReport,
    MultiVoiceReviewer,
    ReviewerVoice,
    ReviewFinding,
    derive_vr_scores_from_report,
    run_multi_voice_review,
)
from canvas_core.rlhf.selection import (
    SelectionRecord,
    VariantInfo,
    validate_selection_record,
    write_selection_record,
)


# ---------------------------------------------------------------------------
# Fixture canvases
# ---------------------------------------------------------------------------


@pytest.fixture
def deck_canvas() -> dict:
    return {
        "nodes": [
            {"id": "title", "type": "text", "text": "Title slide"},
            {"id": "body", "type": "text", "text": "Body content"},
        ],
        "edges": [{"id": "e1", "fromNode": "title", "toNode": "body"}],
    }


@pytest.fixture
def comic_canvas() -> dict:
    return {
        "nodes": [
            {"id": "panel_1", "type": "file", "file": "panel_1.png"},
            {"id": "panel_2", "type": "file", "file": "panel_2.png"},
        ],
        "edges": [],
    }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestCanonicalVoices:
    def test_canonical_voices_count(self) -> None:
        """5 canonical reviewer voices (the substrate-default roster)."""
        assert len(CANONICAL_VOICES) == 5
        voice_ids = {v.voice_id for v in CANONICAL_VOICES}
        assert voice_ids == {
            "visual_quality",
            "narrative_coherence",
            "accessibility",
            "character_consistency",
            "compositional_balance",
        }


class TestBuildReviewPrompts:
    def test_returns_dict_with_voice_ids(self, deck_canvas: dict) -> None:
        """build_review_prompts() returns dict keyed by voice_id; each value
        is a non-empty string containing the voice's focus phrase."""
        reviewer = MultiVoiceReviewer()
        prompts = reviewer.build_review_prompts(deck_canvas)
        assert set(prompts.keys()) == {v.voice_id for v in CANONICAL_VOICES}
        for voice in CANONICAL_VOICES:
            assert prompts[voice.voice_id]
            assert voice.focus in prompts[voice.voice_id]

    def test_overlay_voice_appended_with_is_overlay_true(
        self, deck_canvas: dict
    ) -> None:
        """add_overlay_voice() appends + flips is_overlay True; prompts dict
        gains the overlay voice_id."""
        reviewer = MultiVoiceReviewer()
        community_voice = ReviewerVoice(
            voice_id="community_consent",
            name="Community Consent Critic",
            focus="Consent surfaces, opt-in/out clarity, attribution",
        )
        reviewer.add_overlay_voice(community_voice)
        assert community_voice.is_overlay is True
        assert "community_consent" in reviewer.voice_ids()
        prompts = reviewer.build_review_prompts(deck_canvas)
        assert "community_consent" in prompts


class TestRunMultiVoiceReview:
    def test_run_with_fake_client_invokes_all_voices(
        self, deck_canvas: dict
    ) -> None:
        """run_multi_voice_review() with FakeVisionClient returns a
        MultiVoiceReport listing all 5 voices in voices_invoked + 5 default
        observation findings (one per voice)."""
        client = FakeVisionClient()
        report = run_multi_voice_review(deck_canvas, client)
        assert set(report.voices_invoked) == {v.voice_id for v in CANONICAL_VOICES}
        assert len(report.findings) == 5
        assert report.observations == 5
        assert report.concerns == 0
        assert report.blockers == 0
        assert report.has_blockers is False

    def test_severity_aggregation_counters(self) -> None:
        """MultiVoiceReport.add() increments per-severity counters; has_blockers
        flips True when any blocker is present."""
        report = MultiVoiceReport()
        report.add(
            ReviewFinding(
                voice_id="visual_quality",
                severity="observation",
                finding="x",
            )
        )
        report.add(
            ReviewFinding(
                voice_id="narrative_coherence",
                severity="concern",
                finding="y",
            )
        )
        report.add(
            ReviewFinding(
                voice_id="accessibility",
                severity="blocker",
                finding="z",
            )
        )
        assert report.observations == 1
        assert report.concerns == 1
        assert report.blockers == 1
        assert report.has_blockers is True


class TestKwargThreading:
    def test_r11_node_ids_kwarg_threaded_through(self, deck_canvas: dict) -> None:
        """run_multi_voice_review() threads r11_node_ids into per-voice prompts;
        the gated node ids appear in the prompt body (Critical Rule 7
        honor-by-construction; M-V1-05 uniform kwarg contract)."""
        reviewer = MultiVoiceReviewer()
        prompts = reviewer.build_review_prompts(
            deck_canvas, r11_node_ids={"node_a", "node_b"}
        )
        for prompt in prompts.values():
            assert "R11 (Patient's Voice) gated nodes" in prompt
            assert "node_a" in prompt
            assert "node_b" in prompt

    def test_domain_noun_pluggability_for_comic(self, comic_canvas: dict) -> None:
        """domain_noun='comic page' + item_label='Page' overrides surface in
        the prompt body (matches BV-3 S2 application-pluggable convention)."""
        reviewer = MultiVoiceReviewer()
        prompts = reviewer.build_review_prompts(
            comic_canvas, domain_noun="comic page", item_label="Page"
        )
        first_prompt = next(iter(prompts.values()))
        assert "comic page canvas" in first_prompt
        assert "Reference items as 'Page'" in first_prompt
        assert "presentation slide" not in first_prompt
        assert "'Slide'" not in first_prompt

    def test_default_application_context_preserves_deck_language(
        self, deck_canvas: dict
    ) -> None:
        """Default kwargs leave deck-canonical wording intact."""
        reviewer = MultiVoiceReviewer()
        prompts = reviewer.build_review_prompts(deck_canvas)
        first_prompt = next(iter(prompts.values()))
        assert "presentation slide canvas" in first_prompt
        assert "Reference items as 'Slide'" in first_prompt


class TestFakeVisionClient:
    def test_voice_parse_failure_raises(self) -> None:
        """FakeVisionClient raises ValueError on a prompt without the voice
        prefix (R1 fail-loudly mitigation)."""
        client = FakeVisionClient()
        with pytest.raises(ValueError, match="cannot parse voice name"):
            client.analyze("garbage prompt with no voice prefix")

    def test_unknown_voice_name_raises(self) -> None:
        """FakeVisionClient raises ValueError when the prompt names a voice
        not registered with the client (registered = CANONICAL_VOICES by
        default)."""
        client = FakeVisionClient()
        with pytest.raises(ValueError, match="unknown voice name"):
            client.analyze("You are the Rogue Voice reviewer.\nFocus: ...")


class TestDeriveVrScoresFromReport:
    def test_observation_default_score_8_0(self, deck_canvas: dict) -> None:
        """Default mock report (5 observations, no concerns/blockers) produces
        vr_scores of 8.0 per voice (DEFAULT_SEVERITY_TO_SCORE['observation'])."""
        client = FakeVisionClient()
        report = run_multi_voice_review(deck_canvas, client)
        scores = derive_vr_scores_from_report(report)
        assert set(scores.keys()) == {v.voice_id for v in CANONICAL_VOICES}
        for score in scores.values():
            assert score == DEFAULT_SEVERITY_TO_SCORE["observation"]


class TestEndToEndSelectionRecord:
    def test_run_review_then_write_selection_record(
        self, deck_canvas: dict, tmp_path
    ) -> None:
        """End-to-end: drive canvas through 5 voices via FakeVisionClient,
        derive vr_scores, build SelectionRecord, write to disk via
        write_selection_record(); verify file exists, JSON roundtrips, and all
        5 voice_id keys appear in vr_scores."""
        client = FakeVisionClient()
        report = run_multi_voice_review(deck_canvas, client)
        vr_scores = derive_vr_scores_from_report(report)

        record = SelectionRecord(
            prompt="multi-voice review on test deck (mock)",
            register="R7",
            variants=[
                VariantInfo(
                    image_path="what/artifacts/h0_demos/deck_r7_investor_lattice_protocol.canvas",
                    model="canvas-static",
                    cost_usd=0.0,
                )
            ],
            pick_index=0,
            pick_reason="test smoke",
            approver_id="agent_test",
            vr_scores=vr_scores,
        )
        assert validate_selection_record(record) == []

        target = write_selection_record(record, tmp_path)
        assert target.exists()
        loaded = json.loads(target.read_text())
        assert set(loaded["vr_scores"].keys()) == {
            v.voice_id for v in CANONICAL_VOICES
        }
        assert loaded["selection_id"].startswith("sel_")
        # F-36: vault-relative path round-trip preserved
        assert not loaded["variants"][0]["image_path"].startswith("/")

    def test_write_selection_record_hard_fails_on_absolute_path(
        self, tmp_path
    ) -> None:
        """write_selection_record() raises ValueError listing schema violations
        when variants contain absolute paths (F-36 enforcement)."""
        record = SelectionRecord(
            prompt="x",
            register="R7",
            variants=[VariantInfo(image_path="/Users/foo/canvas.canvas")],
            pick_index=0,
            pick_reason="r",
            approver_id="a",
        )
        with pytest.raises(ValueError, match="vault-relative"):
            write_selection_record(record, tmp_path)
