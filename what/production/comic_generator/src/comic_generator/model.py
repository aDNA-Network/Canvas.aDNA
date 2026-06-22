"""Input model — a structured comic spec (an ordered list of pages, each a 2D grid of panels) + its instance data.

A substrate-free producer-side domain model: a human/agent authors a comic (a title + ordered pages; each page a
grid of panels carrying a panel_type, a scene, characters, an optional already-rendered image path, and an optional
spatial layout) and, optionally, the **instance data** the prompt engine routes through — a character bible, a
per-spread color script, and a per-spread story state. The consumer (``consume.py``) maps the comic onto the aDNA
Canvas Standard and emits each panel's assembled 6-layer image **prompt** as declarative ``_reserved`` metadata.

Per ratified scope D5 the engine is **data-driven**: ``style.py`` carries the canvas-agnostic *mechanism* (panel-type
camera/composition templates, Wally-Wood keyword categories, act-lighting defaults, art-style prefixes); the *instance
data* (a specific character bible / color-script / story-state — e.g. the Science-Stanley dual-protagonist run) is NOT
baked into the engine — it rides on ``ComicInput`` (or defaults to empty). No ``canvas_std`` import here — the model is
pure domain data (ADR-004 two-shelf firewall; Operation Atelier A2).

Lineage (KEEP reference, NOT a dependency): ``Archive.aDNA/CanvasForge.aDNA/what/code/canvas_comic/comic.py`` —
``Panel``/``Page``/``CharacterState``/``StoryState``/``SpreadColorScript`` retyped here as substrate-free frozen
dataclasses; ``CanvasBuilder`` / ``ContextPack`` / ``ImagePrompt`` couplings dropped.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# The panel-type template set (ported verbatim from the quarry's PANEL_TYPE_TEMPLATES keys). A panel's ``panel_type``
# MUST be one of these — the prompt engine looks the camera/composition/nuances up by this key.
PANEL_TYPES: frozenset[str] = frozenset(
    {"establishing", "dialogue", "action", "close_up", "splash", "transition"}
)

# Page layout kinds — how a page's panels tile the page surface (geometry resolved in ``layout.py``).
LAYOUT_TYPES: frozenset[str] = frozenset({"grid", "splash", "spread"})


# ============================================================================================================
# Instance data (data-driven; routed through the input — NOT baked into the engine, scope D5).
# ============================================================================================================

@dataclass(frozen=True)
class CharacterDescriptor:
    """A character's canonical visual descriptor (the character-bible row) + the story-state keys it participates in.

    The ``name`` is matched case-insensitively against a panel's ``characters`` list; ``descriptor`` is the Layer-2
    character-block text. This replaces the quarry's hardcoded ``CHARACTER_STANLEY``/``_AGENT_STANLEY``/``_HELIX``
    constants — the engine no longer knows any specific character; the bible is supplied per comic.
    """

    name: str
    descriptor: str = ""


@dataclass(frozen=True)
class CharacterStateEntry:
    """A character's state within one spread (presence + a mood/pose suffix merged onto its descriptor)."""

    present: bool = False
    mood: str = ""
    pose: str = ""


@dataclass(frozen=True)
class SpreadColorScript:
    """A spread's color-script row — the Layer-5 lighting source (ported from the quarry's SPREAD_COLOR_SCRIPT)."""

    spread: int
    dominant: str = ""
    accent: str = ""
    lighting: str = ""
    mood: str = ""
    act: str = ""


@dataclass(frozen=True)
class SpreadStoryState:
    """A spread's dual-/multi-protagonist story state — keyed by character name (lowercased) → state."""

    spread: int
    characters: dict[str, CharacterStateEntry] = field(default_factory=dict)
    world: str = ""


# ============================================================================================================
# Comic structure.
# ============================================================================================================

