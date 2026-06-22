---
plan_id: mission_p3_interface_surface_spec
type: plan
title: "P3 — Leg-3 interface-surface spec (greenfield, spec-only)"
owner: stanley
status: in_progress
campaign_id: campaign_canvas_salon
campaign_phase: 3
campaign_mission_number: 4
mission_class: specification
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, salon, surface, interface, leg3, p3, spec]
---

# Mission: P3 — Leg-3 interface-surface spec

**Campaign**: [[how/campaigns/campaign_canvas_salon/campaign_canvas_salon|campaign_canvas_salon]]
**Phase**: 3 — Leg-3 interface-surface spec (greenfield)
**Mission**: 4 of 6

## Goal

Specify-and-bound **leg 3** of the Canvas thesis: author the greenfield
[[what/specs/spec_interface_surface|spec_interface_surface.md]] — a canvas as a **human↔AI / human↔human interaction
surface**, *as a contract bounded by [[what/decisions/adr_006_canvas_surface_boundary|ADR-006]]* (no routing, no engine,
no transport; rides `_reserved.interaction` additively). With leg 1 (output, Palette) and leg 2 (context object, Salon
P2) **proven**, this completes the thesis as **proven (1, 2) + specified-and-bounded (3)**.

## Operator decisions (P3 open, plan-mode 2026-06-22)

The external "OIP/interface thesis doc" ADR-000 named to ground leg-3 vocabulary **does not exist** — it is a future
deliverable of the unopened `aDNA.aDNA` OIP-unification campaign. Per the P3 gate ("ratified **or** explicitly
deferred") + ratified **D4** (spec-only) + the risk-register mitigation (spec-only default + coordinate early), the
operator chose:
1. **Proceed first-principles** (not defer) — author the spec now, Canvas-scoped v1, grounded on ADR-006 + the proven
   leg-2 model + ISS as exemplar; re-anchor to the OIP thesis when it lands (`v1.x` alignment pass).
2. **Concrete shape + `I-*` checks** — fix the additive `_reserved.interaction` JSON shape + propose an `I-*`
   conformance family (mirroring how leg-2 fixed `context_object`).

## Exit Gate

`spec_interface_surface.md` is **ratified by the operator** (or explicitly deferred in writing); coordination with
`aDNA.aDNA` (OIP) + ISS is **recorded** (D8 memos filed). **HOLD at the P3 ratification gate** — never self-ratify, never
auto-advance into P4 (SO-1). This session authors the draft + files the memos + presents for ratification; the mission
completes (with AAR) **at** ratification.

## Objectives

### 1. Author the leg-3 interface-surface spec
- **Status**: completed (draft)
- **Description**: `what/specs/spec_interface_surface.md`, mirroring the leg-2 spec structure (frontmatter +
  RFC-2119 + §1 purpose / §2 scope / §3 abstract model / §4 normative contract / §5 binding sub-contract / §6 primitives
  table / §7 authority / §8 degradation / §9 conformance / §10 ref-impl / §11 boundary / §12 related). Core design:
  interaction = a `read → act → re-read` loop over the leg-2 `ContextGraph`; five primitives (`anchor`, `affordance`,
  `response`, `surface state`, `turn`); concrete additive `_reserved.interaction` shape; IX1–IX6; the **round-trip-to-
  baseline** headline property; proposed `I-*` conformance family; ADR-006 boundary table.
- **Files**: `what/specs/spec_interface_surface.md` (created)

### 2. File the D8 coordination heads-up memos
- **Status**: completed (canonical authored; cross-vault delivery operator-gated)
- **Description**: two outbound memos in `who/coordination/` — `seam: Canvas ↔ OIP` (Canvas defines *what* a
  canvas-surface is, not *when* to route to it; requests the OIP thesis outline when authored) and `seam: Canvas ↔ ISS`
  (Canvas owns the affordance/anchor/response/turn *grammar*; ISS owns the gate *engine* that may consume it — clean
  seam, no overlap). Canonical copies live in Canvas; cross-posting into `aDNA.aDNA` is an operator-gated cross-vault
  write (staged, not silently committed into another vault's tree).
- **Files**: `who/coordination/coord_2026_06_22_mondrian_to_oip_canvas_interface_seam.md`,
  `who/coordination/coord_2026_06_22_mondrian_to_iss_canvas_interface_seam.md`

### 3. Governance currency + present for ratification
- **Status**: completed
- **Description**: `STATE.md` resume block → "P3 draft authored, HELD at ratification"; campaign master P3 row
  `planned → in_progress` + risk-register note (OIP-doc dependency resolved by proceeding first-principles per operator);
  campaign `CLAUDE.md` current-phase line; `what/specs/AGENTS.md` indexes the new spec. SITREP + draft presented; **HOLD**.
- **Files**: `STATE.md`, `campaign_canvas_salon.md`, `campaign_canvas_salon/CLAUDE.md`, `what/specs/AGENTS.md`

### 4. Ratify + close (awaits operator)
- **Status**: pending (human gate)
- **Description**: on operator ratification, set spec `status: draft → ratified`, fold the `I-*` family into
  `spec_conformance_suite.md` (separate ratified edit), complete this mission (+AAR), campaign P3 row → completed, and
  HOLD at the P3→P4 gate (P4 is a stretch; do not open without the operator).
- **Files**: this mission (→ completed + AAR), `spec_interface_surface.md` (status flip), `spec_conformance_suite.md`,
  campaign doc, STATE.md

## Campaign Context

### Previous Mission Outputs
- P2 completed (2026-06-22): **leg 2 PROVEN** — `canvas_context` reference loader loads a producer `.canvas` as a
  `ContextGraph` without rendering (28/28; `canvas_std` firewall git-diff 0). The readable-context substrate leg 3
  builds its `read` step on.
- P0 ratified `adr_006` (the boundary) + the 8-decision record (D4 spec-only; D8 coordinate early).

### Next Mission Inputs
- P4 (stretch POC) needs: the ratified leg-3 spec (this mission). P5 (close) needs P2 + P3.

## Notes

- **Boundary is non-negotiable** — `adr_006` is ratified; the spec defines a *contract*, encodes **no routing** (the
  load-bearing §3 line), specifies no renderer/capture runtime/transport, and rides `_reserved.interaction` only.
- **Reuse, don't reinvent** — `anchor` = `panel_link.anchors` (orphan check `validate_anchors`); the read step is a
  leg-2 load; surface state is a leg-2 `ContextGraph`. Leg 3 is a thin overlay.
- **`canvas_std` is immutable** (firewall, D6) — no edit; `git status -s -- what/code/canvas_std/` clean at the gate.

## Completion Summary

*Filled at ratification (the mission completes at the human gate, not at draft-authoring).*

## AAR

*Filed at mission completion (SO-5) — i.e. at ratification.*
