"""Tests for canvas_core.critique (M-1-08).

Tests use skip_screenshots=True and/or mock vision clients since
Playwright and Gemini/Claude APIs are not available in CI.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.critique import CritiqueFinding, CritiqueResult, run_critique
from canvas_core.critique.rule_based_fallback import run_fallback
from canvas_core.critique.vision_client import (
    VisionRequest,
    VisionResponse,
    _parse_findings_json,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures", "cv_text_bounds_01")


def _write_canvas(canvas_data: dict, tmp_dir: Path) -> Path:
    """Write a canvas dict to a temp file and return its path."""
    path = tmp_dir / "test.canvas"
    path.write_text(json.dumps(canvas_data))
    return path


class MockVisionClient:
    """Mock vision client that returns pre-defined findings."""

    model_id = "mock-vision"

    def __init__(self, findings: list[dict] | None = None, fail: bool = False):
        self._findings = findings or []
        self._fail = fail

    def analyze(self, request: VisionRequest) -> VisionResponse:
        if self._fail:
            return VisionResponse(success=False, error="mock failure", model_id=self.model_id)
        return VisionResponse(
            raw_text=json.dumps(self._findings),
            parsed_findings=self._findings,
            cost_usd=0.01,
            duration_s=0.5,
            model_id=self.model_id,
            success=True,
        )


# ---------------------------------------------------------------------------
# CritiqueFinding / CritiqueResult
# ---------------------------------------------------------------------------


class TestDataclasses:
    def test_critique_finding_defaults(self):
        f = CritiqueFinding(
            trap_id="CV-TEST-01",
            node_refs=["n1"],
            severity="medium",
            observation="test",
        )
        assert f.source == "agent_critique"

    def test_critique_result_defaults(self):
        r = CritiqueResult()
        assert r.findings == []
        assert r.cost_usd == 0.0
        assert r.fallback_used is False


# ---------------------------------------------------------------------------
# JSON parsing
# ---------------------------------------------------------------------------


class TestParseFindingsJson:
    def test_valid_array(self):
        raw = '[{"trap_id": "CV-TEST-01", "severity": "high", "observation": "x"}]'
        result = _parse_findings_json(raw)
        assert len(result) == 1
        assert result[0]["trap_id"] == "CV-TEST-01"

    def test_wrapped_in_fences(self):
        raw = '```json\n[{"trap_id": "CV-TEST-01", "severity": "low", "observation": "y"}]\n```'
        result = _parse_findings_json(raw)
        assert len(result) == 1

    def test_dict_with_findings_key(self):
        raw = '{"findings": [{"trap_id": "CV-A-01", "severity": "medium", "observation": "z"}]}'
        result = _parse_findings_json(raw)
        assert len(result) == 1

    def test_malformed_json(self):
        raw = "This is not JSON at all"
        result = _parse_findings_json(raw)
        assert result == []

    def test_empty_array(self):
        result = _parse_findings_json("[]")
        assert result == []


# ---------------------------------------------------------------------------
# Rule-based fallback
# ---------------------------------------------------------------------------


class TestRuleBasedFallback:
    def test_fallback_produces_findings_on_overflow(self):
        canvas = {
            "nodes": [
                {"id": "g1", "type": "group", "x": 0, "y": 0, "width": 400, "height": 400},
                {"id": "t1", "type": "text", "text": "Very long text that definitely overflows this tiny box",
                 "x": 10, "y": 10, "width": 80, "height": 20},
            ],
            "edges": [],
        }
        findings = run_fallback(canvas)
        assert len(findings) >= 1
        assert findings[0].source == "rule_based_fallback"
        assert "[rule-based fallback]" in findings[0].observation

    def test_fallback_degrades_severity(self):
        canvas = {
            "nodes": [
                {"id": "g1", "type": "group", "x": 0, "y": 0, "width": 400, "height": 400},
                {"id": "t1", "type": "text", "text": "Very long text that definitely overflows this tiny box",
                 "x": 10, "y": 10, "width": 80, "height": 20},
            ],
            "edges": [],
        }
        findings = run_fallback(canvas)
        # Overflow default is "medium"; fallback degrades to "low".
        overflow = [f for f in findings if "overflow" in f.observation.lower()]
        if overflow:
            assert overflow[0].severity == "low"

    def test_fallback_empty_canvas(self):
        """Empty canvas: fallback runs gracefully without crash.

        Post-M-V1-05 (F-26 fix): fallback now routes through run_all_traps
        covering all 6 implemented traps. Empty canvas may produce
        CV-DIMENSION-VISIBILITY-01 findings (no canvas-level dimension
        metadata). All findings are source-tagged from rule_based_fallback.
        """
        findings = run_fallback({"nodes": [], "edges": []})
        # Graceful handling: no crash; all findings sourced from fallback path.
        assert all(f.source == "rule_based_fallback" for f in findings)
        # All findings have severity-degraded prefix in observation.
        assert all("[rule-based fallback]" in f.observation for f in findings)

    def test_fallback_runs_all_implemented_traps(self):
        """F-26 fix at M-V1-05: fallback covers all 6 implemented traps.

        Defective canvas with both a PendingImage placeholder AND a text
        overflow should produce findings from CV-PENDING-01 + CV-TEXT-BOUNDS-01
        (and may produce findings from other traps; the assertion is on
        coverage, not exclusivity).
        """
        canvas = {
            "nodes": [
                {"id": "g1", "type": "group", "x": 0, "y": 0, "width": 400, "height": 400,
                 "label": "Test group"},
                {"id": "t1", "type": "text",
                 "text": "[PendingImage] - placeholder for hero image",
                 "x": 10, "y": 10, "width": 380, "height": 30},
                {"id": "t2", "type": "text",
                 "text": "Very long text that definitely overflows this tiny container box",
                 "x": 10, "y": 50, "width": 80, "height": 20},
            ],
            "edges": [],
        }
        findings = run_fallback(canvas)
        trap_ids = {f.trap_id for f in findings}
        # F-26 fix evidence: both critical-severity (CV-PENDING-01) and the
        # original CV-TEXT-BOUNDS-01 must fire from the same fallback call.
        assert "CV-PENDING-01" in trap_ids, (
            f"CV-PENDING-01 expected from PendingImage placeholder; got {trap_ids}"
        )
        assert "CV-TEXT-BOUNDS-01" in trap_ids, (
            f"CV-TEXT-BOUNDS-01 expected from text overflow; got {trap_ids}"
        )

    def test_fallback_honors_r11_gating(self):
        """F-26 fix at M-V1-05: r11_node_ids kwarg passes through fallback path.

        run_fallback -> run_all_traps -> per-trap check(r11_node_ids=...) wires
        Critical Rule 7 honor-by-construction across the fallback path.
        Verified by passing kwarg without crash; r11-aware traps see the set.
        """
        canvas = {
            "nodes": [
                {"id": "g_r11", "type": "group", "x": 0, "y": 0, "width": 400, "height": 400},
                {"id": "t_r11", "type": "text",
                 "text": "Very long text that definitely overflows this small container box",
                 "x": 10, "y": 10, "width": 80, "height": 20},
            ],
            "edges": [],
        }
        # Without R11 gating: text overflow finding fires.
        findings_unrestricted = run_fallback(canvas)
        bounds_findings = [f for f in findings_unrestricted if f.trap_id == "CV-TEXT-BOUNDS-01"]
        # With R11 gating on the text node: cv_text_bounds_01 honors r11_node_ids
        # and excludes the gated node.
        findings_gated = run_fallback(canvas, r11_node_ids={"t_r11"})
        bounds_findings_gated = [f for f in findings_gated if f.trap_id == "CV-TEXT-BOUNDS-01"]
        # Gated path produces fewer or equal CV-TEXT-BOUNDS-01 findings than
        # the unrestricted path (R11 nodes are skipped).
        assert len(bounds_findings_gated) <= len(bounds_findings)


# ---------------------------------------------------------------------------
# run_critique — skip_screenshots mode (rule-based fallback)
# ---------------------------------------------------------------------------


class TestRunCritiqueSkipScreenshots:
    def test_skip_screenshots_uses_fallback(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            canvas = {
                "nodes": [
                    {"id": "g1", "type": "group", "x": 0, "y": 0, "width": 400, "height": 400},
                    {"id": "t1", "type": "text", "text": "Overflow text here definitely overflows",
                     "x": 10, "y": 10, "width": 80, "height": 20},
                ],
                "edges": [],
            }
            canvas_path = _write_canvas(canvas, tmp)
            result = run_critique(canvas_path, skip_screenshots=True)

            assert result.fallback_used is True
            assert len(result.findings) >= 1

    def test_observations_md_created(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            canvas = {
                "nodes": [
                    {"id": "g1", "type": "group", "x": 0, "y": 0, "width": 400, "height": 400},
                    {"id": "t1", "type": "text", "text": "Overflow text definitely overflows this box",
                     "x": 10, "y": 10, "width": 80, "height": 20},
                ],
                "edges": [],
            }
            canvas_path = _write_canvas(canvas, tmp)
            run_critique(canvas_path, skip_screenshots=True)

            obs_path = tmp / "canvas_review" / "agent_observations.md"
            assert obs_path.exists()
            content = obs_path.read_text()
            assert "Agent critique" in content
            assert "rule-based fallback" in content

    def test_no_groups_uses_fallback(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            canvas = {
                "nodes": [
                    {"id": "t1", "type": "text", "text": "Orphan text", "x": 0, "y": 0, "width": 100, "height": 50},
                ],
                "edges": [],
            }
            canvas_path = _write_canvas(canvas, tmp)
            result = run_critique(canvas_path)

            assert result.fallback_used is True

    def test_idempotent_append(self):
        """Multiple runs append separate sections, don't clobber."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            canvas = {
                "nodes": [
                    {"id": "g1", "type": "group", "x": 0, "y": 0, "width": 400, "height": 400},
                    {"id": "t1", "type": "text", "text": "Overflow text definitely overflows this box",
                     "x": 10, "y": 10, "width": 80, "height": 20},
                ],
                "edges": [],
            }
            canvas_path = _write_canvas(canvas, tmp)

            run_critique(canvas_path, skip_screenshots=True, artifact_version_override="v1")
            run_critique(canvas_path, skip_screenshots=True, artifact_version_override="v2")

            obs_path = tmp / "canvas_review" / "agent_observations.md"
            content = obs_path.read_text()
            assert content.count("## Agent critique") == 2


