"""Integration smoke for the M-R2-02 dual-prompt protocol.

Authored at M-R2-02 S3 (campaign_canvasforge_review). Exercises the end-to-end
path from ContextPack -> ComicPageBuilder.generate_panel_prompt -> ImagePrompt
-> assemble_dual_prompt with both single-prompt and dual-prompt paths plus the
str-backcompat shim and the F-38 missing-path surface. Mirrors the
``lattice_comic_canvas.lattice.yaml::image_generation`` ``inputs:`` declaration
landed in S3; demonstrates that the F-38 3-layer closure (signature +
ContextPack pre-flight + builder-state guard) holds at v1.0 even before the
v1.1 orchestrator wires the lattice-level enforcement.

Spec authority:
  ``how/campaigns/campaign_canvasforge_review/missions/artifacts/m_r2_01_dual_prompt_protocol_spec.md``
  § 3 (wrapper) + § 7.1 (ImagePrompt) + § 7.2 (ContextPack) + § 7.3 (signature)
  + § 7.5 (mermaid_layout module) + § 7.6 (lattice file amendment).

Scope at S3 (per Stanley decision 2026-05-03): minimal smoke. Hand-authored
PanelLayout exercises the dual-prompt assembly; the structural-state ->
PanelLayout transform is deferred to the v1.1 hardening campaign.
"""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
import unittest
import warnings
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_comic import ASPECT_RATIOS, ComicPageBuilder
from canvas_comic.comic import ContextNotLoaded, ContextPack
from canvas_comic.mermaid_layout import (
    IMAGEN_DUAL_PROMPT_WRAPPER,
    LayoutNode,
    PanelLayout,
    SpatialEdge,
    assemble_dual_prompt,
    serialize_panel_layout,
)
from canvas_core.image_generation import ImagePrompt, _coerce_prompt


_FIELDS = (
    "storyboard_canvas",
    "character_bible",
    "color_theory",
    "prompt_engineering",
    "voice_foundations",
)


def _make_sentinel_context_pack(tmp_dir: Path) -> ContextPack:
    """Write 5 sentinel files into ``tmp_dir`` and return a ContextPack.

    Mirrors the helper in ``test_comic_builder.py`` (S2 convention: helper
    repeats per-module rather than centralising — pytest test discovery does
    not require importable test modules).
    """
    kwargs: dict[str, Path] = {}
    for f in _FIELDS:
        p = tmp_dir / f"{f}.md"
        p.write_text(f"# Sentinel {f}\n")
        kwargs[f] = p
    return ContextPack(**kwargs)


