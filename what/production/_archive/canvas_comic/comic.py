"""ComicPageBuilder — comic book page/issue generator wrapping CanvasBuilder.

Generates Obsidian canvas layouts for comic book production with print-spec
coordinates, 6-layer prompt assembly, act-based color scripting, story state
tracking, and decoupled image generation (Option A — prompts only).

Migrated from lattice-protocol/extensions/canvas/canvas_comic.py.
Populated in M-2b-01 (Phase 2b — Comic Application Extraction).
"""

from __future__ import annotations

import json
import statistics
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from canvas_core import CanvasBuilder
from canvas_core.image_generation import ImagePrompt

# ---------------------------------------------------------------------------
# Print-spec constants (ComixWellspring standard, 1" = 100 canvas units)
# ---------------------------------------------------------------------------

TRIM_WIDTH = 662.5
TRIM_HEIGHT = 1025.0
SAFE_WIDTH = 637.5
SAFE_HEIGHT = 1000.0
SAFE_ORIGIN_X = 25.0
SAFE_ORIGIN_Y = 12.5
PANEL_GUTTER = 10.0
BLEED_WIDTH = 687.5
BLEED_HEIGHT = 1050.0

# ---------------------------------------------------------------------------
# Issue dimensions
# ---------------------------------------------------------------------------

TOTAL_PAGES = 32
TOTAL_SPREADS = 16

# ---------------------------------------------------------------------------
# Aspect ratio map (panel type → Imagen 4 setting)
# ---------------------------------------------------------------------------

ASPECT_RATIOS: dict[str, str] = {
    "standard": "1:1",
    "tall": "3:4",
    "wide": "16:9",
    "full_page": "3:4",
    "splash": "9:16",
    "spread": "4:3",
}

# ---------------------------------------------------------------------------
# F-38 ContextPack (M-R2-02 spec § 7.2)
# ---------------------------------------------------------------------------


@dataclass
class ContextPack:
    """F-38 sister surface — canonical context library required by canvas_comic
    prompt assembly.

    Forces fail-fast when context wasn't loaded before panel-prompt
    generation. Per ADR 003 + M-R1-03 § 7 (Quinn/UCLA gap): the lattice node
    ``image_generation`` declares these as inputs; the orchestrator loads
    them; :meth:`ComicPageBuilder.generate_panel_prompt` requires this pack
    as a keyword-only argument so it cannot be invoked without it. Hand-
    authored markdown prompt-assembly is no longer supported (deprecated in
    ``skill_canvas_comic.md`` by M-R6-02).

    Consumer-vault overrides: SS comic, CC comic (when authored), WGA (when
    authored), KINN provide their own ContextPack instances pointing at
    vault-local context paths. CanvasForge canonical default points at
    SS-comic-flavored paths; consumer wrappers replace as needed.
    """

    storyboard_canvas: Path
    character_bible: Path
    color_theory: Path
    prompt_engineering: Path
    voice_foundations: Path


class ContextNotLoaded(RuntimeError):
    """Raised by :meth:`ComicPageBuilder.generate_panel_prompt` when
    ``context_pack`` is absent or any of its paths is missing."""


# ---------------------------------------------------------------------------
# Panel type templates (camera + composition + nuances strings)
#
# ``nuances`` sub-dimension landed at M-V1-2-F-01 S4 per ADR-008 §D2
# sub-dimension addendum (the third orthogonal Layer-4 contract after
# §D2 candidate B1 — RLHF hints surface — and §D2 candidate B2 —
# character_registry kwarg). Seed entries drawn verbatim from III
# learning store ``pick_reason`` corpus (lines 6–9 of
# iii/what/context/canvasforge_iii_learning_store.jsonl as of S4 open):
# composition_naturalness (line 6 "composition naturalness (Quinn's own
# presence holds the frame)"); physical_contact_clarity (line 7
# "shoulder-contact issue ... fixed"); crowd_depth_refinement (line 7
# "crowd depth refined"); object_interaction_focus (line 8
# "turning-it-over interaction matches cover; character drawn toward
# variant_02"); fading_visual_effect (line 9 "Fading-hand effect lands;
# vanishing beat"). Vocabulary is generic composition terms — no
# Stanley/Helix/Wilhelm-specific knowledge in the keys or descriptors.
# Re-merge rationale: lattice-labs/who/coordination/coord_2026_04_16_forge_split.md.
# ---------------------------------------------------------------------------

PANEL_TYPE_TEMPLATES: dict[str, dict[str, Any]] = {
    "establishing": {
        "camera": (
            "Wide angle view, long shot, full environment visible, deep "
            "perspective with foreground, midground, and background layers."
        ),
        "composition": "wide establishing shot showing the full environment",
        "nuances": {
            "composition_naturalness": "subject's own presence anchors the frame; avoid forced staging",
            "crowd_depth_refinement": "differentiate foreground, midground, and background crowd density",
        },
    },
    "dialogue": {
        "camera": (
            "Medium shot, eye level view. Upper third of frame clear for dialogue balloon space."
        ),
        "composition": "conversation composition with clear space in upper portion",
        "nuances": {
            "physical_contact_clarity": "spatial relationships between figures read cleanly; avoid shoulder-overlap ambiguity",
            "object_interaction_focus": "hands and any held object share the frame focus",
            "composition_naturalness": "natural stance and gesture; avoid forced posing",
        },
    },
    "action": {
        "camera": (
            "Medium long shot, dynamic angle view. Panel composition "
            "emphasizes movement direction and action focus."
        ),
        "composition": "dynamic action composition with motion energy",
        "nuances": {
            "physical_contact_clarity": "interactions between figures read cleanly without overlap ambiguity",
            "crowd_depth_refinement": "differentiate background motion from foreground action",
        },
    },
    "close_up": {
        "camera": (
            "Close-up shot, eye level angle. Subject filling the frame. "
            "Shallow depth — background blurred or abstracted to dark."
        ),
        "composition": "tight close-up filling the frame",
        "nuances": {
            "object_interaction_focus": "held object and hands share the frame focus",
            "fading_visual_effect": "subtle visual fade or vanishing element carries a narrative beat",
        },
    },
    "splash": {
        "camera": (
            "Splash page composition, single dramatic image, rule of thirds "
            "placement for focal point."
        ),
        "composition": "epic full-page dramatic composition",
        "nuances": {
            "composition_naturalness": "subject's stance anchors the dramatic moment; avoid forced spectacle",
        },
    },
    "transition": {
        "camera": (
            "Wide shot, high angle or flat plane. Minimal detail, emphasis "
            "on color, light, and atmosphere."
        ),
        "composition": "atmospheric transition with visual bridge between scenes",
        "nuances": {
            "fading_visual_effect": "visual element fades or vanishes to bridge scenes",
        },
    },
}

# ---------------------------------------------------------------------------
# Act mapping (page ranges → act info)
# ---------------------------------------------------------------------------

ACT_PAGE_RANGES: dict[str, dict[str, Any]] = {
    "cover": {"pages": (1, 2), "label": "Cover Matter", "color": "#565f89"},
    "act_1": {
        "pages": (3, 10),
        "label": "Act I: The Scientist and His Mission",
        "color": "#7dcfff",
    },
    "act_2": {"pages": (11, 20), "label": "Act II: Learning the Lab", "color": "#9ece6a"},
    "act_3": {"pages": (21, 30), "label": "Act III: The Bigger Picture", "color": "#9d7cd8"},
    "closing": {"pages": (31, 32), "label": "Closing Matter", "color": "#565f89"},
}

ACT_CANVAS_COLORS: dict[str, str | None] = {
    "cover": None,  # neutral
    "act_1": "5",  # cyan
    "act_2": "4",  # green
    "act_3": "6",  # purple
    "closing": None,  # neutral
}

# ---------------------------------------------------------------------------
# 15-spread color script
# ---------------------------------------------------------------------------

