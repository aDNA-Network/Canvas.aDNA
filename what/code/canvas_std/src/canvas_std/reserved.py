"""Validators for the additive ``_reserved`` block (the aDNA-Native A-* checks).

E1.4 implements ``validate_reserved`` + the ``component_types`` and ``panel_link`` sub-validators
(spec_conformance_suite §4; spec_component_model §7; spec_panel_link_semantics §6; spec_context_object §4).

Operation Armature P2 adds ``validate_interaction`` — the ``I-1``/``I-2``/``I-3`` family for the leg-3 interaction
overlay (spec_interface_surface §9.1), wired into the aDNA-Native ``validate`` path per ``adr_007`` (the first
leg-3 touch of the harness; it reuses the same node/anchor substrate the A-* checks already build).

Spec: spec_adna_canvas_standard §7.
"""

from __future__ import annotations

import re
from typing import Any

from canvas_std import schema

# The reserved-key namespace (spec_adna_canvas_standard §7.2).
RESERVED_KEYS: tuple[str, ...] = (
    "adna_version",
    "conformance_level",
    "sync",
    "component_types",
    "semantic_bindings",
    "brand_style_pack_ref",
    "panel_link",
    "context_object",
)

# Component taxonomy (spec_component_model §2) and the baseline degradation types.
COMPONENT_CLASSES: frozenset[str] = frozenset(
    {"text", "typography_run", "image", "video", "shape", "embed", "group", "panel",
     "link", "edge", "table", "code", "caption", "region"}
)
BASELINE_TYPES: frozenset[str] = frozenset({"text", "file", "group", "link"})

# Panel/link vocabularies (spec_panel_link_semantics §3–§4).
PL_EDGE_KINDS: frozenset[str] = frozenset({"sequence", "reading_order", "adjacency", "dependency"})
PL_FLOW: frozenset[str] = frozenset({"none", "vertical", "horizontal", "columns"})
PL_PAGINATION: frozenset[str] = frozenset({"none", "paged", "continuous"})
# `extent` is a pagination/length window; these are the only length units. `extent` is OPTIONAL (AT-1,
# spec §4) — a non-paginated single-surface region (e.g. a diagram, pagination: none) omits it. There is
# deliberately no graph/node unit: a node-graph is sized by content, not paged.
PL_EXTENT_UNITS: frozenset[str] = frozenset({"words", "pages", "slides"})

# Anchor layer vocabularies (spec_panel_link_semantics §5.3/§6).
NC_LABEL_FORMS: frozenset[str] = frozenset({"descriptive", "legacy"})       # naming_convention.label_form (F7/X8)
OD_MODES: frozenset[str] = frozenset({"label_ref", "src_cited"})            # orphan_detector.mode (X2)
# Component `qualities` keys that declare an explicit cross-reference to an anchor (each value MUST resolve).
ANCHOR_REF_KEYS: tuple[str, ...] = ("ref", "anchor", "anchor_ref", "cites", "for")

# Canonical long-form text semantic_types (spec_component_model §4.4 — B2 ride-on-text; carried on class: text,
# not dedicated taxonomy classes). Informational registry — no validator rejects other semantic_type values.
LONGFORM_SEMANTIC_TYPES: frozenset[str] = frozenset({"quote", "block_quote", "footnote", "attribution"})

_SEMVER = re.compile(r"^\d+\.\d+\.\d+")
_HEX16 = re.compile(r"^[0-9a-f]{16}$")

# Leg-3 interaction layer (spec_interface_surface §3.3/§9.1; wired into the harness at Armature P2 per adr_007).
# The four affordance kinds partition what a participant can do at a point — a *closed* enum (IX3).
AFFORDANCE_KINDS: tuple[str, ...] = ("input", "choice", "annotation", "action")
# interaction_version is semver-shaped; "1.0" (2-part) and "1.0.0" (3-part) both accepted (spec §3.1). Deliberately
# distinct from _SEMVER (3-part, for adna_version / context_object.version) — the interaction layer is 2-part-tolerant.
_INTERACTION_SEMVER = re.compile(r"^\d+\.\d+(\.\d+)?$")


