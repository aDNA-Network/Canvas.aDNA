---
type: context
created: 2026-06-20
updated: 2026-06-20
status: active
last_edited_by: agent_stanley
tags: [context, migration, parity, regression, validation, methodology, keystone, graduation]
---

# Migration Parity Methodology

Durable methodology graduated from Operation Keystone (E3.3 + E6.1/E6.2) — the technique that let every producer
migration cut over **without an LLM in the loop** and without trusting a re-scored render. Use it for any future
producer migration: the immediate consumer is the **PT P5 `canvas_core` relocation** (move
`canvas_core` → `Canvas.aDNA/what/production/canvas_core/`, [[adr_004_production_code_layout]]), but the method
generalizes to any vault that absorbs, relocates, or re-floors a code producer.

The question a migration must answer is narrow: **did the deliverable's *output* change?** Answer it with a
deterministic structural proof, not a subjective re-review.

## 1. The deterministic structural-parity proof

Reference implementation: [[e3_3_parity_check]] (`how/campaigns/campaign_canvas_genesis/missions/artifacts/e3_3_parity_check.py`),
re-run verbatim at E6.1. The shape:

1. **Rebuild the artifact through the migrated path** (e.g. the shimmed `canvas_core` floor) — exercise the real
   generation code (`PresentationBuilder → CanvasBuilder`, the `TYPE_MAPPING` / `EDGE_TYPE_MAPPING` / `VALID_*`
   tables), not a fixture.
2. **Normalize away the volatile parts** so the hash captures *only* structural essence:
   - drop each node's random `id` (`secrets.token_hex`); sort nodes by canonical `json.dumps(body, sort_keys=True)`;
     build an id-remap and rewrite edge `fromNode`/`toNode` to the canonical `n0, n1, …`; sort edges the same way.
   - drop **all** top-level keys (metadata, `_reserved` sync hashes, timestamps) — anything date- or run-volatile.
3. **SHA-256 the normalized structure** → `deck_norm_sha256`. The load-bearing field.
4. **Toggle the migration and compare:** run shim-ON vs shim-OFF (or old-path vs new-path). **Identical SHA ⇒ the
   change is output-neutral.** No model, no API, no re-score — a byte-deterministic proof.

**Corroborating invariants** (cheap, catch what a single hash can't localize):
- a **fingerprint** — the sorted sets of `node_types` / `colors` / `shapes` — must match the committed reference;
- a **floor-rejects** sweep — every node's `type`/`color`/`shape` is accepted by the migrated
  `CanvasBuilder.VALID_*` frozensets (expect `[]`); proves the new floor accepts every real reference value.

**Never touch the locked baseline.** The visual-quality baseline (CanvasForge `baseline_vr_scores.json`,
SHA `3ce4d341…`) is read-only and orthogonal — structural parity carries the VR scores by construction, so the
locked scores are *verified unchanged*, never recomputed.

## 2. When a SHA differs, run it down — don't wave it, don't panic

At E6.1 the `deck_norm_sha256` drifted from the E3.3 capture (`aa675665…` → `0d741640…`). The disciplined response
isolated it instead of either ignoring it or declaring regression. The elimination ladder:

- **Date volatility?** No date-like strings in any node body.
- **Within-process nondeterminism?** Two rebuilds in one process are byte-identical.
- **Hash-seed nondeterminism?** SHA stable across `PYTHONHASHSEED ∈ {0,1,2,42}`.
- **A real deliverable change?** No — `canvas_std/src` git-frozen since E0.2; `canvas_core` frozen since E3.2;
  working trees clean.

**Root cause:** diffing today's rebuild against the **committed reference deck** showed exactly **1 of 56 node
bodies** differed — and only in an embedded **absolute image path** (see §3). 55/56 byte-identical, fingerprint
identical, counts identical, 0 floor rejects ⇒ structurally reproduced; only a machine/location-specific string moved.

> **AAR correction (carry this forward):** compare against the **committed locked reference** (path-robust), not a
> prior-capture SHA. A capture-to-capture SHA diff conflates a real regression with an environment artifact; a
> capture-to-committed-golden diff *localizes* the differing node so you can root-cause it in one read.

## 3. Relocation pitfalls (the two that bit Keystone)

Both surfaced only at validation, both root-caused to the pt09 archive move (CanvasForge → `Archive.aDNA/`), neither
implicating `canvas_std`. Expect them in any relocation:

- **Absolute paths embedded in output are non-portable.** The old deck builder emits `Path(...).resolve()` absolute
  asset paths, so the embedded `file` string is machine- *and* location-specific. Relocating the vault (or building
  on a different machine — the committed ref was built on `/Users/herb/…`) changes that one string and the SHA with
  it, even though the rendered image is identical. **Lesson:** emit **relative or content-hash-keyed** asset
  references; flag absolute-path embedding as a portability nit. (PT P5 re-baselines `deck_norm_sha256` at the new
  resident path and notes this on the deck builder.)
- **Path resolution relative to a movable producer location is fragile.** `test_federation_validation.py` resolves
  consumer-wrapper lattice paths *relative to the producer's own location*; relocating the producer under
  `Archive.aDNA/` made all 55 cases `FileNotFoundError` (looking under `…/Archive.aDNA/ScienceStanley.aDNA/…`). This
  is **wiring, not regression** — repointing the ~8 wrappers (PT P5 / E5.2) turns them green. **Lesson:** resolve
  sibling-vault paths from a stable workspace anchor, not from a relocatable `__file__`.

## 4. The KEEP-floor-vs-federation split (don't conflate)

A migration touches two distinct layers; validate and report them separately:

| Layer | Question | How proven | Keystone result |
|-------|----------|-----------|-----------------|
| **KEEP floor** (the deliverable: `canvas_core` consuming `canvas_std` under the shim) | *Did the output regress?* | §1 deterministic proof + the owning suites | GREEN — 835/3 floor; 0 floor rejects; SHA reproduced |
| **Federation-integration** (consumer-wrapper lattice wiring) | *Is the downstream wiring connected?* | integration tests in the real environment | RED, **honestly deferred** to PT P5 (relocation-induced, not a Standard defect) |

The discipline: a federation/wiring red is **not** a deliverable regression. Keystone confirmed cutover at the
floor/Standard level and recorded the federation layer as PT-P5-deferred rather than green-washing it
([[e6_2_cutover_confirmation]] §3). Report the split explicitly; a single "tests red" headline would have falsely
implicated the shipped Standard.

## Cross-references
- Proofs: [[e3_3_parity_check]] (the script) · [[e6_1_parity_report]] (the run-down + relocation root-cause) ·
  [[e6_2_cutover_confirmation]] (floor-vs-federation split + shim schedule) ·
  [[e6_3_handoff_register]] §D (this guide's graduation candidate).
- Governance: [[adr_004_production_code_layout]] (the PT P5 relocation that will exercise this) ·
  [[campaign_canvas_genesis|Operation Keystone]] §Campaign AAR.
