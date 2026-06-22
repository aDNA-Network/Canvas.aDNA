"""Tests for ``canvas_core/gdoc_export.py`` (Pillar D / ADR-011).

Authored at M-V1-2-D-01 S1 (2026-05-28) per Pillar D charter and Stanley
auth-model election (AskUserQuestion 2026-05-28): service-account JSON +
share-on-save, MVP element scope (Paragraph + Heading(1-3) + BulletList +
InlineImage). Substrate-additive: tests verify the gdoc carrier
discipline + Memory A V1-path preservation (existing ``PdfExporter`` and
``PrintExporter`` public surfaces unmutated).

Network-touching tests are gated by ``GOOGLE_DOC_SERVICE_ACCOUNT_PATH``
env-var; default ``pytest`` run mocks the Docs/Drive services so the
suite stays GREEN without credentials.

Re-merge rationale: lattice-labs/who/coordination/coord_2026_04_16_forge_split.md
"""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.gdoc_export import (
    BulletList,
    DocElement,
    GdocApiError,
    GdocAuthError,
    GdocExporter,
    Heading,
    InlineImage,
    Paragraph,
    _build_style_requests,
    _build_text_inserts,
    _text_style_from_token,
    export_canvas_to_gdoc,
)
from canvas_core.typography import TypographyToken


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _mock_docs_and_drive(doc_id: str = "DOC_TEST_ID", file_id: str = "FILE_TEST_ID"):
    """Build mock Docs + Drive service clients with batchUpdate capture."""
    docs = MagicMock(name="docs_service")
    docs.documents().create().execute.return_value = {"documentId": doc_id}
    docs.documents().batchUpdate().execute.return_value = {}

    drive = MagicMock(name="drive_service")
    drive.files().create().execute.return_value = {"id": file_id}
    drive.permissions().create().execute.return_value = {"id": "PERM_ID"}
    return docs, drive


def _patch_services(monkeypatch, docs, drive, creds_path: Path | None = None):
    """Patch _resolve_credentials_path + _build_services helpers."""
    import canvas_core.gdoc_export as mod

    monkeypatch.setattr(
        mod, "_resolve_credentials_path",
        lambda _cp: creds_path or Path("/tmp/fake_creds.json"),
    )
    monkeypatch.setattr(
        mod, "_build_services",
        lambda _path: (docs, drive),
    )


# ---------------------------------------------------------------------------
# TestGdocExporterBasics — smoke
# ---------------------------------------------------------------------------


class TestGdocExporterBasics:
    """Smoke: add appends, save returns doc_id, save-without-elements raises,
    doc_url derived from doc_id."""

    def test_add_appends_to_element_buffer(self):
        exp = GdocExporter(title="t")
        exp.add(Paragraph("hello"))
        exp.add(Heading("Top", level=1))
        assert len(exp._elements) == 2

    def test_save_returns_doc_id_string(self, monkeypatch):
        docs, drive = _mock_docs_and_drive(doc_id="DOC_ABC")
        _patch_services(monkeypatch, docs, drive)
        exp = GdocExporter(title="t")
        exp.add(Paragraph("hello"))
        doc_id = exp.save()
        assert doc_id == "DOC_ABC"

    def test_save_without_elements_raises(self):
        exp = GdocExporter(title="empty")
        with pytest.raises(ValueError, match="no elements"):
            exp.save()

    def test_doc_url_derived_from_doc_id(self, monkeypatch):
        docs, drive = _mock_docs_and_drive(doc_id="DOC_XYZ")
        _patch_services(monkeypatch, docs, drive)
        exp = GdocExporter(title="t")
        exp.add(Paragraph("p"))
        assert exp.doc_url is None  # before save()
        exp.save()
        assert exp.doc_url == "https://docs.google.com/document/d/DOC_XYZ/edit"


# ---------------------------------------------------------------------------
# TestElementValidation — input guards on dataclasses + GdocExporter.add
# ---------------------------------------------------------------------------


class TestElementValidation:
    """Input validation on element dataclasses + GdocExporter.add."""

    def test_paragraph_rejects_non_string_text(self):
        with pytest.raises(TypeError, match="must be str"):
            Paragraph(text=42)  # type: ignore[arg-type]

    def test_heading_rejects_invalid_level(self):
        with pytest.raises(ValueError, match="level must be 1, 2, or 3"):
            Heading(text="oops", level=4)

    def test_inline_image_rejects_non_pil_non_path_source(self):
        with pytest.raises(TypeError, match="PIL.Image.Image or Path or str"):
            InlineImage(source=12345)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# TestElementMapping — element → namedStyleType / bullet preset
# ---------------------------------------------------------------------------


