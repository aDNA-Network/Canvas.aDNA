"""PresentationBuilder — slide-deck generator wrapping CanvasBuilder.

Generates Obsidian canvas presentations where each slide is a group node
with contained text/file nodes. Supports startNode navigation, markdown
parsing, theme auto-application, and pending image lifecycle.

Migrated from lattice-protocol/extensions/canvas/canvas_presentation.py.
Scoring mixin (PresentationScoringMixin) deferred to M-2a-03.

Populated in M-2a-01 (Phase 2a — Deck Application Extraction).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from canvas_core import (
    CanvasBuilder,
    PendingImage,
    PresentationReport,
    containment_check,
    detect_overlaps,
    structural_summary,
)

from .config_deck import (
    _AUDIENCE_CONTEXTS,
    _DENSITY_MULTIPLIERS,
    _WORDS_BY_TYPE,
    MAX_WORDS_PER_NODE,
    NARRATIVE_ARCS,
    PRESENTATION_THEMES,
    AudienceContext,
    NarrativeArc,
    PresentationTheme,
)
from .layout import (
    LAYOUT_GRID_2COL,
    LAYOUT_PRESETS,
    LayoutStrategy,
    auto_select_layout,
    slide_layout_for_strategy,
)
from .scoring import PresentationScoringMixin
from .slide_builders import SlideBuilderMixin


class PresentationBuilder(SlideBuilderMixin, PresentationScoringMixin):
    """Build slide-deck presentations via CanvasBuilder composition.

    Each slide is a canvas group containing text/file nodes.
    Navigation edges connect slides in reading order.
    24-criterion scoring via PresentationScoringMixin (M-2a-03).
    """

    def __init__(
        self,
        name: str = "untitled",
        version: str = "1.0.0",
        presentation_type: str = "technical",
        max_words: int | None = None,
        layout: str | LayoutStrategy | None = None,
        density_profile: str = "balanced",
        arc: str | NarrativeArc | None = None,
        theme: str | PresentationTheme | None = None,
        audience: str | AudienceContext | None = None,
    ):
        self._cb = CanvasBuilder(name, version)
        self._slides: list[dict[str, Any]] = []
        self._pending_images: dict[str, PendingImage] = {}
        self._review_history: list[PresentationReport] = []
        self._accessibility_warnings: list[str] = []
        self.presentation_type = presentation_type
        self._max_words = max_words

        # Audience context
        self._audience: AudienceContext | None = None
        if audience is not None:
            if isinstance(audience, str):
                if audience not in _AUDIENCE_CONTEXTS:
                    raise ValueError(f"Unknown audience {audience!r}. Available: {sorted(_AUDIENCE_CONTEXTS)}")
                self._audience = _AUDIENCE_CONTEXTS[audience]
            else:
                self._audience = audience
            if density_profile == "balanced":
                density_profile = self._audience.density_profile
            if layout is None:
                layout = self._audience.preferred_layout

        self._density_profile = density_profile
        self._density_multiplier = _DENSITY_MULTIPLIERS.get(density_profile, 1.0)

        # Layout engine
        self._auto_layout = False
        if layout is None:
            self._layout = LAYOUT_GRID_2COL
        elif isinstance(layout, str) and layout == "auto":
            self._auto_layout = True
            self._layout = auto_select_layout(0, density_profile)
        elif isinstance(layout, str):
            self._layout = LAYOUT_PRESETS[layout]
        else:
            self._layout = layout
        self._slide_layout = slide_layout_for_strategy(self._layout)

        # Narrative arc
        if arc is None:
            self._arc: NarrativeArc | None = None
        elif isinstance(arc, str):
            if arc not in NARRATIVE_ARCS:
                raise ValueError(f"Unknown arc {arc!r}. Available: {sorted(NARRATIVE_ARCS)}")
            self._arc = NARRATIVE_ARCS[arc]
        else:
            self._arc = arc

        # Theme
        if theme is None:
            self._theme: PresentationTheme | None = None
        elif isinstance(theme, str):
            if theme not in PRESENTATION_THEMES:
                raise ValueError(f"Unknown theme {theme!r}. Available: {sorted(PRESENTATION_THEMES)}")
            self._theme = PRESENTATION_THEMES[theme]
        else:
            self._theme = theme

    @property
    def layout(self) -> LayoutStrategy:
        return self._layout

    def _effective_word_limit(self, slide_type: str, override: int | None = None) -> int:
        if override is not None:
            return override
        if self._max_words is not None:
            return int(self._max_words * self._density_multiplier)
        base = _WORDS_BY_TYPE.get(slide_type, MAX_WORDS_PER_NODE)
        return int(base * self._density_multiplier)

    def _maybe_relayout(self) -> None:
        if not self._auto_layout:
            return
        new_layout = auto_select_layout(len(self._slides), self._density_profile)
        if new_layout.name == self._layout.name:
            return
        self._layout = new_layout
        self._slide_layout = slide_layout_for_strategy(new_layout)
        for idx, slide in enumerate(self._slides):
            group = self._cb.get_node(slide["id"])
            if not group:
                continue
            old_x, old_y = float(group["x"]), float(group["y"])
            new_x, new_y = new_layout.slide_position(idx)
            dx, dy = new_x - old_x, new_y - old_y
            group["x"] = new_x
            group["y"] = new_y
            group["width"] = new_layout.slide_width
            group["height"] = new_layout.slide_height
            for nid in slide.get("node_ids", []):
                node = self._cb.get_node(nid)
                if node:
                    node["x"] = node["x"] + dx
                    node["y"] = node["y"] + dy

    # --- Theme auto-application ---

    _THEME_PRIMARY_TYPES = frozenset({"title", "section_divider"})
    _THEME_SECONDARY_TYPES = frozenset({"stats", "quote"})

    def _apply_theme(self) -> None:
        if self._theme is None:
            return
        for slide in self._slides:
            group = self._cb.get_node(slide["id"])
            if not group or group.get("color"):
                continue
            stype = slide["type"]
            role = slide.get("role")
            if role == "critical":
                group["color"] = self._theme.accent_color
            elif stype in self._THEME_PRIMARY_TYPES:
                group["color"] = self._theme.primary_color
            elif stype in self._THEME_SECONDARY_TYPES:
                group["color"] = self._theme.secondary_color

    # --- CSS class automation ---

    _CSS_CLASS_RULES: dict[str, str] = {
        "title": "hero", "section_divider": "hero", "quote": "cl-pres-quote",
        "stats": "cl-pres-stats", "comparison": "cl-pres-comparison",
        "diagram": "cl-pres-diagram", "image": "cl-pres-image",
        "timeline": "cl-pres-timeline", "process": "cl-pres-process",
        "three_column": "cl-pres-three-col", "key_value": "cl-pres-kv",
        "matrix": "cl-pres-matrix", "collage": "cl-pres-collage",
        "content": "cl-pres-content", "video": "cl-pres-video",
    }
    _ROLE_CSS_MAP: dict[str, str] = {"critical": "critical", "metadata": "muted"}

    def _apply_css_classes(self) -> None:
        for slide in self._slides:
            stype = slide["type"]
            role = slide.get("role")
            css_class = self._CSS_CLASS_RULES.get(stype)
            role_class = self._ROLE_CSS_MAP.get(role) if role else None
            for nid in slide.get("node_ids", []):
                node = self._cb.get_node(nid)
                if not node:
                    continue
                sa = node.setdefault("styleAttributes", {})
                existing = sa.get("cssclasses", "")
                classes = set(existing.split()) if existing else set()
                if css_class:
                    classes.add(css_class)
                if role_class:
                    classes.add(role_class)
                if classes:
                    sa["cssclasses"] = " ".join(sorted(classes))

    # --- Content metrics ---

    def _compute_fill_ratio(self, slide: dict[str, Any]) -> float:
        group = self._cb.get_node(slide["id"])
        if not group:
            return 0.0
        slide_area = group.get("width", 0) * group.get("height", 0)
        if slide_area <= 0:
            return 0.0
        node_area = 0.0
        for nid in slide.get("node_ids", []):
            node = self._cb.get_node(nid)
            if node:
                node_area += node.get("width", 0) * node.get("height", 0)
        return node_area / slide_area

    def _compute_whitespace(self, slide: dict[str, Any]) -> float:
        return 1.0 - self._compute_fill_ratio(slide)

    # --- Navigation ---

    def _apply_navigation(self) -> None:
        if not self._slides:
            return
        first_id = self._slides[0]["id"]
        first_node = self._cb.get_node(first_id)
        if first_node:
            first_node["isStartNode"] = True
            self._cb._start_node = first_id
        slide_ids = {s["id"] for s in self._slides}
        existing_nav = {
            (e["fromNode"], e["toNode"])
            for e in self._cb.edges
            if e["fromNode"] in slide_ids and e["toNode"] in slide_ids
        }
        for i in range(len(self._slides) - 1):
            from_id = self._slides[i]["id"]
            to_id = self._slides[i + 1]["id"]
            if (from_id, to_id) not in existing_nav:
                edge_id = CanvasBuilder.generate_id()
                f_side, t_side = self._layout.nav_sides(i)
                self._cb.add_edge(id=edge_id, from_node=from_id, to_node=to_id,
                                  from_side=f_side, to_side=t_side)

    # --- Markdown parser ---

    @classmethod
    def from_markdown(cls, text: str, name: str = "untitled") -> PresentationBuilder:
        pb = cls(name=name)
        if not text.strip():
            return pb
        lines = text.split("\n")
        i = 0
        title_done = False
        while i < len(lines):
            line = lines[i]
            if line.startswith("# ") and not line.startswith("## ") and not title_done:
                title_text = line[2:].strip()
                subtitle = None
                i += 1
                while i < len(lines) and not lines[i].strip():
                    i += 1
                if i < len(lines) and not lines[i].startswith("#"):
                    subtitle = lines[i].strip()
                    i += 1
                pb.add_title_slide(title_text, subtitle)
                title_done = True
                continue
            if line.startswith("## "):
                heading = line[3:].strip()
                i += 1
                body_lines: list[str] = []
                while (i < len(lines) and not lines[i].startswith("## ")
                       and not (lines[i].startswith("# ") and not lines[i].startswith("## "))):
                    body_lines.append(lines[i])
                    i += 1
                body = "\n".join(body_lines).strip()
                img_match = re.search(r"!\[([^\]]*)\]\(([^)]+)\)", body)
                if img_match:
                    pb.add_image_slide(heading, image_path=img_match.group(2), caption=img_match.group(1) or None)
                    continue
                body_stripped = body.strip()
                if not body_stripped or body_stripped in ("---", "***", "___"):
                    pb.add_section_divider(heading)
                    continue
                pb.add_content_slide(heading, body)
                continue
            i += 1
        return pb

    # --- Structural Analysis ---

    def structural_analysis(self) -> dict:
        canvas = self._cb.build()
        summary = structural_summary(canvas)
        slide_overlaps: dict[str, list[tuple[str, str]]] = {}
        slide_escapes: dict[str, list[str]] = {}
        for slide in self._slides:
            group = self._cb.get_node(slide["id"])
            if not group:
                continue
            interior = [self._cb.get_node(nid) for nid in slide.get("node_ids", [])
                        if self._cb.get_node(nid) is not None]
            if interior:
                pairs = detect_overlaps(interior)
                if pairs:
                    slide_overlaps[slide["id"]] = pairs
                escaped = containment_check(group, interior)
                if escaped:
                    slide_escapes[slide["id"]] = escaped
        summary["slide_overlaps"] = slide_overlaps
        summary["slide_escapes"] = slide_escapes
        return summary

    def _get_slide_text(self, slide: dict[str, Any]) -> str:
        parts: list[str] = []
        for nid in slide.get("node_ids", []):
            node = self._cb.get_node(nid)
            if node and node.get("type") == "text":
                parts.append(node.get("text", ""))
        return "\n".join(parts)

    def _count_slide_words(self, slide: dict[str, Any]) -> int:
        return len(self._get_slide_text(slide).split())

    # --- Structural fixes ---

    def _apply_structural_fixes(self) -> None:
        if self._slides and not self._cb._start_node:
            first_id = self._slides[0]["id"]
            first_node = self._cb.get_node(first_id)
            if first_node:
                first_node["isStartNode"] = True
                self._cb._start_node = first_id
        if len(self._slides) > 1:
            self._apply_navigation()
        for slide in self._slides:
            group = self._cb.get_node(slide["id"])
            if group:
                group["width"] = self._layout.slide_width
                group["height"] = self._layout.slide_height

    def refine(self, max_iterations: int = 3) -> PresentationReport:
        self._apply_structural_fixes()
        for _ in range(max_iterations):
            for slide in list(self._slides):
                slide_limit = self._effective_word_limit(slide["type"], slide.get("max_words"))
                for nid in list(slide.get("node_ids", [])):
                    node = self._cb.get_node(nid)
                    if not node or node.get("type") != "text":
                        continue
                    words = node.get("text", "").split()
                    if len(words) > slide_limit:
                        node["text"] = " ".join(words[:slide_limit]) + "..."
            if len(self._slides) > 1:
                self._apply_navigation()
            for slide in self._slides:
                interior = [self._cb.get_node(nid) for nid in slide.get("node_ids", [])
                            if self._cb.get_node(nid) is not None]
                if len(interior) >= 2:
                    pairs = detect_overlaps(interior)
                    for id_a, id_b in pairs:
                        node_a = self._cb.get_node(id_a)
                        node_b = self._cb.get_node(id_b)
                        if node_a and node_b:
                            a_bottom = node_a["y"] + node_a.get("height", 200)
                            if node_b["y"] < a_bottom:
                                node_b["y"] = a_bottom + 10
            report = self.review()
            if report.passed:
                return report
        return self.review()

    # --- Image lifecycle ---

    def resolve_pending_image(self, pending_id: str, actual_path: str) -> None:
        pending = self._pending_images.get(pending_id)
        if not pending:
            raise ValueError(f"No pending image with id: {pending_id}")
        node = self._cb.get_node(pending_id)
        if not node:
            raise ValueError(f"Node {pending_id} not found in canvas")
        node["type"] = "file"
        node["file"] = actual_path
        node.pop("text", None)
        pending.status = "resolved"

    @property
    def pending_images(self) -> list[PendingImage]:
        return [p for p in self._pending_images.values() if p.status == "pending"]

    @property
    def density_profile(self) -> str:
        return self._density_profile

    def build(self) -> dict:
        self._maybe_relayout()
        self._apply_theme()
        self._apply_css_classes()
        self._apply_navigation()
        self._cb._reserved.update({
            "generator": "PresentationBuilder",
            "version": "1.0.0",
            "slide_count": len(self._slides),
            "presentation_type": self.presentation_type,
            "layout": self._layout.name,
            "density_profile": self._density_profile,
            "narrative_arc": self._arc.name if self._arc else None,
            "theme": self._theme.name if self._theme else None,
            "audience": self._audience.name if self._audience else None,
        })
        report = self.review()
        self._cb._reserved["review_score"] = report.score
        return self._cb.build()

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        canvas = self.build()
        path.write_text(json.dumps(canvas, indent=2) + "\n")
        return path

    def validate(self) -> list[str]:
        return self._cb.validate()

    @property
    def slides(self) -> list[dict[str, Any]]:
        return list(self._slides)

    def __repr__(self) -> str:
        return f"PresentationBuilder({self._cb.name!r}, slides={len(self._slides)}, type={self.presentation_type!r})"
