---
plan_id: mission_e3_1_canvasforge_wrapper
type: plan
title: "E3.1 — Introduce the canvas/ federation wrapper in CanvasForge"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 3
campaign_mission_number: 1
mission_class: integration
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, e3, federation, canvasforge]
---

> **STATUS: completed 2026-06-13** (session `session_stanley_20260613_193008_keystone_e3_open`). Wrapper landed
> additively; see Completion Summary + AAR below.

# Mission: E3.1 — Introduce the `canvas/` federation wrapper in CanvasForge

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]]
**Phase**: 3 — CanvasForge migration (parity-gated) ⚠️ highest risk
**Mission**: 1 of 4

## Goal

Stand up the `canvas/` federation wrapper inside `CanvasForge.aDNA` so the forge declares its consumption of the
**aDNA Canvas Standard v2.0.0** via a `federation_ref` (per `spec_federation_contract` §6.1). This is the **purely
additive** first step of the E3 migration: it establishes the federation seam and the cutover/rollback framing
**without touching any code** — the `canvas_core` repoint behind the deprecation shim is E3.2. It advances Operation
Keystone by making CanvasForge's standard-consumption explicit and contract-bound before any code moves.

## Exit Gate

- `CanvasForge.aDNA/canvas/CLAUDE.md` exists: `type: federation_wrapper`, a well-formed `federation_ref`
  (`source_vault: Canvas.aDNA`, `version: "2.0.0"`, `version_policy: minor`, `conformance_target: adna_native`,
  the spec set in `specs_used`, `profiles_used: [lattice, deck, comic]`, producer engines listed as
  `local_extensions`), plus the standard-bearer relationship + cutover/rollback framing.
- `CanvasForge.aDNA/canvas/graft_manifest.yaml` exists (minimal; `grafts: []` with the §2.2 reference-not-graft
  rationale recorded).
- **Substrate untouched** — `git -C CanvasForge.aDNA status` shows only the additive `canvas/` directory; **no diff
  to `what/code/canvas_core/`**; VR baseline `3ce4d341…` intact.
- Committed in the CanvasForge repo with a `Keystone E3.1 —` message.

## Objectives

### 1. Create the `canvas/` wrapper CLAUDE.md
- **Status**: completed
- **Session**: session_stanley_20260613_193008_keystone_e3_open
- **Description**: Author `CanvasForge.aDNA/canvas/CLAUDE.md` modeled on the proven `Canvas.aDNA/iii/CLAUDE.md`
  precedent (frontmatter + producer-side standard-bearer note + `federation_ref` block + routing notes +
  cross-references). The `federation_ref` shape is taken verbatim from `spec_federation_contract` §6.1/§2.
- **Files**: `CanvasForge.aDNA/canvas/CLAUDE.md`
- **Depends on**: none

### 2. Create the `graft_manifest.yaml`
- **Status**: completed
- **Session**: session_stanley_20260613_193008_keystone_e3_open
- **Description**: Record the §2.2 graft decision: the Standard's spec set + reference impl are **referenced** via
  `federation_ref` (never copied), so no grafts are required at E3.1. Manifest carries `grafts: []` + rationale.
- **Files**: `CanvasForge.aDNA/canvas/graft_manifest.yaml`
- **Depends on**: 1

### 3. Verify additive-only + commit
- **Status**: completed
- **Session**: session_stanley_20260613_193008_keystone_e3_open
- **Description**: Confirm `git status` in CanvasForge shows only the new `canvas/` dir (no `canvas_core` diff);
  commit with a `Keystone E3.1 —` message. (Push deferred per the local-commit-accumulate workspace convention.)
- **Files**: (commit)
- **Depends on**: 1, 2

## Campaign Context

### Previous Mission Outputs
- E2 delivered the complete `canvas_std` reference impl (`Canvas.aDNA/what/code/canvas_std/`) — validators,
  round-trip, `_reserved` validators, conformance harness, v2.0.0 JSON Schema, `canvas-std` CLI. This wrapper
  references that impl as `source_impl`.

