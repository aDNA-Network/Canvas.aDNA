---
type: spec
spec_id: spec_canvas_review_surface
title: "Canvas review surface — Meta Bind capture ↔ interaction affordances ↔ the RLHF sinks (Halftone HR)"
standard_version: "2.3.0"
interaction_version: "1.0"
status: ratified
created: 2026-08-04
updated: 2026-08-04
last_edited_by: agent_mondrian
phase: HR
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
> surface-choice routing is the future OIP layer's call). NOT a dispatcher — **regeneration dispatch is a named
> contract stub (§6)**, deferred pending Bearly P5 evidence (the Callisto seam, coord 2026-07-28 §2).
> `enableJs: false` is preserved throughout — capture is frontmatter-only.

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

## 6. `review_dispatch_contract v0` — NAMED STUB (the Callisto seam)

Deferred pending **Bearly P5 evidence** (coord 2026-07-28 §2 / 2026-08-03 reply §2). When it binds, the
contract MUST honor: the intent record derivable from collected state
(`{surface, variant_id, prompt, prompt_edit, defect_tags, requested_by, at}`); a fresh generation under the
SAME contract; the result minted as a **new node linked to its parent** (nothing overwritten — Bearly §4);
spend under an operator gate. Until then `regenerate_requested` is an inert, collected intent flag. HR ships
**no** dispatcher, no HTTP, no render call.

## 7. Decisions log

| # | Decision | Ruling | Why |
|---|---|---|---|
| 1 | Rating axes | single overall `rating` in v1.0 | control-count sanity; `vr_scores` stays open for v1.1 axes |
| 2 | Multi-tag capture | one response per tag on one `choice` affordance | append-only responses make multi legal without a new kind; I-3 validates each |
| 3 | Reject-only routing | canvas responses only | Schema-A needs a pick; bridge charter is accept-only; H6 #4 owns the seam |
| 4 | Pilot corpus | the real dataset | roadmap §6 explicit; `{kind: ai}` marking keeps agent runs distinguishable |
| 5 | Buttons vs toggles | pilot ships toggles for pin/escalate + one `updateMetadata` button (regenerate) | both JS-less; the render check resolves preference |

**Ratification (§7.7):**

| Field | Value |
|-------|-------|
| Decision | spec_canvas_review_surface v1.0 (mapping · sidecar schema · collector contract · dispatch stub) |
| Ratified by | stanley (operator) — plan approval = the signature (2026-08-04 GO-wave plan; Amendment-1 precedent) |
| Date | 2026-08-04 |
| Status | **accepted** |
