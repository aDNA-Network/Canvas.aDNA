---
plan_id: mission_p2_firewall_touch_version_cut
type: plan
title: "P2 — I-* into the canvas_std harness + interaction_version 1.0 Standard-version cut"
owner: stanley
status: completed
campaign_id: campaign_canvas_armature
campaign_phase: 2
campaign_mission_number: 3
mission_class: build-with-firewall-touch
created: 2026-06-23
updated: 2026-06-23
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, armature, leg3, firewall, conformance, interaction, versioning, p2]
---

# Mission: P2 — I-* into the harness + interaction_version Standard-version cut

**Campaign**: [[how/campaigns/campaign_canvas_armature/campaign_canvas_armature|campaign_canvas_armature]]
**Phase**: 2 — Firewall touch (per ratified [[../../../../what/decisions/adr_007_leg3_firewall_touch|adr_007]])
**Mission**: 3 of 4

## Goal

The **first deliberate edit to `canvas_std` since Operation Keystone** — bounded to the two purposes `adr_007` §1
authorizes, no more: (1) **wire `I-1/I-2/I-3` into the `canvas_std` validator** so an interaction-bearing canvas
validates natively through the `canvas-std` CLI (not just consumer code), and (2) **cut `interaction_version 1.0` into
Standard v2.2.0**. The consumer's `validate_interaction_block` becomes a **thin delegate** to the harness (one source of
truth). Crossed the **P1→P2 gate** only on the operator's explicit approval (2026-06-23).

## Exit Gate (per `adr_007` §3 — full regression replaces git-diff 0)

`I-1/I-2/I-3` validate natively through the `canvas-std` CLI on an interaction-bearing golden; `interaction_version 1.0`
is cut into Standard **v2.2.0**; **D-1..D-3 still prove round-trip-to-baseline** on that golden (the interaction layer
stays additive — strip removes all `_reserved` incl. `interaction` → still a valid Core/Extended canvas); **full
regression green**: `canvas_std` (82/10 + new I-* rows + golden) + `canvas_context` (58, now delegating) + 7 producers
(305) ; `ruff` clean. **HOLD at the P2→P3 gate.**

## Design (carried from the approved plan + the P2 study)

Land the logic first behind the existing 2.0.2 tests (prove no regression), then cut the version atomically.

- **`canvas_std.reserved.validate_interaction(reserved, doc)`** (NEW) — realizes I-1/I-2/I-3 over
  `_reserved.interaction`, **doc-path only** (never imports `ContextGraph` — the firewall is one-way). Ported from the
  consumer's `validate_interaction_block` **minus** the `validate_anchors` re-call (R1: `validate_reserved` already runs
  it on the same aDNA-Native branch — re-calling would double-emit A-5) and **minus** the graph path. Uses a dedicated
  2-part-tolerant interaction semver regex (R3: `reserved._SEMVER` is 3-part; `interaction_version` is `"1.0"`).
- **`canvas_std.validate`** — dispatch `errors += reserved.validate_interaction(reserved_block, doc)` in the
  ADNA_NATIVE branch, right after `validate_reserved`. `validate_suite` + the CLI both call `validate()`, so I-* surfaces
  through them with no further wiring.
