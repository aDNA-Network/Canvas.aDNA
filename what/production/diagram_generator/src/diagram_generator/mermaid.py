"""Mermaid syntax generation — PORTED from the CanvasForge quarry, theme coupling stripped.

Source (KEEP-reference, NOT a dependency): ``Archive.aDNA/CanvasForge.aDNA/what/code/canvas_core/mermaid.py``
(``MermaidGenerator``). The five static generators (``flowchart`` / ``sequence`` / ``class_diagram`` /
``state_diagram`` / ``gantt``), the ``_SHAPE_WRAP`` table, and the lightweight ``validate()`` helper are carried over
verbatim in behavior; everything coupling to ``PresentationTheme`` / ``apply_theme`` / ``CANVAS_COLOR_HEX`` (theme +
the HTML renderer) was DROPPED — this module is pure string output and imports nothing from the substrate.

Retyped to consume the new substrate-free ``DiagramNode`` / ``DiagramEdge`` (``model.py``); ``mermaid_for`` is a thin
adapter that turns a whole ``DiagramInput`` into a Mermaid source string for the derived ``code`` node.
"""

from __future__ import annotations

from diagram_generator.model import DiagramEdge, DiagramInput, DiagramNode

# Shape wrappers for Mermaid syntax (verbatim from the quarry).
_SHAPE_WRAP: dict[str, tuple[str, str]] = {
    "rect": ("[", "]"),
    "round": ("(", ")"),
    "diamond": ("{", "}"),
    "stadium": ("([", "])"),
    "circle": ("((", "))"),
}

# Domain relation -> Mermaid class-diagram relation glyph (class_diagram only).
_CLASS_REL: dict[str, str] = {
    "inherits": "--|>",
    "realizes": "..|>",
    "composition": "--*",
    "aggregation": "--o",
    "dependency": "..>",
    "association": "-->",
    "flow": "-->",
}


def flowchart(nodes: list[DiagramNode], edges: list[DiagramEdge], direction: str = "TD") -> str:
    """Generate a Mermaid flowchart (direction ∈ TD, LR, RL, BT)."""
    if direction not in ("TD", "LR", "RL", "BT"):
        direction = "TD"
    lines = [f"flowchart {direction}"]
    for node in nodes:
        left, right = _SHAPE_WRAP.get(node.shape, ("[", "]"))
        lines.append(f'    {node.id}{left}"{node.label}"{right}')
    for edge in edges:
        if edge.label:
            lines.append(f"    {edge.from_id} -->|{edge.label}| {edge.to_id}")
        else:
            lines.append(f"    {edge.from_id} --> {edge.to_id}")
    return "\n".join(lines)


def sequence(nodes: list[DiagramNode], edges: list[DiagramEdge]) -> str:
    """Generate a Mermaid sequence diagram. Nodes are participants; edges are messages (in declared order)."""
    lines = ["sequenceDiagram"]
    for n in nodes:
        lines.append(f"    participant {n.id}")
    for e in edges:
        msg = e.label or e.relation
        lines.append(f"    {e.from_id}->>+{e.to_id}: {msg}")
    return "\n".join(lines)


def class_diagram(nodes: list[DiagramNode], edges: list[DiagramEdge]) -> str:
    """Generate a Mermaid class diagram. Node ``members`` are class attributes; edge ``relation`` -> glyph."""
    lines = ["classDiagram"]
    for n in nodes:
        lines.append(f"    class {n.id} {{")
        for attr in n.members:
            lines.append(f"        {attr}")
        lines.append("    }")
    for e in edges:
        glyph = _CLASS_REL.get(e.relation, "-->")
        if e.label:
            lines.append(f"    {e.from_id} {glyph} {e.to_id} : {e.label}")
        else:
            lines.append(f"    {e.from_id} {glyph} {e.to_id}")
    return "\n".join(lines)


def state_diagram(nodes: list[DiagramNode], edges: list[DiagramEdge]) -> str:
    """Generate a Mermaid state diagram. Use the id ``[*]`` for start/end pseudo-states."""
    lines = ["stateDiagram-v2"]
    for n in nodes:
        if n.id != "[*]":
            lines.append(f"    {n.id}")
    for e in edges:
        if e.label:
            lines.append(f"    {e.from_id} --> {e.to_id} : {e.label}")
        else:
            lines.append(f"    {e.from_id} --> {e.to_id}")
    return "\n".join(lines)


def gantt(title: str, nodes: list[DiagramNode], edges: list[DiagramEdge]) -> str:
    """Generate a Mermaid Gantt chart. Each node is a task; its ``label`` carries the duration (e.g. ``2d``)."""
    lines = ["gantt"]
    if title:
        lines.append(f"    title {title}")
    lines.append("    dateFormat YYYY-MM-DD")
    lines.append("    section Tasks")
    for n in nodes:
        duration = n.label or "1d"
        lines.append(f"        {n.id} : {duration}")
    return "\n".join(lines)


def mermaid_for(d: DiagramInput) -> str:
    """Adapter: render a whole ``DiagramInput`` to its Mermaid source string (for the derived ``code`` node)."""
    nodes = list(d.nodes)
    edges = list(d.edges)
    if d.diagram_type == "flowchart":
        return flowchart(nodes, edges, d.direction)
    if d.diagram_type == "sequence":
        return sequence(nodes, edges)
    if d.diagram_type == "class_diagram":
        return class_diagram(nodes, edges)
    if d.diagram_type == "state_diagram":
        return state_diagram(nodes, edges)
    if d.diagram_type == "gantt":
        return gantt(d.title, nodes, edges)
    raise ValueError(f"no Mermaid generator for diagram_type {d.diagram_type!r}")


def validate(mermaid_src: str) -> list[str]:
    """Lightweight validation of Mermaid source (verbatim from the quarry). [] == no issues detected."""
    warnings: list[str] = []
    stripped = mermaid_src.strip()

    check_src = stripped
    if check_src.startswith("%%{"):
        newline_idx = check_src.find("\n")
        if newline_idx >= 0:
            check_src = check_src[newline_idx + 1 :].strip()

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
    if not any(first_line.startswith(t) for t in known_types):
        warnings.append(f"No recognized diagram type declaration found. First line: {first_line!r}")

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