class TestM_R2_02IntegrationSmoke(unittest.TestCase):
    """End-to-end smoke for the dual-prompt protocol after S1+S2+S3 closure."""

    def setUp(self) -> None:
        self._tmp = Path(tempfile.mkdtemp())
        self.ctx = _make_sentinel_context_pack(self._tmp)

    def tearDown(self) -> None:
        shutil.rmtree(self._tmp, ignore_errors=True)

    def test_generate_panel_prompt_returns_image_prompt(self):
        """Happy path: builder + ContextPack -> generate_panel_prompt -> ImagePrompt."""
        cpb = ComicPageBuilder(name="smoke", context_pack=self.ctx)
        page_id = cpb.add_page(1, spread_number=1)
        pid = cpb.add_panel(page_id, 0, 0, panel_type="dialogue")
        cpb.set_panel_content(
            pid,
            scene_description="Stanley speaks at a microscope.",
            characters=["Stanley"],
        )

        ip = cpb.generate_panel_prompt(pid, context_pack=self.ctx)

        self.assertIsInstance(ip, ImagePrompt)
        self.assertTrue(ip.text)
        self.assertIn(ip.aspect_ratio, set(ASPECT_RATIOS.values()))
        # Structural-state -> PanelLayout transform deferred to v1.1 hardening;
        # v1.0 single-prompt path always returns mermaid_layout=None.
        self.assertIsNone(ip.mermaid_layout)

    def test_assemble_dual_prompt_single_path_degrades(self):
        """mermaid_layout=None: assemble emits wrapper + PART 1 only."""
        ip = ImagePrompt(
            text="alpha scene description",
            mermaid_layout=None,
            aspect_ratio="1:1",
        )
        out = assemble_dual_prompt(ip)

        self.assertIn("alpha scene description", out)
        self.assertIn(IMAGEN_DUAL_PROMPT_WRAPPER, out)
        # PART 1 marker appears in the wrapper text (referential) AND as the
        # section header that precedes the prompt body -> 2 occurrences.
        self.assertEqual(out.count("[PART 1: TEXT DESCRIPTION]"), 2)
        # PART 2 marker only appears in the wrapper text on the single path.
        self.assertEqual(out.count("[PART 2: SPATIAL LAYOUT]"), 1)

    def test_assemble_dual_prompt_dual_path(self):
        """Hand-authored PanelLayout serialises into mermaid_layout; assemble emits both parts."""
        layout = PanelLayout(
            panel_id="p_smoke",
            framing="medium",
            top=[LayoutNode(name="balloon", depth=None)],
            mid=[LayoutNode(name="stanley", depth="midground")],
            bot=[LayoutNode(name="bench", depth="background")],
            edges=[SpatialEdge(source="balloon", target="stanley", relation="speaks")],
        )
        mermaid = serialize_panel_layout(layout)
        ip = ImagePrompt(
            text="bravo dual scene",
            mermaid_layout=mermaid,
            aspect_ratio="3:4",
        )
        out = assemble_dual_prompt(ip)

        self.assertIn("bravo dual scene", out)
        self.assertIn(IMAGEN_DUAL_PROMPT_WRAPPER, out)
        # On the dual path both PART markers appear in the wrapper (referential)
        # AND as section headers -> 2 occurrences each.
        self.assertEqual(out.count("[PART 1: TEXT DESCRIPTION]"), 2)
        self.assertEqual(out.count("[PART 2: SPATIAL LAYOUT]"), 2)
        # Mermaid content tokens leak into the assembled prompt.
        self.assertIn("graph", out)
        self.assertIn("panel:p_smoke", out)
        self.assertIn("framing=medium", out)
        self.assertIn("speaks", out)

    def test_str_backcompat_emits_deprecation_warning(self):
        """str path coerces to ImagePrompt with v1.2 sunset DeprecationWarning."""
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            ip = _coerce_prompt("legacy text payload")

        self.assertIsInstance(ip, ImagePrompt)
        self.assertEqual(ip.text, "legacy text payload")
        self.assertIsNone(ip.mermaid_layout)
        self.assertTrue(
            any(
                issubclass(w.category, DeprecationWarning)
                and "v1.2" in str(w.message)
                for w in caught
            ),
            "DeprecationWarning with v1.2 sunset wording not emitted",
        )

    def test_context_not_loaded_names_missing_field(self):
        """ContextNotLoaded message includes the missing field name + str(path)."""
        cpb = ComicPageBuilder(name="smoke_missing", context_pack=self.ctx)
        page_id = cpb.add_page(1, spread_number=1)
        pid = cpb.add_panel(page_id, 0, 0, panel_type="dialogue")
        cpb.set_panel_content(
            pid,
            scene_description="Stanley speaks at a microscope.",
            characters=["Stanley"],
        )
        broken = ContextPack(
            storyboard_canvas=self.ctx.storyboard_canvas,
            character_bible=Path("/nonexistent/character_bible.md"),
            color_theory=self.ctx.color_theory,
            prompt_engineering=self.ctx.prompt_engineering,
            voice_foundations=self.ctx.voice_foundations,
        )

        with self.assertRaises(ContextNotLoaded) as exc_ctx:
            cpb.generate_panel_prompt(pid, context_pack=broken)

        msg = str(exc_ctx.exception)
        self.assertIn("character_bible", msg)
        self.assertIn("/nonexistent/character_bible.md", msg)


if __name__ == "__main__":
    unittest.main()
