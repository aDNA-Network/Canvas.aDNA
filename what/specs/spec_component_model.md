---
type: spec
spec_id: spec_component_model
title: "aDNA Canvas component model (D4) — typed components across all 2D outputs"
standard_version: "2.0.0"
status: ratified
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
phase: P2
resolves: D4
tags: [spec, canvas, component-model, genesis, p2, d4]
---

# aDNA Canvas Component Model (D4)

> **Status: RATIFIED 2026-06-12 (operator, P2 gate).** Defines the additive, `_reserved`-namespaced component
> taxonomy that generalizes the v1.0.0 lattice-only mappings to *every* 2D output. Extends — does not replace —
> the [[spec_adna_canvas_standard]] node/edge floor. RFC 2119 keywords.

## 1. Scope

A **component** is a typed role layered onto a baseline node (or group) via `_reserved.component_types`. The
baseline `type` (text/file/group/link) and geometry stay in the node (degradation floor); the component class +
semantics live in `_reserved`. This generalizes `TYPE_MAPPING`/`EDGE_TYPE_MAPPING` ([[p1_source_inventory]] §B1),
folds in the four design-doc schema fragments (§C ⚑ rows), and absorbs the LiteratureForge visual contract (§D1).
Rendering of any component is **producer** business (C8).

## 2. Component taxonomy

| Component class | Baseline carrier | Purpose |
|-----------------|------------------|---------|
| `text` | text node | Prose / markdown block |
| `typography_run` | text node + style | A styled inline/heading run (weight/size/role) |
| `image` | file/link node | Raster or vector still |
| `video` | file/link node | Time-based media |
| `shape` | text/group + `styleAttributes.shape` | Diagrammatic primitive |
| `embed` | file/link node + `portal` | Embedded canvas/doc/widget |
| `group` / `panel` | group node | A bounded region grouping components (= "panel") |
| `link` / `edge` | edge | A typed relation between components |
| `table` | text node (or group) | Tabular data block |
| `code` | text node | Code block (language-tagged) |
| `caption` | text node bound to a target | Figure/table caption with a ref |
| `region` | group node | A layout/flow region (pagination/responsive) — see `spec_panel_link_semantics.md` |

A component class **MUST** degrade: stripping `_reserved` leaves a valid baseline node/group/edge ([[spec_adna_canvas_standard]] §11).

## 3. Component record schema

Each entry in `_reserved.component_types` is keyed by node/edge `id`:
```
component_types:
  <node_id>:
    class:            <one of §2>
    semantic_type:    <profile-defined, §4>          # optional
    qualities:        { … }                           # class-specific (e.g. language for code, level for typography_run)
    brand_style_pack_ref: <federation_ref>            # optional, §6
    degrades_to:      text | file | group | link      # the baseline type a stripper leaves
```
A tool **MUST** preserve unknown `qualities` keys (forward-compat).

## 4. Semantic bindings (generalizes `TYPE_MAPPING`)

4.1. `_reserved.semantic_bindings` maps a **semantic_type** → visual defaults `{ color, shape, node_type }`,
generalizing the lattice-only map to any output domain via **named profiles**.

4.2. The v1.0.0 lattice map is **KEEP**, registered as the built-in profile `lattice` (verbatim, [[p1_fork_baseline]] §3):
`module→{"4",predefined-process,file}`, `dataset→{"5",database,file}`, `reasoning→{"6",diamond,text}`,
`process→{∅,∅,text}`, `input→{"4",parallelogram,text}`, `output→{"5",parallelogram,text}`, `start→{∅,pill,text}`,
`end→{∅,pill,text}`. Edge profile (KEEP): `data, control(long-dashed), optional(dotted,triangle-outline),
bidirectional, weak(short-dashed,circle-outline)`.

4.3. New domains (deck, comic, paper, letter, site) register **additional** profiles (e.g. `deck`, `document`)
without altering the `lattice` profile. A profile's tokens **MUST** stay within the [[spec_adna_canvas_standard]]
§6 enums (so Extended-level degradation holds).

## 5. CSS-class & role-attribute bindings (⚑ C2/C3)

5.1. A component MAY carry `qualities.css_classes` (string list). The Standard owns the **binding contract**: a
class token serializes to the node and surfaces as a DOM `data-css-classes` attribute (from §C2). The *class
list itself* and any palette are **producer** taste, not normative here.

5.2. A component MAY carry `qualities.role` (e.g. `stage`, `hero`) serialized as `styleAttributes.latticeRole` →
DOM `data-lattice-role` (from §C3). The Standard owns the **role-attribute namespace + serialization**; the role
*vocabulary* is producer/profile-defined.

## 6. Visual-component contract (absorbed from LF D1)

6.1. A visual component MAY declare `qualities.substrate` ∈ {`canvas`, `raster`} — the typed routing axis from the
LF visual contract ([[p1_source_inventory]] §D1). `canvas` components are Standard-native; `raster` components are
producer/ComfyForge-generated and embedded as `image`/`file`.

6.2. `brand_style_pack_ref` is a `federation_ref` to a VisualDNA brand pack (style lock, palette, composition).
The Standard carries the **reference**; the pack contents + resolution are producer/VisualDNA business.

6.3. `qualities.style_lock` ∈ {`internal`, `external`} and `qualities.aspect_ratio` MAY be present (per-surface
geometry from the LF X-fields); they inform panel/link region sizing (`spec_panel_link_semantics.md`).

## 7. Conformance

A component_types block is an **aDNA-Native** feature. A validator **MUST** check: each key references an existing
node/edge `id`; `class` ∈ §2; profile tokens ∈ [[spec_adna_canvas_standard]] §6; `degrades_to` ∈ {text,file,group,link}.
Absent `_reserved.component_types` → the canvas is Core/Extended (no component semantics), still valid.

## 8. Related
- [[spec_adna_canvas_standard]] (node/edge floor + `_reserved`) · `spec_panel_link_semantics.md` (region/flow) ·
  [[adr_002_literatureforge_seam]] (visual-contract absorption) · [[p1_source_inventory]] §B1/§C/§D1 · [[p1_fork_baseline]] §3.
