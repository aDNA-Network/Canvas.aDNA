"""Canvas-agnostic style/data tables + lookup helpers — PORTED from the CanvasForge ``canvas_comic.comic`` quarry.

Per ratified scope D5 the engine is **data-driven**: this module carries the *mechanism* (the panel-type camera /
composition / nuance templates, the Wally-Wood keyword categories, the act-lighting defaults, the art-style prefix
strings, the aspect-ratio map) — the canvas-agnostic DEFAULTS every comic shares. The *instance data* (a specific
character bible, a 15/16-spread color-script, a dual-protagonist story-state, a per-page art-style map — e.g. the
Science-Stanley run) is NOT here; it rides on ``ComicInput`` (``model.py``). The quarry baked the Science-Stanley
constants in (``CHARACTER_STANLEY``, ``SPREAD_COLOR_SCRIPT``, ``SPREAD_STORY_STATE``, ``ART_STYLE_MAP``,
``ACT_PAGE_RANGES``) — those are dropped here and supplied per comic instead.

Substrate-neutral: no ``canvas_std`` import (ADR-004 two-shelf firewall). Pure data + pure lookup functions.

Source (KEEP-reference, NOT a dependency): ``Archive.aDNA/CanvasForge.aDNA/what/code/canvas_comic/comic.py``
(constants block + ``_style_to_prefix`` / ``_map_panel_type_to_wood`` mechanism). Provenance of the panel-type
``nuances`` seed vocabulary: III learning-store ``pick_reason`` corpus (per the quarry's PANEL_TYPE_TEMPLATES header) —
generic composition terms only, no project-specific knowledge.
"""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# Aspect-ratio map (panel "size" class -> Imagen-style ratio). Mechanism (verbatim from the quarry).
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
# Panel-type templates (camera + composition + per-type compositional nuances). Mechanism (verbatim from the quarry).
# Keys must match ``model.PANEL_TYPES``. The ``nuances`` sub-dimension is opt-in (Panel.compositional_nuance keys in).
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
            "physical_contact_clarity": "spatial relationships between figures read cleanly; "
            "avoid shoulder-overlap ambiguity",
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
# Wally-Wood keyword categories — composition vocabulary by panel intent. Mechanism (verbatim from the quarry).
# ---------------------------------------------------------------------------

WOOD_KEYWORDS: dict[str, str] = {
    "dialogue": "Big Head close-up, over-the-shoulder view, side profile, layered depth composition",
    "establishing": "tiny figure in vast environment, layered depth, bird's eye view with shadows, "
    "framed by doorway or window",
    "emotional": "extreme close-up of face filling frame, dramatic side lighting, strong shadows, "
    "high contrast chiaroscuro",
    "action": "full body dynamic pose, bird's eye view dramatic shadows, single decisive moment, high contrast",
    "action_sequence": "full body dynamic pose, bird's eye view dramatic shadows, "
    "multiple poses showing progression, high contrast",
    "transition": "dark silhouetted figures bright background, character silhouette backlit, "
    "silhouette against bright background",
    "technical": "eye level straightforward composition, macro close-up of detail, "
    "screen or document insert, single object centered dramatic scale",
}

# ---------------------------------------------------------------------------
# Art-style prefix strings (Layer-1). Mechanism: these three palette/style families are generic comic art directions.
# The per-PAGE art-style map (which page is which style) is INSTANCE data → ``Page.art_style`` / ``ComicInput.art_style``.
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

# Negative suffix (Layer-6). Mechanism: a generic "no real text / no photorealism" guard for comic raster output.
NEGATIVE_SUFFIX = (
    "No photorealism, no 3D rendering, no smooth gradients, no anime "
    "screentones, no watercolor, no bright white background, "
    "no legible real text, no readable words or letters, no typeset fonts, "
    "no OCR-readable characters, stylize any text as abstract glowing "
    "symbols or decorative runes, no speech bubble lettering rendered "
    "as real typography."
)

# Default act-lighting fallbacks (Layer-5, used only when a spread has no color-script row). Mechanism: generic
# act-mood lighting language keyed by an act NAME the input supplies via the color-script row's ``act`` field.
ACT_LIGHTING: dict[str, str] = {
    "cover": "neutral warm lighting, inviting atmosphere",
    "act_1": "cool cyan ambient lighting, screen glow, morning light, discovery mood",
    "act_2": "neutral green-tinted lighting, productive workspace glow, afternoon light, determined mood",
    "act_3": "warm purple ambient lighting, soft glow, evening warmth, collaborative mood",
    "closing": "soft starlight ambient, contemplative mood, educational warmth",
}


# ---------------------------------------------------------------------------
# Lookup helpers (ported mechanism; the quarry's _style_to_prefix / _map_panel_type_to_wood).
# ---------------------------------------------------------------------------

def style_to_prefix(style: str) -> str:
    """Map an art-style NAME to its Layer-1 prefix string. Unknown / ghibli -> Ghibli (the neutral default)."""
    if style == "pixel":
        return STYLE_PIXEL
    if style in ("transition", "mixed"):
        return STYLE_TRANSITION
    return STYLE_GHIBLI


def map_panel_type_to_wood(panel_type: str, *, span_cols: int = 1, span_rows: int = 1) -> str:
    """Map a panel type to a Wally-Wood keyword string (ported verbatim).

    A multi-cell ``action`` panel uses the ``action_sequence`` variant (multi-pose progression); a single-cell action
    panel uses ``action`` (a single decisive moment) to avoid sprite-sheet artifacts.
    """
    if panel_type == "action" and (span_cols > 1 or span_rows > 1):
        return WOOD_KEYWORDS.get("action_sequence", WOOD_KEYWORDS.get("action", ""))
    return WOOD_KEYWORDS.get(panel_type, "")


def aspect_for_panel(panel_type: str, *, span_cols: int = 1, span_rows: int = 1, bleed: bool = False) -> str:
    """Derive a panel's aspect ratio from its type + grid span (ported mechanism). Splash/spread/bleed take the
    matching ratio; a wide multi-col panel -> wide; a tall multi-row panel -> tall; else the panel-type default."""
    if panel_type == "splash" or (bleed and span_rows >= 3 and span_cols >= 2):
        return ASPECT_RATIOS["full_page"]
    if span_cols > span_rows:
        return ASPECT_RATIOS["wide"]
    if span_rows > span_cols:
        return ASPECT_RATIOS["tall"]
    return ASPECT_RATIOS["standard"]