def validate_reserved(reserved: dict[str, Any], doc: dict[str, Any]) -> list[str]:
    """Validate a ``_reserved`` block (A-* checks). ``doc`` supplies node/edge ids for resolution."""
    errors: list[str] = []
    if not isinstance(reserved, dict):
        return ["A-2: _reserved is not an object"]
    node_ids = {n["id"] for n in doc.get("nodes", []) if isinstance(n, dict) and "id" in n}
    edge_ids = {e["id"] for e in doc.get("edges", []) if isinstance(e, dict) and "id" in e}

    # A-2
    av = reserved.get("adna_version")
    if not (isinstance(av, str) and _SEMVER.match(av)):
        errors.append(f"A-2: adna_version {av!r} missing or not semver")
    cl = reserved.get("conformance_level")
    if cl != "adna_native":
        errors.append(f"A-2: conformance_level {cl!r} must be 'adna_native' for an aDNA-Native canvas")

    # A-6 (structural — hash↔source match is checked by the round-trip layer)
    sync = reserved.get("sync")
    if not isinstance(sync, dict):
        errors.append("A-6: _reserved.sync missing")
    else:
        sh = sync.get("sync_hash")
        if not (isinstance(sh, str) and _HEX16.match(sh)):
            errors.append(f"A-6: sync.sync_hash {sh!r} is not 16 hex chars")

    # A-3 / A-5 / A-7
    if "component_types" in reserved:
        errors += validate_component_types(reserved["component_types"], node_ids)
    if "semantic_bindings" in reserved:
        errors += _validate_semantic_bindings(reserved["semantic_bindings"])
    if "panel_link" in reserved:
        errors += validate_panel_link(reserved["panel_link"], node_ids, doc.get("edges", []), edge_ids)
    if "context_object" in reserved:
        errors += _validate_context_object(reserved["context_object"])

    # A-5 anchor layer (spec_panel_link_semantics §5.3/§6) — naming/orphan declaration + reference resolution.
    # Spans semantic_bindings + panel_link + component_types, so it takes the whole reserved block.
    errors += validate_anchors(reserved, node_ids)
    return errors


def validate_component_types(block: dict[str, Any], node_ids: set[str]) -> list[str]:
    """spec_component_model §7 — each key resolves to a node/edge id; class ∈ taxonomy; degrades_to ∈ baseline."""
    errors: list[str] = []
    if not isinstance(block, dict):
        return ["A-3: component_types is not an object"]
    for nid, entry in block.items():
        if nid not in node_ids:
            errors.append(f"A-3: component_types key {nid!r} does not resolve to a node")
        if not isinstance(entry, dict):
            errors.append(f"A-3: component_types[{nid!r}] is not an object")
            continue
        if entry.get("class") not in COMPONENT_CLASSES:
            errors.append(f"A-3: component {nid!r} class {entry.get('class')!r} not in taxonomy")
        dt = entry.get("degrades_to")
        if dt is not None and dt not in BASELINE_TYPES:
            errors.append(f"A-3: component {nid!r} degrades_to {dt!r} not in {sorted(BASELINE_TYPES)}")
    return errors


def _validate_semantic_bindings(block: Any) -> list[str]:
    """spec_component_model §4 — inline bindings use only §6 tokens; the built-in 'lattice' profile is unmodified."""
    errors: list[str] = []
    if not isinstance(block, dict):
        return ["A-4: semantic_bindings is not an object"]
    if block.get("profile") == "lattice" and "bindings" not in block:
        return errors  # naming the built-in profile is fine
    for name, binding in block.get("bindings", {}).items():
        if not isinstance(binding, dict):
            continue
        if "shape" in binding and binding["shape"] not in schema.VALID_SHAPES:
            errors.append(f"A-4: semantic_bindings[{name!r}] shape {binding['shape']!r} not in enum")
        if "color" in binding and binding["color"] is not None and binding["color"] not in schema.VALID_COLORS:
            errors.append(f"A-4: semantic_bindings[{name!r}] color {binding['color']!r} not in enum")
    return errors


def validate_panel_link(block: dict[str, Any], node_ids: set[str], edges: list[Any], edge_ids: set[str]) -> list[str]:
    """spec_panel_link_semantics §6 — kinds/ids resolve, sequence acyclic, exactly one canonical surface."""
    errors: list[str] = []
    if not isinstance(block, dict):
        return ["A-5: panel_link is not an object"]

    edge_endpoints = {e["id"]: (e.get("fromNode"), e.get("toNode")) for e in edges if isinstance(e, dict) and "id" in e}
    seq_graph: dict[str, list[str]] = {}
    for eid, meta in block.get("edges", {}).items():
        if eid not in edge_ids:
            errors.append(f"A-5: panel_link.edges key {eid!r} does not resolve to an edge")
        kind = meta.get("kind") if isinstance(meta, dict) else None
        if kind not in PL_EDGE_KINDS:
            errors.append(f"A-5: panel_link edge {eid!r} kind {kind!r} not in {sorted(PL_EDGE_KINDS)}")
        if kind == "sequence" and eid in edge_endpoints:
            frm, to = edge_endpoints[eid]
            seq_graph.setdefault(frm, []).append(to)
    if _has_cycle(seq_graph):
        errors.append("A-5: panel_link 'sequence' chain has a cycle")

    for gid, region in block.get("regions", {}).items():
        if gid not in node_ids:
            errors.append(f"A-5: panel_link.regions key {gid!r} does not resolve to a node/group")
        if not isinstance(region, dict):
            continue
        if "flow" in region and region["flow"] not in PL_FLOW:
            errors.append(f"A-5: region {gid!r} flow {region['flow']!r} invalid")
        if "pagination" in region and region["pagination"] not in PL_PAGINATION:
            errors.append(f"A-5: region {gid!r} pagination {region['pagination']!r} invalid")
        unit = (region.get("extent") or {}).get("unit")
        if unit is not None and unit not in PL_EXTENT_UNITS:
            errors.append(f"A-5: region {gid!r} extent.unit {unit!r} invalid")

    # Surfaces: enforce the `role` set (exactly one canonical) + id resolution. The `surface` subclass label is an
    # OPEN, producer-defined vocabulary (AT-2, spec §4/§5.2) — deliberately NOT enum-checked here.
    surfaces = block.get("surfaces")
    if surfaces is not None:
        canonical = [s for s in surfaces if isinstance(s, dict) and s.get("role") == "canonical"]
        if len(canonical) != 1:
            errors.append(f"A-5: panel_link must have exactly one canonical surface (found {len(canonical)})")
        for s in surfaces:
            if isinstance(s, dict) and s.get("id") not in node_ids:
                errors.append(f"A-5: surface id {s.get('id')!r} does not resolve to a node/group")
    return errors


def validate_anchors(reserved: dict[str, Any], node_ids: set[str]) -> list[str]:
    """spec_panel_link_semantics §5.3/§6 — the declarative anchor layer the Standard owns.

    Validates ``naming_convention`` / ``orphan_detector`` well-formedness (wherever declared — on the LF contract
    bindings ``semantic_bindings.format``/``visual``, or on ``panel_link``) and that every declared anchor and
    every *explicit* component anchor-reference resolves (no orphaned anchor). The orphan-*traversal* engine
    (prose label scanning per ``orphan_detector.mode``) is producer-side (C8) and is NOT run here.
    """
    errors: list[str] = []
    if not isinstance(reserved, dict):
        return errors

    pl = reserved.get("panel_link")
    pl = pl if isinstance(pl, dict) else {}

    # naming_convention / orphan_detector may ride on the LF contract bindings (F7/X8/X2) or on panel_link.
    decl_blocks: list[dict[str, Any]] = [pl]
    sb = reserved.get("semantic_bindings")
    if isinstance(sb, dict):
        decl_blocks += [sb[k] for k in ("format", "visual") if isinstance(sb.get(k), dict)]

    for blk in decl_blocks:
        nc = blk.get("naming_convention")
        if isinstance(nc, dict):
            lf = nc.get("label_form")
            if lf is not None and lf not in NC_LABEL_FORMS:
                errors.append(f"A-5: naming_convention.label_form {lf!r} not in {sorted(NC_LABEL_FORMS)}")
            mr = nc.get("migration_rule")
            if mr is not None and not isinstance(mr, str):
                errors.append(f"A-5: naming_convention.migration_rule must be a string (got {type(mr).__name__})")
        od = blk.get("orphan_detector")
        if isinstance(od, dict):
            mode = od.get("mode")
            if mode is not None and mode not in OD_MODES:
                errors.append(f"A-5: orphan_detector.mode {mode!r} not in {sorted(OD_MODES)}")
            th = od.get("threshold")
            if th is not None and not (isinstance(th, (int, float)) and not isinstance(th, bool) and 0 <= th <= 1):
                errors.append(f"A-5: orphan_detector.threshold {th!r} must be a number in [0, 1]")

    # Optional anchor registry: a label -> baseline node-id map; every entry resolves.
    anchors = pl.get("anchors")
    anchor_labels: set[str] = set()
    if isinstance(anchors, dict):
        anchor_labels = set(anchors)
        for label, target in anchors.items():
            if isinstance(target, str) and target not in node_ids:
                errors.append(f"A-5: panel_link.anchors[{label!r}] references missing node {target!r}")

    # Explicit component anchor-references must resolve to a node id or a declared anchor label (no orphan).
    comp = reserved.get("component_types")
    if isinstance(comp, dict):
        for nid, entry in comp.items():
            quals = entry.get("qualities") if isinstance(entry, dict) else None
            if not isinstance(quals, dict):
                continue
            for key in ANCHOR_REF_KEYS:
                target = quals.get(key)
                if isinstance(target, str) and target not in node_ids and target not in anchor_labels:
                    errors.append(f"A-5: component {nid!r} {key} references missing anchor {target!r}")
    return errors


def _interaction_value_kind_errors(aid: str, entry: dict[str, Any], value: Any) -> list[str]:
    """IX5 value↔kind consistency: ``choice`` ∈ options · ``action`` ⇒ null · ``input``/``annotation`` non-null."""
    errors: list[str] = []
    kind = entry.get("kind")
    if kind == "action":
        if value is not None:
            errors.append(f"I-3: action affordance {aid!r} response must carry no value (got {value!r})")
    elif kind == "choice":
        options = entry.get("options") or []
        if value not in options:
            errors.append(f"I-3: choice affordance {aid!r} value {value!r} not in declared options {list(options)}")
    elif kind in ("input", "annotation"):
        if value is None:
            errors.append(f"I-3: {kind} affordance {aid!r} response value must not be null")
    # an unknown kind is already flagged by I-2; no value check possible
    return errors


