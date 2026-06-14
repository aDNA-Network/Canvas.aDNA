---
plan_id: mission_e3_3_parity_gate
type: plan
title: "E3.3 — Parity/regression gate vs locked baselines (Wilhelm 8.80 / Issue 01 8.43)"
owner: stanley
status: completed
status_note: "completed 2026-06-13 — GREEN (deterministic structural proof; shim output-neutral; baseline 3ce4d341 unchanged)"
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
- **Status**: ✅ done
- **Description**: Using the shim, regenerate the locked reference set (Wilhelm deck, Issue 01 comic) so the
  canvas-layer logic runs from `canvas_std`. Capture outputs at NEW timestamps (never overwrite the baseline).
- **Files**: regenerated outputs under CanvasForge test/fixtures output dirs (new timestamps)
- **Depends on**: E3.2 (shim in place)

### 2. Diff vs locked baselines + VR scoring
- **Status**: ✅ done
- **Description**: Diff regenerated outputs vs `baseline_vr_scores.json` (SHA `3ce4d341…`); run VR1–VR5 via the
  `iii/` contract; confirm scores ≥ baseline (Wilhelm 8.80 / Issue 01 8.43) and structural diffs are null or
  explained.
- **Files**: parity report (mission artifact)
- **Depends on**: 1

### 3. Record the parity verdict
- **Status**: ✅ done
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

**Completed 2026-06-13 — verdict GREEN** (session `session_stanley_20260613_215108_keystone_e3_3_parity`).
Operator method = **Approach A (deterministic structural proof)**; no Gemini re-score. The E3.2 constants-only shim
is proven **output-neutral**; baseline `3ce4d341…` untouched. HELD at E3.3→E3.4 (cutover is a separate operator gate).

### Deliverables
- [x] Reference output regenerated **through `canvas_std`** — Wilhelm deck rebuilt via the shimmed generation path (`build_wilhelm().build()`, 56 nodes/20 edges); comic exercised on its committed canvas (build does Gemini image-gen, not invoked).
- [x] Parity report (`missions/artifacts/e3_3_parity_report.md`) — static proof + object-identity + determinism + **A/B normalized-SHA identical shim-ON vs shim-OFF** (`aa675665…`) + 0 federated-floor rejects + baseline-SHA witness.
- [x] **GREEN verdict** recorded (`missions/artifacts/e3_3_parity_verdict.md`); reproducible via `missions/artifacts/e3_3_parity_check.py`.

### Descoped
- Cutover + v1.0.0 supersession (E3.4 — operator gate).
- Round-trip-function repoint (was descoped from E3.2; needs its own parity pass later).
- The Gemini median-of-3 LLM re-score (operator chose deterministic Approach A; would add noise + baseline-write risk for a provably output-neutral change).

### Key Findings
- For a constants-only repoint with verified object-identity, **parity is a structural-equivalence question, settleable deterministically** — a stronger and cheaper proof than a non-deterministic LLM re-score. The A/B (build shim-ON vs shim-OFF, normalized modulo random `secrets.token_hex` IDs → identical SHA) isolates the shim's effect to exactly nil.
- Canvas generation is deterministic *modulo random IDs* (`CanvasBuilder.generate_id()` = `secrets.token_hex(8)`); two same-state rebuilds match after ID-normalization, so the A/B is meaningful.
- The federated floor accepts both reference artifacts with 0 rejects.

### Scope Changes
- None to intent. Comic was exercised via validation/fingerprint on its committed canvas rather than a full rebuild (its build invokes Gemini image-gen — out of bounds for an API-free deterministic gate).

## AAR

- **Worked**: Approach A — static proof (logic-free diff) + object-identity + an A/B normalized-canvas-SHA comparison (shim-ON == shim-OFF) deterministically proving the shim is output-neutral. Free, fast, reproducible; zero baseline-write risk.
- **Didn't**: A full like-for-like comic *rebuild* wasn't possible API-free (its build does Gemini image-gen); handled by exercising the federated floor on the committed comic canvas instead.
- **Finding**: Baseline scores (8.80/8.43) come from a non-deterministic Gemini path; re-scoring would measure model noise, not the change. Structural identity makes "VR ≥ baseline" true by construction — the honest, rigorous framing.
- **Change**: Kept `e3_3_parity_check.py` (ID-normalizer + federated-floor fingerprint) as a reusable mission artifact — the same harness can gate the round-trip-function repoint and E4/E5 producer migrations.
- **Follow-up**: E3.4 cutover (operator gate) — retire the embedded v1.0.0 framing + rollback rehearsal; then the descoped round-trip-function repoint can run its own parity pass with this harness.