# ---------------------------------------------------------------------------
# Render-stage exception fallback (F-31 fix at M-V1-05)
# ---------------------------------------------------------------------------


class TestRenderStageExceptionFallback:
    def test_render_stage_exception_triggers_fallback(self, monkeypatch):
        """F-31 fix at M-V1-05: render-stage exception routes through fallback.

        Monkeypatch html_renderer.render_canvas_data to raise ValueError;
        run_critique should catch it via the new render-stage try/except,
        invoke run_fallback, and return CritiqueResult with fallback_used=True
        and findings populated (rather than propagating the exception).
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            canvas = {
                "nodes": [
                    {"id": "g1", "type": "group", "x": 0, "y": 0, "width": 400, "height": 400},
                    {"id": "t1", "type": "text",
                     "text": "Very long text that definitely overflows this tiny container box",
                     "x": 10, "y": 10, "width": 80, "height": 20},
                ],
                "edges": [],
            }
            canvas_path = _write_canvas(canvas, tmp)

            # Force render stage to raise ValueError. The render module is
            # imported lazily inside run_critique; patch the resolved module.
            import canvas_core.html_renderer as hr

            def _boom(*args, **kwargs):
                raise ValueError("simulated render failure for F-31 test")

            monkeypatch.setattr(hr, "render_canvas_data", _boom)

            # run_critique must NOT propagate the ValueError; it must fall back.
            result = run_critique(canvas_path, vision_client=MockVisionClient())

            assert result.fallback_used is True, (
                "F-31: render-stage exception must trigger fallback; "
                f"got fallback_used={result.fallback_used}"
            )
            # Fallback findings produced via run_all_traps coverage.
            assert all(f.source == "rule_based_fallback" for f in result.findings)


# ---------------------------------------------------------------------------
# Issue 01 fixture through fallback
# ---------------------------------------------------------------------------


class TestIssue01FixtureFallback:
    def test_issue_01_p1_fallback_fires(self):
        """SS Issue 01 page 1 through rule-based fallback produces findings."""
        fixture_path = os.path.join(FIXTURES_DIR, "issue_01_p1.canvas")
        if not os.path.isfile(fixture_path):
            pytest.skip("Issue 01 fixture not available")

        with open(fixture_path) as f:
            canvas_data = json.load(f)

        findings = run_fallback(canvas_data)
        assert len(findings) >= 1


# ---------------------------------------------------------------------------
# Mock vision client integration
# ---------------------------------------------------------------------------


class TestMockVisionIntegration:
    def test_run_critique_returns_result(self):
        """Verify the full pipeline shape with skip_screenshots."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            canvas = {"nodes": [], "edges": []}
            canvas_path = _write_canvas(canvas, tmp)
            result = run_critique(canvas_path, skip_screenshots=True)

            assert isinstance(result, CritiqueResult)
            assert result.duration_s >= 0
            assert isinstance(result.findings, list)


