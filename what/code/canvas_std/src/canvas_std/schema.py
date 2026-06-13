"""The KEEP floor — value enums, node/edge schema, semantic profiles.

E0.1: declared, empty. **E0.2 ports the VERBATIM values** from `p1_fork_baseline.md` §3
(the 10 ``VALID_*`` enums, the node/edge required-field schema, and the ``lattice`` semantic
profile from ``TYPE_MAPPING`` / ``EDGE_TYPE_MAPPING``). Do not invent values here — they are
transcribed from the ratified baseline so a valid aDNA canvas degrades to a valid Obsidian canvas.

Spec: spec_adna_canvas_standard §4–§6.
"""

from __future__ import annotations

# --- E0.2 fills these (verbatim KEEP floor). Empty placeholders keep imports valid. ---
VALID_NODE_TYPES: frozenset[str] = frozenset()
VALID_SHAPES: frozenset[str | None] = frozenset()
VALID_BORDERS: frozenset[str | None] = frozenset()
VALID_TEXT_ALIGN: frozenset[str | None] = frozenset()
VALID_COLORS: frozenset[str] = frozenset()
VALID_PATH_STYLES: frozenset[str | None] = frozenset()
VALID_ARROWS: frozenset[str | None] = frozenset()
VALID_PATHFINDING: frozenset[str | None] = frozenset()
VALID_SIDES: frozenset[str] = frozenset()
VALID_ENDS: frozenset[str] = frozenset()

# Built-in semantic profile "lattice" (KEEP, unmodified; E0.2 transcribes the 8 node + 5 edge entries).
TYPE_MAPPING: dict[str, dict[str, object]] = {}
EDGE_TYPE_MAPPING: dict[str, dict[str, object]] = {}

# Required field sets (E0.2 fills from spec §4.1 / §5.1).
NODE_REQUIRED_FIELDS: tuple[str, ...] = ()
EDGE_REQUIRED_FIELDS: tuple[str, ...] = ()


def is_floor_loaded() -> bool:
    """True once E0.2 has populated the KEEP floor. Lets the smoke test assert E0.1-vs-E0.2 state."""
    return bool(VALID_NODE_TYPES)
