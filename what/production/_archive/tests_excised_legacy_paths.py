# Excised legacy-path tests — preserved verbatim at the ADR-009 archive step (2026-08-22).
#
# NOT COLLECTED (pytest.ini: norecursedirs = _archive) and NOT runnable as-is: the imports
# assume the pre-archive layout. This file is a record (SO-7 archive-never-delete), kept so
# the excision from the live suites deletes nothing. Sources and original locations:
#
#   [A] canvas_core/tests/test_image_generation.py  — helpers `_make_sentinel_context_pack`,
#       `_make_comic_with_one_panel`; class TestPanelSelectionCanvas (1 test); from
#       TestResolveSurvivors: test_resolve_panel_with_one_survivor_succeeds,
#       test_resolve_with_zero_survivors_raises, test_resolve_with_multiple_survivors_raises;
#       from TestResolveWithChoice: test_resolve_panel_with_choice_preserves_all_variants.
#       Subject: the legacy panel-side ImagenWiring paths (build_panel_selection_canvas /
#       resolve_panel_from_surviving_files / resolve_panel_with_choice), only ever driven by
#       canvas_comic.ComicPageBuilder. Live comic_render uses only generate_variants.
#
#   [B] canvas_core/tests/test_generation_mode_independence.py —
#       TestBuilderConstructionIndependence.test_comic_builder_construction (subprocess
#       import-independence proof for the now-archived engine).
#
#   [C] tests/test_federation_validation.py — helper `_make_test_context_pack`; from
#       TestSSComicEndToEnd: test_build_1_page_comic, test_character_invariance_stanley,
#       test_comic_quality_scoring (legacy-builder E2E against the legacy SS graphicnovelforge
#       wrapper). The lattice-YAML-only tests of that class remain live.
#
# The verbatim bodies follow, fenced per source file.

