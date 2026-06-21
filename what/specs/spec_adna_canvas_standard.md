---
type: spec
spec_id: spec_adna_canvas_standard
title: "aDNA Canvas Standard v2.0.0 — normative specification"
standard_version: "2.0.1"
status: ratified
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
phase: P2
upstream_baseline: "Advanced Canvas v5.6.6 + JSON Canvas 1.0 (PIN-A)"
tags: [spec, canvas, standard, normative, genesis, p2]
---

# aDNA Canvas Standard — v2.0.0 (normative)

> **Status: RATIFIED 2026-06-12 (operator, P2 gate).** Supersedes the embedded *Canvas Standard v1.0.0*
> ([[p1_source_inventory]] §A3). Normative core; the component model (D4), panel/link semantics (D5), round-trip
> (v2), and context-object (D7) are specified in their own documents and referenced here. Key words **MUST /
> MUST NOT / SHOULD / MAY** per RFC 2119.

## 1. Scope & conformance

This spec defines the file format, document/node/edge schema, the `_reserved` extension carrier, validation
rules, conformance levels, and the Obsidian-degradation contract for an aDNA canvas. It is **substrate-neutral**:
application-specific rendering, layout, composition, and image generation are out of scope and belong to
producers (CanvasForge / ComfyForge / LF-successor / SiteForge), per [[adr_001_canvasforge_relationship]].

A conformant document declares its level in `_reserved.conformance_level` ∈ {`core`, `extended`, `adna_native`}
(see §9 and [[adr_003_standard_governance]] §3).

## 2. Normative references (baseline pin, PIN-A)

- **JSON Canvas 1.0** — the base `.canvas` format floor (top-level `nodes`, `edges`).
- **Advanced Canvas v5.6.6** — the upstream fork point (cited verbatim in the v1.0.0 corpus); contributes
  `styleAttributes`, `isStartNode`, `collapsed`, `portal`, `dynamicHeight`, and the edge `path`/`arrow`/
  `pathfindingMethod` vocabularies. Drift to ~v6.2.1 is tracked (absorbed additively, never as a baseline reset).

## 3. File model

3.1. An aDNA canvas has an **authoritative source** and a **view**. The `.canvas` JSON is the **view layer**; an
external **authoritative source** (the `.lattice.yaml` for lattice canvases, generalized to any authoritative
document) is the semantic source of truth. A consumer **MUST NOT** assume edits to the `.canvas` propagate back
automatically; the reverse path is advisory (see `spec_roundtrip_protocol_v2.md`).

3.2. The `.canvas` document is JSON with top-level `nodes` (array) and `edges` (array), plus a `metadata` object
carrying `frontmatter._reserved` (§7). A document with no `metadata._reserved` is a **Core**-level canvas.

## 4. Node schema

4.1. Every node **MUST** carry: `id` (string, unique), `type` ∈ {`text`, `file`, `group`, `link`}, and integer
geometry `x`, `y`, `width`, `height`. `color` (string, §6) is **OPTIONAL**.

4.2. Type-dependent payload: `text` nodes carry `text` (markdown); `file` nodes carry `file` (vault path); `link`
nodes carry `url`; `group` nodes carry an optional `label`.

4.3. **Advanced Canvas extensions** (Extended level): a `styleAttributes` object MAY carry `shape`, `border`,
`textAlign` (within the §6 enums); top-level `isStartNode` (bool), `collapsed` (bool), `portal`, `dynamicHeight`
MAY be present. Absence of `shape` denotes the default rectangle.

4.4. aDNA-native component semantics (component class, semantic-type binding, brand hooks) are carried in
`_reserved` (§7), **never** as new top-level node keys — see `spec_component_model.md`.

## 5. Edge schema

5.1. Every edge **MUST** carry: `id` (string), `fromNode` (node id), `fromSide` ∈ {top,bottom,left,right},
`toNode` (node id), `toSide` ∈ {top,bottom,left,right}. `label`, `color` are **OPTIONAL**.

5.2. Every **directed** edge **MUST** set top-level `toEnd: "arrow"` (Obsidian defaults to no arrow; this is a
hard invariant — [[p1_fork_baseline]] I4). `fromEnd`/`toEnd` are top-level, **not** in `styleAttributes`.

5.3. Extended-level edge styling lives in `styleAttributes`: `path` ∈ {dotted, short-dashed, long-dashed},
`arrow`, `pathfindingMethod` ∈ {square, a-star}. Typed-edge semantics (data/control/optional/…) bind via
`_reserved` — see `spec_panel_link_semantics.md` and `spec_component_model.md`.

## 6. Value enums (KEEP, verbatim floor)

A validator **MUST** accept exactly these tokens (from [[p1_fork_baseline]] §3):

