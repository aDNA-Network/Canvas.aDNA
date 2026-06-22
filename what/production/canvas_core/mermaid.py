"""MermaidGenerator — programmatic Mermaid diagram generation with theme integration.

Generates Mermaid syntax from structured data, applies Obsidian canvas theme
directives, and provides lightweight validation. Designed for use with
PresentationBuilder but independently testable.

Migrated from lattice-protocol/extensions/canvas/canvas_mermaid.py (M-1-03).
TYPE_CHECKING import of PresentationTheme retained per ADR 001 § Borderline
Files (TYPE_CHECKING imports are import-time no-ops).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .html_renderer import PresentationTheme


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class MermaidNode:
    """A node in a Mermaid flowchart or state diagram."""

    id: str
    label: str
    shape: str = "rect"  # rect, round, diamond, stadium, circle


@dataclass
class MermaidEdge:
    """An edge connecting two Mermaid nodes."""

    from_id: str
    to_id: str
    label: str = ""
    style: str = "-->"  # -->, --->, -.->. ==>


# ---------------------------------------------------------------------------
# Shape wrappers for Mermaid syntax
# ---------------------------------------------------------------------------

_SHAPE_WRAP: dict[str, tuple[str, str]] = {
    "rect": ("[", "]"),
    "round": ("(", ")"),
    "diamond": ("{", "}"),
    "stadium": ("([", "])"),
    "circle": ("((", "))"),
}


# ---------------------------------------------------------------------------
# MermaidGenerator
# ---------------------------------------------------------------------------


class MermaidGenerator:
    """Programmatic Mermaid diagram generation with theme support."""

    # Canvas color index → hex (matches Obsidian's 6 built-in colors)
    CANVAS_COLOR_HEX: dict[str, str] = {
        "1": "#fb464c",
        "2": "#e9973f",
        "3": "#e0de71",
        "4": "#44cf6e",
        "5": "#53dfdd",
        "6": "#a882ff",
    }

    # ----- Diagram generators -----

    @staticmethod
    def flowchart(
        nodes: list[MermaidNode],
        edges: list[MermaidEdge],
        direction: str = "TD",
    ) -> str:
        """Generate a Mermaid flowchart.

        Args:
            nodes: List of MermaidNode objects.
            edges: List of MermaidEdge objects.
            direction: Flow direction — TD, LR, RL, BT.
        """
        if direction not in ("TD", "LR", "RL", "BT"):
            direction = "TD"

        lines = [f"flowchart {direction}"]
        for node in nodes:
            left, right = _SHAPE_WRAP.get(node.shape, ("[", "]"))
            lines.append(f'    {node.id}{left}"{node.label}"{right}')
        for edge in edges:
            if edge.label:
                lines.append(f"    {edge.from_id} {edge.style}|{edge.label}| {edge.to_id}")
            else:
                lines.append(f"    {edge.from_id} {edge.style} {edge.to_id}")
        return "\n".join(lines)

    @staticmethod
    def sequence(
        participants: list[str],
        messages: list[tuple[str, str, str]],
    ) -> str:
        """Generate a Mermaid sequence diagram.

        Args:
            participants: List of participant names.
            messages: List of (from, to, message) tuples.
        """
        lines = ["sequenceDiagram"]
        for p in participants:
            lines.append(f"    participant {p}")
        for frm, to, msg in messages:
            lines.append(f"    {frm}->>+{to}: {msg}")
        return "\n".join(lines)

    @staticmethod
    def class_diagram(
        classes: list[tuple[str, list[str]]],
        relationships: list[tuple[str, str, str]],
    ) -> str:
        """Generate a Mermaid class diagram.

        Args:
            classes: List of (class_name, [attributes]) tuples.
            relationships: List of (from_class, relation, to_class) tuples.
                relation examples: "--|>", "..|>", "--*", "--o"
        """
        lines = ["classDiagram"]
        for cls_name, attrs in classes:
            lines.append(f"    class {cls_name} {{")
            for attr in attrs:
                lines.append(f"        {attr}")
            lines.append("    }")
        for frm, rel, to in relationships:
            lines.append(f"    {frm} {rel} {to}")
        return "\n".join(lines)

    @staticmethod
    def state_diagram(
        states: list[str],
        transitions: list[tuple[str, str, str]],
    ) -> str:
        """Generate a Mermaid state diagram.

        Args:
            states: List of state names.
            transitions: List of (from_state, to_state, label) tuples.
                Use "[*]" for start/end pseudo-states.
        """
        lines = ["stateDiagram-v2"]
        for state in states:
            if state != "[*]":
                lines.append(f"    {state}")
        for frm, to, label in transitions:
            if label:
                lines.append(f"    {frm} --> {to} : {label}")
            else:
                lines.append(f"    {frm} --> {to}")
        return "\n".join(lines)

    @staticmethod
    def gantt(
        title: str,
        sections: list[tuple[str, list[tuple[str, str]]]],
    ) -> str:
        """Generate a Mermaid Gantt chart.

        Args:
            title: Chart title.
            sections: List of (section_name, [(task_name, duration)]) tuples.
                duration examples: "2d", "1w", "3h"
        """
        lines = ["gantt"]
        if title:
            lines.append(f"    title {title}")
        lines.append("    dateFormat YYYY-MM-DD")
        for section_name, tasks in sections:
            lines.append(f"    section {section_name}")
            for task_name, duration in tasks:
                lines.append(f"        {task_name} : {duration}")
        return "\n".join(lines)

    # ----- Theme methods -----

    @classmethod
    def theme_directive(cls, theme: PresentationTheme) -> str:
        """Build a Mermaid init directive from a PresentationTheme.

        Maps canvas color codes to hex values for Mermaid theming.
        """
        primary = cls.CANVAS_COLOR_HEX.get(theme.primary_color, theme.primary_color)
        secondary = cls.CANVAS_COLOR_HEX.get(theme.secondary_color, theme.secondary_color)
        accent = cls.CANVAS_COLOR_HEX.get(theme.accent_color, theme.accent_color)
        return (
            "%%{init: {'theme': 'base', 'themeVariables': {"
            f"'primaryColor': '{primary}', "
            f"'secondaryColor': '{secondary}', "
            f"'tertiaryColor': '{accent}'"
            "}}}%%"
        )

    @classmethod
    def apply_theme(cls, mermaid_src: str, theme: PresentationTheme) -> str:
        """Prepend a theme directive to Mermaid source.

        If the source already contains an init directive, returns unchanged.
        """
        if "%%{init:" in mermaid_src:
            return mermaid_src
        directive = cls.theme_directive(theme)
        return f"{directive}\n{mermaid_src}"

    # ----- Conversion methods (structured data → Mermaid) -----

    @classmethod
    def process_to_flowchart(
        cls,
        steps: list[str],
        direction: str = "TD",
    ) -> str:
        """Convert a list of process steps into a flowchart.

        Each step becomes a stadium-shaped node connected sequentially.
        """
        nodes = [
            MermaidNode(id=f"S{i}", label=step, shape="stadium") for i, step in enumerate(steps)
        ]
        edges = [MermaidEdge(from_id=f"S{i}", to_id=f"S{i + 1}") for i in range(len(steps) - 1)]
        return cls.flowchart(nodes, edges, direction=direction)

    @classmethod
    def timeline_to_gantt(
        cls,
        events: list[tuple[str, str]],
        title: str = "",
    ) -> str:
        """Convert timeline events into a Gantt chart.

        Args:
            events: List of (label, description) tuples.
            title: Optional chart title.
        """
        tasks = [(f"{label}: {desc}", "1d") for label, desc in events]
        section_name = title or "Timeline"
        return cls.gantt(title=title, sections=[(section_name, tasks)])

    # ----- Validation -----

    @staticmethod
    def validate(mermaid_src: str) -> list[str]:
        """Lightweight validation of Mermaid source.

        Returns a list of warning strings. Empty list = no issues detected.
        """
        warnings: list[str] = []
        stripped = mermaid_src.strip()

        # Remove init directive for type check
        check_src = stripped
        if check_src.startswith("%%{"):
            newline_idx = check_src.find("\n")
            if newline_idx >= 0:
                check_src = check_src[newline_idx + 1 :].strip()

        # Check for diagram type declaration
        known_types = (
            "flowchart",
            "graph",
            "sequenceDiagram",
            "classDiagram",
            "stateDiagram",
            "stateDiagram-v2",
            "gantt",
            "pie",
            "erDiagram",
            "journey",
            "gitGraph",
            "mindmap",
            "timeline",
        )
        first_line = check_src.split("\n")[0].strip() if check_src else ""
        has_type = any(first_line.startswith(t) for t in known_types)
        if not has_type:
            warnings.append(
                f"No recognized diagram type declaration found. First line: {first_line!r}"
            )

        # Check balanced brackets
        for open_ch, close_ch, name in [
            ("{", "}", "braces"),
            ("(", ")", "parentheses"),
            ("[", "]", "brackets"),
        ]:
            opens = stripped.count(open_ch)
            closes = stripped.count(close_ch)
            if opens != closes:
                warnings.append(f"Unbalanced {name}: {opens} opening vs {closes} closing")

        return warnings