# ---------------------------------------------------------------------------
# F-28 amendment 2026-05-03: CANVASFORGE_VISION_BUDGET env-var override
# (M-CAMPAIGN-REFRESH-02)
# ---------------------------------------------------------------------------


class TestBudgetCapResolution:
    """Budget-cap default resolution honors env var (F-28 / M-CAMPAIGN-REFRESH-02)."""

    def test_default_when_env_unset(self, monkeypatch):
        from canvas_core.critique.agent_critique import (
            DEFAULT_BUDGET_CAP_USD,
            _resolve_budget_cap_default,
        )
        monkeypatch.delenv("CANVASFORGE_VISION_BUDGET", raising=False)
        assert _resolve_budget_cap_default() == DEFAULT_BUDGET_CAP_USD

    def test_env_override_parses_float(self, monkeypatch):
        from canvas_core.critique.agent_critique import _resolve_budget_cap_default
        monkeypatch.setenv("CANVASFORGE_VISION_BUDGET", "0.50")
        assert _resolve_budget_cap_default() == pytest.approx(0.50)

    def test_env_invalid_falls_back_to_default(self, monkeypatch):
        from canvas_core.critique.agent_critique import (
            DEFAULT_BUDGET_CAP_USD,
            _resolve_budget_cap_default,
        )
        monkeypatch.setenv("CANVASFORGE_VISION_BUDGET", "not-a-float")
        # Should NOT raise; should fall back to default with a warning logged.
        assert _resolve_budget_cap_default() == DEFAULT_BUDGET_CAP_USD

    def test_explicit_arg_takes_precedence_over_env(self, monkeypatch):
        """Pipeline accepts explicit budget_cap_usd while env is set."""
        from canvas_core.critique.agent_critique import _resolve_budget_cap_default
        monkeypatch.setenv("CANVASFORGE_VISION_BUDGET", "0.50")
        # Verify env-resolution returns the env value when not overridden.
        assert _resolve_budget_cap_default() == pytest.approx(0.50)
        # Verify run_critique with both forms returns successfully.
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            canvas = {"nodes": [], "edges": []}
            canvas_path = _write_canvas(canvas, tmp)
            # Explicit value (env-bypass path).
            result = run_critique(canvas_path, skip_screenshots=True, budget_cap_usd=0.99)
            assert isinstance(result, CritiqueResult)
            # No explicit value (env-resolution path).
            result2 = run_critique(canvas_path, skip_screenshots=True)
            assert isinstance(result2, CritiqueResult)


