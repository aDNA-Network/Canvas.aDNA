---
type: spec
spec_id: spec_rlhf_seam
title: "The RLHF seam — Canvas owns the capture substrate, III owns the signal schema (Lodestar R4.2)"
standard_version: "2.3.0"
interaction_version: "1.0"
status: proposed
created: 2026-08-09
updated: 2026-08-09
last_edited_by: agent_mondrian
phase: H6
campaign_id: campaign_canvas_halftone
audience: [mondrian, argus_panoptes, consumer-vault agents wiring a Canvas review surface]
resolves: "gap G6 — RLHF seam ownership undocumented; Lodestar R4.2 (C-ii)"
supersedes:
superseded_by:
tags: [spec, rlhf, seam, iii, interaction, schema_a, capture, signal, halftone, h6, lodestar]
---

# The RLHF Seam (Halftone H6)

> **What this is.** The ownership boundary between the two record systems a Canvas review surface writes to, and
> the routing rules across them. Authority: Lodestar **R4.2** (C-ii) · gap register **G6** · the ratified
> [[spec_canvas_review_surface]] (which this spec's §4 completes). Emitting code:
> `canvas_context/interaction.py` (`apply_response`, L228) · `canvas_core/rlhf/selection.py`
> (`SelectionRecord`, L40) · `canvas_core/rlhf/iii_bridge.py` (`selection_to_iii_signal` L132 ·
> `accumulate` L251) · `canvas_core/rlhf/review_collect.py` (the collector, the only writer of record).
>
> **Status `proposed`.** §7.7 ratification block at the foot; the operator signs. Nothing in §5 is built —
> this spec is written *before* its implementation deliberately (agents author, operators ratify).

## 1. The boundary (normative)

**Canvas owns the capture substrate. III owns the signal schema.**

| | Capture substrate | Signal schema |
|---|---|---|
| **Owner** | Canvas.aDNA (this vault) | III.aDNA (Argus Panoptes), via ADR-005 |
| **Question it answers** | *What did the reviewer do, and when?* | *What should the system learn from it?* |
| **Record** | `_reserved.interaction.responses[]` | an ADR-005 §2 learning-store signal |
| **Discipline** | append-only, immutable once logged (`interaction.py` L271 — an existing entry is never mutated or removed) | idempotent accumulate, deduped on the consumer-namespace `selection_id` (`iii_bridge.py` L251–275) |
| **Completeness** | **total** — every verdict, approve and reject alike | **selective** — only what carries evaluative meaning |
| **Lifetime** | the canvas is the record; it travels with the artifact | the store outlives any one canvas |

The two are not redundant. The capture substrate is a **provenance log** — it must be able to answer "who said
what about which variant on which turn" without interpretation. The signal store is an **interpretation** —
lossy by design, shaped by a schema Canvas does not own. Conflating them is what made this seam undocumented
for as long as it was: both are correctly called "the RLHF record", and they are different objects.

**The corollary that matters:** Canvas may never unilaterally change the ADR-005 signal shape, and III may never
require a change to `responses[]` semantics. Changes cross the seam as coordination, not as edits.

## 2. The three sinks — ground truth

The collector (`review_collect.py`) fans one operator verdict into three writes, in a fixed order
(canvas → Schema-A → III → ledger last, so a mid-run crash re-runs clean — review-surface spec §4.1):

1. **Canvas** — `apply_response()` appends to `_reserved.interaction.responses[]`. A pure, append-only fold on
   a deep copy. Topology is untouched, so `sync.sync_hash` never moves.
2. **Schema-A** — a `SelectionRecord` (`selection.py` L40) written to `what/artifacts/image_gen_dataset/`.
   **Structurally requires a pick**: it records *which variant won*. Absolute `image_path` values are a hard
   schema violation (L124, F-36).
3. **III** — `selection_to_iii_signal()` maps a Schema-A record to an ADR-005 §2 signal;
   `accumulate()` appends it to `how/federation/iii/what/context/canvas_iii_learning_store.jsonl`.

### 2a. The store is heterogeneous by design

The live learning store currently holds a `_meta` header line plus two **III learning-pattern** entries
(`CANVAS-L-001`, `CANVAS-L-002` — the `lens`/`pattern`/`proposed_fix`/`graduated` idiom). Canvas RLHF signals
are a *different shape* in the *same* JSONL. This is deliberate, and the discriminator is already implemented:
`_existing_selection_ids()` (L225) skips any line without a consumer-namespace `selection_id`, so pattern
entries are correctly ignored by the idempotency check rather than corrupting it.

**Normative:** a reader of this store MUST discriminate record classes by the presence of
`rlhf_consumer_namespace.canvasforge.image_generation.selection_id`, not by line position or file. A future
reader that assumes homogeneity is wrong about a store that has been mixed since it was repointed at HR.

## 3. The ISS-vs-III contradiction — resolved as a scope conflation

R4.2 recorded a contradiction: *the docs say ISS, the code routes III*. Both were right about different things.

- [[spec_interface_surface]] §2 (L81, L299) assigns "HTML rendering, RLHF schema, and the 4-tier round-trip" to
  **ISS** (`aDNA.aDNA`, ADR-006 §2 / `adr_028_iss_architecture`).
- `iii_bridge.py` routes canvas review signal to **III**.

These name two different objects that shared one word:

| Object | Owner | Scope |
|---|---|---|
| The **ISS gate's own** RLHF schema | ISS (`aDNA.aDNA`) | how an HTML gate runtime captures and round-trips *its* responses |
| The **evaluative signal schema** for canvas review | III (ADR-005) | what a review verdict means as a learning signal |

**Ruling:** no re-assignment is needed — the ISS wording is qualified in place (this spec's companion edit to
`spec_interface_surface.md` §2). ISS remains the sibling *surface* for flat rich-context gates; it is not, and
never was, the signal store for canvas review. The review-surface spec's non-goals already said as much
(§Non-goals: "ISS remains the sibling surface for flat rich-context gates"); this spec makes it normative.

## 4. Open decision #4 — reject routing (RULED)

### The actual gap

`RLHF_SIGNAL_TYPE_REJECT` has been **declared since the bridge was written** (`iii_bridge.py` L66, alongside
`DEFER` and `ACCEPT_WITH_MODIFICATION`) and is **never emitted** — L184 hard-codes `accept`. Combined with
Schema-A structurally requiring a pick, the consequence is concrete: **a reject-only review pass produces no
Schema-A record and therefore no III signal at all.** The rejection is durable in `responses[]` and the
sidecars, and invisible to every learning consumer.

This is the whole of open decision #4, and it is a real loss: "none of these six is acceptable" is a *stronger*
preference signal than "this one is best", and it is exactly the signal a generation pipeline needs.

### The ruling (operator, 2026-08-09)

**Both sinks, with the boundary of §1 enforced. III carries the signal.**

1. `responses[]` remains the **complete** record. Unchanged. Every verdict lands there, including rejects. This
   is already true and is now normative.
2. A reject **SHALL** produce an III signal of `rlhf_signal_type: reject`, using the constant already declared.
3. That signal is derived from **`responses[]`, not from Schema-A** — because Schema-A structurally cannot
   express "no pick". Schema-A stays exactly as it is; no schema change, no migration.
4. Schema-A remains **approval-only**. Its charter is "which variant won", and a reject-only pass has no winner.
5. `defect_tags` and `note` on a rejected variant carry into the reject signal's rationale field — they are the
   *content* of the rejection and are what makes it learnable.

This is what "generalize the `selection_to_iii_signal` bridge to the generic leg-3 `response` log" (R4.2) means
concretely: today the bridge's only input is a Schema-A record; it gains a second input path rooted in
`responses[]`, and the two converge on one ADR-005 signal vocabulary.

## 5. Implementation follow-ups (named, NOT built in this pass)

Deliberately unbuilt while this spec is `proposed` — building against an unratified spec inverts §7.7.

| # | Work | Where |
|---|---|---|
| S-1 | `response_to_iii_signal()` — the reject path: `responses[]` → ADR-005 signal, `rlhf_signal_type: reject`, rationale from `defect_tags` + `note` | `canvas_core/rlhf/iii_bridge.py` |
| S-2 | An idempotency key for reject signals — Schema-A's `selection_id` does not exist here; needs a deterministic response-derived id, and `_existing_selection_ids` must learn to see it | `iii_bridge.py` L215–248 |
| S-3 | Collector wiring: emit S-1 on a reject verdict; review-surface spec §4.4 + decisions-log row 3 update from "canvas responses only" | `review_collect.py` |
| S-4 | Cross-vault: ADR-005 vocabulary confirmation with Argus before first emission — the signal shape is III's, not ours (§1 corollary) | coord memo to III.aDNA |
| S-5 | Stale docstring: `iii_bridge.py` L230–231 cites "the 4 G-01 F3-migrated `C-NEW-*` entries"; the live store holds 2 `CANVAS-L-*` pattern entries | `iii_bridge.py` (fixed in this pass — see §6) |

## 6. What this pass changed

Documentation and one stale comment only. **No routing behavior changed**; a reject still writes no III signal
until S-1..S-4 land under a ratified spec.

- This spec (new).
- `spec_interface_surface.md` §2 — the ISS wording qualified per §3.
- `spec_canvas_review_surface.md` §6 — the dispatch contract, separately (H6 O3).
- `iii_bridge.py` — the S-5 docstring corrected to ground truth.

## 7. Decisions log

| # | Decision | Ruling | Why |
|---|---|---|---|
| 1 | Sink ownership | Canvas = capture substrate; III = signal schema | they answer different questions; conflation is what left G6 open |
| 2 | Store homogeneity | heterogeneous by design; discriminate on consumer-namespace `selection_id` | already implemented at L225; making it normative stops a future reader assuming otherwise |
| 3 | ISS-vs-III | scope conflation, not a conflict; qualify the ISS wording, re-assign nothing | two objects shared one word |
| 4 | Reject routing (**roadmap open decision #4**) | reject → III as `rlhf_signal_type: reject`, derived from `responses[]`; Schema-A stays approval-only | Schema-A cannot express "no pick"; the reject constant already exists; the signal is worth more than the schema change would cost |
| 5 | Build now? | no — spec `proposed`, implementation named as S-1..S-4 | building against an unratified spec inverts §7.7 |

**Ratification (§7.7):**

| Field | Value |
|-------|-------|
| Decision | spec_rlhf_seam v1.0 (the ownership boundary · store discrimination · ISS resolution · reject routing) |
| Ratified by | *(pending — operator)* |
| Date | *(pending)* |
| Status | **proposed** |
