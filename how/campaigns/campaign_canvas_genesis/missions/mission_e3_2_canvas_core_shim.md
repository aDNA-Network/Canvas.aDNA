---
plan_id: mission_e3_2_canvas_core_shim
type: plan
title: "E3.2 — Repoint canvas_core → canvas_std behind a deprecation shim"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 3
campaign_mission_number: 2
mission_class: implementation
status_note: "completed 2026-06-13 — constants-only shim landed; suite green at parity; E-D2=12mo"
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
- **Status**: ✅ done
- **Description**: Diff the reference surface CanvasForge consumes (`CanvasBuilder` constants/schema,
  `validate`/`read_back`/`diff`/`merge`/`compute_sync_hash`, `TYPE_MAPPING`/`EDGE_TYPE_MAPPING`, the `VALID_*`
  enums) against `canvas_std`'s public API. Record any gap as a blocker (fix in `canvas_std` via the governed
  process before repointing). Confirm `canvas_std` import works from the CanvasForge environment.
- **Files**: audit note in mission artifacts; possibly `Canvas.aDNA/what/code/canvas_std/` (gap fixes)
- **Depends on**: E3.1 (wrapper anchors the seam)

### 2. Install the deprecation shim in canvas_core
- **Status**: ✅ done
- **Description**: Convert `canvasforge/canvas_core/` reference modules to re-export from `canvas_std` with a
  module docstring (deprecation date, old→new import path in federation_ref form, expiry), `warnings.warn(...,
  DeprecationWarning, stacklevel=2)`, `from canvas_std... import *`, and a trailing `# DEPRECATED_STUB Canvas.aDNA`
  marker. Keep producer engines importing the live (now-federated) symbols.
- **Files**: `CanvasForge.aDNA/what/code/canvas_core/*` (reference modules only)
- **Depends on**: 1

### 3. Decide E-D2 grace-window length
- **Status**: ✅ done
- **Description**: Set the shim grace window (default 12mo per the lattice-protocol precedent). Register the shim in
  `Home.aDNA` shim ledger (class, window, retire-condition, owner) per workspace Standing Rule 9.
- **Files**: shim ledger entry (Home.aDNA); note in this mission
- **Depends on**: 2

### 4. CanvasForge test suite green under the shim
- **Status**: ✅ done
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

**Completed 2026-06-13** (session `session_stanley_20260613_205753_keystone_e3_2_shim`). Operator scope:
**constants-only** repoint + **editable install**. The `canvasforge.canvas_core` Standard floor now resolves from
`canvas_std.schema` (SSOT) behind a deprecation shim; CanvasForge suite green at parity; baseline `3ce4d341`
untouched. HELD at the E3.2→E3.3 boundary.

### Deliverables
- [x] `canvas_core` shim re-exporting from `canvas_std` (`DeprecationWarning` stacklevel=2 + `# DEPRECATED_STUB Canvas.aDNA` marker) — `CanvasForge.aDNA/what/code/canvas_core/core.py`, the 10 `VALID_*` enums + `TYPE_MAPPING` + `EDGE_TYPE_MAPPING` as `CanvasBuilder` class attributes now bound to `canvas_std.schema` objects (verified `is`-identical).
- [x] E-D2 grace window decided (**12 months**, expiry **2027-06-13**) + shim ledger entry — `Home.aDNA/.../disposition_ledger_v2.md` §C (count 17→18; row + row-note; class `deprecation (in-code re-export)`; owner Mondrian + Hermes).
- [x] CanvasForge suite green under the shim — canonical **900 passed / 3 skipped / 0 failed**; complete tree (incl. `canvas_presentation`) **957 passed / 5 skipped / 0 failed**; old + new import paths exercised; old path emits the `DeprecationWarning`. `canvas_std` own suite unregressed (46/8).
- [x] API-parity audit artifact — `missions/artifacts/e3_2_api_parity_audit.md` (byte-identity of all 12; no mutation; no module-level floor imports; PASS/no blockers).

### Descoped
- Round-trip **function** repointing (`validate`/`diff`/`merge`/round-trip) — deferred to post-E3.3 (operator chose constants-only; functions repoint once parity is proven).
- Parity regeneration + cutover (E3.3 / E3.4). Baseline `3ce4d341` deliberately unchanged.

### Key Findings
- The floor constants live as **`CanvasBuilder` class attributes** (`core.py` 46–117), accessed via `self.X` / `CanvasBuilder.X` — NOT module-level (corrects the planning-time exploration summary). This made the repoint a clean class-attribute reassignment with object identity preserved; no producer touched.
- The cross-vault import gap was real but trivial to close: `adna-canvas-std` is a zero-dep installable package; an editable install into a py3.12 `.venv` at `CanvasForge.aDNA/what/code/.venv` (gitignored) suffices. Pillow + googleapiclient were the only env deps blocking a fully-green pre-existing suite (orthogonal to the floor).
- All 12 floor constants are **value-identical** (verbatim E0.2 port) → zero behavioral drift from the constants repoint; the only suite delta is +1 `DeprecationWarning`.

### Scope Changes
- None to mission intent. Skipped the planned `what/code/.gitignore` add — CanvasForge's **root** `.gitignore` already ignores `.venv/`. No `pytest.ini` edit needed — it does not elevate warnings to errors.

## AAR

- **Worked**: Class-attribute reassignment to `canvas_std.schema` + module-level `DeprecationWarning`/marker, validated by `is`-identity and a differential pre/post-shim suite diff (897→identical pass set; 0 regression). Editable install of the zero-dep `adna-canvas-std`.
- **Didn't**: Pre-existing suite wasn't green out-of-the-box in a fresh venv — 28 collection errors (`PIL`) + 3 gdoc failures (`googleapiclient`); both were missing test deps, unrelated to the shim. Resolved by installing them.
- **Finding**: The exploration summary mislocated the floor as module-level; reading the actual definition site (class attributes) changed the shim shape from "wholesale module redirect" to "surgical class-attr rebind." Verifying the definition site firsthand was load-bearing.
- **Change**: Establish a documented CanvasForge test env (the gitignored `.venv` + the canvas_std editable install) as the standard runner for E3.3+ — captured here and in the audit note so the parity gate inherits it.
- **Follow-up**: E3.3 parity gate (Wilhelm 8.80 / Issue 01 8.43) — regenerate locked outputs *through* `canvas_std` via this shim; if green, the round-trip-function repoint (descoped here) can follow. Shim retirement tracked to Keystone E6 (Home.aDNA §C).
