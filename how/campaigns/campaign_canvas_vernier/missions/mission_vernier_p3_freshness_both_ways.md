---
plan_id: mission_vernier_p3_freshness_both_ways
type: plan
title: "Freshness both ways — gate #9 gains the source-hash pre-filter, each blind spot printed on the line, and third parties get a checker"
owner: stanley
status: in_progress
campaign_id: campaign_canvas_vernier
campaign_phase: "P3"
campaign_mission_number: 2
mission_class: implementation
executor_tier: sonnet
token_budget_estimated: "~120k"
created: 2026-10-12
updated: 2026-10-16
last_edited_by: agent_mondrian
tags: [plan, campaign, vernier, freshness]
---

# Mission: Freshness both ways — gate #9 gains the source-hash pre-filter, each blind spot printed on the line, and third parties get a checker

**Campaign**: [[how/campaigns/campaign_canvas_vernier/campaign_canvas_vernier|campaign_canvas_vernier]]
**Phase**: P3 · **Mission**: 2 of 6 (chartered at the 2026-10-12 scope amendment)
**Depends on**: the signed verdicts at `how/gates/vernier_p1_exit_20261012` (P2) unless stated otherwise per objective.
**⛩ Opened 2026-10-16**: the P2b → P3 gate was approved by the operator. **Scope widened the same day** by two operator rulings and one residue, all landing in **one firewall touch, #8**:
- **Touch-#7 residue** (LIP-0011 §As implemented): `conformance.py` neither prints advisories in the CLI nor carries them in `ConformanceReport`, and its `json_schema()` docstring, CLI description and `schema` help, plus `canvas_std/README.md` (×4), still say v2.4.0.
- **Queue ③ RULED 2026-10-16** (`how/gates/operator_queue_20260916.output.json`, 5/5 approve): *partial*. Add fixture coverage for the two zero-coverage enums only, `edge.styleAttributes.arrow` (0/7) and `edge.fromEnd` (0/2), and leave the other values as published, named exposure.
- ⛔ **Touch #8 is not authorised yet.** As with #7, every file is named row by row and the operator signs before `canvas_std` moves (a door, rendered at objective 1's design).

## Goal

Implement the P0 ruling 'adopt both freshness mechanisms, each with its blind spot published'. Rebuild-and-compare (gate #9) catches generator drift (F-PL-6) and needs the generator; a source hash catches input drift, is cheap, and is third-party verifiable (Vernier P1). Neither subsumes the other. Ship both in the gate and a CLI so Terminal/City/LP can verify a canvas from outside its vault.

## Exit Gate

Gate line reads `dual-channel freshness N/N (source · rebuild)`; `canvas-std check-sync <canvas> [--source <path>]` exits 0/1 with the blind spot named in its output; Terminal's 8 pass from outside their tree; gate #9's two legs can disagree and the disagreement is reported, not averaged.

## Objectives

### 1. `check-sync` CLI in `canvas_std` (firewall touch — may ride #7 or be #8; name it)
### 2. Gate #9 second leg + the blind-spot label on every line
### 3. Prove the false-positive / false-negative pair by derivation: a prose typo → source stale, rebuild fresh; a layout-engine change → source fresh, rebuild stale (the F-PL-6 shape)
### 4. `how/gates/AGENTS.md` gate #9 row updated with both legs and what each cannot see
### 5. Touch #8's two riders (added 2026-10-16)
- `conformance.py`: advisories in the CLI output + `ConformanceReport.advisories` (additive field); the v2.4.0 docstrings + `canvas_std/README.md` → v2.5.0.
- Corpus: fixture(s) exercising every `edge.styleAttributes.arrow` and `edge.fromEnd` value. Re-read the coverage line, expected 12/40 → 21/40 (7 + 2), **measured, not predicted**. Gate pins re-derived by stash/restore.

## Campaign Context

- Review + triage this mission answers to: `artifacts/review_20261012_vault_state_and_inbox_triage.md`.
- Standing rules: phase gates are human gates · firewall touches named file-by-file before the signature · every figure re-derived before it is written · state the population on the face of the number.

## Notes

## Completion Summary

*Fill out when setting `status: completed`.*

## AAR

*Mandatory before `status: completed` — Worked / Didn't / Finding / Change / Follow-up.*
