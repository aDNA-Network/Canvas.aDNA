"""The 6-layer image-prompt assembly — PORTED from the CanvasForge quarry, refactored to PURE FUNCTIONS.

The quarry assembled prompts as ``ComicPageBuilder`` methods (``generate_panel_prompt`` + ``_build_character_block`` /
``_build_camera_block`` / ``_build_lighting_block``) that read hardcoded Science-Stanley constants and gated on a
``ContextPack`` file-existence check. Here those become free functions over the substrate-free ``Panel`` / ``Page``
(``model.py``); the instance data (character bible, color-script, story-state, art-style) is THREADED IN as arguments
(scope D5 — data-driven) rather than read from module constants. The ``ContextPack`` / ``ContextNotLoaded``
file-existence gate is DROPPED (those five inputs are carried as ``context_object.refs`` instead — Operation Atelier A2
ratified scope). The optional RLHF hints (``rlhf_hints.py``) are dormant by default.

A local ``ImagePrompt`` dataclass replaces ``canvas_core.image_generation.ImagePrompt`` (the old substrate type). It
carries the assembled Layer-1..6 ``text``, an optional ``mermaid_layout`` (the panel's spatial grammar), an
``aspect_ratio``, and an optional ``compositional_intent`` (the PART-3 anchor). This module imports neither
``canvas_std`` nor ``panel_layout`` (``panel_layout`` imports ``ImagePrompt`` from HERE — keeping the dependency
acyclic); the dual-prompt *concatenation* lives in ``panel_layout.assemble_dual_prompt``.

NEVER renders an image — emits prompt TEXT only.
"""

from __future__ import annotations

from dataclasses import dataclass

from comic_generator import style
from comic_generator.model import CharacterStateEntry, Page, Panel, SpreadColorScript, SpreadStoryState


@dataclass
class ImagePrompt:
    """A panel's image-generation directive — TEXT ONLY (no pixels). Replaces the old ``canvas_core`` ImagePrompt.

    ``text``: the assembled Layer-1..6 prompt. ``mermaid_layout``: the panel's ``comic_panel_layout`` spatial grammar
    (or ``None``). ``aspect_ratio``: the Imagen-style ratio. ``compositional_intent``: an optional free-text PART-3
    anchor surfaced by ``panel_layout.assemble_dual_prompt``.
    """

    text: str
    mermaid_layout: str | None = None
    aspect_ratio: str = "1:1"
    compositional_intent: str | None = None


