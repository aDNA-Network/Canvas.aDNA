---
plan_id: mission_e3_2_canvas_core_shim
type: plan
title: "E3.2 — Repoint canvas_core → canvas_std behind a deprecation shim"
owner: stanley
status: active
campaign_id: campaign_canvas_genesis
campaign_phase: 3
campaign_mission_number: 2
mission_class: implementation
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, e3, shim, deprecation, canvasforge]
---

# Mission: E3.2 — Repoint `canvas_core` → `canvas_std` behind a deprecation shim

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]]
**Phase**: 3 — CanvasForge migration (parity-gated) ⚠️ highest risk
**Mission**: 2 of 4

## Goal

Make `canvas_std` (Canvas.aDNA) the single source of truth for the reference canvas logic by repointing
`canvasforge.canvas_core` to re-export from it **behind a deprecation shim** — mirroring the proven
`lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` precedent. Both import paths stay live
during the grace window (decision **E-D2**, default 12 months) so nothing breaks and rollback is a one-line revert.
This is the first consequential code change of E3; it is **gated downstream by the E3.3 parity gate** — no cutover
here, only the reversible repoint.

## Exit Gate

- `canvasforge.canvas_core` re-exports the reference surface from `canvas_std` with a `DeprecationWarning`
  (`stacklevel=2`) and a `DEPRECATED_STUB` provenance marker, per the lattice-protocol shim pattern.
- Producer-side engines (`layout_*`, `selection_board`, deck/comic composition, `pdf_export`, `gdoc_export`) remain
  in CanvasForge, **unchanged**.
- CanvasForge's existing test suite is **green under the shim** (both old and new import paths exercised).
- **E-D2 grace-window length decided** and recorded (default 12mo).
- **No baseline regeneration yet** — the parity proof is E3.3; baseline `3ce4d341…` stays UNCHANGED.

## Objectives

### 1. API-parity audit: canvas_std covers the canvas_core reference surface
- **Status**: planned
- **Description**: Diff the reference surface CanvasForge consumes (`CanvasBuilder` constants/schema,
  `validate`/`read_back`/`diff`/`merge`/`compute_sync_hash`, `TYPE_MAPPING`/`EDGE_TYPE_MAPPING`, the `VALID_*`
  enums) against `canvas_std`'s public API. Record any gap as a blocker (fix in `canvas_std` via the governed
  process before repointing). Confirm `canvas_std` import works from the CanvasForge environment.
- **Files**: audit note in mission artifacts; possibly `Canvas.aDNA/what/code/canvas_std/` (gap fixes)
- **Depends on**: E3.1 (wrapper anchors the seam)

### 2. Install the deprecation shim in canvas_core
- **Status**: planned
- **Description**: Convert `canvasforge/canvas_core/` reference modules to re-export from `canvas_std` with a
  module docstring (deprecation date, old→new import path in federation_ref form, expiry), `warnings.warn(...,
  DeprecationWarning, stacklevel=2)`, `from canvas_std... import *`, and a trailing `# DEPRECATED_STUB Canvas.aDNA`
  marker. Keep producer engines importing the live (now-federated) symbols.
- **Files**: `CanvasForge.aDNA/what/code/canvas_core/*` (reference modules only)
- **Depends on**: 1

### 3. Decide E-D2 grace-window length
- **Status**: planned
- **Description**: Set the shim grace window (default 12mo per the lattice-protocol precedent). Register the shim in
  `Home.aDNA` shim ledger (class, window, retire-condition, owner) per workspace Standing Rule 9.
- **Files**: shim ledger entry (Home.aDNA); note in this mission
- **Depends on**: 2

### 4. CanvasForge test suite green under the shim
- **Status**: planned
- **Description**: Run CanvasForge's full suite; both old (`canvas_core`) and new (`canvas_std`) paths must pass,
  old path emitting `DeprecationWarning`. Fix import/compat issues until green.
- **Files**: (tests)
- **Depends on**: 2

## Campaign Context

### Previous Mission Outputs
- E3.1 created `CanvasForge.aDNA/canvas/` with the `federation_ref` → `canvas_std` (the seam this mission wires in code).

### Next Mission Inputs
- E3.3 regenerates CanvasForge's locked reference outputs **through `canvas_std`** (via the shim) and proves parity
  vs Wilhelm 8.80 / Issue 01 8.43. The shim makes that regeneration possible while keeping rollback trivial.

## Notes

- **Risk (High):** `canvas_std` ↔ embedded `CanvasBuilder` drift. Mitigation: single source post-repoint; shim
  re-exports; both paths tested during the window (Risk Register, campaign doc).
- Only the **reference** `canvas_core` logic repoints — the application layers (`canvas_presentation`,
  `canvas_comic`) and export/layout engines stay producer-side (D2 = extract, not absorb).

## Completion Summary

*Fill out when setting `status: completed`.*

### Deliverables
- [ ] `canvas_core` shim re-exporting from `canvas_std` (DeprecationWarning + marker)
- [ ] E-D2 grace window decided + shim ledger entry
- [ ] CanvasForge suite green under the shim

### Descoped
- Parity regeneration + cutover (E3.3 / E3.4).

### Key Findings
-

### Scope Changes
-

## AAR

*Mandatory before setting `status: completed`. See `how/templates/template_aar_lightweight.md`.*

- **Worked**:
- **Didn't**:
- **Finding**:
- **Change**:
- **Follow-up**:
