"""The KEEP floor — value enums, node/edge schema, semantic profiles.

VERBATIM transcription of the ratified baseline (``p1_fork_baseline.md`` §3, itself a verbatim
extraction of ``CanvasForge.canvas_core.core.py``). **No values are invented here** — fidelity to the
baseline is what guarantees a valid aDNA canvas degrades to a valid Obsidian canvas
(spec_adna_canvas_standard §11). The two semantic maps are KEEP-as-floor (the built-in ``lattice``
profile) and are EXTENDed additively by new profiles — never by editing these.

Spec: spec_adna_canvas_standard §4–§6 · upstream baseline: Advanced Canvas v5.6.6 / JSON Canvas 1.0.
Ported: Operation Keystone E0.2 (2026-06-13).
"""

from __future__ import annotations

from typing import Any

# --- Value enums (10 VALID_* families, verbatim) -----------------------------------------------
VALID_NODE_TYPES: frozenset[str] = frozenset({"text", "file", "group", "link"})

VALID_SHAPES: frozenset[str | None] = frozenset(
    {None, "pill", "diamond", "parallelogram", "circle", "predefined-process", "document", "database"}
)

VALID_BORDERS: frozenset[str | None] = frozenset({None, "dashed", "dotted", "invisible"})

VALID_TEXT_ALIGN: frozenset[str | None] = frozenset({None, "center", "right"})  # left = implicit default

VALID_COLORS: frozenset[str] = frozenset({"0", "1", "2", "3", "4", "5", "6"})  # validate() also accepts #-hex

VALID_PATH_STYLES: frozenset[str | None] = frozenset({None, "dotted", "short-dashed", "long-dashed"})

VALID_ARROWS: frozenset[str | None] = frozenset(
    {
        None,
        "triangle-outline",
        "thin-triangle",
        "halved-triangle",
        "diamond",
        "diamond-outline",
        "circle",
        "circle-outline",
    }
)

VALID_PATHFINDING: frozenset[str | None] = frozenset({None, "square", "a-star"})

VALID_SIDES: frozenset[str] = frozenset({"top", "bottom", "left", "right"})

VALID_ENDS: frozenset[str] = frozenset({"none", "arrow"})

# --- Required field sets (spec §4.1 / §5.1) ----------------------------------------------------
NODE_REQUIRED_FIELDS: tuple[str, ...] = ("id", "type", "x", "y", "width", "height")
EDGE_REQUIRED_FIELDS: tuple[str, ...] = ("id", "fromNode", "fromSide", "toNode", "toSide")

# --- Semantic color/edge conventions (SHOULD; spec §6) -----------------------------------------
# Reserved color slots: "1" red=warn/error, "2" orange=note, "3" yellow=highlight; "4""5""6" node-type.

# --- Built-in semantic profile "lattice" (KEEP, unmodified) ------------------------------------
# Node profile — value keys mirror legacy core.py: {color, shape, node_type}.
TYPE_MAPPING: dict[str, dict[str, Any]] = {
    "module": {"color": "4", "shape": "predefined-process", "node_type": "file"},
    "dataset": {"color": "5", "shape": "database", "node_type": "file"},
    "reasoning": {"color": "6", "shape": "diamond", "node_type": "text"},
    "process": {"color": None, "shape": None, "node_type": "text"},
    "input": {"color": "4", "shape": "parallelogram", "node_type": "text"},
    "output": {"color": "5", "shape": "parallelogram", "node_type": "text"},
    "start": {"color": None, "shape": "pill", "node_type": "text"},
    "end": {"color": None, "shape": "pill", "node_type": "text"},
}

# Edge profile — value keys: {path_style, arrow, from_end, to_end}.
EDGE_TYPE_MAPPING: dict[str, dict[str, Any]] = {
    "data": {"path_style": None, "arrow": None, "from_end": None, "to_end": "arrow"},
    "control": {"path_style": "long-dashed", "arrow": None, "from_end": None, "to_end": "arrow"},
    "optional": {"path_style": "dotted", "arrow": "triangle-outline", "from_end": None, "to_end": "arrow"},
    "bidirectional": {"path_style": None, "arrow": None, "from_end": "arrow", "to_end": "arrow"},
    "weak": {"path_style": "short-dashed", "arrow": "circle-outline", "from_end": None, "to_end": "arrow"},
}

# Registry of built-in profiles (new profiles register additively — spec_component_model §4.3).
SEMANTIC_PROFILES: dict[str, dict[str, dict[str, Any]]] = {"lattice": TYPE_MAPPING}
EDGE_PROFILES: dict[str, dict[str, dict[str, Any]]] = {"lattice": EDGE_TYPE_MAPPING}


def is_floor_loaded() -> bool:
    """True once the KEEP floor is populated (E0.2 done)."""
    return bool(VALID_NODE_TYPES)
