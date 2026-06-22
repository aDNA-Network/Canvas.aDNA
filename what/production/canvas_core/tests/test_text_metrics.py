"""Tests for canvas_core.text_metrics (M-1-07 O1)."""

from __future__ import annotations

import pytest

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.text_metrics import (
    _strip_markdown,
    measure_text_extent,
)


# ---------------------------------------------------------------------------
# Markdown stripping
# ---------------------------------------------------------------------------


class TestStripMarkdown:
    def test_bold(self):
        assert _strip_markdown("**bold text**") == "bold text"

    def test_italic(self):
        assert _strip_markdown("*italic*") == "italic"

    def test_heading(self):
        assert _strip_markdown("## Heading") == "Heading"

    def test_link(self):
        assert _strip_markdown("[click](http://example.com)") == "click"

    def test_mixed(self):
        result = _strip_markdown("**bold** and *italic* with `code`")
        assert result == "bold and italic with code"

    def test_plain(self):
        assert _strip_markdown("no markdown here") == "no markdown here"

    def test_bullet(self):
        assert _strip_markdown("- item one") == "item one"


# ---------------------------------------------------------------------------
# Text measurement — heuristic path
# ---------------------------------------------------------------------------


class TestMeasureTextExtent:
    def test_empty_text(self):
        w, h, path = measure_text_extent("")
        assert w == 0.0
        assert h == 0.0

    def test_short_text_fits(self):
        w, h, path = measure_text_extent("Hi", font_size=16.0, max_width=200)
        assert w < 200
        assert h > 0
        assert path in ("pillow", "heuristic")

    def test_long_text_wider_than_max(self):
        """Long text in a narrow box should wrap — height increases."""
        text = "This is a very long sentence that should definitely wrap"
        _, h_narrow, _ = measure_text_extent(text, font_size=16.0, max_width=80)
        _, h_wide, _ = measure_text_extent(text, font_size=16.0, max_width=800)
        assert h_narrow > h_wide

    def test_multiline_text(self):
        text = "Line one\nLine two\nLine three"
        _, h, _ = measure_text_extent(text, font_size=16.0)
        # Three lines should be taller than one line.
        _, h_single, _ = measure_text_extent("Line one", font_size=16.0)
        assert h > h_single

    def test_markdown_stripped_for_measurement(self):
        """Bold markers should not inflate width."""
        w_md, _, _ = measure_text_extent("**bold**", font_size=16.0)
        w_plain, _, _ = measure_text_extent("bold", font_size=16.0)
        # They may not be exactly equal (heuristic rounding), but close.
        assert abs(w_md - w_plain) < 2.0

    def test_returns_three_tuple(self):
        result = measure_text_extent("test")
        assert len(result) == 3
        assert isinstance(result[0], float)
        assert isinstance(result[1], float)
        assert result[2] in ("pillow", "heuristic")

    def test_font_size_scales_measurement(self):
        _, h_small, _ = measure_text_extent("Hello", font_size=12.0)
        _, h_large, _ = measure_text_extent("Hello", font_size=24.0)
        assert h_large > h_small
