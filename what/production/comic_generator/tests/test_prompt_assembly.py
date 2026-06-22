"""Tests for comic_generator.prompt — the 6-layer image-prompt assembly as PURE FUNCTIONS (PORTED, refactored).

The quarry assembled prompts as ``ComicPageBuilder`` methods reading hardcoded constants behind a ``ContextPack``
file-existence gate. Here the layers are free functions over the substrate-free ``Panel``/``Page`` with the instance
data (character bible, color-script, story-state, default style) THREADED IN (scope D5) and NO ContextPack gate. These
tests verify each layer + the full 6-layer assembly + the dual-prompt thread-through, and that no pixels are produced.
"""

from __future__ import annotations

from comic_generator.model import (
    CharacterStateEntry,
    Page,
    Panel,
    SpreadColorScript,
    SpreadStoryState,
)
from comic_generator.panel_layout import assemble_dual_prompt
from comic_generator.prompt import (
    ImagePrompt,
    build_camera_block,
    build_character_block,
    build_lighting_block,
    generate_panel_prompt,
)
from comic_generator import style


# --- Layer 2: character block --------------------------------------------------------------------------------

def test_character_block_uses_bible_descriptor():
    panel = Panel(panel_type="dialogue", characters=("Stanley",))
    bible = {"stanley": "spiky-haired scientist in a lab coat"}
    block = build_character_block(panel, character_bible=bible)
    assert "spiky-haired scientist in a lab coat" in block


def test_character_block_merges_story_state_mood_and_pose():
    panel = Panel(panel_type="action", characters=("Helix",))
    bible = {"helix": "golden retriever"}
    state = SpreadStoryState(
        spread=4,
        characters={"helix": CharacterStateEntry(present=True, pose="sleeping_at_feet")},
    )
    block = build_character_block(panel, character_bible=bible, story_state=state)
    assert "golden retriever" in block
    assert "sleeping_at_feet" in block


def test_character_block_falls_back_to_bare_name_without_bible():
    panel = Panel(panel_type="action", characters=("Newcomer",))
    block = build_character_block(panel, character_bible={})
    assert block == "Newcomer"


def test_character_block_empty_when_no_characters():
    assert build_character_block(Panel(panel_type="action"), character_bible={}) == ""


def test_character_block_rlhf_hint_dormant_without_register():
    panel = Panel(panel_type="action", characters=("X",))
    # hints present but register None -> inert
    block = build_character_block(panel, character_bible={}, rlhf_hints={"r7": "h"})
    assert "RLHF hint" not in block


def test_character_block_rlhf_hint_applies_when_register_resolves():
    panel = Panel(panel_type="action", characters=("X",))
    block = build_character_block(panel, character_bible={}, register="R7", rlhf_hints={"r7": "frame holds"})
    assert "(RLHF hint: frame holds)" in block


# --- Layer 4: camera block -----------------------------------------------------------------------------------

def test_camera_block_uses_panel_type_template():
    panel = Panel(panel_type="establishing")
    block = build_camera_block(panel)
    assert style.PANEL_TYPE_TEMPLATES["establishing"]["camera"] in block
    # establishing -> Wood "establishing" keywords
    assert "tiny figure in vast environment" in block


def test_camera_block_explicit_camera_angle_overrides_template():
    panel = Panel(panel_type="action", camera_angle="worm's eye view")
    assert build_camera_block(panel).startswith("worm's eye view")


def test_camera_block_action_sequence_for_multicell():
    single = build_camera_block(Panel(panel_type="action"))
    multi = build_camera_block(Panel(panel_type="action", span_cols=2))
    assert "single decisive moment" in single
    assert "multiple poses showing progression" in multi


def test_camera_block_balloon_space():
    panel = Panel(panel_type="dialogue", balloon_space="upper third")
    assert "clear space in upper third" in build_camera_block(panel)


def test_camera_block_compositional_nuance_keys_in():
    panel = Panel(panel_type="dialogue", compositional_nuance="physical_contact_clarity")
    block = build_camera_block(panel)
    assert "compositional nuance:" in block
    assert "shoulder-overlap ambiguity" in block


def test_camera_block_compositional_nuance_inert_when_absent_key():
    panel = Panel(panel_type="dialogue", compositional_nuance="does_not_exist")
    assert "compositional nuance:" not in build_camera_block(panel)


# --- Layer 5: lighting block ---------------------------------------------------------------------------------

def test_lighting_block_spread_color_script_primary():
    panel = Panel(panel_type="action", mood="determined")
    cs = SpreadColorScript(spread=3, dominant="#e0af68", lighting="warm_golden", mood="inviting")
    block = build_lighting_block(panel, color_script=cs)
    assert "determined" in block
    assert "warm_golden lighting, dominant #e0af68" in block
    assert "Mood: inviting" in block