@dataclass(frozen=True)
class Panel:
    """A single comic panel within a page's grid.

    ``image_path`` (optional): an already-rendered image — when present the panel becomes a baseline ``file`` node and
    its ``qualities.status`` is ``"rendered"``; otherwise a ``text`` placeholder carrying the scene excerpt with
    ``status: "prompt_only"``. ``spatial_layout`` (optional): a ``comic_panel_layout`` Mermaid string (parsed/validated
    by ``panel_layout.py``) that rides into the panel's ``qualities.spatial_layout`` + the assembled dual prompt.
    ``camera_angle``/``mood``/``balloon_space``/``style_override``/``compositional_nuance`` are optional prompt
    overrides; ``row``/``col``/``span_rows``/``span_cols`` place the panel in the page grid.
    """

    panel_type: str = "action"
    scene: str = ""
    characters: tuple[str, ...] = ()
    image_path: str = ""
    aspect_ratio: str = ""
    spatial_layout: str = ""
    camera_angle: str = ""
    mood: str = ""
    balloon_space: str = ""
    style_override: str = ""
    compositional_nuance: str = ""
    compositional_intent: str = ""
    row: int = 0
    col: int = 0
    span_rows: int = 1
    span_cols: int = 1
    bleed: bool = False

    def __post_init__(self) -> None:
        if self.panel_type not in PANEL_TYPES:
            raise ValueError(
                f"unknown panel_type {self.panel_type!r}; expected one of {sorted(PANEL_TYPES)}"
            )


@dataclass(frozen=True)
class Page:
    """A comic page: an ordered grid of panels + an optional spread number (keys the color-script / story-state).

    ``layout_type`` selects how the panels tile the page (grid | splash | spread); ``art_style`` overrides the page's
    style prefix (else the comic default). ``number`` is the 1-based page number.
    """

    number: int
    panels: tuple[Panel, ...]
    layout_type: str = "grid"
    spread_number: int | None = None
    art_style: str = ""

    def __post_init__(self) -> None:
        if self.layout_type not in LAYOUT_TYPES:
            raise ValueError(
                f"unknown layout_type {self.layout_type!r}; expected one of {sorted(LAYOUT_TYPES)}"
            )
        if not self.panels:
            raise ValueError(f"page {self.number} has no panels")


@dataclass(frozen=True)
class Spread:
    """A two-page spread grouping (the spread number + its two page numbers). Optional structural overlay."""

    number: int
    pages: tuple[int, ...] = ()


