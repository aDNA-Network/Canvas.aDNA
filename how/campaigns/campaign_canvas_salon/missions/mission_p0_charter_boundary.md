---
plan_id: mission_p0_charter_boundary
type: plan
title: "P0.1 — Charter + boundary ADR + decision record"
owner: stanley
status: completed
campaign_id: campaign_canvas_salon
campaign_phase: 0
campaign_mission_number: 1
mission_class: reconnaissance
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, salon, surface, boundary, decision, p0]
---

# Mission: P0.1 — Charter + boundary ADR + decision record

**Campaign**: [[how/campaigns/campaign_canvas_salon/campaign_canvas_salon|campaign_canvas_salon]]
**Phase**: 0 — Charter, boundary ADR & decision record
**Mission**: 1 of 6

## Goal

Open Operation Salon on a fixed footing — **before any build** — by (1) chartering the campaign, (2) drawing the
canvas-as-surface **boundary** vs ISS / Astro / Terminal / OIP as a citable ADR, and (3) recording the eight
governance/scope decisions that gate the leg-2 and leg-3 work as a single ratifiable record. This front-loads the two
real risks (boundary creep into neighbour systems; an avoidable touch of the immutable `canvas_std`) into a cheap,
ratifiable decision phase — the Keystone/Atelier/Palette lesson that governance touches discovered mid-build cost the
most. No spec is authored and no code is written this mission.

## Exit Gate

A campaign charter, a boundary ADR (`adr_006`), and an 8-decision record exist — each decision with a doctrine-aligned
default + rationale; the foundation facts (leg-2 spec ratified but loading "how" unspecified; leg-3 greenfield;
`adr_006` next free number; no slug collision) are confirmed. **The operator ratifies the decision record + `adr_006`
at the P0→P1 gate — that ratification activates the campaign (`status: active`) and authorizes Phase P1 (the leg-2
loading-protocol spec).**

## Objectives

### 1. Confirm the foundation
- **Status**: completed
- **Session**: session_stanley_20260622_133716_salon_scaffold_p0
- **Description**: Verify leg-1 done (×7); leg-2 metadata spec ratified (`spec_context_object.md`) but the agent
  loading/traversal protocol unspecified; leg-3 greenfield (no interface-surface spec; "OIP/interface thesis" doc not
  in vault; future `aDNA.aDNA` OIP campaign owns routing). Confirm `adr_006` is the next free ADR number and
  `campaign_canvas_salon` does not collide.
- **Files**: `what/specs/`, `what/decisions/`, `how/campaigns/` (read-only)
- **Depends on**: none

### 2. Scaffold + author charter, boundary ADR, decision record
- **Status**: completed
- **Session**: session_stanley_20260622_133716_salon_scaffold_p0
- **Description**: Create the campaign dir (`campaign_canvas_salon.md` + `CLAUDE.md` + `missions/` + `missions/artifacts/`);
  author `what/decisions/adr_006_canvas_surface_boundary.md` (status: proposed) on the LP↔Canvas seam model; author
  the 8-decision record (D1–D8, defaults + rationale + alternatives, status: pending).
- **Files**: campaign scaffold, `what/decisions/adr_006_canvas_surface_boundary.md`, `missions/artifacts/p0_decision_record.md`, `STATE.md`
- **Depends on**: 1

### 3. Operator ratification (P0→P1 gate)
- **Status**: completed
- **Session**: session_stanley_20260622_140033_salon_p0_ratify_p1_spec
- **Description**: Present the decision record + `adr_006`. On accept/edit of each: set both records `status: ratified`,
  update the campaign Decision Points, complete this mission (+AAR), set the campaign `status: active`, and open Phase
  P1 (author the P1 mission — the leg-2 loading/traversal protocol spec).
- **Files**: this mission (→ completed + AAR), campaign doc (Decision Points → ratified), `p0_decision_record.md`
  (→ ratified), `adr_006` (→ ratified), STATE.md
- **Depends on**: 2

## Campaign Context

### Previous Mission Outputs
- None — first mission of the campaign (predecessor: Operation Palette, completed 2026-06-22).

### Next Mission Inputs
- P1 (leg-2 loading spec) needs: ratified leg-2 spec home (D5) + leg-2 impl/firewall posture (D6) + the boundary
  (`adr_006`, D7).
- P3 (leg-3 interface spec) needs: ratified leg-3 depth (D4) + boundary (D7) + coordination posture (D8).

## Notes

All eight decisions have plan defaults in the approved plan (`~/.claude/plans/please-read-the-claude-md-sleepy-aho.md`).
This mission only *records* them and *drafts* `adr_006`; it authors no spec and writes no code. The single biggest call
is **D6** (leg-2 impl placement + firewall posture) — the default preserves the `canvas_std` firewall by building the
loader as a new sibling package; the alternative deliberately re-opens `canvas_std` as a sanctioned reference-impl
extension. It is an explicit operator decision precisely because it changes the frozen-since-Keystone guarantee.

## Completion Summary

Completed 2026-06-22 at the P0→P1 gate (`session_stanley_20260622_140033_salon_p0_ratify_p1_spec`). The operator
ratified the 8-decision record + `adr_006` — **all eight decisions at their doctrine-aligned defaults** (D6 = the
firewall-preserving sibling `canvas_context`). Salon is now `active` at P1.

### Deliverables
- Campaign scaffold (charter `campaign_canvas_salon.md` + per-campaign `CLAUDE.md` + this P0 mission) — **ratified**.
- `what/decisions/adr_006_canvas_surface_boundary.md` (boundary vs ISS/Astro/Terminal/OIP) — **ratified** (binding).
- `missions/artifacts/p0_decision_record.md` (D1–D8, defaults + rationale + alternatives) — **ratified**.
- 3/3 objectives complete (foundation confirmed · scaffold/draft · operator ratification).

### Descoped
- None. P0 closed on its charter.

### Key Findings
- Front-loading the boundary (`adr_006`) + the load-bearing firewall posture (D6) into a cheap, ratifiable decision
  phase worked exactly as the Cartography/Keystone lesson predicted — the single biggest call (touch `canvas_std` or
  not) was surfaced as an explicit operator choice rather than an agent assumption, and resolved cleanly (preserve).

### Scope Changes
- None.

## AAR

- **Worked**: All 8 decisions carried doctrine-aligned defaults, so the gate cleared in one pass at defaults (incl. the load-bearing D6 → preserve the firewall).
- **Didn't**: Nothing material; the gate was a clean human ratification with no edits.
- **Finding**: Drawing the boundary ADR *before* any build gives the leg-2 spec a citable fence (contract-not-engine), which made the immediately-following P1 spec scope itself unambiguously.
- **Change**: None — the planning-phase pattern (charter + boundary + ratifiable decision record, HOLD at gate) is reusable as-is.
- **Follow-up**: P1 mission `mission_p1_context_loading_spec.md` — author `spec_canvas_context_loading.md` (this session); HOLD at P1→P2.