def test_lighting_block_act_fallback_when_no_script_lighting():
    panel = Panel(panel_type="action")
    cs = SpreadColorScript(spread=5, act="act_1")  # no lighting -> act fallback
    block = build_lighting_block(panel, color_script=cs)
    assert style.ACT_LIGHTING["act_1"] in block


def test_lighting_block_default_when_nothing():
    assert build_lighting_block(Panel(panel_type="action")) == "ambient lighting"


# --- full 6-layer assembly -----------------------------------------------------------------------------------

def test_generate_panel_prompt_six_layers_in_order():
    panel = Panel(
        panel_type="dialogue",
        scene="Stanley explains the lattice at a whiteboard.",
        characters=("Stanley",),
        mood="passionate",
        balloon_space="upper third",
    )
    page = Page(number=3, panels=(panel,), art_style="ghibli", spread_number=2)
    bible = {"stanley": "spiky-haired scientist"}
    cs = SpreadColorScript(spread=2, dominant="#e0af68", lighting="warm_golden", mood="inviting")
    ip = generate_panel_prompt(panel, page, character_bible=bible, color_script=cs)
    # Layer 1 (style), 2 (char), 3 (scene), 4 (camera), 5 (lighting), 6 (negative) — all present, in order.
    assert ip.text.startswith(style.STYLE_GHIBLI)
    assert "spiky-haired scientist" in ip.text
    assert "Stanley explains the lattice at a whiteboard." in ip.text
    assert style.PANEL_TYPE_TEMPLATES["dialogue"]["camera"] in ip.text
    assert "warm_golden lighting" in ip.text
    assert ip.text.rstrip().endswith(style.NEGATIVE_SUFFIX)
    # ordering: style < char < scene < camera < lighting < negative
    idxs = [
        ip.text.index(style.STYLE_GHIBLI),
        ip.text.index("spiky-haired scientist"),
        ip.text.index("Stanley explains the lattice"),
        ip.text.index(style.PANEL_TYPE_TEMPLATES["dialogue"]["camera"]),
        ip.text.index("warm_golden lighting"),
        ip.text.index(style.NEGATIVE_SUFFIX),
    ]
    assert idxs == sorted(idxs)


def test_generate_panel_prompt_style_override_precedence():
    panel = Panel(panel_type="action", scene="x", style_override="pixel")
    page = Page(number=8, panels=(panel,), art_style="ghibli")
    ip = generate_panel_prompt(panel, page)
    assert ip.text.startswith(style.STYLE_PIXEL)  # panel override beats page style


def test_generate_panel_prompt_aspect_ratio_default_from_type():
    splash = Panel(panel_type="splash", scene="x")
    ip = generate_panel_prompt(splash)
    assert ip.aspect_ratio == style.ASPECT_RATIOS["full_page"]


def test_generate_panel_prompt_explicit_aspect_ratio_wins():
    panel = Panel(panel_type="action", scene="x", aspect_ratio="21:9")
    assert generate_panel_prompt(panel).aspect_ratio == "21:9"


def test_generate_panel_prompt_threads_spatial_layout_into_mermaid():
    layout = (
        "graph TB\n"
        '    panel["panel:p1<br/>framing=medium"]\n'
        "    subgraph TOP[TOP balloon space]\n    end\n"
        "    subgraph MID[MID subject zone]\n    end\n"
        "    subgraph BOT[BOT ground zone]\n    end\n"
    )
    panel = Panel(panel_type="dialogue", scene="x", spatial_layout=layout)
    ip = generate_panel_prompt(panel)
    assert ip.mermaid_layout == layout
    # and the dual-prompt concatenation surfaces PART 2
    dual = assemble_dual_prompt(ip)
    assert dual.count("[PART 2: SPATIAL LAYOUT]") == 2


def test_generate_panel_prompt_threads_compositional_intent():
    panel = Panel(panel_type="close_up", scene="x", compositional_intent="object_interaction_focus")
    ip = generate_panel_prompt(panel)
    assert ip.compositional_intent == "object_interaction_focus"
    assert "[PART 3: COMPOSITIONAL INTENT]" in assemble_dual_prompt(ip)


def test_generate_panel_prompt_returns_image_prompt_only():
    """The producer emits a prompt object — text + metadata, never a rendered image."""
    ip = generate_panel_prompt(Panel(panel_type="action", scene="x"))
    assert isinstance(ip, ImagePrompt)
    assert isinstance(ip.text, str) and ip.text
