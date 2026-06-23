---
plan_id: mission_p4_interaction_poc
type: plan
title: "P4 — Minimal canvas-native interaction loop (leg-3 POC, stretch)"
owner: stanley
status: completed
campaign_id: campaign_canvas_salon
campaign_phase: 4
campaign_mission_number: 5
mission_class: proof_of_concept
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, salon, surface, interface, leg3, p4, poc, interaction]
---

# Mission: P4 — Minimal canvas-native interaction loop (leg-3 POC)

**Campaign**: [[how/campaigns/campaign_canvas_salon/campaign_canvas_salon|campaign_canvas_salon]]
**Phase**: 4 — Leg-3 proof-of-concept (stretch)
**Mission**: 5 of 6

## Goal

Turn leg 3 from *ratified-on-paper* into *proven-by-POC*: build the minimal, runnable `read → act → re-read` loop named
in the campaign — an operator annotates a canvas → an agent re-reads it **as context** (via the proven leg-2 loader, no
rendering) → responds → the surface state advances. Outcome: all three thesis legs not just specified but **exercised**.

## Operator decision (P3→P4 gate, plan-mode 2026-06-22)

At the P3→P4 gate ("P4 *or* P5 close — operator's call") the operator chose **build P4** (the stretch POC), and **HOLD
at the P4→P5 gate** afterward (close decided separately). Approved plan:
`~/.claude/plans/please-read-the-claude-md-goofy-whistle.md`.

## Exit Gate

A minimal interaction loop is **demonstrated** — load an interaction-bearing `.canvas`, read its affordances + surface
state, an agent responds, and the re-read surface state advances (the loop closes onto leg 2) — with the **`canvas_std`
firewall git-diff 0** and no leg-2 regression. **HOLD at the P4→P5 gate** (SO-1); never auto-advance into P5 close. The
mission completes (with AAR) when the loop is green + verified.

## Binding scope (spec_interface_surface §10.2 + ADR-006)