### Next Mission Inputs
- E3.2 repoints `canvasforge.canvas_core` onto `canvas_std` behind a deprecation shim. The wrapper this mission
  creates is where E3.2's federation seam is anchored and where the cutover/rollback framing is recorded.

## Notes

- **Standard-bearer inversion (producer side):** unlike Canvas's `iii/` wrapper (Canvas consuming III's engine),
  here CanvasForge is the **producer** consuming the **Standard** from Canvas.aDNA. The wrapper declares
  consumption only; Canvas governs the standard, CanvasForge holds the code.
- Producer-side engines — `layout_*`, `selection_board`, deck/comic composition, `pdf_export`, `gdoc_export` —
  **stay in CanvasForge** (listed as `local_extensions`); only the reference `canvas_core` logic federates (E3.2).
- The seam this anchors was formalized two-sided on 2026-06-13 (Mondrian's countersign of Noether's LP↔Canvas seam
  memo); §3.2 of that memo affirms CanvasForge as canonical code home + baseline `3ce4d341` authoritative.

## Completion Summary

Completed 2026-06-13 in session `session_stanley_20260613_193008_keystone_e3_open`.

### Deliverables
- [x] `CanvasForge.aDNA/canvas/CLAUDE.md` — `type: federation_wrapper`; `federation_ref` → Canvas.aDNA v2.0.0
  (`source_spec` + `source_impl` `canvas_std`, `version_policy: minor`, `conformance_target: adna_native`,
  `specs_used` ×5, `profiles_used: [lattice, deck, comic]`, producer engines as `local_extensions`); producer-side
  standard-bearer note; downstream-safety note; routing notes; cross-references. Commit `7bb833f` (CanvasForge).
- [x] `CanvasForge.aDNA/canvas/graft_manifest.yaml` — `grafts: []` with the §2.2 reference-not-graft rationale.
- [x] Additive-only commit in CanvasForge (`7bb833f`) — verified `git status` shows only `canvas/`; **no diff to
  `what/code/canvas_core/`**; baseline `3ce4d341` intact. `canvas_std` suite re-confirmed green (46 pass / 8 skip).

### Descoped
- Any `canvas_core` code change — that is E3.2 (the deprecation shim), behind which the repoint happens.
- A CanvasForge root Standing Order routing canvas consumption through this wrapper — deferred to E3.2/cutover when
  the seam becomes load-bearing (kept E3.1 additive/reversible).

### Key Findings
- CanvasForge already carried a mature `iii/` federation wrapper (v0.5.0-pinned, bridge_pack + local_skill) — a
  strong local precedent for the `canvas/` wrapper's shape and the downstream-safety discipline.
- The three downstream consumers (SS presentationforge/graphicnovelforge, CC presentationforge) reference
  CanvasForge **lattices**, not code paths — so the wrapper is downstream-safe; the only path that will affect them
  is the `canvas_core` public surface, which E3.2's shim is designed to preserve.

### Scope Changes
- None. (The LP↔Canvas seam countersign + the broader E3 phase-open were done in the same session but are tracked
  separately — coordination + campaign-doc/STATE, not this mission.)

## AAR

- **Worked**: Modeling the wrapper on the existing CanvasForge `iii/` wrapper + `spec_federation_contract` §6.1 made
  the `federation_ref` shape unambiguous; the additive-only constraint held cleanly (zero `canvas_core` diff).
- **Didn't**: Nothing blocked. Minor: a pre-existing untracked Hypnos AAR sat in CanvasForge `who/coordination/` —
  scoped the commit to `canvas/` only to avoid sweeping unrelated work.
- **Finding**: Anchoring the federation seam *before* touching code (E3.1 → E3.2) keeps the highest-risk phase
  reversible — the wrapper + pinned `federation_ref` exist and are reviewable before any import repoints.
- **Change**: none.
- **Follow-up**: E3.2 (`mission_e3_2_canvas_core_shim`) — repoint `canvas_core` → `canvas_std` behind the
  deprecation shim; decide the E-D2 grace window; register the shim in the Home.aDNA ledger.
