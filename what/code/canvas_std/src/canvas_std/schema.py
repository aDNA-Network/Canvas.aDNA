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
#
# ⛩ F-DT-7 (Operation Datum P3, 2026-09-15) — WHY EVERY CONSTANT BELOW CARRIES A `SCHEMA-TWIN` CLAIM.
#
# Each of these has a counterpart enum in `data/adna_canvas_v2.schema.json`, and until P3 **nothing
# compared them**. The census (`how/gates/registry_census.py`) appeared to: it pairs BY CONTENT and
# reported "12 SCHEMA-TWIN, all agreeing exactly". But content-pairing dissolves precisely when
# content diverges — drift below its Jaccard 0.5 floor does not report DRIFT?, it **unpairs**, and the
# constant reclassifies to VALIDATOR-ONLY, an accepted state. Measured: gutting the schema's
# `fromSide`/`toSide` enums from four values to one left the census at **exit 0** and **all ten gates
# green**, while `jsonschema` correctly rejected an ordinary canvas with *"'bottom' is not one of
# ['top']"*. The schema half is genuinely load-bearing and its consumers are OUTSIDE this vault — a
# fork, a `pip install adna-canvas-std`, any external validator. Inside the package, every reader of
# `json_schema()` reads `$defs.reserved` only.
#
# ⇒ a registry that LOOKS watched is better hidden than one that visibly is not.
#
# The docstrings below are therefore not labels. Each is a falsifiable claim checked against a
# derivation by `tests/test_registry_consistency.py` (package scope) and `registry_census.py` (vault
# scope, which additionally checks spec §7.2). A constant declaring SCHEMA-TWIN whose twin has
# vanished now FAILS. No name map is involved: the claim is per-object and the twin is still found by
# content — the declaration supplies the memory that content-pairing cannot have.
#
# ⚠ This file's header says "No values are invented here" — still true. Nothing below changes a
# VALUE; the docstrings state what each vocabulary's relationship to the schema IS.

VALID_NODE_TYPES: frozenset[str] = frozenset({"text", "file", "group", "link"})
"""SCHEMA-TWIN — `$defs.node.properties.type.enum`.

⛩ F-DT-3: identical in content to `reserved.BASELINE_TYPES`, and the operator ruled 2026-09-15 **two
vocabularies that coincide — link, do not merge.** This one answers *what node types exist in the
baseline document*; `BASELINE_TYPES` answers *what a component may degrade to* (§11). Both stand;
`test_baseline_types_and_node_types_agree` fails if they ever diverge."""

VALID_SHAPES: frozenset[str | None] = frozenset(
    {None, "pill", "diamond", "parallelogram", "circle", "predefined-process", "document", "database"}
)
"""SCHEMA-TWIN — `$defs.node.properties.styleAttributes.properties.shape.enum`."""

VALID_BORDERS: frozenset[str | None] = frozenset({None, "dashed", "dotted", "invisible"})
"""SCHEMA-TWIN — `$defs.node.properties.styleAttributes.properties.border.enum`."""

VALID_TEXT_ALIGN: frozenset[str | None] = frozenset({None, "center", "right"})  # left = implicit default
"""SCHEMA-TWIN — `$defs.node.properties.styleAttributes.properties.textAlign.enum`. `None` carries
`left`, the implicit default — absence is a value here, which is why the set is `str | None`."""

VALID_COLORS: frozenset[str] = frozenset({"0", "1", "2", "3", "4", "5", "6"})  # validate() also accepts #-hex
"""VALIDATOR-ONLY — no schema enum, and a twin would be WRONG: `validate()` also accepts `#`-hex, so
an enum of the seven preset slots would reject colors the Standard permits. The schema constrains
`color` by type/pattern instead. ⛔ Do not give this one a twin to make the census symmetric."""

VALID_PATH_STYLES: frozenset[str | None] = frozenset({None, "dotted", "short-dashed", "long-dashed"})
"""SCHEMA-TWIN — `$defs.edge.properties.styleAttributes.properties.path.enum`."""

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
"""SCHEMA-TWIN — `$defs.edge.properties.styleAttributes.properties.arrow.enum`."""

VALID_PATHFINDING: frozenset[str | None] = frozenset({None, "square", "a-star"})
"""SCHEMA-TWIN — `$defs.edge.properties.styleAttributes.properties.pathfindingMethod.enum`."""

VALID_SIDES: frozenset[str] = frozenset({"top", "bottom", "left", "right"})
"""SCHEMA-TWIN — `$defs.edge.properties.fromSide.enum` AND `.toSide.enum` (one vocabulary, two
fields). ⛩ This is the constant F-DT-7 was measured on: gutting the schema side left every gate
green, so this claim is the check that now stands between the published schema and silent drift."""

VALID_ENDS: frozenset[str] = frozenset({"none", "arrow"})
"""SCHEMA-TWIN — `$defs.edge.properties.toEnd.enum` AND `.fromEnd.enum`. ⚠ Its `none` collides with
`PL_FLOW`/`PL_PAGINATION`; the census files that as coincidence, not drift (F-DT-2)."""

# --- Required field sets (spec §4.1 / §5.1) ----------------------------------------------------
NODE_REQUIRED_FIELDS: tuple[str, ...] = ("id", "type", "x", "y", "width", "height")
"""VALIDATOR-ONLY — no schema ENUM, and correctly so: the schema expresses this as `node.required`,
a JSON Schema keyword, not an enum. A twin would be a category error — these are field NAMES, not a
value domain."""

EDGE_REQUIRED_FIELDS: tuple[str, ...] = ("id", "fromNode", "fromSide", "toNode", "toSide")
"""VALIDATOR-ONLY — same as `NODE_REQUIRED_FIELDS`: expressed as `edge.required` in the schema, not
as an enum. ⚠ Note `toEnd` is NOT here — C-4 requires it explicitly at aDNA-Native level, which is a
conformance rule, not a baseline structural requirement."""

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
