"""HTML canvas renderer — converts canvas JSON into standalone HTML pages.

Each canvas group node becomes a self-contained HTML page with design-token
CSS, themed colors, and approximate markdown rendering.

This is the first half of the visual inspection pipeline:
  canvas JSON → HTML pages → Playwright screenshots → visual scoring

Migrated from lattice-protocol/extensions/canvas/canvas_html_renderer.py
(M-1-01 session 2). Full file kept in canvas_core/ per ADR 001 § Borderline
Files. Deck-specific slide-routing layer will be extracted to
canvas_presentation/presentation_renderer.py in Wave 2 (M-2a).

Theme/palette definitions are inlined here (not in config_substrate.py)
because ADR 001 § canvas_config Split classifies them as deck data.
They leave with the deck routing layer in Wave 2.
"""

from __future__ import annotations

import base64
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .design_tokens import (
    LETTER_SPACING,
    LINE_HEIGHTS,
    SPACING_TOKENS,
    TYPE_SIZES,
    export_css_custom_properties,
    get_slide_tokens,
)
from .geometry import _DEFAULT_VIEWPORT, resolve_viewport
from .typography import TypographyToken, to_css_fragment as _typography_css_fragment

# ---------------------------------------------------------------------------
# Theme & Palette definitions (inlined from canvas_config.py)
# ADR 001 classifies these as deck — they migrate to
# canvas_presentation/config_deck.py in Wave 2 (M-2a).
# ---------------------------------------------------------------------------


@dataclass
class PresentationTheme:
    """Visual theme for presentations."""

    name: str
    primary_color: str  # Obsidian canvas color (1-6 or hex)
    secondary_color: str
    accent_color: str
    background_style: str = "default"
    font_suggestion: str = ""
    logo_path: str | None = None

    # Theme-level typography token (ADR-009; opt-in; default None).
    # When None, V1 CSS path: font-family from `font_suggestion`, weights
    # hardcoded in `_generate_base_css`, monospace hardcoded at the
    # `code` selector. When set, `_generate_base_css` appends opt-in
    # overrides AFTER the V1 rules so the CSS cascade applies them.
    typography_tokens: TypographyToken | None = None


@dataclass
class ThemePalette:
    """Background, text, and border colors for HTML rendering."""

    bg: str
    bg_lighter: str
    text: str
    text_dim: str
    border: str


# Built-in themes
THEME_TOKYO_NIGHT = PresentationTheme(
    name="tokyo_night",
    primary_color="6",
    secondary_color="5",
    accent_color="4",
    font_suggestion="JetBrains Mono, Fira Code, Menlo, Consolas, monospace",
)

THEME_LATTICE_BRAND = PresentationTheme(
    name="lattice_brand",
    primary_color="6",  # Purple (Rebecca Purple)
    secondary_color="4",  # Green
    accent_color="1",  # Red accent
    font_suggestion="Space Grotesk, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif",
)

THEME_SCIENTIFIC = PresentationTheme(
    name="scientific",
    primary_color="5",  # Cyan/teal
    secondary_color="3",  # Green
    accent_color="2",  # Orange
    font_suggestion="Charter, Georgia, Cambria, Times New Roman, serif",
)

THEME_LATTICE_DARK = PresentationTheme(
    name="lattice_dark",
    primary_color="6",  # Purple
    secondary_color="4",  # Cyan
    accent_color="1",  # Red
    font_suggestion="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
)

THEME_LATTICE_LIGHT = PresentationTheme(
    name="lattice_light",
    primary_color="5",  # Green
    secondary_color="3",  # Amber
    accent_color="1",  # Red
    font_suggestion="Inter, -apple-system, BlinkMacSystemFont, sans-serif",
)

THEME_SCIENCE_STANLEY = PresentationTheme(
    name="science_stanley",
    primary_color="6",  # Purple
    secondary_color="5",  # Green
    accent_color="4",  # Cyan
    font_suggestion="JetBrains Mono, Fira Code, Menlo, monospace",
)

THEME_ACADEMIC = PresentationTheme(
    name="academic",
    primary_color="5",  # Green
    secondary_color="3",  # Amber
    accent_color="2",  # Orange
    font_suggestion="Charter, Georgia, Cambria, serif",
)

# Interim Wilhelm-Foundation-evocative palette pending brand-book confirmation.
# See how/skills/skill_per_customer_brand_theme.md § Brand-color sourcing discipline.
THEME_WILHELM_FOUNDATION = PresentationTheme(
    name="wilhelm_foundation",
    primary_color="5",  # green/teal — anchor (foundation/hope tone)
    secondary_color="2",  # warm accent — dedication tone
    accent_color="4",  # cyan — clinical/scientific tone
    font_suggestion="Charter, Georgia, Cambria, serif",
)

PRESENTATION_THEMES: dict[str, PresentationTheme] = {
    "tokyo_night": THEME_TOKYO_NIGHT,
    "lattice_brand": THEME_LATTICE_BRAND,
    "scientific": THEME_SCIENTIFIC,
    "lattice_dark": THEME_LATTICE_DARK,
    "lattice_light": THEME_LATTICE_LIGHT,
    "science_stanley": THEME_SCIENCE_STANLEY,
    "academic": THEME_ACADEMIC,
    "wilhelm_foundation": THEME_WILHELM_FOUNDATION,
}

THEME_PALETTES: dict[str, ThemePalette] = {
    "tokyo_night": ThemePalette(
        bg="#1a1b26",
        bg_lighter="#24283b",
        text="#c0caf5",
        text_dim="#6272a4",
        border="#3b4261",
    ),
    "lattice_dark": ThemePalette(
        bg="#1e1e2e",
        bg_lighter="#2a2a3e",
        text="#cdd6f4",
        text_dim="#6c7086",
        border="#45475a",
    ),
    "lattice_brand": ThemePalette(
        bg="#1a1b26",
        bg_lighter="#24283b",
        text="#c0caf5",
        text_dim="#6272a4",
        border="#3b4261",
    ),
    "science_stanley": ThemePalette(
        bg="#1a1b26",
        bg_lighter="#24283b",
        text="#c0caf5",
        text_dim="#6272a4",
        border="#3b4261",
    ),
    "lattice_light": ThemePalette(
        bg="#ffffff",
        bg_lighter="#f5f5f7",
        text="#1d1d1f",
        text_dim="#6e6e73",
        border="#d2d2d7",
    ),
    "scientific": ThemePalette(
        bg="#fafaf8",
        bg_lighter="#f0f0ec",
        text="#2c2c2c",
        text_dim="#6b6b6b",
        border="#d4d4cc",
    ),
    "academic": ThemePalette(
        bg="#fffef9",
        bg_lighter="#f8f6f0",
        text="#2d2926",
        text_dim="#7a7267",
        border="#d6cfc4",
    ),
    "wilhelm_foundation": ThemePalette(
        bg="#fffefb",  # off-white serif backdrop
        bg_lighter="#f7f3ec",  # warm parchment lift
        text="#1f2a2a",  # deep teal-anthracite
        text_dim="#5e6e6c",
        border="#cdc8bc",
    ),
}