def _maybe_append_rlhf_hint(block: str, *, register: str | None, rlhf_hints: dict[str, str] | None) -> str:
    """Append an RLHF hint as a parenthetical suffix when both kwargs resolve (ported mechanism; inert by default).

    Inert if ``register`` is None, ``rlhf_hints`` is None/empty for the normalized key, or the hint is empty. Register
    normalization mirrors the quarry: lowercase, then ``+``/``-``/`` `` → ``_``.
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


def build_character_block(
    panel: Panel,
    *,
    character_bible: dict[str, str] | None = None,
    story_state: SpreadStoryState | None = None,
    register: str | None = None,
    rlhf_hints: dict[str, str] | None = None,
) -> str:
    """Layer 2 — the character block, with a story-state mood/pose merge (ported mechanism, data-driven).

    For each character named on the panel: look its descriptor up in ``character_bible`` (name lowercased); if the
    spread's ``story_state`` marks it present, merge its mood/pose suffix; fall back to the bare name when the bible
    has no entry. The quarry hardcoded three characters — here every descriptor is supplied via the bible (scope D5).
    """
    bible = character_bible or {}
    parts: list[str] = []
    for char_name in panel.characters:
        key = char_name.lower()
        desc = bible.get(key, char_name)
        st: CharacterStateEntry | None = (
            story_state.characters.get(key) if story_state else None
        )
        if st and st.present:
            if st.mood:
                desc += f", {st.mood}"
            if st.pose:
                desc += f", {st.pose}"
        parts.append(desc)

    block = ". ".join(parts) if parts else ""
    return _maybe_append_rlhf_hint(block, register=register, rlhf_hints=rlhf_hints)


def build_camera_block(
    panel: Panel,
    *,
    register: str | None = None,
    rlhf_hints: dict[str, str] | None = None,
) -> str:
    """Layer 4 — the camera/composition block: panel-type template + Wally-Wood keywords + balloon space + nuance.

    Ported verbatim in behavior. ``panel.compositional_nuance`` (opt-in) appends a template-scoped nuance descriptor
    when it keys into the matching template's ``nuances`` dict; inert otherwise. RLHF hints append when resolved.
    """
    parts: list[str] = []
    template = style.PANEL_TYPE_TEMPLATES.get(panel.panel_type)

    if panel.camera_angle:
        parts.append(panel.camera_angle)
    elif template:
        parts.append(template["camera"])

    wood = style.map_panel_type_to_wood(
        panel.panel_type, span_cols=panel.span_cols, span_rows=panel.span_rows
    )
    if wood:
        parts.append(wood)

    if panel.balloon_space:
        parts.append(f"Composition with clear space in {panel.balloon_space} for text overlay.")

    block = " ".join(parts)

    if panel.compositional_nuance and template:
        nuance_text = template.get("nuances", {}).get(panel.compositional_nuance)
        if nuance_text:
            block = f"{block} (compositional nuance: {nuance_text})"

    return _maybe_append_rlhf_hint(block, register=register, rlhf_hints=rlhf_hints)


def build_lighting_block(
    panel: Panel,
    *,
    color_script: SpreadColorScript | None = None,
) -> str:
    """Layer 5 — the lighting/mood block, spread-color-script-priority (ported mechanism, data-driven).

    A spread color-script (if supplied) is the primary lighting descriptor; otherwise the act-level default
    (``style.ACT_LIGHTING`` keyed by the color-script row's ``act``, when present) applies. The quarry read its
    color-script + act tables from module constants; here the row is supplied per spread (scope D5).
    """
    parts: list[str] = []
    if panel.mood:
        parts.append(panel.mood)

    if color_script and color_script.lighting:
        parts.append(f"{color_script.lighting} lighting, dominant {color_script.dominant}")
        if color_script.mood:
            parts.append(f"Mood: {color_script.mood}")
    elif color_script and color_script.act and color_script.act in style.ACT_LIGHTING:
        parts.append(style.ACT_LIGHTING[color_script.act])

    return ". ".join(parts) if parts else "ambient lighting"


def _layer1_style(panel: Panel, page: Page | None, *, comic_default: str = "ghibli") -> str:
    """Layer 1 — the art-style prefix. Panel override > page override > comic default."""
    if panel.style_override:
        return style.style_to_prefix(panel.style_override)
    if page and page.art_style:
        return style.style_to_prefix(page.art_style)
    return style.style_to_prefix(comic_default)


def generate_panel_prompt(
    panel: Panel,
    page: Page | None = None,
    *,
    character_bible: dict[str, str] | None = None,
    color_script: SpreadColorScript | None = None,
    story_state: SpreadStoryState | None = None,
    comic_default_style: str = "ghibli",
    register: str | None = None,
    rlhf_character_hints: dict[str, str] | None = None,
    rlhf_camera_nuances: dict[str, str] | None = None,
) -> ImagePrompt:
    """Assemble a panel's 6-layer image PROMPT (pure function; emits text only, NEVER renders).

    Layers (joined by blank lines, quarry order verbatim):
      1. style prefix (panel override > page override > comic default)
      2. character block (bible + story-state merge)
      3. scene/environment (the panel's free-text scene)
      4. camera/composition (panel-type template + Wood keywords + balloon space + nuance)
      5. lighting/mood (spread color-script priority, else act default)
      6. negative suffix

    The instance data (bible / color-script / story-state / default style) is threaded in — nothing is read from
    module constants (scope D5). ``mermaid_layout`` is set from the panel's ``spatial_layout`` (the dual-prompt
    concatenation happens in ``panel_layout.assemble_dual_prompt``); ``compositional_intent`` rides through as the
    PART-3 anchor. The ``aspect_ratio`` is the panel's explicit value, else derived from its type + grid span.
    """
    layers: list[str] = []

    # Layer 1
    layers.append(_layer1_style(panel, page, comic_default=comic_default_style))

    # Layer 2
    char_block = build_character_block(
        panel,
        character_bible=character_bible,
        story_state=story_state,
        register=register,
        rlhf_hints=rlhf_character_hints,
    )
    if char_block:
        layers.append(char_block)

    # Layer 3
    if panel.scene:
        layers.append(panel.scene)

    # Layer 4
    layers.append(build_camera_block(panel, register=register, rlhf_hints=rlhf_camera_nuances))

    # Layer 5
    layers.append(build_lighting_block(panel, color_script=color_script))

    # Layer 6
    layers.append(style.NEGATIVE_SUFFIX)

    text = "\n\n".join(layer for layer in layers if layer)
    aspect = panel.aspect_ratio or style.aspect_for_panel(
        panel.panel_type, span_cols=panel.span_cols, span_rows=panel.span_rows, bleed=panel.bleed
    )
    return ImagePrompt(
        text=text,
        mermaid_layout=panel.spatial_layout or None,
        aspect_ratio=aspect,
        compositional_intent=panel.compositional_intent or None,
    )
