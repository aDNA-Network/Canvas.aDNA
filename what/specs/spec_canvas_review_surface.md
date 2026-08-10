---
type: spec
spec_id: spec_canvas_review_surface
title: "Canvas review surface — Meta Bind capture ↔ interaction affordances ↔ the RLHF sinks (Halftone HR)"
standard_version: "2.3.0"
interaction_version: "1.0"
status: ratified
created: 2026-08-04
updated: 2026-08-09
last_edited_by: agent_mondrian
phase: HR
amendments:
  - date: 2026-08-09
    phase: H6
    section: "§6 review_dispatch_contract v0"
    summary: "Named stub → six-clause contract; D5 (refusal atomicity, F-S030-1) + D6 (venue boundary) folded in from Bearly s030/s031 evidence. Still contract-only. Ratification PENDING."
    status: proposed
campaign_id: campaign_canvas_halftone
resolves: "gap G9 — the RLHF review surface (every layer existed; no assembled operator surface)"
supersedes:
superseded_by:
tags: [spec, canvas, review, rlhf, metabind, interaction, affordance, schema_a, iii, halftone, hr]
---

# Canvas Review Surface (Halftone HR)

> **Ratified 2026-08-04** (operator, §7.7 block below — the GO-wave plan approval was the signature).
>
> **What this is.** The canonical mapping from **Meta Bind controls** on sidecar notes to the ratified
> **interaction-runtime affordance kinds** (`spec_interface_surface.md`, `interaction_version: 1.0`), plus the
> **collector contract** that fans one operator verdict into the three sinks — the canvas's append-only
> `interaction.responses[]`, a Schema-A `SelectionRecord`, and the III learning store. Reference
> implementation: `canvas_core/rlhf/{review_canvas,review_collect}.py`; pilot:
> `what/artifacts/review_surface_pilot/`.
>
> **Non-goals.** NOT a `canvas_std` change (the overlay is the ratified additive `_reserved.interaction`; the
> firewall holds). NOT a capture runtime (ISS remains the sibling surface for flat rich-context gates, ADR-006;
> surface-choice routing is the future OIP layer's call). NOT a dispatcher — **regeneration dispatch is
> contract-only (§6)**: as of the 2026-08-09 amendment the contract has *bound* (six clauses, Bearly evidence
> discharged), but no dispatcher, HTTP client or render call ships. `enableJs: false` is preserved throughout —
> capture is frontmatter-only.

## 1. Architecture

```
image variants ──builder──▶ review .canvas (per variant: image file node + sidecar-note file node, linked)
sidecar note  ──Meta Bind INPUT / updateMetadata BUTTON──▶ frontmatter verdicts (the operator's act)
frontmatter   ──collector──▶ (a) apply_response → _reserved.interaction.responses[]   (append-only view)
                             (b) Schema-A SelectionRecord → what/artifacts/image_gen_dataset/   (approvals)
                             (c) III signal → the live learning store (iii_bridge.accumulate)
regenerate/pin/escalate ──── intent flags ONLY (§6 stub; nothing dispatches) ────
```

The canvas declares affordances additively under `metadata.frontmatter._reserved.interaction` (one namespaced
set per variant: `var{N}.{verdict|rating|defect|note|prompt_edit|regenerate|pin|escalate}`, anchored on the
variant's **sidecar node id**); the sidecar's frontmatter is the capture medium; the collector is the only
writer of record.

## 2. Control ↔ affordance mapping (normative)

Bearly's nine-control table (`Bearly.aDNA/what/specs/spec_bearly_rlhf_canvas.md` §3) is the **informative
precedent**; the Canvas normative set:

| Control | Sidecar key | Affordance kind | Value discipline | Sink(s) |
|---|---|---|---|---|
| **Verdict** (required) | `verdict` | `choice` `[approve, reject, skip]` | one response | canvas; `approve` additionally → Schema-A + III |
| **Rating** | `rating` | `choice` `["1".."5"]` | int normalized → str | canvas; folded into `vr_scores.overall` on approval |
| **Defect tags** | `defect_tags[]` | `choice` (10-term vocab: `off-model · wrong-palette · line-quality · expression · composition · text-error · tone · safety · provenance-gap · slop`) | **one response per tag** (append-only makes multi legal; I-3 checks each) | canvas; folded into `pick_reason` |
| **Note** | `note` | `annotation` | non-empty only | canvas; folded into `pick_reason` |
| **Prompt edit** | `prompt_edit` | `input` | whole-string delta in v1.0 (named-layer delta = v1.1 reserve) | canvas |
| **Regenerate** | `regenerate_requested` | `action` (value `null`) | intent flag | canvas only — dispatch = §6 |
| **Pin as reference** | `pin_requested` | `action` | intent flag | canvas only (VisualDNA promotion is the owner-vault's act) |
| **Escalate** | `escalate` | `action` | intent flag; `#needs-human` semantics | canvas only |

*(Bearly's `Approve` folds into `verdict`; `Fan variants` defers with dispatch. Bearly's four rating axes
(`canon·style·composition·text`) are reserved as `rating_canon`-style keys for a v1.1 extension — `vr_scores`
is already an open dict.)*

## 3. Sidecar frontmatter schema

Identity (builder-seeded): `type: review_sidecar` · `review_surface` · `review_canvas` · `variant_id` ·
`variant_label` · `image_path` (vault-relative — F-36-clean by construction) · `model` · `prompt`.
Controls (operator-set, §2 keys, seeded null/`[]`/`""`/`false`): `reviewer` is optional self-identification.
Collector ledger (collector-owned): `collected_at` · `selection_id` · `review_turn`.

## 4. The collector contract (`review_collect`)

1. **Order per variant:** canvas sink → Schema-A → III → **ledger last** (a mid-run crash re-runs clean).
2. **Attribution is honest by construction:** every response carries `participant: {kind, id}`; agent plumbing
   runs MUST pass `kind: ai` — simulated verdicts are never recorded as human signal.
3. **Idempotency, layered:** (L1) the `collected_at` ledger skips collected variants (`--force`/clearing
   re-opens; `--turn t2` starts an append-only re-review); (L2) response dedup on
   `(affordance, value, participant.id, turn)` — identical replays are no-ops even with a lost ledger; two
   *different* defect tags on one affordance are both kept; (L3) deterministic
   `selection_id = sel_<stamp>_<sha4(canvas|variant|approver|turn)>` with the stamp taken from `collected_at`,
   else the canvas's earliest matching verdict-response `at` (the fallback clock), else now — plus an existence
   check before writing; (L4) `iii_bridge.accumulate` is natively idempotent on `selection_id`.
4. **Approvals only reach Schema-A/III.** A reject-only pass appends responses and writes no records — Schema-A
   structurally requires a pick and the bridge charter is `accept`-only; the rejection signal stays durable in
   `responses[]` + the sidecars. The reject→III seam is **H6 open decision #4** (III store vs
   `interaction.responses` routing) — capture keeps Schema-A either way.
5. **Multi-approve is legal** — one `SelectionRecord` per approved variant (same-second multi-record precedent
   exists in the corpus). Pilot records land in the REAL corpus (`what/artifacts/image_gen_dataset/`, roadmap
   §6: "beside the existing 13"); tests use tmp roots.
6. `--dry-run` runs the full pipeline and writes nothing (byte-identical, test-asserted).

## 5. Conformance + the ship gate

The review canvas declares `adna_native` (`adna_version` + nested `sync.sync_hash`) so `canvas-std validate`
exercises **I-1/I-2/I-3**; the builder self-gates on `validate_suite`. The three-check ship gate applies
(`spec_federation_contract` §4 Amendment 1): schema (`canvas-std validate`) → geometry (`canvas-visual-check`)
→ **agent-confirmed Obsidian render** (the HTML renderer is file-node-blind by design — a file-node board can
only be sight-certified live). Clean CV-FILE-PROPS-01 requires `.obsidian/app.json` →
`"propertiesInDocument": "hidden"` (frontmatter IS the capture mechanism; authoring-guidance rule 5).
Appending responses never perturbs `sync.sync_hash` (topology-only).

## 6. `review_dispatch_contract v0` (the Callisto seam)

> **Amended 2026-08-09 (Halftone H6) — the stub binds.** The evidence dependency this section was deferred
> behind is **discharged**: Callisto's `bearly_s030` memo (`outbound_20260807_mondrian_hr_dispatch_evidence.md`)
> delivered render-class RLHF loop traces plus finding **F-S030-1**, and `bearly_s031`
> (`coord_2026_08_08_..._bundle_011_and_mode_l.md`) added a **second render venue** (ADR-007 mode L). Both are
> folded in below as clauses **D5** and **D6**. This remains **contract-only**: no dispatcher, no HTTP, no
> render call ships with it, and `regenerate_requested` stays an inert collected intent flag.

A conforming dispatcher MUST honor all six clauses.

| # | Clause | Source |
|---|---|---|
| **D1** | **Derivable intent.** The dispatch intent record is derivable from collected state alone — `{surface, variant_id, prompt, prompt_edit, defect_tags, requested_by, at}`. No out-of-band context. | HR original |
| **D2** | **Same contract.** The regeneration runs under the SAME generation contract as the variant it descends from — same prompt assembly, same backend chain semantics. A regenerate is a *re-roll*, not a new brief. | HR original |
| **D3** | **New node, linked to parent.** The result is minted as a **new node linked to its parent**. Nothing is overwritten — the rejected variant and its verdict remain in the record. | HR original; Bearly §4 |
| **D4** | **Operator spend gate.** Spend passes an operator gate before dispatch, never after. | HR original |
| **D5** | **Refusal atomicity.** A refused dispatch or verdict leaves **zero trace in any store.** Guards run *before* any append; a refusal is line-count-invariant across every sink. | **F-S030-1** — Callisto `bearly_s030`, credited |
| **D6** | **Venue boundary.** A render venue may be a **third party's node on their own key**. The contract therefore composes with: operator-**pull** of verified per-batch bundles (not push), a **two-consent** spend gate (both the requesting and the hosting operator), and **arrival verification before any asset enters the canvas**. | Bearly V5 (mode G) + **ADR-007 mode L**, `bearly_s031` |

### On D5 — why a clause earned by failure is worth more than one earned by design

Bearly's verdict pipeline originally **appended the loop record and then refused** at the guard stage, leaving a
phantom `approve` record behind a refusal. They found it, fixed it (guards before any append; refusals now
line-count-invariant, machine-verified), and handed it over. It failed live in a **single-machine** loop — which
is the cheap case. A cross-machine dispatch hop has strictly more places to fail between "append" and "refuse",
so a contract that did not state D5 would be inviting the same defect at higher cost. Adopted verbatim in intent,
credited to its finder.

### On D6 — what a fourth-party venue does to the boundary

Two venues now exist on the Bearly side: **mode G** (cloud, Luke's lane) and **mode L** (local inference on a
third party's RTX 3090, operator-administered, per-render consent). Neither is Canvas's machine, and the second
is not even the requesting operator's. D6 is the shape that survives both: pull-not-push, two-consent, and
verify-on-arrival. Canvas ships no transport for this — D6 constrains what a conforming dispatcher may do, and
the venue's own vault governs the venue.

### Still out of scope at v0

No dispatcher, no HTTP client, no render call, no transport. `regenerate_requested`, `pin_requested` and
`escalate` remain inert intent flags collected into `responses[]`. Implementation is a later phase's work under
a ratified contract.

## 7. Decisions log

| # | Decision | Ruling | Why |
|---|---|---|---|
| 1 | Rating axes | single overall `rating` in v1.0 | control-count sanity; `vr_scores` stays open for v1.1 axes |
| 2 | Multi-tag capture | one response per tag on one `choice` affordance | append-only responses make multi legal without a new kind; I-3 validates each |
| 3 | Reject-only routing | ~~canvas responses only~~ → **RULED at H6**: reject also routes to III as `rlhf_signal_type: reject`, derived from `responses[]`; Schema-A stays approval-only | [[spec_rlhf_seam]] §4 (2026-08-09). Behavior is **unchanged until S-1..S-4 land** under a ratified seam spec — the collector still writes no III signal on reject today |
| 4 | Pilot corpus | the real dataset | roadmap §6 explicit; `{kind: ai}` marking keeps agent runs distinguishable |
| 5 | Buttons vs toggles | pilot ships toggles for pin/escalate + one `updateMetadata` button (regenerate) | both JS-less; the render check resolves preference |
| 6 | Dispatch contract binding (H6) | stub → **six clauses** (D1–D6); D5 refusal-atomicity + D6 venue-boundary adopted from Bearly evidence | the deferral condition ("pending Bearly P5 evidence") was met; keeping it a stub after the evidence landed would be deferral by inertia |
| 7 | Build the dispatcher? (H6) | **no** — contract-only stands | D6's venue shape is still moving (mode L's kit transfer is deferred on the aDNALabs node-ready signal); a dispatcher built now would bind to a venue that has not yet run a batch |

**Ratification (§7.7):**

| Field | Value |
|-------|-------|
| Decision | spec_canvas_review_surface v1.0 (mapping · sidecar schema · collector contract · dispatch stub) |
| Ratified by | stanley (operator) — plan approval = the signature (2026-08-04 GO-wave plan; Amendment-1 precedent) |
| Date | 2026-08-04 |
| Status | **accepted** |

**Ratification — 2026-08-09 amendment (§6 D1–D6):**

| Field | Value |
|-------|-------|
| Decision | `review_dispatch_contract v0` — the six-clause contract (D5 refusal atomicity · D6 venue boundary) |
| Ratified by | *(pending — operator)* |
| Date | *(pending)* |
| Status | **proposed** |

> *Why this amendment does not ride the plan approval as its signature (unlike v1.0): the 2026-08-09 plan
> approved **writing** the clauses; D5/D6 did not exist as text when it was given. A signature cannot precede
> the text it signs. Surfaced at the H6 gate.*
