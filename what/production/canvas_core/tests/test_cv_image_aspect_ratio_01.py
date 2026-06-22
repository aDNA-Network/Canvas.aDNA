"""Tests for canvas_core.traps.cv_image_aspect_ratio_01 (M-V1-2-G-02 O4)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.traps.cv_image_aspect_ratio_01 import check

PIL_AVAILABLE = True
try:
    from PIL import Image  # noqa: F401
except Exception:
    PIL_AVAILABLE = False


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _canvas(nodes: list[dict]) -> dict:
    return {"nodes": nodes, "edges": []}


def _group_node(id: str, x: float, y: float, w: float, h: float, label: str = "") -> dict:
    return {"id": id, "type": "group", "label": label,
            "x": x, "y": y, "width": w, "height": h}


def _image_node(
    id: str,
    x: float,
    y: float,
    width: float,
    height: float,
    file: str = "img.png",
) -> dict:
    return {"id": id, "type": "file", "file": file,
            "x": x, "y": y, "width": width, "height": height}


def _write_image(path: Path, w: int, h: int) -> None:
    """Write a tiny PNG of the given dimensions to *path* (no-op if PIL unavailable)."""
    from PIL import Image
    img = Image.new("RGB", (w, h), color=(128, 128, 128))
    img.save(path, format="PNG")


# ---------------------------------------------------------------------------
# Aspect drift (a)
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not PIL_AVAILABLE, reason="PIL required for aspect-drift tests")
class TestAspectDrift:
    def test_no_drift_no_fire(self, tmp_path):
        # Source 100x100 (1:1), rendered 200x200 (1:1) → 0% drift
        img_path = tmp_path / "a.png"
        _write_image(img_path, 100, 100)
        canvas = _canvas([
            _group_node("g1", 0, 0, 1000, 1000),
            _image_node("i1", 100, 100, 200, 200, file="a.png"),
        ])
        findings = check(canvas, asset_root=tmp_path)
        drifts = [f for f in findings if f.condition == "aspect_drift"]
        assert len(drifts) == 0

    def test_medium_drift_fires_medium(self, tmp_path):
        # Source 100x100 (1:1 = 1.0), rendered 200x150 (4:3 = 1.333) → drift ≈ 0.333
        # That's > 0.30 critical. Use smaller drift:
        # Source 100x100, rendered 110x100 (1.1) → drift = 0.1 → high (>0.05, >=not >0.15)
        # Actually we want medium: drift > 0.05 AND <= 0.15
        # Source 100x100, rendered 108x100 (1.08) → drift = 0.08 → medium
        img_path = tmp_path / "a.png"
        _write_image(img_path, 100, 100)
        canvas = _canvas([
            _group_node("g1", 0, 0, 1000, 1000),
            _image_node("i1", 100, 100, 108, 100, file="a.png"),
        ])
        findings = check(canvas, asset_root=tmp_path)
        drifts = [f for f in findings if f.condition == "aspect_drift"]
        assert len(drifts) == 1
        assert drifts[0].severity == "medium"

    def test_high_drift_fires_high(self, tmp_path):
        # Source 100x100, rendered 125x100 (1.25) → drift = 0.25 → high (>0.15)
        img_path = tmp_path / "a.png"
        _write_image(img_path, 100, 100)
        canvas = _canvas([
            _group_node("g1", 0, 0, 1000, 1000),
            _image_node("i1", 100, 100, 125, 100, file="a.png"),
        ])
        findings = check(canvas, asset_root=tmp_path)
        drifts = [f for f in findings if f.condition == "aspect_drift"]
        assert len(drifts) == 1
        assert drifts[0].severity == "high"

    def test_critical_drift_fires_critical(self, tmp_path):
        # Source 100x100, rendered 200x100 (2.0) → drift = 1.0 → critical
        img_path = tmp_path / "a.png"
        _write_image(img_path, 100, 100)
        canvas = _canvas([
            _group_node("g1", 0, 0, 1000, 1000),
            _image_node("i1", 100, 100, 200, 100, file="a.png"),
        ])
        findings = check(canvas, asset_root=tmp_path)
        drifts = [f for f in findings if f.condition == "aspect_drift"]
        assert len(drifts) == 1
        assert drifts[0].severity == "critical"


# ---------------------------------------------------------------------------
# Slot under-fill (b)
# ---------------------------------------------------------------------------


class TestSlotUnderfill:
    def test_hero_slot_underfill_fires(self):
        # Largest group is 1000x1000 = 1_000_000 area; hero threshold = 250_000
        # Parent slot 600x600 = 360_000 > 250_000 (hero)
        # Image 100x100 / 360_000 = 0.0278 < 0.20 → fires
        canvas = _canvas([
            _group_node("big", 0, 0, 1000, 1000, label="big container"),
            _group_node("slot", 50, 50, 600, 600, label="hero slot"),
            _image_node("img", 100, 100, 100, 100),
        ])
        findings = check(canvas)
        underfills = [f for f in findings if f.condition == "slot_underfill"]
        assert len(underfills) == 1
        assert underfills[0].severity == "medium"
        assert "img" in underfills[0].node_ids

    def test_non_hero_slot_no_fire(self):
        # Parent slot 200x200 = 40_000 < 250_000 (not hero); image 50x50 small
        # but slot is not hero-sized → no fire
        canvas = _canvas([
            _group_node("big", 0, 0, 1000, 1000),
            _group_node("small_slot", 0, 0, 200, 200),
            _image_node("img", 10, 10, 50, 50),
        ])
        findings = check(canvas)
        underfills = [f for f in findings if f.condition == "slot_underfill"]
        assert len(underfills) == 0

    def test_full_fill_no_fire(self):
        # Slot 500x500; image 480x480 covers ~92% → no underfill
        canvas = _canvas([
            _group_node("big", 0, 0, 1000, 1000),
            _group_node("slot", 0, 0, 500, 500),
            _image_node("img", 10, 10, 480, 480),
        ])
        findings = check(canvas)
        underfills = [f for f in findings if f.condition == "slot_underfill"]
        assert len(underfills) == 0


# ---------------------------------------------------------------------------
# Asset root resolution
# ---------------------------------------------------------------------------


class TestAssetRootResolution:
    def test_no_asset_root_skips_aspect_drift(self):
        """Without asset_root, aspect_drift sub-condition must be skipped."""
        canvas = _canvas([
            _group_node("g1", 0, 0, 1000, 1000),
            _image_node("i1", 100, 100, 200, 150),  # would drift if source known
        ])
        findings = check(canvas, asset_root=None)
        drifts = [f for f in findings if f.condition == "aspect_drift"]
        assert len(drifts) == 0

    def test_missing_file_silently_skips(self, tmp_path):
        """Asset_root set but file missing → no aspect_drift; no crash."""
        canvas = _canvas([
            _group_node("g1", 0, 0, 1000, 1000),
            _image_node("i1", 100, 100, 200, 150, file="nonexistent.png"),
        ])
        findings = check(canvas, asset_root=tmp_path)
        drifts = [f for f in findings if f.condition == "aspect_drift"]
        assert len(drifts) == 0

    @pytest.mark.skipif(not PIL_AVAILABLE, reason="PIL required")
    def test_string_asset_root_accepted(self, tmp_path):
        """asset_root as str (not Path) is accepted."""
        img_path = tmp_path / "a.png"
        _write_image(img_path, 100, 100)
        canvas = _canvas([
            _group_node("g1", 0, 0, 1000, 1000),
            _image_node("i1", 100, 100, 200, 100, file="a.png"),  # 2:1 → critical
        ])
        findings = check(canvas, asset_root=str(tmp_path))
        drifts = [f for f in findings if f.condition == "aspect_drift"]
        assert len(drifts) == 1


# ---------------------------------------------------------------------------
# R11 escalation
# ---------------------------------------------------------------------------


class TestR11Escalation:
    def test_r11_image_underfill_escalates(self):
        canvas = _canvas([
            _group_node("big", 0, 0, 1000, 1000),
            _group_node("slot", 50, 50, 600, 600),
            _image_node("img", 100, 100, 100, 100),
        ])
        findings = check(canvas, r11_node_ids={"img"})
        underfills = [f for f in findings if f.condition == "slot_underfill"]
        assert len(underfills) == 1
        assert underfills[0].severity == "high"  # escalated from medium

    @pytest.mark.skipif(not PIL_AVAILABLE, reason="PIL required")
    def test_r11_image_drift_escalates(self, tmp_path):
        img_path = tmp_path / "a.png"
        _write_image(img_path, 100, 100)
        canvas = _canvas([
            _group_node("g1", 0, 0, 1000, 1000),
            _image_node("i1", 100, 100, 108, 100, file="a.png"),  # medium drift
        ])
        findings = check(canvas, asset_root=tmp_path, r11_node_ids={"i1"})
        drifts = [f for f in findings if f.condition == "aspect_drift"]
        assert len(drifts) == 1
        assert drifts[0].severity == "high"  # escalated from medium


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_non_image_nodes_ignored(self):
        canvas = _canvas([
            _group_node("g1", 0, 0, 1000, 1000),
            {"id": "txt", "type": "text", "text": "hi",
             "x": 0, "y": 0, "width": 100, "height": 20},
        ])
        findings = check(canvas)
        assert len(findings) == 0

    def test_zero_width_image_no_div_by_zero(self):
        canvas = _canvas([
            _group_node("g1", 0, 0, 1000, 1000),
            _image_node("i1", 0, 0, 0, 0),
        ])
        # Must not raise
        findings = check(canvas)
        # No aspect/underfill possible with zero dims; assert no crash
        assert isinstance(findings, list)


# ---------------------------------------------------------------------------
# Substrate neutrality
# ---------------------------------------------------------------------------


class TestSubstrateNeutrality:
    def test_zero_application_imports(self):
        trap_path = os.path.join(
            os.path.dirname(__file__), "..", "traps",
            "cv_image_aspect_ratio_01.py",
        )
        with open(trap_path) as f:
            src = f.read()
        assert "canvas_presentation" not in src
        assert "canvas_comic" not in src
