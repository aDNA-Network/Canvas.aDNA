"""Comic-application spatial layout for the dual-prompt protocol — PORTED from the CanvasForge quarry, near-verbatim.

The ``comic_panel_layout`` Mermaid schema (TOP/MID/BOT region enum + DEPTH + FRAMING grammar) is comic-specific. The
parser/serializer + dataclasses are carried over from ``Archive.aDNA/CanvasForge.aDNA/what/code/canvas_comic/
mermaid_layout.py`` essentially verbatim — the only change is dropping ``from canvas_core.image_generation import
ImagePrompt`` (substrate dependency in the old world) in favor of a small local ``ImagePrompt`` dataclass (defined in
``prompt.py`` and re-exported here). All of ``parse_panel_layout`` / ``serialize_panel_layout`` /
``assemble_dual_prompt`` is pure string/regex work — no ``canvas_std`` import, no I/O.

The parser/serializer round-trip is load-bearing for III consumption (the parsed ``PanelLayout`` feeds a future
compositional-grounding review lens). ``serialize(parse(serialize(parse(s)))) == serialize(parse(s))`` is idempotent.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Literal

from comic_generator.prompt import ImagePrompt

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

VALID_REGIONS: tuple[str, ...] = ("TOP", "MID", "BOT")
VALID_FRAMINGS: tuple[str, ...] = ("close-up", "medium", "wide", "establishing")
VALID_DEPTHS: tuple[str, ...] = ("foreground", "midground", "background")
VALID_RELATIONS: tuple[str, ...] = (
    "left-of", "right-of", "above", "below", "contains", "overlaps", "speaks",
)

REGION_DESCRIPTIONS: dict[str, str] = {
    "TOP": "TOP balloon space",
    "MID": "MID subject zone",
    "BOT": "BOT ground zone",
}


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class LayoutNode:
    """A single visual element inside a region (TOP / MID / BOT)."""

    name: str
    depth: Literal["foreground", "midground", "background"] | None
    attrs: dict[str, str] = field(default_factory=dict)


@dataclass
class SpatialEdge:
    """A spatial relationship between two nodes (within or across regions)."""

    source: str  # display name
    target: str  # display name
    relation: Literal[
        "left-of", "right-of", "above", "below", "contains", "overlaps", "speaks"
    ]


@dataclass
class PanelLayout:
    """Structured spatial layout for one comic panel.

    Maps to / from the ``comic_panel_layout`` Mermaid schema. Carries panel-id + framing + nodes-by-region + edges.
    The optional ``compositional_intent`` carries a free-text compositional anchor at the authoring surface; it is NOT
    serialized into the Mermaid emission (the panel label stays purely spatial). Application code threads the value
    onto the corresponding ``ImagePrompt.compositional_intent`` separately, where ``assemble_dual_prompt`` surfaces it
    as ``[PART 3: COMPOSITIONAL INTENT]``.
    """

    panel_id: str
    framing: Literal["close-up", "medium", "wide", "establishing"]
    top: list[LayoutNode] = field(default_factory=list)
    mid: list[LayoutNode] = field(default_factory=list)
    bot: list[LayoutNode] = field(default_factory=list)
    edges: list[SpatialEdge] = field(default_factory=list)
    compositional_intent: str | None = None


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

_GRAPH_HEADER_RE = re.compile(r"^\s*graph\s+(TB|BT|LR|RL|TD)\s*$")
_PANEL_RE = re.compile(r'^\s*panel\["([^"]+)"\]\s*$')
_SUBGRAPH_START_RE = re.compile(r"^\s*subgraph\s+(\w+)(?:\[[^\]]*\])?\s*$")
_SUBGRAPH_END_RE = re.compile(r"^\s*end\s*$")
_NODE_RE = re.compile(r'^\s*(\w+)\["([^"]+)"\]\s*$')
_EDGE_RE = re.compile(r"^\s*(\w+)\s*--\s*([\w-]+)\s*-->\s*(\w+)\s*$")
_BLANK_OR_COMMENT_RE = re.compile(r"^\s*(%%.*)?$")


def parse_panel_layout(mermaid_str: str) -> PanelLayout:
    """Parse a ``comic_panel_layout`` Mermaid string into a :class:`PanelLayout`.

    Expected shape (whitespace-flexible, blank lines and ``%%`` comments allowed)::

        graph TB
            panel["panel:<id><br/>framing=<value>"]
            subgraph TOP[TOP balloon space]
                <node_id>["<name><br/>key=val<br/>...]
            end
            subgraph MID[MID subject zone]
                ...
            end
            subgraph BOT[BOT ground zone]
                ...
            end
            <a> -- <relation> --> <b>

    Edges may cross subgraph boundaries. Node IDs are scoped to the whole panel (unique across all three regions).

    Raises ``ValueError`` if the Mermaid is missing the ``graph`` header, missing the panel node, missing any of the
    three subgraphs, has a duplicate node ID, references an unknown node ID in an edge, or contains an invalid
    framing / depth / relation enum value.
    """
    if not mermaid_str or not mermaid_str.strip():
        raise ValueError("parse_panel_layout: empty mermaid string")

    lines = mermaid_str.splitlines()
    panel_id: str | None = None
    framing: str | None = None
    regions_seen: set[str] = set()
    nodes_by_region: dict[str, list[LayoutNode]] = {"TOP": [], "MID": [], "BOT": []}
    id_to_name: dict[str, str] = {}
    edges_raw: list[tuple[str, str, str]] = []  # (src_id, relation, tgt_id)
    current_region: str | None = None
    saw_header = False

    for raw in lines:
        if _BLANK_OR_COMMENT_RE.match(raw):
            continue
        line = raw

        if not saw_header:
            if _GRAPH_HEADER_RE.match(line):
                saw_header = True
                continue
            raise ValueError(f"parse_panel_layout: expected `graph TB` header, got: {line!r}")

        if current_region is None:
            m_panel = _PANEL_RE.match(line)
            if m_panel:
                panel_id, framing = _parse_panel_label(m_panel.group(1))
                continue

            m_sub = _SUBGRAPH_START_RE.match(line)
            if m_sub:
                region = m_sub.group(1)
                if region not in VALID_REGIONS:
                    raise ValueError(
                        f"parse_panel_layout: unknown subgraph region {region!r} "
                        f"(expected one of {VALID_REGIONS})"
                    )
                if region in regions_seen:
                    raise ValueError(f"parse_panel_layout: duplicate subgraph region {region!r}")
                regions_seen.add(region)
                current_region = region
                continue

            m_edge = _EDGE_RE.match(line)
            if m_edge:
                edges_raw.append((m_edge.group(1), m_edge.group(2), m_edge.group(3)))
                continue

            raise ValueError(f"parse_panel_layout: unrecognized line outside subgraph: {line!r}")

        # Inside a subgraph
        if _SUBGRAPH_END_RE.match(line):
            current_region = None
            continue

        m_node = _NODE_RE.match(line)
        if m_node:
            node_id, label = m_node.group(1), m_node.group(2)
            if node_id in id_to_name:
                raise ValueError(f"parse_panel_layout: duplicate node id {node_id!r}")
            name, depth, attrs = _parse_node_label(label)
            id_to_name[node_id] = name
            nodes_by_region[current_region].append(LayoutNode(name=name, depth=depth, attrs=attrs))
            continue

        raise ValueError(f"parse_panel_layout: unrecognized line inside {current_region}: {line!r}")

    if not saw_header:
        raise ValueError("parse_panel_layout: missing `graph TB` header")
    if panel_id is None or framing is None:
        raise ValueError("parse_panel_layout: missing `panel[...]` node")
    if regions_seen != set(VALID_REGIONS):
        missing = set(VALID_REGIONS) - regions_seen
        raise ValueError(f"parse_panel_layout: missing subgraph(s): {sorted(missing)}")

    edges: list[SpatialEdge] = []
    for src_id, relation, tgt_id in edges_raw:
        if relation not in VALID_RELATIONS:
            raise ValueError(
                f"parse_panel_layout: unknown relation {relation!r} "
                f"(expected one of {VALID_RELATIONS})"
            )
        if src_id not in id_to_name:
            raise ValueError(f"parse_panel_layout: edge references unknown source id {src_id!r}")
        if tgt_id not in id_to_name:
            raise ValueError(f"parse_panel_layout: edge references unknown target id {tgt_id!r}")
        edges.append(
            SpatialEdge(source=id_to_name[src_id], target=id_to_name[tgt_id], relation=relation)
        )

    return PanelLayout(
        panel_id=panel_id,
        framing=framing,  # type: ignore[arg-type]
        top=nodes_by_region["TOP"],
        mid=nodes_by_region["MID"],
        bot=nodes_by_region["BOT"],
        edges=edges,
    )


def _parse_panel_label(label: str) -> tuple[str, str]:
    """Extract panel_id + framing from ``panel:<id><br/>framing=<value>``."""
    parts = [p.strip() for p in label.split("<br/>")]
    if not parts or not parts[0].startswith("panel:"):
        raise ValueError(
            f"parse_panel_layout: panel label must start with `panel:<id>`, got: {label!r}"
        )
    panel_id = parts[0][len("panel:"):]
    framing: str | None = None
    for part in parts[1:]:
        if "=" not in part:
            continue
        key, _, val = part.partition("=")
        if key.strip() == "framing":
            framing = val.strip()
    if framing is None:
        raise ValueError(f"parse_panel_layout: panel label missing framing=<value>: {label!r}")
    if framing not in VALID_FRAMINGS:
        raise ValueError(
            f"parse_panel_layout: invalid framing {framing!r} (expected one of {VALID_FRAMINGS})"
        )
    return panel_id, framing


def _parse_node_label(label: str) -> tuple[str, str | None, dict[str, str]]:
    """Extract name + depth + attrs from ``<name><br/>key=val<br/>...``."""
    parts = [p.strip() for p in label.split("<br/>")]
    if not parts or not parts[0]:
        raise ValueError(f"parse_panel_layout: empty node label: {label!r}")
    name = parts[0]
    depth: str | None = None
    attrs: dict[str, str] = {}
    for part in parts[1:]:
        if "=" not in part:
            continue
        key, _, val = part.partition("=")
        key, val = key.strip(), val.strip()
        if key == "depth":
            if val not in VALID_DEPTHS:
                raise ValueError(
                    f"parse_panel_layout: invalid depth {val!r} (expected one of {VALID_DEPTHS})"
                )
            depth = val
        else:
            attrs[key] = val
    return name, depth, attrs


# ---------------------------------------------------------------------------
# Serializer
# ---------------------------------------------------------------------------

def serialize_panel_layout(layout: PanelLayout) -> str:
    """Re-emit canonical Mermaid for a :class:`PanelLayout`.

    Property: ``serialize(parse(serialize(parse(s)))) == serialize(parse(s))`` (idempotent normalization). Region
    labels canonical per :data:`REGION_DESCRIPTIONS`; node IDs deterministic ``top_<i>`` / ``mid_<i>`` / ``bot_<i>``.
    """
    if layout.framing not in VALID_FRAMINGS:
        raise ValueError(f"serialize_panel_layout: invalid framing {layout.framing!r}")

    lines: list[str] = ["graph TB"]
    lines.append(f'    panel["panel:{layout.panel_id}<br/>framing={layout.framing}"]')

    name_to_id: dict[str, str] = {}
    for region_name, nodes, prefix in (
        ("TOP", layout.top, "top"),
        ("MID", layout.mid, "mid"),
        ("BOT", layout.bot, "bot"),
    ):
        lines.append("")
        lines.append(f"    subgraph {region_name}[{REGION_DESCRIPTIONS[region_name]}]")
        for i, node in enumerate(nodes):
            canonical_id = f"{prefix}_{i}"
            if node.name in name_to_id:
                raise ValueError(
                    f"serialize_panel_layout: duplicate display name {node.name!r} "
                    "(must be unique across all regions)"
                )
            name_to_id[node.name] = canonical_id
            label = _format_node_label(node)
            lines.append(f'        {canonical_id}["{label}"]')
        lines.append("    end")

    if layout.edges:
        lines.append("")
        for edge in layout.edges:
            if edge.relation not in VALID_RELATIONS:
                raise ValueError(f"serialize_panel_layout: invalid relation {edge.relation!r}")
            src = name_to_id.get(edge.source)
            tgt = name_to_id.get(edge.target)
            if src is None:
                raise ValueError(
                    f"serialize_panel_layout: edge source {edge.source!r} not declared in any region"
                )
            if tgt is None:
                raise ValueError(
                    f"serialize_panel_layout: edge target {edge.target!r} not declared in any region"
                )
            lines.append(f"    {src} -- {edge.relation} --> {tgt}")

    return "\n".join(lines) + "\n"


def _format_node_label(node: LayoutNode) -> str:
    """Format a :class:`LayoutNode` as ``name<br/>depth=<v><br/>k=v...`` (deterministic attr ordering)."""
    if node.depth is not None and node.depth not in VALID_DEPTHS:
        raise ValueError(
            f"serialize_panel_layout: invalid depth {node.depth!r} for node {node.name!r}"
        )
    parts: list[str] = [node.name]
    if node.depth is not None:
        parts.append(f"depth={node.depth}")
    for k in sorted(node.attrs):  # deterministic attr ordering
        parts.append(f"{k}={node.attrs[k]}")
    return "<br/>".join(parts)


# ---------------------------------------------------------------------------
# Dual-prompt assembly (spec § 3 verbatim — Imagen-4 instruction wrapper)
# ---------------------------------------------------------------------------

IMAGEN_DUAL_PROMPT_WRAPPER: str = (
    "The following description has TWO parts that describe THE SAME image.\n"
    "\n"
    "[PART 1: TEXT DESCRIPTION]\n"
    "A natural-language description of the scene's content, characters, "
    "style, and mood. This is the primary description of what to render.\n"
    "\n"
    "[PART 2: SPATIAL LAYOUT]\n"
    "A structured spatial description in Mermaid graph syntax that "
    "specifies WHERE elements appear in the frame:\n"
    "- Which third of the frame (TOP / MID / BOT)\n"
    "- Which depth layer (foreground / midground / background)\n"
    "- Spatial relationships between elements (left-of, above, contains, "
    "speaks, etc.)\n"
    "- The framing attribute (close-up | medium | wide | establishing) "
    "sets the camera distance\n"
    "\n"
    "Treat both parts as mutual descriptions of the SAME target image. "
    "Use PART 2 to disambiguate spatial intent in PART 1:\n"
    "- Place elements in the frame thirds (TOP / MID / BOT) as PART 2 "
    "specifies\n"
    "- Honor depth-layer assignments — foreground subjects render larger "
    "and sharper than background\n"
    '- Honor spatial relationships ("left-of", "above") in the rendered '
    "composition\n"
    "- Set camera distance to match the framing attribute\n"
    "\n"
    "DO NOT render the Mermaid syntax itself, the bracket markers, the "
    "section headers, or any structural text in the output image. The "
    "Mermaid is a composition guide, not visible content."
)

IMAGEN_DUAL_PROMPT_WRAPPER_WITH_COMPOSITIONAL_INTENT: str = (
    "The following description has THREE parts that describe THE SAME image.\n"
    "\n"
    "[PART 1: TEXT DESCRIPTION]\n"
    "A natural-language description of the scene's content, characters, "
    "style, and mood. This is the primary description of what to render.\n"
    "\n"
    "[PART 2: SPATIAL LAYOUT]\n"
    "A structured spatial description in Mermaid graph syntax that "
    "specifies WHERE elements appear in the frame:\n"
    "- Which third of the frame (TOP / MID / BOT)\n"
    "- Which depth layer (foreground / midground / background)\n"
    "- Spatial relationships between elements (left-of, above, contains, "
    "speaks, etc.)\n"
    "- The framing attribute (close-up | medium | wide | establishing) "
    "sets the camera distance\n"
    "\n"
    "[PART 3: COMPOSITIONAL INTENT]\n"
    "A short free-text compositional anchor describing the overall "
    "compositional feel the image should achieve (e.g. composition "
    "naturalness, physical contact clarity, crowd depth refinement, "
    "object interaction focus, fading visual effect). PART 3 is a guiding "
    "compositional intent — not a literal element to render — and "
    "operates as a tie-breaker when PART 1 and PART 2 leave compositional "
    "choices ambiguous.\n"
    "\n"
    "Treat all three parts as mutual descriptions of the SAME target "
    "image. Use PART 2 to disambiguate spatial intent in PART 1; use "
    "PART 3 to disambiguate compositional intent across PART 1 + PART 2:\n"
    "- Place elements in the frame thirds (TOP / MID / BOT) as PART 2 "
    "specifies\n"
    "- Honor depth-layer assignments — foreground subjects render larger "
    "and sharper than background\n"
    '- Honor spatial relationships ("left-of", "above") in the rendered '
    "composition\n"
    "- Set camera distance to match the framing attribute\n"
    "- Honor the PART 3 compositional intent as an anchor — when PART 1 "
    "and PART 2 admit multiple compositional readings, prefer the reading "
    "that matches PART 3\n"
    "\n"
    "DO NOT render the Mermaid syntax itself, the bracket markers, the "
    "section headers, the PART 3 anchor text, or any structural text in "
    "the output image. The Mermaid is a composition guide, not visible "
    "content; PART 3 is an instruction, not visible content."
)


def assemble_dual_prompt(image_prompt: ImagePrompt) -> str:
    """Concatenate wrapper + text + mermaid + intent into one Imagen-4 input string.

    When ``image_prompt.mermaid_layout`` is falsy, degrades to the single-prompt path (wrapper + PART 1). When
    ``image_prompt.compositional_intent`` is set, switches to the V2 wrapper and appends ``[PART 3]``; otherwise the
    V1 wrapper is emitted verbatim and no PART 3 appears.
    """
    wrapper = (
        IMAGEN_DUAL_PROMPT_WRAPPER_WITH_COMPOSITIONAL_INTENT
        if image_prompt.compositional_intent
        else IMAGEN_DUAL_PROMPT_WRAPPER
    )
    parts: list[str] = [wrapper, "[PART 1: TEXT DESCRIPTION]", image_prompt.text]
    if image_prompt.mermaid_layout:
        parts += ["[PART 2: SPATIAL LAYOUT]", image_prompt.mermaid_layout]
    if image_prompt.compositional_intent:
        parts += ["[PART 3: COMPOSITIONAL INTENT]", image_prompt.compositional_intent]
    return "\n\n".join(parts)


__all__ = [
    "PanelLayout",
    "LayoutNode",
    "SpatialEdge",
    "VALID_REGIONS",
    "VALID_FRAMINGS",
    "VALID_DEPTHS",
    "VALID_RELATIONS",
    "REGION_DESCRIPTIONS",
    "IMAGEN_DUAL_PROMPT_WRAPPER",
    "IMAGEN_DUAL_PROMPT_WRAPPER_WITH_COMPOSITIONAL_INTENT",
    "parse_panel_layout",
    "serialize_panel_layout",
    "assemble_dual_prompt",
]
