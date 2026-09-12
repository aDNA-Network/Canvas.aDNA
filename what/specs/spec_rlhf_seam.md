---
type: spec
spec_id: spec_rlhf_seam
title: "The RLHF seam — Canvas owns the capture substrate, III owns the signal schema (Lodestar R4.2)"
standard_version: "2.4.0"
interaction_version: "1.0"
status: accepted
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
> **Status `accepted`** (operator, 2026-08-09 — §7.7 block at the foot). This spec was written *before* its
> implementation deliberately (agents author, operators ratify); the signature is what released §5's
> **S-1..S-4** to be built. Implementation landed in the same session as the signature, never ahead of it.

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

Deliberately unbuilt while this spec was `proposed` — building against an unratified spec inverts §7.7.
**Released by the 2026-08-09 ratification**; build status is tracked in §6a.

| # | Work | Where |
|---|---|---|
| S-1 | `response_to_iii_signal()` — the reject path: `responses[]` → ADR-005 signal, `rlhf_signal_type: reject`, rationale from `defect_tags` + `note` | `canvas_core/rlhf/iii_bridge.py` |
| S-2 | An idempotency key for reject signals — Schema-A's `selection_id` does not exist here; needs a deterministic response-derived id, and `_existing_selection_ids` must learn to see it | `iii_bridge.py` L215–248 |
| S-3 | Collector wiring: emit S-1 on a reject verdict; review-surface spec §4.4 + decisions-log row 3 update from "canvas responses only" | `review_collect.py` |
| S-4 | Cross-vault: ADR-005 vocabulary confirmation with Argus before first emission — the signal shape is III's, not ours (§1 corollary) | coord memo to III.aDNA |
| S-5 | Stale docstring: `iii_bridge.py` L230–231 cites "the 4 G-01 F3-migrated `C-NEW-*` entries"; the live store holds 2 `CANVAS-L-*` pattern entries | `iii_bridge.py` (fixed in this pass — see §6) |

## 6a. Build status (S-1..S-4) — added 2026-08-09, H3

Released by the ratification above and built the same session.

| # | Status | Where |
|---|--------|-------|
| S-1 | ✅ **built** — `response_to_iii_signal()` + `fold_variant_responses()` + `is_reject()` | `canvas_core/rlhf/iii_bridge.py` |
| S-2 | ✅ **built** — `response_id()` (`rej_YYYYMMDD_HHMMSS_<4hex>`); the dedup reader now accepts `selection_id` **or** `response_id` | `iii_bridge.py` |
| S-3 | ✅ **built** — collector reject branch; `rejects` / `rejects_held` counts; §4.4 + decisions-log row 3 updated | `review_collect.py` |
| S-4 | ✅ **RULED + OPEN 2026-09-07** — Argus ruled reading **(b)**; `REJECT_VOCABULARY_CONFIRMED = True`, reject entries carry `accepted: false`. See §6b. | `iii_bridge.py` · `who/coordination/` |

**The S-4 gate is a mechanism, not a promise.** This spec required vocabulary confirmation *before
first emission*, so `REJECT_VOCABULARY_CONFIRMED = False` in `iii_bridge.py` holds every reject
signal out of the shared learning store: the signal is still built and counted (`rejects`), and
held (`rejects_held`), and the rejection remains durable in `responses[]` regardless. Flip that one
constant when Argus replies. Two tests assert the default holds — writing "we'll remember not to
run it" into a spec is not the same as making it true.

**The open question put to Argus** is `accepted`: we emit `true`, reading ADR-003 §4 as "this entry
was admitted to the store" rather than "the reviewer accepted the image" (which lives in
`rlhf_signal_type`). The two readings produce opposite training signal from the same line.

Three consumer-namespace choices made Canvas-side (ADR-005 §3 rule 1 — ours to choose, but
flagged): a **distinct trap** `image_generation_variant_reject` (folding rejects into the pick trap
would let refusals accumulate toward "this register is working" under ADR-003 §3 graduation
scoring) · **`response_id` not `selection_id`** (there is no `SelectionRecord` behind a reject, and
naming one would be a lie the store cannot detect) · **`defect_tags` + `note` carried into the
rationale**, with a bare reject saying explicitly that no reason was captured.

## 6b. The S-4 ruling — `accepted` = the reviewer's verdict (2026-09-07)

> **Source:** `who/coordination/coord_2026_09_07_argus_to_mondrian_accepted_semantics_ruling.md`
> (Argus → Mondrian, in reply to `coord_2026_08_09_mondrian_to_argus_reject_signal_vocabulary.md`;
> `ack_required: false`, no reply owed). Provenance given as III's Operation Noria DP-1,
> operator-authorized dispatch. **§6a above is kept as written** — the gate was real while it held.