- Reader **extends `canvas_context` read-only** (`affordances()` / `surface_state()` over the existing `ContextGraph`);
  **MUST NOT** become a capture runtime (ISS's boundary), a renderer, or a transport.
- **`canvas_std` firewall** (D6) — import only; `git status -s -- what/code/canvas_std/` clean at the gate.
- Rides additive `_reserved.interaction` only — no core-schema change; no canvas-as-primitive re-open (Δ2/LIP-0009).
- `apply_response` advances the **view** only (append-only, §7.2); the governed round-trip write (`.lattice.yaml`) is
  out of scope (`spec_roundtrip_protocol_v2`).

## Objectives

### 1. Build the interaction module (reader + reducer)
- **Status**: completed
- **Description**: new additive sibling `what/code/canvas_context/src/canvas_context/interaction.py` that **composes**
  the leg-2 `ContextGraph` (leg-2 code byte-unchanged). Reader: `load_interaction_surface()` + `InteractionSurface`
  (`affordances()` / `surface_state()` / `responses()` / `open_affordances()` / `validate_interaction()`), realizing
  spec §3.1 record shapes + I-1/I-2/I-3. Reducer: `apply_response()` — a pure append-only fold (recompute `state`) +
  `is_round_trip_safe()` (I-D, via `canvas_std.strip` + `validate`). Reuses `canvas_std.reserved.validate_anchors`
  read-only. Additive `__init__.py` exports.
- **Files**: `…/canvas_context/interaction.py`, `…/canvas_context/__init__.py`

### 2. Author the interaction-bearing golden fixture
- **Status**: completed
- **Description**: `…/tests/fixtures/interaction_review.canvas` — a small valid `adna_native` canvas with a
  `_reserved.interaction` overlay declaring **one affordance of each of the four kinds** (`input`/`choice`/`annotation`/
  `action`), anchored to real node ids + one via a `panel_link.anchors` label (both binding paths). Must validate
  `adna_native [OK]`; strip ⇒ valid baseline (I-D).
- **Files**: `…/tests/fixtures/interaction_review.canvas`

### 3. Tests + on-disk demo
- **Status**: completed
- **Description**: `test_interaction.py` (I-1/I-2/I-3), `test_interaction_loop.py` (the pilot proof: read → respond →
  re-read advances; no render libs imported), `test_interaction_degradation.py` (I-D round-trip-to-baseline);
  `pilot_interaction_loop.py` (`__main__` demo: operator annotates → agent re-reads → responds, runnable end-to-end).
- **Files**: `…/tests/test_interaction.py`, `…/tests/test_interaction_loop.py`,
  `…/tests/test_interaction_degradation.py`, `…/tests/pilot_interaction_loop.py`

### 4. Verify + governance currency + HOLD
- **Status**: completed
- **Description**: new + existing `canvas_context` suite green (28 leg-2 + new); `canvas_std` 82/10 unchanged; fixture
  validates; ruff clean; **firewall git-diff 0**; CHANGELOG + AGENTS index the module; campaign master P4 row →
  completed; CLAUDE/STATE current; SITREP + 5-line AAR. **HOLD at the P4→P5 gate.**
- **Files**: `…/CHANGELOG.md`, `…/AGENTS.md`, `campaign_canvas_salon.md`, `campaign_canvas_salon/CLAUDE.md`, `STATE.md`,
  this mission (→ completed + AAR)

## Campaign Context

### Previous Mission Outputs
- P3 completed (2026-06-22): leg-3 **ratified** (`spec_interface_surface.md`); `I-*` family folded into
  `spec_conformance_suite.md §4.1` (validator forward-pointed — this mission is its first code realization).
- P2 completed: leg-2 `canvas_context` loader (28/28) — the `read` step + the `ContextGraph` a surface-state *is*.

### Next Mission Inputs
- P5 (close) needs P2 + P3 (+ this P4 if taken): Completion Summary + Campaign AAR + follow-on leg-3-build charter.

## Notes

- **Reuse, don't reinvent**: read step = `load_context_graph`; anchor resolution over `ContextGraph.anchors()` +
  `.component()`; I-D = `canvas_std.strip` + `validate`; I-2 reuses `validate_anchors`. The no-render assertion copies
  the leg-2 pilot (`PIL`/`cairosvg` never enter `sys.modules`).
- **Append-only / view-only**: `apply_response` never mutates/deletes a logged response, never writes `.lattice.yaml`.
- **First code realization of `I-*`** — housed in the consumer (`canvas_context`), NOT wired into the `canvas_std`
  harness (firewall).

## Completion Summary

Completed 2026-06-22 (built + verified same session). **Leg 3 proven by POC** — the minimal `read → act → re-read`
loop runs live on the proven leg-2 loader, with `canvas_std` untouched. All three thesis legs are now **exercised**
(1 output + 2 context-object proven; 3 interface-surface ratified *and* demonstrated).

### Deliverables
- **`canvas_context/interaction.py`** (v0.2.0) — the leg-3 surface composing the leg-2 `ContextGraph`: reader
  (`load_interaction_surface` / `InteractionSurface` / `affordances()` / `surface_state()` / `validate_interaction`),
  reducer (`apply_response` — a pure append-only fold, IX5/IX6), and conformance (`validate_interaction_block` =
  I-1/I-2/I-3 reusing `validate_anchors`; `strip_interaction` §8.2 + `is_round_trip_safe` I-D reusing
  `canvas_std.strip`/`validate`). Additive `__init__` exports; leg-2 surface unchanged.
- **`tests/fixtures/interaction_review.canvas`** (+ self-validating generator) — interaction-bearing golden, one
  affordance of each of the 4 kinds, both anchor-binding forms; `canvas-std validate` → `adna_native [OK]` (D-1/D-2/D-3).
- **Tests (22 new):** `test_interaction.py` (I-1/I-2/I-3), `test_interaction_loop.py` (the loop proof + no-render
  assertion), `test_interaction_degradation.py` (I-D). **`pilot_interaction_loop.py`** — the runnable on-disk demo.
- Code currency: CHANGELOG `[0.2.0]`, AGENTS map, version bump. Governance currency: campaign master P4 → completed,
  campaign CLAUDE, STATE.

### Verified
- `canvas_context` **50 passed** (28 leg-2 + 22 leg-3); `canvas_std` **82/10 unchanged** (no regression); `ruff` clean;
  CLI `adna_native [OK]`; **firewall `git status -s -- what/code/canvas_std/` git-diff 0**.

### Descoped / deferred
- **Capture runtime / renderer / transport** — ADR-006 boundary (ISS / OIP / federation). The POC is read + a view-fold.
- **Governed round-trip write** (`.lattice.yaml` reconciliation) — `spec_roundtrip_protocol_v2` (§2); `apply_response`
  advances the view only.
- **`I-*` in the `canvas_std` harness + the formal Standard-version cut** — deferred (firewall; a deliberate release).
- **A full leg-3 runtime build** — follow-on charter (Salon P5).

### Key findings
- Framing the POC as **compose-not-extend** (an `InteractionSurface` *has-a* `ContextGraph`) kept the 28 leg-2 tests
  byte-unchanged and the firewall trivially clean — the spec's "accessors over the existing `ContextGraph`" is best met
  by composition, not by widening the `ContextGraph` constructor.
- The honest `read → act → re-read` demonstration needs a **write**, which leg-2 deliberately lacks; splitting it into a
  pure append-only **view-fold** (`apply_response`) — explicitly not a round-trip write and not a capture runtime — let
  the loop close end-to-end while staying inside the ADR-006 fence.
- `compute_sync_hash` is topology-only, so the interaction overlay (and later responses) never staleness the fixture —
  the golden stays `adna_native [OK]` across the whole loop.

### Scope changes
- None. Built within the P4 charter; **HOLD at the P4→P5 gate** (no auto-advance into close).

## AAR

- **Worked**: Composing the leg-3 surface over the proven leg-2 `ContextGraph` + a pure append-only fold made the
  greenfield POC land green (50/50) and firewall-clean (git-diff 0) in one session.
- **Didn't**: The spec's literal "read-only extension" wording undersells that an honest loop needs a write — resolved
  by a view-only fold (not a runtime), but it's a boundary the spec could name more sharply (→ a `v1.x` clarification).
- **Finding**: The `I-*` family realizes cleanly in the *consumer* by reusing `validate_anchors` + `strip`/`validate` —
  no `canvas_std` edit needed to prove conformance, vindicating the two-shelf firewall.
- **Change**: Generate interaction fixtures via a self-validating builder (asserts `adna_native` + I-* before writing) —
  caught zero defects because it caught them at author time; keep as the fixture pattern.
- **Follow-up**: P5 (close) — operator's call at the P4→P5 gate; a full leg-3 runtime build + wiring `I-*` into the
  `canvas_std` harness + the formal Standard-version cut ride a follow-on charter / deliberate release.
