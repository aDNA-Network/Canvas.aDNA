"""LOC-heavy substrate smoke for `canvas_core/print.py` (507 LOC).

Authored under M-R5-01a S2 Phase 4 (`campaign_canvasforge_review`) to
provide minimum-viable test coverage for the print-export module not
covered by inherited Phase 1 migrations. Goal: prevent silent breakage
on Phase 7 cleanup-mission file moves; not full unit coverage.

Exercises the public utility surface (canvas_units_to_px, effective_dpi)
and dataclass instantiation (PanelPlacement, PageExportSpec, ExportResult).
PrintExporter integration smoke is deferred — its duck-typed cpb interface
requires a comic-builder fixture and would partially overlap canvas_comic
test scope. Pure substrate.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.print import (
    BLEED_PX_H,
    BLEED_PX_W,
    BLEED_WIDTH,
    DPI_WARNING_THRESHOLD,
    PRINT_DPI,
    SAFE_PX_H,
    SAFE_PX_W,
    STD_PANEL_PX_H,
    STD_PANEL_PX_W,
    TOTAL_PAGES,
    TRIM_PX_H,
    TRIM_PX_W,
    ExportResult,
    PageExportSpec,
    PanelPlacement,
    PrintExporter,
    canvas_units_to_px,
    effective_dpi,
)


class TestPrintConstants:
    """Smoke: print constants are sane and follow CWS specifications."""

    def test_print_dpi_default(self):
        assert PRINT_DPI == 300

    def test_bleed_pixel_dimensions(self):
        # 687.5 canvas units * 300 DPI / 100 = 2062.5 -> 2062
        assert BLEED_PX_W == 2062
        # 1050 * 300 / 100 = 3150
        assert BLEED_PX_H == 3150

    def test_trim_pixel_dimensions(self):
        # 662.5 * 300 / 100 = 1987.5 -> 1988
        assert TRIM_PX_W == 1988
        # 1025 * 300 / 100 = 3075
        assert TRIM_PX_H == 3075

    def test_safe_pixel_dimensions(self):
        # 637.5 * 300 / 100 = 1912.5 -> 1913
        assert SAFE_PX_W == 1913
        # 1000 * 300 / 100 = 3000
        assert SAFE_PX_H == 3000

    def test_panel_pixel_dimensions(self):
        assert STD_PANEL_PX_W == 941
        assert STD_PANEL_PX_H == 980

    def test_origin_constants(self):
        assert BLEED_WIDTH == 687.5
        assert TOTAL_PAGES == 32

    def test_dpi_warning_threshold(self):
        assert DPI_WARNING_THRESHOLD == 200


class TestCanvasUnitsToPx:
    """Smoke: canvas_units_to_px round-trips against the documented formula."""

    def test_default_dpi(self):
        # 100 units * 300 / 100 = 300
        assert canvas_units_to_px(100) == 300

    def test_zero_units(self):
        assert canvas_units_to_px(0) == 0

    def test_fractional_units_rounded(self):
        # 1.5 * 300 / 100 = 4.5 -> 4 (banker's) or 5; Python round() is banker's
        # Just check it's a valid int near 4-5
        result = canvas_units_to_px(1.5)
        assert isinstance(result, int)
        assert 4 <= result <= 5

    def test_custom_dpi(self):
        # 100 units * 600 / 100 = 600
        assert canvas_units_to_px(100, dpi=600) == 600


class TestEffectiveDpi:
    """Smoke: effective_dpi returns float and handles edge cases."""

    def test_exact_match(self):
        # source_px == target_px → effective_dpi == target_dpi
        assert effective_dpi(2062, 2062, 300) == 300.0

    def test_undersize_source_lowers_dpi(self):
        # source 1000 px / target 2000 px * 300 dpi = 150 dpi (low)
        assert effective_dpi(1000, 2000, 300) == 150.0

    def test_oversize_source_raises_dpi(self):
        # source 4000 / target 2000 * 300 = 600 dpi
        assert effective_dpi(4000, 2000, 300) == 600.0

    def test_zero_target(self):
        # Guard against div-by-zero
        assert effective_dpi(1000, 0, 300) == 0.0


class TestPanelPlacement:
    """Smoke: PanelPlacement dataclass instantiates with sensible defaults."""

    def test_minimal_construction(self):
        pp = PanelPlacement(panel_id="p1", x=0, y=0, width=941, height=980)
        assert pp.panel_id == "p1"
        assert pp.is_bleed is False
        assert pp.is_spread is False
        assert pp.effective_dpi_w == 0.0

    def test_full_construction(self):
        pp = PanelPlacement(
            panel_id="p2",
            x=100,
            y=200,
            width=941,
            height=980,
            source_width=2000,
            source_height=2000,
            effective_dpi_w=300.0,
            effective_dpi_h=300.0,
            is_bleed=True,
            is_spread=False,
        )
        assert pp.is_bleed is True
        assert pp.source_width == 2000


class TestPageExportSpec:
    """Smoke: PageExportSpec dataclass instantiates and accepts panel placements."""

    def test_minimal_construction(self):
        spec = PageExportSpec(page_number=1, page_id="p_001")
        assert spec.page_number == 1
        assert spec.page_id == "p_001"
        assert spec.panel_placements == []
        assert spec.is_ifc is False
        assert spec.is_ibc is False

    def test_with_placements(self):
        pp = PanelPlacement(panel_id="p1", x=0, y=0, width=941, height=980)
        spec = PageExportSpec(
            page_number=2,
            page_id="p_002",
            panel_placements=[pp],
            bg_color=(20, 20, 20),
            is_ifc=True,
        )
        assert len(spec.panel_placements) == 1
        assert spec.is_ifc is True
        assert spec.bg_color == (20, 20, 20)


class TestExportResult:
    """Smoke: ExportResult dataclass."""

    def test_basic(self):
        r = ExportResult(
            page_number=5,
            filename="ScienceStanley_Issue01_p005.jpg",
            path="/tmp/output/p005.jpg",
            width=2062,
            height=3150,
            file_size_bytes=12345,
            cmyk=True,
        )
        assert r.page_number == 5
        assert r.cmyk is True
        assert r.warnings == []


class TestPrintExporterInstantiation:
    """Smoke: PrintExporter can be constructed with a duck-typed cpb stub.

    Only verifies the constructor does not raise — full integration
    requires a comic-builder fixture which is out of substrate scope.
    """

    def test_construct_with_minimal_stub(self, tmp_path):
        # A bare object suffices for construction; pages access happens later.
        class _Stub:
            pages = []

        exporter = PrintExporter(
            cpb=_Stub(),
            output_dir=tmp_path / "print_out",
            issue_name="Smoke_Test",
            cmyk=False,
            jpeg_quality=80,
        )
        assert exporter.issue_name == "Smoke_Test"
        assert exporter.cmyk is False
        assert exporter.jpeg_quality == 80