class TestElementMapping:
    """Element-class → Docs namedStyleType / bullet preset (ADR-011 §D4)."""

    def test_heading_levels_map_to_named_style_h1_h2_h3(self):
        elements = [Heading("a", level=1), Heading("b", level=2), Heading("c", level=3)]
        _, ranges = _build_text_inserts(elements, None)
        reqs = _build_style_requests(ranges, None)
        named_styles = [
            r["updateParagraphStyle"]["paragraphStyle"]["namedStyleType"]
            for r in reqs
            if "updateParagraphStyle" in r
        ]
        assert named_styles == ["HEADING_1", "HEADING_2", "HEADING_3"]

    def test_paragraph_roles_map_to_named_style(self):
        elements = [
            Paragraph("title", role="display"),
            Paragraph("body", role="body"),
            Paragraph("cap", role="caption"),
        ]
        _, ranges = _build_text_inserts(elements, None)
        reqs = _build_style_requests(ranges, None)
        named_styles = [
            r["updateParagraphStyle"]["paragraphStyle"]["namedStyleType"]
            for r in reqs
            if "updateParagraphStyle" in r
        ]
        assert named_styles == ["TITLE", "NORMAL_TEXT", "NORMAL_TEXT"]

    def test_bullet_list_unordered_maps_to_disc_circle_square(self):
        _, ranges = _build_text_inserts([BulletList(items=["x", "y"])], None)
        reqs = _build_style_requests(ranges, None)
        bullet_reqs = [r for r in reqs if "createParagraphBullets" in r]
        assert len(bullet_reqs) == 1
        assert bullet_reqs[0]["createParagraphBullets"]["bulletPreset"] == "BULLET_DISC_CIRCLE_SQUARE"

    def test_bullet_list_ordered_maps_to_numbered_decimal(self):
        _, ranges = _build_text_inserts([BulletList(items=["x"], ordered=True)], None)
        reqs = _build_style_requests(ranges, None)
        bullet_reqs = [r for r in reqs if "createParagraphBullets" in r]
        assert "NUMBERED" in bullet_reqs[0]["createParagraphBullets"]["bulletPreset"]


# ---------------------------------------------------------------------------
# TestImageFidelity — Drive upload preserves Imagen 4 Ultra source
# ---------------------------------------------------------------------------


class TestImageFidelity:
    """Image carriage (ADR-011 §D3): Drive multipart upload (not base64-inline)
    preserves source resolution; source PIL image is not mutated."""

    def test_inline_image_uploads_via_drive_not_base64(self, monkeypatch):
        docs, drive = _mock_docs_and_drive(doc_id="DOC_IMG", file_id="FILE_IMG")
        _patch_services(monkeypatch, docs, drive)
        exp = GdocExporter(title="t")
        exp.add(InlineImage(source=Image.new("RGB", (100, 100), (255, 0, 0))))
        exp.save()

        # Drive files().create() was called (image went through Drive)
        assert drive.files().create.called

        # The second batchUpdate (images pass) contains an insertInlineImage
        # request whose uri points at drive.google.com (NOT base64 inline)
        bu_calls = docs.documents().batchUpdate.call_args_list
        # Find call(s) with insertInlineImage
        image_calls = [
            c for c in bu_calls
            if any(
                "insertInlineImage" in r
                for r in c.kwargs.get("body", {}).get("requests", [])
            )
        ]
        assert image_calls, "no insertInlineImage request captured"
        for c in image_calls:
            for r in c.kwargs["body"]["requests"]:
                if "insertInlineImage" in r:
                    uri = r["insertInlineImage"]["uri"]
                    assert uri.startswith("https://drive.google.com/")
                    assert "base64" not in uri

    def test_inline_image_preserves_native_resolution_when_width_pt_none(self, monkeypatch):
        docs, drive = _mock_docs_and_drive()
        _patch_services(monkeypatch, docs, drive)
        exp = GdocExporter(title="t")
        exp.add(InlineImage(
            source=Image.new("RGB", (2000, 2000), (255, 255, 255)),
            width_pt=None,
        ))
        exp.save()

        bu_calls = docs.documents().batchUpdate.call_args_list
        for c in bu_calls:
            for r in c.kwargs.get("body", {}).get("requests", []):
                if "insertInlineImage" in r:
                    # No objectSize key when width_pt is None — Docs uses native
                    assert "objectSize" not in r["insertInlineImage"]

    def test_source_image_pixels_unchanged_after_save(self, monkeypatch):
        docs, drive = _mock_docs_and_drive()
        _patch_services(monkeypatch, docs, drive)
        source = Image.new("RGB", (10, 10), (0, 0, 0))
        # Stamp a known pattern on the diagonal
        for i in range(10):
            source.putpixel((i, i), (i * 25, 50, 100))
        baseline = [source.getpixel((i, i)) for i in range(10)]

        exp = GdocExporter(title="t")
        exp.add(InlineImage(source=source))
        exp.save()

        after = [source.getpixel((i, i)) for i in range(10)]
        assert baseline == after


# ---------------------------------------------------------------------------
# TestTypographyTokenConsumption — Pillar B token-driven textStyle emission
# ---------------------------------------------------------------------------


