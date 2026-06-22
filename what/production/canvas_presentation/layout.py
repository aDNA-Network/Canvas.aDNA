"""Deck layout engine — grid positioning and interior node placement.

Deck-bound residue of lattice-protocol/extensions/canvas/canvas_layout.py.
Golden-ratio helpers (PHI, golden_split, golden_rect, thirds_points,
fibonacci_spacing) extracted to canvas_core.geometry per ADR 001.

Populated in M-2a-01 (Phase 2a — Deck Application Extraction).
"""

from __future__ import annotations

from dataclasses import dataclass

from canvas_core.geometry import golden_split

# ---------------------------------------------------------------------------
# LayoutStrategy — grid-level positioning
# ---------------------------------------------------------------------------


@dataclass
class LayoutStrategy:
    """Configures the overall grid layout for slide positioning."""

    name: str
    columns: int
    slide_width: int
    slide_height: int
    h_gap: int = 200
    v_gap: int = 200
    min_height: int = 600
    max_height: int = 1600

    def slide_position(self, index: int) -> tuple[float, float]:
        col = index % self.columns
        row = index // self.columns
        x = col * (self.slide_width + self.h_gap)
        y = row * (self.slide_height + self.v_gap)
        return float(x), float(y)

    def nav_sides(self, index: int) -> tuple[str, str]:
        if index % self.columns < self.columns - 1:
            return "right", "left"
        return "bottom", "top"


# ---------------------------------------------------------------------------
# Built-in strategy presets
# ---------------------------------------------------------------------------

LAYOUT_GRID_2COL = LayoutStrategy("grid_2col", columns=2, slide_width=1200, slide_height=1100)
LAYOUT_GRID_1COL = LayoutStrategy("grid_1col", columns=1, slide_width=1200, slide_height=1100)
LAYOUT_GRID_3COL = LayoutStrategy("grid_3col", columns=3, slide_width=1000, slide_height=900, h_gap=150, v_gap=150)

LAYOUT_PRESETS: dict[str, LayoutStrategy] = {
    "grid_2col": LAYOUT_GRID_2COL,
    "grid_1col": LAYOUT_GRID_1COL,
    "grid_3col": LAYOUT_GRID_3COL,
}


def get_layout(name: str) -> LayoutStrategy:
    if name not in LAYOUT_PRESETS:
        raise ValueError(f"Unknown layout {name!r}. Available: {sorted(LAYOUT_PRESETS)}")
    return LAYOUT_PRESETS[name]


def auto_select_layout(slide_count: int, density_profile: str = "balanced") -> LayoutStrategy:
    if density_profile == "sparse" or slide_count <= 4:
        return LAYOUT_GRID_1COL
    if density_profile == "dense" and slide_count >= 8:
        return LAYOUT_GRID_3COL
    return LAYOUT_GRID_2COL


# ---------------------------------------------------------------------------
# SlideLayout — interior node positioning
# ---------------------------------------------------------------------------


@dataclass
class NodePlacement:
    """Computed position and size for an interior node."""

    x: float
    y: float
    width: float
    height: float


@dataclass
class SlideLayout:
    """Computes interior node positions within a slide group."""

    name: str
    slide_width: int = 1200
    slide_height: int = 1100
    margin_top: int = 40
    margin_side: int = 60
    margin_bottom: int = 40
    heading_height: int = 120
    gap: int = 20

    @property
    def content_width(self) -> int:
        return self.slide_width - 2 * self.margin_side

    @property
    def body_top(self) -> int:
        return self.margin_top + self.heading_height + self.gap

    @property
    def body_height(self) -> int:
        return self.slide_height - self.body_top - self.margin_bottom

    def heading(self) -> NodePlacement:
        return NodePlacement(x=self.margin_side, y=self.margin_top,
                             width=self.content_width, height=self.heading_height)

    def compute_stacked(self, body_count: int = 1) -> list[NodePlacement]:
        if body_count <= 0:
            return []
        node_gap = 10
        available = self.body_height - (body_count - 1) * node_gap
        node_h = available / body_count
        placements: list[NodePlacement] = []
        y = self.body_top
        for _ in range(body_count):
            placements.append(NodePlacement(x=self.margin_side, y=y, width=self.content_width, height=node_h))
            y += node_h + node_gap
        return placements

    def compute_split(self, ratio: float = 0.6) -> tuple[NodePlacement, NodePlacement]:
        col_gap = 25
        available = self.content_width - col_gap
        if abs(ratio - 0.5) < 0.01:
            left_w = available // 2
            right_w = left_w
        else:
            left_w = int(available * ratio)
            right_w = available - left_w
        left = NodePlacement(x=self.margin_side, y=self.body_top, width=left_w, height=self.body_height)
        right = NodePlacement(x=self.margin_side + left_w + col_gap, y=self.body_top, width=right_w, height=self.body_height)
        return left, right

    def compute_centered(self) -> NodePlacement:
        content_h = self.body_height * 0.5
        return NodePlacement(
            x=self.margin_side + self.content_width * 0.1,
            y=self.body_top + (self.body_height - content_h) / 2,
            width=self.content_width * 0.8,
            height=content_h,
        )

    def compute_grid(self, count: int, cols: int = 2) -> list[NodePlacement]:
        if count <= 0:
            return []
        rows = (count + cols - 1) // cols
        col_gap = 25
        row_gap = 20
        item_w = (self.content_width - (cols - 1) * col_gap) / cols
        item_h = (self.body_height - (rows - 1) * row_gap) / rows
        placements: list[NodePlacement] = []
        for i in range(count):
            r = i // cols
            c = i % cols
            placements.append(NodePlacement(
                x=self.margin_side + c * (item_w + col_gap),
                y=self.body_top + r * (item_h + row_gap),
                width=item_w, height=item_h,
            ))
        return placements

    def compute_asymmetric(self, ratio: float = 0.4, *, golden: bool = False) -> tuple[NodePlacement, NodePlacement]:
        col_gap = 30
        if golden:
            major, minor = golden_split(self.content_width - col_gap)
            accent_w = int(major)
            main_w = int(minor)
        else:
            accent_w = int((self.content_width - col_gap) * ratio)
            main_w = self.content_width - col_gap - accent_w
        accent = NodePlacement(x=self.margin_side, y=self.body_top, width=accent_w, height=self.body_height)
        main = NodePlacement(x=self.margin_side + accent_w + col_gap, y=self.body_top, width=main_w, height=self.body_height)
        return accent, main


def slide_layout_for_strategy(strategy: LayoutStrategy) -> SlideLayout:
    return SlideLayout(name=strategy.name, slide_width=strategy.slide_width, slide_height=strategy.slide_height)


def compute_dynamic_height(
    word_count: int, node_count: int, strategy: LayoutStrategy,
    *, words_per_100px: int = 15, base_overhead: int = 300,
) -> int:
    text_height = (word_count / words_per_100px) * 100
    node_overhead = node_count * 30
    raw = base_overhead + text_height + node_overhead
    return max(strategy.min_height, min(int(raw), strategy.max_height))
