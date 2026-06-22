---
plan_id: mission_p2_context_loader_pilot
type: plan
title: "P2 — Canvas-as-context reference loader + load-without-rendering pilot"
owner: stanley
status: completed
campaign_id: campaign_canvas_salon
campaign_phase: 2
campaign_mission_number: 3
mission_class: implementation
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, salon, surface, context_object, loader, pilot, leg2, p2]
---

# Mission: P2 — Canvas-as-context reference loader + pilot

**Campaign**: [[how/campaigns/campaign_canvas_salon/campaign_canvas_salon|campaign_canvas_salon]]
**Phase**: 2 — Leg-2 reference impl + pilot
**Mission**: 3 of 6

## Goal

Prove leg 2 is **buildable**: implement the ratified [[what/specs/spec_canvas_context_loading|spec_canvas_context_loading]]
as a **new sibling package** `what/code/canvas_context/` that imports `canvas_std` **read-only** (D6 — firewall
preserved), then run a **load-without-rendering pilot** that loads an existing producer `.canvas`
(`what/production/document_generator/examples/canvas_standard_whitepaper.canvas`) into a navigable `ContextGraph` and
walks its reading order — **with no render pipeline, rasterizer, or media decoder invoked**. When the loader + pilot
are green and `canvas_std` is untouched, **leg 2 (canvas as a first-class context object) is proven**.

## Exit Gate

