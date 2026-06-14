---
plan_id: mission_e3_3_parity_gate
type: plan
title: "E3.3 — Parity/regression gate vs locked baselines (Wilhelm 8.80 / Issue 01 8.43)"
owner: stanley
status: active
campaign_id: campaign_canvas_genesis
campaign_phase: 3
campaign_mission_number: 3
mission_class: verification
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, e3, parity, regression, gate, canvasforge]
---

# Mission: E3.3 — Parity/regression gate

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]]
**Phase**: 3 — CanvasForge migration (parity-gated) ⚠️ highest risk
**Mission**: 3 of 4

## Goal

Prove that routing CanvasForge's canvas generation through `canvas_std` (via the E3.2 shim) produces **no output
regression** against the locked baselines — **Wilhelm 8.80** (presentation deck) and **Issue 01 8.43** (comic) —
with visual quality (VR1–VR5, via the `iii/` contract) **not dropping below baseline**. This is the **load-bearing
gate of E3**: cutover (E3.4) happens *only* on a green result here; a red result rolls back via the shim.

## Exit Gate

- CanvasForge's locked reference outputs, **regenerated through `canvas_std`**, diff-clean (or
  explained-and-accepted) vs the pre-migration baselines (Wilhelm 8.80 / Issue 01 8.43).
- VR1–VR5 scores via the `iii/` review contract are **≥ baseline** for the reference set.
- The locked VR baseline SHA **`3ce4d341…` is UNCHANGED** (baselines are never overwritten — CanvasForge Critical
  Rule 2); new outputs tracked at new timestamps.
- A **parity verdict (GREEN / RED)** is recorded in mission artifacts. RED ⇒ do not proceed to E3.4; roll back via
  the shim and remediate.

## Objectives

### 1. Regenerate reference outputs through canvas_std
- **Status**: planned
- **Description**: Using the shim, regenerate the locked reference set (Wilhelm deck, Issue 01 comic) so the
  canvas-layer logic runs from `canvas_std`. Capture outputs at NEW timestamps (never overwrite the baseline).
- **Files**: regenerated outputs under CanvasForge test/fixtures output dirs (new timestamps)
- **Depends on**: E3.2 (shim in place)

### 2. Diff vs locked baselines + VR scoring
- **Status**: planned
- **Description**: Diff regenerated outputs vs `baseline_vr_scores.json` (SHA `3ce4d341…`); run VR1–VR5 via the
  `iii/` contract; confirm scores ≥ baseline (Wilhelm 8.80 / Issue 01 8.43) and structural diffs are null or
  explained.
- **Files**: parity report (mission artifact)
- **Depends on**: 1

### 3. Record the parity verdict
- **Status**: planned
- **Description**: Write the GREEN/RED verdict + evidence to mission artifacts and the campaign doc. GREEN unblocks
  E3.4; RED triggers shim rollback + remediation loop (back to E3.2).
- **Files**: parity verdict artifact; campaign doc update
- **Depends on**: 2

## Campaign Context

### Previous Mission Outputs
- E3.2 installed the `canvas_core` → `canvas_std` deprecation shim (both paths live), enabling regeneration through
  the federated reference logic.

### Next Mission Inputs
- E3.4 cutover is **gated on this mission's GREEN verdict**; the parity evidence is a cutover criterion.

## Notes

- Parity baselines: **Wilhelm 8.80** / **Issue 01 8.43**; VR criteria weights VR1 .25 / VR2 .25 / VR3 .20 /
  VR4 .15 / VR5 .15; pass threshold per cell ≥ 7.5 (CanvasForge `visual_review.py` + `baseline_vr_scores.json`).
- The `iii/` review here is **stage 4** (output quality), distinct from format conformance (stage 3,
  `spec_conformance_suite`). Confirm the III pin at use (Canvas `iii/` pins v0.4.0; CanvasForge `iii/` pins v0.5.0 —
  the formal reconcile is **E5.1**; for E3.3 use CanvasForge's own `iii/` review path against its baseline).

## Completion Summary

*Fill out when setting `status: completed`.*

### Deliverables
- [ ] Regenerated reference outputs (new timestamps)
- [ ] Parity report (diff + VR ≥ baseline)
- [ ] GREEN/RED parity verdict recorded

### Descoped
- Cutover + v1.0.0 supersession (E3.4).

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