- `node.type`: `text, file, group, link`
- `styleAttributes.shape`: *(absent)*, `pill, diamond, parallelogram, circle, predefined-process, document, database`
- `styleAttributes.border`: *(absent)*, `dashed, dotted, invisible`
- `styleAttributes.textAlign`: *(absent=left)*, `center, right`
- `color`: `"0".."6"` (semantic slots) **or** a `#`-prefixed hex string
- edge `path`: *(absent)*, `dotted, short-dashed, long-dashed`
- edge `arrow`: *(absent)*, `triangle-outline, thin-triangle, halved-triangle, diamond, diamond-outline, circle, circle-outline`
- edge `pathfindingMethod`: *(absent)*, `square, a-star`
- edge `fromEnd`/`toEnd`: `none, arrow`

Semantic color slots (convention, SHOULD): `"1"` red = warn/error, `"2"` orange = note, `"3"` yellow =
highlight; `"4""5""6"` = node-type colors. Edge-style convention (SHOULD): solid = data flow, `long-dashed` =
control/federation, `dotted` = optional.

## 7. The `_reserved` extension block (aDNA-Native)

7.1. All aDNA-native semantics **MUST** live under `metadata.frontmatter._reserved` (a preserved, no-validation
custom store in baseline Obsidian — [[p1_fork_baseline]] I3). This is the **only** carrier for v2.0.0 additions;
the baseline node/edge fields are **not** extended (§11).

7.2. Reserved keys (schemas in the cited specs):
```
_reserved:
  adna_version:        "2.0.0"
  conformance_level:   core | extended | adna_native
  sync:                { sync_hash, source_name, source_version }   # §8, spec_roundtrip_protocol_v2
  component_types:     { … }     # spec_component_model.md (D4)
  semantic_bindings:   { … }     # spec_component_model.md (D4)
  panel_link:          { … }     # spec_panel_link_semantics.md (D5)
  brand_style_pack_ref: <federation_ref>   # producer-resolved (VisualDNA)
  context_object:      { … }     # spec_context_object.md (D7)
```
7.3. Unknown `_reserved` keys **MUST** be preserved by any tool that rewrites a canvas (forward-compat).

## 8. Required `_lattice_meta` group

8.1. A lattice canvas **MUST** include a group node with `id: "_lattice_meta"` encoding the source name +
version and the **sync hash** of the authoritative-source topology ([[p1_fork_baseline]] I2). The sync hash
detects view staleness (`spec_roundtrip_protocol_v2.md`). For non-lattice canvases the equivalent metadata MAY
live solely in `_reserved.sync`.

## 9. Conformance levels

Per [[adr_003_standard_governance]] §3: **Core** (JSON Canvas 1.0 + the §4/§5/§6 floor incl. `toEnd:"arrow"`) ⊂
**Extended** (Core + Advanced Canvas `styleAttributes` within §6 enums) ⊂ **aDNA-Native** (Extended + a populated
`_reserved` block). A document **MUST** satisfy every rule of its declared level.

## 10. Validation rules (normative summary)

A conformant validator **MUST** reject a document that: has a duplicate or missing `id`; has a node `type`,
`shape`, `border`, `textAlign`, `color`, edge `path`/`arrow`/`pathfindingMethod`, or `fromSide`/`toSide` outside
§6; has a directed edge missing `toEnd:"arrow"`; references a non-existent `fromNode`/`toNode`; or (aDNA-Native)
carries a `_reserved` block that fails the cited sub-spec schemas. The reference validator lives in
`what/code/canvas_std/` (Option P; built in the execution campaign — [[adr_001_canvasforge_relationship]]).

## 11. Obsidian degradation contract (C4)

For any aDNA canvas `K` (per [[p1_fork_baseline]] §5): **(1) Strip** — removing `metadata.frontmatter._reserved`
yields a valid JSON Canvas 1.0 / Advanced Canvas v5.6.6 file. **(2) Ignore** — a vanilla reader opens `K`
unchanged and ignores `_reserved`. **(3) No-baseline-overload** — v2.0.0 introduces **no** new top-level node/edge
keys and **no** new `styleAttributes` tokens outside §6; new power is in `_reserved` or proposed upstream. **(4)**
the P3 conformance suite **MUST** include a degradation test: `validate(strip(K))` passes the baseline schema.

## 12. Related
- [[adr_001_canvasforge_relationship]] · [[adr_002_literatureforge_seam]] · [[adr_003_standard_governance]]
- `spec_component_model.md` · `spec_panel_link_semantics.md` · `spec_roundtrip_protocol_v2.md` · `spec_context_object.md`
- [[p1_fork_baseline]] (invariants/enums) · [[p1_source_inventory]] · [[adr_000_canvas_identity]] §4.
