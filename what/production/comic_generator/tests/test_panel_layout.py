"""Tests for comic_generator.panel_layout — the comic_panel_layout schema parser / serializer / dual-prompt assembly.

PORTED from the CanvasForge quarry test ``test_mermaid_layout.py`` (M-R2-02 S1), refactored to plain pytest functions
and the local ``ImagePrompt``. Exercises the parse / serialize round-trip (idempotent normalization) + the dual-prompt
concatenation (V1 + V2/PART-3 paths). The spec § 3 Imagen wrapper text is carried verbatim.
"""

from __future__ import annotations

import pytest

from comic_generator.panel_layout import (
    IMAGEN_DUAL_PROMPT_WRAPPER,
    IMAGEN_DUAL_PROMPT_WRAPPER_WITH_COMPOSITIONAL_INTENT,
    REGION_DESCRIPTIONS,
    VALID_DEPTHS,
    VALID_FRAMINGS,
    VALID_REGIONS,
    VALID_RELATIONS,
    LayoutNode,
    PanelLayout,
    SpatialEdge,
    assemble_dual_prompt,
    parse_panel_layout,
    serialize_panel_layout,
)
from comic_generator.prompt import ImagePrompt

WORKED_EXAMPLE = """\
graph TB
    panel["panel:p1_1<br/>framing=medium"]

    subgraph TOP[TOP balloon space]
        b1["balloon-1<br/>type=speech"]
    end

    subgraph MID[MID subject zone]
        s1["Stanley<br/>depth=foreground"]
        s2["monitor<br/>depth=midground"]
    end

    subgraph BOT[BOT ground zone]
        h1["Helix<br/>depth=background<br/>pose=sleeping"]
    end

    s1 -- left-of --> s2
    s1 -- above --> h1
    s2 -- above --> h1
    s1 -- speaks --> b1
"""


def _empty_panel(panel_id: str = "p1", framing: str = "medium") -> str:
    return (
        f"graph TB\n"
        f'    panel["panel:{panel_id}<br/>framing={framing}"]\n\n'
        f"    subgraph TOP[{REGION_DESCRIPTIONS['TOP']}]\n    end\n\n"
        f"    subgraph MID[{REGION_DESCRIPTIONS['MID']}]\n    end\n\n"
        f"    subgraph BOT[{REGION_DESCRIPTIONS['BOT']}]\n    end\n"
    )


# --- dataclass shape -----------------------------------------------------------------------------------------

def test_panel_layout_default_lists_empty():
    layout = PanelLayout(panel_id="p1", framing="medium")
    assert layout.top == [] and layout.mid == [] and layout.bot == [] and layout.edges == []


def test_layout_node_optional_depth_defaults_attrs_empty():
    node = LayoutNode(name="balloon-1", depth=None)
    assert node.depth is None
    assert node.attrs == {}


def test_spatial_edge_all_seven_relations_construct():
    for rel in VALID_RELATIONS:
        assert SpatialEdge(source="a", target="b", relation=rel).relation == rel


# --- parser --------------------------------------------------------------------------------------------------

def test_parse_minimal_panel_three_empty_regions():
    layout = parse_panel_layout(_empty_panel("p1", "medium"))
    assert layout.panel_id == "p1"
    assert layout.framing == "medium"
    assert layout.top == [] and layout.mid == [] and layout.bot == []


def test_parse_panel_top_node_only():
    mermaid = (
        "graph TB\n"
        '    panel["panel:p2<br/>framing=close-up"]\n'
        "    subgraph TOP[TOP balloon space]\n"
        '        b1["caption<br/>type=narration"]\n'
        "    end\n"
        "    subgraph MID[MID subject zone]\n    end\n"
        "    subgraph BOT[BOT ground zone]\n    end\n"
    )
    layout = parse_panel_layout(mermaid)
    assert len(layout.top) == 1
    assert layout.top[0].name == "caption"
    assert layout.top[0].attrs == {"type": "narration"}


def test_parse_worked_example_all_three_regions():
    layout = parse_panel_layout(WORKED_EXAMPLE)
    assert layout.panel_id == "p1_1"
    assert [n.name for n in layout.top] == ["balloon-1"]
    assert [n.name for n in layout.mid] == ["Stanley", "monitor"]
    assert [n.name for n in layout.bot] == ["Helix"]


def test_parse_blank_lines_and_comments_ignored():
    mermaid = (
        "graph TB\n%% leading comment\n\n"
        '    panel["panel:p3<br/>framing=wide"]\n\n'
        "    subgraph TOP[TOP balloon space]\n    end\n"
        "%% mid comment\n"
        "    subgraph MID[MID subject zone]\n    end\n"
        "    subgraph BOT[BOT ground zone]\n    end\n"
    )
    assert parse_panel_layout(mermaid).framing == "wide"


def test_parse_node_depth_and_attrs():
    layout = parse_panel_layout(WORKED_EXAMPLE)
    assert layout.mid[0].name == "Stanley"
    assert layout.mid[0].depth == "foreground"
    assert layout.mid[0].attrs == {}
    assert layout.top[0].depth is None
    assert layout.top[0].attrs == {"type": "speech"}
    assert layout.bot[0].depth == "background"
    assert layout.bot[0].attrs == {"pose": "sleeping"}


def test_parse_framing_all_four_values():
    for framing in VALID_FRAMINGS:
        assert parse_panel_layout(_empty_panel("px", framing)).framing == framing


def test_parse_depths_all_three_values():
    for depth in VALID_DEPTHS:
        mermaid = (
            "graph TB\n"
            '    panel["panel:pd<br/>framing=medium"]\n'
            "    subgraph TOP[TOP balloon space]\n    end\n"
            "    subgraph MID[MID subject zone]\n"
            f'        s1["x<br/>depth={depth}"]\n'
            "    end\n"
            "    subgraph BOT[BOT ground zone]\n    end\n"
        )
        assert parse_panel_layout(mermaid).mid[0].depth == depth


def test_parse_edge_left_of():
    layout = parse_panel_layout(WORKED_EXAMPLE)
    edge = next(e for e in layout.edges if e.relation == "left-of")
    assert edge.source == "Stanley" and edge.target == "monitor"


def test_parse_edge_speaks_crosses_subgraphs():
    layout = parse_panel_layout(WORKED_EXAMPLE)
    edge = next(e for e in layout.edges if e.relation == "speaks")
    assert edge.source == "Stanley" and edge.target == "balloon-1"


def test_parse_all_seven_relations_round_trip():
    nodes_top, nodes_mid, rel_lines = [], [], []
    for i, rel in enumerate(VALID_RELATIONS):
        nodes_top.append(f'        t{i}["t{i}<br/>type=marker"]')
        nodes_mid.append(f'        m{i}["m{i}<br/>depth=foreground"]')
        rel_lines.append(f"    m{i} -- {rel} --> t{i}")
    mermaid = (
        "graph TB\n"
        '    panel["panel:perel<br/>framing=medium"]\n'
        "    subgraph TOP[TOP balloon space]\n" + "\n".join(nodes_top) + "\n    end\n"
        "    subgraph MID[MID subject zone]\n" + "\n".join(nodes_mid) + "\n    end\n"
        "    subgraph BOT[BOT ground zone]\n    end\n" + "\n".join(rel_lines) + "\n"
    )
    layout = parse_panel_layout(mermaid)
    assert sorted(e.relation for e in layout.edges) == sorted(VALID_RELATIONS)


# --- parser errors -------------------------------------------------------------------------------------------

def test_parse_empty_string_raises():
    with pytest.raises(ValueError):
        parse_panel_layout("")
    with pytest.raises(ValueError):
        parse_panel_layout("   \n  \n")


def test_parse_missing_header_raises():
    with pytest.raises(ValueError, match="graph TB"):
        parse_panel_layout('    panel["panel:p1<br/>framing=medium"]\n')


def test_parse_missing_subgraph_raises():
    mermaid = (
        "graph TB\n"
        '    panel["panel:p1<br/>framing=medium"]\n'
        "    subgraph TOP[TOP balloon space]\n    end\n"
        "    subgraph MID[MID subject zone]\n    end\n"
    )
    with pytest.raises(ValueError, match="BOT"):
        parse_panel_layout(mermaid)


def test_parse_invalid_framing_raises():
    bad = _empty_panel("p1", "medium").replace("framing=medium", "framing=zoom")
    with pytest.raises(ValueError, match="framing"):
        parse_panel_layout(bad)


def test_parse_invalid_depth_raises():
    bad = (
        "graph TB\n"
        '    panel["panel:p1<br/>framing=medium"]\n'
        "    subgraph TOP[TOP balloon space]\n    end\n"
        "    subgraph MID[MID subject zone]\n"
        '        s1["Stanley<br/>depth=middlegrade"]\n'
        "    end\n"
        "    subgraph BOT[BOT ground zone]\n    end\n"
    )
    with pytest.raises(ValueError, match="depth"):
        parse_panel_layout(bad)


def test_parse_unknown_edge_id_raises():
    bad = (
        "graph TB\n"
        '    panel["panel:p1<br/>framing=medium"]\n'
        "    subgraph TOP[TOP balloon space]\n    end\n"
        "    subgraph MID[MID subject zone]\n"
        '        s1["Stanley<br/>depth=foreground"]\n'
        "    end\n"
        "    subgraph BOT[BOT ground zone]\n    end\n"
        "    s1 -- left-of --> nonexistent\n"
    )
    with pytest.raises(ValueError, match="nonexistent"):
        parse_panel_layout(bad)


# --- serializer ----------------------------------------------------------------------------------------------

def test_serialize_minimal_empty_panel():
    out = serialize_panel_layout(PanelLayout(panel_id="p1", framing="medium"))
    assert "graph TB" in out
    assert 'panel["panel:p1<br/>framing=medium"]' in out
    for region in VALID_REGIONS:
        assert f"subgraph {region}[{REGION_DESCRIPTIONS[region]}]" in out
    assert "end" in out