DEFAULT_PALETTE = THEME_PALETTES["tokyo_night"]

# ---------------------------------------------------------------------------
# End inlined theme/palette definitions
# ---------------------------------------------------------------------------

# File extensions that should be embedded as <img> tags when the file is found.
_IMAGE_EXTS = frozenset({".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"})


def _resolve_asset(file_path: str, asset_root: Path | None) -> Path | None:
    """Resolve a canvas file= path against asset_root (or cwd) if it exists."""
    if not file_path:
        return None
    p = Path(file_path)
    if p.is_absolute() and p.exists():
        return p
    root = asset_root if asset_root is not None else Path.cwd()
    candidate = root / file_path
    if candidate.exists():
        return candidate
    return None


def _file_to_data_url(path: Path) -> str | None:
    """Encode an image file as a data: URL. Returns None on failure."""
    try:
        ext = path.suffix.lower()
        mime_map = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".svg": "image/svg+xml",
        }
        mime = mime_map.get(ext, "application/octet-stream")
        data = path.read_bytes()
        b64 = base64.b64encode(data).decode("ascii")
        return f"data:{mime};base64,{b64}"
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Theme registry
# ---------------------------------------------------------------------------

THEMES: dict[str, PresentationTheme] = PRESENTATION_THEMES

# Tokyo Night palette — maps canvas color slots to hex values
TOKYO_NIGHT_COLORS: dict[str, str] = {
    "1": "#f7768e",  # Red
    "2": "#ff9e64",  # Orange
    "3": "#e0af68",  # Amber
    "4": "#7dcfff",  # Cyan
    "5": "#9ece6a",  # Green
    "6": "#9d7cd8",  # Purple
}

TOKYO_NIGHT_BG = "#1a1b26"
TOKYO_NIGHT_BG_LIGHTER = "#24283b"
TOKYO_NIGHT_TEXT = "#c0caf5"
TOKYO_NIGHT_TEXT_DIM = "#565f89"
TOKYO_NIGHT_BORDER = "#3b4261"

_DARK_PALETTE = DEFAULT_PALETTE


def _get_palette(theme_name: str) -> ThemePalette:
    """Get the palette for a theme name, defaulting to dark."""
    return THEME_PALETTES.get(theme_name, _DARK_PALETTE)


# Lattice role → border/accent color
ROLE_COLORS: dict[str, str] = {
    "stage": "#9ece6a",  # Green
    "io": "#7dcfff",  # Cyan
    "decision": "#e0af68",  # Amber
    "critical": "#f7768e",  # Red
    "metadata": "#565f89",  # Gray
}


@dataclass
class SlideHTML:
    """A rendered slide as HTML."""

    index: int
    title: str
    slide_type: str
    html: str
    filename: str


@dataclass
class RenderedPresentation:
    """All slides rendered as HTML pages."""

    title: str
    slides: list[SlideHTML] = field(default_factory=list)
    theme_name: str = "tokyo_night"


# ---------------------------------------------------------------------------
# Canvas JSON → Slide Extraction
# ---------------------------------------------------------------------------


