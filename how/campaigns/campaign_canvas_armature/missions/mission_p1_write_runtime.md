---
plan_id: mission_p1_write_runtime
type: plan
title: "P1 — Governed advisory-reverse write runtime + pilot"
owner: stanley
status: completed
campaign_id: campaign_canvas_armature
campaign_phase: 1
campaign_mission_number: 2
mission_class: build
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, armature, leg3, runtime, roundtrip, reconcile, p1]
---

# Mission: P1 — Governed advisory-reverse write runtime + pilot

**Campaign**: [[how/campaigns/campaign_canvas_armature/campaign_canvas_armature|campaign_canvas_armature]]
**Phase**: 1 — Governed round-trip write runtime (firewall-clean)
**Mission**: 2 of 4

## Goal

Promote the Salon POC's **view-only** `apply_response` into a **governed runtime** that closes the
`read → act → re-read` loop to the authoritative source (the `.lattice.yaml`) — **via the advisory reverse path**
([[../../../../what/specs/spec_roundtrip_protocol_v2|spec_roundtrip_protocol_v2]] §1.2/§5): a response advances the
*view*, and `reconcile()` produces a **reviewed source DRAFT**. The runtime **never** writes the authoritative source —
it emits a draft + a review payload + a staleness verdict; promoting a draft to authoritative is an explicit human
action. Built as a new `reconcile` module in `canvas_context` (D5), reusing `canvas_std.roundtrip`
(`merge`/`diff`/`to_canvas`/`from_canvas`/`compute_sync_hash`) **read-only** — the `canvas_std` firewall stays
git-diff 0 (D3 lifts it only at P2).

## Exit Gate

A response reconciles to a **reviewed** source draft via the advisory reverse path (no silent write); the runtime
restores the §6 lossy fields, surfaces the interaction response log + topology delta + merge conflicts + a staleness
verdict, and **leaves the on-disk source byte-unchanged** (asserted by a test); a runnable pilot demonstrates the loop
end-to-end; `canvas_context` tests green; `ruff` clean; **`canvas_std` firewall git-diff 0**. **HOLD at the P1→P2 gate.**

## Design (carried from the approved plan + the P1 study)

- **`reconcile(view, source) → Reconciliation`** — the governed advisory reverse:
  1. **staleness gate** (§3.2): the view's stored `_reserved.sync.sync_hash` vs `compute_sync_hash(source)` — warns if
     the source changed since the view was generated;
  2. **topology delta** (§5 step 3): `diff(to_canvas(source), view)` — what the view changed vs the source's canonical view;
  3. **merged source draft** (§5 step 4): `merge(source, view, strategy="yaml_wins")` — three-way merge + flagged conflicts;
  4. **restore §6 lossy fields** (§5 step 5, §6): `config`/`data_mapping`/`port`/`execution`/`fair`/`federation` restored
     from the current source onto the draft (the step `merge`/`from_canvas` deliberately drop) — mark `_draft: True`;
  5. **surface the interaction responses** — the participant's submitted values, surfaced for review, **never written to source**.
- **`governed_apply(view, source, affordance_id, value, …) → (advanced_view, Reconciliation)`** — the governed *act*:
  `apply_response` (advance the view, append-only) **then** `reconcile`. Writes nothing to disk.
- **`write_source_draft(recon, path, *, reviewed_by=None) → Path`** — writes the draft to a **separate** path
  (e.g. `<source>.draft.json`), **never** the authoritative source; stamps `reviewed_by` when a human has reviewed
  (the §1.2 human-review gate). Authoritative promotion is an explicit action outside the runtime.
- **Firewall:** `canvas_std` imported read-only (public API + `roundtrip`); the dependency stays one-way
  (`canvas_context → canvas_std`); no editable install (pythonpath only).
- **Serialization boundary:** the runtime takes the **parsed** source dict (the production `.lattice.yaml` is parsed by
  the caller — `canvas_context` stays stdlib-only, no YAML dep), mirroring how `load_context_graph` takes a parsed canvas.

## Objectives

### 1. Build the reconcile runtime
- **Status**: completed
- **Description**: `what/code/canvas_context/src/canvas_context/reconcile.py` — `Reconciliation` dataclass +
  `reconcile` / `governed_apply` / `write_source_draft` + the §6 lossy-field restore. Export from `__init__` (bump
  `canvas_context` 0.2.0 → 0.3.0). Reuse `canvas_std.roundtrip` + `canvas_context.interaction.apply_response`.
- **Files**: `src/canvas_context/reconcile.py`, `src/canvas_context/__init__.py`, `CHANGELOG.md`
- **Depends on**: P0 ratification

### 2. Source fixture + tests
- **Status**: completed
- **Description**: a `review_request.source.json` fixture (the roundtrip source contract + §6 lossy fields) whose
  topology matches `interaction_review.canvas` (so `sync_hash` aligns), via a `_build_review_source.py` generator that
  asserts the hash match. `test_reconcile.py` — the headline **source-byte-unchanged** test, the `_draft`/`requires_review`
  marking, lossy-field restoration, response surfacing, the staleness gate (mutate the source → `stale=True`), and
  round-trip-to-baseline (`is_round_trip_safe`).
- **Files**: `tests/fixtures/_build_review_source.py`, `tests/fixtures/review_request.source.json`, `tests/test_reconcile.py`
- **Depends on**: 1

### 3. Pilot + verify
- **Status**: completed
- **Description**: `pilot_governed_write.py` — the loop end-to-end (operator annotates → agent re-reads as context →
  responds → a reviewed source draft is emitted; the authoritative source unchanged). Verify: `canvas_context` pytest
  green, `ruff` clean, `canvas_std` firewall git-diff 0.
- **Files**: `tests/pilot_governed_write.py`
- **Depends on**: 2

## Notes

The governed write is **governed because it is advisory** — `spec_roundtrip_protocol_v2 §1.2` forbids silent source
propagation, so the runtime's whole job is to make the reverse path *safe + reviewable*: a draft, a delta, a staleness
warning, a conflict list — never a silent mutation. The biggest reuse win is that `merge`/`diff`/`to_canvas` already
exist in `canvas_std.roundtrip`; P1 adds the **governance layer** the reference round-trip left for "a higher layer"
(the §6 lossy-field restore + the never-touch-source discipline + the interaction-response review payload). **Do not
touch `canvas_std`** — the firewall holds until P2.

## Completion Summary

Completed 2026-06-22 (`session_stanley_20260622_193153_armature_scaffold_p0`, continued through P0 ratification into the
P1 build). The governed advisory-reverse write runtime is built + green; the `canvas_std` firewall held git-diff 0
throughout (the P2 lift is `adr_007`'s, not P1's).

### Deliverables
- **`reconcile.py`** (`canvas_context` 0.2.0 → **0.3.0**) — `reconcile` / `governed_apply` / `write_source_draft` +
  `Reconciliation` + the §6 lossy-field restore, all over `canvas_std.roundtrip` (read-only). Exported from `__init__`.
- **`review_request.source.json`** (+ `_build_review_source.py`) — the authoritative source paired with
  `interaction_review.canvas` (topology-matched; `sync_hash` aligned, verified by the generator).
- **`test_reconcile.py`** — 8 tests incl. the headline **source-byte-unchanged** guarantee, lossy restoration, the
  staleness gate, response surfacing, round-trip-to-baseline, and input purity.
- **`pilot_governed_write.py`** — the runnable governed loop (read → act → reconcile → reviewed draft; source
  byte-unchanged); the generated draft output is gitignored (the `interaction_review_after.canvas` precedent).
- **Verified:** `canvas_context` **58 passed** (50 + 8 new); `ruff` clean; `canvas_std` **82/10 unchanged**; **firewall
  `git status -s -- what/code/canvas_std/` git-diff 0**; pilot closes the loop with the authoritative source byte-unchanged.

### Descoped (→ P2, per `adr_007`)
- Wiring `I-*` into the `canvas_std` harness + the `interaction_version 1.0` Standard-version cut (the firewall touch).
- YAML parsing of a real `.lattice.yaml` — the runtime takes a parsed source dict (stdlib-only; the caller parses), so
  a JSON source fixture stands in (serialization boundary documented in `reconcile.py`).

### Key Findings
- **"Governed" = "advisory done safely."** `spec_roundtrip_protocol_v2 §1.2` forbids a silent source write, so the
  runtime's whole value is making the reverse path *reviewable*: a draft + delta + staleness + conflicts + the response
  payload, with the on-disk source provably byte-unchanged. The honesty the POC bought with a view-only fold, the
  runtime keeps with a review gate.
- **The reuse line fell exactly where the spec drew it.** `merge`/`diff`/`to_canvas` already do the topology work;
  the genuine gap `roundtrip.py` left to "a higher layer" was the **§6 lossy-field restoration** (top-level
  `fair`/`federation`/`execution` that `merge` drops) + the governance discipline — which is precisely what `reconcile`
  adds, no core algorithm rebuilt.

### Scope Changes
- The custom per-node `semantic_type` was dropped from the source fixture (it read as 4 spurious merge conflicts the
  view can't round-trip) — out of scope for the P1 happy path; conflict-flagging stays `merge`'s own tested contract.

## AAR

- **Worked**: building the governed write as a thin governance layer over `canvas_std.roundtrip` — `reconcile` is glue (staleness gate + §6 restore + review payload), not a new engine; green first integration, firewall untouched.
- **Didn't**: the first source fixture gave nodes custom `semantic_type`s the canvas can't round-trip → 4 spurious merge conflicts; dropped them for a clean happy path (conflict-flagging remains demonstrated by `merge`'s own tests).
- **Finding**: the spec's "advisory reverse" (§1.2) makes the headline test trivial to state and strong to hold — *the authoritative source is byte-unchanged* — which is exactly the property a leg-3 runtime must never violate.
- **Change**: keep the runtime serialization-agnostic (takes a parsed source dict; caller parses YAML) so `canvas_context` stays stdlib-only — documented as the boundary, mirrors how the loader takes a parsed canvas.
- **Follow-up**: P2 — the `adr_007` firewall touch (wire `I-*` into `canvas_std/validate.py` + cut `interaction_version 1.0` into Standard v2.2.0); **HELD at the P1→P2 gate** for operator approval.
