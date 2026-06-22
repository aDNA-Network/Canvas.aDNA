"""Shared fixtures — a worked multi-spread ``ComicInput`` + the default built canvas doc.

The ``comic`` fixture exercises the load-bearing shapes: multiple spreads, a splash page, a grid page, a multi-cell
panel (adjacency), a rendered panel (``image_path`` -> file node), an un-rendered panel (text placeholder), a panel
with a spatial layout (dual-prompt PART 2), and the data-driven instance overlays (character bible / color script /
story state) supplied through the input (scope D5).
"""

from __future__ import annotations

import pytest

from comic_generator.consume import build_comic
from comic_generator.model import (
    CharacterDescriptor,
    CharacterStateEntry,
    ComicInput,
    Page,
    Panel,
    Spread,
    SpreadColorScript,
    SpreadStoryState,
)

_LAYOUT = (
    "graph TB\n"
    '    panel["panel:p3_2<br/>framing=medium"]\n'
    "    subgraph TOP[TOP balloon space]\n"
    '        b1["balloon-1<br/>type=speech"]\n'
    "    end\n"
    "    subgraph MID[MID subject zone]\n"
    '        s1["Stanley<br/>depth=foreground"]\n'
    "    end\n"
    "    subgraph BOT[BOT ground zone]\n    end\n"
    "    s1 -- speaks --> b1\n"
)


@pytest.fixture
def comic() -> ComicInput:
    return ComicInput(
        title="Science Stanley — Test Issue",
        id="urn:adna:canvas:comic:test",
        version="0.1.0",
        art_style="ghibli",
        refs=("[[character_bible]]", "[[color_script]]", "[[storyboard]]"),
        characters=(
            CharacterDescriptor(name="stanley", descriptor="spiky-haired Ghibli scientist in a lab coat"),
            CharacterDescriptor(name="helix", descriptor="golden retriever lab mascot"),
        ),
        color_script=(
            SpreadColorScript(spread=1, act="cover", dominant="#565f89", lighting="neutral", mood="cover_matter"),
            SpreadColorScript(spread=2, act="act_1", dominant="#e0af68", lighting="warm_golden", mood="inviting"),
        ),
        story_state=(
            SpreadStoryState(spread=1, world="cover",
                             characters={"stanley": CharacterStateEntry(present=True, mood="confident")}),
            SpreadStoryState(spread=2, world="ghibli",
                             characters={"stanley": CharacterStateEntry(present=True, mood="determined"),
                                         "helix": CharacterStateEntry(present=True, pose="walking_alongside")}),
        ),
        spreads=(Spread(number=1, pages=(1, 2)), Spread(number=2, pages=(3, 4))),
        pages=(
            Page(number=1, layout_type="splash", spread_number=1, panels=(
                Panel(panel_type="splash", scene="Stanley in a sunlit lab, title-card energy.",
                      characters=("stanley",), balloon_space="upper third",
                      compositional_nuance="composition_naturalness"),
            )),
            Page(number=2, layout_type="grid", spread_number=1, panels=(
                Panel(panel_type="establishing", scene="Wide lab shot.", characters=("stanley", "helix"),
                      row=0, col=0, span_cols=2),
                Panel(panel_type="dialogue", scene="Stanley grins at the reader.", characters=("stanley",),
                      row=1, col=0, balloon_space="upper third"),
                Panel(panel_type="close_up", scene="A glowing lattice on a screen.", row=1, col=1,
                      image_path="images/panel_lattice.png"),  # a RENDERED panel -> file node
            )),
            Page(number=3, layout_type="grid", spread_number=2, panels=(
                Panel(panel_type="action", scene="Stanley races down a server corridor, Helix beside him.",
                      characters=("stanley", "helix"), row=0, col=0, span_cols=2,
                      compositional_nuance="physical_contact_clarity"),
                Panel(panel_type="dialogue", scene="Stanley points at a monitor.", characters=("stanley",),
                      row=1, col=0, balloon_space="upper third",
                      compositional_intent="object_interaction_focus", spatial_layout=_LAYOUT),
                Panel(panel_type="transition", scene="Screen glow fades to a pixel dissolve.", row=1, col=1,
                      style_override="transition"),
            )),
            Page(number=4, layout_type="grid", spread_number=2, panels=(
                Panel(panel_type="dialogue", scene="Agent Stanley waves as a pixel sprite.",
                      characters=("agent_stanley",), row=0, col=0, style_override="pixel"),
                Panel(panel_type="close_up", scene="The lattice resolves into a clear picture.", row=0, col=1,
                      compositional_nuance="fading_visual_effect"),
            )),
        ),
    )


@pytest.fixture
def doc(comic: ComicInput) -> dict:
    return build_comic(comic)
