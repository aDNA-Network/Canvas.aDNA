---
type: review
created: 2026-06-23
updated: 2026-06-23
status: active
last_edited_by: agent_stanley
reviewer: iii (structural)
campaign: campaign_canvas_armature
scope: structural
tags: [iii, review, canvas, armature, leg3, runtime, firewall, interaction, structural]
---

# III structural review — Operation Armature leg-3 runtime (P1 governed write + P2 firewall touch)

Structural review of the Armature **code** deliverables via the `iii/` wrapper (III.aDNA v0.5.0). Unlike the prior
reviews (canvas *output* artifacts), the subject here is **Python design** — the leg-3 governed-write runtime (P1) and
the first `canvas_std` harness touch (P2). The **VR1–VR5 / pixel CV-\*** visual schema is therefore **not applicable**
(no `.canvas` output is produced); the 5-lens panel applies structurally (design soundness · rigor of the
claims/tests · boundary adherence · code clarity · claim-to-code provenance). Consistent with the Palette/Atelier
reviews' structural-vs-pixel split.

## Artifacts reviewed
- `what/code/canvas_context/src/canvas_context/reconcile.py` (P1) — `reconcile` / `governed_apply` / `write_source_draft`
  + `Reconciliation` (the advisory-reverse governed write over `canvas_std.roundtrip`, read-only).
- `what/code/canvas_std/src/canvas_std/reserved.py::validate_interaction` (P2) — the `I-1`/`I-2`/`I-3` family + the
  `validate.py` dispatch + the `__init__` re-export (the bounded firewall touch under `adr_007`).
- `what/code/canvas_context/src/canvas_context/interaction.py::validate_interaction_block` (P2) — the thin delegate.
- Tests + pilot: `canvas_std/tests/test_interaction.py` (16) + `adna_interaction.canvas`; `canvas_context/tests/test_reconcile.py` (8) + `pilot_governed_write.py`.

## Findings

**0 High · 0 Med.**

Lows / notes (non-blocking):
- **L1** — `AFFORDANCE_KINDS` is now declared in **both** `canvas_std.reserved` and `canvas_context.interaction`
  (constant duplication, not logic). Latent divergence risk if the closed enum ever changes; mitigated by the spec
  pinning it (§3.3) and a test in each tree asserting the tuple. Accept; a future re-source of the consumer's copy from
  `canvas_std` is optional. No action.
- **L2** — the value↔kind check lives in two places: `canvas_std.reserved._interaction_value_kind_errors` (conformance,
  I-3) and `canvas_context.interaction._value_kind_errors` (the **act-time** guard `apply_response` raises on). Same
  logic, different call sites (conformance vs reducer-input guard) — defensible, but a consolidation candidate if a
  third caller appears. No action.
- **L3** — `canvas_std/CHANGELOG.md` had **no `[2.0.2]` entry** (the AT-1/AT-2 errata cut bumped version strings only);
  the new `[2.2.0]` entry bridges explicitly from 2.0.2. The back-fill is a `canvas_std` edit and is **firewall-gated
  out of P3** (P0/P1/P3 hold git-diff 0) → a future editorial PATCH (v2.0.x errata or the next firewall touch). Recorded,
  not done here.

## Structural checks (design · boundary · tests)
- **Boundary (ADR-006) unchanged** — the P2 touch adds only a conformance check + a version cut; **no** rendering,
  capture, transport, or cross-surface router enters `canvas_std`. The firewall touch is **+159/−9 across 9 files**
  (logic = `validate_interaction` +108 + a 1-line dispatch) — minimal and reviewable.
- **One-way dependency held** — `canvas_std` never imports `ContextGraph`; `validate_interaction` resolves anchors via
  the **doc path** only (`panel_link.anchors`), so the consumer→Standard direction is preserved.
- **No double-validation (R1)** — `validate_interaction` does I-1/I-2/I-3 only; it does **not** re-run `validate_anchors`
  (which `validate_reserved` already runs on the same aDNA-Native branch). Locked by
  `test_anchor_orphan_emits_a_single_a5_not_duplicated`.
- **Governed write is advisory (P1)** — a response advances the *view*; `reconcile` emits a `_draft`/`requires_review`
  source draft and **never** writes the authoritative source (a test asserts the on-disk source is byte-unchanged).
  `spec_roundtrip_protocol_v2 §1.2` honored.
- **Round-trip-to-baseline holds (D-1..D-3)** — `strip(adna_interaction.canvas)` removes all `_reserved` incl.
  `interaction` and still validates at Core/Extended; the interaction layer stays **additive** (no baseline overload).
- **One source of truth** — the consumer's `validate_interaction_block` is a thin delegate to
  `canvas_std.validate_interaction`; the duplicated I-1/I-2/I-3 logic was removed.
- **Regression-covered** — `canvas_std` **105/10** (+23 incl. `test_interaction.py` 16) · `canvas_context` **58** · 7
  producers **223** · `ruff` clean both · `canvas-std 2.2.0` CLI validates `adna_interaction.canvas` `[OK]`.
- **Firewall (P3)** — `git status -s -- what/code/canvas_std/` **clean** (git-diff 0 restored; the P2 lift was bounded
  to its phase + committed).

## ACCUMULATE
Local learning-store candidate (frequency 1; logged for future graduation, not yet canonical): **firewall-touch as a
bounded ADR** — lifting an immutable reference tree for one phase + two named purposes, swapping the git-diff-0 gate for
full-regression-green, keeps a "first-ever edit" small and reviewable. Canonical III store untouched (read-only from the
consumer per ADR-003 §2).

## Verdict
**SHIP.** The leg-3 governed-write runtime (P1) and the `I-*` harness touch + v2.2.0 cut (P2) are structurally sound,
boundary-respecting, and fully regression-covered — **0 High / 0 Med**; three non-blocking Lows (one a pre-existing
doc gap). Pixel/visual review is **not applicable** (code, not canvas output) and the PT-P5 render-scoring track is
untouched.
