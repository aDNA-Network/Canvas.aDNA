---
plan_id: mission_p0_charter
type: plan
title: "P0 — Charter + 8-decision record + ADR-007 draft"
owner: stanley
status: completed
campaign_id: campaign_canvas_armature
campaign_phase: 0
campaign_mission_number: 1
mission_class: reconnaissance
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, armature, leg3, runtime, firewall, decision, p0]
---

# Mission: P0 — Charter + 8-decision record + ADR-007 draft

**Campaign**: [[how/campaigns/campaign_canvas_armature/campaign_canvas_armature|campaign_canvas_armature]]
**Phase**: 0 — Charter + decision record + ADR-007 draft
**Mission**: 1 of 4

## Goal

Open Operation Armature on a fixed footing — **before any build** — by (1) chartering the campaign (graduating the Salon
follow-on stub), (2) recording the eight governance/scope decisions that gate the leg-3 runtime as a single ratifiable
record, and (3) drafting **ADR-007** — the ratifiable decision to make the *first-ever* `canvas_std` firewall touch
(wire `I-*` into the harness + cut `interaction_version 1.0` into a Standard version), isolated to a gated P2. This
front-loads the campaign's two real risks — an unbounded `canvas_std` regression, and a governed write that drifts into
a *silent* source mutation — into a cheap, ratifiable decision phase (the Keystone/Salon lesson: governance touches
discovered mid-build cost the most). **No spec is changed and no code is written this mission.**

## Exit Gate

A campaign charter, the firewall-touch ADR (`adr_007`, `status: proposed`), and an 8-decision record exist — each
decision with a default + rationale + the alternative considered; the foundation facts (leg-3 spec ratified + POC
demonstrated; `I-*` realized only in the consumer; `interaction_version 1.0` uncut; `adr_007` the next free number; no
slug collision) are confirmed. **The operator ratifies the decision record + `adr_007` at the P0→P1 gate — that
ratification activates the campaign (`status: active`) and authorizes Phase P1 (the governed write runtime).**

## Objectives

### 1. Confirm the foundation
- **Status**: completed
- **Session**: session_stanley_20260622_193153_armature_scaffold_p0
- **Description**: Verify leg-3 spec ratified ([[../../../what/specs/spec_interface_surface|spec_interface_surface.md]])
  + POC demonstrated (`interaction.py` v0.2.0, `canvas_context` 50 passed); the `I-1/I-2/I-3/I-D` family realized in the
  *consumer* (`validate_interaction_block`), forward-pointed into the `canvas_std` harness (spec_conformance_suite §4.1);
  `interaction_version 1.0` rides `_reserved.interaction` additively but is uncut as a Standard version; the existing
  `canvas_std.roundtrip` already ships `diff`/`merge`/`preserve_positions`/`compute_sync_hash`/`from_canvas`/`to_canvas`
  for the governed write to reuse; `spec_roundtrip_protocol_v2 §1.2` mandates the reverse path is **advisory-only**.
  Confirm `adr_007` is the next free ADR number and `campaign_canvas_armature` does not collide.
- **Files**: `what/specs/`, `what/decisions/`, `what/code/`, `how/campaigns/` (read-only)
- **Depends on**: none

