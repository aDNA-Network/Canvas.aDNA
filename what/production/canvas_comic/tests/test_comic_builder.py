"""Tests for canvas_comic (M-2b-01)."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_comic import (
    ComicPageBuilder,
    ComicProductionAdapter,
    ComicReport,
    Page,
    Panel,
    PendingPanel,
    TOTAL_PAGES,
    TRIM_WIDTH,
    TRIM_HEIGHT,
    ASPECT_RATIOS,
    CHARACTER_STANLEY,
)
from canvas_comic.comic import ContextNotLoaded, ContextPack
from canvas_core.image_generation import ImagePrompt


def _make_test_context_pack(tmp_path: Path) -> ContextPack:
    """Create 5 sentinel files in ``tmp_path`` and return a ContextPack.

    Used by tests that call :meth:`ComicPageBuilder.generate_panel_prompt`
    or any path that depends on ``builder.context_pack`` being set.
    """
    fields = (
        "storyboard_canvas",
        "character_bible",
        "color_theory",
        "prompt_engineering",
        "voice_foundations",
    )
    kwargs: dict[str, Path] = {}
    for f in fields:
        p = tmp_path / f"{f}.md"
        p.write_text(f"# Sentinel {f}\n")
        kwargs[f] = p
    return ContextPack(**kwargs)


class TestComicPageBuilder:
    def test_basic_build(self):
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(1, spread_number=1)
        cpb.standard_grid(p1)
        canvas = cpb.build()
        assert len(canvas["nodes"]) >= 7  # 1 group + 6 panels

    def test_add_page_with_act(self):
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(3)  # Act 1
        page = cpb.get_page(p1)
        assert page is not None
        assert page.act is not None
        assert page.act.name == "act_1"

    def test_panel_types(self):
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(1)
        pid = cpb.add_panel(p1, 0, 0, panel_type="dialogue")
        panel = cpb.get_panel(pid)
        assert panel is not None
        assert panel.panel_type == "dialogue"

    def test_splash_page(self):
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(1)
        pid = cpb.splash_page(p1)
        panel = cpb.get_panel(pid)
        assert panel.bleed is True
        assert panel.span_rows == 3
        assert panel.span_cols == 2

    def test_6_layer_prompt(self, tmp_path):
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(3, spread_number=2)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(
            panels[0],
            scene_description="Stanley enters the lab",
            characters=["Stanley"],
            mood="curious",
            spread_number=2,
        )
        prompt = cpb.generate_panel_prompt(panels[0], context_pack=ctx_pack)
        text = prompt.text
        # Should contain all 6 layers
        assert "Ghibli" in text or "pixel" in text  # Layer 1: style
        assert "Stanley" in text or "scientist" in text.lower()  # Layer 2: character
        assert "enters the lab" in text  # Layer 3: scene
        assert "shot" in text.lower() or "angle" in text.lower()  # Layer 4: camera
        assert "lighting" in text.lower() or "mood" in text.lower()  # Layer 5: lighting
        assert "No photorealism" in text  # Layer 6: negative

    def test_character_invariance(self, tmp_path):
        """Character block includes story state mood."""
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(3, spread_number=2)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(panels[0], scene_description="Lab scene",
                              characters=["Stanley"], spread_number=2)
        prompt = cpb.generate_panel_prompt(panels[0], context_pack=ctx_pack)
        # Spread 2 has science_stanley mood="confident"
        assert "confident" in prompt.text

    def test_character_registry_default_none_preserves_hardcoded(self, tmp_path):
        """ADR-008 §D2 (M-V1-2-F-01 S2): character_registry default None keeps
        the hardcoded CHARACTER_STANLEY descriptor — regression guard for all
        existing call sites that don't supply a registry."""
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(3, spread_number=2)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(panels[0], scene_description="Lab scene",
                              characters=["Stanley"], spread_number=2)
        prompt = cpb.generate_panel_prompt(panels[0], context_pack=ctx_pack)
        # Hardcoded CHARACTER_STANLEY descriptor present (substring fingerprint).
        assert "Studio Ghibli-style young scientist" in prompt.text

    def test_character_registry_override_known_character(self, tmp_path):
        """ADR-008 §D2: registry override replaces the hardcoded descriptor for
        a known story-state character; story-state mood/pose merge still
        applies on top of the overridden descriptor."""
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(3, spread_number=2)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(panels[0], scene_description="Lab scene",
                              characters=["Stanley"], spread_number=2)
        registry = {"stanley": "FINGERPRINT_OVERRIDE_DESCRIPTOR"}
        prompt = cpb.generate_panel_prompt(
            panels[0], context_pack=ctx_pack, character_registry=registry
        )
        # Override descriptor replaced the hardcoded one.
        assert "FINGERPRINT_OVERRIDE_DESCRIPTOR" in prompt.text
        assert "Studio Ghibli-style young scientist" not in prompt.text
        # Story-state mood still merges onto the overridden descriptor.
        assert "confident" in prompt.text

    def test_character_registry_unknown_character_injection(self, tmp_path):
        """ADR-008 §D2: registry-only character (not Stanley / Agent Stanley /
        Helix) injects the registry descriptor instead of falling back to the
        raw character name."""
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(3, spread_number=2)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(panels[0], scene_description="Lab scene",
                              characters=["Quinn"], spread_number=2)
        registry = {"quinn": "QUINN_FINGERPRINT_DESCRIPTOR_text"}
        prompt = cpb.generate_panel_prompt(
            panels[0], context_pack=ctx_pack, character_registry=registry
        )
        assert "QUINN_FINGERPRINT_DESCRIPTOR_text" in prompt.text

    def test_rlhf_hints_default_none_preserves_s2_baseline(self, tmp_path):
        """ADR-008 §D2 candidate B1 (M-V1-2-F-01 S3): with no register or
        hint kwargs supplied, the prompt is byte-identical to the
        equivalent call without the kwargs — re-baseline gate guarantee."""
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(3, spread_number=2)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(panels[0], scene_description="Lab scene",
                              characters=["Stanley"], spread_number=2)
        baseline = cpb.generate_panel_prompt(panels[0], context_pack=ctx_pack)
        # Re-invoke supplying explicit None — must produce identical text.
        with_kwargs = cpb.generate_panel_prompt(
            panels[0],
            context_pack=ctx_pack,
            register=None,
            rlhf_character_hints=None,
            rlhf_camera_nuances=None,
        )
        assert baseline.text == with_kwargs.text
        # No "RLHF hint:" marker present.
        assert "RLHF hint:" not in baseline.text

    def test_rlhf_hints_caller_override_applied(self, tmp_path):
        """ADR-008 §D2 candidate B1: when register + rlhf_hints both
        resolve, the hint text is appended as a parenthetical to both
        the character and camera blocks."""
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(3, spread_number=2)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(panels[0], scene_description="Lab scene",
                              characters=["Stanley"], spread_number=2)
        prompt = cpb.generate_panel_prompt(
            panels[0],
            context_pack=ctx_pack,
            register="R7",
            rlhf_character_hints={"r7": "CHAR_FINGERPRINT_HINT_xyz"},
            rlhf_camera_nuances={"r7": "CAM_FINGERPRINT_HINT_abc"},
        )
        assert "(RLHF hint: CHAR_FINGERPRINT_HINT_xyz)" in prompt.text
        assert "(RLHF hint: CAM_FINGERPRINT_HINT_abc)" in prompt.text

    def test_rlhf_hints_unknown_register_no_op(self, tmp_path):
        """ADR-008 §D2 candidate B1: when register doesn't resolve in
        the supplied hint dict, the prompt is unchanged (no parenthetical
        suffix added)."""
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(3, spread_number=2)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(panels[0], scene_description="Lab scene",
                              characters=["Stanley"], spread_number=2)
        prompt = cpb.generate_panel_prompt(
            panels[0],
            context_pack=ctx_pack,
            register="R99_NOT_PRESENT",
            rlhf_character_hints={"r7": "SHOULD_NOT_APPEAR"},
            rlhf_camera_nuances={"r7": "ALSO_SHOULD_NOT_APPEAR"},
        )
        assert "SHOULD_NOT_APPEAR" not in prompt.text
        assert "ALSO_SHOULD_NOT_APPEAR" not in prompt.text
        assert "RLHF hint:" not in prompt.text

    def test_compositional_nuance_default_none_preserves_s3_baseline(self, tmp_path):
        """ADR-008 §D2 sub-dimension addendum (M-V1-2-F-01 S4): with no
        compositional_nuance field set, the prompt is byte-identical to
        the S3 baseline — re-baseline gate guarantee."""
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(3, spread_number=2)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(panels[0], scene_description="Lab scene",
                              characters=["Stanley"], spread_number=2,
                              panel_type="dialogue")
        baseline = cpb.generate_panel_prompt(panels[0], context_pack=ctx_pack)
        # No compositional nuance marker present.
        assert "compositional nuance:" not in baseline.text

    def test_compositional_nuance_known_key_appended(self, tmp_path):
        """ADR-008 §D2 sub-dimension addendum: when compositional_nuance
        resolves in the matching template's nuances dict, the descriptor
        is appended to the camera block as a parenthetical."""
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(3, spread_number=2)
        panels = cpb.standard_grid(p1)
        # dialogue template has nuance composition_naturalness in its nuances dict
        cpb.set_panel_content(panels[0], scene_description="Lab scene",
                              characters=["Stanley"], spread_number=2,
                              panel_type="dialogue",
                              compositional_nuance="composition_naturalness")
        prompt = cpb.generate_panel_prompt(panels[0], context_pack=ctx_pack)
        assert "compositional nuance:" in prompt.text
        assert "natural stance and gesture" in prompt.text

    def test_compositional_nuance_unknown_key_no_op(self, tmp_path):
        """ADR-008 §D2 sub-dimension addendum: when compositional_nuance
        is set to a nuance_id absent from the matching template's
        nuances dict, the prompt is unchanged (silent no-op)."""
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(3, spread_number=2)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(panels[0], scene_description="Lab scene",
                              characters=["Stanley"], spread_number=2,
                              panel_type="dialogue",
                              compositional_nuance="nonexistent_nuance_id")
        prompt = cpb.generate_panel_prompt(panels[0], context_pack=ctx_pack)
        assert "compositional nuance:" not in prompt.text
        assert "nonexistent_nuance_id" not in prompt.text

    def test_spread_color_script(self):
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(3, spread_number=2)
        page = cpb.get_page(p1)
        assert page.color_script is not None
        assert page.color_script.mood == "inviting"

    def test_art_style_map(self):
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(8)  # pixel
        page = cpb.get_page(p1)
        assert page.art_style == "pixel"

    def test_pending_panels(self, tmp_path):
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test", context_pack=ctx_pack)
        p1 = cpb.add_page(1)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(panels[0], scene_description="Test scene")
        pending = cpb.prepare_panel_generation(panels[0])
        assert pending.status == "pending"
        assert len(cpb.pending_panels) == 1
        cpb.resolve_panel(panels[0], "test.png")
        assert len(cpb.pending_panels) == 0

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cpb = ComicPageBuilder(name="save_test")
            p1 = cpb.add_page(1)
            cpb.standard_grid(p1)
            path = cpb.save(Path(tmpdir) / "test.canvas")
            assert path.exists()
            with open(path) as f:
                data = json.load(f)
            assert "nodes" in data

    def test_review_scoring(self):
        cpb = ComicPageBuilder(name="test")
        for i in range(1, 33):
            p = cpb.add_page(i, spread_number=(i + 1) // 2)
            cpb.standard_grid(p)
        report = cpb.review()
        assert isinstance(report, ComicReport)
        assert 0.0 <= report.score <= 1.0
        assert report.page_count == 32
        assert report.panel_count == 192  # 32 pages * 6 panels

    def test_no_cross_package_imports(self):
        """canvas_comic must not import canvas_presentation."""
        import canvas_comic.comic as m
        source = Path(m.__file__).read_text()
        assert "from canvas_presentation" not in source
        assert "import canvas_presentation" not in source


# ---------------------------------------------------------------------------
# M-2b-02: PrintExporter integration
# ---------------------------------------------------------------------------


class TestPrintIntegration:
    def test_print_exporter_accepts_comic_builder(self):
        """PrintExporter should instantiate with ComicPageBuilder (duck typing)."""
        from canvas_core.print import PrintExporter
        cpb = ComicPageBuilder(name="print_test")
        p1 = cpb.add_page(1)
        cpb.standard_grid(p1)
        with tempfile.TemporaryDirectory() as tmpdir:
            exporter = PrintExporter(cpb, tmpdir)
            assert exporter is not None

    def test_panel_attributes_match_print_contract(self):
        """Comic Panel must have all attributes PrintExporter accesses."""
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(1)
        panels = cpb.standard_grid(p1)
        panel = cpb.get_panel(panels[0])
        # PrintExporter accesses these via duck typing
        for attr in ("bleed", "span_rows", "span_cols", "x", "y", "width", "height", "image_path"):
            assert hasattr(panel, attr), f"Panel missing attribute: {attr}"

    def test_page_attributes_match_print_contract(self):
        """Comic Page must have all attributes PrintExporter accesses."""
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(1)
        page = cpb.get_page(p1)
        for attr in ("page_number", "id", "panel_ids"):
            assert hasattr(page, attr), f"Page missing attribute: {attr}"


# ---------------------------------------------------------------------------
# M-2b-03: Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_dual_worlds_transition_spread(self, tmp_path):
        """Spread 4 (pages 7-8) is transition world."""
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test")
        p7 = cpb.add_page(7, spread_number=4)
        page = cpb.get_page(p7)
        assert page.art_style == "transition"
        panels = cpb.standard_grid(p7)
        cpb.set_panel_content(panels[0], scene_description="Portal opening",
                              characters=["Stanley"], spread_number=4)
        prompt = cpb.generate_panel_prompt(panels[0], context_pack=ctx_pack)
        assert "transition" in prompt.text.lower() or "dissolving" in prompt.text.lower()

    def test_gutter_spacing(self):
        """Standard grid panels respect PANEL_GUTTER between cells."""
        from canvas_comic.comic import PANEL_GUTTER, SAFE_ORIGIN_X, SAFE_WIDTH
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(1)
        panels = cpb.standard_grid(p1, rows=3, cols=2)
        p0 = cpb.get_panel(panels[0])
        p1_panel = cpb.get_panel(panels[1])
        # Panels in same row, adjacent columns — gap should be PANEL_GUTTER
        gap = p1_panel.x - (p0.x + p0.width)
        assert abs(gap - PANEL_GUTTER) < 1.0, f"Gutter gap {gap} != {PANEL_GUTTER}"

    def test_bleed_dimensions(self):
        """Full-bleed splash panel starts at (0,0) with BLEED dims."""
        from canvas_comic.comic import BLEED_WIDTH, BLEED_HEIGHT
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(1)
        pid = cpb.splash_page(p1)
        panel = cpb.get_panel(pid)
        assert panel.x == 0.0
        assert panel.y == 0.0
        assert panel.width == BLEED_WIDTH
        assert panel.height == BLEED_HEIGHT

    def test_spread_panel_dimensions(self):
        """Two-page spread panel width = 2 * BLEED_WIDTH + 25."""
        from canvas_comic.comic import BLEED_WIDTH, BLEED_HEIGHT
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(1)
        p2 = cpb.add_page(2)
        pid = cpb.spread(p1, p2)
        panel = cpb.get_panel(pid)
        assert panel.width == BLEED_WIDTH * 2 + 25

    def test_character_invariance_across_spreads(self, tmp_path):
        """Stanley's base description persists across different spreads."""
        from canvas_comic.comic import CHARACTER_STANLEY
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="test")
        p3 = cpb.add_page(3, spread_number=2)
        p29 = cpb.add_page(29, spread_number=15)
        panels_3 = cpb.standard_grid(p3)
        panels_29 = cpb.standard_grid(p29)
        cpb.set_panel_content(panels_3[0], scene_description="Lab", characters=["Stanley"], spread_number=2)
        cpb.set_panel_content(panels_29[0], scene_description="Sunset", characters=["Stanley"], spread_number=15)
        prompt_3 = cpb.generate_panel_prompt(panels_3[0], context_pack=ctx_pack)
        prompt_29 = cpb.generate_panel_prompt(panels_29[0], context_pack=ctx_pack)
        # Base character description appears in both
        assert "lab coat" in prompt_3.text.lower()
        assert "lab coat" in prompt_29.text.lower()

    def test_page_30_art_style(self):
        """Page 30 is 'mixed' style (memorial page)."""
        from canvas_comic.comic import ART_STYLE_MAP
        assert ART_STYLE_MAP[30] == "mixed"

    def test_r11_gap_documented(self):
        """R11 page-gating is substrate-level, not in comic.py."""
        import canvas_comic.comic as m
        source = Path(m.__file__).read_text()
        # R11 gating is in canvas_core/r11_gate.py, not here
        assert "r11_gate" not in source.lower() or "R11" not in source


