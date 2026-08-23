"""Tests for CV-COMIC-STYLE-01 (comic style-lock drift) — implemented at H6 re-open."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from canvas_core.traps.cv_comic_style_01 import DRIFT_THRESHOLD, MIN_PANELS, check


def _solid(path: Path, rgb: tuple[int, int, int], size: int = 96) -> None:
    Image.new("RGB", (size, size), rgb).save(path)


def _noisy_warm(path: Path, base: tuple[int, int, int], size: int = 96) -> None:
    """A warm-palette image with mild per-pixel variation (a 'consistent' panel)."""
    im = Image.new("RGB", (size, size))
    px = im.load()
    r0, g0, b0 = base
    for x in range(size):
        for y in range(size):
            d = (x * 7 + y * 3) % 24 - 12
            px[x, y] = (max(0, min(255, r0 + d)), max(0, min(255, g0 + d)), max(0, min(255, b0 + d // 2)))
    im.save(path)


def _canvas_for(files: list[str]) -> dict:
    return {
        "nodes": [
            {"id": f"panel_{i}", "type": "file", "file": name}
            for i, name in enumerate(files)
        ]
    }


class TestCvComicStyle01(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_skips_without_asset_root(self) -> None:
        self.assertEqual(check(_canvas_for(["a.png"])), [])

    def test_skips_below_min_panels(self) -> None:
        names = [f"p{i}.png" for i in range(MIN_PANELS - 1)]
        for n in names:
            _solid(self.tmp / n, (200, 120, 80))
        self.assertEqual(check(_canvas_for(names), asset_root=self.tmp), [])

    def test_consistent_run_is_silent(self) -> None:
        names = [f"p{i}.png" for i in range(4)]
        bases = [(200, 120, 80), (205, 125, 85), (195, 118, 78), (202, 122, 82)]
        for n, b in zip(names, bases):
            _noisy_warm(self.tmp / n, b)
        findings = check(_canvas_for(names), asset_root=self.tmp)
        self.assertEqual(findings, [])

    def test_gross_palette_break_fires(self) -> None:
        names = [f"p{i}.png" for i in range(4)]
        for n in names[:3]:
            _noisy_warm(self.tmp / n, (200, 120, 80))
        _solid(self.tmp / names[3], (20, 40, 220))  # cold solid blue in a warm run
        findings = check(_canvas_for(names), asset_root=self.tmp)
        self.assertEqual(len(findings), 1)
        f = findings[0]
        self.assertEqual(f.trap_id, "CV-COMIC-STYLE-01")
        self.assertEqual(f.condition, "style_lock_drift")
        self.assertEqual(f.node_ids, ["panel_3"])
        self.assertEqual(f.severity, "high")
        self.assertIn("style centroid", f.message)

    def test_non_raster_and_missing_files_ignored(self) -> None:
        names = [f"p{i}.png" for i in range(3)]
        for n in names:
            _noisy_warm(self.tmp / n, (200, 120, 80))
        canvas = _canvas_for(names + ["notes.md", "missing.png"])
        findings = check(canvas, asset_root=self.tmp)
        self.assertEqual(findings, [])

    def test_threshold_is_h3_calibrated(self) -> None:
        # Guard the calibration constant against silent drift: the H3-measured
        # consistent max was 0.987; the threshold must stay above it and below
        # the 1.482 a grayscale break of an H3 panel scored.
        self.assertGreater(DRIFT_THRESHOLD, 0.987)
        self.assertLess(DRIFT_THRESHOLD, 1.482)


if __name__ == "__main__":
    unittest.main()
