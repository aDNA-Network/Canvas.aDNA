---
plan_id: mission_p3_conformance_federation
type: plan
title: "P3 — Conformance & Federation Contract"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis_planning
campaign_phase: 3
campaign_mission_number: 3
mission_class: implementation
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
tags: [plan, campaign, genesis, canvas, p3, conformance, federation, iii]
---

# Mission: P3 — Conformance & Federation Contract

**Campaign**: [[how/campaigns/campaign_canvas_genesis_planning/campaign_canvas_genesis_planning|campaign_canvas_genesis_planning]] (Operation Cartography)
**Phase**: 3 — Conformance & Federation Contract
**Mission**: 3 of N

> **✅ DELIVERABLES COMPLETE — HELD at the P3 exit gate, 2026-06-12.** Authored on operator go ("Ratify all → P3")
> directly after the P2 ratification. Builds on the ratified v2.0.0 spec set + ADRs (D2 extract / D3 schema-absorb
> + federated / D6 governance). **Operator reviews the consumer-integration story end-to-end** to clear the gate.

## Goal

Specify (1) how a canvas is checked against the three conformance levels and (2) how producers consume the
Standard via the SiteForge forge pattern, with worked examples for CanvasForge + an LF-successor + ≥1 net-new
consumer, plus an `iii/` quality wrapper. Planning only — contracts, not engines (C8).

## Exit Gate

Operator reviews the consumer-integration story end to end (campaign charter, P3 gate).

## Objectives

### 1. Conformance-suite spec → `what/specs/spec_conformance_suite.md`
- **Status**: completed — Core/Extended/aDNA-Native check sets + degradation tests + the validator contract
  (validator lives in `canvas_std`, per D2 extract). Binds to `adr_003` levels + `spec_adna_canvas_standard` §10.

### 2. Federation contract → `what/specs/spec_federation_contract.md`
- **Status**: completed — the SiteForge forge pattern applied to the Canvas Standard: `federation_ref` field set,
  graft discipline, `version_policy: minor`, 5-stage gates, wrapper discipline; 3 worked consumers
  (CanvasForge / LF-successor / net-new "letter" producer).

### 3. Reference `.lattice.yaml` stub → `what/lattices/examples/example_canvas_v2.lattice.yaml`
- **Status**: completed — a minimal v2.0.0 canvas-bearing lattice showing the `_reserved` extension block
  (component_types / semantic_bindings / panel_link / context_object) + sync + a `federation_ref` to the Standard.

### 4. `iii/` wrapper scaffold → `iii/CLAUDE.md` (+ empty learning store)
- **Status**: completed — federates to III.aDNA (Argus); asserts the **canvas review contract** (VR1–VR5 rubric +
  canvas-visual trap schema) is **Canvas.aDNA-owned** while the III **engines** stay upstream (specify contracts,
  not engines). Consumes `context_iii_canvas_visual`.

## Campaign Context

### Previous Mission Outputs (P2, ratified)
- v2.0.0 spec set + `adr_001/002/003`. D2 extract → validator/conformance location is `canvas_std`; D3 → LF
  successor is a federated producer (a worked example here).

### Next Mission Inputs (P4)
- The federation contract + conformance suite → the execution-campaign charter's migrate/parity gates.

## Completion Summary

### Deliverables
- `spec_conformance_suite.md` · `spec_federation_contract.md` · `example_canvas_v2.lattice.yaml` · `iii/CLAUDE.md`
  (+ `iii/what/context/canvas_iii_learning_store.jsonl`).

### Key Findings
- Canvas.aDNA's standard-bearer status inverts the usual III posture: the canvas review **contract** (VR1–VR5 +
  trap schema) is owned **here**, not in CanvasForge — the wrapper documents that authority while keeping III's
  engines upstream. A clean "specify contracts, not engines" exemplar.
- The federation contract needed a `tracking` version_policy note: pre-1.0 producers (like today's CanvasForge)
  pin by commit, not minor — surfaced as a conformance caveat.

### Scope Changes
- None.

## AAR

- **Worked**: the two pattern-research passes (sf_forge + a real `iii/` wrapper) let the federation contract +
  wrapper be authored conformant-to-precedent in one pass.
- **Didn't**: III version pin ambiguity (router says v0.4.0; sibling wrappers track v0.5.0) — pinned v0.4.0 with a
  confirm-at-wiring note rather than guess.
- **Finding**: the standard-bearer owns the *review contract*; the framework owns the *engine* — a reusable split.
- **Change**: confirm the III pin against `III.aDNA/STATE.md` when the wrapper is actually wired (execution).
- **Follow-up**: **HELD at P3 exit gate** — operator reviews the consumer story; then P4 (execution charter).
