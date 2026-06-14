---
plan_id: mission_e3_4_cutover
type: plan
title: "E3.4 — Cutover criteria + rollback rehearsal; retire embedded v1.0.0 framing"
owner: stanley
status: active
campaign_id: campaign_canvas_genesis
campaign_phase: 3
campaign_mission_number: 4
mission_class: closeout
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, e3, cutover, rollback, supersede, canvasforge]
---

# Mission: E3.4 — Cutover criteria + rollback rehearsal; retire v1.0.0 framing

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]]
**Phase**: 3 — CanvasForge migration (parity-gated) ⚠️ highest risk
**Mission**: 4 of 4

## Goal

Close the CanvasForge migration: document and meet the **cutover criteria**, **rehearse the rollback**, and — on a
green gate + operator approval — **retire the embedded Canvas Standard v1.0.0 framing** in CanvasForge (supersede it
in favor of consuming v2.0.0 from Canvas.aDNA). This converts the reversible E3.2/E3.3 work into a committed, single-
source state while keeping the shim as the safety net through its grace window.

## Exit Gate

- **Cutover criteria documented and met**: E3.3 parity GREEN + conformance suite green + `iii/` review ≥ baseline +
  **operator gate** (cutover is operator-approved; it is consequential).
- **Rollback rehearsed**: demonstrate that reverting the wrapper repoint restores the pre-migration path with no
  consumer breakage (the shim keeps the old import path working).
- **Embedded v1.0.0 framing superseded**: `CanvasForge.aDNA/what/context/advanced_canvas/` (Standard v1.0.0 +
  roundtrip) carries a supersession banner pointing to Canvas.aDNA v2.0.0; CanvasForge consumes the standard via
  `canvas/` + the shim, not its embedded copy.
- **Shim-retirement scheduled** (window + retire-condition + owner) in the `Home.aDNA` shim ledger (Standing Rule 9)
  and noted for E6.2.

## Objectives

### 1. Document cutover criteria
- **Status**: planned
- **Description**: Write the cutover checklist (parity GREEN + conformance green + iii ≥ baseline + operator gate)
  per the campaign Cutover & Rollback section.
- **Files**: cutover criteria artifact (mission artifacts)
- **Depends on**: E3.3 GREEN

### 2. Rehearse rollback
- **Status**: planned
- **Description**: Rehearse `revert the wrapper repoint`; confirm the shim keeps the old path working and no
  consumer (SS presentationforge / graphicnovelforge, CC presentationforge) breaks. Record the rehearsal.
- **Files**: rollback rehearsal note
- **Depends on**: 1

### 3. Retire embedded v1.0.0 framing (supersede) — operator-gated
- **Status**: planned
- **Description**: On green + operator approval, add a supersession banner to CanvasForge's embedded Standard
  v1.0.0 context; point consumption at v2.0.0 via the `canvas/` wrapper. Archive-never-delete the v1.0.0 framing.
- **Files**: `CanvasForge.aDNA/what/context/advanced_canvas/*` (banner), wrapper notes
- **Depends on**: 1, 2

### 4. Schedule shim retirement
- **Status**: planned
- **Description**: Register the `canvas_core` shim retirement (window from E-D2, retire-condition = ref-sweep-zero +
  operator-ack, owner) in the `Home.aDNA` shim ledger; flag for E6.2 final cutover.
- **Files**: shim ledger entry (Home.aDNA)
- **Depends on**: 3

## Campaign Context

### Previous Mission Outputs
- E3.3 produced the parity verdict (GREEN required to proceed). E3.2 left both import paths live via the shim.

### Next Mission Inputs
- E4 (LF-successor + net-new consumer) builds on a migrated, single-source CanvasForge. E6.2 executes the final
  cutover + shim-retirement scheduled here.

## Notes

- **Cutover is the one-way step** of E3 — hence the operator gate. Everything before it (E3.1/E3.2/E3.3) is
  reversible via the shim. Do not cut over on a RED or AMBER parity result.
- Supersession follows **archive-never-delete** (SO-6): the v1.0.0 framing is banner-superseded, not removed.

## Completion Summary

*Fill out when setting `status: completed`.*

### Deliverables
- [ ] Cutover criteria documented + met
- [ ] Rollback rehearsed (no consumer breakage)
- [ ] v1.0.0 framing superseded (operator-gated)
- [ ] Shim retirement scheduled (Home.aDNA ledger)

### Descoped
- Final cross-system cutover (E6.2) + campaign AAR (E6.3).

### Key Findings
-

### Scope Changes
-

## AAR

*Mandatory before setting `status: completed`. See `how/templates/template_aar_lightweight.md`.*

- **Worked**:
- **Didn't**:
- **Finding**:
- **Change**:
- **Follow-up**:
