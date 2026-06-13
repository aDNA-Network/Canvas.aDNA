---
plan_id: mission_p1_source_inventory
type: plan
title: "P1 — Source Inventory & Fork Baseline"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis_planning
campaign_phase: 1
campaign_mission_number: 1
mission_class: reconnaissance
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
tags: [plan, campaign, genesis, canvas, p1, inventory]
---

# Mission: P1 — Source Inventory & Fork Baseline

**Campaign**: [[how/campaigns/campaign_canvas_genesis_planning/campaign_canvas_genesis_planning|campaign_canvas_genesis_planning]] (Operation Cartography)
**Phase**: 1 — Source Inventory & Fork Baseline
**Mission**: 1 of 1 (this phase)

## Goal

Produce the empirical foundation the v2.0.0 Standard forks from: a labeled catalog of every source
artifact (the embedded Canvas Standard v1.0.0, the `CanvasBuilder` constants, the `advanced_canvas/`
corpus, the Round-Trip Protocol, the graft_manifest, and the LiteratureForge visual/format/genre specs)
and a fork-baseline doc (what v2.0.0 inherits, the additive `_reserved` extension map, and the pinned
upstream version). This lets P2 author the normative spec on solid, classified ground rather than re-deriving
from scratch. Planning only — no code, no migration, no breaking changes (C3).

## Exit Gate

Operator reviews the **KEEP / EXTEND / SUPERSEDE / DEFER-TO-PRODUCER** classification and the **upstream
version pin** decision. (Per campaign charter, Phase P1 exit gate.)

## Objectives

### 1. Catalog the v1.0.0 standard + schema + round-trip + graft
- **Status**: completed
- **Session**: session_stanley_20260612_211907_p1_source_inventory
- **Description**: Read & classify `advanced_canvas/` standard/schema/roundtrip/validation/tooling-gaps/graft.
- **Files**: `p1_source_inventory.md` §A
- **Depends on**: none

### 2. Extract & classify the `CanvasBuilder` constants + reference-impl surface
- **Status**: completed
- **Description**: Transcribe `VALID_*`, `TYPE_MAPPING`, `EDGE_TYPE_MAPPING` verbatim; classify the
  builder's normative core vs. application convenience; mark Option-P extraction targets.
- **Files**: `p1_source_inventory.md` §B; feeds `p1_fork_baseline.md`
- **Depends on**: none

### 3. Classify the design context corpus (15 docs) + LF specs (3)
- **Status**: completed
- **Description**: Separate normative schema hiding in design docs (EXTEND) from producer design taste
  (DEFER); classify the LF visual/format/genre specs and capture the D3 signal.
- **Files**: `p1_source_inventory.md` §C, §D
- **Depends on**: none

### 4. Author the fork-baseline (inheritance map + `_reserved` map + version pin)
- **Status**: completed
- **Description**: Pin the upstream baseline; map what v2.0.0 inherits from Advanced Canvas + v1.0.0;
  define the additive `_reserved` extension map; restate the C4 degradation contract.
- **Files**: `p1_fork_baseline.md`
- **Depends on**: 1, 2, 3

### 5. Reconcile the inherited template scaffold
- **Status**: completed
- **Description**: Archive `adr_001/002/003` + `campaign_adna_workspace_upgrade/` to `_inherited_scaffold/`
  holders (operator chose archive-to-holder); free the `adr_001+` namespace for P2's real ADRs.
- **Files**: `what/decisions/_inherited_scaffold/`, `how/campaigns/_inherited_scaffold/`, `decision_register_genesis.md`
- **Depends on**: none

## Campaign Context

### Previous Mission Outputs
- P0: `adr_000` (Mondrian; Platform/Option P; scope confirmed) + `decision_register_genesis.md` (D1–D7) + charter.

### Next Mission Inputs
- P2 (Standard spec) consumes: the KEEP/EXTEND set (schema floor + round-trip + constants), the SUPERSEDE
  target (standalone normative spec replacing the embedded framing), the `_reserved` extension map, the
  pinned baseline, and the D3 signal (LF absorb-vs-peer).

## Notes

- Upstream version **resolved at source**: v1.0.0 cites Advanced Canvas **v5.6.6** verbatim
  (`context_advanced_canvas_standard.md:103`, `schema.md:60`); **no JSON Canvas spec version cited**. Current
  upstream is **~v6.2.1** → drift-delta recorded for P2/execution evaluation.
- Inventory built via 4 parallel read-and-classify subagents (lean-context synthesis); verbatim constants
  and invariants captured in the deliverables.

## Completion Summary

### Deliverables
- `p1_source_inventory.md` — labeled catalog (28 source rows across 4 clusters).
- `p1_fork_baseline.md` — inheritance map + `_reserved` extension map + pinned baseline (v5.6.6) + degradation contract.
- Inherited scaffold archived to `_inherited_scaffold/` holders; `adr_001+` namespace freed.

### Descoped
- None. (Both P1 deliverables + reconciliation completed in one pass per operator decision.)

### Key Findings
- No source file is *already* generalized across all 2D outputs — EXTEND work is net-new in P2, performed
  *on* the KEEP invariants (schema floor + round-trip) and the SUPERSEDE target (the embedded standard).
- The LF `format_contract`'s `round_trip_surface` already cross-references the Canvas Round-Trip Protocol —
  the strongest single absorb-signal for D3 (still leaves a clean producer seam; not decided here).
- `CanvasBuilder` has no literal `to_canvas`/`from_canvas`; `build()`/`read_back()` fill those roles — alias
  at extraction so the conformance vocabulary matches the API.

### Scope Changes
- None.

## AAR

- **Worked**: Parallel read-and-classify subagents produced a verbatim-grounded, fully-labeled inventory in one pass; the upstream pin resolved at source rather than by external lookup alone.
- **Didn't**: The "~22 files" estimate undercounted the *constant families* — core.py carries 10 `VALID_*` enums (not 5), surfaced and captured.
- **Finding**: The normative Standard already exists, scattered — schema floor (KEEP), round-trip (KEEP), and four design-doc schema fragments (EXTEND) — the embedded "standard" doc is mostly framing to SUPERSEDE.
- **Change**: Carry the `_reserved` extension map + the no-`to_canvas`/`from_canvas` aliasing note into P2 so the spec's component model and the reference-impl API agree from the start.
- **Follow-up**: P2 mints real ADRs for D2/D3/D6 + the component/panel-link/context-object specs into the freed `adr_001+` namespace.
