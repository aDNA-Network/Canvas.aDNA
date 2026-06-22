"""Tests for the HTML slide renderer.

Covers: slide extraction, markdown conversion, HTML rendering,
node positioning, theme application, and full presentation rendering.

Migrated from `lattice-protocol/extensions/canvas/tests/test_html_renderer.py`
under M-R5-01a (campaign_canvasforge_review). Pure substrate — no
canvas_presentation / canvas_comic imports. Substrate target:
`canvas_core/html_renderer.py` (1801 LOC; largest substrate module + this
test file's primary risk concentration). Theme constants previously living
in upstream `canvas_config.py` are consolidated under `canvas_core.html_renderer`
in canonical, so this migration collapses two imports into one.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import json
import tempfile
from pathlib import Path

import pytest

from canvas_core.html_renderer import (
    PRESENTATION_THEMES,
    THEME_LATTICE_LIGHT,
    THEME_PALETTES,
    THEME_TOKYO_NIGHT,
    THEMES,
    TOKYO_NIGHT_BG,
    TOKYO_NIGHT_COLORS,
    RenderedPresentation,
    SlideHTML,
    ThemePalette,
    ThemePalette as ConfigThemePalette,
    _color_slot_to_hex,
    _convert_tables,
    _escape_html,
    _generate_type_css,
    _get_palette,
    _infer_slide_type,
    _md_to_html,
    extract_slides,
    render_canvas_data,
    render_presentation,
    render_slide_html,
)
from canvas_core.design_tokens import validate_theme_palette

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def minimal_canvas():
    """Minimal canvas with one title slide."""
    return {
        "nodes": [
            {
                "id": "g1",
                "type": "group",
                "x": 0,
                "y": 0,
                "width": 1200,
                "height": 1100,
                "color": "6",
                "label": "Title Slide",
            },
            {
                "id": "n1",
                "type": "text",
                "x": 60,
                "y": 40,
                "width": 1080,
                "height": 200,
                "text": "# Hello World",
                "styleAttributes": {"textAlign": "center", "cssclasses": "hero"},
            },
        ],
        "edges": [],
        "metadata": {"startNode": "g1"},
    }


@pytest.fixture
def multi_slide_canvas():
    """Canvas with 3 slides in 2-column grid with navigation edges."""
    return {
        "nodes": [
            {
                "id": "g1",
                "type": "group",
                "x": 0,
                "y": 0,
                "width": 1200,
                "height": 1100,
                "color": "6",
                "label": "Title",
            },
            {
                "id": "t1",
                "type": "text",
                "x": 60,
                "y": 198,
                "width": 1080,
                "height": 200,
                "text": "# Presentation Title",
                "styleAttributes": {"textAlign": "center", "cssclasses": "hero"},
            },
            {
                "id": "g2",
                "type": "group",
                "x": 1400,
                "y": 0,
                "width": 1200,
                "height": 1100,
                "color": "1",
                "label": "The Problem",
            },
            {
                "id": "t2h",
                "type": "text",
                "x": 1460,
                "y": 40,
                "width": 1080,
                "height": 120,
                "text": "## The Problem",
                "styleAttributes": {"cssclasses": "cl-pres-content"},
            },
            {
                "id": "t2b",
                "type": "text",
                "x": 1460,
                "y": 180,
                "width": 1080,
                "height": 400,
                "text": "### Issues\n\n- **Problem one**: details\n- Problem two\n- Problem three",
                "styleAttributes": {
                    "latticeRole": "critical",
                    "cssclasses": "cl-pres-content critical",
                },
            },
            {
                "id": "g3",
                "type": "group",
                "x": 0,
                "y": 1300,
                "width": 1200,
                "height": 1100,
                "color": "5",
                "label": "Stats",
            },
            {
                "id": "t3h",
                "type": "text",
                "x": 60,
                "y": 1340,
                "width": 1080,
                "height": 120,
                "text": "## Key Metrics",
                "styleAttributes": {"cssclasses": "cl-pres-stats"},
            },
            {
                "id": "t3s1",
                "type": "text",
                "x": 60,
                "y": 1480,
                "width": 251,
                "height": 250,
                "color": "5",
                "text": "# 42\n\n*Units Sold*",
                "styleAttributes": {
                    "shape": "pill",
                    "textAlign": "center",
                    "cssclasses": "cl-pres-stats",
                },
            },
            {
                "id": "t3s2",
                "type": "text",
                "x": 336,
                "y": 1480,
                "width": 251,
                "height": 250,
                "color": "5",
                "text": "# 99%\n\n*Uptime*",
                "styleAttributes": {
                    "shape": "pill",
                    "textAlign": "center",
                    "cssclasses": "cl-pres-stats",
                },
            },
        ],
        "edges": [
            {
                "id": "e1",
                "fromNode": "g1",
                "toNode": "g2",
                "fromSide": "right",
                "toSide": "left",
                "toEnd": "arrow",
            },
            {
                "id": "e2",
                "fromNode": "g2",
                "toNode": "g3",
                "fromSide": "bottom",
                "toSide": "top",
                "toEnd": "arrow",
            },
        ],
        "metadata": {
            "startNode": "g1",
            "frontmatter": {
                "_reserved": {"theme": "lattice_brand"},
            },
        },
    }


# ---------------------------------------------------------------------------
# Slide Extraction
# ---------------------------------------------------------------------------


class TestExtractSlides:
    def test_single_slide(self, minimal_canvas):
        slides = extract_slides(minimal_canvas)
        assert len(slides) == 1
        assert slides[0]["label"] == "Title Slide"
        assert slides[0]["color"] == "6"
        assert len(slides[0]["nodes"]) == 1

    def test_multi_slide_order(self, multi_slide_canvas):
        slides = extract_slides(multi_slide_canvas)
        assert len(slides) == 3
        # Navigation edges should produce: Title -> Problem -> Stats
        assert slides[0]["label"] == "Title"
        assert slides[1]["label"] == "The Problem"
        assert slides[2]["label"] == "Stats"

    def test_contained_nodes(self, multi_slide_canvas):
        slides = extract_slides(multi_slide_canvas)
        # Title slide has 1 text node
        assert len(slides[0]["nodes"]) == 1
        # Problem slide has 2 text nodes (heading + body)
        assert len(slides[1]["nodes"]) == 2
        # Stats slide has 3 nodes (heading + 2 pills)
        assert len(slides[2]["nodes"]) == 3

    def test_slide_type_inference(self, multi_slide_canvas):
        slides = extract_slides(multi_slide_canvas)
        assert slides[0]["slide_type"] == "title"
        assert slides[1]["slide_type"] == "content"
        assert slides[2]["slide_type"] == "stats"

    def test_empty_canvas(self):
        slides = extract_slides({"nodes": [], "edges": []})
        assert slides == []

    def test_groups_without_edges(self):
        canvas = {
            "nodes": [
                {
                    "id": "g1",
                    "type": "group",
                    "x": 0,
                    "y": 0,
                    "width": 1200,
                    "height": 1100,
                    "label": "First",
                },
                {
                    "id": "g2",
                    "type": "group",
                    "x": 1400,
                    "y": 0,
                    "width": 1200,
                    "height": 1100,
                    "label": "Second",
                },
            ],
            "edges": [],
        }
        slides = extract_slides(canvas)
        assert len(slides) == 2
        # Should fall back to spatial order
        assert slides[0]["label"] == "First"
        assert slides[1]["label"] == "Second"


# ---------------------------------------------------------------------------
# Slide Type Inference
# ---------------------------------------------------------------------------


class TestSlideTypeInference:
    def test_hero_class(self):
        group = {"id": "g1"}
        nodes = [{"styleAttributes": {"cssclasses": "hero"}}]
        assert _infer_slide_type(group, nodes, 0) == "title"

    def test_stats_class(self):
        group = {"id": "g1"}
        nodes = [{"styleAttributes": {"cssclasses": "cl-pres-stats"}}]
        assert _infer_slide_type(group, nodes, 1) == "stats"

    def test_comparison_class(self):
        group = {"id": "g1"}
        nodes = [{"styleAttributes": {"cssclasses": "cl-pres-comparison"}}]
        assert _infer_slide_type(group, nodes, 1) == "comparison"

    def test_process_class(self):
        group = {"id": "g1"}
        nodes = [{"styleAttributes": {"cssclasses": "cl-pres-process"}}]
        assert _infer_slide_type(group, nodes, 1) == "process"

    def test_key_value_class(self):
        group = {"id": "g1"}
        nodes = [{"styleAttributes": {"cssclasses": "cl-pres-kv"}}]
        assert _infer_slide_type(group, nodes, 1) == "key_value"

    def test_pill_shapes_infer_stats(self):
        group = {"id": "g1"}
        nodes = [
            {"styleAttributes": {"shape": "pill"}},
            {"styleAttributes": {"shape": "pill"}},
        ]
        assert _infer_slide_type(group, nodes, 1) == "stats"

    def test_first_slide_few_words_is_title(self):
        group = {"id": "g1"}
        nodes = [{"text": "Hello", "styleAttributes": {}}]
        assert _infer_slide_type(group, nodes, 0) == "title"

    def test_default_content(self):
        group = {"id": "g1"}
        nodes = [{"styleAttributes": {}}]
        assert _infer_slide_type(group, nodes, 5) == "content"


# ---------------------------------------------------------------------------
# Markdown -> HTML
# ---------------------------------------------------------------------------


class TestMarkdownToHtml:
    def test_heading(self):
        html = _md_to_html("# Title")
        assert "<h1>Title</h1>" in html

    def test_h2(self):
        html = _md_to_html("## Subtitle")
        assert "<h2>Subtitle</h2>" in html

    def test_bold(self):
        html = _md_to_html("**bold text**")
        assert "<strong>bold text</strong>" in html

    def test_italic(self):
        html = _md_to_html("*italic*")
        assert "<em>italic</em>" in html

    def test_inline_code(self):
        html = _md_to_html("`code`")
        assert "<code>code</code>" in html

    def test_unordered_list(self):
        html = _md_to_html("- item 1\n- item 2")
        assert "<ul>" in html
        assert "<li>item 1</li>" in html
        assert "<li>item 2</li>" in html
        assert "</ul>" in html

    def test_ordered_list(self):
        html = _md_to_html("1. first\n2. second")
        assert "<ol>" in html
        assert "<li>first</li>" in html
        assert "</ol>" in html

    def test_code_block(self):
        html = _md_to_html("```python\nprint('hi')\n```")
        assert "<pre><code" in html
        assert "print(" in html
        assert "</code></pre>" in html

    def test_blockquote(self):
        html = _md_to_html("> quoted text")
        assert "<blockquote>" in html
        assert "quoted text" in html

    def test_link(self):
        html = _md_to_html("[click](https://example.com)")
        assert '<a href="https://example.com">click</a>' in html

    def test_horizontal_rule(self):
        html = _md_to_html("---")
        assert "<hr>" in html

    def test_empty_text(self):
        assert _md_to_html("") == ""

    def test_mixed_content(self):
        md = "# Title\n\n- **Bold** item\n- *Italic* item\n\nParagraph"
        html = _md_to_html(md)
        assert "<h1>Title</h1>" in html
        assert "<strong>Bold</strong>" in html
        assert "<em>Italic</em>" in html
        assert "<p>Paragraph</p>" in html


# ---------------------------------------------------------------------------
# HTML Rendering
# ---------------------------------------------------------------------------


class TestRenderSlideHtml:
    def test_basic_render(self, minimal_canvas):
        slides = extract_slides(minimal_canvas)
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert "<!DOCTYPE html>" in html
        assert "Title Slide" in html
        assert "Hello World" in html

    def test_contains_css(self, minimal_canvas):
        slides = extract_slides(minimal_canvas)
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert TOKYO_NIGHT_BG in html
        assert "font-size" in html

    def test_node_positioning(self, minimal_canvas):
        slides = extract_slides(minimal_canvas)
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert "position: absolute" in html or "left:" in html

    def test_color_applied(self, minimal_canvas):
        slides = extract_slides(minimal_canvas)
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert "has-color" in html
        purple_hex = TOKYO_NIGHT_COLORS["6"]
        assert purple_hex in html

    def test_text_alignment(self, minimal_canvas):
        slides = extract_slides(minimal_canvas)
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert "align-center" in html

    def test_shape_pill(self, multi_slide_canvas):
        slides = extract_slides(multi_slide_canvas)
        stats_slide = slides[2]  # Stats slide
        html = render_slide_html(stats_slide, THEME_TOKYO_NIGHT)
        assert "shape-pill" in html

    def test_lattice_role(self, multi_slide_canvas):
        slides = extract_slides(multi_slide_canvas)
        problem_slide = slides[1]  # Problem slide
        html = render_slide_html(problem_slide, THEME_TOKYO_NIGHT)
        assert "role-critical" in html

    def test_viewport_dimensions(self, minimal_canvas):
        slides = extract_slides(minimal_canvas)
        html = render_slide_html(
            slides[0],
            THEME_TOKYO_NIGHT,
            viewport_width=1920,
            viewport_height=1080,
        )
        assert "width:1920px" in html
        assert "height:1080px" in html


# ---------------------------------------------------------------------------
# Color Utilities
# ---------------------------------------------------------------------------


class TestColorUtils:
    def test_slot_to_hex(self):
        assert _color_slot_to_hex("6") == TOKYO_NIGHT_COLORS["6"]
        assert _color_slot_to_hex("1") == TOKYO_NIGHT_COLORS["1"]

    def test_hex_passthrough(self):
        assert _color_slot_to_hex("#ff0000") == "#ff0000"

    def test_none_fallback(self):
        result = _color_slot_to_hex(None)
        assert result.startswith("#")

    def test_escape_html(self):
        assert _escape_html("<script>") == "&lt;script&gt;"
        assert _escape_html('a "b"') == "a &quot;b&quot;"


# ---------------------------------------------------------------------------
# Themed Rendering
# ---------------------------------------------------------------------------


class TestThemedRendering:
    def test_all_themes_registered(self):
        assert len(THEMES) == 8
        assert "tokyo_night" in THEMES
        assert "lattice_brand" in THEMES
        assert "scientific" in THEMES
        assert "wilhelm_foundation" in THEMES

    def test_theme_font_in_css(self, minimal_canvas):
        slides = extract_slides(minimal_canvas)
        for name, theme in THEMES.items():
            html = render_slide_html(slides[0], theme)
            if theme.font_suggestion:
                # At least the first font family should appear
                first_font = theme.font_suggestion.split(",")[0].strip()
                assert first_font in html, f"Theme {name} font not found"

    def test_wilhelm_foundation_font_renders(self, minimal_canvas):
        """M-V1-09: Wilhelm Foundation theme renders with Charter serif font."""
        with tempfile.TemporaryDirectory() as tmpdir:
            canvas_path = Path(tmpdir) / "test.canvas"
            canvas_path.write_text(json.dumps(minimal_canvas))
            result = render_presentation(
                canvas_path,
                Path(tmpdir) / "output",
                theme_name="wilhelm_foundation",
            )
            assert result.theme_name == "wilhelm_foundation"
            html = (Path(tmpdir) / "output" / result.slides[0].filename).read_text()
            assert "Charter" in html


# ---------------------------------------------------------------------------
# Full Presentation Rendering
# ---------------------------------------------------------------------------


class TestRenderPresentation:
    def test_renders_to_files(self, multi_slide_canvas):
        with tempfile.TemporaryDirectory() as tmpdir:
            canvas_path = Path(tmpdir) / "test.canvas"
            canvas_path.write_text(json.dumps(multi_slide_canvas))

            result = render_presentation(canvas_path, Path(tmpdir) / "output")

            assert isinstance(result, RenderedPresentation)
            assert len(result.slides) == 3
            assert result.theme_name == "lattice_brand"

            # Check files exist
            for slide in result.slides:
                fpath = Path(tmpdir) / "output" / slide.filename
                assert fpath.exists(), f"Missing: {fpath}"
                content = fpath.read_text()
                assert "<!DOCTYPE html>" in content

    def test_theme_override(self, minimal_canvas):
        with tempfile.TemporaryDirectory() as tmpdir:
            canvas_path = Path(tmpdir) / "test.canvas"
            canvas_path.write_text(json.dumps(minimal_canvas))

            result = render_presentation(
                canvas_path,
                Path(tmpdir) / "output",
                theme_name="scientific",
            )
            assert result.theme_name == "scientific"

    def test_render_canvas_data(self, multi_slide_canvas):
        slides = render_canvas_data(multi_slide_canvas)
        assert len(slides) == 3
        assert all(isinstance(s, SlideHTML) for s in slides)
        assert all(s.html.startswith("<!DOCTYPE html>") for s in slides)

    def test_filenames_sanitized(self, minimal_canvas):
        slides = render_canvas_data(minimal_canvas)
        for s in slides:
            assert "/" not in s.filename
            assert s.filename.endswith(".html")
            assert s.filename.startswith("slide_")


# ---------------------------------------------------------------------------
# File Node Rendering
# ---------------------------------------------------------------------------


class TestFileNodeRendering:
    def test_file_node_placeholder(self):
        canvas = {
            "nodes": [
                {
                    "id": "g1",
                    "type": "group",
                    "x": 0,
                    "y": 0,
                    "width": 1200,
                    "height": 1100,
                    "label": "Image Slide",
                },
                {
                    "id": "f1",
                    "type": "file",
                    "x": 200,
                    "y": 200,
                    "width": 800,
                    "height": 500,
                    "file": "images/diagram.png",
                },
            ],
            "edges": [],
        }
        slides = render_canvas_data(canvas)
        assert len(slides) == 1
        assert "[Image: diagram.png]" in slides[0].html

    def test_link_node_placeholder(self):
        canvas = {
            "nodes": [
                {
                    "id": "g1",
                    "type": "group",
                    "x": 0,
                    "y": 0,
                    "width": 1200,
                    "height": 1100,
                    "label": "Video Slide",
                },
                {
                    "id": "l1",
                    "type": "link",
                    "x": 100,
                    "y": 200,
                    "width": 1000,
                    "height": 562,
                    "url": "https://youtube.com/watch?v=abc123",
                },
            ],
            "edges": [],
        }
        slides = render_canvas_data(canvas)
        assert len(slides) == 1
        assert "[Embed:" in slides[0].html


# ---------------------------------------------------------------------------
# Session 2: Theme Palette System
# ---------------------------------------------------------------------------


class TestThemePalettes:
    """Verify per-theme palette system produces correct colors."""

    def test_all_themes_have_palettes(self):
        for name in THEMES:
            palette = _get_palette(name)
            assert isinstance(palette, ThemePalette), f"No palette for {name}"
            assert palette.bg.startswith("#")
            assert palette.text.startswith("#")

    def test_dark_themes_have_dark_bg(self):
        dark_themes = ["tokyo_night", "lattice_dark", "lattice_brand", "science_stanley"]
        for name in dark_themes:
            palette = _get_palette(name)
            # Dark backgrounds have low RGB values
            bg_r = int(palette.bg[1:3], 16)
            assert bg_r < 80, f"{name} bg doesn't look dark: {palette.bg}"

    def test_light_themes_have_light_bg(self):
        light_themes = ["lattice_light", "scientific", "academic", "wilhelm_foundation"]
        for name in light_themes:
            palette = _get_palette(name)
            # Light backgrounds have high RGB values
            bg_r = int(palette.bg[1:3], 16)
            assert bg_r > 200, f"{name} bg doesn't look light: {palette.bg}"

    def test_light_themes_have_dark_text(self):
        light_themes = ["lattice_light", "scientific", "academic", "wilhelm_foundation"]
        for name in light_themes:
            palette = _get_palette(name)
            text_r = int(palette.text[1:3], 16)
            assert text_r < 80, f"{name} text not dark: {palette.text}"

    def test_wilhelm_foundation_palette_distinct(self):
        """M-V1-09: Wilhelm Foundation palette differs from THEME_ACADEMIC (off-white shift)."""
        wilhelm = _get_palette("wilhelm_foundation")
        academic = _get_palette("academic")
        assert wilhelm.bg == "#fffefb"
        assert wilhelm.bg != academic.bg
        assert wilhelm.text == "#1f2a2a"
        assert wilhelm.text != academic.text

    def test_dark_themes_have_light_text(self):
        dark_themes = ["tokyo_night", "lattice_dark"]
        for name in dark_themes:
            palette = _get_palette(name)
            text_r = int(palette.text[1:3], 16)
            assert text_r > 150, f"{name} text not light: {palette.text}"

    @pytest.mark.parametrize("theme_name", list(THEMES.keys()))
    def test_render_uses_palette_bg(self, minimal_canvas, theme_name):
        """Each theme renders with its own background color."""
        slides = extract_slides(minimal_canvas)
        theme = THEMES[theme_name]
        palette = _get_palette(theme_name)
        html = render_slide_html(
            slides[0],
            theme,
            theme_name=theme_name,
        )
        assert palette.bg in html, f"{theme_name} bg {palette.bg} not in HTML"

    @pytest.mark.parametrize("theme_name", list(THEMES.keys()))
    def test_render_uses_palette_text(self, minimal_canvas, theme_name):
        """Each theme renders with its own text color."""
        slides = extract_slides(minimal_canvas)
        theme = THEMES[theme_name]
        palette = _get_palette(theme_name)
        html = render_slide_html(
            slides[0],
            theme,
            theme_name=theme_name,
        )
        assert palette.text in html, f"{theme_name} text {palette.text} not in HTML"

    # M05: THEME_LATTICE_LIGHT restored — un-skipped
    def test_light_theme_no_tokyo_night_bg(self, minimal_canvas):
        """Light themes must NOT contain Tokyo Night dark background."""
        slides = extract_slides(minimal_canvas)
        html = render_slide_html(
            slides[0],
            THEME_LATTICE_LIGHT,
            theme_name="lattice_light",
        )
        assert TOKYO_NIGHT_BG not in html

    def test_unknown_theme_gets_dark_palette(self):
        palette = _get_palette("nonexistent_theme")
        assert palette.bg == "#1a1b26"  # Falls back to dark

    def test_color_slot_respects_palette(self):
        light = _get_palette("lattice_light")
        result = _color_slot_to_hex(None, light)
        assert result == light.bg_lighter


# ---------------------------------------------------------------------------
# Session 3: Per-Slide-Type CSS
# ---------------------------------------------------------------------------


class TestSlideTypeCss:
    """Verify slide-type-specific CSS is generated and applied."""

    def test_type_css_generated(self):
        css = _generate_type_css(THEME_TOKYO_NIGHT)
        assert "slide-type-title" in css
        assert "slide-type-quote" in css
        assert "slide-type-stats" in css
        assert "slide-type-comparison" in css
        assert "slide-type-timeline" in css
        assert "slide-type-process" in css

    def test_type_css_has_per_type_margins(self):
        css = _generate_type_css(THEME_TOKYO_NIGHT)
        # Title should have 64px top margin (SPACE_3XL)
        assert "padding: 64px 64px 48px" in css
        # Section divider should have 96px top margin (SPACE_4XL)
        assert "padding: 96px 64px 48px" in css

    def test_slide_type_class_in_html(self, minimal_canvas):
        """Rendered HTML includes slide-type-{type} class."""
        slides = extract_slides(minimal_canvas)
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert "slide-type-title" in html

    def test_content_slide_has_type_class(self, multi_slide_canvas):
        slides = extract_slides(multi_slide_canvas)
        html = render_slide_html(slides[1], THEME_TOKYO_NIGHT)
        assert "slide-type-content" in html

    def test_stats_slide_has_type_class(self, multi_slide_canvas):
        slides = extract_slides(multi_slide_canvas)
        html = render_slide_html(slides[2], THEME_TOKYO_NIGHT)
        assert "slide-type-stats" in html

    def test_quote_css_has_accent_border(self):
        css = _generate_type_css(THEME_TOKYO_NIGHT)
        assert "slide-type-quote" in css
        assert "border-left: 4px solid" in css

    def test_stats_css_has_pill_styling(self):
        css = _generate_type_css(THEME_TOKYO_NIGHT)
        assert "slide-type-stats .slide-node.shape-pill" in css

    def test_comparison_css_has_column_borders(self):
        css = _generate_type_css(THEME_TOKYO_NIGHT)
        assert "slide-type-comparison .flow-row .slide-node" in css
        assert "border-right:" in css

    def test_timeline_css_has_left_line(self):
        css = _generate_type_css(THEME_TOKYO_NIGHT)
        assert "slide-type-timeline" in css
        assert "border-left: 3px solid" in css

    # M05: THEME_LATTICE_LIGHT restored — un-skipped
    def test_type_css_uses_palette(self):
        """Light theme type CSS uses light palette colors."""
        light = _get_palette("lattice_light")
        css = _generate_type_css(THEME_LATTICE_LIGHT, light)
        assert light.border in css
        assert light.bg_lighter in css

    def test_collage_has_tight_spacing(self):
        css = _generate_type_css(THEME_TOKYO_NIGHT)
        assert "slide-type-collage" in css
        # Collage should use sm gap (12px)
        assert "gap: 12px" in css

    def test_key_value_has_uppercase_label(self):
        css = _generate_type_css(THEME_TOKYO_NIGHT)
        assert "slide-type-key_value" in css
        assert "text-transform: uppercase" in css


# ---------------------------------------------------------------------------
# Session 4A: Markdown Table Support
# ---------------------------------------------------------------------------


class TestMarkdownTables:
    """Verify pipe-delimited markdown tables convert to HTML."""

    def test_basic_table(self):
        md = "| A | B |\n| --- | --- |\n| 1 | 2 |"
        html = _md_to_html(md)
        assert "<table>" in html
        assert "<th>A</th>" in html
        assert "<th>B</th>" in html
        assert "<td>1</td>" in html
        assert "<td>2</td>" in html
        assert "</table>" in html

    def test_table_with_multiple_rows(self):
        md = "| Name | Value |\n| --- | --- |\n| x | 1 |\n| y | 2 |\n| z | 3 |"
        html = _md_to_html(md)
        assert html.count("<tr>") == 4  # 1 header + 3 data rows

    def test_table_with_inline_formatting(self):
        md = "| Col |\n| --- |\n| **bold** |"
        html = _md_to_html(md)
        assert "<strong>bold</strong>" in html

    def test_table_in_mixed_content(self):
        md = "# Title\n\n| A | B |\n| --- | --- |\n| 1 | 2 |\n\nParagraph"
        html = _md_to_html(md)
        assert "<h1>Title</h1>" in html
        assert "<table>" in html
        assert "<p>Paragraph</p>" in html

    def test_non_table_pipes_ignored(self):
        md = "A | B"
        html = _md_to_html(md)
        assert "<table>" not in html

    def test_convert_tables_standalone(self):
        text = "| H1 | H2 |\n| --- | --- |\n| v1 | v2 |"
        result = _convert_tables(text)
        assert "<table>" in result
        assert "<thead>" in result
        assert "<tbody>" in result

    def test_table_ends_at_non_pipe_line(self):
        md = "| A |\n| --- |\n| 1 |\nNot a table"
        html = _md_to_html(md)
        assert "<td>1</td>" in html
        assert "Not a table" in html


# ---------------------------------------------------------------------------
# Session 4B: Letter Spacing in Typography
# ---------------------------------------------------------------------------


class TestLetterSpacing:
    """Verify letter-spacing from design tokens is in CSS output."""

    def test_h1_has_letter_spacing(self, minimal_canvas):
        slides = extract_slides(minimal_canvas)
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert "letter-spacing:" in html
        assert "-0.015em" in html  # h1 letter-spacing

    def test_display_has_letter_spacing(self, minimal_canvas):
        slides = extract_slides(minimal_canvas)
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert "-0.02em" in html  # display letter-spacing


# ---------------------------------------------------------------------------
# Visual Refinement: Mermaid CDN Integration
# ---------------------------------------------------------------------------


class TestMermaidRendering:
    """Verify Mermaid.js CDN integration in HTML output."""

    def test_mermaid_block_uses_pre_class(self):
        """Mermaid code blocks emit <pre class='mermaid'> not <pre><code>."""
        html = _md_to_html("```mermaid\ngraph TD\n  A-->B\n```")
        assert '<pre class="mermaid">' in html
        assert "graph TD" in html
        assert "<code" not in html  # No <code> wrapper for mermaid

    def test_regular_code_block_unchanged(self):
        """Non-mermaid code blocks still use <pre><code>."""
        html = _md_to_html("```python\nprint('hi')\n```")
        assert '<pre><code class="language-python">' in html
        assert "</code></pre>" in html

    def test_mermaid_content_not_escaped(self):
        """Mermaid content preserves arrows and special chars."""
        html = _md_to_html("```mermaid\ngraph TD\n  A-->B\n```")
        assert "A-->B" in html

    def test_mermaid_cdn_script_included(self):
        """Slides with mermaid content include CDN script."""
        canvas = {
            "nodes": [
                {
                    "id": "g1",
                    "type": "group",
                    "x": 0,
                    "y": 0,
                    "width": 1200,
                    "height": 1100,
                    "label": "Diagram",
                },
                {
                    "id": "n1",
                    "type": "text",
                    "x": 60,
                    "y": 40,
                    "width": 1080,
                    "height": 800,
                    "text": "## Flowchart\n\n```mermaid\ngraph TD\n  A-->B\n```",
                    "styleAttributes": {},
                },
            ],
            "edges": [],
        }
        slides = extract_slides(canvas)
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert "mermaid.min.js" in html
        assert "mermaid.initialize" in html
        assert '"dark"' in html  # Dark theme for tokyo_night

    def test_mermaid_cdn_not_included_without_mermaid(self, minimal_canvas):
        """Slides without mermaid do NOT include CDN script."""
        slides = extract_slides(minimal_canvas)
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert "mermaid.min.js" not in html

    # M05: THEME_LATTICE_LIGHT restored — un-skipped
    def test_mermaid_light_theme(self):
        """Light themes use 'default' mermaid theme."""
        canvas = {
            "nodes": [
                {
                    "id": "g1",
                    "type": "group",
                    "x": 0,
                    "y": 0,
                    "width": 1200,
                    "height": 1100,
                    "label": "Diagram",
                },
                {
                    "id": "n1",
                    "type": "text",
                    "x": 60,
                    "y": 40,
                    "width": 1080,
                    "height": 800,
                    "text": "```mermaid\ngraph LR\n  X-->Y\n```",
                    "styleAttributes": {},
                },
            ],
            "edges": [],
        }
        slides = extract_slides(canvas)
        html = render_slide_html(
            slides[0],
            THEME_LATTICE_LIGHT,
            theme_name="lattice_light",
        )
        assert '"default"' in html  # Light mermaid theme


# ---------------------------------------------------------------------------
# Visual Refinement: Subtitle Node Detection
# ---------------------------------------------------------------------------


class TestSubtitleNode:
    """Verify subtitle node detection on title slides."""

    def test_subtitle_class_on_title_slide(self):
        """Second text node in title slide gets subtitle-node class."""
        canvas = {
            "nodes": [
                {
                    "id": "g1",
                    "type": "group",
                    "x": 0,
                    "y": 0,
                    "width": 1200,
                    "height": 1100,
                    "label": "Title",
                    "color": "6",
                },
                {
                    "id": "h1",
                    "type": "text",
                    "x": 60,
                    "y": 100,
                    "width": 1080,
                    "height": 200,
                    "text": "# Main Title",
                    "styleAttributes": {"textAlign": "center", "cssclasses": "hero"},
                },
                {
                    "id": "s1",
                    "type": "text",
                    "x": 60,
                    "y": 400,
                    "width": 1080,
                    "height": 100,
                    "text": "A subtitle description",
                    "styleAttributes": {"textAlign": "center"},
                },
            ],
            "edges": [],
        }
        slides = extract_slides(canvas)
        assert slides[0]["slide_type"] == "title"
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert "heading-node" in html
        assert "subtitle-node" in html

    def test_no_subtitle_on_content_slide(self, multi_slide_canvas):
        """Content slides do NOT get subtitle-node class on nodes."""
        slides = extract_slides(multi_slide_canvas)
        html = render_slide_html(slides[1], THEME_TOKYO_NIGHT)  # Problem slide
        # subtitle-node appears in CSS but should NOT appear on any node element
        assert 'class="slide-node text-node subtitle-node' not in html

    def test_subtitle_css_exists(self, minimal_canvas):
        """Subtitle CSS rules present in output."""
        slides = extract_slides(minimal_canvas)
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert "subtitle-node" in html  # CSS rule exists


# ---------------------------------------------------------------------------
# Visual Refinement: Process Layout
# ---------------------------------------------------------------------------


class TestProcessLayout:
    """Verify process step layout fixes."""

    def test_process_solo_step_constrained(self):
        """Solo process step should be max-width constrained."""
        css = _generate_type_css(THEME_TOKYO_NIGHT)
        assert "slide-type-process .flow-row:last-child .slide-node:only-child" in css
        assert "max-width: 50%" in css
        assert "margin: 0 auto" in css

    def test_heading_no_border_top_in_process(self):
        """Heading node in process slides should not get border-top."""
        canvas = {
            "nodes": [
                {
                    "id": "g1",
                    "type": "group",
                    "x": 0,
                    "y": 0,
                    "width": 1200,
                    "height": 1100,
                    "label": "Process",
                },
                {
                    "id": "h1",
                    "type": "text",
                    "x": 60,
                    "y": 40,
                    "width": 1080,
                    "height": 120,
                    "text": "## Steps",
                    "styleAttributes": {"cssclasses": "cl-pres-process"},
                },
                {
                    "id": "s1",
                    "type": "text",
                    "x": 60,
                    "y": 200,
                    "width": 500,
                    "height": 300,
                    "text": "### Step 1\nDo this",
                    "styleAttributes": {"cssclasses": "cl-pres-process"},
                },
                {
                    "id": "s2",
                    "type": "text",
                    "x": 600,
                    "y": 200,
                    "width": 500,
                    "height": 300,
                    "text": "### Step 2\nDo that",
                    "styleAttributes": {"cssclasses": "cl-pres-process"},
                },
            ],
            "edges": [],
        }
        slides = extract_slides(canvas)
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert "heading-node" in html  # Heading detected
        # CSS: heading-node gets border-top: none
        assert "border-top: none" in html


# ---------------------------------------------------------------------------
# Visual Refinement: Image Placeholder
# ---------------------------------------------------------------------------


class TestImagePlaceholder:
    """Verify styled image placeholders."""

    def test_image_placeholder_has_dashed_border(self):
        """File nodes get dashed border placeholder style."""
        canvas = {
            "nodes": [
                {
                    "id": "g1",
                    "type": "group",
                    "x": 0,
                    "y": 0,
                    "width": 1200,
                    "height": 1100,
                    "label": "Image Slide",
                },
                {
                    "id": "f1",
                    "type": "file",
                    "x": 200,
                    "y": 200,
                    "width": 800,
                    "height": 500,
                    "file": "images/photo.png",
                },
            ],
            "edges": [],
        }
        slides = render_canvas_data(canvas)
        assert "image-placeholder" in slides[0].html
        assert "border:2px dashed" in slides[0].html
        assert "photo.png" in slides[0].html

    def test_placeholder_not_raw_text(self):
        """Image placeholder should not show bare [Pending Image] text."""
        canvas = {
            "nodes": [
                {
                    "id": "g1",
                    "type": "group",
                    "x": 0,
                    "y": 0,
                    "width": 1200,
                    "height": 1100,
                    "label": "Slide",
                },
                {
                    "id": "f1",
                    "type": "file",
                    "x": 100,
                    "y": 100,
                    "width": 800,
                    "height": 500,
                    "file": "chart.svg",
                },
            ],
            "edges": [],
        }
        slides = render_canvas_data(canvas)
        assert "opacity:0.7" in slides[0].html
        assert "border-radius:8px" in slides[0].html


# ---------------------------------------------------------------------------
# Visual Refinement: Content Overflow
# ---------------------------------------------------------------------------


class TestContentOverflow:
    """Verify overflow handling CSS."""

    def test_overflow_css_in_flow_layout(self, minimal_canvas):
        """Flow layout nodes should have overflow protection."""
        slides = extract_slides(minimal_canvas)
        html = render_slide_html(slides[0], THEME_TOKYO_NIGHT)
        assert "word-wrap: break-word" in html
        assert "overflow-wrap: break-word" in html


# ---------------------------------------------------------------------------
# Visual Refinement: Light Theme Enhancements
# ---------------------------------------------------------------------------


class TestLightThemeEnhancements:
    """Verify light theme-specific CSS improvements."""

    @pytest.mark.parametrize("theme_name", ["lattice_light", "scientific", "academic"])
    def test_light_theme_card_borders(self, minimal_canvas, theme_name):
        """Light themes add visible borders to text nodes."""
        slides = extract_slides(minimal_canvas)
        palette = _get_palette(theme_name)
        theme = THEMES[theme_name]
        html = render_slide_html(slides[0], theme, theme_name=theme_name)
        # Should have border rule for text-node
        assert f"border: 1px solid {palette.border}" in html

    @pytest.mark.parametrize("theme_name", ["tokyo_night", "lattice_dark"])
    def test_dark_theme_no_extra_borders(self, minimal_canvas, theme_name):
        """Dark themes do NOT get the light-theme card border rules."""
        slides = extract_slides(minimal_canvas)
        theme = THEMES[theme_name]
        html = render_slide_html(slides[0], theme, theme_name=theme_name)
        # The light-theme-specific section should not appear
        assert "Light theme:" not in html


# ---------------------------------------------------------------------------
# M05: Theme Consolidation + Publication-Ready HTML Tests
# ---------------------------------------------------------------------------


class TestM05ThemeConsolidation:
    """Verify all 8 themes are registered and WCAG-compliant."""

    def test_all_themes_in_presentation_themes(self):
        """PRESENTATION_THEMES has all 8 entries."""
        assert len(PRESENTATION_THEMES) == 8
        expected = {
            "tokyo_night", "lattice_brand", "scientific",
            "lattice_dark", "lattice_light", "science_stanley", "academic",
            "wilhelm_foundation",
        }
        assert set(PRESENTATION_THEMES.keys()) == expected

    def test_all_themes_in_renderer(self):
        """Renderer THEMES dict matches PRESENTATION_THEMES."""
        assert set(THEMES.keys()) == set(PRESENTATION_THEMES.keys())

    def test_all_palettes_exist(self):
        """Every theme in PRESENTATION_THEMES has a matching palette."""
        for name in PRESENTATION_THEMES:
            assert name in THEME_PALETTES, f"Missing palette for {name}"

    @pytest.mark.parametrize("theme_name", sorted(THEME_PALETTES.keys()))
    def test_theme_palette_wcag_compliance(self, theme_name):
        """All theme palettes pass WCAG AA validation."""
        palette = THEME_PALETTES[theme_name]
        issues = validate_theme_palette(palette)
        assert issues == [], f"{theme_name} WCAG issues: {issues}"


class TestM05PublicationHTML:
    """Verify publication-ready HTML features."""

    def test_css_custom_properties_in_output(self, minimal_canvas):
        """Rendered HTML contains :root block with --cl-* variables."""
        slides = extract_slides(minimal_canvas)
        theme = THEMES["scientific"]
        html = render_slide_html(slides[0], theme, theme_name="scientific")
        assert ":root" in html
        assert "--cl-space-" in html
        assert "--cl-type-" in html
        assert "--cl-bg:" in html
        assert "--cl-text:" in html
        assert "--cl-primary:" in html

    def test_print_stylesheet_present(self, minimal_canvas):
        """Rendered HTML contains @media print rules."""
        slides = extract_slides(minimal_canvas)
        theme = THEMES["scientific"]
        html = render_slide_html(slides[0], theme, theme_name="scientific")
        assert "@media print" in html
        assert "page-break-after: always" in html

    def test_publication_meta_tags(self, minimal_canvas):
        """HTML contains generator, theme, and slide-type meta tags."""
        slides = extract_slides(minimal_canvas)
        theme = THEMES["scientific"]
        html = render_slide_html(slides[0], theme, theme_name="scientific")
        assert 'name="generator"' in html
        assert 'content="Lattice Canvas HTML Renderer"' in html
        assert 'name="theme"' in html
        assert 'content="scientific"' in html
        assert 'name="slide-type"' in html

    @pytest.mark.parametrize("theme_name", sorted(THEMES.keys()))
    def test_all_themes_render_without_error(self, minimal_canvas, theme_name):
        """Every theme produces non-empty HTML without errors."""
        slides = extract_slides(minimal_canvas)
        theme = THEMES[theme_name]
        html = render_slide_html(slides[0], theme, theme_name=theme_name)
        assert len(html) > 200, f"{theme_name} HTML too short"
        palette = THEME_PALETTES[theme_name]
        assert palette.bg in html, f"{theme_name} bg color missing"


# ---------------------------------------------------------------------------
# Typography Token Contract V2 routing (ADR-009; M-V1-2-B-01 S1 2026-05-27)
# Verifies Memory A discipline: opt-in only, V1 byte-clean when token is None.
# ---------------------------------------------------------------------------


class TestTypographyTokenRouting:
    """Verify the opt-in V2 routing in _generate_base_css.

    Re-baseline gate Q5 guarantee at S1: every built-in theme has
    typography_tokens=None by default → base CSS contains zero ADR-009
    markers and behaves byte-identically to S0 (pre-Pillar-B).
    """

    @pytest.mark.parametrize("theme_name", sorted(PRESENTATION_THEMES.keys()))
    def test_v1_path_emits_no_adr_009_marker(self, theme_name):
        """All 8 built-in themes default typography_tokens=None → V1 byte-clean."""
        from canvas_core.html_renderer import _generate_base_css

        theme = PRESENTATION_THEMES[theme_name]
        assert theme.typography_tokens is None, (
            f"{theme_name} built-in theme must default typography_tokens=None"
        )
        palette = THEME_PALETTES[theme_name]
        css = _generate_base_css(theme, palette)
        assert "/* Typography token overrides (ADR-009) */" not in css, (
            f"{theme_name} V1 path leaked ADR-009 marker"
        )

    def test_v2_opt_in_appends_marker_and_overrides(self):
        """Setting typography_tokens injects ADR-009 marker + opt-in CSS rules."""
        from dataclasses import replace

        from canvas_core.design_tokens import TYPOGRAPHY_TOKENS_PUBLICATION
        from canvas_core.html_renderer import (
            THEME_WILHELM_FOUNDATION,
            _generate_base_css,
        )

        v2_theme = replace(
            THEME_WILHELM_FOUNDATION, typography_tokens=TYPOGRAPHY_TOKENS_PUBLICATION
        )
        css = _generate_base_css(
            v2_theme, THEME_PALETTES["wilhelm_foundation"]
        )
        assert "/* Typography token overrides (ADR-009) */" in css
        assert "font-kerning: normal" in css
        assert "font-optical-sizing: auto" in css

    def test_v2_fragment_appended_last_so_cascade_overrides_v1_weights(self):
        """V2 fragment must follow the hardcoded h1 weight=700 rule so cascade wins."""
        from dataclasses import replace

        from canvas_core.html_renderer import (
            THEME_WILHELM_FOUNDATION,
            _generate_base_css,
        )
        from canvas_core.typography import TypographyToken

        v2_theme = replace(
            THEME_WILHELM_FOUNDATION,
            typography_tokens=TypographyToken(weight_h1=900),
        )
        css = _generate_base_css(
            v2_theme, THEME_PALETTES["wilhelm_foundation"]
        )
        v1_weight_idx = css.find("font-weight: 700;")  # hardcoded h1
        v2_weight_idx = css.find("h1 { font-weight: 900; }")
        assert v1_weight_idx > 0
        assert v2_weight_idx > 0
        assert v1_weight_idx < v2_weight_idx, (
            "V2 fragment must appear AFTER V1 hardcoded weights for cascade override"
        )

    def test_v1_css_length_unchanged_with_none_token_vs_baseline(self):
        """Wilhelm V1 CSS must be byte-stable across the typography_tokens=None call."""
        from canvas_core.html_renderer import (
            THEME_WILHELM_FOUNDATION,
            _generate_base_css,
        )

        # typography_tokens defaults to None on the built-in
        css_default = _generate_base_css(
            THEME_WILHELM_FOUNDATION, THEME_PALETTES["wilhelm_foundation"]
        )
        # Re-render with same explicit None — must produce identical string.
        from dataclasses import replace

        css_explicit_none = _generate_base_css(
            replace(THEME_WILHELM_FOUNDATION, typography_tokens=None),
            THEME_PALETTES["wilhelm_foundation"],
        )
        assert css_default == css_explicit_none
