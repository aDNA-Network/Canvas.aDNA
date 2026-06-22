"""Tests for ``canvas_core/pdf_export.py`` (Pillar C / ADR-010).

Authored at M-V1-2-C-01 S1 (2026-05-28) per Pillar C charter and Stanley
"lean reuse" library election (AskUserQuestion 2026-05-28). Substrate-
additive: tests verify the PDF carrier discipline + Memory A V1-path
preservation (existing ``PrintExporter`` JPG path unmutated).

Re-merge rationale: lattice-labs/who/coordination/coord_2026_04_16_forge_split.md
"""

import re
import sys
import os

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.pdf_export import (
    PdfExporter,
    export_composites_to_pdf,
)
from canvas_core.print import PRINT_DPI


class TestPdfExporterBasics:
    """Smoke: file emission, PDF magic-bytes, empty-state guard."""

    def test_save_emits_a_file_at_output_path(self, tmp_path):
        out = tmp_path / "single.pdf"
        exp = PdfExporter(output_path=str(out))
        exp.add_page(Image.new("CMYK", (100, 100), 0))
        result = exp.save()
        assert result == out
        assert out.exists()
        assert out.stat().st_size > 0

    def test_saved_file_starts_with_pdf_magic(self, tmp_path):
        out = tmp_path / "magic.pdf"
        exp = PdfExporter(output_path=str(out))
        exp.add_page(Image.new("CMYK", (100, 100), 0))
        exp.save()
        assert out.read_bytes()[:4] == b"%PDF"

    def test_save_without_pages_raises(self, tmp_path):
        exp = PdfExporter(output_path=str(tmp_path / "empty.pdf"))
        with pytest.raises(ValueError, match="no pages"):
            exp.save()

    def test_page_count_tracks_added_pages(self, tmp_path):
        exp = PdfExporter(output_path=str(tmp_path / "x.pdf"))
        assert exp.page_count == 0
        exp.add_page(Image.new("CMYK", (100, 100)))
        exp.add_page(Image.new("CMYK", (100, 100)))
        assert exp.page_count == 2

    def test_default_dpi_is_print_dpi(self, tmp_path):
        exp = PdfExporter(output_path=str(tmp_path / "x.pdf"))
        assert exp.dpi == PRINT_DPI
        assert exp.dpi == 300


class TestPdfExporterValidation:
    """Input validation: type + size guards on add_page."""

    def test_add_page_rejects_non_image(self, tmp_path):
        exp = PdfExporter(output_path=str(tmp_path / "x.pdf"))
        with pytest.raises(TypeError, match="PIL.Image.Image"):
            exp.add_page("not an image")  # type: ignore[arg-type]

    def test_add_page_rejects_zero_width(self, tmp_path):
        exp = PdfExporter(output_path=str(tmp_path / "x.pdf"))
        with pytest.raises(ValueError, match="zero-sized"):
            exp.add_page(Image.new("CMYK", (0, 100)))

    def test_add_page_rejects_zero_height(self, tmp_path):
        exp = PdfExporter(output_path=str(tmp_path / "x.pdf"))
        with pytest.raises(ValueError, match="zero-sized"):
            exp.add_page(Image.new("CMYK", (100, 0)))


class TestMultiPage:
    """Multi-page PDF emission via PIL's ``save_all`` + ``append_images``."""

    def test_three_pages_emits_count_3_in_pdf_page_tree(self, tmp_path):
        out = tmp_path / "multi.pdf"
        composites = [
            Image.new("CMYK", (200, 200), (i * 30, 0, 0, 0)) for i in range(3)
        ]
        export_composites_to_pdf(composites, str(out))
        # PDF page tree carries `/Count N` for the number of pages
        content = out.read_bytes()
        assert b"/Count 3" in content

    def test_helper_raises_on_empty_composites(self, tmp_path):
        with pytest.raises(ValueError, match="empty composites"):
            export_composites_to_pdf([], str(tmp_path / "x.pdf"))


class TestCmykPreservation:
    """CMYK fidelity — PIL's PDF writer emits ``/DeviceCMYK`` color space for
    CMYK source images (ADR-010 §D3: CMYK conversion happens upstream in
    ``print.py``; PDF carrier preserves mode unchanged)."""

    def test_cmyk_image_emits_devicecmyk_marker(self, tmp_path):
        out = tmp_path / "cmyk.pdf"
        # Solid cyan: (255, 0, 0, 0) in CMYK channel order
        image = Image.new("CMYK", (200, 200), (255, 0, 0, 0))
        exp = PdfExporter(output_path=str(out))
        exp.add_page(image)
        exp.save()
        content = out.read_bytes()
        assert b"/DeviceCMYK" in content

    def test_rgb_image_emits_devicergb_marker(self, tmp_path):
        out = tmp_path / "rgb.pdf"
        image = Image.new("RGB", (200, 200), (255, 0, 0))
        exp = PdfExporter(output_path=str(out))
        exp.add_page(image)
        exp.save()
        content = out.read_bytes()
        assert b"/DeviceRGB" in content