SPREAD_COLOR_SCRIPT: dict[int, dict[str, Any]] = {
    1: {
        "pages": (1, 2),
        "act": "cover",
        "dominant": "#565f89",
        "accent": "#e0af68",
        "lighting": "neutral",
        "mood": "cover_matter",
    },
    2: {
        "pages": (3, 4),
        "act": "act_1",
        "dominant": "#e0af68",
        "accent": "#cfc9c2",
        "lighting": "warm_golden",
        "mood": "inviting",
    },
    3: {
        "pages": (5, 6),
        "act": "act_1",
        "dominant": "#e0af68",
        "accent": "#565f89",
        "lighting": "warm_to_midnight",
        "mood": "determined_to_exhausted",
    },
    4: {
        "pages": (7, 8),
        "act": "act_1",
        "dominant": "#2f3549",
        "accent": "#7dcfff",
        "lighting": "dark_screen_glow",
        "mood": "mysterious_discovery",
    },
    5: {
        "pages": (9, 10),
        "act": "act_1",
        "dominant": "#7aa2f7",
        "accent": "#9ece6a",
        "lighting": "crt_glow",
        "mood": "confused_to_purposeful",
    },
    6: {
        "pages": (11, 12),
        "act": "act_2",
        "dominant": "#9ece6a",
        "accent": "#e0af68",
        "lighting": "multi_station_glow",
        "mood": "exploration_mastery",
    },
    7: {
        "pages": (13, 14),
        "act": "act_2",
        "dominant": "#9d7cd8",
        "accent": "#f7768e",
        "lighting": "speed_blur",
        "mood": "euphoric_to_sobering",
    },
    8: {
        "pages": (15, 16),
        "act": "act_2",
        "dominant": "#9ece6a",
        "accent": "#e0af68",
        "lighting": "cycle_glow",
        "mood": "instructive_awe",
    },
    9: {
        "pages": (17, 18),
        "act": "act_2",
        "dominant": "#7dcfff",
        "accent": "#cfc9c2",
        "lighting": "network_luminance",
        "mood": "revelation_recognition",
    },
    10: {
        "pages": (19, 20),
        "act": "act_2",
        "dominant": "#9ece6a",
        "accent": "#e0af68",
        "lighting": "terminal_green",
        "mood": "concrete_to_expansive",
    },
    11: {
        "pages": (21, 22),
        "act": "act_3",
        "dominant": "#1a1b26",
        "accent": "#e0af68",
        "lighting": "cosmic_starfield",
        "mood": "cosmic_structural",
    },
    12: {
        "pages": (23, 24),
        "act": "act_3",
        "dominant": "#e0af68",
        "accent": "#73daca",
        "lighting": "warm_amber",
        "mood": "emotional_hopeful",
    },
    13: {
        "pages": (25, 26),
        "act": "act_3",
        "dominant": "#f7768e",
        "accent": "#565f89",
        "lighting": "warning_split",
        "mood": "responsible_urgent",
    },
    14: {
        "pages": (27, 28),
        "act": "act_3",
        "dominant": "#e0af68",
        "accent": "#cfc9c2",
        "lighting": "golden_craft",
        "mood": "virtuous_proud",
    },
    15: {
        "pages": (29, 30),
        "act": "act_3",
        "dominant": "#ff9e64",
        "accent": "#f7768e",
        "lighting": "sunset",
        "mood": "warm_exciting",
    },
    16: {
        "pages": (31, 32),
        "act": "closing",
        "dominant": "#565f89",
        "accent": "#e0af68",
        "lighting": "starlight",
        "mood": "educational_contemplative",
    },
}

# ---------------------------------------------------------------------------
# 15-spread story state table (dual protagonist)
# ---------------------------------------------------------------------------

SPREAD_STORY_STATE: dict[int, dict[str, Any]] = {
    1: {
        "science_stanley": {"present": False},
        "agent_stanley": {"present": False},
        "helix": {"present": False},
        "world": "cover",
    },
    2: {
        "science_stanley": {
            "present": True,
            "mood": "confident",
            "props": ["clipboard"],
            "glasses": True,
            "cap": False,
        },
        "agent_stanley": {"present": False},
        "helix": {"present": False},
        "world": "ghibli",
    },
    3: {
        "science_stanley": {
            "present": True,
            "mood": "determined",
            "props": ["papers", "phone"],
            "glasses": True,
            "cap": False,
        },
        "agent_stanley": {"present": False},
        "helix": {"present": False},
        "world": "ghibli",
    },
    4: {
        "science_stanley": {
            "present": True,
            "mood": "exhausted",
            "props": ["keyboard"],
            "glasses": True,
            "cap": False,
        },
        "agent_stanley": {"present": True, "mood": "cheeky", "pose": "waving"},
        "helix": {"present": False},
        "world": "transition",
    },
    5: {
        "science_stanley": {"present": False},
        "agent_stanley": {
            "present": True,
            "mood": "confused_to_determined",
            "pose": "reading_file",
        },
        "helix": {"present": False},
        "world": "pixel",
    },
    6: {
        "science_stanley": {"present": False},
        "agent_stanley": {"present": True, "mood": "exploring", "pose": "looking_around"},
        "helix": {"present": False},
        "world": "pixel",
    },
    7: {
        "science_stanley": {"present": False},
        "agent_stanley": {"present": True, "mood": "euphoric", "pose": "speed_blur"},
        "helix": {"present": False},
        "world": "pixel_mixed",
    },
    8: {
        "science_stanley": {"present": False},
        "agent_stanley": {"present": True, "mood": "learning", "pose": "reading"},
        "helix": {"present": False},
        "world": "pixel",
    },
    9: {
        "science_stanley": {"present": False},
        "agent_stanley": {"present": True, "mood": "revelatory", "pose": "pointing_at_viewer"},
        "helix": {"present": False},
        "world": "pixel_mixed",
    },
    10: {
        "science_stanley": {"present": False},
        "agent_stanley": {"present": True, "mood": "concrete", "pose": "bridging_worlds"},
        "helix": {"present": False},
        "world": "pixel",
    },
    11: {
        "science_stanley": {"present": False},
        "agent_stanley": {"present": False},
        "helix": {"present": False},
        "world": "cosmic_mixed",
    },
    12: {
        "science_stanley": {"present": False},
        "agent_stanley": {"present": False},
        "helix": {"present": False},
        "world": "mixed",
    },
    13: {
        "science_stanley": {"present": False},
        "agent_stanley": {"present": True, "mood": "responsible", "pose": "stop_gesture"},
        "helix": {"present": False},
        "world": "mixed",
    },
    14: {
        "science_stanley": {
            "present": True,
            "mood": "proud",
            "props": ["monitor"],
            "glasses": True,
            "cap": False,
        },
        "agent_stanley": {"present": False},
        "helix": {"present": True, "pose": "sleeping_at_feet"},
        "world": "ghibli_mixed",
    },
    15: {
        "science_stanley": {
            "present": True,
            "mood": "hopeful",
            "props": [],
            "glasses": False,
            "cap": False,
        },
        "agent_stanley": {"present": False},
        "helix": {"present": False},
        "world": "ghibli_mixed",
    },
    16: {
        "science_stanley": {
            "present": True,
            "mood": "contemplative",
            "props": [],
            "glasses": True,
            "cap": False,
        },
        "agent_stanley": {"present": True, "mood": "companionable", "pose": "on_shoulder_sprite"},
        "helix": {"present": False},
        "world": "ghibli",
    },
}

# ---------------------------------------------------------------------------
# Wally Wood keyword categories
# ---------------------------------------------------------------------------

WOOD_KEYWORDS: dict[str, str] = {
    "dialogue": "Big Head close-up, over-the-shoulder view, side profile, layered depth composition",
    "establishing": "tiny figure in vast environment, layered depth, bird's eye view with shadows, framed by doorway or window",
    "emotional": "extreme close-up of face filling frame, dramatic side lighting, strong shadows, high contrast chiaroscuro",
    "action": "full body dynamic pose, bird's eye view dramatic shadows, single decisive moment, high contrast",
    "action_sequence": "full body dynamic pose, bird's eye view dramatic shadows, multiple poses showing progression, high contrast",
    "transition": "dark silhouetted figures bright background, character silhouette backlit, silhouette against bright background",
    "technical": "eye level straightforward composition, macro close-up of detail, screen or document insert, single object centered dramatic scale",
}

# ---------------------------------------------------------------------------
# Art style constants (3 separate styles)
# ---------------------------------------------------------------------------

STYLE_GHIBLI = (
    "Studio Ghibli-inspired illustration style. "
    "Warm palette — golden ambers, soft greens, sunset oranges. "
    "Natural lighting, organic textures — paper, wood, fabric, glass. "
    "Expressive faces, fluid movement, lived-in spaces. "
    "Clean linework with painterly warmth."
)

STYLE_PIXEL = (
    "16-bit pixel art style, retro RPG aesthetic. "
    "CRT-glow palette — blues, neon greens, electric purples on dark backgrounds. "
    "Screen glow, circuit-board luminescence, scanline overlay. "
    "Sharp pixels, blocky geometry, sprite-sheet animation energy. "
    "Warm retro color palette with neon accent glows."
)

STYLE_TRANSITION = (
    "Mixed transition style — Studio Ghibli illustration dissolving into 16-bit pixel art at edges. "
    "Reality pixelates at borders. Human world details break into visible pixels. "
    "The monitor/screen serves as portal between worlds. "
    "CRT hum aesthetic at the boundary."
)

# ---------------------------------------------------------------------------
# Art style map (page number → style)
# ---------------------------------------------------------------------------

ART_STYLE_MAP: dict[int, str] = {
    1: "ghibli",  # Front Cover (outside)
    2: "ghibli",  # Inside Front Cover (IFC)
    3: "ghibli",
    4: "ghibli",
    5: "ghibli",
    6: "ghibli",
    7: "transition",
    8: "pixel",
    9: "pixel",
    10: "pixel",
    11: "pixel",
    12: "pixel",
    13: "pixel",
    14: "mixed",
    15: "pixel",
    16: "pixel",
    17: "pixel",
    18: "mixed",
    19: "pixel",
    20: "pixel",
    21: "pixel",
    22: "mixed",
    23: "mixed",
    24: "mixed",
    25: "mixed",
    26: "mixed",
    27: "mixed",
    28: "ghibli",
    29: "ghibli",
    30: "mixed",
    31: "ghibli",  # Inside Back Cover (IBC)
    32: "ghibli",  # Back Cover (outside)
}

# ---------------------------------------------------------------------------
# Character constants
# ---------------------------------------------------------------------------

CHARACTER_STANLEY = (
    "Studio Ghibli-style young scientist. Spiky brown hair, lean mid-height build. "
    "White lab coat over purple turtleneck, black pants. 'STANLEY' name badge. "
    "Rayban Wayfarer frames with clear lenses (usually on, not always). "
    "Optional accessory: sometimes a black Peaky Blinders-style flat cap. "
    "Props: clipboard, coffee mug, scattered papers, occasionally safety goggles pushed up on forehead. "
    "Expression range: passionate lecturing, exhausted slumped-over, joyful discovery, wry humor. "
    "Animated posture — always in motion or deep in thought."
)

