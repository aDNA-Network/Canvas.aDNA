"""Tests for canvas_comic.mermaid_layout — comic_panel_layout schema parser /
serializer / dual-prompt assembly.

Mission: M-R2-02 S1 (campaign_canvasforge_review). Spec authority:
``how/campaigns/campaign_canvasforge_review/missions/artifacts/m_r2_01_dual_prompt_protocol_spec.md``
§ 2 (region grammar) · § 3 (Imagen-4 wrapper text — verbatim) · § 7.5
(substrate-placement decision: this module lives in canvas_comic, not
canvas_core).

Substrate-neutrality contract: the module under test imports only
``ImagePrompt`` from ``canvas_core.image_generation``. It does NOT import
from ``canvas_presentation`` or any other application package. The
substrate-neutrality grep + ``test_substrate_neutrality.py`` enforces this
at the directory level; this file exercises the round-trip + assembly
contract.
"""

from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path

# what/code on sys.path so canvas_core / canvas_comic resolve as
# top-level packages (parents[2] from canvas_comic/tests/).
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from canvas_comic.mermaid_layout import (  # noqa: E402
    IMAGEN_DUAL_PROMPT_WRAPPER,
    IMAGEN_DUAL_PROMPT_WRAPPER_WITH_COMPOSITIONAL_INTENT,
    LayoutNode,
    PanelLayout,
    REGION_DESCRIPTIONS,
    SpatialEdge,
    VALID_DEPTHS,
    VALID_FRAMINGS,
    VALID_REGIONS,
    VALID_RELATIONS,
    assemble_dual_prompt,
    parse_panel_layout,
    serialize_panel_layout,
)
from canvas_core.image_generation import ImagePrompt  # noqa: E402


# Fixtures ------------------------------------------------------------------


