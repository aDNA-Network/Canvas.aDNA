---
plan_id: mission_vernier_p2b_lip_0011_sync_semantics
type: plan
title: "LIP-0011 — sync semantics: define what sync_hash hashes, register a full-digest key, and cut Standard v2.5.0 additively"
owner: stanley
status: planned
campaign_id: campaign_canvas_vernier
campaign_phase: "P2b"
campaign_mission_number: 1
mission_class: implementation
executor_tier: opus
token_budget_estimated: "~250k"
created: 2026-10-12
updated: 2026-10-15
last_edited_by: agent_mondrian
tags: [plan, campaign, vernier, lip_0011]
---

# Mission: LIP-0011 — sync semantics: define what sync_hash hashes, register a full-digest key, and cut Standard v2.5.0 additively

**Campaign**: [[how/campaigns/campaign_canvas_vernier/campaign_canvas_vernier|campaign_canvas_vernier]]
**Phase**: P2b · **Mission**: 1 of 6 (chartered at the 2026-10-12 scope amendment)
**Depends on**: the signed verdicts at `how/gates/vernier_p1_exit_20261012` (P2) unless stated otherwise per objective.
**⛩ Unblocked 2026-10-15:** P2 ruled 9/9 as recommended (V-1 (b) · V-2 at `extended` · V-3 `sync.generator`); record `how/gates/vernier_p1_exit_20261012.output.json`. The V-2 census is committed as `how/gates/axis_tier_census.py` (obj 4's re-home, done early).

## Goal

Turn the V-1/V-2/V-3 verdicts into the Standard. Three implementations currently pass A-6 with three semantics (topology · source-document bytes · master-file bytes). The LIP defines the field, adds the standard full-digest key (per the V-1 verdict, expected `sync.source_sha256`, 64 hex) and the provenance carrier (per V-3, expected `sync.generator`), rules the A-8 tier (V-2), and ships as v2.5.0 with every existing passer still passing — a claim that is MEASURED on the fleet corpus (F-GL-6), not asserted.

## Exit Gate

LIP-0011 Final in `who/governance/lips/`; `canvas_std` green at new pins; certification corpus gains one Terminal canvas, one City twin, one Canvas native as cases; fleet census (`~/aDNA/*/what/lattices/examples/*.canvas` + the five known external carriers) shows 0 new failures; firewall touch #7 back to diff 0 on commit; §7.7 signature on the LIP; registry + §7.2 + schema `$defs.reserved.sync` + `RESERVED_KEYS` all updated in the same touch (F-GL-1: one definition, consumed).

## Objectives

### 1. Draft LIP-0011 from the door's `.output.json`
- **Status**: planned · **Files**: `who/governance/lips/lip_0011_sync_semantics.md`, `lip_registry.md`
- Options as ruled; migration table per implementer (Terminal 8 · City 1 · LP gen-canvas · Home 1 · Canvas 26); backward-compat claim written as a *command that is run*, not a sentence.

### 2. Firewall touch #7 (named before signature)
- **Files**: `canvas_std/reserved.py` (A-6 semantic check: `source_sha256` 64-hex when present; `sync_hash` == topology recomputation when `production: generated` and the verdict says so; `sync.generator` string), `roundtrip.py` (helper `compute_source_sha256(path)`), `schema/adna_canvas_v2.schema.json` (`$defs.reserved.sync`), `spec_adna_canvas_standard.md` §7.2/§8.1, `__init__.py` version 2.5.0.
- Depends on: 1 + the signature.

### 3. Fixtures + certification
- One Terminal canvas (copied, attribution kept), one City twin, one Canvas native; `test_schema_conformance.py` coverage report re-read (12/40 residue unchanged unless widened here).

### 4. Fleet backward-compat census — run, paste, do not predict
- Script in `how/gates/` or `what/code/canvas_std/tools/`; output pasted into the LIP with glob + date + HEADs.

### 5. Version sweep classified, not globbed
- `2.4.0` literals split into live pins vs dated historical claims (Gridline (E) precedent); peer rows in `federation_index` §2 **not touched**.

## Campaign Context

- Review + triage this mission answers to: `artifacts/review_20261012_vault_state_and_inbox_triage.md`.
- Standing rules: phase gates are human gates · firewall touches named file-by-file before the signature · every figure re-derived before it is written · state the population on the face of the number.

## Notes

## Completion Summary

*Fill out when setting `status: completed`.*

## AAR

*Mandatory before `status: completed` — Worked / Didn't / Finding / Change / Follow-up.*
