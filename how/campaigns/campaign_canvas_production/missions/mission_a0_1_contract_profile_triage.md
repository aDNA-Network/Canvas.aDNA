---
plan_id: mission_a0_1_contract_profile_triage
type: plan
title: "A0.1 — Production-contract + profile triage (decision record)"
owner: stanley
status: completed
campaign_id: campaign_canvas_production
campaign_phase: 0
campaign_mission_number: 1
mission_class: reconnaissance
created: 2026-06-21
updated: 2026-06-21
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, production, atelier, decision]
---

# Mission: A0.1 — Production-contract + profile triage (decision record)

**Campaign**: [[how/campaigns/campaign_canvas_production/campaign_canvas_production|campaign_canvas_production]]
**Phase**: 0 — Spec/contract triage
**Mission**: 1 of 9

## Goal

Resolve the six governance/contract questions that gate the diagram and comic builds — **before** any code — and
record them as a single ratifiable decision record. This removes the only governance ambiguity ahead of A1/A2 (the
Keystone lesson: governance touches discovered mid-build cost the most). No code, no spec edits.

## Exit Gate

A decision record exists capturing the 6 Decision Points (quality-contract posture · profiles-are-producer-side ·
shape-enum policy · diagram-type scope · comic data-driven scope · codename), each with a doctrine-aligned default and
rationale; the absence of any dedicated diagram/comic spec in `what/specs/` is confirmed. **The operator ratifies the
record at the A0→A1 gate — that ratification activates the campaign and authorizes A1.**

## Objectives

### 1. Confirm spec landscape
- **Status**: completed
- **Session**: session_stanley_20260621_193649_atelier_scaffold_a0
- **Description**: Verify no dedicated `spec_diagram_*` / `spec_comic_*` exists; note where diagram/comic are already referenced (federation/component/panel-link specs).
- **Files**: `what/specs/` (read-only)
- **Depends on**: none

### 2. Author the decision record
- **Status**: completed
- **Session**: session_stanley_20260621_193649_atelier_scaffold_a0
- **Description**: Write the 6-decision triage record with defaults + rationale.
- **Files**: `missions/artifacts/a0_1_contract_profile_decision.md`
- **Depends on**: 1

### 3. Operator ratification (A0→A1 gate)
- **Status**: completed
- **Session**: session_stanley_20260621_194755_a1_diagram_build
- **Description**: Present the record; operator ratifies/edits each decision. On ratification → campaign `status: active`, open A1. **Operator accepted all 6 defaults 2026-06-21.**
- **Files**: this mission (→ completed + AAR), campaign doc (Decision Points → ratified), STATE.md
- **Depends on**: 2

## Campaign Context

### Previous Mission Outputs
- None — first mission of the campaign (predecessor campaign: Operation Keystone, completed 2026-06-20).

### Next Mission Inputs
- A1.1 (diagram build) needs: ratified quality-contract posture, profile-side confirmation, shape-enum policy,
  diagram-type scope for v1.

## Notes

All six decisions have plan defaults in the approved plan file. This mission only *records and ratifies* them; it
writes no producer code.

## Completion Summary

### Deliverables
- The A0.1 decision record (`missions/artifacts/a0_1_contract_profile_decision.md`) — 6 decisions, defaults + rationale, **ratified** (operator accepted all 6 defaults 2026-06-21).
- Confirmed: no dedicated `spec_diagram_*`/`spec_comic_*` in `what/specs/` → no Standard LIP required.

### Descoped
- None.

### Key Findings
- The two producers operate entirely within ratified specs + the `_reserved` namespace; profiles stay producer-side (zero Standard touch), so the build is decoupled from the LIP calendar gate (2026-06-27) and from PT P5.

### Scope Changes
- At activation, A1.2 folded into A1.1 (single diagram-build mission); campaign `mission_count` 9→8.

## AAR

- **Worked**: Front-loading the 6 governance decisions into a cheap, ratifiable record cleared the build path with zero ambiguity (the Keystone lesson applied).
- **Didn't**: n/a — decision phase, no execution surprises.
- **Finding**: All six questions had doctrine-aligned defaults; the operator accepted all, so no design divergence to absorb downstream.
- **Change**: none.
- **Follow-up**: A1.1 — build `diagram_generator` ([[how/campaigns/campaign_canvas_production/missions/mission_a1_1_diagram_build|mission]]).