`canvas_context` implements the §4 L1–L7 load pipeline + the §6 traversal read-contract + the §5 resolver interface;
the loader loads a real producer `.canvas` as a context graph **without rendering**; the `canvas_context` test suite
(loader · traversal · pilot) is **green**; the `canvas_std` suite still passes (no regression); **`git status -s --
what/code/canvas_std/` is clean** (firewall — canvas_std is part of Canvas.aDNA's git, not a nested repo). **HOLD at
the P2→P3 gate** — never auto-advance into the leg-3 interface-surface spec (SO-1).

## Objectives

### 1. Scaffold the `canvas_context` sibling package
- **Status**: completed
- **Description**: Mirror the `canvas_std` layout: `pyproject.toml` (hatchling; pytest `pythonpath = ["src",
  "../canvas_std/src"]` — no install, firewall-safe), `README.md` / `AGENTS.md` / `CHANGELOG.md`, `src/canvas_context/`
  package skeleton, `tests/`. One-way dependency: `canvas_context → canvas_std`, never the reverse.
- **Files**: `what/code/canvas_context/**`

### 2. Implement model + loader (L1–L7) + resolver + traversal
- **Status**: completed
- **Description**: `model.py` (§3 dataclasses: `ContextGraph`, `Component`, `Panel`, `Relation`, `Ref`, `Surface`,
  `Conformance`); `loader.py` (`load_context_graph` — the normative L1–L7 pipeline; uses `canvas_std` public API
  `validate_suite`/`strip`/`compute_sync_hash` + `canvas_std.reserved` enums; cycle-safe); `resolver.py` (abstract
  `Resolver` + `DefaultPathResolver` in-vault wikilink; federation deferred to a descriptor); `traversal.py` /
  `ContextGraph` methods (§6 read-only primitives incl. the `reading_order` walk over `kind ∈ {reading_order,
  sequence}` from `isStartNode`). **`_reserved` lives at `metadata.frontmatter._reserved`.** **No rendering (L7).**
- **Files**: `what/code/canvas_context/src/canvas_context/*.py`

### 3. Tests + the load-without-rendering pilot (the leg-2 proof)
- **Status**: completed
- **Description**: `test_loader.py` (L1 refuses Core-invalid; L2 baseline on a stripped canvas; L3 additive overlay;
  L4 null-identity degradation; L5 ref classification; L6 staleness flag — incl. a computed-hash "not stale" case);
  `test_traversal.py` (`reading_order`/`neighbors`/`refs`/degradation); **`test_pilot.py`** — load the whitepaper
  `.canvas` as a `ContextGraph` **without rendering**: assert identity (`id` + `version`) resolved, `reading_order()`
  ordered from `page0`, 4 wikilink refs exposed, conformance reached, and **zero render invocation**.
- **Files**: `what/code/canvas_context/tests/*.py`

### 4. Firewall + regression + close
- **Status**: completed
- **Description**: `git status -s -- what/code/canvas_std/` clean; re-run the `canvas_std` suite green. Complete this
  mission (+AAR); campaign P2 row → completed (leg 2 PROVEN); STATE.md + campaign CLAUDE.md updated; **SITREP + HOLD at
  the P2→P3 gate**.
- **Files**: this mission (→ completed + AAR), campaign doc, campaign CLAUDE.md, STATE.md

## Campaign Context

### Previous Mission Outputs
- P1 ratified (2026-06-22): `spec_canvas_context_loading` — the binding leg-2 contract (L1–L7 + traversal + resolver +
  conformance + D6 forward-pointer), bounded by `adr_006`.

### Next Mission Inputs
- P3 (leg-3 interface-surface spec, greenfield) needs: leg 2 proven (this mission) + the `adr_006` boundary + the
  external OIP/interface thesis doc (risk-registered; P3 may defer if unavailable).

## Notes

`canvas_std` is **immutable** (firewall). The loader uses its **public API only** (`validate_suite`, `validate`,
`strip`, `degradation_report`, `compute_sync_hash`, `ConformanceLevel`) + `canvas_std.reserved` enums
(`COMPONENT_CLASSES`, `PL_EDGE_KINDS`). The spec is impl-agnostic; this sibling is one conformant realization that
**may fold into `canvas_std` later** at a deliberate Standard release (§10). No cross-surface routing, no federation
transport, no rendering (`adr_006` §2–§3 / spec §2).

## Completion Summary

Completed 2026-06-22. **Leg 2 PROVEN** — a canvas loads + traverses as a first-class context object without rendering.

### Deliverables
- `what/code/canvas_context/` — the leg-2 reference loader (new sibling, imports `canvas_std` read-only): `model.py`
  (§3 shapes), `loader.py` (the L1–L7 pipeline), `resolver.py` (`Resolver` + `DefaultPathResolver`), `traversal.py`
  (§6 reading-order walk + neighbors), plus `pyproject.toml` / `README.md` / `AGENTS.md` / `CHANGELOG.md` / `LICENSE`
  / `.gitignore`.
- Test suite **28 passed**, ruff clean: `test_loader` (L1–L7), `test_traversal` (reading_order/neighbors/cycle/
  fallback/containment), `test_resolver` (§5), **`test_pilot`** (the proof).
- **Pilot:** `canvas_standard_whitepaper.canvas` (32 nodes / 23 edges, adna_native) loads as a `ContextGraph` —
  identity `urn:adna:canvas:whitepaper:canvas-standard` v0.1.0, `reading_order() == [page0..page4]`, 4 wikilink refs,
  L3 overlay (`doc_root` → class `panel` / `document`), file node by reference — **no rendering** (PIL/cairosvg
  never imported). Second producer (`grant_proposal.canvas`) loads identically.
- **Firewall:** `canvas_std` git-diff 0; its suite still 82 passed / 10 skipped (no regression).

### Descoped
- Multi-canvas recursive resolution across vaults (the `_seen` cycle-safety hook is in place; cross-vault *fetch* is
  the federation layer's, out of scope per ADR-006). Federation transport remains a descriptor-only stub.

### Key Findings
- Drafting L1–L7 against the real `canvas_std` API + a real producer canvas paid off: the loader landed with **zero**
  spec rework. The only relaxation was `summary` (absent on the producer canvases → exposed as null, not an error).
- `reading_order()` on the whitepaper recovers the **page-level** document order (page0→…→page4) by walking the
  `sequence` chain; the in-page `reading_order` edges form content chains reachable via panel-scoped traversal. Both
  are spec-correct — reading order follows order-bearing edges, not containment.
- The golden fixtures carry a **placeholder** `sync_hash`, but real producer outputs carry a **correct** one — so the
  L6 staleness flag reads `True` on fixtures and `False` on the whitepaper. Good evidence the advisory check is live.

### Scope Changes
- None. Built within the P2 charter; HOLD at P2→P3 (no auto-advance into leg-3).

## AAR

- **Worked**: Spec-before-impl with a real-fixture anchor — the L1–L7 pipeline mapped 1:1 onto code; pilot green first try.
- **Didn't**: `canvas_std` is part of Canvas.aDNA's git (not a nested repo), so the charter's `git -C canvas_std diff`
  firewall check is misleading — corrected to the pathspec form `git status -s -- what/code/canvas_std/`.
- **Finding**: `_reserved` lives at `metadata.frontmatter._reserved`; pythonpath (not editable install) keeps the
  firewall provably clean (no `*.egg-info` written into the immutable tree).
- **Change**: record the pathspec firewall check in the campaign Standing Orders / verification (done at close).
- **Follow-up**: P3 — leg-3 interface-surface spec (greenfield; gated on the external OIP/interface thesis doc). The
  `canvas_context` sibling MAY fold into `canvas_std` at a future deliberate Standard release (spec §10).
