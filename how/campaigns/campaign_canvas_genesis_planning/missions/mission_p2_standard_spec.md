---
plan_id: mission_p2_standard_spec
type: plan
title: "P2 — Standard Specification (v2.0.0 core)"
owner: stanley
status: planned
campaign_id: campaign_canvas_genesis_planning
campaign_phase: 2
campaign_mission_number: 2
mission_class: implementation
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
tags: [plan, campaign, genesis, canvas, p2, standard, spec]
---

# Mission: P2 — Standard Specification (v2.0.0 core)

**Campaign**: [[how/campaigns/campaign_canvas_genesis_planning/campaign_canvas_genesis_planning|campaign_canvas_genesis_planning]] (Operation Cartography)
**Phase**: 2 — Standard Specification (the core deliverable; heaviest gate)
**Mission**: 2 of N

> **📋 CHARTERED 2026-06-12 — awaiting operator go to execute.** P1 exit gate cleared (classification ratified;
> PIN-A locked). This charter decomposes P2; **no P2 ADR or spec is authored until the operator approves the go**
> (phase gates are human gates, SO-1). Built directly on the accepted P1 deliverables
> ([[p1_source_inventory]] · [[p1_fork_baseline]]).

## Goal

Produce the **normative aDNA Canvas Standard v2.0.0** — the campaign's core output. Consolidate the P1-classified
sources into: three load-bearing ADRs (D2 CanvasForge relationship · D3 LiteratureForge seam · D6 governance) and
five specs (the normative standard, component model, panel/link semantics, round-trip v2, context-object). On
completion, Canvas.aDNA has a ratifiable spec a producer can conform to — the input P3 (conformance + federation)
and P4 (execution charter) build on. Still **planning** (C3): specs + ADRs only, no runnable code.

## Exit Gate

**Operator signs off on the v2.0.0 spec + the D2/D3 decisions** (campaign charter, P2 gate — the heaviest).
Recommended **internal checkpoint α** after the three foundational ADRs (O1–O3), before the specs build on them.

## Baseline locked (from P1 — do not re-litigate)

- **Upstream:** Advanced Canvas **v5.6.6** + **JSON Canvas 1.0** (PIN-A); v5.6.6→~v6.2.1 drift absorbed
  *additively* via `_reserved`, never as a baseline reset.
- **KEEP (verbatim floor):** the JSON node/edge/`metadata` schema (A1), the Round-Trip Protocol (A2), the 10
  `VALID_*` enums (B1). See [[p1_fork_baseline]] §2–§3.
- **`_reserved` namespace:** fixed at P1; this mission mints the key *schemas* (`component_types`,
  `semantic_bindings`, `panel_link`, `conformance_level`, `context_object`). See [[p1_fork_baseline]] §4.
- **Degradation contract (C4):** strip `_reserved` → valid Obsidian canvas. See [[p1_fork_baseline]] §5.
- **ADR namespace `adr_001+` is free** (scaffold archived at P1).

## Objectives

> Order is dependency-driven: foundational ADRs first (they decide *where* the spec/impl lives and *how* it is
> versioned), then the normative spec, then the dependent component/panel-link/round-trip/context specs.

### 1. ADR — D2 CanvasForge relationship  → `what/decisions/adr_001_canvasforge_relationship.md`
- **Status**: planned
- **Description**: Score A (extract Standard OUT → CanvasForge consumes via `federation_ref`, becomes pure
  producer; mirrors the `lattice-protocol→canvasforge` extraction precedent) vs B (spec-here/impl-stays-in-
  CanvasForge) vs C (reject). **P1 evidence (§B inventory) tilts → A**: the builder's normative core is cleanly
  separable from producer convenience, and Option P already homes the reference impl at `what/code/canvas_std/`.
  Record the chosen option + the rejected ones + the parity-gated migration shape (execution-campaign, not now).
- **Depends on**: none (P1 accepted)

### 2. ADR — D3 LiteratureForge seam  → `what/decisions/adr_002_literatureforge_seam.md`
- **Status**: planned
- **Description**: Resolve A (document-AS-canvas) vs B (federated peers) vs C (absorb — operator-directed
  starting point 2026-06-07). **P1 signal (§D):** the LF format-spec's `round_trip_surface` *already*
  cross-references the Canvas Round-Trip Protocol (strongest absorb-signal), but the clean producer seam keeps
  federated-peer viable. If **absorb**, this ADR **re-opens P0 Option-P scope** (Canvas → a two-faced platform:
  producer-neutral Standard face + a producer face absorbing LF's composition pipeline, Thoth as sub-persona) —
  flag the two sub-forks (producer scope; substrate-neutrality firewall) per
  `aDNALabs.aDNA/what/migration/decision_literatureforge_canvas_subsumption.md`. **Couples to D2.**
- **Depends on**: 1 (couples to D2)

### 3. ADR — D6 versioning & governance  → `what/decisions/adr_003_standard_governance.md`
- **Status**: planned
- **Description**: Ratify the **v2.0.0** successor line; the LIP-style change process (real mechanism
  `lattice-labs/how/governance/lips/lip_0001_lip_process.md`); the three **conformance levels Core / Extended /
  aDNA-Native**; consumer `version_policy` default **minor**. The major bump is justified here (new component
  model + panel/link + context-object).
- **Depends on**: none

### ◆ Internal checkpoint α (recommended) — operator reviews O1–O3 before the specs build on them.

### 4. SPEC — normative v2.0.0 standard  → `what/specs/spec_adna_canvas_standard.md`
- **Status**: planned
- **Description**: The normative spec that **SUPERSEDES** the embedded v1.0.0 framing (§A3). Contains: the JSON
  shape (KEEP floor + Advanced Canvas v5.6.6 extensions); the `_reserved` extension block; the required
  `_lattice_meta`; node/edge schemas; the three conformance levels (per O3); validation rules; the **Obsidian
  degradation contract**. The spine the other four specs slot into.
- **Depends on**: 1 (where it lives), 3 (levels/versioning)

### 5. SPEC — component model (D4)  → `what/specs/spec_component_model.md`
- **Status**: planned
- **Description**: The generalized, `_reserved`-namespaced component taxonomy across all 2D outputs
  {text, typography-run, image, video, shape, embed, group/panel, link/edge, table, code, caption, region}.
  Generalizes `TYPE_MAPPING`/`EDGE_TYPE_MAPPING` **beyond the 8 lattice types** (KEEP the 8 as a registered
  profile) and folds in the four ⚑ design-doc schema fragments (C1 visual-vocabulary, C2 css-class binding,
  C3 latticeRole, C4 isStartNode/portal) + the LF visual-component contract (D1). Each component: schema ·
  position/qualities · aDNA semantic-type binding · `brand_style_pack_ref` hook · degradation rule.
- **Depends on**: 4 (, 2 if absorb → must cover long-form document components)

### 6. SPEC — panel/link semantics (D5)  → `what/specs/spec_panel_link_semantics.md`
- **Status**: planned
- **Description**: Reading-order / flow / pagination / region / sequence for **non-DAG** outputs
  (papers/letters/decks/comics/sites) expressed as typed edges + region properties **without breaking
  lattice-graph semantics**. Built from C4 (slide-graph) + the LF format-spec's ordered/order-locked `sections`
  + `output_surfaces` (D2 inventory row).
- **Depends on**: 4, 5

### 7. SPEC — round-trip protocol v2  → `what/specs/spec_roundtrip_protocol_v2.md`
- **Status**: planned
- **Description**: Generalize the KEEP A2 protocol: authoritative-source ↔ view; the authority matrix;
  `compute_sync_hash` staleness detection; advisory reverse path. Generalize "`.lattice.yaml`" → "authoritative
  source" for non-lattice outputs; keep the lossy-by-design boundary.
- **Depends on**: 4

### 8. SPEC — context-object model (D7, Δ2)  → `what/specs/spec_context_object.md`
- **Status**: planned
- **Description**: How an aDNA canvas is a first-class **context** object (stored · referenced via wikilinks /
  `federation_ref` · versioned; read-AS-context vs render-AS-output). Document **Δ2** (canvas-as-primitive vs
  canvas-as-view) and route it through a **LIP** — **do NOT touch the aDNA core primitive set** in this campaign
  (out of scope). Produces the LIP draft as an output, not a core change.
- **Depends on**: 4

## Campaign Context

### Previous Mission Outputs (P1, accepted)
- `p1_source_inventory.md` (28 sources classified) · `p1_fork_baseline.md` (invariants + `_reserved` map +
  PIN-A) · freed `adr_001+` namespace.

### Next Mission Inputs (P3)
- A ratified v2.0.0 spec + conformance levels (O3/O4) → P3 conformance-suite spec; the federation posture
  (O1/O2) → P3 federation contract + `iii/` wrapper.

## Notes

- **`what/specs/` does not exist yet** — O4 creates it (P2 is the first phase to write specs; P1 outputs are
  campaign-local).
- Deck-generator parked mission (`mission_deck_generator_canvas_pilot`) stays parked — a P4 execution candidate;
  no change here.
- Proposed ADR numbering (D2→`adr_001`, D3→`adr_002`, D6→`adr_003`) is recorded in `decision_register_genesis.md`;
  adjust at execution if the operator prefers a different assignment.

## Completion Summary

*Fill out when setting `status: completed`.*

## AAR

*Mandatory before `status: completed`.*