def validate_interaction(reserved: dict[str, Any], doc: dict[str, Any]) -> list[str]:
    """spec_interface_surface §9.1 — the ``I-1``/``I-2``/``I-3`` family for the leg-3 interaction overlay.

    Validates ``_reserved.interaction``: **I-1** (well-formed overlay — semver ``interaction_version``, object
    ``affordances``, list ``responses``, object ``state``), **I-2** (per affordance: its ``anchor`` resolves to a
    node id or a declared ``panel_link.anchors`` label; ``kind`` ∈ the closed enum; ``options`` present iff
    ``choice``), **I-3** (per response: it references a declared affordance with a kind-consistent value). A canvas
    with no ``_reserved.interaction`` is **vacuously conformant** (I-1 — a non-interactive surface, spec §8).
    Returns human-readable failures ([] == conformant).

    Wired into the aDNA-Native ``validate`` path at Armature P2 (``adr_007``). The I-2 anchor-orphan substrate
    (``validate_anchors``) is already run by ``validate_reserved`` on this same branch, so it is **not** re-run here:
    this does I-1/I-2/I-3 only. ``doc`` supplies node ids; anchor labels come from ``panel_link.anchors`` (the
    doc path only — ``canvas_std`` never imports a ``ContextGraph``; the dependency is one-way).
    """
    errors: list[str] = []
    if not isinstance(reserved, dict):
        return errors
    block = reserved.get("interaction")
    if not isinstance(block, dict) or not block:
        return errors  # non-interactive surface: vacuously conformant (I-1)

    # I-1 — well-formed overlay
    iv = block.get("interaction_version")
    if iv is not None and not (isinstance(iv, str) and _INTERACTION_SEMVER.match(iv)):
        errors.append(f"I-1: interaction_version {iv!r} is not semver")
    affs = block.get("affordances")
    if affs is None:
        affs = {}
    elif not isinstance(affs, dict):
        errors.append("I-1: affordances must be an object")
        affs = {}
    responses = block.get("responses")
    if responses is None:
        responses = []
    elif not isinstance(responses, list):
        errors.append("I-1: responses must be a list (append-only log)")
        responses = []
    if block.get("state") is not None and not isinstance(block.get("state"), dict):
        errors.append("I-1: state must be an object")

    # resolution sets — node ids (from the doc) + declared anchor labels (from panel_link.anchors)
    node_ids = {n["id"] for n in doc.get("nodes", []) if isinstance(n, dict) and "id" in n}
    pl = reserved.get("panel_link")
    anchors = pl.get("anchors") if isinstance(pl, dict) else None
    anchor_labels = set(anchors) if isinstance(anchors, dict) else set()

    # I-2 — per affordance: anchor resolves; kind ∈ enum; options iff choice
    for aid, entry in affs.items():
        if not isinstance(entry, dict):
            errors.append(f"I-2: affordance {aid!r} is not an object")
            continue
        anchor = entry.get("anchor")
        if anchor not in node_ids and anchor not in anchor_labels:
            errors.append(f"I-2: affordance {aid!r} anchor {anchor!r} does not resolve (orphaned affordance)")
        kind = entry.get("kind")
        if kind not in AFFORDANCE_KINDS:
            errors.append(f"I-2: affordance {aid!r} kind {kind!r} not in {list(AFFORDANCE_KINDS)}")
        options = entry.get("options")
        if kind == "choice":
            if not (isinstance(options, list) and options):
                errors.append(f"I-2: choice affordance {aid!r} must declare a non-empty options[]")
        elif options is not None:
            errors.append(f"I-2: affordance {aid!r} (kind {kind!r}) must not declare options[]")

    # I-3 — per response: references a declared affordance; value is kind-consistent
    for i, r in enumerate(responses):
        if not isinstance(r, dict):
            errors.append(f"I-3: responses[{i}] is not an object")
            continue
        aid = r.get("affordance")
        entry = affs.get(aid)
        if not isinstance(entry, dict):
            errors.append(f"I-3: responses[{i}] references undeclared affordance {aid!r}")
            continue
        errors += _interaction_value_kind_errors(str(aid), entry, r.get("value"))
    return errors


def _has_cycle(graph: dict[str, list[str]]) -> bool:
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {}

    def visit(u: str) -> bool:
        color[u] = GRAY
        for v in graph.get(u, []):
            if color.get(v, WHITE) == GRAY:
                return True
            if color.get(v, WHITE) == WHITE and visit(v):
                return True
        color[u] = BLACK
        return False

    return any(color.get(n, WHITE) == WHITE and visit(n) for n in list(graph))


def _validate_context_object(block: Any) -> list[str]:
    """spec_context_object §4 — stable id; semver version; well-formed refs."""
    errors: list[str] = []
    if not isinstance(block, dict):
        return ["A-7: context_object is not an object"]
    if not isinstance(block.get("id"), str) or not block["id"]:
        errors.append("A-7: context_object.id missing")
    v = block.get("version")
    if v is not None and not (isinstance(v, str) and _SEMVER.match(v)):
        errors.append(f"A-7: context_object.version {v!r} not semver")
    refs = block.get("refs", [])
    if not isinstance(refs, list):
        errors.append("A-7: context_object.refs must be a list")
    return errors