class TestDpiAffectsPageGeometry:
    """DPI metadata (ADR-010 §D1): higher DPI → smaller PDF page (same
    pixel image takes fewer inches of physical extent)."""

    def test_300_dpi_page_smaller_than_72_dpi_page(self, tmp_path):
        image = Image.new("CMYK", (600, 600), 0)
        out_300 = tmp_path / "p300.pdf"
        out_72 = tmp_path / "p72.pdf"

        e1 = PdfExporter(output_path=str(out_300), dpi=300)
        e1.add_page(image)
        e1.save()

        e2 = PdfExporter(output_path=str(out_72), dpi=72)
        e2.add_page(image)
        e2.save()

        # MediaBox format from PIL: `/MediaBox [ 0 0 W H ]` (note inner spaces)
        # in PDF user units (1/72 inch)
        media_re = re.compile(rb"/MediaBox \[\s*0\s+0\s+([\d.]+)\s+([\d.]+)\s*\]")
        m300 = media_re.search(out_300.read_bytes())
        m72 = media_re.search(out_72.read_bytes())
        assert m300 is not None, "300 DPI PDF missing /MediaBox"
        assert m72 is not None, "72 DPI PDF missing /MediaBox"
        w300 = float(m300.group(1))
        w72 = float(m72.group(1))
        # 600 px / 300 DPI = 2 in × 72 pt/in = 144 pt
        # 600 px / 72 DPI = 8.33 in × 72 pt/in = 600 pt
        assert w300 < w72


class TestNoSourceMutation:
    """No re-encode discipline (ADR-010 §D4): source PIL.Image is not
    mutated by ``save()``. Imagen 4 Ultra resolution preserved end-to-end
    through the carrier."""

    def test_source_image_pixels_unchanged_after_save(self, tmp_path):
        out = tmp_path / "pattern.pdf"
        image = Image.new("CMYK", (10, 10), 0)
        # Stamp a known pattern on the diagonal
        for i in range(10):
            image.putpixel((i, i), (i * 25, 50, 100, 0))
        baseline = [image.getpixel((i, i)) for i in range(10)]

        exp = PdfExporter(output_path=str(out))
        exp.add_page(image)
        exp.save()

        after = [image.getpixel((i, i)) for i in range(10)]
        assert baseline == after

    def test_source_image_size_unchanged_after_save(self, tmp_path):
        out = tmp_path / "size.pdf"
        # BLEED_PX_W × BLEED_PX_H from canvas_core/print.py at 300 DPI
        image = Image.new("CMYK", (2062, 3150), 0)
        original_size = image.size
        exp = PdfExporter(output_path=str(out))
        exp.add_page(image)
        exp.save()
        assert image.size == original_size


class TestSubstrateAdditiveDiscipline:
    """Memory A discipline check: existing ``PrintExporter`` JPG path
    public surface is unmutated by Pillar C. No PDF method/attr leakage
    into ``PrintExporter``; substrate-additive boundary preserved.

    Re-merge rationale persistence: PDF export rides as a new module
    next to the canvas-substrate primitives that the 2026-04-16
    re-merge made load-bearing.
    """

    def test_print_exporter_public_surface_has_no_pdf_leakage(self):
        from canvas_core.print import PrintExporter

        public = {
            name
            for name in dir(PrintExporter)
            if not name.startswith("_")
        }
        # Sanity: JPG path methods still present
        assert "export_page" in public
        assert "export_spread" in public
        assert "export_all" in public
        # And nothing PDF-shaped has leaked into PrintExporter
        pdf_leaks = {name for name in public if "pdf" in name.lower()}
        assert pdf_leaks == set(), (
            "Pillar C must be substrate-additive: PrintExporter should "
            f"remain PDF-free, but found: {pdf_leaks}"
        )

    def test_pdf_export_module_does_not_import_canvas_comic(self):
        """Substrate-neutrality check (ADR-001 + ADR-010 §D2): the PDF
        carrier must not import comic-specific application modules."""
        import canvas_core.pdf_export as mod

        source = open(mod.__file__).read()
        assert "canvas_comic" not in source
        assert "from canvas_comic" not in source
