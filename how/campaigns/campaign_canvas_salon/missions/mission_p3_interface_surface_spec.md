---
plan_id: mission_p3_interface_surface_spec
type: plan
title: "P3 — Leg-3 interface-surface spec (greenfield, spec-only)"
owner: stanley
status: completed
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

### 4. Ratify + close
- **Status**: completed
- **Description**: operator ratified 2026-06-22 ("Approved") at all 9 default open-question resolutions. Spec
  `status: draft → ratified` (+ RATIFIED banner; open-questions → resolved-decisions log); the `I-*` family folded into
  `spec_conformance_suite.md` §4.1 (additive/optional; `interaction_version 1.0`; validator-impl forward-pointed;
  Standard-version cut deferred). Mission completed (+AAR), campaign P3 row → completed. **HOLD at the P3→P4 gate** (P4
  is a stretch; not opened).
- **Files**: this mission (→ completed + AAR), `spec_interface_surface.md` (ratified), `spec_conformance_suite.md`
  (§4.1 I-*), campaign doc, campaign CLAUDE.md, STATE.md, `what/specs/AGENTS.md`

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

Completed 2026-06-22 (drafted + ratified same session). **Leg 3 specified-and-bounded — the Canvas three-leg thesis is
complete** (1 output + 2 context-object PROVEN; 3 interface-surface RATIFIED).

### Deliverables
- **[[../../../what/specs/spec_interface_surface|spec_interface_surface.md]]** (`status: ratified`) — a canvas as a
  human↔AI / human↔human interaction surface, **as a contract** bounded by `adr_006` (no routing/engine/transport;
  rides `_reserved.interaction` additively). Mirrors the leg-2 spec 1:1: interaction = a `read → act → re-read` loop
  over the leg-2 `ContextGraph`; five primitives (`anchor` · `affordance` · `response` · `surface state` · `turn`);
  concrete `_reserved.interaction` shape; normative IX1–IX6; the affordance↔anchor binding sub-contract;
  round-trip-to-baseline as the headline property; participant-neutrality. Ratified at all 9 default open-question
  resolutions (recorded as the §Ratification-decisions log).
- **`I-*` conformance family** folded into `spec_conformance_suite.md` §4.1 (I-1..I-3; additive + optional;
  `interaction_version 1.0`; degradation covered by §5; validator-impl forward-pointed; reuses `validate_anchors`).
- **D8 coordination memos** filed — `seam: Canvas ↔ OIP` + `seam: Canvas ↔ ISS` (canonical in `who/coordination/`;
  delivery copies staged uncommitted in `aDNA.aDNA/who/coordination/`, commit operator-gated).
- Governance currency: STATE, campaign master (P3 → completed; OIP risk RESOLVED), campaign CLAUDE, `what/specs/AGENTS.md`.

### Descoped / deferred
- **Leg-3 runtime build** — deferred to a follow-on charter (D4 spec-only). The stretch **P4 POC** (operator-annotates →
  agent re-reads → responds) is **not opened** (HELD at the P3→P4 gate).
- **Formal Standard-version cut** for the `I-*` family — deferred (operator/FA at a deliberate release; open-Q7 default).
- **OIP re-anchoring** — a future `v1.x` alignment pass when the `aDNA.aDNA` OIP/interface thesis is authored.

### Key findings
- The external "OIP/interface thesis" doc the campaign nominally gated P3 on **does not exist** (a future, unopened
  `aDNA.aDNA` deliverable). Proceeding **first-principles, Canvas-scoped v1** — grounded on `adr_006` + the proven leg-2
  model + ISS as exemplar — let leg 3 land without blocking on a cross-vault campaign, with a clean `interaction_version`
  seam to re-anchor later. The High-risk register entry is resolved.
- Framing interaction as a **loop over the leg-2 `ContextGraph`** (not a new model) kept leg 3 a thin additive overlay —
  `anchor` reuses `panel_link.anchors`, the read step is a leg-2 load, surface-state *is* a `ContextGraph`. This is what
  kept it inside the ADR-006 "contract, not engine" fence.

### Scope changes
- None. Built + ratified within the P3 charter; HOLD at P3→P4 (no auto-advance into the stretch POC).

## AAR

- **Worked**: Mirroring the ratified leg-2 spec 1:1 (structure + RFC-2119 + the `read → act → re-read` framing over its
  `ContextGraph`) made the greenfield leg-3 spec land coherent and firewall-safe in one session.
- **Didn't**: The campaign's stated P3 gate ("acquire the OIP thesis doc") was unworkable as written — the doc doesn't
  exist; the gate's own "ratified **or** deferred" escape + ratified D4 (spec-only) were what actually unblocked it.
- **Finding**: Greenfield-with-a-missing-external-dependency resolves cleanly by **proceeding Canvas-scoped v1 with a
  versioned re-anchor seam** (`interaction_version`), not by deferring on an unopened sibling campaign.
- **Change**: When a phase gate names an external artifact that turns out not to exist, surface it as an operator
  decision *before* authoring (done here in plan-mode) rather than discovering it mid-build.
- **Follow-up**: P4 (stretch POC) or P5 (close) — operator's call at the P3→P4 gate; `I-*` validator implementation +
  the formal Standard-version cut ride a future deliberate release; OIP `v1.x` re-anchor when the thesis lands.
