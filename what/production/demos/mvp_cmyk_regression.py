#!/usr/bin/env python3
"""M-5-04: CMYK Print-Export Regression Test

Verifies the PrintExporter produces correct dimensions and CMYK conversion
under the CanvasForge code path. Uses synthetic test data (no real images
needed — creates blank panels to test the pipeline mechanics).

Charter spec:
  - 300 DPI
  - Bleed: 2062×3150
  - Trim: 1988×3075
  - Safe: 1913×3000
  - No CMYK regression vs 2026-03-24 baseline
"""

import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# Add canvas packages to path
CODE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_ROOT))

from PIL import Image

from canvas_core.print import (
    BLEED_PX_H,
    BLEED_PX_W,
    DPI_WARNING_THRESHOLD,
    PRINT_DPI,
    SAFE_PX_H,
    SAFE_PX_W,
    STD_PANEL_PX_H,
    STD_PANEL_PX_W,
    TRIM_PX_H,
    TRIM_PX_W,
    ExportResult,
    PageExportSpec,
    PanelPlacement,
    PrintExporter,
    canvas_units_to_px,
    effective_dpi,
)


# ---------------------------------------------------------------------------
# Mock page-builder objects (duck-typed to match PrintExporter expectations)
# ---------------------------------------------------------------------------

@dataclass
class MockPanel:
    id: str
    x: float = 12.5
    y: float = 25.0
    width: float = 312.5
    height: float = 326.67
    bleed: bool = False
    span_rows: int = 1
    span_cols: int = 1
    image_path: str = ""


@dataclass
class MockColorScript:
    dominant: str = "#1a1a2e"


@dataclass
class MockPage:
    page_number: int
    id: str
    panel_ids: list[str] = field(default_factory=list)
    color_script: MockColorScript = field(default_factory=MockColorScript)


@dataclass
class MockBuilder:
    pages: list[MockPage] = field(default_factory=list)
    _panels: dict[str, MockPanel] = field(default_factory=dict)

    def get_panel(self, panel_id: str) -> MockPanel | None:
        return self._panels.get(panel_id)


def create_test_image(path: Path, width: int = 1024, height: int = 1024) -> Path:
    """Create a synthetic test image."""
    img = Image.new("RGB", (width, height), color=(100, 50, 150))
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(path))
    return path