def extract_slides(canvas_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract slide groups and their contained nodes from canvas JSON.

    Returns a list of slide dicts, each with:
      - id, label, x, y, width, height, color
      - nodes: list of contained node dicts (text, file, link)
      - slide_type: inferred from cssclasses or content structure
    """
    nodes = canvas_data.get("nodes", [])

    # Separate groups from interior nodes
    groups: list[dict[str, Any]] = []
    interior: list[dict[str, Any]] = []
    for node in nodes:
        if node.get("type") == "group":
            groups.append(node)
        else:
            interior.append(node)

    # Sort groups by reading order (top-to-bottom, left-to-right)
    groups.sort(key=lambda g: (g.get("y", 0), g.get("x", 0)))

    # Find startNode for ordering
    metadata = canvas_data.get("metadata", {})
    start_id = metadata.get("startNode")

    # Build navigation order from edges
    edges = canvas_data.get("edges", [])
    edge_map: dict[str, str] = {}  # fromNode → toNode (group-level)
    group_ids = {g["id"] for g in groups}
    for edge in edges:
        fn = edge.get("fromNode", "")
        tn = edge.get("toNode", "")
        if fn in group_ids and tn in group_ids:
            edge_map[fn] = tn

    # Try to build ordered list from edge chain
    ordered: list[dict[str, Any]] = []
    if start_id and start_id in group_ids:
        visited: set[str] = set()
        current = start_id
        group_map = {g["id"]: g for g in groups}
        while current and current not in visited:
            visited.add(current)
            if current in group_map:
                ordered.append(group_map[current])
            current = edge_map.get(current)
        # Add any groups not in the chain
        for g in groups:
            if g["id"] not in visited:
                ordered.append(g)
    else:
        ordered = groups

    # Assign contained nodes to each group
    slides: list[dict[str, Any]] = []
    for i, group in enumerate(ordered):
        gx = group.get("x", 0)
        gy = group.get("y", 0)
        gw = group.get("width", 1200)
        gh = group.get("height", 1100)

        contained = []
        for node in interior:
            nx = node.get("x", 0)
            ny = node.get("y", 0)
            # Node is contained if its position is within the group bounds
            if gx <= nx <= gx + gw and gy <= ny <= gy + gh:
                contained.append(node)

        # Sort contained nodes top-to-bottom
        contained.sort(key=lambda n: (n.get("y", 0), n.get("x", 0)))

        # Infer slide type from cssclasses
        slide_type = _infer_slide_type(group, contained, i)

        slides.append(
            {
                "id": group.get("id", ""),
                "index": i,
                "label": group.get("label", f"Slide {i + 1}"),
                "x": gx,
                "y": gy,
                "width": gw,
                "height": gh,
                "color": group.get("color"),
                "nodes": contained,
                "slide_type": slide_type,
            }
        )

    return slides


def _infer_slide_type(
    group: dict[str, Any],
    nodes: list[dict[str, Any]],
    index: int,
) -> str:
    """Infer slide type from CSS classes and content structure."""
    for node in nodes:
        classes = node.get("styleAttributes", {}).get("cssclasses", "")
        if "cl-pres-stats" in classes:
            return "stats"
        if "cl-pres-comparison" in classes:
            return "comparison"
        if "cl-pres-process" in classes:
            return "process"
        if "cl-pres-kv" in classes:
            return "key_value"
        if "hero" in classes:
            return "title"

    # Check for pill shapes (stats)
    pill_count = sum(1 for n in nodes if n.get("styleAttributes", {}).get("shape") == "pill")
    if pill_count >= 2:
        return "stats"

    # First slide with few words is likely title
    if index == 0:
        total_words = sum(len(n.get("text", "").split()) for n in nodes)
        if total_words < 30:
            return "title"

    return "content"


# ---------------------------------------------------------------------------
# Markdown → HTML
# ---------------------------------------------------------------------------


def _convert_tables(text: str) -> str:
    """Convert markdown pipe tables to HTML table elements.

    Detects table blocks: header row | separator row | data rows.
    Replaces them in-place with HTML.
    """
    lines = text.split("\n")
    result: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Detect potential table: line with pipes, followed by separator
        if (
            "|" in line
            and i + 1 < len(lines)
            and re.match(r"^\|[\s:]*-+[\s:]*(\|[\s:]*-+[\s:]*)*\|?\s*$", lines[i + 1].strip())
        ):
            # Parse header
            header_cells = _parse_table_row(line)
            if header_cells:
                table_lines = ["<table>", "<thead>", "<tr>"]
                for cell in header_cells:
                    table_lines.append(f"<th>{_inline_md(cell)}</th>")
                table_lines.extend(["</tr>", "</thead>", "<tbody>"])

                # Skip separator row
                i += 2

                # Parse data rows
                while i < len(lines):
                    row_line = lines[i].strip()
                    if not row_line or "|" not in row_line:
                        break
                    cells = _parse_table_row(row_line)
                    if not cells:
                        break
                    table_lines.append("<tr>")
                    for cell in cells:
                        table_lines.append(f"<td>{_inline_md(cell)}</td>")
                    table_lines.append("</tr>")
                    i += 1

                table_lines.extend(["</tbody>", "</table>"])
                result.extend(table_lines)
                continue

        result.append(lines[i])
        i += 1

    return "\n".join(result)


def _parse_table_row(line: str) -> list[str]:
    """Parse a markdown table row into cell contents."""
    # Strip leading/trailing pipes and split
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    cells = [c.strip() for c in stripped.split("|")]
    return cells if cells and any(c for c in cells) else []


def _md_to_html(text: str) -> str:
    """Convert simple markdown to HTML.

    Handles: headings, bold, italic, bullets, numbered lists, code blocks,
    inline code, blockquotes, links, horizontal rules, and tables.
    """
    if not text:
        return ""

    # Pre-process: extract table blocks before line-by-line parsing
    text = _convert_tables(text)

    lines = text.split("\n")
    html_lines: list[str] = []
    in_code_block = False
    in_mermaid_block = False
    in_list = False
    in_ol = False

    for line in lines:
        stripped = line.strip()

        # Pass through pre-converted table HTML
        if stripped.startswith("<table") or stripped.startswith("</table"):
            _close_lists(html_lines, in_list, in_ol)
            in_list = False
            in_ol = False
            html_lines.append(line)
            continue
        if stripped.startswith(
            ("<thead", "</thead", "<tbody", "</tbody", "<tr", "</tr", "<th", "<td")
        ):
            html_lines.append(line)
            continue

        # Code blocks
        if stripped.startswith("```"):
            if in_code_block:
                if in_mermaid_block:
                    html_lines.append("</pre>")
                    in_mermaid_block = False
                else:
                    html_lines.append("</code></pre>")
                in_code_block = False
            else:
                lang = stripped[3:].strip()
                if lang == "mermaid":
                    # Mermaid blocks use <pre class="mermaid"> for CDN rendering
                    html_lines.append('<pre class="mermaid">')
                    in_mermaid_block = True
                else:
                    cls = f' class="language-{lang}"' if lang else ""
                    html_lines.append(f"<pre><code{cls}>")
                in_code_block = True
            continue

        if in_code_block:
            if in_mermaid_block:
                html_lines.append(line)  # Mermaid content raw (not escaped)
            else:
                html_lines.append(_escape_html(line))
            continue

        # Horizontal rule
        if stripped in ("---", "***", "___"):
            _close_lists(html_lines, in_list, in_ol)
            in_list = False
            in_ol = False
            html_lines.append("<hr>")
            continue

        # Empty line
        if not stripped:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            continue

        # Headings
        heading_match = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading_match:
            _close_lists(html_lines, in_list, in_ol)
            in_list = False
            in_ol = False
            level = len(heading_match.group(1))
            content = _inline_md(heading_match.group(2))
            html_lines.append(f"<h{level}>{content}</h{level}>")
            continue

        # Blockquote
        if stripped.startswith("> "):
            _close_lists(html_lines, in_list, in_ol)
            in_list = False
            in_ol = False
            content = _inline_md(stripped[2:])
            html_lines.append(f"<blockquote>{content}</blockquote>")
            continue

        # Unordered list
        list_match = re.match(r"^[-*]\s+(.+)$", stripped)
        if list_match:
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            content = _inline_md(list_match.group(1))
            html_lines.append(f"  <li>{content}</li>")
            continue

        # Ordered list
        ol_match = re.match(r"^(\d+)\.\s+(.+)$", stripped)
        if ol_match:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            content = _inline_md(ol_match.group(2))
            html_lines.append(f"  <li>{content}</li>")
            continue

        # Regular paragraph
        _close_lists(html_lines, in_list, in_ol)
        in_list = False
        in_ol = False
        html_lines.append(f"<p>{_inline_md(stripped)}</p>")

    _close_lists(html_lines, in_list, in_ol)
    if in_code_block:
        if in_mermaid_block:
            html_lines.append("</pre>")
        else:
            html_lines.append("</code></pre>")

    return "\n".join(html_lines)


def _close_lists(html_lines: list[str], in_list: bool, in_ol: bool) -> None:
    """Close any open list tags."""
    if in_list:
        html_lines.append("</ul>")
    if in_ol:
        html_lines.append("</ol>")


def _inline_md(text: str) -> str:
    """Convert inline markdown (bold, italic, code, links)."""
    # Inline code (before bold/italic to avoid conflicts)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Bold + italic
    text = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", text)
    # Bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # Italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Links
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def _escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (
        text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    )


# ---------------------------------------------------------------------------
# HTML Page Generation
# ---------------------------------------------------------------------------


def _color_slot_to_hex(
    color: str | None,
    palette: ThemePalette | None = None,
) -> str:
    """Convert canvas color slot (1-6) or hex string to hex color."""
    fallback = (palette or _DARK_PALETTE).bg_lighter
    if not color:
        return fallback
    if color.startswith("#"):
        return color
    return TOKYO_NIGHT_COLORS.get(color, fallback)


def _role_border_color(nodes: list[dict[str, Any]]) -> str | None:
    """Get the dominant latticeRole border color from slide nodes."""
    for node in nodes:
        role = node.get("styleAttributes", {}).get("latticeRole")
        if role and role in ROLE_COLORS:
            return ROLE_COLORS[role]
    return None


def _generate_base_css(
    theme: PresentationTheme,
    palette: ThemePalette | None = None,
    viewport_width: int = 1920,
    viewport_height: int = 1080,
) -> str:
    """Generate the base CSS for all slides using design tokens."""
    p = palette or _DARK_PALETTE
    primary_hex = _color_slot_to_hex(theme.primary_color, p)
    _color_slot_to_hex(theme.secondary_color, p)
    _color_slot_to_hex(theme.accent_color, p)
    font = theme.font_suggestion or "Inter, -apple-system, sans-serif"

    # CSS custom properties from design tokens + theme colors
    token_props = export_css_custom_properties()
    theme_props = (
        f"/* Theme colors */\n"
        f"--cl-bg: {p.bg};\n"
        f"--cl-bg-lighter: {p.bg_lighter};\n"
        f"--cl-text: {p.text};\n"
        f"--cl-text-dim: {p.text_dim};\n"
        f"--cl-border: {p.border};\n"
        f"--cl-primary: {primary_hex};\n"
    )

    base_css = f"""
    :root {{
        {token_props}
        {theme_props}
    }}

    * {{ margin: 0; padding: 0; box-sizing: border-box; }}

    body {{
        background: {p.bg};
        color: {p.text};
        font-family: {font};
        font-size: {TYPE_SIZES["body"]}px;
        line-height: {LINE_HEIGHTS["body"]};
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    .slide-viewport {{
        width: {viewport_width}px;
        height: {viewport_height}px;
        position: relative;
        overflow: hidden;
        background: {p.bg};
        border: 1px solid {p.border};
    }}

    .slide-group {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 8px;
        overflow: hidden;
    }}

    /* Flow layout: vertical stack with auto-sizing */
    .slide-group.flow-layout {{
        display: flex;
        flex-direction: column;
        padding: {SPACING_TOKENS["2xl"]}px {SPACING_TOKENS["3xl"]}px;
        gap: {SPACING_TOKENS["lg"]}px;
        justify-content: center;
    }}

    /* Top-align for content-heavy slides */
    .slide-group.flow-layout.flow-top {{
        justify-content: flex-start;
    }}

    .slide-group.has-color {{
        border-left: 4px solid var(--slide-color);
    }}

    /* Absolute positioning for canvas-faithful mode */
    .slide-node {{
        position: absolute;
        padding: {SPACING_TOKENS["lg"]}px {SPACING_TOKENS["xl"]}px;
        border-radius: 6px;
        overflow: hidden;
    }}

    /* Flow-mode nodes: no absolute positioning, auto height */
    .slide-group.flow-layout .slide-node {{
        position: relative;
        width: 100% !important;
        height: auto !important;
        left: auto !important;
        top: auto !important;
    }}

    .slide-node.text-node {{
        background: {p.bg_lighter};
    }}

    .slide-node.text-node.no-bg {{
        background: transparent;
    }}

    /* Heading node: transparent background in flow layout */
    .slide-group.flow-layout > .slide-node.heading-node {{
        background: transparent;
        padding-bottom: 0;
        border-top: none;
        border-left: none;
    }}

    /* Subtitle node: transparent bg, dimmed, smaller text */
    .slide-group.flow-layout > .slide-node.subtitle-node {{
        background: transparent;
        border-top: none;
        border-left: none;
        padding-top: 0;
    }}
    .slide-group.flow-layout > .slide-node.subtitle-node p {{
        font-size: {TYPE_SIZES["h3"]}px;
        color: {p.text_dim};
    }}

    /* Horizontal row container for side-by-side nodes */
    .flow-row {{
        display: flex;
        gap: {SPACING_TOKENS["lg"]}px;
        width: 100%;
        position: relative;
    }}

    .flow-row .slide-node {{
        flex: 1;
        min-width: 0;
    }}

    /* Shape: pill */
    .slide-node.shape-pill {{
        border-radius: 50px;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: {SPACING_TOKENS["md"]}px;
        background: {p.bg_lighter};
    }}

    /* Shape: diamond */
    .slide-node.shape-diamond {{
        clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);
    }}

    /* Border styles */
    .slide-node.border-dashed {{
        border: 2px dashed {p.border};
    }}

    .slide-node.border-dotted {{
        border: 2px dotted {p.border};
    }}

    .slide-node.border-invisible {{
        border: none;
        background: transparent;
    }}

    /* Lattice roles */
    .slide-node.role-stage {{
        border-left: 3px solid {ROLE_COLORS["stage"]};
    }}

    .slide-node.role-io {{
        border-left: 3px solid {ROLE_COLORS["io"]};
    }}

    .slide-node.role-decision {{
        border-left: 3px solid {ROLE_COLORS["decision"]};
    }}

    .slide-node.role-critical {{
        border-left: 3px solid {ROLE_COLORS["critical"]};
    }}

    .slide-node.role-metadata {{
        border-left: 3px solid {ROLE_COLORS["metadata"]};
    }}

    /* Content overflow protection */
    .slide-node .overflow-ellipsis {{
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .slide-group.flow-layout .slide-node {{
        overflow: hidden;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }}

    /* Node color tint */
    .slide-node.has-node-color {{
        background: color-mix(in srgb, var(--node-color) 15%, {p.bg_lighter});
    }}

    /* Text alignment */
    .slide-node.align-center {{ text-align: center; }}
    .slide-node.align-right {{ text-align: right; }}

    /* Typography */
    h1 {{
        font-size: {TYPE_SIZES["h1"]}px;
        line-height: {LINE_HEIGHTS["h1"]};
        letter-spacing: {LETTER_SPACING["h1"]}em;
        font-weight: 700;
        color: {p.text};
        margin-bottom: {SPACING_TOKENS["lg"]}px;
    }}

    h2 {{
        font-size: {TYPE_SIZES["h2"]}px;
        line-height: {LINE_HEIGHTS["h2"]};
        letter-spacing: {LETTER_SPACING["h2"]}em;
        font-weight: 600;
        color: {p.text};
        margin-bottom: {SPACING_TOKENS["md"]}px;
    }}

    h3 {{
        font-size: {TYPE_SIZES["h3"]}px;
        line-height: {LINE_HEIGHTS["h3"]};
        letter-spacing: {LETTER_SPACING["h3"]}em;
        font-weight: 600;
        color: {p.text};
        margin-bottom: {SPACING_TOKENS["sm"]}px;
    }}

    h4 {{
        font-size: {TYPE_SIZES["h4"]}px;
        line-height: {LINE_HEIGHTS["h4"]};
        font-weight: 600;
        margin-bottom: {SPACING_TOKENS["xs"]}px;
    }}

    p {{
        margin-bottom: {SPACING_TOKENS["sm"]}px;
    }}

    ul, ol {{
        margin-left: {SPACING_TOKENS["xl"]}px;
        margin-bottom: {SPACING_TOKENS["sm"]}px;
    }}

    li {{
        margin-bottom: {SPACING_TOKENS["xs"]}px;
    }}

    pre {{
        background: {p.bg};
        border: 1px solid {p.border};
        border-radius: 4px;
        padding: {SPACING_TOKENS["md"]}px;
        margin-bottom: {SPACING_TOKENS["md"]}px;
        overflow-x: auto;
    }}

    code {{
        font-family: JetBrains Mono, Fira Code, monospace;
        font-size: 0.9em;
    }}

    :not(pre) > code {{
        background: {p.bg};
        padding: 2px 6px;
        border-radius: 3px;
    }}

    blockquote {{
        border-left: 3px solid {primary_hex};
        padding-left: {SPACING_TOKENS["lg"]}px;
        margin-bottom: {SPACING_TOKENS["md"]}px;
        color: {p.text_dim};
        font-style: italic;
    }}

    strong {{
        font-weight: 700;
        color: {p.text};
    }}

    em {{
        font-style: italic;
    }}

    hr {{
        border: none;
        border-top: 1px solid {p.border};
        margin: {SPACING_TOKENS["lg"]}px 0;
    }}

    a {{
        color: {primary_hex};
        text-decoration: none;
    }}

    /* Hero text styling */
    .hero h1 {{
        font-size: {TYPE_SIZES["display"]}px;
        line-height: {LINE_HEIGHTS["display"]};
        letter-spacing: {LETTER_SPACING["display"]}em;
        color: {primary_hex};
    }}

    .hero p {{
        font-size: {TYPE_SIZES["h3"]}px;
        color: {p.text_dim};
    }}

    /* Markdown table styling */
    table {{
        border-collapse: collapse;
        width: 100%;
        margin-bottom: {SPACING_TOKENS["md"]}px;
    }}

    th, td {{
        border: 1px solid {p.border};
        padding: {SPACING_TOKENS["xs"]}px {SPACING_TOKENS["sm"]}px;
        text-align: left;
    }}

    th {{
        background: {p.bg_lighter};
        font-weight: 600;
    }}

    tr:nth-child(even) td {{
        background: color-mix(in srgb, {p.bg_lighter} 50%, {p.bg});
    }}
    """

    # Light theme enhancements: better code block contrast, visible borders
    is_light = int(p.bg[1:3], 16) > 200
    if is_light:
        base_css += f"""
    /* Light theme: enhanced code block contrast */
    pre {{
        background: {p.bg_lighter};
        border: 1px solid {p.border};
    }}
    :not(pre) > code {{
        background: {p.bg_lighter};
        border: 1px solid {p.border};
    }}

    /* Light theme: stronger heading contrast */
    h1 {{
        color: {p.text};
    }}
    .hero h1 {{
        color: {p.text};
        border-bottom: 3px solid {primary_hex};
        display: inline-block;
        padding-bottom: {SPACING_TOKENS["xs"]}px;
    }}

    /* Light theme: subtitle bump to h2 size for readability */
    .slide-group.flow-layout > .slide-node.subtitle-node p {{
        font-size: {TYPE_SIZES["h2"]}px;
    }}

    /* Light theme: bold text uses primary for visual interest */
    strong {{
        color: {p.text};
    }}

    /* Light theme: card borders for visibility */
    .slide-node.text-node {{
        border: 1px solid {p.border};
    }}
    .slide-group.flow-layout > .slide-node.heading-node {{
        border: none;
    }}
    .slide-group.flow-layout > .slide-node.subtitle-node {{
        border: none;
    }}
    """

    # Print stylesheet
    base_css += """
    @media print {
        .slide-viewport {
            border: none;
            box-shadow: none;
            page-break-after: always;
        }
        body {
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }
        script, .mermaid-script { display: none; }
    }
    """

    # Typography token overrides (ADR-009; M-V1-2-B-01 S1; opt-in / V2 path).
    # Appended LAST so the cascade applies overrides over hardcoded V1 weights
    # / monospace family. Returns "" when theme.typography_tokens is None →
    # V1 CSS output byte-identical to S0 for every existing theme.
    base_css += _typography_css_fragment(theme.typography_tokens)

    return base_css


def _generate_type_css(
    theme: PresentationTheme,
    palette: ThemePalette | None = None,
) -> str:
    """Generate per-slide-type CSS rules.

    Replicates the visual treatments from canvas_system.css for each
    slide type, with per-type margin profiles from design tokens.
    """
    p = palette or _DARK_PALETTE
    primary_hex = _color_slot_to_hex(theme.primary_color, p)
    accent_hex = _color_slot_to_hex(theme.accent_color, p)

    # Build per-type margin overrides from design tokens
    type_margins: dict[str, str] = {}
    for stype in (
        "title",
        "content",
        "comparison",
        "quote",
        "stats",
        "section_divider",
        "diagram",
        "image",
        "timeline",
        "process",
        "three_column",
        "key_value",
        "matrix",
        "collage",
    ):
        tokens = get_slide_tokens(stype)
        type_margins[stype] = (
            f"padding: {tokens.margin_top}px {tokens.margin_side}px {tokens.margin_bottom}px;"
        )

    return f"""
    /* --- Per-slide-type CSS treatments --- */

    /* Title / Section Divider: centered, display-size heading */
    .slide-type-title.flow-layout {{
        {type_margins["title"]}
        text-align: center;
    }}
    .slide-type-title h1 {{
        font-size: {TYPE_SIZES["display"]}px;
        line-height: {LINE_HEIGHTS["display"]};
        letter-spacing: {LETTER_SPACING["display"]}em;
    }}

    .slide-type-section_divider.flow-layout {{
        {type_margins["section_divider"]}
        text-align: center;
    }}
    .slide-type-section_divider h1,
    .slide-type-section_divider h2 {{
        font-size: {TYPE_SIZES["display"]}px;
        line-height: {LINE_HEIGHTS["display"]};
    }}

    /* Content: standard margins, readable line length */
    .slide-type-content.flow-layout {{
        {type_margins["content"]}
    }}
    .slide-type-content .slide-node.text-node {{
        max-width: 960px;
    }}
    /* Content-heavy slides: improved typography for readability */
    .slide-type-content.flow-top .slide-node.text-node p {{
        font-size: {TYPE_SIZES["h4"]}px;
        line-height: {LINE_HEIGHTS["h4"]};
    }}
    .slide-type-content .slide-node.text-node strong {{
        color: {primary_hex};
    }}
    /* Content: accent border-top for visual interest */
    .slide-type-content.flow-top .slide-node.text-node:not(.heading-node) {{
        border-top: 2px solid {primary_hex};
        padding-top: {SPACING_TOKENS["lg"]}px;
    }}

    /* Quote: left accent border, italic, centered text */
    .slide-type-quote.flow-layout {{
        {type_margins["quote"]}
    }}
    .slide-type-quote .slide-node.text-node {{
        border-left: 4px solid {primary_hex};
        font-style: italic;
        font-size: {TYPE_SIZES["h3"]}px;
        line-height: {LINE_HEIGHTS["h3"]};
        text-align: center;
        background: transparent;
    }}

    /* Stats: pill shapes centered, bold large numbers, accent tint */
    .slide-type-stats.flow-layout {{
        {type_margins["stats"]}
    }}
    .slide-type-stats .slide-node.shape-pill {{
        background: color-mix(in srgb, {primary_hex} 10%, {p.bg_lighter});
        min-height: 120px;
        padding: {SPACING_TOKENS["lg"]}px {SPACING_TOKENS["xl"]}px;
    }}
    .slide-type-stats .slide-node.shape-pill h1 {{
        font-size: {TYPE_SIZES["display"]}px;
        color: {primary_hex};
    }}
    .slide-type-stats .flow-row {{
        justify-content: center;
    }}

    /* Comparison: centered h2 with bottom border, equal column widths */
    .slide-type-comparison.flow-layout {{
        {type_margins["comparison"]}
    }}
    .slide-type-comparison h2 {{
        text-align: center;
        padding-bottom: {SPACING_TOKENS["sm"]}px;
        border-bottom: 2px solid {p.border};
        margin-bottom: {SPACING_TOKENS["lg"]}px;
    }}
    .slide-type-comparison .flow-row .slide-node {{
        flex: 1;
        border-right: 1px solid {p.border};
    }}
    .slide-type-comparison .flow-row .slide-node:last-child {{
        border-right: none;
    }}

    /* Timeline: left accent line with marker dots */
    .slide-type-timeline.flow-layout {{
        {type_margins["timeline"]}
        border-left: 3px solid {primary_hex};
        margin-left: {SPACING_TOKENS["xl"]}px;
        padding-left: {SPACING_TOKENS["2xl"]}px;
    }}
    .slide-type-timeline .slide-node.text-node {{
        position: relative;
        background: transparent;
    }}
    .slide-type-timeline .slide-node.text-node::before {{
        content: '';
        position: absolute;
        left: -{SPACING_TOKENS["2xl"] + 6}px;
        top: {SPACING_TOKENS["md"]}px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: {primary_hex};
    }}

    /* Process: top border accent, step indicators */
    .slide-type-process.flow-layout {{
        {type_margins["process"]}
    }}
    .slide-type-process .slide-node.text-node {{
        border-top: 3px solid {accent_hex};
    }}
    /* Prevent solo process step from spanning full width */
    .slide-type-process .flow-row:last-child .slide-node:only-child {{
        max-width: 50%;
        margin: 0 auto;
    }}

    /* Three-column: separator borders between columns */
    .slide-type-three_column.flow-layout {{
        {type_margins["three_column"]}
    }}
    .slide-type-three_column .flow-row .slide-node {{
        border-right: 1px solid {p.border};
    }}
    .slide-type-three_column .flow-row .slide-node:last-child {{
        border-right: none;
    }}

    /* Key-Value: uppercase label, larger value */
    .slide-type-key_value.flow-layout {{
        {type_margins["key_value"]}
    }}
    .slide-type-key_value .slide-node.text-node p:first-child {{
        text-transform: uppercase;
        font-size: {TYPE_SIZES["caption"]}px;
        letter-spacing: {LETTER_SPACING["label"]}em;
        color: {p.text_dim};
    }}

    /* Diagram / Image: centered content, full-width */
    .slide-type-diagram.flow-layout {{
        {type_margins["diagram"]}
        align-items: center;
    }}
    .slide-type-image.flow-layout {{
        {type_margins["image"]}
        align-items: center;
    }}

    /* Matrix: cell borders, consistent padding */
    .slide-type-matrix.flow-layout {{
        {type_margins["matrix"]}
    }}
    .slide-type-matrix .slide-node.text-node {{
        border: 1px solid {p.border};
        border-radius: 0;
    }}

    /* Collage: tighter spacing */
    .slide-type-collage.flow-layout {{
        {type_margins["collage"]}
        gap: {SPACING_TOKENS["sm"]}px;
    }}
    .slide-type-collage .flow-row {{
        gap: {SPACING_TOKENS["sm"]}px;
    }}
    """


def render_slide_html(
    slide: dict[str, Any],
    theme: PresentationTheme,
    viewport_width: int | None = None,
    viewport_height: int | None = None,
    *,
    flow_layout: bool = True,
    theme_name: str = "tokyo_night",
    asset_root: Path | None = None,
) -> str:
    """Render a single slide as a standalone HTML page.

    Args:
        slide: Slide dict from extract_slides().
        theme: Presentation theme.
        viewport_width: HTML viewport width (px). If None, derived from
            the slide's canvas-group dimensions via resolve_viewport().
        viewport_height: HTML viewport height (px). If None, derived from
            the slide's canvas-group dimensions via resolve_viewport().
        flow_layout: Use CSS flow layout (auto-height nodes) instead of
            canvas-faithful absolute positioning. Default True for better
            visual quality.
        theme_name: Theme name for palette lookup.

    Returns:
        Complete HTML page string.
    """
    # M-1-06: derive viewport from canvas-group dimensions when not explicit
    if viewport_width is None or viewport_height is None:
        resolved_w, resolved_h = resolve_viewport(slide)
        viewport_width = viewport_width or resolved_w
        viewport_height = viewport_height or resolved_h

    palette = _get_palette(theme_name)
    slide_color = _color_slot_to_hex(slide.get("color"), palette)
    role_color = _role_border_color(slide.get("nodes", []))
    title = _escape_html(slide.get("label", "Untitled"))
    stype = slide.get("slide_type", "content")

    # Scale factor: canvas coords → viewport coords
    canvas_w = slide.get("width") or viewport_width
    canvas_h = slide.get("height") or viewport_height
    scale_x = viewport_width / canvas_w
    scale_y = viewport_height / canvas_h

    # Base offsets (slide group origin in canvas space)
    gx = slide.get("x", 0)
    gy = slide.get("y", 0)

    # Build node HTML
    nodes = slide.get("nodes", [])
    if flow_layout and nodes:
        nodes_html = _render_flow_nodes(
            nodes,
            gx,
            gy,
            scale_x,
            scale_y,
            palette=palette,
            slide_type=stype,
            asset_root=asset_root,
        )
    else:
        node_html_parts: list[str] = []
        for node in nodes:
            node_html_parts.append(
                _render_node(
                    node,
                    gx,
                    gy,
                    scale_x,
                    scale_y,
                    palette=palette,
                    asset_root=asset_root,
                )
            )
        nodes_html = "\n".join(node_html_parts)

    css = _generate_base_css(theme, palette, viewport_width, viewport_height)
    type_css = _generate_type_css(theme, palette)

    color_style = ""
    color_class = ""
    if slide.get("color"):
        color_style = f"--slide-color: {slide_color};"
        color_class = " has-color"

    # Add slide-type class
    color_class += f" slide-type-{stype}"

    if flow_layout:
        color_class += " flow-layout"
        # Content-heavy slides align top; others center vertically
        total_words = sum(len(n.get("text", "").split()) for n in nodes)
        if total_words > 80 or stype in ("diagram", "matrix", "collage"):
            color_class += " flow-top"

    border_style = ""
    if role_color:
        border_style = f"border-left: 4px solid {role_color};"

    # Detect Mermaid content for CDN inclusion
    has_mermaid = any("```mermaid" in n.get("text", "") for n in nodes)
    mermaid_script = ""
    if has_mermaid:
        # Determine mermaid theme based on palette brightness
        mermaid_theme = "dark" if int(palette.bg[1:3], 16) < 128 else "default"
        mermaid_script = (
            '\n<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>'
            f'\n<script>mermaid.initialize({{startOnLoad:true, theme:"{mermaid_theme}"}});</script>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width={viewport_width}">
<meta name="generator" content="Lattice Canvas HTML Renderer">
<meta name="theme" content="{theme_name}">
<meta name="slide-type" content="{stype}">
<title>{title}</title>
<style>{css}\n{type_css}</style>{mermaid_script}
</head>
<body>
<div class="slide-viewport" style="width:{viewport_width}px;height:{viewport_height}px;">
  <div class="slide-group{color_class}" style="{color_style}{border_style}">
    {nodes_html}
  </div>
</div>
</body>
</html>"""


def _render_node(
    node: dict[str, Any],
    group_x: int,
    group_y: int,
    scale_x: float,
    scale_y: float,
    *,
    palette: ThemePalette | None = None,
    asset_root: Path | None = None,
) -> str:
    """Render a single interior node as positioned HTML."""
    p = palette or _DARK_PALETTE
    node_type = node.get("type", "text")
    style_attrs = node.get("styleAttributes", {})

    # Position relative to group, scaled to viewport
    nx = (node.get("x", 0) - group_x) * scale_x
    ny = (node.get("y", 0) - group_y) * scale_y
    nw = node.get("width", 400) * scale_x
    nh = node.get("height", 200) * scale_y

    # CSS classes
    classes = ["slide-node"]
    if node_type == "text":
        classes.append("text-node")

    # Shape
    shape = style_attrs.get("shape")
    if shape:
        classes.append(f"shape-{shape}")

    # Border
    border = style_attrs.get("border")
    if border:
        classes.append(f"border-{border}")

    # Lattice role
    role = style_attrs.get("latticeRole")
    if role:
        classes.append(f"role-{role}")

    # Text alignment
    align = style_attrs.get("textAlign")
    if align:
        classes.append(f"align-{align}")

    # CSS classes from canvas
    cssclasses = style_attrs.get("cssclasses", "")
    if cssclasses:
        for cls in cssclasses.split():
            classes.append(cls)

    # Node color
    node_color = node.get("color")
    color_style = ""
    if node_color:
        classes.append("has-node-color")
        color_style = f"--node-color: {_color_slot_to_hex(node_color, p)};"

    class_str = " ".join(classes)
    style = f"left:{nx:.1f}px;top:{ny:.1f}px;width:{nw:.1f}px;height:{nh:.1f}px;{color_style}"

    # Content
    if node_type == "text":
        text = node.get("text", "")
        content = _md_to_html(text)
    elif node_type == "file":
        file_path = node.get("file", "")
        fname = Path(file_path).name if file_path else "image"
        content = ""
        # Try to embed as a real image if the file exists and has an image extension.
        ext = Path(file_path).suffix.lower() if file_path else ""
        if ext in _IMAGE_EXTS:
            resolved = _resolve_asset(file_path, asset_root)
            if resolved is not None:
                data_url = _file_to_data_url(resolved)
                if data_url:
                    alt = node.get("alt", fname)
                    content = (
                        f'<img src="{data_url}" alt="{_escape_html(alt)}" '
                        f'style="display:block;width:100%;height:100%;object-fit:cover;'
                        f'border-radius:8px;" />'
                    )
        # Fall back to italic placeholder if file is missing, unsupported, or read fails.
        if not content:
            content = (
                f'<div class="image-placeholder" style="display:flex;align-items:center;'
                f"justify-content:center;height:100%;color:{p.text_dim};"
                f"border:2px dashed {p.border};border-radius:8px;"
                f'background:color-mix(in srgb, {p.bg_lighter} 50%, {p.bg});">'
                f'<span style="font-style:italic;opacity:0.7;">'
                f"[Image: {_escape_html(fname)}]</span></div>"
            )
    elif node_type == "link":
        url = node.get("url", "")
        content = (
            f'<div style="display:flex;align-items:center;justify-content:center;'
            f'height:100%;color:{p.text_dim};font-style:italic;">'
            f"[Embed: {_escape_html(url[:60])}]</div>"
        )
    else:
        content = ""

    return f'<div class="{class_str}" style="{style}">{content}</div>'


def _render_flow_nodes(
    nodes: list[dict[str, Any]],
    group_x: int,
    group_y: int,
    scale_x: float,
    scale_y: float,
    *,
    palette: ThemePalette | None = None,
    slide_type: str = "content",
    asset_root: Path | None = None,
) -> str:
    """Render nodes using flow layout, grouping same-y nodes into rows.

    Nodes at similar y-positions (within 50px tolerance) are placed in
    a flex-row container for side-by-side rendering. Other nodes flow
    vertically.
    """
    if not nodes:
        return ""

    # Group nodes by approximate y-position (50px tolerance)
    y_groups: list[list[dict[str, Any]]] = []
    current_group: list[dict[str, Any]] = []
    last_y: float | None = None

    for node in nodes:
        ny = node.get("y", 0)
        if last_y is not None and abs(ny - last_y) > 50:
            if current_group:
                y_groups.append(current_group)
            current_group = [node]
        else:
            current_group.append(node)
        last_y = ny

    if current_group:
        y_groups.append(current_group)

    # Render each group
    html_parts: list[str] = []
    is_first = True
    heading_found = False
    for group in y_groups:
        if len(group) == 1:
            # Single node — render directly
            node_html = _render_node(
                group[0],
                group_x,
                group_y,
                scale_x,
                scale_y,
                palette=palette,
                asset_root=asset_root,
            )
            # Mark first single node as heading if it contains a heading
            if is_first:
                text = group[0].get("text", "")
                has_heading = any(
                    line.strip().startswith("#") for line in text.split("\n") if line.strip()
                )
                if has_heading:
                    node_html = node_html.replace(
                        'class="slide-node text-node',
                        'class="slide-node text-node heading-node',
                        1,
                    )
                    heading_found = True
            # Subtitle: second single node in title slides after heading
            elif (
                heading_found
                and not getattr(group[0], "_subtitle_checked", False)
                and slide_type == "title"
            ):
                node_html = node_html.replace(
                    'class="slide-node text-node',
                    'class="slide-node text-node subtitle-node',
                    1,
                )
                heading_found = False  # Only first subtitle
            html_parts.append(node_html)
        else:
            # Multiple nodes at same y — wrap in flex row
            row_parts = [
                _render_node(
                    n,
                    group_x,
                    group_y,
                    scale_x,
                    scale_y,
                    palette=palette,
                    asset_root=asset_root,
                )
                for n in group
            ]
            html_parts.append(f'<div class="flow-row">{"".join(row_parts)}</div>')
        is_first = False

    return "\n".join(html_parts)


# ---------------------------------------------------------------------------
# Full Presentation Rendering
# ---------------------------------------------------------------------------


def render_presentation(
    canvas_path: str | Path,
    output_dir: str | Path,
    *,
    theme_name: str | None = None,
    viewport_width: int | None = None,
    viewport_height: int | None = None,
    asset_root: str | Path | None = None,
) -> RenderedPresentation:
    """Render all slides from a canvas file as HTML pages.

    Args:
        canvas_path: Path to .canvas JSON file.
        output_dir: Directory to write HTML files into.
        theme_name: Override theme (default: read from canvas metadata).
        viewport_width: HTML viewport width. If None, derived per-slide
            from canvas-group dimensions via resolve_viewport().
        viewport_height: HTML viewport height. If None, derived per-slide.

    Returns:
        RenderedPresentation with all slide HTML files.
    """
    canvas_path = Path(canvas_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Asset root defaults to current working directory so vault-relative file=
    # paths in canvas nodes resolve when the renderer is invoked from the
    # vault root (the conventional pattern in lattice-labs scripts).
    asset_root_path: Path | None = (
        Path(asset_root) if asset_root is not None else Path.cwd()
    )

    with open(canvas_path) as f:
        canvas_data = json.load(f)

    # Determine theme
    if theme_name is None:
        meta = canvas_data.get("metadata", {})
        reserved = meta.get("frontmatter", {}).get("_reserved", {})
        theme_name = reserved.get("theme", "tokyo_night")

    theme = THEMES.get(theme_name, THEME_TOKYO_NIGHT)

    # Extract and render slides
    slides = extract_slides(canvas_data)

    result = RenderedPresentation(
        title=canvas_path.stem,
        theme_name=theme_name,
    )

    for slide in slides:
        idx = slide["index"]
        label = slide["label"]
        stype = slide["slide_type"]

        html = render_slide_html(
            slide,
            theme,
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            theme_name=theme_name,
            asset_root=asset_root_path,
        )

        # Sanitize filename
        safe_label = re.sub(r"[^\w\s-]", "", label).strip().replace(" ", "_")
        safe_label = safe_label[:50].lower()
        filename = f"slide_{idx + 1:02d}_{safe_label}.html"

        filepath = output_dir / filename
        filepath.write_text(html, encoding="utf-8")

        result.slides.append(
            SlideHTML(
                index=idx,
                title=label,
                slide_type=stype,
                html=html,
                filename=filename,
            )
        )

    return result


def render_canvas_data(
    canvas_data: dict[str, Any],
    *,
    theme_name: str = "tokyo_night",
    viewport_width: int | None = None,
    viewport_height: int | None = None,
    asset_root: str | Path | None = None,
) -> list[SlideHTML]:
    """Render slides from in-memory canvas data (no file I/O).

    Useful for testing and pipeline integration.

    Args:
        canvas_data: Parsed canvas JSON dict.
        theme_name: Theme name.
        viewport_width: HTML viewport width. If None, derived per-slide.
        viewport_height: HTML viewport height. If None, derived per-slide.

    Returns:
        List of SlideHTML objects.
    """
    theme = THEMES.get(theme_name, THEME_TOKYO_NIGHT)
    slides = extract_slides(canvas_data)
    results: list[SlideHTML] = []
    asset_root_path: Path | None = (
        Path(asset_root) if asset_root is not None else Path.cwd()
    )

    for slide in slides:
        idx = slide["index"]
        html = render_slide_html(
            slide,
            theme,
            viewport_width=viewport_width,
            viewport_height=viewport_height,
            theme_name=theme_name,
            asset_root=asset_root_path,
        )
        safe_label = re.sub(r"[^\w\s-]", "", slide["label"]).strip().replace(" ", "_")
        safe_label = safe_label[:50].lower()

        results.append(
            SlideHTML(
                index=idx,
                title=slide["label"],
                slide_type=slide["slide_type"],
                html=html,
                filename=f"slide_{idx + 1:02d}_{safe_label}.html",
            )
        )

    return results
