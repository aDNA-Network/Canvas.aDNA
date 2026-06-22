"""Tests for MermaidGenerator — diagram generation, theming, and validation.

Migrated from `lattice-protocol/extensions/canvas/tests/test_canvas_mermaid.py`
under M-R5-01a (campaign_canvasforge_review). Pure substrate — uses
`canvas_core/html_renderer.py::PresentationTheme` + the substrate-resident
THEME_TOKYO_NIGHT/SCIENTIFIC/LATTICE_BRAND copies (no canvas_presentation imports).

Part of campaign_presentation_excellence M10a (upstream).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import pytest

from canvas_core.mermaid import MermaidEdge, MermaidGenerator, MermaidNode
from canvas_core.html_renderer import (
    PresentationTheme,
    THEME_LATTICE_BRAND,
    THEME_SCIENTIFIC,
    THEME_TOKYO_NIGHT,
)


@pytest.fixture
def gen():
    return MermaidGenerator()


# ---------------------------------------------------------------------------
# Flowchart generation
# ---------------------------------------------------------------------------


class TestFlowchart:
    def test_basic_flowchart(self):
        nodes = [
            MermaidNode("A", "Start"),
            MermaidNode("B", "End"),
        ]
        edges = [MermaidEdge("A", "B")]
        result = MermaidGenerator.flowchart(nodes, edges)
        assert result.startswith("flowchart TD")
        assert 'A["Start"]' in result
        assert 'B["End"]' in result
        assert "A --> B" in result

    def test_flowchart_lr_direction(self):
        nodes = [MermaidNode("X", "Node")]
        result = MermaidGenerator.flowchart(nodes, [], direction="LR")
        assert result.startswith("flowchart LR")

    def test_flowchart_invalid_direction_defaults_td(self):
        result = MermaidGenerator.flowchart([], [], direction="ZZ")
        assert result.startswith("flowchart TD")

    def test_flowchart_shapes(self):
        nodes = [
            MermaidNode("A", "Rect", shape="rect"),
            MermaidNode("B", "Round", shape="round"),
            MermaidNode("C", "Diamond", shape="diamond"),
            MermaidNode("D", "Stadium", shape="stadium"),
            MermaidNode("E", "Circle", shape="circle"),
        ]
        result = MermaidGenerator.flowchart(nodes, [])
        assert 'A["Rect"]' in result
        assert 'B("Round")' in result
        assert 'C{"Diamond"}' in result
        assert 'D(["Stadium"])' in result
        assert 'E(("Circle"))' in result

    def test_flowchart_edge_labels(self):
        edges = [MermaidEdge("A", "B", label="yes")]
        result = MermaidGenerator.flowchart(
            [MermaidNode("A", "Q"), MermaidNode("B", "R")],
            edges,
        )
        assert "A -->|yes| B" in result

    def test_flowchart_empty(self):
        result = MermaidGenerator.flowchart([], [])
        assert result == "flowchart TD"


# ---------------------------------------------------------------------------
# Sequence diagram
# ---------------------------------------------------------------------------


class TestSequence:
    def test_basic_sequence(self):
        result = MermaidGenerator.sequence(
            participants=["Alice", "Bob"],
            messages=[("Alice", "Bob", "Hello")],
        )
        assert "sequenceDiagram" in result
        assert "participant Alice" in result
        assert "participant Bob" in result
        assert "Alice->>+Bob: Hello" in result

    def test_sequence_multiple_messages(self):
        result = MermaidGenerator.sequence(
            participants=["A", "B", "C"],
            messages=[("A", "B", "req"), ("B", "C", "fwd")],
        )
        assert result.count("->>+") == 2


# ---------------------------------------------------------------------------
# Class diagram
# ---------------------------------------------------------------------------


class TestClassDiagram:
    def test_basic_class_diagram(self):
        result = MermaidGenerator.class_diagram(
            classes=[("Animal", ["+name: str", "+speak()"])],
            relationships=[],
        )
        assert "classDiagram" in result
        assert "class Animal {" in result
        assert "+name: str" in result

    def test_class_relationships(self):
        result = MermaidGenerator.class_diagram(
            classes=[("Dog", []), ("Animal", [])],
            relationships=[("Dog", "--|>", "Animal")],
        )
        assert "Dog --|> Animal" in result


# ---------------------------------------------------------------------------
# State diagram
# ---------------------------------------------------------------------------


class TestStateDiagram:
    def test_basic_state_diagram(self):
        result = MermaidGenerator.state_diagram(
            states=["Idle", "Running"],
            transitions=[("[*]", "Idle", ""), ("Idle", "Running", "start")],
        )
        assert "stateDiagram-v2" in result
        assert "Idle" in result
        assert "[*] --> Idle" in result
        assert "Idle --> Running : start" in result

    def test_start_state_not_declared(self):
        """[*] pseudo-state should not appear as a state declaration."""
        result = MermaidGenerator.state_diagram(
            states=["[*]", "Active"],
            transitions=[],
        )
        lines = result.split("\n")
        state_lines = [ln.strip() for ln in lines if ln.strip() and ln.strip() != "stateDiagram-v2"]
        assert "[*]" not in [ln for ln in state_lines if not ln.startswith("[*] -->")]


# ---------------------------------------------------------------------------
# Gantt chart
# ---------------------------------------------------------------------------


class TestGantt:
    def test_basic_gantt(self):
        result = MermaidGenerator.gantt(
            title="Project",
            sections=[("Phase 1", [("Task A", "2d"), ("Task B", "3d")])],
        )
        assert "gantt" in result
        assert "title Project" in result
        assert "section Phase 1" in result
        assert "Task A : 2d" in result

    def test_gantt_no_title(self):
        result = MermaidGenerator.gantt(
            title="",
            sections=[("Work", [("Do thing", "1d")])],
        )
        assert "title" not in result


# ---------------------------------------------------------------------------
# Theme directive
# ---------------------------------------------------------------------------


class TestTheme:
    def test_theme_directive_tokyo_night(self):
        directive = MermaidGenerator.theme_directive(THEME_TOKYO_NIGHT)
        assert "%%{init:" in directive
        assert "'theme': 'base'" in directive
        # Tokyo Night: primary=6 → #a882ff
        assert "#a882ff" in directive

    def test_theme_directive_lattice_brand(self):
        directive = MermaidGenerator.theme_directive(THEME_LATTICE_BRAND)
        assert "#a882ff" in directive  # primary_color="6"
        assert "#44cf6e" in directive  # secondary_color="4"
        assert "#fb464c" in directive  # accent_color="1"

    def test_theme_directive_scientific(self):
        directive = MermaidGenerator.theme_directive(THEME_SCIENTIFIC)
        assert "#53dfdd" in directive  # primary_color="5"

    def test_apply_theme_prepends(self):
        src = "flowchart TD\n    A --> B"
        themed = MermaidGenerator.apply_theme(src, THEME_TOKYO_NIGHT)
        assert themed.startswith("%%{init:")
        assert themed.endswith(src)

    def test_apply_theme_idempotent(self):
        """If source already has init directive, don't double-apply."""
        src = "%%{init: {'theme': 'dark'}}%%\nflowchart TD\n    A --> B"
        result = MermaidGenerator.apply_theme(src, THEME_TOKYO_NIGHT)
        assert result == src

    def test_color_hex_mapping_all_six(self):
        """All 6 canvas colors should have hex mappings."""
        assert len(MermaidGenerator.CANVAS_COLOR_HEX) == 6
        for key in ("1", "2", "3", "4", "5", "6"):
            assert key in MermaidGenerator.CANVAS_COLOR_HEX
            assert MermaidGenerator.CANVAS_COLOR_HEX[key].startswith("#")

    def test_custom_hex_passthrough(self):
        """If theme uses hex directly instead of canvas index, pass through."""
        theme = PresentationTheme(
            name="custom",
            primary_color="#ff0000",
            secondary_color="#00ff00",
            accent_color="#0000ff",
        )
        directive = MermaidGenerator.theme_directive(theme)
        assert "#ff0000" in directive
        assert "#00ff00" in directive
        assert "#0000ff" in directive


# ---------------------------------------------------------------------------
# Conversion methods
# ---------------------------------------------------------------------------


class TestConversion:
    def test_process_to_flowchart(self):
        steps = ["Collect", "Analyze", "Report"]
        result = MermaidGenerator.process_to_flowchart(steps)
        assert "flowchart TD" in result
        assert "Collect" in result
        assert "Analyze" in result
        assert "Report" in result
        # 3 steps → 2 edges
        assert result.count("-->") == 2

    def test_process_to_flowchart_lr(self):
        result = MermaidGenerator.process_to_flowchart(["A", "B"], direction="LR")
        assert "flowchart LR" in result

    def test_process_single_step(self):
        result = MermaidGenerator.process_to_flowchart(["Only"])
        assert "Only" in result
        assert "-->" not in result

    def test_timeline_to_gantt(self):
        events = [("Q1", "Launch"), ("Q2", "Scale")]
        result = MermaidGenerator.timeline_to_gantt(events, title="Roadmap")
        assert "gantt" in result
        assert "title Roadmap" in result
        assert "Q1: Launch" in result
        assert "Q2: Scale" in result


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidation:
    def test_valid_flowchart(self):
        src = "flowchart TD\n    A[Start] --> B[End]"
        warnings = MermaidGenerator.validate(src)
        assert warnings == []

    def test_missing_type_declaration(self):
        src = "A --> B"
        warnings = MermaidGenerator.validate(src)
        assert len(warnings) == 1
        assert "diagram type" in warnings[0].lower()

    def test_unbalanced_brackets(self):
        src = "flowchart TD\n    A[Start --> B[End]"
        warnings = MermaidGenerator.validate(src)
        assert any("brackets" in w.lower() for w in warnings)

    def test_unbalanced_braces(self):
        src = "flowchart TD\n    A{Decision"
        warnings = MermaidGenerator.validate(src)
        assert any("braces" in w.lower() for w in warnings)

    def test_valid_with_init_directive(self):
        src = "%%{init: {'theme': 'base'}}%%\nflowchart TD\n    A --> B"
        warnings = MermaidGenerator.validate(src)
        assert warnings == []

    def test_empty_source(self):
        warnings = MermaidGenerator.validate("")
        assert len(warnings) >= 1

    def test_all_diagram_types_recognized(self):
        """Each known type should pass the type declaration check."""
        for dtype in [
            "flowchart TD",
            "graph LR",
            "sequenceDiagram",
            "classDiagram",
            "stateDiagram-v2",
            "gantt",
        ]:
            src = f"{dtype}\n    placeholder"
            warnings = MermaidGenerator.validate(src)
            type_warnings = [w for w in warnings if "diagram type" in w.lower()]
            assert type_warnings == [], f"{dtype} should be recognized"
