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
updated: 2026-10-26
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

Gate line reads `dual-channel freshness N/N (source · rebuild)`; `canvas-std check-sync <canvas> [--source <path>]` exits 0/1 with the blind spot named in its output; ~~Terminal's 8 pass from outside their tree;~~ gate #9's two legs can disagree and the disagreement is reported, not averaged.

> ⛩ **Amended 2026-10-26 (his morning word, RULED row 11112; struck, not deleted).** *"Terminal's 8 pass from outside their tree"* **moved to P4's Exit Gate**: none of Terminal's 8 carries `sync.source_sha256`, so the clause waits on their one regeneration after P4, not on anything P3 builds. Record: `../campaign_canvas_vernier.md` §P3 exit-gate amendment — 2026-10-26.

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

- **2026-10-26 (Mondrian, unattended, Automator N2-19): objective 1 DESIGNED, proposed.** [`p3_obj1_touch_8_design_20261026.md`](../artifacts/p3_obj1_touch_8_design_20261026.md) has the `check-sync` contract (topology · source legs, each printing its blind spot; exit 2 when no leg ran), touch #8 in nine rows, and three door decision points (D-1 home · D-2 topology advisory · D-3 no LIP). ~~⛩ **Exit-gate dependency found:** "Terminal's 8 pass from outside their tree" can be met in P3 only if D-2 makes the topology leg advisory.~~ *(Struck 2026-10-26 01:4x, not deleted: a reviewer seat showed it false; see the next note.)* Terminal measured 0/8 topology at P1 and migrates once, after P4. Objective 2 (the gate #9 source leg) needs no signature and can run before the door. Nothing in `canvas_std` moved, and the door is not rendered yet.
- **2026-10-26 (Mondrian, unattended, Automator N2-J): objective 2 CARDED `proposed`; the reviewer seat read it UNSOUND, so it stops at the card.**
  - The card is [`p3_obj2_gate9_source_leg_card_20261026.md`](../artifacts/p3_obj2_gate9_source_leg_card_20261026.md). The text the seat read is `f4c6b32`; the revision applying its findings comes after.
  - **F-V-16:** the drafted source leg had a population of 0 here. Neither pair's canvas carried a digest, and the producer could not write one.
  - **The seat's blocking finding:** neither leg reads the prose `.md`, and the card never said so. In this vault "source" first meant the prose, so the line would have read as prose coverage. The seat called the fix text-only. It is applied, and **not yet re-reviewed**. Eight non-blocking findings are applied or routed as well. The card now records that the verdict follows the rebuild, the authority, as D-O2-7.
  - **The corrected exit-gate dependency (the seat's #6).** None of Terminal's 8 carries `sync.source_sha256`: their source digest lives in `sync_hash`, 16 hex. So `check-sync`'s source leg cannot run on any of them, under either D-2 ruling. *"Terminal's 8 pass from outside their tree"* therefore waits on Terminal's one regeneration after P4, not on D-2. That makes it a dated amendment for him at the touch-8 door. The obj 1 design carries this and three more findings in a dated §6.
  - Nothing was built. `canvas_std` diff 0. The gate line at HEAD `be15ce4` was measured three times, all green; that is a measurement, not a claim on any objective or gate.
  - **Next:** a fresh seat over the revised card, then the build in one commit (rows 1-5), then objective 3's true layout-engine derivation, then objective 4.
- **2026-10-26 (Mondrian, M3 under N2-J, on his morning word): objective 2 BUILT.** A fresh read-only seat that did not build read the card SOUND at `f817de9` (0 blocking, 6 non-blocking, applied as text; card §9). His D-O2-7 is the verdict rule; D-O2-8 (the recompute cross-checked against the rebuild's own stamp) was taken from the seat's offer. Rows 1-5 landed in one commit: the producer stamps `sync.source_sha256` from its CLI through `canvas_std`'s one function; gate #9 runs both legs on every pair and prints each with its blind spot and *"prose channel: neither leg reads it"*; `--probe-freshness` 11 of 11 with a control that must mismatch; both vault canvases regenerated (one key each, parsed). Gate line after the build: dual-channel freshness **2/2** (yaml source 2/2 · rebuild 2/2; prose unread), ALL GATES GREEN, pasted in the session record and STATE. **No objective is closed and no gate is claimed here**: objective 4 (the `how/gates/AGENTS.md` row) and objective 3 follow, and the P3 gate is his. `canvas_std` diff 0.
  - *Same sitting, after the build:* objective 4's row written in `how/gates/AGENTS.md` (§gate #9, "Two legs since 2026-10-26": both legs, what each cannot see, the prose line, D-O2-7/8, F-V-16, the probe) and the usage block gains `--probe-freshness`. Objective 3 (the true layout-engine derivation, plus the prose case named as the third blind spot) is the next card.

## Completion Summary

*Fill out when setting `status: completed`.*

## AAR

*Mandatory before `status: completed` — Worked / Didn't / Finding / Change / Follow-up.*