WORKED_EXAMPLE_FROM_SPEC_2_7 = """\
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


def _empty_panel_mermaid(panel_id: str = "p1", framing: str = "medium") -> str:
    """Minimal valid mermaid: panel + 3 empty subgraphs, no nodes, no edges."""
    return (
        f"graph TB\n"
        f'    panel["panel:{panel_id}<br/>framing={framing}"]\n'
        f"\n"
        f"    subgraph TOP[{REGION_DESCRIPTIONS['TOP']}]\n"
        f"    end\n"
        f"\n"
        f"    subgraph MID[{REGION_DESCRIPTIONS['MID']}]\n"
        f"    end\n"
        f"\n"
        f"    subgraph BOT[{REGION_DESCRIPTIONS['BOT']}]\n"
        f"    end\n"
    )


# TestPanelLayoutDataclasses ------------------------------------------------


class TestPanelLayoutDataclasses(unittest.TestCase):
    """Bare-dataclass shape — defaults + field types."""

    def test_panel_layout_default_lists_are_empty(self) -> None:
        layout = PanelLayout(panel_id="p1", framing="medium")
        self.assertEqual(layout.top, [])
        self.assertEqual(layout.mid, [])
        self.assertEqual(layout.bot, [])
        self.assertEqual(layout.edges, [])

    def test_layout_node_optional_depth_defaults_attrs_empty(self) -> None:
        node = LayoutNode(name="balloon-1", depth=None)
        self.assertIsNone(node.depth)
        self.assertEqual(node.attrs, {})

    def test_spatial_edge_all_seven_relations_construct_cleanly(self) -> None:
        for rel in VALID_RELATIONS:
            with self.subTest(relation=rel):
                edge = SpatialEdge(source="a", target="b", relation=rel)
                self.assertEqual(edge.relation, rel)


# TestParserBasics ----------------------------------------------------------


class TestParserBasics(unittest.TestCase):
    """Region / panel parsing — empty + single-region + populated."""

    def test_parse_minimal_panel_with_three_empty_regions(self) -> None:
        layout = parse_panel_layout(_empty_panel_mermaid("p1", "medium"))
        self.assertEqual(layout.panel_id, "p1")
        self.assertEqual(layout.framing, "medium")
        self.assertEqual(layout.top, [])
        self.assertEqual(layout.mid, [])
        self.assertEqual(layout.bot, [])
        self.assertEqual(layout.edges, [])

    def test_parse_panel_with_top_node_only(self) -> None:
        mermaid = (
            "graph TB\n"
            '    panel["panel:p2<br/>framing=close-up"]\n'
            "    subgraph TOP[TOP balloon space]\n"
            '        b1["caption<br/>type=narration"]\n'
            "    end\n"
            "    subgraph MID[MID subject zone]\n"
            "    end\n"
            "    subgraph BOT[BOT ground zone]\n"
            "    end\n"
        )
        layout = parse_panel_layout(mermaid)
        self.assertEqual(len(layout.top), 1)
        self.assertEqual(layout.top[0].name, "caption")
        self.assertEqual(layout.top[0].attrs, {"type": "narration"})

    def test_parse_panel_worked_example_all_three_regions(self) -> None:
        layout = parse_panel_layout(WORKED_EXAMPLE_FROM_SPEC_2_7)
        self.assertEqual(layout.panel_id, "p1_1")
        self.assertEqual(layout.framing, "medium")
        self.assertEqual([n.name for n in layout.top], ["balloon-1"])
        self.assertEqual([n.name for n in layout.mid], ["Stanley", "monitor"])
        self.assertEqual([n.name for n in layout.bot], ["Helix"])

    def test_parse_panel_with_blank_lines_and_comments_ignored(self) -> None:
        mermaid = (
            "graph TB\n"
            "%% leading comment\n"
            "\n"
            '    panel["panel:p3<br/>framing=wide"]\n'
            "\n"
            "    subgraph TOP[TOP balloon space]\n"
            "    end\n"
            "%% mid comment\n"
            "    subgraph MID[MID subject zone]\n"
            "    end\n"
            "    subgraph BOT[BOT ground zone]\n"
            "    end\n"
        )
        layout = parse_panel_layout(mermaid)
        self.assertEqual(layout.framing, "wide")


# TestParserAttributes ------------------------------------------------------


class TestParserAttributes(unittest.TestCase):
    """Depth + arbitrary attrs + framing enum."""

    def test_parse_node_with_depth_foreground(self) -> None:
        layout = parse_panel_layout(WORKED_EXAMPLE_FROM_SPEC_2_7)
        stanley = layout.mid[0]
        self.assertEqual(stanley.name, "Stanley")
        self.assertEqual(stanley.depth, "foreground")
        self.assertEqual(stanley.attrs, {})

    def test_parse_node_without_depth_attribute(self) -> None:
        layout = parse_panel_layout(WORKED_EXAMPLE_FROM_SPEC_2_7)
        balloon = layout.top[0]
        self.assertEqual(balloon.name, "balloon-1")
        self.assertIsNone(balloon.depth)
        self.assertEqual(balloon.attrs, {"type": "speech"})

    def test_parse_node_with_depth_and_arbitrary_attrs(self) -> None:
        layout = parse_panel_layout(WORKED_EXAMPLE_FROM_SPEC_2_7)
        helix = layout.bot[0]
        self.assertEqual(helix.depth, "background")
        self.assertEqual(helix.attrs, {"pose": "sleeping"})

    def test_parse_panel_framing_all_four_values(self) -> None:
        for framing in VALID_FRAMINGS:
            with self.subTest(framing=framing):
                mermaid = _empty_panel_mermaid("px", framing)
                layout = parse_panel_layout(mermaid)
                self.assertEqual(layout.framing, framing)


# TestParserEdges -----------------------------------------------------------


class TestParserEdges(unittest.TestCase):
    """Spatial edges — including the special `speaks` semantic."""

    def test_parse_edge_left_of_relation(self) -> None:
        layout = parse_panel_layout(WORKED_EXAMPLE_FROM_SPEC_2_7)
        edge = next(e for e in layout.edges if e.relation == "left-of")
        self.assertEqual(edge.source, "Stanley")
        self.assertEqual(edge.target, "monitor")

    def test_parse_edge_speaks_semantic_crosses_subgraphs(self) -> None:
        layout = parse_panel_layout(WORKED_EXAMPLE_FROM_SPEC_2_7)
        edge = next(e for e in layout.edges if e.relation == "speaks")
        self.assertEqual(edge.source, "Stanley")  # MID region
        self.assertEqual(edge.target, "balloon-1")  # TOP region

    def test_parse_all_seven_relations_round_trip(self) -> None:
        # Build a panel containing one edge per relation, parse, verify.
        rel_lines = []
        nodes_top = []
        nodes_mid = []
        for i, rel in enumerate(VALID_RELATIONS):
            nodes_top.append(f'        t{i}["t{i}<br/>type=marker"]')
            nodes_mid.append(f'        m{i}["m{i}<br/>depth=foreground"]')
            rel_lines.append(f"    m{i} -- {rel} --> t{i}")
        mermaid = (
            "graph TB\n"
            '    panel["panel:perel<br/>framing=medium"]\n'
            "    subgraph TOP[TOP balloon space]\n"
            + "\n".join(nodes_top)
            + "\n    end\n"
            "    subgraph MID[MID subject zone]\n"
            + "\n".join(nodes_mid)
            + "\n    end\n"
            "    subgraph BOT[BOT ground zone]\n"
            "    end\n"
            + "\n".join(rel_lines)
            + "\n"
        )
        layout = parse_panel_layout(mermaid)
        self.assertEqual(
            sorted(e.relation for e in layout.edges),
            sorted(VALID_RELATIONS),
        )


# TestParserErrors ----------------------------------------------------------


class TestParserErrors(unittest.TestCase):
    """Non-canonical mermaid raises ValueError per spec § 8 R4."""

    def test_parse_empty_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_panel_layout("")
        with self.assertRaises(ValueError):
            parse_panel_layout("   \n  \n")

    def test_parse_missing_graph_header_raises(self) -> None:
        mermaid = '    panel["panel:p1<br/>framing=medium"]\n'
        with self.assertRaises(ValueError) as ctx:
            parse_panel_layout(mermaid)
        self.assertIn("graph TB", str(ctx.exception))

    def test_parse_missing_subgraph_raises(self) -> None:
        # Only TOP + MID; BOT missing
        mermaid = (
            "graph TB\n"
            '    panel["panel:p1<br/>framing=medium"]\n'
            "    subgraph TOP[TOP balloon space]\n"
            "    end\n"
            "    subgraph MID[MID subject zone]\n"
            "    end\n"
        )
        with self.assertRaises(ValueError) as ctx:
            parse_panel_layout(mermaid)
        self.assertIn("BOT", str(ctx.exception))

    def test_parse_invalid_framing_raises(self) -> None:
        mermaid = _empty_panel_mermaid("p1", "medium").replace(
            "framing=medium", "framing=zoom"
        )
        with self.assertRaises(ValueError) as ctx:
            parse_panel_layout(mermaid)
        self.assertIn("framing", str(ctx.exception))

    def test_parse_invalid_depth_and_unknown_edge_id_raise(self) -> None:
        # depth=middlegrade is invalid
        bad_depth = (
            "graph TB\n"
            '    panel["panel:p1<br/>framing=medium"]\n'
            "    subgraph TOP[TOP balloon space]\n"
            "    end\n"
            "    subgraph MID[MID subject zone]\n"
            '        s1["Stanley<br/>depth=middlegrade"]\n'
            "    end\n"
            "    subgraph BOT[BOT ground zone]\n"
            "    end\n"
        )
        with self.assertRaises(ValueError) as ctx:
            parse_panel_layout(bad_depth)
        self.assertIn("depth", str(ctx.exception))

        # Edge references unknown id
        unknown_edge = (
            "graph TB\n"
            '    panel["panel:p1<br/>framing=medium"]\n'
            "    subgraph TOP[TOP balloon space]\n"
            "    end\n"
            "    subgraph MID[MID subject zone]\n"
            '        s1["Stanley<br/>depth=foreground"]\n'
            "    end\n"
            "    subgraph BOT[BOT ground zone]\n"
            "    end\n"
            "    s1 -- left-of --> nonexistent\n"
        )
        with self.assertRaises(ValueError) as ctx:
            parse_panel_layout(unknown_edge)
        self.assertIn("nonexistent", str(ctx.exception))


# TestSerializer ------------------------------------------------------------


class TestSerializer(unittest.TestCase):
    """Canonical re-emit — region descriptions + deterministic node IDs."""

    def test_serialize_minimal_empty_panel(self) -> None:
        layout = PanelLayout(panel_id="p1", framing="medium")
        out = serialize_panel_layout(layout)
        self.assertIn("graph TB", out)
        self.assertIn('panel["panel:p1<br/>framing=medium"]', out)
        for region in VALID_REGIONS:
            self.assertIn(
                f"subgraph {region}[{REGION_DESCRIPTIONS[region]}]", out
            )
            self.assertIn("end", out)

    def test_serialize_assigns_canonical_node_ids(self) -> None:
        layout = PanelLayout(
            panel_id="p1",
            framing="medium",
            top=[LayoutNode(name="b1", depth=None, attrs={})],
            mid=[
                LayoutNode(name="s1", depth="foreground"),
                LayoutNode(name="s2", depth="midground"),
            ],
            bot=[LayoutNode(name="h1", depth="background")],
        )
        out = serialize_panel_layout(layout)
        self.assertIn('top_0["b1"]', out)
        self.assertIn("mid_0[", out)
        self.assertIn("mid_1[", out)
        self.assertIn("bot_0[", out)

    def test_serialize_resolves_edges_to_canonical_ids(self) -> None:
        layout = PanelLayout(
            panel_id="p1",
            framing="medium",
            top=[LayoutNode(name="b1", depth=None)],
            mid=[LayoutNode(name="s1", depth="foreground")],
            bot=[],
            edges=[SpatialEdge(source="s1", target="b1", relation="speaks")],
        )
        out = serialize_panel_layout(layout)
        self.assertIn("mid_0 -- speaks --> top_0", out)

    def test_serialize_orders_attrs_deterministically(self) -> None:
        layout = PanelLayout(
            panel_id="p1",
            framing="medium",
            top=[],
            mid=[
                LayoutNode(
                    name="x",
                    depth="foreground",
                    attrs={"zeta": "1", "alpha": "2", "mu": "3"},
                )
            ],
            bot=[],
        )
        out = serialize_panel_layout(layout)
        # alpha < mu < zeta lexicographically
        self.assertIn(
            'mid_0["x<br/>depth=foreground<br/>alpha=2<br/>mu=3<br/>zeta=1"]',
            out,
        )


# TestRoundTrip -------------------------------------------------------------


class TestRoundTrip(unittest.TestCase):
    """``serialize(parse(serialize(parse(s)))) == serialize(parse(s))`` —
    idempotent normalization."""

    def test_round_trip_worked_example_idempotent(self) -> None:
        once = serialize_panel_layout(parse_panel_layout(WORKED_EXAMPLE_FROM_SPEC_2_7))
        twice = serialize_panel_layout(parse_panel_layout(once))
        self.assertEqual(once, twice)

    def test_round_trip_preserves_structural_content(self) -> None:
        layout = parse_panel_layout(WORKED_EXAMPLE_FROM_SPEC_2_7)
        re_emitted = serialize_panel_layout(layout)
        re_parsed = parse_panel_layout(re_emitted)
        self.assertEqual(re_parsed.panel_id, layout.panel_id)
        self.assertEqual(re_parsed.framing, layout.framing)
        self.assertEqual(
            [(n.name, n.depth, n.attrs) for n in re_parsed.top],
            [(n.name, n.depth, n.attrs) for n in layout.top],
        )
        self.assertEqual(
            [(n.name, n.depth, n.attrs) for n in re_parsed.mid],
            [(n.name, n.depth, n.attrs) for n in layout.mid],
        )
        self.assertEqual(
            [(n.name, n.depth, n.attrs) for n in re_parsed.bot],
            [(n.name, n.depth, n.attrs) for n in layout.bot],
        )
        self.assertEqual(
            [(e.source, e.target, e.relation) for e in re_parsed.edges],
            [(e.source, e.target, e.relation) for e in layout.edges],
        )

    def test_round_trip_empty_panel_idempotent(self) -> None:
        empty_in = _empty_panel_mermaid("p_empty", "establishing")
        once = serialize_panel_layout(parse_panel_layout(empty_in))
        twice = serialize_panel_layout(parse_panel_layout(once))
        self.assertEqual(once, twice)


# TestAssembleDualPrompt ----------------------------------------------------


class TestAssembleDualPrompt(unittest.TestCase):
    """Strategy 1 wrapper concatenation — wrapper + PART 1 + PART 2."""

    def test_assemble_with_text_only_no_mermaid(self) -> None:
        ip = ImagePrompt(text="A serene desk scene with monitor glow.")
        out = assemble_dual_prompt(ip)
        self.assertIn(IMAGEN_DUAL_PROMPT_WRAPPER, out)
        self.assertIn("A serene desk scene with monitor glow.", out)
        # Wrapper text itself contains the literal "[PART 2: SPATIAL LAYOUT]"
        # marker once (as referential text describing the structure). When the
        # actual PART 2 section is omitted, total count must remain 1.
        self.assertEqual(out.count("[PART 2: SPATIAL LAYOUT]"), 1)
        # PART 1 marker appears in wrapper + as section header → 2 occurrences
        self.assertEqual(out.count("[PART 1: TEXT DESCRIPTION]"), 2)
        # The output must end with the user text (no trailing PART 2 block)
        self.assertTrue(out.endswith("A serene desk scene with monitor glow."))

    def test_assemble_with_text_and_mermaid(self) -> None:
        ip = ImagePrompt(
            text="Stanley at desk, Helix below.",
            mermaid_layout=WORKED_EXAMPLE_FROM_SPEC_2_7,
        )
        out = assemble_dual_prompt(ip)
        self.assertIn("Stanley at desk, Helix below.", out)
        self.assertIn("graph TB", out)
        self.assertIn("subgraph TOP", out)
        # Both markers appear in wrapper (1×) and as section headers (1× each)
        self.assertEqual(out.count("[PART 1: TEXT DESCRIPTION]"), 2)
        self.assertEqual(out.count("[PART 2: SPATIAL LAYOUT]"), 2)

    def test_assemble_preserves_wrapper_verbatim(self) -> None:
        ip = ImagePrompt(text="x")
        out = assemble_dual_prompt(ip)
        # Spec § 3 verbatim leading line
        self.assertTrue(
            out.startswith(
                "The following description has TWO parts that describe THE SAME image."
            )
        )
        # Negative clause (DO NOT render the Mermaid syntax) — last paragraph
        self.assertIn("DO NOT render the Mermaid syntax itself", out)

    def test_assemble_empty_mermaid_string_treated_as_none(self) -> None:
        # mermaid_layout="" (empty string falsy) → degrade to single-prompt:
        # PART 2 marker appears only once (in wrapper), not twice.
        ip = ImagePrompt(text="hello", mermaid_layout="")
        out = assemble_dual_prompt(ip)
        self.assertEqual(out.count("[PART 2: SPATIAL LAYOUT]"), 1)
        self.assertTrue(out.endswith("hello"))

    # M-V1-2-F-01 S5 (2026-05-26) — compositional_intent third dual-prompt
    # segment per ADR-005 § D5 amendment. Default-None preserves baseline;
    # set-value switches to V2 wrapper + appends PART 3 section.

    def test_compositional_intent_default_none_preserves_s4_baseline(self) -> None:
        # Assemble with compositional_intent=None must emit V1 wrapper
        # verbatim and zero PART 3 markers — the re-baseline gate
        # (Q5 + CR1 + CR2) guarantee.
        ip = ImagePrompt(text="hello")
        out = assemble_dual_prompt(ip)
        self.assertIn(IMAGEN_DUAL_PROMPT_WRAPPER, out)
        self.assertNotIn(IMAGEN_DUAL_PROMPT_WRAPPER_WITH_COMPOSITIONAL_INTENT, out)
        self.assertNotIn("[PART 3", out)

    def test_compositional_intent_emitted_when_set(self) -> None:
        # Set compositional_intent → V2 wrapper + PART 3 section appended.
        ip = ImagePrompt(
            text="A serene desk scene.",
            compositional_intent="composition_naturalness",
        )
        out = assemble_dual_prompt(ip)
        self.assertIn(IMAGEN_DUAL_PROMPT_WRAPPER_WITH_COMPOSITIONAL_INTENT, out)
        self.assertIn("[PART 3: COMPOSITIONAL INTENT]", out)
        self.assertIn("composition_naturalness", out)
        # V1 wrapper must NOT also be present (V2 supersedes it on this path)
        self.assertNotIn(IMAGEN_DUAL_PROMPT_WRAPPER, out)
        # Output ends with the intent text (last section)
        self.assertTrue(out.endswith("composition_naturalness"))

    def test_panel_layout_compositional_intent_field_default_none(self) -> None:
        # PanelLayout gains a compositional_intent: str | None = None field
        # at S5. Default None preserves dataclass construction shape; explicit
        # value round-trips through the dataclass.
        layout_default = PanelLayout(panel_id="p1", framing="medium")
        self.assertIsNone(layout_default.compositional_intent)
        layout_with_intent = PanelLayout(
            panel_id="p2",
            framing="wide",
            compositional_intent="crowd_depth_refinement",
        )
        self.assertEqual(
            layout_with_intent.compositional_intent, "crowd_depth_refinement"
        )


# TestImagePromptDataclass --------------------------------------------------


class TestImagePromptDataclass(unittest.TestCase):
    """Substrate-side ImagePrompt dataclass shape (per spec § 7.1)."""

    def test_image_prompt_text_only_default_aspect(self) -> None:
        ip = ImagePrompt(text="hello")
        self.assertEqual(ip.text, "hello")
        self.assertIsNone(ip.mermaid_layout)
        self.assertEqual(ip.aspect_ratio, "1:1")

    def test_image_prompt_full_construction(self) -> None:
        ip = ImagePrompt(
            text="hello",
            mermaid_layout="graph TB\n    a-->b\n",
            aspect_ratio="16:9",
        )
        self.assertEqual(ip.text, "hello")
        self.assertEqual(ip.mermaid_layout, "graph TB\n    a-->b\n")
        self.assertEqual(ip.aspect_ratio, "16:9")


if __name__ == "__main__":
    unittest.main()
