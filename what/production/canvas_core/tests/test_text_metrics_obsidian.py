"""Tests for the Obsidian-calibrated extent model (Halftone HV O2).

The model's constants are Obsidian-CSS-derived and were validated against
two operator-observed failures before adoption (Kennedy coord 2026-08-03):
n_s01 (320x110, `##` lead) predicted ~52% shown, observed ~51%.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.text_metrics import (
    OBSIDIAN_LEAD_COST,
    OBSIDIAN_SAFE_FILL,
    classify_lead_block,
    measure_obsidian_extent,
    obsidian_chars_per_line,
    obsidian_required_node_height,
)


class TestClassifyLead:
    def test_kinds(self):
        assert classify_lead_block("# T") == "h1"
        assert classify_lead_block("## T") == "h2"
        assert classify_lead_block("### T") == "h3"
        assert classify_lead_block("#### T") == "h4"
        assert classify_lead_block("**T** rest") == "bold"
        assert classify_lead_block("plain") == "plain"


class TestCharsPerLine:
    def test_padding_subtracted(self):
        # (320 - 48) / 8.1 = 33 chars at body size
        assert obsidian_chars_per_line(320) == 33

    def test_heading_factor_narrows(self):
        assert obsidian_chars_per_line(320, 1.6) < obsidian_chars_per_line(320)

    def test_never_below_one(self):
        assert obsidian_chars_per_line(10) == 1


class TestMeasure:
    def test_empty_is_zero(self):
        assert measure_obsidian_extent("", 320) == 0.0

    def test_h2_lead_costs_more_than_bold(self):
        body = "\nSame body text that wraps a couple of lines at this width."
        h2 = measure_obsidian_extent("## Title" + body, 320)
        bold = measure_obsidian_extent("**Title**" + body, 320)
        expected = OBSIDIAN_LEAD_COST["h2"] - OBSIDIAN_LEAD_COST["bold"]
        assert abs((h2 - bold) - expected) < 1e-9

    def test_oration_n_s01_calibration_point(self):
        """The validated failure: 320x110 with a `##` lead shows ~52%."""
        text = (
            "## Discovery\n"
            "Interview the subject until the story surprises you; the detail "
            "that embarrasses them is usually the one that moves the room."
        )
        need = measure_obsidian_extent(text, 320)
        avail = OBSIDIAN_SAFE_FILL * 110
        assert need > avail  # it overflows
        shown = avail / need
        assert 0.30 < shown < 0.70  # the observed "about half" band

    def test_non_collapsing_paragraph_margins(self):
        one = measure_obsidian_extent("Line one.", 320)
        two = measure_obsidian_extent("Line one.\nLine two.", 320)
        # Second paragraph adds its line PLUS a full (non-collapsed) margin.
        assert two > 2 * one


class TestRequiredHeight:
    def test_hint_rounds_up_to_ten(self):
        h = obsidian_required_node_height("**T**\nSome body text.", 320)
        assert h % 10 == 0
        assert measure_obsidian_extent("**T**\nSome body text.", 320) <= OBSIDIAN_SAFE_FILL * h

    def test_empty_zero(self):
        assert obsidian_required_node_height("", 320) == 0