def test_serialize_canonical_node_ids():
    layout = PanelLayout(
        panel_id="p1",
        framing="medium",
        top=[LayoutNode(name="b1", depth=None, attrs={})],
        mid=[LayoutNode(name="s1", depth="foreground"), LayoutNode(name="s2", depth="midground")],
        bot=[LayoutNode(name="h1", depth="background")],
    )
    out = serialize_panel_layout(layout)
    assert 'top_0["b1"]' in out
    assert "mid_0[" in out and "mid_1[" in out and "bot_0[" in out


def test_serialize_resolves_edges_to_canonical_ids():
    layout = PanelLayout(
        panel_id="p1",
        framing="medium",
        top=[LayoutNode(name="b1", depth=None)],
        mid=[LayoutNode(name="s1", depth="foreground")],
        bot=[],
        edges=[SpatialEdge(source="s1", target="b1", relation="speaks")],
    )
    assert "mid_0 -- speaks --> top_0" in serialize_panel_layout(layout)


def test_serialize_orders_attrs_deterministically():
    layout = PanelLayout(
        panel_id="p1",
        framing="medium",
        top=[],
        mid=[LayoutNode(name="x", depth="foreground", attrs={"zeta": "1", "alpha": "2", "mu": "3"})],
        bot=[],
    )
    out = serialize_panel_layout(layout)
    assert 'mid_0["x<br/>depth=foreground<br/>alpha=2<br/>mu=3<br/>zeta=1"]' in out


# --- round-trip ----------------------------------------------------------------------------------------------

def test_round_trip_worked_example_idempotent():
    once = serialize_panel_layout(parse_panel_layout(WORKED_EXAMPLE))
    twice = serialize_panel_layout(parse_panel_layout(once))
    assert once == twice


def test_round_trip_preserves_structural_content():
    layout = parse_panel_layout(WORKED_EXAMPLE)
    re_parsed = parse_panel_layout(serialize_panel_layout(layout))
    assert re_parsed.panel_id == layout.panel_id
    assert re_parsed.framing == layout.framing
    for region in ("top", "mid", "bot"):
        assert [(n.name, n.depth, n.attrs) for n in getattr(re_parsed, region)] == [
            (n.name, n.depth, n.attrs) for n in getattr(layout, region)
        ]
    assert [(e.source, e.target, e.relation) for e in re_parsed.edges] == [
        (e.source, e.target, e.relation) for e in layout.edges
    ]


def test_round_trip_empty_panel_idempotent():
    empty_in = _empty_panel("p_empty", "establishing")
    once = serialize_panel_layout(parse_panel_layout(empty_in))
    twice = serialize_panel_layout(parse_panel_layout(once))
    assert once == twice


# --- dual-prompt assembly ------------------------------------------------------------------------------------

def test_assemble_text_only_no_mermaid():
    out = assemble_dual_prompt(ImagePrompt(text="A serene desk scene with monitor glow."))
    assert IMAGEN_DUAL_PROMPT_WRAPPER in out
    assert "A serene desk scene with monitor glow." in out
    assert out.count("[PART 2: SPATIAL LAYOUT]") == 1  # only in the wrapper, no PART 2 section
    assert out.count("[PART 1: TEXT DESCRIPTION]") == 2  # wrapper + section header
    assert out.endswith("A serene desk scene with monitor glow.")


def test_assemble_text_and_mermaid():
    out = assemble_dual_prompt(ImagePrompt(text="Stanley at desk, Helix below.", mermaid_layout=WORKED_EXAMPLE))
    assert "Stanley at desk, Helix below." in out
    assert "graph TB" in out and "subgraph TOP" in out
    assert out.count("[PART 1: TEXT DESCRIPTION]") == 2
    assert out.count("[PART 2: SPATIAL LAYOUT]") == 2


def test_assemble_preserves_wrapper_verbatim():
    out = assemble_dual_prompt(ImagePrompt(text="x"))
    assert out.startswith("The following description has TWO parts that describe THE SAME image.")
    assert "DO NOT render the Mermaid syntax itself" in out


def test_assemble_empty_mermaid_treated_as_none():
    out = assemble_dual_prompt(ImagePrompt(text="hello", mermaid_layout=""))
    assert out.count("[PART 2: SPATIAL LAYOUT]") == 1
    assert out.endswith("hello")


def test_compositional_intent_default_none_v1_wrapper():
    out = assemble_dual_prompt(ImagePrompt(text="hello"))
    assert IMAGEN_DUAL_PROMPT_WRAPPER in out
    assert IMAGEN_DUAL_PROMPT_WRAPPER_WITH_COMPOSITIONAL_INTENT not in out
    assert "[PART 3" not in out


def test_compositional_intent_emitted_when_set():
    out = assemble_dual_prompt(ImagePrompt(text="A serene desk scene.", compositional_intent="composition_naturalness"))
    assert IMAGEN_DUAL_PROMPT_WRAPPER_WITH_COMPOSITIONAL_INTENT in out
    assert "[PART 3: COMPOSITIONAL INTENT]" in out
    assert "composition_naturalness" in out
    assert IMAGEN_DUAL_PROMPT_WRAPPER not in out
    assert out.endswith("composition_naturalness")
