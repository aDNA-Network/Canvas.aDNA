---
plan_id: mission_vernier_p7_post_generator_social_formats
type: plan
title: "post_generator for Socials — social formats, style_ref by reference, the binding quality contract, and the RLHF read path"
owner: stanley
status: planned
campaign_id: campaign_canvas_vernier
campaign_phase: "P7"
campaign_mission_number: 6
mission_class: implementation
executor_tier: opus
token_budget_estimated: "~160k"
created: 2026-10-12
updated: 2026-10-12
last_edited_by: agent_mondrian
tags: [plan, campaign, vernier, socials]
---

# Mission: post_generator for Socials — social formats, style_ref by reference, the binding quality contract, and the RLHF read path

**Campaign**: [[how/campaigns/campaign_canvas_vernier/campaign_canvas_vernier|campaign_canvas_vernier]]
**Phase**: P7 · **Mission**: 6 of 6 (chartered at the 2026-10-12 scope amendment)
**Depends on**: the signed verdicts at `how/gates/vernier_p1_exit_20261012` (P2) unless stated otherwise per objective.

## Goal

Answer Stentor's two memos with code, not a 'not yet'. Today `post_generator` carries advisory char budgets + aspect hints only. Ship: platform pixel envelopes consumed from Socials' encode table; carousel / quote-card / thumbnail formats; a `style_ref` field {taste_ref, kept_refs, constraints{must,prefer,avoid,never}} on `Post`/`PostPanel` passed by reference (never inlined brand assets); `iii_quality_contract.md` versioned and declared the binding consumer contract; a documented read-only path to Canvas-side RLHF capture rows under Socials' own namespace (III store access stays Argus's).

## Exit Gate

`post_generator` tests green at new pins (manifest updated by derivation); a fixture request from Socials' wrapper renders a carousel + a quote card at platform pixel size; `style_ref` round-trips; `iii_quality_contract.md` carries a version + a change rule; Socials' wrapper reads `counterparty_confirmed: true` (their edit, on our memo); SG-4 unblocked by their own statement.

## Objectives

### 1. Contract first — `iii_quality_contract.md` versioned; request schema agreed against Socials' `wrapper_canvas.md`
### 2. `style_ref` on the model (by reference; validation that nothing inlines)
### 3. Formats — carousel · quote card · thumbnail; pixel envelopes from the encode table (producer-side, never in `canvas_std.schema`)
### 4. RLHF read path — document + a read-only helper over Canvas-side sidecars; §6b semantics kept
### 5. Memo to Stentor with the fixture outputs attached

## Campaign Context

- Review + triage this mission answers to: `artifacts/review_20261012_vault_state_and_inbox_triage.md`.
- Standing rules: phase gates are human gates · firewall touches named file-by-file before the signature · every figure re-derived before it is written · state the population on the face of the number.

## Notes

## Completion Summary

*Fill out when setting `status: completed`.*

## AAR

*Mandatory before `status: completed` — Worked / Didn't / Finding / Change / Follow-up.*