CHARACTER_AGENT_STANLEY = (
    "16-bit pixel art sprite character. Spiky brown pixel hair, white pixel lab coat "
    "over purple pixel turtleneck, black pixel pants. 32×48 pixel base size. "
    "Retro RPG aesthetic — idle bounce, sprite-sheet animation energy. "
    "Expressive within pixel constraints: confusion (floating ? marks), "
    "determination (glowing eyes), speed (ghost-trail multiples), "
    "comedy (exaggerated expressions). "
    "Environment: pixel laboratory with glowing screens, beakers, circuit-board floors."
)

CHARACTER_HELIX = (
    "Golden retriever, lab mascot. Warm, loyal presence. "
    "Sleeping, sitting, or walking alongside Science Stanley."
)

NEGATIVE_SUFFIX = (
    "No photorealism, no 3D rendering, no smooth gradients, no anime "
    "screentones, no watercolor, no bright white background, "
    "no legible real text, no readable words or letters, no typeset fonts, "
    "no OCR-readable characters, stylize any text as abstract glowing "
    "symbols or decorative runes, no speech bubble lettering rendered "
    "as real typography, no stethoscope, no medical equipment"
)

# Act-specific lighting modifiers
ACT_LIGHTING: dict[str, str] = {
    "cover": "neutral warm lighting, inviting atmosphere, neutral gray (#565f89) with golden (#e0af68) accents",
    "act_1": "cool cyan ambient lighting, screen glow, morning light, dominant cyan (#7dcfff) accents, discovery mood",
    "act_2": "neutral green-tinted lighting, productive workspace glow, afternoon light, dominant green (#9ece6a) accents, determined mood",
    "act_3": "warm purple ambient lighting, soft glow, evening warmth, dominant purple (#9d7cd8) accents, collaborative mood",
    "closing": "soft starlight ambient, contemplative mood, neutral gray (#565f89) accents, educational warmth",
}


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class PanelTypeTemplate:
    """Camera and composition strings for a panel type."""

    camera: str
    composition: str


@dataclass
class ActInfo:
    """Act metadata for a page."""

    name: str
    color_hex: str
    canvas_color: str | None
    label: str = ""


@dataclass
class SpreadColorScript:
    """Color script entry for a spread."""

    pages: tuple[int, int]
    act: str
    dominant: str
    accent: str
    lighting: str
    mood: str


@dataclass
class CharacterState:
    """State for a single character in a spread."""

    present: bool = False
    mood: str = ""
    props: list[str] = field(default_factory=list)
    glasses: bool | None = None
    cap: bool | None = None
    pose: str = ""


@dataclass
class StoryState:
    """Story state for a spread — dual protagonist tracking."""

    science_stanley: CharacterState
    agent_stanley: CharacterState
    helix: CharacterState
    world: str = ""


@dataclass
class PendingPanel:
    """Tracks a panel awaiting image generation."""

    panel_id: str
    prompt: str
    aspect_ratio: str
    target_path: str
    status: str = "pending"  # pending | resolved | failed


@dataclass
class Panel:
    """A single comic panel.

    ``compositional_nuance`` (M-V1-2-F-01 S4 / ADR-008 §D2 sub-dimension
    addendum): opt-in Layer-4 compositional nuance selector. When set to
    a nuance_id that exists in the panel's matching
    ``PANEL_TYPE_TEMPLATES[panel_type]["nuances"]`` dict, the camera
    block appends that nuance descriptor; otherwise inert (silent
    no-op). Substrate stays neutral — vocabulary is generic composition
    terms, not project-specific knowledge. Re-merge rationale:
    lattice-labs/who/coordination/coord_2026_04_16_forge_split.md.
    """

    id: str
    page_id: str
    row: int
    col: int
    span_rows: int = 1
    span_cols: int = 1
    bleed: bool = False
    panel_type: str = "action"
    x: float = 0.0
    y: float = 0.0
    width: float = 0.0
    height: float = 0.0
    aspect_ratio: str = "1:1"
    scene_description: str = ""
    camera_angle: str = ""
    characters: list[str] = field(default_factory=list)
    mood: str = ""
    spread_number: int | None = None
    balloon_space: str | None = None
    image_path: str | None = None
    node_id: str | None = None
    art_style: str = ""
    style_override: str | None = None
    compositional_nuance: str | None = None


@dataclass
class Page:
    """A comic page containing panels."""

    id: str
    page_number: int
    spread_number: int | None = None
    act: ActInfo | None = None
    color_script: SpreadColorScript | None = None
    story_state: StoryState | None = None
    art_style: str = ""
    panel_ids: list[str] = field(default_factory=list)
    group_id: str | None = None


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _get_act_for_page(page_number: int) -> ActInfo | None:
    """Return act info for a page number, or None if outside act ranges."""
    for act_name, info in ACT_PAGE_RANGES.items():
        start, end = info["pages"]
        if start <= page_number <= end:
            canvas_color = ACT_CANVAS_COLORS.get(act_name)
            return ActInfo(
                name=act_name,
                color_hex=info["color"],
                canvas_color=canvas_color,
                label=info["label"],
            )
    return None


def _get_spread_color_script(spread_number: int) -> SpreadColorScript | None:
    """Return color script for a spread number."""
    entry = SPREAD_COLOR_SCRIPT.get(spread_number)
    if entry:
        return SpreadColorScript(**entry)
    return None


def _get_story_state(spread_number: int) -> StoryState | None:
    """Return story state for a spread number."""
    entry = SPREAD_STORY_STATE.get(spread_number)
    if entry:
        return StoryState(
            science_stanley=CharacterState(**entry.get("science_stanley", {})),
            agent_stanley=CharacterState(**entry.get("agent_stanley", {})),
            helix=CharacterState(**entry.get("helix", {})),
            world=entry.get("world", ""),
        )
    return None


def _get_art_style_for_page(page_number: int) -> str:
    """Look up art style for a page number from ART_STYLE_MAP."""
    return ART_STYLE_MAP.get(page_number, "ghibli")


def _style_to_prefix(style: str) -> str:
    """Map art style name to style prefix string."""
    if style == "pixel":
        return STYLE_PIXEL
    elif style in ("transition", "mixed"):
        return STYLE_TRANSITION
    else:
        return STYLE_GHIBLI


def _get_style_prefix_for_page(page_number: int) -> str:
    """Get the style prefix string for a page number."""
    return _style_to_prefix(_get_art_style_for_page(page_number))


# ---------------------------------------------------------------------------
# ComicReport — review() output
# ---------------------------------------------------------------------------


def _comic_grade(score: float) -> str:
    """Convert 0.0-1.0 score to letter grade."""
    if score >= 0.9:
        return "A"
    elif score >= 0.8:
        return "B"
    elif score >= 0.7:
        return "C"
    elif score >= 0.6:
        return "D"
    return "F"


def _maybe_append_rlhf_hint(
    block: str,
    *,
    register: str | None,
    rlhf_hints: dict[str, str] | None,
) -> str:
    """Append RLHF hint as a parenthetical suffix when both kwargs resolve.

    M-V1-2-F-01 S3 / ADR-008 §D2 candidate B1 surface. Inert if
    ``register`` is None, ``rlhf_hints`` is None, the dict is empty for
    the normalized key, or the resolved hint is an empty string. This
    keeps the default-kwarg behavior identical to the S2 baseline.

    Register normalization mirrors ``canvas_core.rlhf.iii_bridge.
    _derive_pattern``: lowercase, then ``+``/``-``/`` `` → ``_``.
    """
    if register is None or not rlhf_hints:
        return block
    key = register.lower().replace("+", "_").replace("-", "_").replace(" ", "_")
    hint = rlhf_hints.get(key)
    if not hint:
        return block
    if not block:
        return f"(RLHF hint: {hint})"
    return f"{block} (RLHF hint: {hint})"


@dataclass
class ComicReport:
    """Scored quality report from ComicPageBuilder.review()."""

    score: float  # 0.0-1.0
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    pass_threshold: float = 0.85
    page_count: int = 0
    panel_count: int = 0
    structural_score: float = 0.0
    content_score: float = 0.0
    production_score: float = 0.0
    quality_score: float = 0.0

    @property
    def passed(self) -> bool:
        return self.score >= self.pass_threshold

    @property
    def grade(self) -> str:
        return _comic_grade(self.score)

    def __str__(self) -> str:
        return (
            f"ComicReport(score={self.score}, grade={self.grade}, "
            f"passed={self.passed}, pages={self.page_count}, "
            f"panels={self.panel_count}, issues={len(self.issues)})"
        )


# ---------------------------------------------------------------------------
# ComicPageBuilder
# ---------------------------------------------------------------------------


