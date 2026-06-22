---
plan_id: mission_p1_context_loading_spec
type: plan
title: "P1 — Leg-2 context-loading / traversal protocol spec"
owner: stanley
status: completed
campaign_id: campaign_canvas_salon
campaign_phase: 1
campaign_mission_number: 2
mission_class: specification
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, salon, surface, context_object, loading, traversal, spec, p1]
---

# Mission: P1 — Leg-2 context-loading / traversal protocol spec

**Campaign**: [[how/campaigns/campaign_canvas_salon/campaign_canvas_salon|campaign_canvas_salon]]
**Phase**: 1 — Leg-2 loading/traversal protocol (spec)
**Mission**: 2 of 6

## Goal

Supply the **"how"** that `spec_context_object.md` (D7, ratified) declares but leaves unspecified: a substrate-neutral
protocol for how an agent **loads a `.canvas` as a navigable context graph without rendering it** — resolving the
`_reserved.context_object` metadata + `refs` + `summary`, parsing the panel/component/edge structure into a traversable
graph, and resolving wikilinks (in-vault) + `federation_ref` (cross-vault). This proves leg 2 is **specifiable** before
P2 proves it is **buildable**. Per the ratified decisions: spec home is a **new** `spec_canvas_context_loading.md`
(D5, keeps `spec_context_object.md` stable); the reference loader is a **new sibling `canvas_context`** importing
`canvas_std` read-only (D6, firewall preserved) — declared here as a forward-pointer, **built at P2**. The spec stays
within the `adr_006` boundary: a **contract + a reference loader**, never a runtime/transport/router.

## Exit Gate

`spec_canvas_context_loading.md` is authored (valid frontmatter; the L1–L7 load pipeline + the traversal-primitive
read contract + conformance rules + the `adr_006` boundary note + the D6 reference-impl forward-pointer), indexed in
`what/specs/AGENTS.md`, and **operator-ratified**. `canvas_std` firewall git-diff 0 (no code this phase). **HOLD at the
P1→P2 gate** — never auto-advance into the loader build (SO-1).

## Objectives

### 1. Author the leg-2 loading/traversal spec
- **Status**: completed
- **Session**: session_stanley_20260622_140033_salon_p0_ratify_p1_spec
- **Description**: Write `what/specs/spec_canvas_context_loading.md` — substrate-neutral, RFC-2119, grounded in the real
  Standard (`spec_adna_canvas_standard.md` JSON shape + `_reserved` layers; `spec_component_model`; `spec_panel_link_semantics`;
  `spec_roundtrip_protocol_v2`; `spec_federation_contract`) and the `canvas_std` public API. Define the abstract
  context-graph model, the normative L1–L7 load pipeline, the agent-facing traversal primitives, conformance, and the
  D6 reference-impl forward-pointer.
- **Files**: `what/specs/spec_canvas_context_loading.md`
- **Depends on**: P0 ratification (D5 spec home + D6 firewall posture + D7 boundary)

### 2. Index the spec
- **Status**: completed
- **Session**: session_stanley_20260622_140033_salon_p0_ratify_p1_spec
- **Description**: Add the new spec to `what/specs/AGENTS.md` Contents, keeping the spec set coherent.
- **Files**: `what/specs/AGENTS.md`
- **Depends on**: 1

### 3. Operator ratification (P1→P2 gate)
- **Status**: completed
- **Session**: session_stanley_20260622_143651_salon_p1_ratify_p2_loader
- **Description**: Operator ratified `spec_canvas_context_loading.md` **as drafted** (P1→P2 gate, 2026-06-22). Spec set
  `status: ratified`; AGENTS.md index updated; this mission `completed` (+AAR); Phase P2 opened
  (`mission_p2_context_loader_pilot` authored). Same gate authorized building P2 this session.
- **Files**: this mission (→ completed + AAR), `spec_canvas_context_loading.md` (→ ratified), `what/specs/AGENTS.md`,
  campaign doc, campaign CLAUDE.md, STATE.md
- **Depends on**: 1, 2

## Campaign Context

### Previous Mission Outputs
- P0 ratified (2026-06-22): `adr_006` (boundary, binding) + the 8-decision record (all defaults). D5 = new spec home;
  D6 = sibling `canvas_context` (firewall preserved); D7 = boundary accepted.

### Next Mission Inputs
- P2 (leg-2 reference impl + pilot) needs: the ratified loading/traversal spec (this mission) + D6 placement
  (`what/code/canvas_context/`, read-only import of `canvas_std`) + a known-good producer `.canvas`
  (`what/production/document_generator/examples/`).

## Notes

No code is written this phase — the spec is impl-agnostic; the `canvas_context` sibling is declared as a forward-pointer
and built at P2. The `canvas_std` firewall is verified git-diff 0 at the gate. The spec must **not** encode cross-surface
routing (that is the future `aDNA.aDNA` OIP layer, per `adr_006` §3) or federation network transport (interface only).

## Completion Summary

Ratified 2026-06-22 (operator, P1→P2 gate, all-as-drafted).

### Deliverables
- `what/specs/spec_canvas_context_loading.md` — **ratified** (RFC-2119; abstract context-graph model §3 + normative
  L1–L7 load pipeline §4 + resolver interface §5 + traversal read-contract §6 + authority/staleness §7 + degradation
  §8 + conformance §9 + the D6 reference-impl forward-pointer §10 + the `adr_006` boundary §11).
- `what/specs/AGENTS.md` — index entry updated to `ratified`.

### Descoped
- None. The spec was authored complete in the P1 session; this session only ratified it.

### Key Findings
- Grounding the spec on the **actual `canvas_std` public API** (`validate_suite`/`strip`/`compute_sync_hash` +
  `reserved.py` enums) and a **real producer `.canvas`** (rather than a synthetic shape) meant the L1–L7 pipeline
  mapped 1:1 onto the build with no spec rework — the pilot canvas exercises every layer (identity, component_types,
  panel_link reading_order/sequence, surfaces, wikilink refs).

### Scope Changes
- None.

## AAR

- **Worked**: Drafting against the real Standard + a known-good producer canvas made the spec immediately buildable —
  P2 opened and the loader landed in the same session.
- **Didn't**: `context_object.summary` is absent on the producer canvases, so the "identity = id+version+summary"
  framing had to relax to "summary MAY be null" — caught at build, not draft.
- **Finding**: `_reserved` lives at `metadata.frontmatter._reserved` (not top-level) and the golden fixtures carry a
  **placeholder `sync_hash`** — both load-bearing for a correct loader; neither is obvious from the spec prose alone.
- **Change**: none — spec-before-impl with a real-fixture anchor is the right cadence; keep it.
- **Follow-up**: P2 mission `mission_p2_context_loader_pilot` (the reference loader + pilot); AT-1/AT-2 errata stay in
  the LIP queue.