### 2. Scaffold + author charter, decision record, ADR-007
- **Status**: completed
- **Session**: session_stanley_20260622_193153_armature_scaffold_p0
- **Description**: Create the campaign dir (`campaign_canvas_armature.md` master doc + `CLAUDE.md` + `missions/` +
  `missions/artifacts/`); author `what/decisions/adr_007_leg3_firewall_touch.md` (`status: proposed`) — the leg-3
  firewall-touch decision (the inverse of Salon's firewall-preserving D6), bounded by `adr_006`; author the 8-decision
  record (D1–D8, defaults + rationale + alternatives; D1 + D3 carry the operator's planning-session choice). Index
  `adr_007` in `what/decisions/AGENTS.md`; update `STATE.md`.
- **Files**: campaign scaffold, `what/decisions/adr_007_leg3_firewall_touch.md`,
  `missions/artifacts/p0_decision_record.md`, `what/decisions/AGENTS.md`, `STATE.md`
- **Depends on**: 1

### 3. Operator ratification (P0→P1 gate)
- **Status**: completed
- **Session**: session_stanley_20260622_193153_armature_scaffold_p0 (continued)
- **Description**: Present the decision record + `adr_007`. On accept/edit of each: set both records `status: ratified`,
  update the campaign Decision Points, complete this mission (+AAR), set the campaign `status: active`, graduate the
  backlog idea (`idea_campaign_leg3_interface_runtime` → note in-progress), and open Phase P1 (author the P1 mission —
  the governed write runtime + pilot).
- **Files**: this mission (→ completed + AAR), campaign doc (Decision Points → ratified), `p0_decision_record.md`
  (→ ratified), `adr_007` (→ ratified), `idea_campaign_leg3_interface_runtime.md`, STATE.md
- **Depends on**: 2

## Campaign Context

### Previous Mission Outputs
- None — first mission of the campaign. Predecessor: Operation Salon (completed 2026-06-22), whose Completion Summary
  §Descoped named exactly this campaign's three deliverables (governed write · `I-*` into the harness · the version cut).

### Next Mission Inputs
- P1 (governed write runtime) needs: ratified governed-write semantics (D4) + runtime home (D5) + the firewall posture
  (D3/`adr_007`, so P1 knows it stays firewall-clean).
- P2 (firewall touch) needs: ratified `adr_007` (D3) + Standard-version coordination (D6).

## Notes

All eight decisions have defaults in the approved plan (`~/.claude/plans/please-read-the-claude-md-glimmering-teapot.md`).
This mission only *records* them and *drafts* `adr_007`; it authors no spec and writes no code. The single biggest call
is **D3** (firewall posture) — already chosen by the operator at the planning gate to **lift** `canvas_std` in a gated
P2 (the inverse of Salon's D6, which preserved it). `adr_007` is the citable instrument of that lift; it bounds the touch
to one phase + one purpose and replaces the P2 git-diff-0 check with full regression. **Do not touch `canvas_std` this
mission** (or in P1) — the lift takes effect only at P2 under the ratified ADR.

## Completion Summary

Completed 2026-06-22 at the P0→P1 gate (`session_stanley_20260622_193153_armature_scaffold_p0`, continued). The operator
asked for the agent's recommendation on each decision, then ratified the 8-decision record + `adr_007` — **all eight at
the agent's recommended values** (D5 = extend `canvas_context`; D6 = cut `interaction_version 1.0` into v2.2.0 by
maintainer discretion, reserving v2.1.0 for LIP-0008; no fresh leg-3 LIP). Operation Armature is now `active` at P1.

### Deliverables
- Campaign scaffold (master doc `campaign_canvas_armature.md` + per-campaign `CLAUDE.md` + this P0 mission) — **ratified**.
- `what/decisions/adr_007_leg3_firewall_touch.md` (the leg-3 firewall-touch ADR — the inverse of Salon's D6) —
  **ratified** (`accepted`, signed_by stanley; binding instrument for the P2 lift).
- `missions/artifacts/p0_decision_record.md` (D1–D8, defaults/choices + rationale + alternatives) — **ratified**.
- 3/3 objectives complete (foundation confirmed · scaffold/draft · operator ratification).

### Descoped
- None. P0 closed on its charter.

### Key Findings
- Front-loading the firewall posture (D3) into a ratifiable ADR (`adr_007`) — *before* any `canvas_std` touch — gives
  the P2 phase a citable lift instrument with an explicit replacement gate (full regression for git-diff-0). The
  inverse-of-Salon-D6 framing made the single biggest call legible and bounded rather than an in-flight surprise.

### Scope Changes
- None.

## AAR

- **Worked**: All 8 decisions carried defaults/choices, so the gate cleared in one pass at the agent's recs (incl. the load-bearing D3 → lift the firewall, bounded by `adr_007`).
- **Didn't**: Nothing material; the operator asked for recommendations first, then ratified at them — a clean human gate with no edits.
- **Finding**: Recording the firewall *lift* as its own ADR (the mirror of Salon's firewall-*preserve* D6) keeps the two-shelf-firewall doctrine coherent — the firewall is never touched on assumption, only under a ratified, phase-bounded instrument.
- **Change**: None — the planning-phase pattern (charter + decisions + a ratifiable ADR for the load-bearing call, HOLD at gate) ported cleanly from Salon to a build campaign.
- **Follow-up**: P1 mission `mission_p1_write_runtime.md` — author + build the governed advisory-reverse write runtime + pilot (this session); HOLD at P1→P2.
