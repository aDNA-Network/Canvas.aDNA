"""Tests for canvas_core.image_generation.ImagenWiring.

Uses ``unittest`` so the suite runs with system Python (no pytest required) —
the broader CanvasForge test tree follows pytest assert style but
M02's plan calls for a green test pass and pytest is not always installed
on dev machines. ``unittest`` discovery is also pytest-compatible.

Migrated from `lattice-protocol/extensions/canvas/tests/test_canvas_image_generation.py`
under M-R5-01a (campaign_canvasforge_review). This is an integration test
for substrate code (`canvas_core.image_generation.ImagenWiring`) that uses
comic and presentation builders as fixtures — a common pattern for
cross-application substrate tests (mirrors `test_generation_mode_independence.py`).
Substrate target: `canvas_core/image_generation.py` (453 LOC).
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

# what/production on sys.path so canvas_core / canvas_presentation resolve as
# top-level packages (parents[2] from canvas_core/tests/). canvas_comic was
# archived at ADR-009 (2026-08-22); its legacy panel-side tests moved to
# what/production/_archive/tests_excised_legacy_paths.py.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from canvas_core.image_generation import ImagenWiring  # noqa: E402
from canvas_presentation.presentation import PresentationBuilder  # noqa: E402


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


class FakeImageClient:
    """Drop-in stand-in for GeminiImageClient. Records calls and writes
    minimal valid PNG bytes to ``output_path`` so file-presence checks pass."""

    # 67-byte 1x1 transparent PNG
    PNG_BYTES = bytes.fromhex(
        "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4"
        "890000000a49444154789c6300010000000500010d0a2db40000000049454e44"
        "ae426082"
    )

    def __init__(self, fail_on: set[int] | None = None) -> None:
        self.calls: list[dict[str, Any]] = []
        self.fail_on = fail_on or set()

    def generate_image(
        self,
        prompt: str,
        output_path: str | None = None,
        style: str = "photo",
        aspect_ratio: str = "1:1",
        image_size: str = "2K",
        model: str = "ultra",
    ) -> dict[str, Any]:
        call_index = len(self.calls) + 1
        self.calls.append(
            {
                "prompt": prompt,
                "output_path": output_path,
                "style": style,
                "aspect_ratio": aspect_ratio,
                "image_size": image_size,
                "model": model,
            }
        )
        if call_index in self.fail_on:
            return {"success": False, "error": f"intentional failure on call {call_index}"}
        if not output_path:
            return {"success": False, "error": "no output_path"}
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(self.PNG_BYTES)
        return {
            "success": True,
            "image_path": output_path,
            "mime_type": "image/png",
            "size_bytes": len(self.PNG_BYTES),
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect_ratio,
        }


# ---------------------------------------------------------------------------
# Helpers — small builders for fixture state
# ---------------------------------------------------------------------------


def _make_presentation_with_pending_image() -> tuple[PresentationBuilder, str]:
    """Build a presentation with one PendingImage and return (builder, id)."""
    from canvas_core.config_substrate import PendingImage

    pres = PresentationBuilder(name="test_deck")
    slide_id = pres.add_title_slide(title="Test Title", subtitle="Test Subtitle")

    # Inject a PendingImage directly via the internal dict — mirrors the
    # pattern build_deck.py will follow once Wilhelm slide 1 is wired.
    # The placeholder text node must exist on the canvas so that
    # resolve_pending_image can find and swap it.
    pending_id = "pending_test_hero_001"
    pending = PendingImage(
        id=pending_id,
        prompt="Test prompt for hero image",
        target_path="who/assets/banners/test_hero.png",
        slide_id=slide_id,
        format="landscape_16_9",
    )
    pres._pending_images[pending_id] = pending  # noqa: SLF001
    pres._cb.add_text_node(  # noqa: SLF001
        id=pending_id, text="[pending image]", x=0, y=0, width=400, height=300
    )
    return pres, pending_id


# ---------------------------------------------------------------------------
# Path planning
# ---------------------------------------------------------------------------


class TestPathPlanning(unittest.TestCase):
    def setUp(self) -> None:
        self.wiring = ImagenWiring()
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_variant_path_format(self) -> None:
        p = self.wiring.variant_path(self.tmp, "panel_p07_01", 2)
        self.assertEqual(p.name, "panel_p07_01_v2.png")

    def test_selection_canvas_path_format(self) -> None:
        p = self.wiring.selection_canvas_path(self.tmp, "panel_p07_01")
        self.assertEqual(p.name, "panel_p07_01_selection.canvas")

    def test_sidecar_path_format(self) -> None:
        p = self.wiring.sidecar_path(self.tmp, "panel_p07_01")
        self.assertEqual(p.name, "panel_p07_01.selection.json")

    def test_prepare_variant_paths_default_count(self) -> None:
        paths = self.wiring.prepare_variant_paths(self.tmp, "x")
        self.assertEqual(len(paths), 3)
        self.assertEqual(paths[0].name, "x_v1.png")
        self.assertEqual(paths[2].name, "x_v3.png")

    def test_prepare_variant_paths_custom_count(self) -> None:
        paths = self.wiring.prepare_variant_paths(self.tmp, "x", count=5)
        self.assertEqual(len(paths), 5)
        self.assertEqual(paths[4].name, "x_v5.png")


# ---------------------------------------------------------------------------
# generate_variants
# ---------------------------------------------------------------------------


class TestGenerateVariants(unittest.TestCase):
    def setUp(self) -> None:
        self.wiring = ImagenWiring()
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_generates_n_files_with_canonical_names(self) -> None:
        client = FakeImageClient()
        paths = self.wiring.generate_variants(
            client=client,
            prompt="A small cat in a sunlit lab",
            aspect_ratio="16:9",
            target_dir=self.tmp,
            item_id="hero_test",
            count=3,
        )
        self.assertEqual(len(paths), 3)
        self.assertEqual(len(client.calls), 3)
        for i, path in enumerate(paths, start=1):
            self.assertTrue(Path(path).exists(), f"variant {i} missing on disk")
            self.assertEqual(Path(path).name, f"hero_test_v{i}.png")
        for call in client.calls:
            self.assertEqual(call["aspect_ratio"], "16:9")
            self.assertEqual(call["model"], "pro")  # default
            self.assertEqual(call["style"], "photo")

    def test_failure_raises_runtime_error_with_all_errors(self) -> None:
        client = FakeImageClient(fail_on={2, 3})
        with self.assertRaises(RuntimeError) as ctx:
            self.wiring.generate_variants(
                client=client,
                prompt="x",
                aspect_ratio="1:1",
                target_dir=self.tmp,
                item_id="x",
                count=3,
            )
        msg = str(ctx.exception)
        self.assertIn("variant 2", msg)
        self.assertIn("variant 3", msg)

    def test_overrides_propagate_to_client(self) -> None:
        client = FakeImageClient()
        self.wiring.generate_variants(
            client=client,
            prompt="x",
            aspect_ratio="3:4",
            target_dir=self.tmp,
            item_id="x",
            count=1,
            model="ultra",
            style="illustration",
        )
        self.assertEqual(client.calls[0]["model"], "ultra")
        self.assertEqual(client.calls[0]["style"], "illustration")
        self.assertEqual(client.calls[0]["aspect_ratio"], "3:4")


# ---------------------------------------------------------------------------
# Selection canvas construction
# ---------------------------------------------------------------------------


# TestPanelSelectionCanvas removed at the ADR-009 archive (2026-08-22): its only
# subject was the legacy panel-side path driven by canvas_comic.ComicPageBuilder.
# Preserved at what/production/_archive/tests_excised_legacy_paths.py [A].


class TestImageSelectionCanvas(unittest.TestCase):
    def setUp(self) -> None:
        self.wiring = ImagenWiring()
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_build_image_selection_canvas_writes_file(self) -> None:
        pres, pending_id = _make_presentation_with_pending_image()
        variant_paths = [
            str(self.tmp / f"{pending_id}_v{i}.png") for i in (1, 2, 3)
        ]
        for p in variant_paths:
            Path(p).write_bytes(FakeImageClient.PNG_BYTES)

        out = self.wiring.selection_canvas_path(self.tmp, pending_id)
        result = self.wiring.build_image_selection_canvas(
            presentation_builder=pres,
            pending_id=pending_id,
            variant_paths=variant_paths,
            output_path=out,
        )
        self.assertTrue(result.exists())
        canvas = json.loads(result.read_text())
        file_nodes = [n for n in canvas["nodes"] if n.get("type") == "file"]
        self.assertEqual(len(file_nodes), 3)
        for node in file_nodes:
            self.assertIn(node["file"], variant_paths)


# ---------------------------------------------------------------------------
# Resolution
# ---------------------------------------------------------------------------


class TestResolveSurvivors(unittest.TestCase):
    def setUp(self) -> None:
        self.wiring = ImagenWiring()
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _make_three_variants(self, item_id: str) -> list[Path]:
        paths = self.wiring.prepare_variant_paths(self.tmp, item_id)
        for p in paths:
            p.write_bytes(FakeImageClient.PNG_BYTES)
        return paths

    def test_find_survivors_returns_only_existing_files(self) -> None:
        item_id = "panel_test"
        paths = self._make_three_variants(item_id)
        # Delete the first two — only v3 survives
        paths[0].unlink()
        paths[1].unlink()
        survivors = self.wiring.find_survivors(self.tmp, item_id)
        self.assertEqual(len(survivors), 1)
        self.assertEqual(survivors[0].name, f"{item_id}_v3.png")

    # test_resolve_panel_with_one_survivor_succeeds, test_resolve_with_zero_survivors_raises,
    # and test_resolve_with_multiple_survivors_raises removed at the ADR-009 archive
    # (2026-08-22): legacy panel-side paths, canvas_comic-driven. Preserved at
    # what/production/_archive/tests_excised_legacy_paths.py [A].

    def test_resolve_image_with_one_survivor_succeeds(self) -> None:
        pres, pending_id = _make_presentation_with_pending_image()
        paths = self._make_three_variants(pending_id)
        paths[1].unlink()
        paths[2].unlink()
        # v1 survives

        sidecar_dir = self.tmp / "sidecar"
        result = self.wiring.resolve_image_from_surviving_files(
            presentation_builder=pres,
            pending_id=pending_id,
            variant_dir=self.tmp,
            sidecar_dir=sidecar_dir,
            all_variant_paths=[str(p) for p in paths],
        )
        self.assertEqual(Path(result).name, f"{pending_id}_v1.png")
        # The pending image record is now resolved
        self.assertEqual(pres._pending_images[pending_id].status, "resolved")  # noqa: SLF001
        # The placeholder text node was rewritten to a file node
        node = pres._cb.get_node(pending_id)  # noqa: SLF001
        self.assertEqual(node["type"], "file")
        self.assertIn(f"{pending_id}_v1.png", node["file"])


class TestResolveWithChoice(unittest.TestCase):
    """Explicit selection — preserves all variants on disk."""

    def setUp(self) -> None:
        self.wiring = ImagenWiring()
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _three_variant_paths(self, item_id: str) -> list[Path]:
        paths = self.wiring.prepare_variant_paths(self.tmp, item_id)
        for p in paths:
            p.write_bytes(FakeImageClient.PNG_BYTES)
        return paths

    # test_resolve_panel_with_choice_preserves_all_variants removed at the ADR-009
    # archive (2026-08-22) — preserved at _archive/tests_excised_legacy_paths.py [A].

    def test_resolve_image_with_choice_preserves_all_variants(self) -> None:
        pres, pending_id = _make_presentation_with_pending_image()
        paths = self._three_variant_paths(pending_id)
        chosen = paths[0]  # v1

        sidecar_dir = self.tmp / "sidecar"
        result = self.wiring.resolve_image_with_choice(
            presentation_builder=pres,
            pending_id=pending_id,
            selected_path=chosen,
            all_variant_paths=[str(p) for p in paths],
            sidecar_dir=sidecar_dir,
        )
        # Builder updated and node rewritten to file type
        self.assertEqual(Path(result).name, f"{pending_id}_v1.png")
        self.assertEqual(pres._pending_images[pending_id].status, "resolved")  # noqa: SLF001
        node = pres._cb.get_node(pending_id)  # noqa: SLF001
        self.assertEqual(node["type"], "file")
        self.assertIn(f"{pending_id}_v1.png", node["file"])
        # All 3 variants still on disk
        for p in paths:
            self.assertTrue(p.exists(), f"{p} was unexpectedly deleted")
        sidecar = self.wiring.sidecar_path(sidecar_dir, pending_id)
        record = json.loads(sidecar.read_text())
        self.assertEqual(record["selected_index"], 1)

    def test_resolve_image_with_choice_works_without_sidecar(self) -> None:
        pres, pending_id = _make_presentation_with_pending_image()
        chosen = self.tmp / f"{pending_id}_v1.png"
        chosen.write_bytes(FakeImageClient.PNG_BYTES)

        result = self.wiring.resolve_image_with_choice(
            presentation_builder=pres,
            pending_id=pending_id,
            selected_path=chosen,
        )
        self.assertEqual(Path(result).name, f"{pending_id}_v1.png")
        # No sidecar dir passed -> no sidecar written, but builder still updated
        self.assertEqual(pres._pending_images[pending_id].status, "resolved")  # noqa: SLF001


# ---------------------------------------------------------------------------
# Sidecar record
# ---------------------------------------------------------------------------


class TestSelectionRecord(unittest.TestCase):
    def setUp(self) -> None:
        self.wiring = ImagenWiring()
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_write_selection_record_round_trip(self) -> None:
        all_variants = [
            "/abs/path/x_v1.png",
            "/abs/path/x_v2.png",
            "/abs/path/x_v3.png",
        ]
        path = self.wiring.write_selection_record(
            item_id="x",
            kind="pending_image",
            all_variant_paths=all_variants,
            selected_path="/abs/path/x_v3.png",
            sidecar_dir=self.tmp,
        )
        self.assertTrue(path.exists())
        record = json.loads(path.read_text())
        self.assertEqual(record["item_id"], "x")
        self.assertEqual(record["kind"], "pending_image")
        self.assertEqual(record["selected_index"], 3)
        self.assertEqual(record["all_variants"], all_variants)
        self.assertIn("selected_at", record)

    def test_write_selection_record_rejects_unknown_kind(self) -> None:
        with self.assertRaises(ValueError):
            self.wiring.write_selection_record(
                item_id="x",
                kind="bogus",
                all_variant_paths=[],
                selected_path="x",
                sidecar_dir=self.tmp,
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
