---
plan_id: mission_e6_2_cutover_shim_schedule
type: plan
title: "E6.2 — Final cutover confirmation + rollback rehearsal + shim-retirement schedule"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 6
campaign_mission_number: 2
mission_class: cutover
created: 2026-06-20
updated: 2026-06-20
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, e6, cutover, rollback, shim, retirement]
---

> **STATUS: completed 2026-06-20** (session `session_stanley_20260620_170330_keystone_e6_validation_cutover`).
> Artifact: `missions/artifacts/e6_2_cutover_confirmation.md`. Memo: `who/coordination/coord_2026_06_20_mondrian_to_hestia_shim_retirement_schedule.md`.

# Mission: E6.2 — Final cutover confirmation + shim-retirement schedule

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]]
**Phase**: 6 — Validation & cutover · **Mission**: E6.2

## Goal

Confirm the cutover at campaign level (the E3.4 floor cutover already happened), re-confirm the rollback path is
intact, and **schedule** (not execute) the `canvas_core→canvas_std` deprecation-shim retirement.

## Exit Gate
- Cutover criteria checklist all-green at the Standard/floor level (`e6_2_cutover_confirmation.md`).
- Rollback runbook re-confirmed intact (core.py frozen at `1a51801`; baseline `3ce4d341` unchanged).
- Shim retirement scheduled (2027-06-13, SR-9 retire-condition) via memo to Hestia (Home.aDNA owns the ledger).

## Objectives

### 1. Confirm cutover criteria
- **Status**: completed · **Result**: criteria 1/3/4/5/6 ✅; criterion 2 ✅ at the **floor** level (`canvas_core`
  736/3 + `canvas_comic` 99/+11 = 835/3 green; shim DeprecationWarning expected; no Standard API breakage).
  **Criterion 2b — federation-integration tests deferred → PT P5** (see objective 3). · **Files**:
  `artifacts/e6_2_cutover_confirmation.md`

### 2. Rollback rehearsal (re-confirm net-zero)
- **Status**: completed · **Result**: `e3_4_rollback_rehearsal.md` runbook still valid — `core.py` frozen at
  `1a51801` (shim markers = 2, clean; the 4 commits since are banners/coordination/archive); revert target exists;
  baseline `3ce4d341` intact. Not re-executed on the archived tree (preconditions intact = runbook valid; net-zero
  already proven at E3.4).

### 3. Shim-retirement schedule + the federation finding
- **Status**: completed · **Description**: scheduled retirement 2027-06-13 (E-D2), SR-9 retire-condition, coupled to
  PT-P5 relocation; memo to Hestia for §C. **Discovered + characterized:** the CanvasForge `test_federation_validation.py`
  suite is 25f/30e — **all** `FileNotFoundError` on consumer-wrapper lattices (SS/CC) under a wrong `Archive.aDNA/`
  prefix from the pt09 relocation. **PT-P5 refederation territory** (the ~8 consumer wrappers), not a floor/Standard
  regression. The shim ref-sweep is naturally downstream of PT P5. · **Files**:
  `who/coordination/coord_2026_06_20_mondrian_to_hestia_shim_retirement_schedule.md`

## Notes
- **Honest criterion 2:** the E3.4 record's "900/3" is stale post-pt09 — recorded accurately as 835/3 floor-green +
  55 federation-integration reds (relocation path breaks → PT P5). Not green-washed.
- **Reversibility preserved:** cutover supersedes by banner (SO-6); the shim stays live to 2027-06-13; rollback is
  never time-pressured during the window.

## Completion Summary

Completed 2026-06-20. Cutover confirmed at the Standard/floor level; rollback intact; shim retirement scheduled
(PT-P5-coupled). The federation-integration breakage is recorded and handed to PT P5 (E5.2), not treated as a
cutover blocker.

## AAR
- **Worked**: Reusing the E3.4 cutover-criteria + rollback artifacts gave a ready checklist; verifying rollback
  *preconditions* (HEAD/markers/baseline) re-confirmed the runbook without disturbing the archived tree.
- **Didn't**: Did not re-run the literal "900/3" green — pt09 relocation invalidated it; did not fix the federation
  tests (PT-P5 refederation scope) or remove the shim (scheduled, not executed).
- **Finding**: The federation-validation reds are the concrete face of "E5.2 is PT-P5-coupled" — the pt09 archive
  broke sibling-vault path resolution for the consumer wrappers PT P5 will repoint.
- **Change**: The shim retire-condition now explicitly notes its **PT-P5 ref-sweep dependency** (the consumer
  wrappers are live floor importers until repointed).
- **Follow-up**: Hestia §C ack; PT P5 repoints the ~8 consumer wrappers (federation tests go green) + relocates
  `canvas_core` → re-baseline parity + evaluate shim ref-sweep.
