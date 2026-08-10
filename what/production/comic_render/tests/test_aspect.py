"""Geometry-derived aspect (H3) — the 2026-08-04 ruling, and the honest limits of it.

The named regression case is the mini-issue splash: it declares ``3:4`` and is drawn 663x1025.
That gap is what ``CV-IMAGE-ASPECT-RATIO-01`` caught on the H2 render, and it is what these tests
exist to keep caught.
"""

from __future__ import annotations

import math

import pytest

from comic_render.aspect import (
    DEFAULT_SUPPORTED,
    SNAP_WARN_THRESHOLD,
    drift_report,
    effective_for,
    parse_ratio,
    ratio_error,
    snap,
)
from comic_render.backends import supported_aspects_for
from comic_render.extract import plan

# The real geometry, straight off the fixture's nodes.
SPLASH_W, SPLASH_H = 663, 1025
WIDE_W, WIDE_H = 638, 326
SQUARE_W, SQUARE_H = 314, 326


class TestParsing:
    @pytest.mark.parametrize(
        "spec,expected",
        [("1:1", 1.0), ("16:9", 16 / 9), ("9:16", 0.5625), ("3:4", 0.75), ("4:3", 4 / 3)],
    )
    def test_parses_the_supported_menu(self, spec, expected):
        assert parse_ratio(spec) == pytest.approx(expected)

    @pytest.mark.parametrize("bad", [None, "", "16", "16:0", "0:9", "wide", "a:b", "-1:2"])
    def test_unparseable_input_returns_none_never_raises(self, bad):
        # Author-supplied qualities reach this directly; a malformed one must degrade, not crash.
        assert parse_ratio(bad) is None


class TestErrorMetric:
    def test_is_scale_symmetric(self):
        # The whole reason for log space: doubling and halving are the same amount of wrong.
        assert ratio_error(2.0, 1.0) == pytest.approx(ratio_error(1.0, 0.5))

    def test_identical_ratios_have_zero_error(self):
        assert ratio_error(1.5, 1.5) == 0.0


class TestSnap:
    def test_splash_geometry_snaps_away_from_its_declaration(self):
        # THE regression case. Declared 3:4 (0.750); drawn 0.647; nearest supported is 9:16.
        spec, err = snap(SPLASH_W / SPLASH_H)
        assert spec == "9:16"
        assert err == pytest.approx(0.140, abs=0.001)

    def test_wide_panel_keeps_its_label_but_not_its_shape(self):
        # Declared 16:9 and snapped to 16:9 — yet drawn at 1.957, ~9.6% off. The label being
        # right is not the same as the geometry being right.
        spec, err = snap(WIDE_W / WIDE_H)
        assert spec == "16:9"
        assert err == pytest.approx(0.096, abs=0.001)
        assert err > SNAP_WARN_THRESHOLD, "a ~10% crop must not be reported as agreement"

    def test_near_square_panel_is_quiet(self):
        spec, err = snap(SQUARE_W / SQUARE_H)
        assert spec == "1:1"
        assert err < SNAP_WARN_THRESHOLD

    def test_ties_break_toward_the_earlier_entry(self):
        # Menus are written most-common-first so an ambiguous panel lands on the conventional shape.
        midpoint = math.exp((math.log(1.0) + math.log(4 / 3)) / 2)
        spec, _ = snap(midpoint, ("1:1", "4:3"))
        assert spec == "1:1"

    def test_empty_menu_is_an_error_not_a_silent_default(self):
        with pytest.raises(ValueError):
            snap(1.0, ())


class TestEffectiveFor:
    def test_degenerate_geometry_honors_the_declaration(self):
        # A zero-area node is malformed, not a panel; inventing a ratio there is worse than
        # trusting what the author wrote.
        assert effective_for(0, 100, "3:4") == ("3:4", 0.0)
        assert effective_for(100, 0, "16:9") == ("16:9", 0.0)
        assert effective_for(-5, 10, "1:1") == ("1:1", 0.0)

    def test_uses_the_menu_it_is_given(self):
        # With 2:3 available the splash lands there instead — the menu is the backend's, and the
        # snap is only ever as good as the menu.
        spec, err = effective_for(SPLASH_W, SPLASH_H, "3:4", ("1:1", "2:3", "3:4"))
        assert spec == "2:3"
        assert err < 0.04


class TestDriftReport:
    def test_agreement_within_threshold_is_silent(self):
        assert drift_report("1:1", "1:1", 0.03) is None

    def test_a_changed_ratio_always_reports(self):
        note = drift_report("3:4", "9:16", 0.140)
        assert note is not None
        assert "3:4" in note and "9:16" in note and "0.140" in note

    def test_same_ratio_with_large_residual_still_reports(self):
        note = drift_report("16:9", "16:9", 0.096)
        assert note is not None
        assert "geometry" in note


class TestBackendMenuLookup:
    def test_resolves_without_constructing_a_client(self):
        # Plan must never need a credential. ``gemini``'s registry entry declares its menu as a
        # class attribute precisely so this stays true.
        assert supported_aspects_for("gemini")

    def test_unknown_and_missing_backends_fall_back(self):
        assert supported_aspects_for("no-such-backend") == DEFAULT_SUPPORTED
        assert supported_aspects_for(None) == DEFAULT_SUPPORTED


class TestPlanIntegration:
    def test_declared_ratio_is_never_overwritten(self, canvas_path):
        manifest, _ = plan(canvas_path)
        splash = manifest.panel("spread0_page0_p0")
        assert splash.aspect_ratio == "3:4", "the author's declaration is a record, not a draft"
        assert splash.effective_aspect_ratio == "9:16"
        assert splash.request_aspect_ratio == "9:16", "dispatch asks for the geometry-derived one"

    def test_drift_is_recorded_in_the_manifest(self, canvas_path):
        manifest, _ = plan(canvas_path)
        assert any("spread0_page0_p0" in n for n in manifest.aspect_notes)
        assert any("spread0_page1_p0" in n for n in manifest.aspect_notes)
        # The six near-square panels stay out of it.
        assert len(manifest.aspect_notes) == 3

    def test_survives_a_manifest_round_trip(self, canvas_path, tmp_path):
        from comic_render.manifest import RenderManifest

        manifest, mpath = plan(canvas_path)
        reloaded = RenderManifest.load(mpath)
        assert reloaded.panel("spread0_page0_p0").effective_aspect_ratio == "9:16"
        assert reloaded.aspect_notes == manifest.aspect_notes

    def test_a_pre_h3_manifest_still_dispatches_on_its_declared_ratio(self):
        # Back-compat: manifests planned before this field existed must keep working, requesting
        # exactly what they always did.
        from comic_render.manifest import PanelSpec

        legacy = PanelSpec(
            panel_id="p", page_number=1, reading_index=0, status="prompt_only",
            prompt_text="x", aspect_ratio="4:3", target_px={"w": 100, "h": 75}, seed=1,
            variant_count=1, output_dir="runs/x",
        )
        assert legacy.effective_aspect_ratio is None
        assert legacy.request_aspect_ratio == "4:3"