@dataclass(frozen=True)
class ComicInput:
    """A whole comic: title + id + version + ordered pages, plus the data-driven instance overlays.

    ``characters`` is the character bible (name → descriptor); ``color_script`` and ``story_state`` are keyed by spread
    number. All overlays default empty — an empty comic still builds (the engine falls back to mechanism defaults), so
    the producer is fully substrate- AND project-neutral (scope D5). ``art_style`` is the comic-wide default style
    prefix name; ``refs`` are declarative context-object wikilinks (character-bible / color-script / storyboard).
    """

    title: str
    id: str
    version: str
    pages: tuple[Page, ...]
    spreads: tuple[Spread, ...] = ()
    characters: tuple[CharacterDescriptor, ...] = ()
    color_script: tuple[SpreadColorScript, ...] = ()
    story_state: tuple[SpreadStoryState, ...] = ()
    art_style: str = "ghibli"
    refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.pages:
            raise ValueError("comic has no pages")
        nums = [p.number for p in self.pages]
        if len(nums) != len(set(nums)):
            raise ValueError("duplicate page number in comic")

    # --- Lookups (the data-driven analogs of the quarry's _get_* helpers) ----------------------------------

    def character_bible(self) -> dict[str, str]:
        """name.lower() -> descriptor (the character registry the prompt engine consults)."""
        return {c.name.lower(): c.descriptor for c in self.characters}

    def color_script_for(self, spread_number: int | None) -> SpreadColorScript | None:
        if spread_number is None:
            return None
        for cs in self.color_script:
            if cs.spread == spread_number:
                return cs
        return None

    def story_state_for(self, spread_number: int | None) -> SpreadStoryState | None:
        if spread_number is None:
            return None
        for ss in self.story_state:
            if ss.spread == spread_number:
                return ss
        return None

    def page_count(self) -> int:
        return len(self.pages)

    def panel_count(self) -> int:
        return sum(len(p.panels) for p in self.pages)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ComicInput:
        pages: list[Page] = []
        for pg in d.get("pages", []):
            panels = tuple(_panel_from_dict(p) for p in pg.get("panels", []))
            pages.append(
                Page(
                    number=int(pg["number"]),
                    panels=panels,
                    layout_type=str(pg.get("layout_type", "grid")),
                    spread_number=(int(pg["spread_number"]) if pg.get("spread_number") is not None else None),
                    art_style=str(pg.get("art_style", "")),
                )
            )

        spreads = tuple(
            Spread(number=int(s["number"]), pages=tuple(int(x) for x in s.get("pages", [])))
            for s in d.get("spreads", [])
        )
        characters = tuple(
            CharacterDescriptor(name=str(c["name"]), descriptor=str(c.get("descriptor", "")))
            for c in d.get("characters", [])
        )
        color_script = tuple(
            SpreadColorScript(
                spread=int(cs["spread"]),
                dominant=str(cs.get("dominant", "")),
                accent=str(cs.get("accent", "")),
                lighting=str(cs.get("lighting", "")),
                mood=str(cs.get("mood", "")),
                act=str(cs.get("act", "")),
            )
            for cs in d.get("color_script", [])
        )
        story_state = tuple(_story_state_from_dict(ss) for ss in d.get("story_state", []))

        return cls(
            title=str(d["title"]),
            id=str(d["id"]),
            version=str(d.get("version", "0.1.0")),
            pages=tuple(pages),
            spreads=spreads,
            characters=characters,
            color_script=color_script,
            story_state=story_state,
            art_style=str(d.get("art_style", "ghibli")),
            refs=tuple(str(r) for r in d.get("refs", [])),
        )


def _panel_from_dict(p: dict[str, Any]) -> Panel:
    return Panel(
        panel_type=str(p.get("panel_type", "action")),
        scene=str(p.get("scene", "")).strip(),
        characters=tuple(str(c) for c in p.get("characters", [])),
        image_path=str(p.get("image_path", "")),
        aspect_ratio=str(p.get("aspect_ratio", "")),
        spatial_layout=str(p.get("spatial_layout", "")),
        camera_angle=str(p.get("camera_angle", "")),
        mood=str(p.get("mood", "")),
        balloon_space=str(p.get("balloon_space", "")),
        style_override=str(p.get("style_override", "")),
        compositional_nuance=str(p.get("compositional_nuance", "")),
        compositional_intent=str(p.get("compositional_intent", "")),
        row=int(p.get("row", 0)),
        col=int(p.get("col", 0)),
        span_rows=int(p.get("span_rows", 1)),
        span_cols=int(p.get("span_cols", 1)),
        bleed=bool(p.get("bleed", False)),
    )


def _story_state_from_dict(ss: dict[str, Any]) -> SpreadStoryState:
    chars_raw = ss.get("characters", {})
    characters = {
        str(name).lower(): CharacterStateEntry(
            present=bool(st.get("present", False)),
            mood=str(st.get("mood", "")),
            pose=str(st.get("pose", "")),
        )
        for name, st in chars_raw.items()
    }
    return SpreadStoryState(
        spread=int(ss["spread"]),
        characters=characters,
        world=str(ss.get("world", "")),
    )


def load_comic(path: str | Path) -> ComicInput:
    """Load a comic from ``.yaml``/``.yml`` (PyYAML) or ``.json``."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in (".yaml", ".yml"):
        import yaml

        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"comic input {p} did not parse to a mapping")
    return ComicInput.from_dict(data)