**Ruling: (b).** `accepted` is the **reviewer's verdict**, not store admission. Flip to `false` on
rejects before first emission.

**Argus's rationale, as given.** ADR-003 §3's graduation gate computes acceptance ≥80% over the
`accepted` field. Under reading (a) every stored entry is vacuously `accepted: true` and the gate
measures *store admission* rather than *operator judgment* — refusals would accumulate toward "this
register is working," which is precisely the failure the distinct-trap choice avoids. Verdict
semantics keep the channels orthogonal: **`rlhf_signal_type` = what the signal *is*; `accepted` =
what the reviewer *ruled*.**

**The three consumer-namespace choices are blessed as made** — the distinct
`image_generation_variant_reject` trap, `response_id` dedup, explicit no-rationale marking. Nothing
in §6a's third paragraph changes. Argus has queued a clarifying in-place amendment writing this
semantics into ADR-003 §4 / ADR-005 (**Noria OQ-N11**) so the next consumer need not ask.

**What changed in code** (`canvas_core/rlhf/iii_bridge.py`):

| Site | Before | After |
|---|---|---|
| `REJECT_VOCABULARY_CONFIRMED` | `False` | **`True`** |
| reject entry `accepted` | `True` | **`False`** |
| pick entry `accepted` (`selection_to_iii_signal`) | `True` | **`True` — unchanged, and correct** |

⚠ **The asymmetry is the ruling**, not an inconsistency: on the Schema-A path a record exists
*because* the operator picked, so the reviewer genuinely did accept. Both halves are pinned by
`test_accepted_is_the_reviewers_verdict_not_store_admission`, and the old guard test was **inverted
rather than deleted** (it had asserted the pre-ruling default).

⚠ **Flipping the constant arms the path; it does not emit anything.** At the flip the HR pilot held
**0 rejects** (gate 3/3 recorded 3 approve / 3 skip; the local store's three `C-CFE-*` entries are
all `rlhf_signal_type: accept`), so re-running the collector produced **no new lines**. The intended
first emitter is the **P4 ComfyUI variant-selection board** — the pilot's second consumer.

*Measured, not assumed* — collector re-run against `what/artifacts/review_surface_pilot/`
post-flip, 2026-09-07:
`{variants: 0, responses: 0, selections: 0, rejects: 0, rejects_held: 0, iii_lines: 0, skipped: 6}`;
store md5 `dca90b37757c1fa365a49daaaab18a98` **unchanged**, 6 lines before and after. Note
`rejects_held: 0` here means *there were no rejects*, **not** *the gate held them* — the two read
identically in the counts and only the `rejects` field distinguishes them.

### Store pin — two objects, two populations

Argus's FYI: *"canonical store rotated at our DP-1 (28→30, md5 → `a28ec2a1815cf3cc08b375a40a23aca3`)
… your graduation scans should pin the new hash."* Recorded honestly rather than acted on as
described, because two things are not true of Canvas today:

1. **Canvas has no graduation scan and no hash pin** — verified by grep across `canvas_core/rlhf/`
   and this spec at the time of the ruling. There is nothing here to re-pin; the pin is recorded so
   that whatever scan is *built* starts from the right number.
2. **The object Canvas writes is a different file** from the one that rotated. Canvas's
   `DEFAULT_LEARNING_STORE` is the wrapper store
   `how/federation/iii/what/context/canvas_iii_learning_store.jsonl` — **6 lines**, md5
   `dca90b37757c1fa365a49daaaab18a98` (working tree, 2026-09-07). III's canonical store is theirs.

| Object | Owner | Population (2026-09-07) | md5 |
|---|---|---|---|
| III canonical store | III.aDNA | 30 entries (was 28, rotated at their DP-1) | `a28ec2a1815cf3cc08b375a40a23aca3` |
| Canvas wrapper store | Canvas.aDNA | 6 lines — a `_meta` header (L1) + 2 `CANVAS-L-*` pattern entries (L2–3) + 3 `C-CFE-*` picks (L4–6), all `rlhf_signal_type: accept` | `dca90b37757c1fa365a49daaaab18a98` |

*Both numbers state their population on their face, per the practice Hopper ratified as their
ADR-011 A8 §5 — the pin is useless if a reader cannot tell which file it belongs to.*

## 6. What this pass changed

*(The H6 pass, 2026-08-09 — kept as written. Superseded on the same date by §6a, which records the
H3 pass that built S-1..S-3 once the ratification released them.)*

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
| Ratified by | stanley |
| Date | 2026-08-09 |
| Status | **accepted** |

> Ratified at the H3 plan gate (2026-08-09). The signature is what unblocks **S-1..S-4** (§5): the
> implementation was deliberately withheld while this spec was `proposed`, so it becomes buildable
> work the moment the boundary is signed — not before.