# ---------------------------------------------------------------------------
# M-2b-04: Enhanced scoring
# ---------------------------------------------------------------------------


class TestEnhancedScoring:
    def test_quality_score_present(self):
        """ComicReport includes quality_score field."""
        cpb = ComicPageBuilder(name="test")
        p1 = cpb.add_page(1, spread_number=1)
        cpb.standard_grid(p1)
        report = cpb.review()
        assert hasattr(report, "quality_score")

    def test_quality_scoring_with_full_content(self):
        """Full content assignment yields higher quality score."""
        cpb = ComicPageBuilder(name="test")
        for i in range(1, 33):
            p = cpb.add_page(i, spread_number=(i + 1) // 2)
            panels = cpb.standard_grid(p)
            for pid in panels:
                cpb.set_panel_content(
                    pid, scene_description=f"Scene for panel on page {i}",
                    characters=["Stanley"], mood="determined",
                    spread_number=(i + 1) // 2,
                )
        report = cpb.review()
        assert report.quality_score > 0.5
        assert report.structural_score > 0.5

    def test_empty_comic_zero_quality(self):
        """Empty comic has zero quality score."""
        cpb = ComicPageBuilder(name="empty")
        report = cpb.review()
        assert report.quality_score == 0.0

    def test_weight_scheme_30_25_25_20(self):
        """Aggregate uses 30/25/25/20 weight scheme."""
        cpb = ComicPageBuilder(name="test")
        for i in range(1, 33):
            p = cpb.add_page(i, spread_number=(i + 1) // 2)
            cpb.standard_grid(p)
        report = cpb.review()
        # Verify aggregate is weighted combination
        expected = (report.structural_score * 0.30 + report.content_score * 0.25
                    + report.production_score * 0.25 + report.quality_score * 0.20)
        assert abs(report.score - round(expected, 2)) < 0.02


class TestComicProductionAdapter:
    def test_story_bible(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cpb = ComicPageBuilder(name="test")
            adapter = ComicProductionAdapter(cpb, tmpdir)
            result = adapter.execute_story_bible({"pages": [], "spreads": {}})
            assert result.success
            assert result.output_path is not None

    def test_panel_layout(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cpb = ComicPageBuilder(name="test")
            adapter = ComicProductionAdapter(cpb, tmpdir)
            specs = [{"page_number": 1, "layout_type": "grid", "rows": 3, "cols": 2}]
            result = adapter.execute_panel_layout(specs)
            assert result.success
            assert len(result.metadata["panel_ids"]) == 6


# ---------------------------------------------------------------------------
# M-R2-02 S2: ContextPack + dual-prompt return shape (spec § 7.2 / § 7.3)
# ---------------------------------------------------------------------------


class TestContextPack:
    """F-38 ContextPack pre-flight + ImagePrompt return shape."""

    def _seeded_builder(self, ctx_pack: ContextPack) -> tuple[ComicPageBuilder, str]:
        cpb = ComicPageBuilder(name="ctxpack_test", context_pack=ctx_pack)
        p1 = cpb.add_page(3, spread_number=2)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(
            panels[0],
            scene_description="Stanley examines a strand",
            characters=["Stanley"],
            spread_number=2,
        )
        return cpb, panels[0]

    def test_generate_panel_prompt_returns_image_prompt(self, tmp_path):
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb, panel_id = self._seeded_builder(ctx_pack)
        result = cpb.generate_panel_prompt(panel_id, context_pack=ctx_pack)
        assert isinstance(result, ImagePrompt)
        assert result.text != ""
        assert result.mermaid_layout is None  # S2: structural transform deferred to S3
        assert result.aspect_ratio in ASPECT_RATIOS.values()

    def test_generate_panel_prompt_raises_when_path_missing(self, tmp_path):
        ctx_pack = _make_test_context_pack(tmp_path)
        # Surgically remove one of the sentinel files
        ctx_pack.color_theory.unlink()
        cpb, panel_id = self._seeded_builder(ctx_pack)
        with pytest.raises(ContextNotLoaded) as exc_info:
            cpb.generate_panel_prompt(panel_id, context_pack=ctx_pack)
        assert "color_theory" in str(exc_info.value)
        assert str(ctx_pack.color_theory) in str(exc_info.value)

    def test_generate_panel_prompt_keyword_only(self, tmp_path):
        """Positional ContextPack call must fail (spec § 7.3 keyword-only)."""
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb, panel_id = self._seeded_builder(ctx_pack)
        with pytest.raises(TypeError):
            # Positional ContextPack — disallowed by `*,` in signature
            cpb.generate_panel_prompt(panel_id, ctx_pack)

    def test_prepare_panel_generation_raises_when_context_pack_unset(self, tmp_path):
        """prepare_panel_generation enforces builder.context_pack set (F-38 layer)."""
        cpb = ComicPageBuilder(name="no_ctx_pack")  # context_pack=None default
        p1 = cpb.add_page(1)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(panels[0], scene_description="Test")
        with pytest.raises(ContextNotLoaded):
            cpb.prepare_panel_generation(panels[0])