class TestTypographyTokenConsumption:
    """Memory A opt-in semantics: typography_tokens=None emits no overrides;
    a populated TypographyToken emits weightedFontFamily + bold flags."""

    def test_publication_tokens_emit_weighted_font_family_in_text_style(self):
        token = TypographyToken(
            font_family_heading="Lora",
            font_family_body="Inter",
            weight_h1=700,
            weight_body=400,
        )
        elements = [Heading("Top", level=1), Paragraph("body text", role="body")]
        _, ranges = _build_text_inserts(elements, token)
        reqs = _build_style_requests(ranges, token)
        text_style_reqs = [r for r in reqs if "updateTextStyle" in r]
        assert text_style_reqs, "no updateTextStyle requests emitted"

        families = [
            r["updateTextStyle"]["textStyle"]["weightedFontFamily"]["fontFamily"]
            for r in text_style_reqs
        ]
        assert "Lora" in families
        assert "Inter" in families

        # h1 weight 700 → bold flag True
        h1_styles = [
            r["updateTextStyle"]["textStyle"]
            for r in text_style_reqs
            if r["updateTextStyle"]["textStyle"]
                .get("weightedFontFamily", {})
                .get("fontFamily") == "Lora"
        ]
        assert any(s.get("bold") is True for s in h1_styles)

    def test_default_none_tokens_emit_no_text_style_overrides(self):
        elements = [Heading("Top", level=1), Paragraph("body text", role="body")]
        _, ranges = _build_text_inserts(elements, None)
        reqs = _build_style_requests(ranges, None)
        text_style_reqs = [r for r in reqs if "updateTextStyle" in r]
        # Default-None TypographyToken → no updateTextStyle requests; Docs
        # default styling applies (Memory A opt-in-gated discipline)
        assert text_style_reqs == []


# ---------------------------------------------------------------------------
# TestSubstrateAdditiveDiscipline — Memory A discipline check
# ---------------------------------------------------------------------------


class TestSubstrateAdditiveDiscipline:
    """Memory A discipline check (ADR-011 §D2): existing ``PdfExporter`` and
    ``PrintExporter`` public surfaces are unmutated by Pillar D import;
    substrate-additive boundary preserved.

    Re-merge rationale persistence: gdoc export rides as a new module
    next to the canvas-substrate primitives that the 2026-04-16 re-merge
    made load-bearing.
    """

    def test_pdf_exporter_and_print_exporter_unmutated_by_gdoc_module(self):
        # Import gdoc_export first (triggers any side-effects)
        import canvas_core.gdoc_export  # noqa: F401
        from canvas_core.pdf_export import PdfExporter
        from canvas_core.print import PrintExporter

        pdf_public = {n for n in dir(PdfExporter) if not n.startswith("_")}
        print_public = {n for n in dir(PrintExporter) if not n.startswith("_")}

        # PDF surface unchanged
        assert "add_page" in pdf_public
        assert "save" in pdf_public
        assert "page_count" in pdf_public
        gdoc_leaks_in_pdf = {n for n in pdf_public if "gdoc" in n.lower() or "google" in n.lower()}
        assert gdoc_leaks_in_pdf == set(), (
            f"PdfExporter leaked gdoc-shaped attrs: {gdoc_leaks_in_pdf}"
        )

        # Print surface unchanged
        assert "export_page" in print_public
        gdoc_leaks_in_print = {n for n in print_public if "gdoc" in n.lower() or "google" in n.lower()}
        assert gdoc_leaks_in_print == set(), (
            f"PrintExporter leaked gdoc-shaped attrs: {gdoc_leaks_in_print}"
        )

    def test_gdoc_export_module_does_not_import_canvas_comic(self):
        """Substrate-neutrality check (ADR-001 + ADR-011 §D2): the gdoc
        carrier must not import comic-specific application modules."""
        import canvas_core.gdoc_export as mod

        source = open(mod.__file__).read()
        assert "canvas_comic" not in source
        assert "from canvas_comic" not in source


# ---------------------------------------------------------------------------
# Bonus: end-to-end helper smoke (also mocked)
# ---------------------------------------------------------------------------


class TestExportHelper:
    """Module-level convenience wrapper."""

    def test_helper_rejects_empty_elements(self):
        with pytest.raises(ValueError, match="empty elements"):
            export_canvas_to_gdoc([], "t")

    def test_helper_round_trip_returns_doc_id(self, monkeypatch):
        docs, drive = _mock_docs_and_drive(doc_id="DOC_HELP")
        _patch_services(monkeypatch, docs, drive)
        doc_id = export_canvas_to_gdoc(
            [Paragraph("hi"), Heading("Top", level=1)],
            title="helper-doc",
        )
        assert doc_id == "DOC_HELP"

    def test_share_with_invokes_drive_permissions_create_per_email(self, monkeypatch):
        docs, drive = _mock_docs_and_drive()
        _patch_services(monkeypatch, docs, drive)
        export_canvas_to_gdoc(
            [Paragraph("p")],
            title="t",
            share_with=["a@x.com", "b@x.com"],
        )
        # Assert the two share emails surface as emailAddress kwargs on the
        # captured permissions().create(...) calls (semantic check; avoids
        # MagicMock setup-chain inflation of call_count).
        emails = [
            c.kwargs.get("body", {}).get("emailAddress")
            for c in drive.permissions().create.call_args_list
            if c.kwargs
        ]
        assert "a@x.com" in emails
        assert "b@x.com" in emails