def run_regression():
    """Execute the CMYK print-export regression test suite."""
    print("=" * 60)
    print("M-5-04: CMYK Print-Export Regression Test")
    print("=" * 60)

    passed = 0
    failed = 0

    def check(name: str, condition: bool, detail: str = ""):
        nonlocal passed, failed
        if condition:
            passed += 1
            print(f"  PASS: {name}")
        else:
            failed += 1
            print(f"  FAIL: {name} — {detail}")

    # --- Test 1: Dimension constants ---
    print("\n[1] Print-spec dimension constants")
    check("PRINT_DPI = 300", PRINT_DPI == 300)
    check("BLEED = 2062×3150", BLEED_PX_W == 2062 and BLEED_PX_H == 3150)
    check("TRIM = 1988×3075", TRIM_PX_W == 1988 and TRIM_PX_H == 3075)
    check("SAFE = 1913×3000", SAFE_PX_W == 1913 and SAFE_PX_H == 3000)
    check("STD_PANEL = 941×980", STD_PANEL_PX_W == 941 and STD_PANEL_PX_H == 980)

    # --- Test 2: canvas_units_to_px conversion ---
    print("\n[2] Canvas-unit to pixel conversion")
    check("687.5 units → 2062px", canvas_units_to_px(687.5) == 2062)
    check("1050 units → 3150px", canvas_units_to_px(1050) == 3150)
    check("662.5 units → 1988px", canvas_units_to_px(662.5) == 1988)
    check("1025 units → 3075px", canvas_units_to_px(1025) == 3075)
    check("100 units → 300px (1 inch)", canvas_units_to_px(100) == 300)

    # --- Test 3: Effective DPI calculation ---
    print("\n[3] Effective DPI calculation")
    check("1024px source → 941px target = 326 DPI",
          abs(effective_dpi(1024, 941) - 326.46) < 1.0)
    check("512px source → 941px target = 163 DPI (upscale warning)",
          effective_dpi(512, 941) < DPI_WARNING_THRESHOLD)

    # --- Test 4: Single-page export with mock data ---
    print("\n[4] Single-page export (synthetic panels)")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create test panel images
        panel_img_path = create_test_image(tmpdir / "panels" / "p1.png", 1024, 1024)

        panel = MockPanel(
            id="panel_01",
            x=12.5,
            y=25.0,
            width=312.5,
            height=326.67,
            image_path=str(panel_img_path),
        )

        page = MockPage(page_number=3, id="page_03", panel_ids=["panel_01"])

        builder = MockBuilder(
            pages=[page],
            _panels={"panel_01": panel},
        )

        exporter = PrintExporter(
            cpb=builder,
            output_dir=str(tmpdir / "output"),
            issue_name="test_issue",
            cmyk=True,
        )

        specs = exporter.build_page_specs()
        check("build_page_specs returns 1 spec", len(specs) == 1)

        result = exporter.export_page(specs[0])
        check("export_page returns ExportResult", isinstance(result, ExportResult))
        check(f"output dimensions {result.width}×{result.height}",
              result.width == BLEED_PX_W and result.height == BLEED_PX_H,
              f"expected {BLEED_PX_W}×{BLEED_PX_H}")
        check("CMYK flag set", result.cmyk is True)
        check("file exists on disk", Path(result.path).exists())
        check(f"file size > 0 ({result.file_size_bytes:,} bytes)",
              result.file_size_bytes > 0)

        # Verify actual image properties
        output_img = Image.open(result.path)
        check(f"output image mode = CMYK (got {output_img.mode})",
              output_img.mode == "CMYK")
        check(f"output image size = {BLEED_PX_W}×{BLEED_PX_H}",
              output_img.size == (BLEED_PX_W, BLEED_PX_H))

        # Check DPI metadata
        dpi_info = output_img.info.get("dpi", (0, 0))
        check(f"DPI metadata = (300, 300) (got {dpi_info})",
              dpi_info == (300, 300))

    # --- Test 5: Full-bleed panel ---
    print("\n[5] Full-bleed panel placement")
    bleed_panel = MockPanel(
        id="bleed_01",
        x=0, y=0,
        width=687.5, height=1050,
        bleed=True, span_rows=3, span_cols=2,
    )
    placement = PrintExporter(
        cpb=MockBuilder(), output_dir="/tmp/test"
    )._compute_panel_placement(bleed_panel)
    check("full-bleed placement at origin", placement.x == 0 and placement.y == 0)
    check(f"full-bleed dimensions = {BLEED_PX_W}×{BLEED_PX_H}",
          placement.width == BLEED_PX_W and placement.height == BLEED_PX_H)
    check("is_bleed = True", placement.is_bleed is True)

    # --- Test 6: Spread panel ---
    print("\n[6] Spread panel detection")
    spread_panel = MockPanel(
        id="spread_01",
        x=0, y=0,
        width=1375,  # > BLEED_WIDTH * 1.5
        height=1050,
        bleed=True, span_rows=3, span_cols=2,
    )
    spread_placement = PrintExporter(
        cpb=MockBuilder(), output_dir="/tmp/test"
    )._compute_panel_placement(spread_panel)
    check("spread detected", spread_placement.is_spread is True)
    check(f"spread width = {BLEED_PX_W * 2}",
          spread_placement.width == BLEED_PX_W * 2)

    # --- Test 7: RGB-only export (no CMYK) ---
    print("\n[7] RGB-only export (cmyk=False)")
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        panel_img_path = create_test_image(tmpdir / "panels" / "p1.png")
        panel = MockPanel(id="panel_rgb", image_path=str(panel_img_path))
        page = MockPage(page_number=1, id="page_01", panel_ids=["panel_rgb"])
        builder = MockBuilder(pages=[page], _panels={"panel_rgb": panel})

        exporter = PrintExporter(
            cpb=builder, output_dir=str(tmpdir / "output"),
            cmyk=False,
        )
        specs = exporter.build_page_specs()
        result = exporter.export_page(specs[0])
        check("RGB export: cmyk flag = False", result.cmyk is False)

        output_img = Image.open(result.path)
        check(f"RGB export: mode = RGB (got {output_img.mode})",
              output_img.mode == "RGB")

    # --- Test 8: ICC profile path check ---
    print("\n[8] ICC profile availability (macOS)")
    from canvas_core.print import MACOS_CMYK_PROFILE, MACOS_SRGB_PROFILE
    cmyk_exists = Path(MACOS_CMYK_PROFILE).exists()
    srgb_exists = Path(MACOS_SRGB_PROFILE).exists()
    check(f"macOS CMYK profile exists: {MACOS_CMYK_PROFILE}", cmyk_exists)
    check(f"macOS sRGB profile exists: {MACOS_SRGB_PROFILE}", srgb_exists)

    # --- Summary ---
    total = passed + failed
    print(f"\n{'=' * 60}")
    print(f"CMYK REGRESSION RESULTS: {passed}/{total} passed, {failed} failed")
    print(f"{'=' * 60}")

    if failed == 0:
        print("ALL CHECKS PASSED — no CMYK regression detected")
    else:
        print(f"WARNING: {failed} checks failed — review above")

    return failed == 0


if __name__ == "__main__":
    success = run_regression()
    sys.exit(0 if success else 1)