- **`canvas_std.__init__`** — re-export `validate_interaction`; add to `__all__`.
- **golden** — `tests/fixtures/adna_interaction.canvas` (copied from the proven `canvas_context` interaction fixture —
  all four affordance kinds; `adna_version` normalized to the canvas_std corpus's `2.0.0`) + a `manifest.json` row
  (adna_native / valid / degrades_to extended) + `tests/test_interaction.py` (valid e2e; orphan affordance → I-2; bad
  response value → I-3; strip → Core valid (D-1); CLI exit 0 on the golden, 1 on an orphan variant).
- **consumer delegate** — `canvas_context.validate_interaction_block(doc, graph=None)` body → `return
  validate_interaction(_reserved(doc), doc)` (preserve the `graph` param; keep `InteractionSurface.validate_interaction`
  + `apply_response`'s `_value_kind_errors`). The 58 stay green: no consumer test relies on the dropped `validate_anchors`
  output, and the well-formed fixture resolves `status_marker` via `panel_link.anchors` (doc path == graph path).
- **version cut v2.0.2 → v2.2.0** (every site the v2.0.1/v2.0.2 cuts established — `lip_queue_disposition.md` §Release
  packaging): `__init__.STANDARD_VERSION` · schema `title` + `x-standard-version` (keep `$id`) · `conformance.py` (×3) ·
  `test_smoke.py` (×2) + `test_conformance.py` (×1) · all `what/specs/spec_*.md` `standard_version` frontmatters +
  the `spec_federation_contract` example · `canvas_std/CHANGELOG.md` [2.2.0]. **Fixtures' `adna_version` untouched**
  (a 2.0.0 canvas stays valid under 2.2.0 — why producers don't regress, R5). v2.1.0 reserved for in-review LIP-0008.
- **forward-pointer flips** — `spec_conformance_suite §4.1` + `spec_interface_surface §10` (+ §9.1 note + status block):
  "forward-pointed" → "implemented in `canvas_std` (Armature P2)".

## Objectives

### 1. Wire I-* into canvas_std (no version change)
- **Status**: completed
- **Files**: `canvas_std/src/canvas_std/{reserved,validate,__init__}.py`, `canvas_std/tests/fixtures/adna_interaction.canvas`, `canvas_std/tests/fixtures/manifest.json`, `canvas_std/tests/test_interaction.py`
- **Verify**: `canvas_std` pytest green (~88-90), still v2.0.2.

### 2. Consumer delegate
- **Status**: completed
- **Files**: `canvas_context/src/canvas_context/interaction.py`
- **Verify**: `canvas_context` 58 green; 7 producers green.

### 3. The version cut + forward-pointer flips
- **Status**: completed
- **Files**: the bump sites above + `spec_conformance_suite.md`, `spec_interface_surface.md`
- **Verify**: full regression green at v2.2.0; CLI validates the golden.

## Notes

`adr_007` is the binding instrument: the touch is **isolated to this phase + two purposes**, the boundary of `adr_006`
is unchanged (no rendering/capture/transport/routing enters `canvas_std`). The git-diff-0 firewall check is replaced by
full-regression-green **for P2 only**; P3 returns to git-diff 0. Push is operator-gated (Git-Ops §3).

## Completion Summary

Completed 2026-06-23 (`session_stanley_20260623_105436_armature_p2_firewall_touch`). The **first deliberate `canvas_std`
edit since Operation Keystone** is done + green, bounded to `adr_007`'s two purposes.

### Deliverables
- **`canvas_std.reserved.validate_interaction(reserved, doc)`** — the `I-1`/`I-2`/`I-3` family (doc-path only; a
  2-part-tolerant `_INTERACTION_SEMVER`; reuses the node/anchor substrate `validate_reserved` builds and does **not**
  re-run `validate_anchors` — no double A-5). Dispatched on the aDNA-Native `validate()` path (after `validate_reserved`);
  surfaces through `validate_suite` + the `canvas-std` CLI; re-exported from `__init__`.
- **`tests/fixtures/adna_interaction.canvas`** (4 affordance kinds; one label-anchored) + manifest row + **`tests/test_interaction.py`**
  (16 tests: valid e2e · I-2 orphan · I-3 bad value · D-1 strip→Core · the **no-double-A-5** R1 guard · CLI 0/1).
- **`canvas_context.validate_interaction_block` → thin delegate** to `canvas_std.validate_interaction` (dropped the
  duplicated logic + the dead `_SEMVER`/`re`; kept `AFFORDANCE_KINDS` + the act-time `_value_kind_errors` for
  `apply_response`); `canvas_context` **0.3.0 → 0.3.1**.
- **Standard v2.2.0 cut** — `2.0.2 → 2.2.0` at `STANDARD_VERSION` · schema `title` + `x-standard-version` (**kept `$id`**)
  · `conformance.py` ×3 · `test_smoke` ×2 + `test_conformance` ×1 · the 9 spec frontmatters + the `spec_federation_contract`
  example · both CHANGELOGs. Forward-pointers flipped: `spec_conformance_suite §4.1` + `spec_interface_surface §9.1/§10`
  (+ status block + Q7) "forward-pointed/deferred" → "implemented in `canvas_std`". **v2.1.0 reserved for LIP-0008.**
- **Verified (P2 exit gate = full regression, `adr_007` §3):** `canvas_std` **105/10** · `canvas_context` **58** · 7
  producers **223** · D-1..D-3 on the interaction golden · `canvas-std 2.2.0` CLI → golden `adna_native [OK]`; `ruff` clean
  both. Firewall touch **+159/−9 across 9 files** (logic = `reserved.py` +108 + 1 dispatch line) — minimal + reviewable.

### Scope notes / deviations
- Bumped `canvas_context.STANDARD_VERSION → 2.2.0` + package `0.3.1` (the plan flagged this optional; done for vault-wide
  version coherence + to mark the delegate refactor).
- **Did not** add `x-interaction-version` to the schema (ADR-007 §1.2 names only `x-standard-version`; stayed minimal).
- Fixtures' `_reserved.adna_version` left at `2.0.0` (additive layer; why producers don't regress).

### Pre-existing finding (→ P3 doc currency)
- The `canvas_std` CHANGELOG had **no `[2.0.2]` entry** (the AT-1/AT-2 errata cut bumped version strings only). The new
  `[2.2.0]` entry bridges explicitly from 2.0.2; a back-fill `[2.0.2]` note is a P3 doc-currency candidate.

## AAR

- **Worked**: the touch fell exactly where `adr_007` scoped it — `validate_interaction` is a pure additive function + a
  one-line dispatch; landing the logic behind the existing 2.0.2 tests first (105 green, still 2.0.2) proved no regression
  before the version cut, so the cut was a clean mechanical pass. Firewall diff stayed +159/−9, fully reviewable.
- **Didn't**: nothing failed; the one judgment call was the consumer delegate — the pure delegate (drop `validate_anchors`
  from `validate_interaction_block`) held all 58 green because no test relied on that A-5 emission and the well-formed
  fixture resolves its label anchor via the doc path (graph path == doc path).
- **Finding**: keeping `validate_interaction` from re-running `validate_anchors` (R1) was the load-bearing correctness
  call — `validate_reserved` already runs it on the same branch, so a re-call would double-emit A-5; a dedicated test
  (`test_anchor_orphan_emits_a_single_a5_not_duplicated`) locks it.
- **Change**: bumped the consumer's `STANDARD_VERSION`/package version (beyond the plan's "optional, leave") for vault
  coherence — cheap, test-safe, and it documents the delegate.
- **Follow-up**: P3 — cross-suite sweep · structural `iii/` review of the P1 runtime + the P2 harness touch · Campaign AAR
  + Completion Summary · doc currency (incl. the missing `[2.0.2]` CHANGELOG back-fill) · mark
  `idea_campaign_leg3_interface_runtime` `implemented` · file the OIP `v1.x` re-anchor stub. **HELD at the P2→P3 gate.**
