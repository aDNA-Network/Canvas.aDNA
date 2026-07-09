"""Halftone H1 hardening — prompt_layers, configurable negative, input validation, RLHF E2E, span geometry.

Locks the gap-G5 fixes (`campaign_canvas_halftone`, `halftone_gap_register.md`): the structured Layer-1..6
breakdown (`qualities.prompt_layers` — the render bridge's per-channel source, incl. the separate `negative`
channel a ComfyUI-style backend feeds its negative CLIP encode), the data-driven negative override, the new
spread/splash/story-state/image-path validations, the end-to-end RLHF-hint activation through ``build_comic``,
and the full-page-span geometry case.
"""

from __future__ import annotations

import textwrap

import pytest

from comic_generator import layout, style
from comic_generator.consume import build_comic
from comic_generator.model import (
    CharacterDescriptor,
    CharacterStateEntry,
    ComicInput,
    Page,
    Panel,
    Spread,
    SpreadStoryState,
    load_comic,
    validate_image_paths,
)

LAYER_KEYS = ["style", "characters", "scene", "camera", "lighting", "negative"]


def _panel_quals(doc: dict) -> dict:
    """qualities of the first image-class component in a built canvas."""
    comp = doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
    return next(e["qualities"] for e in comp.values() if e.get("class") == "image")


def _mini(**overrides) -> ComicInput:
    base = dict(
        title="t",
        id="urn:adna:canvas:comic:hardening",
        version="0.1.0",
        pages=(Page(number=1, panels=(Panel(panel_type="action", scene="A scene.", characters=("zed",)),)),),
    )
    base.update(overrides)
    return ComicInput(**base)


# --- prompt_layers (the structured Layer-1..6 breakdown) --------------------------------------------

def test_prompt_layers_emitted_with_all_keys_and_default_negative():
    quals = _panel_quals(build_comic(_mini()))
    assert list(quals["prompt_layers"].keys()) == LAYER_KEYS
    assert quals["prompt_layers"]["negative"] == style.NEGATIVE_SUFFIX
    assert quals["prompt_layers"]["scene"] == "A scene."


def test_prompt_layers_join_equals_assembled_text():
    # the assembled single-prompt form is exactly the non-empty layers joined by blank lines (back-compat)
    quals = _panel_quals(build_comic(_mini()))
    joined = "\n\n".join(v for v in quals["prompt_layers"].values() if v)
    assert joined == quals["image_prompt"]


def test_negative_suffix_is_configurable_instance_data():
    quals = _panel_quals(build_comic(_mini(negative_suffix="no cartoon outlines")))
    assert quals["prompt_layers"]["negative"] == "no cartoon outlines"
    assert quals["image_prompt"].endswith("no cartoon outlines")
    assert style.NEGATIVE_SUFFIX not in quals["image_prompt"]


# --- spread cross-validation (only when spreads are declared) ---------------------------------------

def test_undeclared_spread_reference_rejected():
    with pytest.raises(ValueError, match="references spread 5"):
        _mini(
            spreads=(Spread(number=1, pages=(1,)),),
            pages=(Page(number=1, spread_number=5, panels=(Panel(),)),),
        )


def test_declared_spread_with_dangling_page_rejected():
    with pytest.raises(ValueError, match="spread 1 declares pages"):
        _mini(spreads=(Spread(number=1, pages=(1, 9)),))


def test_implicit_spreads_without_declaration_stay_legal():
    comic = _mini(pages=(Page(number=1, spread_number=7, panels=(Panel(),)),))  # no spreads: block
    assert build_comic(comic)["nodes"]


# --- splash + story-state guards (warnings, not errors) ---------------------------------------------

def test_splash_with_multiple_panels_warns():
    with pytest.warns(UserWarning, match="splash"):
        Page(number=1, layout_type="splash", panels=(Panel(), Panel()))


def test_story_state_unknown_character_warns_when_bible_declared():
    with pytest.warns(UserWarning, match="ghost"):
        _mini(
            characters=(CharacterDescriptor(name="zed", descriptor="d"),),
            story_state=(SpreadStoryState(spread=1, characters={"ghost": CharacterStateEntry(present=True)}),),
        )


def test_story_state_without_bible_does_not_warn(recwarn):
    _mini(story_state=(SpreadStoryState(spread=1, characters={"ghost": CharacterStateEntry(present=True)}),))
    assert not [w for w in recwarn.list if issubclass(w.category, UserWarning)]


# --- image_path existence -----------------------------------------------------------------------------

def test_validate_image_paths_reports_missing_and_load_comic_warns(tmp_path):
    (tmp_path / "real.png").write_bytes(b"\x89PNG")
    spec = textwrap.dedent(
        """
        title: t
        id: urn:adna:canvas:comic:paths
        version: 0.1.0
        pages:
          - number: 1
            panels:
              - {panel_type: action, scene: ok, image_path: real.png}
              - {panel_type: action, scene: broken, image_path: nope.png}
        """
    )
    inp = tmp_path / "c.yaml"
    inp.write_text(spec, encoding="utf-8")
    with pytest.warns(UserWarning, match="nope.png"):
        comic = load_comic(inp)
    assert validate_image_paths(comic, base_dir=tmp_path) == ["nope.png"]


# --- RLHF hints activate end-to-end through build_comic ----------------------------------------------

def test_rlhf_hints_flow_end_to_end_when_register_supplied():
    doc = build_comic(
        _mini(),
        register="R7",
        rlhf_character_hints={"r7": "frame holds the gaze"},
        rlhf_camera_nuances={"r7": "let negative space breathe"},
    )
    quals = _panel_quals(doc)
    assert "RLHF hint: frame holds the gaze" in quals["prompt_layers"]["characters"]
    assert "RLHF hint: let negative space breathe" in quals["prompt_layers"]["camera"]
    assert "RLHF hint" in quals["image_prompt"]


def test_rlhf_hints_inert_without_register():
    doc = build_comic(_mini(), rlhf_character_hints={"r7": "frame holds the gaze"})
    assert "RLHF hint" not in _panel_quals(doc)["image_prompt"]


# --- full-page-span geometry ---------------------------------------------------------------------------

def test_full_page_span_panel_fills_the_trim_box():
    box = layout.panel_box_in_page(0, 0, layout.GRID_ROWS, layout.GRID_COLS, "grid")
    assert (box.x, box.y, box.w, box.h) == (0, 0, layout.TRIM_W, layout.TRIM_H)