class ComicPageBuilder:
    """Build comic book pages and issues via CanvasBuilder composition.

    Uses print-spec coordinates (ComixWellspring standard), 6-layer prompt
    assembly, act-based color scripting, and decoupled image generation.
    """

    def __init__(
        self,
        name: str = "untitled_comic",
        version: str = "1.0.0",
        page_width: float = 6.625,
        page_height: float = 10.25,
        style: str = "pixel_art_ghibli",
        context_pack: ContextPack | None = None,
    ):
        self._cb = CanvasBuilder(name, version)
        self.page_width = page_width
        self.page_height = page_height
        self.style = style
        self.context_pack = context_pack
        self._pages: dict[str, Page] = {}
        self._panels: dict[str, Panel] = {}
        self._pending_panels: dict[str, PendingPanel] = {}
        self._page_order: list[str] = []

    # --- Page methods ---

    def add_page(self, page_number: int, spread_number: int | None = None) -> str:
        """Add a page. Auto-assigns act color, art style, and color script."""
        page_id = CanvasBuilder.generate_id()
        act = _get_act_for_page(page_number)
        art_style = _get_art_style_for_page(page_number)
        color_script = _get_spread_color_script(spread_number) if spread_number else None
        story_state = _get_story_state(spread_number) if spread_number else None

        page = Page(
            id=page_id,
            page_number=page_number,
            spread_number=spread_number,
            act=act,
            color_script=color_script,
            story_state=story_state,
            art_style=art_style,
        )
        self._pages[page_id] = page
        self._page_order.append(page_id)
        return page_id

    # --- Panel methods ---

    def add_panel(
        self,
        page_id: str,
        row: int,
        col: int,
        span_rows: int = 1,
        span_cols: int = 1,
        bleed: bool = False,
        panel_type: str = "action",
        balloon_space: str | None = None,
    ) -> str:
        """Add a panel to a page. Returns panel_id."""
        if page_id not in self._pages:
            raise ValueError(f"Unknown page_id: {page_id}")

        panel_id = CanvasBuilder.generate_id()
        x, y, w, h = self._grid_to_coords(row, col, span_rows, span_cols, bleed)
        aspect_ratio = self._auto_aspect_ratio(w, h, span_rows, span_cols, bleed)

        panel = Panel(
            id=panel_id,
            page_id=page_id,
            row=row,
            col=col,
            span_rows=span_rows,
            span_cols=span_cols,
            bleed=bleed,
            panel_type=panel_type,
            x=x,
            y=y,
            width=w,
            height=h,
            aspect_ratio=aspect_ratio,
            balloon_space=balloon_space,
        )
        self._panels[panel_id] = panel
        self._pages[page_id].panel_ids.append(panel_id)
        return panel_id

    def standard_grid(
        self, page_id: str, rows: int = 3, cols: int = 2, panel_type: str = "action"
    ) -> list[str]:
        """Create a standard grid of panels. Returns list of panel_ids."""
        panel_ids = []
        for r in range(rows):
            for c in range(cols):
                pid = self.add_panel(page_id, r, c, panel_type=panel_type)
                panel_ids.append(pid)
        return panel_ids

    def dynamic_layout(self, page_id: str, panel_specs: list[dict[str, Any]]) -> list[str]:
        """Create panels from a list of spec dicts. Returns panel_ids."""
        panel_ids = []
        for spec in panel_specs:
            pid = self.add_panel(
                page_id,
                row=spec.get("row", 0),
                col=spec.get("col", 0),
                span_rows=spec.get("span_rows", 1),
                span_cols=spec.get("span_cols", 1),
                bleed=spec.get("bleed", False),
                panel_type=spec.get("panel_type", "action"),
                balloon_space=spec.get("balloon_space"),
            )
            panel_ids.append(pid)
        return panel_ids

    def splash_page(self, page_id: str, panel_type: str = "splash") -> str:
        """Create a single full-page panel. Returns panel_id."""
        return self.add_panel(
            page_id,
            row=0,
            col=0,
            span_rows=3,
            span_cols=2,
            bleed=True,
            panel_type=panel_type,
        )

    def spread(self, left_page_id: str, right_page_id: str) -> str:
        """Create a two-page spread panel on the left page. Returns panel_id."""
        panel_id = CanvasBuilder.generate_id()
        x = 0.0
        y = 0.0
        w = BLEED_WIDTH * 2 + 25  # two pages + gutter
        h = BLEED_HEIGHT

        panel = Panel(
            id=panel_id,
            page_id=left_page_id,
            row=0,
            col=0,
            span_rows=3,
            span_cols=2,
            bleed=True,
            panel_type="splash",
            x=x,
            y=y,
            width=w,
            height=h,
            aspect_ratio="4:3",
        )
        self._panels[panel_id] = panel
        self._pages[left_page_id].panel_ids.append(panel_id)
        self._pages[right_page_id].panel_ids.append(panel_id)
        return panel_id

    # --- Coordinate calculation ---

    def _grid_to_coords(
        self, row: int, col: int, span_rows: int, span_cols: int, bleed: bool
    ) -> tuple[float, float, float, float]:
        """Convert grid position to canvas coordinates (x, y, w, h)."""
        if bleed and span_rows >= 3 and span_cols >= 2:
            return (0.0, 0.0, BLEED_WIDTH, BLEED_HEIGHT)

        # Standard 2-col, 3-row grid within safe area
        cols = 2
        rows = 3
        col_width = (SAFE_WIDTH - (cols - 1) * PANEL_GUTTER) / cols
        row_height = (SAFE_HEIGHT - (rows - 1) * PANEL_GUTTER) / rows

        x = SAFE_ORIGIN_X + col * (col_width + PANEL_GUTTER)
        y = SAFE_ORIGIN_Y + row * (row_height + PANEL_GUTTER)
        w = col_width * span_cols + PANEL_GUTTER * (span_cols - 1)
        h = row_height * span_rows + PANEL_GUTTER * (span_rows - 1)

        return (round(x, 2), round(y, 2), round(w, 2), round(h, 2))

    def _auto_aspect_ratio(
        self, width: float, height: float, span_rows: int, span_cols: int, bleed: bool
    ) -> str:
        """Determine aspect ratio from panel dimensions."""
        if bleed and span_rows >= 3 and span_cols >= 2:
            return ASPECT_RATIOS["full_page"]

        ratio = width / height if height > 0 else 1.0
        if ratio > 1.5:
            return ASPECT_RATIOS["wide"]
        elif ratio < 0.7:
            return ASPECT_RATIOS["tall"]
        else:
            return ASPECT_RATIOS["standard"]

    # --- Content / prompt methods ---

    def set_panel_content(
        self,
        panel_id: str,
        scene_description: str,
        camera_angle: str = "",
        panel_type: str | None = None,
        characters: list[str] | None = None,
        mood: str = "",
        spread_number: int | None = None,
        style_override: str | None = None,
        compositional_nuance: str | None = None,
    ) -> None:
        """Set content for a panel. Auto-populates story state when spread_number set."""
        panel = self._panels.get(panel_id)
        if not panel:
            raise ValueError(f"Unknown panel_id: {panel_id}")

        panel.scene_description = scene_description
        panel.camera_angle = camera_angle
        if panel_type:
            panel.panel_type = panel_type
        if characters is not None:
            panel.characters = characters
        panel.mood = mood
        if spread_number is not None:
            panel.spread_number = spread_number
        if style_override is not None:
            panel.style_override = style_override
        if compositional_nuance is not None:
            panel.compositional_nuance = compositional_nuance

    def generate_panel_prompt(
        self,
        panel_id: str,
        *,
        context_pack: ContextPack,
        character_registry: dict[str, str] | None = None,
        register: str | None = None,
        rlhf_character_hints: dict[str, str] | None = None,
        rlhf_camera_nuances: dict[str, str] | None = None,
    ) -> ImagePrompt:
        """Generate a 6-layer dual-prompt for a panel.

        M-R2-02 upgrade (per spec § 7.3): keyword-only ``context_pack`` is
        required (F-38 closure — caller cannot invoke without it). Return
        type changed from ``{text_prompt, aspect_ratio}`` dict to the
        substrate-neutral ``ImagePrompt`` dataclass. The 6-layer assembly
        logic is preserved verbatim — only the entry-validation and
        return-shape change.

        The ``mermaid_layout`` field is set to ``None`` for v1.0 single-prompt
        path; the structural-state→PanelLayout transform that produces a
        non-None ``mermaid_layout`` lands at S3 integration smoke.

        ``character_registry`` (M-V1-2-F-01 S2 / ADR-008 §D2 candidate B2,
        caller-supplied registry): optional ``dict[char_name_lower, descriptor]``
        that the Layer-2 character block consults BEFORE the hardcoded
        defaults. Application-layer wrappers may supply project-specific
        character descriptors (e.g., from a Visual-DNA bundle at
        ``ScienceStanley.aDNA/what/visual_dna/characters/<name>/<name>.yaml``)
        without the substrate carrying brand-specific knowledge. When the
        override matches a known story-state character (Stanley / Agent
        Stanley / Helix), the story-state mood/pose suffix still merges onto
        the overridden descriptor. Unknown characters present in the registry
        inject the registry descriptor instead of the raw-name fallback.
        Default ``None`` preserves all existing call-site behavior.

        ``register`` + ``rlhf_character_hints`` + ``rlhf_camera_nuances``
        (M-V1-2-F-01 S3 / ADR-008 §D2 candidate B1, RLHF-derived hints):
        opt-in tuning channel for the Layer-2 character block and Layer-4
        camera block. ``register`` is the voice-register identifier (e.g.,
        ``"R7"``, ``"R11+R3"``) that keys into per-register hint dicts;
        normalization mirrors ``canvas_core.rlhf.iii_bridge._derive_pattern``
        (lowercase + ``+``/``-``/`` `` → ``_``). When ``register`` is None,
        no hints apply (the kwargs are inert). When ``register`` is provided
        and the matching hint kwarg dict has a non-empty entry for the
        normalized key, the hint text is appended as a parenthetical
        suffix to the corresponding builder's output. Callers wishing to
        consume the bridged learning store's module-load constants pass
        ``rlhf_character_hints=RLHF_CHARACTER_HINTS`` and
        ``rlhf_camera_nuances=RLHF_CAMERA_NUANCES`` from
        ``canvas_comic._rlhf_hints``. All three default to ``None``,
        preserving all existing call-site behavior.

        Raises:
            ValueError: panel_id unknown.
            ContextNotLoaded: any ``context_pack`` path missing or unreadable.
        """
        panel = self._panels.get(panel_id)
        if not panel:
            raise ValueError(f"Unknown panel_id: {panel_id}")

        # F-38 pre-flight: every ContextPack path must exist
        for field_name in (
            "storyboard_canvas",
            "character_bible",
            "color_theory",
            "prompt_engineering",
            "voice_foundations",
        ):
            path = getattr(context_pack, field_name)
            if not path.exists():
                raise ContextNotLoaded(
                    f"context_pack.{field_name} missing: {path}"
                )

        page = self._pages.get(panel.page_id)
        layers = []

        # Layer 1: Style prefix (page-specific, with panel override)
        if panel.style_override:
            layers.append(_style_to_prefix(panel.style_override))
        elif page and page.art_style:
            layers.append(_style_to_prefix(page.art_style))
        else:
            layers.append(STYLE_GHIBLI)

        # Layer 2: Character block
        char_block = self._build_character_block(
            panel,
            character_registry=character_registry,
            register=register,
            rlhf_hints=rlhf_character_hints,
        )
        if char_block:
            layers.append(char_block)

        # Layer 3: Scene/environment
        if panel.scene_description:
            layers.append(panel.scene_description)

        # Layer 4: Camera/composition
        camera_block = self._build_camera_block(
            panel,
            register=register,
            rlhf_hints=rlhf_camera_nuances,
        )
        layers.append(camera_block)

        # Layer 5: Lighting/mood
        lighting_block = self._build_lighting_block(panel, page)
        layers.append(lighting_block)

        # Layer 6: Negative suffix
        layers.append(NEGATIVE_SUFFIX)

        text_prompt = "\n\n".join(layers)
        return ImagePrompt(
            text=text_prompt,
            mermaid_layout=None,
            aspect_ratio=panel.aspect_ratio,
        )

    def _build_character_block(
        self,
        panel: Panel,
        *,
        character_registry: dict[str, str] | None = None,
        register: str | None = None,
        rlhf_hints: dict[str, str] | None = None,
    ) -> str:
        """Build Layer 2 character block with story state merge.

        ``character_registry`` (optional) overrides the hardcoded character
        descriptors per ADR-008 §D2 (caller-supplied registry pattern). Keys
        match ``char_name.lower()``. Story-state mood/pose merge still applies
        on top of the overridden descriptor for the three known story-state
        characters; unknown characters in the registry inject the registry
        descriptor instead of the raw-name fallback.

        ``register`` + ``rlhf_hints`` (M-V1-2-F-01 S3 / ADR-008 §D2
        candidate B1 surface): opt-in RLHF-derived character-block hint.
        When ``register`` is non-None and ``rlhf_hints`` has an entry for
        the normalized key (lowercase + ``+``/``-``/`` `` → ``_``), the
        hint text is appended as a parenthetical suffix to the final
        character block. ``register=None`` OR ``rlhf_hints=None`` makes
        the kwargs inert (S2-baseline behavior preserved).
        """
        parts = []
        story_state = None
        if panel.spread_number:
            story_state = _get_story_state(panel.spread_number)

        for char_name in panel.characters:
            char_lower = char_name.lower()
            override = (
                character_registry.get(char_lower) if character_registry else None
            )
            if char_lower == "stanley":
                desc = override if override is not None else CHARACTER_STANLEY
                if story_state and story_state.science_stanley.present:
                    cs = story_state.science_stanley
                    if cs.mood:
                        desc += f", {cs.mood}"
                parts.append(desc)
            elif char_lower == "agent_stanley":
                desc = override if override is not None else CHARACTER_AGENT_STANLEY
                if story_state and story_state.agent_stanley.present:
                    cs = story_state.agent_stanley
                    if cs.mood:
                        desc += f", {cs.mood}"
                    if cs.pose:
                        desc += f", {cs.pose}"
                parts.append(desc)
            elif char_lower == "helix":
                desc = override if override is not None else CHARACTER_HELIX
                if story_state and story_state.helix.present:
                    cs = story_state.helix
                    if cs.pose:
                        desc += f", {cs.pose}"
                parts.append(desc)
            elif override is not None:
                parts.append(override)
            else:
                parts.append(char_name)

        block = ". ".join(parts) if parts else ""
        block = _maybe_append_rlhf_hint(block, register=register, rlhf_hints=rlhf_hints)
        return block

    def _build_camera_block(
        self,
        panel: Panel,
        *,
        register: str | None = None,
        rlhf_hints: dict[str, str] | None = None,
    ) -> str:
        """Build Layer 4 camera block with Wally Wood keywords + balloon space.

        ``register`` + ``rlhf_hints`` (M-V1-2-F-01 S3 / ADR-008 §D2
        candidate B1 surface): opt-in RLHF-derived camera-block nuance.
        Same semantics as ``_build_character_block``: inert when either
        kwarg is None or the normalized register key is absent from the
        hint dict; otherwise the hint text is appended as a parenthetical
        suffix to the final camera block.

        ``panel.compositional_nuance`` (M-V1-2-F-01 S4 / ADR-008 §D2
        sub-dimension addendum): opt-in template-scoped composition
        nuance. When set to a nuance_id that exists in the matching
        ``PANEL_TYPE_TEMPLATES[panel.panel_type]["nuances"]`` dict, the
        nuance descriptor is appended to the camera block as a
        parenthetical suffix. Silent no-op when the field is None or the
        key is absent — re-baseline gate guarantee. Seed entries
        provenance: III learning store ``pick_reason`` corpus (per
        PANEL_TYPE_TEMPLATES header). Re-merge rationale:
        lattice-labs/who/coordination/coord_2026_04_16_forge_split.md.
        """
        parts = []

        # Panel type template
        template = PANEL_TYPE_TEMPLATES.get(panel.panel_type)
        if panel.camera_angle:
            parts.append(panel.camera_angle)
        elif template:
            parts.append(template["camera"])

        # Wally Wood keywords
        wood_keywords = self._map_panel_type_to_wood(
            panel.panel_type, span_cols=panel.span_cols, span_rows=panel.span_rows
        )
        if wood_keywords:
            parts.append(wood_keywords)

        # Balloon space
        if panel.balloon_space:
            parts.append(f"Composition with clear space in {panel.balloon_space} for text overlay.")

        block = " ".join(parts)

        # Compositional nuance (S4 §D2 sub-dimension addendum): inert
        # unless panel.compositional_nuance is set AND keys into the
        # matching template's nuances dict.
        if panel.compositional_nuance is not None and template:
            nuance_text = template.get("nuances", {}).get(panel.compositional_nuance)
            if nuance_text:
                block = f"{block} (compositional nuance: {nuance_text})"

        block = _maybe_append_rlhf_hint(block, register=register, rlhf_hints=rlhf_hints)
        return block

    def _build_lighting_block(self, panel: Panel, page: Page | None) -> str:
        """Build Layer 5 lighting block with spread color script priority.

        When a spread color script exists for this panel's spread, its
        ``lighting`` key and ``dominant`` hex are used as the primary
        lighting descriptor.  ACT_LIGHTING falls back only when no spread
        color script is present — this eliminates warm/cyan tension (e.g.,
        spread 2 warm amber vs act_1 cyan ambient).
        """
        parts = []

        # Panel mood
        if panel.mood:
            parts.append(panel.mood)

        # Resolve color script (spread-level lighting takes priority)
        color_script = None
        if page and page.color_script:
            color_script = page.color_script
        elif panel.spread_number:
            color_script = _get_spread_color_script(panel.spread_number)

        if color_script:
            # Spread color script lighting is primary — replaces ACT_LIGHTING
            parts.append(f"{color_script.lighting} lighting, dominant {color_script.dominant}")
            parts.append(f"Mood: {color_script.mood}")
        else:
            # Fallback to act-level lighting when no spread script
            act_name = None
            if page and page.act:
                act_name = page.act.name
            elif panel.spread_number:
                spread_entry = SPREAD_COLOR_SCRIPT.get(panel.spread_number)
                if spread_entry:
                    act_name = spread_entry["act"]

            if act_name and act_name in ACT_LIGHTING:
                parts.append(ACT_LIGHTING[act_name])

        return ". ".join(parts) if parts else "ambient lighting"

    @staticmethod
    def _map_panel_type_to_wood(
        panel_type: str,
        span_cols: int = 1,
        span_rows: int = 1,
    ) -> str:
        """Map panel type to Wally Wood keyword string.

        For action panels spanning multiple columns or rows, uses the
        ``action_sequence`` variant which allows multi-pose progression.
        Single-cell action panels use ``action`` (single decisive moment)
        to avoid sprite-sheet rendering artifacts.
        """
        if panel_type == "action" and (span_cols > 1 or span_rows > 1):
            return WOOD_KEYWORDS.get("action_sequence", WOOD_KEYWORDS.get("action", ""))
        return WOOD_KEYWORDS.get(panel_type, "")

    # --- Image generation interface (Option A — prompts only) ---

    def prepare_panel_generation(self, panel_id: str) -> PendingPanel:
        """Prepare a panel for image generation. Returns PendingPanel.

        M-R2-02: requires ``self.context_pack`` to be set (via constructor
        kwarg or attribute assignment). Raises :class:`ContextNotLoaded`
        otherwise. The panel-prompt generation now returns an
        :class:`ImagePrompt`; ``.text`` is forwarded as the prompt str on
        the PendingPanel record.
        """
        panel = self._panels.get(panel_id)
        if not panel:
            raise ValueError(f"Unknown panel_id: {panel_id}")
        if self.context_pack is None:
            raise ContextNotLoaded(
                "context_pack not set on builder; pass context_pack= to "
                "ComicPageBuilder() or assign builder.context_pack before "
                "calling prepare_panel_generation()."
            )

        image_prompt = self.generate_panel_prompt(
            panel_id, context_pack=self.context_pack
        )
        target_path = f"how/presentations/{self._cb.name}/images/panel_{panel_id}.png"

        pending = PendingPanel(
            panel_id=panel_id,
            prompt=image_prompt.text,
            aspect_ratio=image_prompt.aspect_ratio,
            target_path=target_path,
        )
        self._pending_panels[panel_id] = pending
        return pending

    def resolve_panel(self, panel_id: str, image_path: str) -> None:
        """Mark a panel as resolved with an image path."""
        panel = self._panels.get(panel_id)
        if not panel:
            raise ValueError(f"Unknown panel_id: {panel_id}")

        panel.image_path = image_path
        pending = self._pending_panels.get(panel_id)
        if pending:
            pending.status = "resolved"

    @property
    def pending_panels(self) -> list[PendingPanel]:
        """List of unresolved PendingPanel records."""
        return [p for p in self._pending_panels.values() if p.status == "pending"]

    def prepare_all_panels(self) -> list[PendingPanel]:
        """Prepare all panels for generation. Returns list of PendingPanels."""
        results = []
        for panel_id in self._panels:
            panel = self._panels[panel_id]
            if panel.scene_description:
                pending = self.prepare_panel_generation(panel_id)
                results.append(pending)
        return results

    # --- Variant selection ---

    def generate_panel_variants(
        self,
        panel_id: str,
        variant_paths: list[str],
        variant_labels: list[str] | None = None,
    ) -> CanvasBuilder:
        """Create a selection board for panel variants."""
        panel = self._panels.get(panel_id)
        if not panel:
            raise ValueError(f"Unknown panel_id: {panel_id}")

        variants = [{"id": CanvasBuilder.generate_id(), "file": path} for path in variant_paths]
        labels = variant_labels or [f"Variant {i + 1}" for i in range(len(variant_paths))]

        return self._cb.selection_board(
            variants=variants,
            labels=labels,
            title=f"Panel {panel_id} — Variant Selection",
        )

    def regenerate_panel(self, panel_id: str, prompt_override: str | None = None) -> PendingPanel:
        """Re-prepare a panel for generation, optionally with a new prompt."""
        panel = self._panels.get(panel_id)
        if not panel:
            raise ValueError(f"Unknown panel_id: {panel_id}")

        panel.image_path = None
        if panel_id in self._pending_panels:
            del self._pending_panels[panel_id]

        if prompt_override:
            target_path = f"how/presentations/{self._cb.name}/images/panel_{panel_id}.png"
            pending = PendingPanel(
                panel_id=panel_id,
                prompt=prompt_override,
                aspect_ratio=panel.aspect_ratio,
                target_path=target_path,
            )
            self._pending_panels[panel_id] = pending
            return pending

        return self.prepare_panel_generation(panel_id)

    def regenerate_all(self, style_override: str | None = None) -> list[PendingPanel]:
        """Re-prepare all panels. Optionally override style prefix."""
        results = []
        for panel_id, panel in self._panels.items():
            if panel.scene_description:
                panel.image_path = None
                if panel_id in self._pending_panels:
                    del self._pending_panels[panel_id]

                if style_override:
                    if self.context_pack is None:
                        raise ContextNotLoaded(
                            "context_pack not set on builder; pass "
                            "context_pack= to ComicPageBuilder() or assign "
                            "builder.context_pack before calling "
                            "regenerate_all(style_override=...)."
                        )
                    image_prompt = self.generate_panel_prompt(
                        panel_id, context_pack=self.context_pack
                    )
                    # Replace the page-specific style prefix (first layer)
                    text = image_prompt.text
                    first_break = text.find("\n\n")
                    if first_break > 0:
                        modified_prompt = style_override + text[first_break:]
                    else:
                        modified_prompt = style_override
                    target_path = f"how/presentations/{self._cb.name}/images/panel_{panel_id}.png"
                    pending = PendingPanel(
                        panel_id=panel_id,
                        prompt=modified_prompt,
                        aspect_ratio=image_prompt.aspect_ratio,
                        target_path=target_path,
                    )
                    self._pending_panels[panel_id] = pending
                else:
                    pending = self.prepare_panel_generation(panel_id)
                results.append(pending)
        return results

    # --- Spread assignment ---

    def set_spread(self, page_id: str, spread_number: int) -> None:
        """Assign a spread number to a page, applying color script and story state."""
        page = self._pages.get(page_id)
        if not page:
            raise ValueError(f"Unknown page_id: {page_id}")

        page.spread_number = spread_number
        page.color_script = _get_spread_color_script(spread_number)
        page.story_state = _get_story_state(spread_number)

        # Update panels on this page
        for panel_id in page.panel_ids:
            panel = self._panels.get(panel_id)
            if panel:
                panel.spread_number = spread_number

    # --- Issue assembly ---

    def build_issue_canvas(self, page_gap: float = 600) -> dict:
        """Build the complete issue canvas with page groups and navigation.

        Args:
            page_gap: Gap between pages in canvas units. Use 600+ for
                presentation mode (one page at a time); 100 for compact view.
        """
        page_spacing = TRIM_WIDTH + page_gap

        for i, page_id in enumerate(self._page_order):
            page = self._pages[page_id]
            page_x = i * page_spacing
            page_y = 0.0

            # Page group node
            act_color = page.act.canvas_color if page.act else None
            label = f"Page {page.page_number}"
            if page.act:
                label += f" ({page.act.label or page.act.name})"

            group_id = CanvasBuilder.generate_id()
            self._cb.add_group(
                id=group_id,
                label=label,
                x=page_x,
                y=page_y,
                width=TRIM_WIDTH,
                height=TRIM_HEIGHT,
                color=act_color,
                is_start_node=(i == 0),
            )
            page.group_id = group_id

            # Panel nodes within page group
            for panel_id in page.panel_ids:
                panel = self._panels[panel_id]
                node_x = page_x + panel.x
                node_y = page_y + panel.y

                node_id = CanvasBuilder.generate_id()
                panel.node_id = node_id

                if panel.image_path:
                    self._cb.add_file_node(
                        id=node_id,
                        file=panel.image_path,
                        x=node_x,
                        y=node_y,
                        width=panel.width,
                        height=panel.height,
                    )
                else:
                    # Placeholder text node
                    text = f"**Panel {panel.panel_type}**\n\n"
                    if panel.scene_description:
                        text += panel.scene_description[:200]
                    else:
                        text += f"[{panel.panel_type} panel — no content set]"

                    self._cb.add_text_node(
                        id=node_id,
                        text=text,
                        x=node_x,
                        y=node_y,
                        width=panel.width,
                        height=panel.height,
                    )

        # Navigation edges between pages
        for i in range(len(self._page_order) - 1):
            from_page = self._pages[self._page_order[i]]
            to_page = self._pages[self._page_order[i + 1]]
            if from_page.group_id and to_page.group_id:
                self._cb.add_edge(
                    id=CanvasBuilder.generate_id(),
                    from_node=from_page.group_id,
                    to_node=to_page.group_id,
                    from_side="right",
                    to_side="left",
                )

        # Metadata
        self._cb._reserved.update(
            {
                "generator": "ComicPageBuilder",
                "version": "1.0.0",
                "page_count": len(self._pages),
                "panel_count": len(self._panels),
                "style": self.style,
            }
        )

        return self._cb.build()

    def build(self) -> dict:
        """Build the canvas JSON dict."""
        return self.build_issue_canvas()

    def save(self, path: str | Path) -> Path:
        """Save the comic canvas to a file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        canvas = self.build()
        path.write_text(json.dumps(canvas, indent=2) + "\n")
        return path

    def validate(self) -> list[str]:
        """Validate the underlying canvas."""
        errors = []

        # Check all pages have panels
        for _page_id, page in self._pages.items():
            if not page.panel_ids:
                errors.append(f"Page {page.page_number} has no panels")

        # Check all panels with content have scene descriptions
        for panel_id, panel in self._panels.items():
            if panel.image_path and not panel.scene_description:
                errors.append(f"Panel {panel_id} has image but no scene description")

        # Delegate to CanvasBuilder validation after building
        if self._cb.nodes:
            errors.extend(self._cb.validate())

        return errors

    # --- Accessors ---

    @property
    def pages(self) -> list[Page]:
        """Read-only list of pages in order."""
        return [self._pages[pid] for pid in self._page_order]

    @property
    def panels(self) -> list[Panel]:
        """Read-only list of all panels."""
        return list(self._panels.values())

    def get_panel(self, panel_id: str) -> Panel | None:
        """Get a panel by ID."""
        return self._panels.get(panel_id)

    def get_page(self, page_id: str) -> Page | None:
        """Get a page by ID."""
        return self._pages.get(page_id)

    # --- Review & Structural Scoring (M07) ---

    def _apply_structural_fixes(self) -> None:
        """Apply idempotent structural fixes before scoring.

        Safe to call multiple times. Ensures the canvas is in a consistent
        state so review() reports steady-state quality, not transient gaps.
        """
        if not self._pages:
            return

        # Ensure all pages have group_id assigned (needed for navigation)
        for page in self.pages:
            if page.group_id is None and self._cb.nodes:
                # Try to find a matching group node
                for node in self._cb.nodes:
                    if node.get("type") == "group" and node.get("label", "").startswith(f"Page {page.page_number}"):
                        page.group_id = node["id"]
                        break

    def review(self) -> ComicReport:
        """Review comic quality across structural, content, and production categories.

        Applies structural fixes first (idempotent), then scores.
        Returns a ComicReport with score, grade, issues, and suggestions.
        """
        self._apply_structural_fixes()

        issues: list[str] = []
        suggestions: list[str] = []

        # --- Structural scoring ---
        page_count = len(self._pages)
        panel_count = len(self._panels)

        # S1: Page count (target: 28-34 for standard issue)
        if page_count == 0:
            s1 = 0.0
            issues.append("No pages in comic")
        elif 28 <= page_count <= 34:
            s1 = 1.0
        elif 20 <= page_count < 28 or 34 < page_count <= 40:
            s1 = 0.8
        elif 10 <= page_count < 20:
            s1 = 0.6
            issues.append(f"Low page count: {page_count} (target 28-34)")
        else:
            s1 = 0.4
            issues.append(f"Page count {page_count} outside expected range (target 28-34)")

        # S2: Panel coverage (all pages should have at least 1 panel)
        pages_without_panels = [p for p in self.pages if not p.panel_ids]
        if page_count > 0:
            s2 = 1.0 - (len(pages_without_panels) / page_count)
        else:
            s2 = 0.0
        for p in pages_without_panels:
            issues.append(f"Page {p.page_number} has no panels")

        # S3: Panel type variety (not all same type)
        panel_types = {p.panel_type for p in self.panels if p.panel_type}
        if panel_count == 0:
            s3 = 0.0
        elif len(panel_types) >= 4:
            s3 = 1.0
        elif len(panel_types) >= 2:
            s3 = 0.8
        else:
            s3 = 0.5
            suggestions.append("Add more panel type variety (action, dialogue, establishing, close_up)")

        # S4: Scene description coverage
        panels_with_desc = sum(1 for p in self.panels if p.scene_description)
        if panel_count > 0:
            s4 = panels_with_desc / panel_count
        else:
            s4 = 0.0
        missing_desc = panel_count - panels_with_desc
        if missing_desc > 0:
            issues.append(f"{missing_desc} panel(s) missing scene descriptions")

        structural_score = statistics.mean([s1, s2, s3, s4]) if page_count > 0 else 0.0

        # --- Content scoring ---
        # C1: Character assignment coverage
        panels_with_chars = sum(1 for p in self.panels if p.characters)
        if panel_count > 0:
            c1 = min(1.0, panels_with_chars / max(1, panel_count * 0.7))
        else:
            c1 = 0.0

        # C2: Camera angle coverage
        panels_with_camera = sum(1 for p in self.panels if p.camera_angle)
        if panel_count > 0:
            c2 = panels_with_camera / panel_count
        else:
            c2 = 0.0
        if c2 < 0.8:
            suggestions.append("Assign camera angles to more panels for visual variety")

        # C3: Art style consistency
        styles_used = {p.art_style for p in self.panels if p.art_style} | {self.style}
        c3 = 1.0 if len(styles_used) <= 2 else 0.7

        content_score = statistics.mean([c1, c2, c3]) if panel_count > 0 else 0.0

        # --- Production scoring ---
        # P1: Pending panel resolution
        pending = [p for p in self._pending_panels.values() if p.status == "pending"]
        resolved = [p for p in self._pending_panels.values() if p.status == "resolved"]
        total_pending = len(pending) + len(resolved)
        if total_pending > 0:
            p1 = len(resolved) / total_pending
        else:
            p1 = 1.0 if panel_count == 0 else 0.0
        if pending:
            issues.append(f"{len(pending)} pending panel(s) unresolved")

        # P2: Image readiness
        panels_with_image = sum(1 for p in self.panels if p.image_path)
        if panel_count > 0:
            p2 = panels_with_image / panel_count
        else:
            p2 = 0.0

        production_score = statistics.mean([p1, p2]) if panel_count > 0 else 0.0

        # --- Quality scoring (M-2b-04) ---
        # Q1: Prompt completeness (all 6 layers populated)
        if panel_count > 0:
            complete = 0
            for p in self.panels:
                has_scene = bool(p.scene_description)
                has_camera = bool(p.camera_angle) or p.panel_type in PANEL_TYPE_TEMPLATES
                has_chars = bool(p.characters)
                has_style = bool(p.art_style or p.style_override)
                if has_scene and has_camera and has_chars and has_style:
                    complete += 1
            q1 = complete / panel_count
        else:
            q1 = 0.0
        if q1 < 0.7:
            suggestions.append("Populate scene + camera + characters + style on more panels")

        # Q2: Story state coverage (pages with spread_number assigned)
        content_pages = [p for p in self.pages if p.page_number >= 3 and p.page_number <= 30]
        if content_pages:
            q2 = sum(1 for p in content_pages if p.spread_number is not None) / len(content_pages)
        else:
            q2 = 0.0
        if q2 < 0.8:
            suggestions.append("Assign spread numbers to more content pages for story state tracking")

        # Q3: Color script continuity (no gaps in spread sequence)
        if page_count > 0:
            spread_nums = sorted({p.spread_number for p in self.pages if p.spread_number})
            if spread_nums:
                expected = set(range(spread_nums[0], spread_nums[-1] + 1))
                q3 = len(set(spread_nums) & expected) / len(expected) if expected else 1.0
            else:
                q3 = 0.0
        else:
            q3 = 0.0

        # Q4: Character presence balance (≥70% of content pages)
        if content_pages:
            pages_with_chars = sum(
                1 for p in content_pages
                if any(self._panels[pid].characters for pid in p.panel_ids if pid in self._panels)
            )
            q4 = min(1.0, pages_with_chars / (len(content_pages) * 0.7)) if content_pages else 0.0
        else:
            q4 = 0.0

        quality_score = statistics.mean([q1, q2, q3, q4]) if page_count > 0 else 0.0

        # --- Aggregate ---
        # Weights: structural 30%, content 25%, production 25%, quality 20%
        if page_count > 0:
            score = (
                structural_score * 0.30
                + content_score * 0.25
                + production_score * 0.25
                + quality_score * 0.20
            )
        else:
            score = 0.0

        return ComicReport(
            score=round(score, 2),
            issues=issues,
            suggestions=suggestions,
            page_count=page_count,
            panel_count=panel_count,
            structural_score=round(structural_score, 2),
            content_score=round(content_score, 2),
            production_score=round(production_score, 2),
            quality_score=round(quality_score, 2),
        )

    def __repr__(self) -> str:
        return (
            f"ComicPageBuilder({self._cb.name!r}, "
            f"pages={len(self._pages)}, "
            f"panels={len(self._panels)}, "
            f"style={self.style!r})"
        )


# ---------------------------------------------------------------------------
# ComicProductionAdapter — lattice node → ComicPageBuilder wiring (M12b)
# ---------------------------------------------------------------------------


@dataclass
class StageResult:
    """Result of executing a pipeline stage."""

    stage: str
    success: bool
    output_path: str | None = None
    errors: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


class ComicProductionAdapter:
    """Map lattice nodes to ComicPageBuilder method call sequences.

    Orchestration glue for Design B (agentic flow). Each ``execute_*`` method
    corresponds to a node in ``lattice_comic_production`` and handles:
    - Reading inputs from the pipeline stage directory
    - Calling the appropriate ComicPageBuilder methods
    - Writing outputs to the next stage directory

    The conditional rework loop (quality_review → prompt_generation) is
    supported via ``execute_prompt_generation`` accepting a ``rework_list``.
    """

    STAGES = (
        "01_brief",
        "02_storyboard",
        "03_layout",
        "04_prompts",
        "05_generate",
        "06_review",
        "07_final",
    )

    def __init__(
        self,
        cpb: ComicPageBuilder,
        pipeline_root: str | Path,
    ) -> None:
        self.cpb = cpb
        self.pipeline_root = Path(pipeline_root)

    def _stage_dir(self, stage: str) -> Path:
        """Return the pipeline stage directory, creating it if needed."""
        d = self.pipeline_root / stage
        d.mkdir(parents=True, exist_ok=True)
        return d

    # --- Stage executors ---

    def execute_story_bible(
        self,
        storyboard_data: dict[str, Any],
    ) -> StageResult:
        """Node: story_bible — extract act structure from storyboard data.

        Parameters
        ----------
        storyboard_data:
            Dict with keys ``pages`` (list of page dicts) and optional
            ``spreads`` (spread mapping). Typically parsed from a storyboard
            canvas file externally.

        Returns
        -------
        StageResult with output_path to the generated story bible markdown.
        """
        out_dir = self._stage_dir("01_brief")
        pages = storyboard_data.get("pages", [])
        spreads = storyboard_data.get("spreads", {})

        lines = ["# Story Bible\n"]
        lines.append(f"**Issue**: {self.cpb._cb.name}\n")
        lines.append(f"**Pages**: {len(pages)}\n")
        lines.append(f"**Spreads**: {len(spreads)}\n\n")

        # Act structure
        lines.append("## Act Structure\n")
        lines.append("| Act | Pages | Color | Art Style |\n")
        lines.append("|-----|-------|-------|-----------|\n")
        for act_name, act_info in ACT_PAGE_RANGES.items():
            start, end = act_info["pages"]
            color = ACT_CANVAS_COLORS.get(act_name, "—")
            styles = {ART_STYLE_MAP.get(p, "unknown") for p in range(start, end + 1)}
            lines.append(
                f"| {act_name} | {start}-{end} | {color or '—'} | {', '.join(sorted(styles))} |\n"
            )

        # Spread color script
        lines.append("\n## Spread Color Script\n")
        lines.append("| Spread | Pages | Dominant | Accent | Mood |\n")
        lines.append("|--------|-------|----------|--------|------|\n")
        for spread_num in range(1, TOTAL_SPREADS + 1):
            sc = _get_spread_color_script(spread_num)
            if sc:
                lines.append(
                    f"| {spread_num} | {sc.pages[0]}-{sc.pages[1]} "
                    f"| {sc.dominant} | {sc.accent} | {sc.mood} |\n"
                )

        # Character inventory
        lines.append("\n## Character Inventory\n")
        lines.append("| Spread | Science Stanley | Agent Stanley | Helix | World |\n")
        lines.append("|--------|----------------|---------------|-------|-------|\n")
        for spread_num in range(1, TOTAL_SPREADS + 1):
            ss = _get_story_state(spread_num)
            if ss:
                sci = "Yes" if ss.science_stanley.present else "—"
                agt = "Yes" if ss.agent_stanley.present else "—"
                hlx = "Yes" if ss.helix.present else "—"
                lines.append(f"| {spread_num} | {sci} | {agt} | {hlx} | {ss.world} |\n")

        bible_path = out_dir / "story_bible.md"
        bible_path.write_text("".join(lines))
        return StageResult(
            stage="story_bible",
            success=True,
            output_path=str(bible_path),
        )

    def execute_panel_layout(
        self,
        page_specs: list[dict[str, Any]],
    ) -> StageResult:
        """Node: panel_layout — create panel grids from page specifications.

        Parameters
        ----------
        page_specs:
            List of dicts, each with ``page_number``, ``spread_number``,
            ``layout_type`` (``"grid"``, ``"dynamic"``, ``"splash"``,
            ``"spread"``), and layout-specific params (``rows``, ``cols``,
            ``panel_specs``, ``panel_type``).

        Returns
        -------
        StageResult with metadata containing page_ids and panel_ids.
        """
        out_dir = self._stage_dir("03_layout")
        page_ids: list[str] = []
        all_panel_ids: list[str] = []
        errors: list[str] = []

        for spec in page_specs:
            page_num = spec["page_number"]
            spread_num = spec.get("spread_number")
            layout_type = spec.get("layout_type", "grid")

            page_id = self.cpb.add_page(page_num, spread_number=spread_num)
            page_ids.append(page_id)

            if layout_type == "grid":
                rows = spec.get("rows", 3)
                cols = spec.get("cols", 2)
                panel_type = spec.get("panel_type", "action")
                panel_ids = self.cpb.standard_grid(
                    page_id, rows=rows, cols=cols, panel_type=panel_type
                )
                all_panel_ids.extend(panel_ids)

            elif layout_type == "dynamic":
                panel_specs = spec.get("panel_specs", [])
                panel_ids = self.cpb.dynamic_layout(page_id, panel_specs)
                all_panel_ids.extend(panel_ids)

            elif layout_type == "splash":
                panel_type = spec.get("panel_type", "splash")
                panel_id = self.cpb.splash_page(page_id, panel_type=panel_type)
                all_panel_ids.append(panel_id)

            else:
                errors.append(f"Unknown layout_type '{layout_type}' for page {page_num}")

        # Write summary
        summary = f"# Layout Summary\n\nPages: {len(page_ids)}\nPanels: {len(all_panel_ids)}\n"
        summary_path = out_dir / "layout_summary.md"
        summary_path.write_text(summary)

        return StageResult(
            stage="panel_layout",
            success=len(errors) == 0,
            output_path=str(summary_path),
            errors=errors,
            metadata={"page_ids": page_ids, "panel_ids": all_panel_ids},
        )

    def execute_prompt_generation(
        self,
        panel_content: list[dict[str, Any]],
        rework_list: list[tuple[str, str]] | None = None,
    ) -> StageResult:
        """Node: prompt_generation — set content and generate prompts.

        Parameters
        ----------
        panel_content:
            List of dicts with ``panel_id`` and content fields matching
            ``set_panel_content`` params (scene_description, camera_angle,
            characters, mood, spread_number, style_override).
        rework_list:
            Optional list of (panel_id, correction_note) for rework cycles
            from quality_review.

        Returns
        -------
        StageResult with metadata containing prompt count.
        """
        out_dir = self._stage_dir("04_prompts")

        # Handle rework panels
        if rework_list:
            for panel_id, correction in rework_list:
                self.cpb.regenerate_panel(panel_id, prompt_override=correction)
        else:
            # Set content for all panels
            for content in panel_content:
                pid = content["panel_id"]
                self.cpb.set_panel_content(
                    pid,
                    scene_description=content.get("scene_description", ""),
                    camera_angle=content.get("camera_angle", ""),
                    characters=content.get("characters"),
                    mood=content.get("mood", ""),
                    spread_number=content.get("spread_number"),
                    style_override=content.get("style_override"),
                )

        # Generate all prompts
        pending = self.cpb.prepare_all_panels()

        # Write prompt files for pipeline tracking
        for p in pending:
            prompt_file = out_dir / f"panel_{p.panel_id[:8]}.md"
            prompt_file.write_text(
                f"# Panel {p.panel_id}\n\n"
                f"**Aspect Ratio**: {p.aspect_ratio}\n"
                f"**Target**: {p.target_path}\n\n"
                f"## Prompt\n\n{p.prompt}\n"
            )

        return StageResult(
            stage="prompt_generation",
            success=True,
            output_path=str(out_dir),
            metadata={"prompt_count": len(pending)},
        )

    def execute_quality_review(
        self,
        rubric_scores: dict[str, dict[str, float]],
        pass_threshold: float = 3.0,
        min_dimension: float = 2.0,
    ) -> StageResult:
        """Node: quality_review — evaluate rubric scores and route.

        Parameters
        ----------
        rubric_scores:
            Dict mapping page_id to a dict of 6 dimension scores (1-5):
            character_accuracy, style_lock, narrative_coherence,
            color_script, composition, voice_alignment.
        pass_threshold:
            Minimum weighted average to pass (default 3.0).
        min_dimension:
            Minimum score for any single dimension (default 2.0).

        Returns
        -------
        StageResult with metadata containing pass/fail status and any
        rework_list for rejected panels.
        """
        out_dir = self._stage_dir("06_review")
        weights = {
            "character_accuracy": 0.25,
            "style_lock": 0.20,
            "narrative_coherence": 0.15,
            "color_script": 0.15,
            "composition": 0.15,
            "voice_alignment": 0.10,
        }

        passed_pages: list[str] = []
        failed_pages: list[str] = []
        rework_list: list[tuple[str, str]] = []
        report_lines = ["# Quality Review Report\n\n"]

        for page_id, scores in rubric_scores.items():
            weighted_avg = sum(scores.get(dim, 0) * w for dim, w in weights.items())
            below_min = [dim for dim, score in scores.items() if score < min_dimension]

            passed = weighted_avg >= pass_threshold and not below_min

            if passed:
                passed_pages.append(page_id)
            else:
                failed_pages.append(page_id)
                reasons = []
                if weighted_avg < pass_threshold:
                    reasons.append(f"avg {weighted_avg:.1f} < {pass_threshold}")
                if below_min:
                    reasons.append(f"below min: {', '.join(below_min)}")
                rework_list.append((page_id, "; ".join(reasons)))

            report_lines.append(f"## {page_id}\n\n")
            for dim, score in scores.items():
                report_lines.append(f"- {dim}: {score}/5\n")
            report_lines.append(f"- **Weighted avg**: {weighted_avg:.2f}\n")
            report_lines.append(f"- **Result**: {'PASS' if passed else 'FAIL'}\n\n")

        report_path = out_dir / "review_report.md"
        report_path.write_text("".join(report_lines))

        return StageResult(
            stage="quality_review",
            success=len(failed_pages) == 0,
            output_path=str(report_path),
            metadata={
                "passed_pages": passed_pages,
                "failed_pages": failed_pages,
                "rework_list": rework_list,
            },
        )

    def execute_issue_assembly(
        self,
        output_path: str | Path,
    ) -> StageResult:
        """Node: issue_assembly — build and save the final canvas.

        Parameters
        ----------
        output_path:
            Path where the .canvas file should be saved.

        Returns
        -------
        StageResult with output_path to the saved canvas.
        """
        final_dir = self._stage_dir("07_final")
        errors = self.cpb.validate()

        if errors:
            return StageResult(
                stage="issue_assembly",
                success=False,
                errors=errors,
            )

        saved = self.cpb.save(output_path)

        # Write assembly report
        report = (
            f"# Assembly Report\n\n"
            f"**Pages**: {len(self.cpb.pages)}\n"
            f"**Panels**: {len(self.cpb.panels)}\n"
            f"**Canvas**: {saved}\n"
            f"**Warnings**: {len(errors)}\n"
        )
        report_path = final_dir / "assembly_report.md"
        report_path.write_text(report)

        return StageResult(
            stage="issue_assembly",
            success=True,
            output_path=str(saved),
            metadata={
                "pages": len(self.cpb.pages),
                "panels": len(self.cpb.panels),
                "warnings": len(errors),
            },
        )
