---
type: spec
spec_id: spec_conformance_suite
title: "aDNA Canvas conformance suite — checks for Core / Extended / aDNA-Native"
standard_version: "2.0.1"
status: ratified
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
phase: P3
tags: [spec, canvas, conformance, validator, genesis, p3]
---

# aDNA Canvas Conformance Suite

> **Status: RATIFIED 2026-06-12 (operator, P2 gate) — P3 deliverable, HELD at the P3 exit gate.** Specifies the
> checks a validator runs for each conformance level + the degradation tests. It is a **contract**, not an engine —
> the reference validator is built later in `what/code/canvas_std/` (Option P / [[adr_001_canvasforge_relationship]]).
> Binds to [[adr_003_standard_governance]] §3 and [[spec_adna_canvas_standard]] §10. RFC 2119 keywords.

## 1. Validator contract

1.1. A conformant validator exposes `validate(doc, level) → {ok, level_reached, errors[]}` and
`strip(doc) → doc'` (removes `_reserved`). It lives in `what/code/canvas_std/` (the Standard ships its reference
tooling, Option P) — **not** in any producer.

1.2. Conformance is **monotone**: aDNA-Native ⊃ Extended ⊃ Core. `level_reached` is the highest level all of
whose checks pass. A document **MUST** declare its target level in `_reserved.conformance_level`; the validator
**MUST** verify the declared level is actually reached.

## 2. Core checks (C-*)

| ID | Check |
|----|-------|
| C-1 | Valid JSON; top-level `nodes` + `edges` arrays present. |
| C-2 | Every node has unique `id`, `type` ∈ {text,file,group,link}, integer `x`,`y`,`width`,`height`. |
| C-3 | Every edge has `id`, `fromNode`, `fromSide`∈sides, `toNode`, `toSide`∈sides; `fromNode`/`toNode` resolve. |
| C-4 | Every **directed** edge sets top-level `toEnd:"arrow"` ([[spec_adna_canvas_standard]] §5.2). |
| C-5 | `color` (if present) ∈ `"0".."6"` or `#`-hex. |

A Core-valid document **MUST** be a valid JSON Canvas 1.0 file (the degradation floor).

## 3. Extended checks (E-*)

| ID | Check |
|----|-------|
| E-1 | All of Core. |
| E-2 | `styleAttributes.shape`/`border`/`textAlign` ∈ the [[spec_adna_canvas_standard]] §6 enums. |
| E-3 | edge `styleAttributes.path`/`arrow`/`pathfindingMethod` ∈ §6 enums. |
| E-4 | Top-level `isStartNode`/`collapsed` are boolean; `portal`/`dynamicHeight` well-formed if present. |

## 4. aDNA-Native checks (A-*)

| ID | Check |
|----|-------|
| A-1 | All of Extended. |
| A-2 | `_reserved.adna_version` present + semver; `conformance_level` = `adna_native`. |
| A-3 | `_reserved.component_types` valid per [[spec_component_model]] §7 (keys resolve; `class`∈taxonomy; profile tokens∈§6; `degrades_to`∈baseline types). |
| A-4 | `_reserved.semantic_bindings` profiles use only §6 tokens; the built-in `lattice` profile is unmodified ([[spec_component_model]] §4.2). |
| A-5 | `_reserved.panel_link` valid per [[spec_panel_link_semantics]] §6 (ids resolve; `sequence` acyclic; exactly one `canonical` surface; no orphaned anchors). |
| A-6 | `_reserved.sync` present; `sync_hash` matches `compute_sync_hash(source)` **or** the canvas is flagged stale ([[spec_roundtrip_protocol_v2]] §3). |
| A-7 | `_reserved.context_object` (if present) valid per [[spec_context_object]] §4 (stable `id`; semver `version`; well-formed `refs`). |

## 5. Degradation tests (D-*) — the C4 contract

| ID | Check |
|----|-------|
| D-1 | `validate(strip(doc), core)` passes — stripping `_reserved` yields a valid Core/Obsidian canvas. |
| D-2 | `strip(doc)` introduces **no** new top-level node/edge keys and **no** `styleAttributes` token outside §6 (no-baseline-overload, [[spec_adna_canvas_standard]] §11.3). |
| D-3 | A vanilla JSON-Canvas reader opens `doc` without error (round-trip-to-baseline). |

A suite run **MUST** include D-1..D-3 for every aDNA-Native document — degradation is a first-class conformance property, not an afterthought.

## 6. Quality contract (separate from format conformance)

Format conformance (§2–§5) is distinct from **output quality**. Visual/narrative quality is reviewed via the
III framework against the **canvas review contract** Canvas.aDNA owns — the VR1–VR5 rubric + the canvas-visual
trap schema — specified in [[iii/CLAUDE]] (`iii/` wrapper). The conformance suite checks *format*; III checks
*quality*; the engines for both stay out of producers (`canvas_std` for format, III.aDNA for quality).

## 7. Conformance report

`validate` returns a report: `{ standard_version, level_reached, declared_level, passed: [ids], failed: [{id, node/edge, msg}], degradation: {D-1,D-2,D-3} }`. Producers attach it to a build artifact as evidence (feeds the P3 federation 5-stage gates §3 — `spec_federation_contract.md`).

## 8. Related
- [[adr_003_standard_governance]] §3 (levels) · [[spec_adna_canvas_standard]] §10 (validation) · [[spec_component_model]] · [[spec_panel_link_semantics]] · [[spec_roundtrip_protocol_v2]] · `spec_federation_contract.md` · `what/code/canvas_std/` (reference validator, P-Option).