EXCISED = {
    "A_test_image_generation": r'''
from canvas_comic.comic import ComicPageBuilder, ContextPack  # noqa: E402


def _make_sentinel_context_pack() -> ContextPack:
    """Create 5 sentinel context files in a fresh tmp dir and return a ContextPack."""
    ctx_dir = Path(tempfile.mkdtemp(prefix="canvasforge_test_"))
    fields = (
        "storyboard_canvas",
        "character_bible",
        "color_theory",
        "prompt_engineering",
        "voice_foundations",
    )
    kwargs: dict[str, Path] = {}
    for f in fields:
        p = ctx_dir / f"{f}.md"
        p.write_text("# sentinel\n")
        kwargs[f] = p
    return ContextPack(**kwargs)


def _make_comic_with_one_panel() -> tuple[ComicPageBuilder, str]:
    """Build a one-page, one-panel comic and return (builder, panel_id)."""
    comic = ComicPageBuilder(
        name="test_issue",
        context_pack=_make_sentinel_context_pack(),
    )
    page_id = comic.add_page(page_number=1)
    panel_id = comic.add_panel(
        page_id=page_id,
        row=1,
        col=1,
        panel_type="action",
    )
    comic.set_panel_content(
        panel_id=panel_id,
        scene_description="Hero shot of test character standing in a sunlit lab.",
        camera_angle="medium",
        characters=["test_character"],
        mood="hopeful",
    )
    comic.prepare_panel_generation(panel_id)
    return comic, panel_id


class TestPanelSelectionCanvas(unittest.TestCase):
    def setUp(self) -> None:
        self.wiring = ImagenWiring()
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_build_panel_selection_canvas_writes_file(self) -> None:
        comic, panel_id = _make_comic_with_one_panel()
        variant_paths = [
            str(self.tmp / f"{panel_id}_v{i}.png") for i in (1, 2, 3)
        ]
        for p in variant_paths:
            Path(p).write_bytes(FakeImageClient.PNG_BYTES)

        out = self.wiring.selection_canvas_path(self.tmp, panel_id)
        result = self.wiring.build_panel_selection_canvas(
            comic_builder=comic,
            panel_id=panel_id,
            variant_paths=variant_paths,
            output_path=out,
        )
        self.assertTrue(result.exists())
        canvas = json.loads(result.read_text())
        self.assertIn("nodes", canvas)
        file_nodes = [n for n in canvas["nodes"] if n.get("type") == "file"]
        self.assertEqual(len(file_nodes), 3)
        for node in file_nodes:
            self.assertIn(node["file"], variant_paths)


# from TestResolveSurvivors:
    def test_resolve_panel_with_one_survivor_succeeds(self) -> None:
        comic, panel_id = _make_comic_with_one_panel()
        paths = self._make_three_variants(panel_id)
        paths[0].unlink()
        paths[2].unlink()
        # v2 survives

        sidecar_dir = self.tmp / "sidecar"
        result = self.wiring.resolve_panel_from_surviving_files(
            comic_builder=comic,
            panel_id=panel_id,
            variant_dir=self.tmp,
            sidecar_dir=sidecar_dir,
            all_variant_paths=[str(p) for p in paths],
        )
        self.assertEqual(Path(result).name, f"{panel_id}_v2.png")
        panel_obj = comic._panels[panel_id]  # noqa: SLF001
        self.assertEqual(Path(panel_obj.image_path).name, f"{panel_id}_v2.png")
        sidecar = self.wiring.sidecar_path(sidecar_dir, panel_id)
        self.assertTrue(sidecar.exists())
        record = json.loads(sidecar.read_text())
        self.assertEqual(record["item_id"], panel_id)
        self.assertEqual(record["kind"], "panel")
        self.assertEqual(record["selected_index"], 2)
        self.assertEqual(len(record["all_variants"]), 3)

    def test_resolve_with_zero_survivors_raises(self) -> None:
        comic, panel_id = _make_comic_with_one_panel()
        # No variants on disk
        with self.assertRaises(RuntimeError) as ctx:
            self.wiring.resolve_panel_from_surviving_files(
                comic_builder=comic,
                panel_id=panel_id,
                variant_dir=self.tmp,
            )
        self.assertIn("no surviving variants", str(ctx.exception))

    def test_resolve_with_multiple_survivors_raises(self) -> None:
        comic, panel_id = _make_comic_with_one_panel()
        self._make_three_variants(panel_id)
        with self.assertRaises(RuntimeError) as ctx:
            self.wiring.resolve_panel_from_surviving_files(
                comic_builder=comic,
                panel_id=panel_id,
                variant_dir=self.tmp,
            )
        msg = str(ctx.exception)
        self.assertIn("3 variants survive", msg)
        self.assertIn(panel_id, msg)


# from TestResolveWithChoice:
    def test_resolve_panel_with_choice_preserves_all_variants(self) -> None:
        comic, panel_id = _make_comic_with_one_panel()
        paths = self._three_variant_paths(panel_id)
        chosen = paths[1]  # v2

        sidecar_dir = self.tmp / "sidecar"
        result = self.wiring.resolve_panel_with_choice(
            comic_builder=comic,
            panel_id=panel_id,
            selected_path=chosen,
            all_variant_paths=[str(p) for p in paths],
            sidecar_dir=sidecar_dir,
        )
        self.assertEqual(Path(result).name, f"{panel_id}_v2.png")
        panel_obj = comic._panels[panel_id]  # noqa: SLF001
        self.assertEqual(Path(panel_obj.image_path).name, f"{panel_id}_v2.png")
        for p in paths:
            self.assertTrue(p.exists(), f"{p} was unexpectedly deleted")
        sidecar = self.wiring.sidecar_path(sidecar_dir, panel_id)
        self.assertTrue(sidecar.exists())
        record = json.loads(sidecar.read_text())
        self.assertEqual(record["selected_index"], 2)
        self.assertEqual(len(record["all_variants"]), 3)
''',
    "B_test_generation_mode_independence": r'''
    def test_comic_builder_construction(self):
        """ComicPageBuilder constructs without canvas_presentation."""
        code = textwrap.dedent(
            """
            import sys
            import canvas_comic.comic as cc
            cpb = cc.ComicPageBuilder(name="independence_test")
            page = cpb.add_page(1)
            assert page is not None
            leaked = sorted(k for k in sys.modules if k.startswith("canvas_presentation"))
            print("LEAKED:" + ",".join(leaked))
            """
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(CODE_ROOT),
            env={**os.environ, "PYTHONPATH": str(CODE_ROOT)},
        )
        assert result.returncode == 0, f"subprocess failed: stderr={result.stderr}"
        leaked_line = next((line for line in result.stdout.splitlines() if line.startswith("LEAKED:")), "")
        leaked = leaked_line.removeprefix("LEAKED:").strip()
        assert leaked == "", f"comic builder construction leaked: {leaked}"
''',
    "C_test_federation_validation": r'''
from canvas_comic import ComicPageBuilder, CHARACTER_STANLEY
from canvas_comic.comic import ContextPack


def _make_test_context_pack(tmp_path: Path) -> ContextPack:
    """Create 5 sentinel files in ``tmp_path`` and return a ContextPack."""
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


# from TestSSComicEndToEnd:
    def test_build_1_page_comic(self):
        cpb = ComicPageBuilder(name="ss_federation_test")
        p1 = cpb.add_page(1, spread_number=1)
        cpb.standard_grid(p1)
        canvas = cpb.build()

        assert "nodes" in canvas
        assert "edges" in canvas
        assert len(cpb.pages) == 1

    def test_character_invariance_stanley(self, tmp_path):
        ctx_pack = _make_test_context_pack(tmp_path)
        cpb = ComicPageBuilder(name="ss_invariance_test")
        p1 = cpb.add_page(1, spread_number=1)
        panels = cpb.standard_grid(p1)
        cpb.set_panel_content(panels[0], scene_description="Stanley in the lab", characters=["Stanley"])
        prompt = cpb.generate_panel_prompt(panels[0], context_pack=ctx_pack)

        assert "purple turtleneck" in prompt.text
        assert "Wayfarer" in prompt.text  # Rayban Wayfarer frames

    def test_comic_quality_scoring(self):
        cpb = ComicPageBuilder(name="ss_scoring_test")
        p1 = cpb.add_page(1, spread_number=1)
        cpb.standard_grid(p1)
        cpb.build()

        report = cpb.review()
        assert report.score >= 0
        assert report.structural_score >= 0
        assert report.content_score >= 0
''',
}