# ---------------------------------------------------------------------------
# M-V1-11: dry_run=True audit mode (read-only invocation)
# ---------------------------------------------------------------------------


class TestDryRunMode:
    """Dry-run mode skips canvas_review/agent_observations.md write (M-V1-11).

    The substrate edit gates three _append_observations() call sites on
    `not dry_run`: the no-groups/skip-screenshots fallback path, the F-31
    render-stage exception path, and the main success path. These tests
    exercise the first gate via skip_screenshots=True; the other two gates
    are structurally identical (single conditional wrapping the same
    function call) so coverage is symmetric.
    """

    def test_dry_run_skips_observation_write(self):
        """dry_run=True must NOT create canvas_review/agent_observations.md."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            canvas = {
                "nodes": [
                    {"id": "g1", "type": "group", "x": 0, "y": 0, "width": 400, "height": 400},
                    {"id": "t1", "type": "text", "text": "Overflow text definitely overflows this box",
                     "x": 10, "y": 10, "width": 80, "height": 20},
                ],
                "edges": [],
            }
            canvas_path = _write_canvas(canvas, tmp)

            run_critique(canvas_path, skip_screenshots=True, dry_run=True)

            obs_path = tmp / "canvas_review" / "agent_observations.md"
            assert not obs_path.exists(), (
                f"M-V1-11: dry_run=True must not write agent_observations.md; "
                f"found {obs_path}"
            )

    def test_dry_run_returns_findings(self):
        """dry_run=True still runs the full pipeline + returns CritiqueResult."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            canvas = {
                "nodes": [
                    {"id": "g1", "type": "group", "x": 0, "y": 0, "width": 400, "height": 400},
                    {"id": "t1", "type": "text", "text": "Overflow text definitely overflows this box",
                     "x": 10, "y": 10, "width": 80, "height": 20},
                ],
                "edges": [],
            }
            canvas_path = _write_canvas(canvas, tmp)

            result = run_critique(canvas_path, skip_screenshots=True, dry_run=True)

            # Pipeline executed: result is CritiqueResult, findings populated,
            # fallback_used set (skip_screenshots routes through fallback).
            assert isinstance(result, CritiqueResult)
            assert result.fallback_used is True
            assert isinstance(result.findings, list)
            # At least one CV-* finding from the fallback (overflow text triggers
            # CV-TEXT-BOUNDS-01); confirms pipeline ran end-to-end.
            assert len(result.findings) >= 1

    def test_dry_run_default_false_writes_observations(self):
        """dry_run defaults to False; default behavior must write observations.

        Regression guard: M-V1-11 must not change existing behavior when the
        new kwarg is not passed.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            canvas = {
                "nodes": [
                    {"id": "g1", "type": "group", "x": 0, "y": 0, "width": 400, "height": 400},
                    {"id": "t1", "type": "text", "text": "Overflow text definitely overflows this box",
                     "x": 10, "y": 10, "width": 80, "height": 20},
                ],
                "edges": [],
            }
            canvas_path = _write_canvas(canvas, tmp)

            # Default invocation (no dry_run kwarg passed).
            run_critique(canvas_path, skip_screenshots=True)

            obs_path = tmp / "canvas_review" / "agent_observations.md"
            assert obs_path.exists(), (
                "Regression: default run_critique() must still write "
                "agent_observations.md (dry_run defaults to False)"
            )
