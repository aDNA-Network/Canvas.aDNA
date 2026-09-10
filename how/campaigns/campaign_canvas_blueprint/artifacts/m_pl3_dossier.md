---
type: artifact
artifact_id: m_pl3_dossier
title: "M-PL3 dossier — the comic_book_design corpus, the archive-only context_ref, and the comic nine: assembled for a joint sitting, deliberately not ruled"
campaign: campaign_canvas_blueprint
phase: P5
created: 2026-09-09
updated: 2026-09-09
status: staged_for_joint_sitting
last_edited_by: agent_mondrian
decision_owner: "joint — Mondrian (Canvas.aDNA) + ScienceStanley (SS.aDNA); SS agreed 2026-09-08"
tags: [artifact, m_pl3, comic_book_design, canvas_comic, archive, so7, federation, dossier]
---

# M-PL3 dossier — what the joint sitting needs, in one place

> **This dossier does not contain a decision, and that is deliberate.** The carried tail was written
> as *"`comic_book_design/` resurrect-or-archive **ruling**"* — a Canvas-side call. SS's 2026-09-08
> reply changed its shape and we accepted: *"stage the dossier at your end when Blueprint reaches
> it, and we will sit it jointly… we would also rather take it together than receive a fait
> accompli."* Blueprint reached it today and closed. **The sitting is unscheduled and the decision
> is open.**

## 1. What the object actually is (measured 2026-09-09, at the object)

`Archive.aDNA/CanvasForge.aDNA/what/context/comic_book_design/` — **14 files**, of which 12 are
context documents, 1 is a folder note, 1 is a provenance manifest.

| File | Lines | What it holds |
|---|---:|---|
| `context_comic_prompt_engineering.md` | 447 | prompt construction for comic panels |
| `context_comic_character_consistency.md` | 334 | holding a character stable across panels |
| `context_comic_print_specs.md` | 248 | bleed, trim, DPI, CMYK |
| `context_comic_page_architecture.md` | 228 | page-level layout grammar |
| `context_comic_visual_storytelling.md` | 227 | beat → panel translation |
| `context_comic_lettering.md` | 225 | balloon/caption typography |
| `context_comic_panel_composition.md` | 219 | within-panel composition |
| `context_comic_color_theory.md` | 213 | palette + mood |
| `context_comic_lettering_workflow.md` | 176 | lettering as a production step |
| `context_comic_production_workflow.md` | 163 | end-to-end production sequence |
| `context_comic_spread_coordination.md` | 139 | two-page spread continuity |
| `comic_book_design.md` | 46 | folder note / entry point |
| `AGENTS.md` | 73 | topic directory index |
| `graft_manifest.yaml` | — | provenance: 13 files grafted from `lattice-labs` at M-3-03, 2026-04-22, wave 4b, each with an integrity hash |

**≈2619 lines of authored context.** Lineage: `lattice-labs` → CanvasForge (2026-04-22, hashed
graft) → Archive when CanvasForge merged into Canvas.aDNA at Production Tidy pt09. It was **not**
migrated in with the production code — that is the whole of the open question.

## 2. Why it is a decision at all — three parties hold a piece

**(a) SS's wrapper points at the archive, on purpose, and says so three times.**
`ScienceStanley.aDNA/how/federation/canvas_comic/` carries an explicit **archive-only**
`context_ref` in `CLAUDE.md`, `MANIFEST.md` and `STATE.md`, each flagging the same thing:

> *"NOT migrated into Canvas.aDNA — read-only quarry per SO-7; resurrect-or-migrate is a
> Canvas-side decision, flagged at the Plumb Line M-PL3 gate because the Prism single-panel work
> will want it."*

M-PL2 `ls`-verified those paths on 2026-07-18, so this is a **live, correct, deliberately-pending**
reference — not the dead-path class P3 found in Obsidian, Astro and WebForge's wrappers. SS
confirmed 2026-09-08 that it *"will not move before then."*

**(b) Canvas shipped a comic system without it.** Operation Halftone took the comic pipeline
end-to-end real — hardened producer → render bridge → 27 real panels → 4 print-ready pages → eye
gate passed → panel export under contract v1.0. The in-vault contracts that carry comic knowledge
today are **two files**: `what/docs/comic_authoring_contract.md` and
`what/docs/comic_prompt_contract.md`, plus `comic_generator/iii_quality_contract.md` and the
`what/docs/visual_dna_schema/` set relocated at Halftone.

⇒ **The archived corpus is ~2619 lines of context that a working comic system was built without.**
That is the strongest single fact in the dossier and it cuts both ways: either the corpus is
genuinely redundant, or Halftone re-derived a subset of it at cost and the rest is still unclaimed
knowledge. **This dossier does not assert which**; a resurrect decision that skipped an overlap
measurement would repeat F-P2b-3, where we counted our own output as a consumer's problem.

**(c) The comic nine.** Nine SS `.canvas` files were emitted by `canvas_comic` — the producer
Canvas **archived** at Halftone under `adr_009`; today's `comic_generator` emits canonical
`_reserved`. P2b initially miscounted these as SS hygiene debt (F-P2b-3); they are our output in
their tree. SS and we agreed regeneration and the resurrect-vs-repoint call are **one decision**,
which is why they are in one dossier. They render fine today; there is no urgency from either side.

## 3. The options, with their costs — none recommended here

| # | Option | What it costs | What it buys | Who it binds |
|---|---|---|---|---|
| **A** | **Resurrect** — migrate the 12 context docs into `Canvas.aDNA/what/context/comic_book_design/` | an overlap audit against the Halftone-era contracts first (nobody has done one); ~2619 lines to own, update and keep true | SS's `context_ref` repoints at a live vault; the Prism single-panel work gets the context it was flagged for | Canvas owns and maintains it |
| **B** | **Confirm archive** — the corpus stays a read-only SO-7 quarry, cited not owned | nothing now; each future consumer pays a small archive-read cost | honest about what is maintained; nothing pretends to be current that isn't | SS's wrapper keeps a permanent archive-only ref, which is *correct* but always looks like a defect to a census |
| **C** | **Selective graft** — migrate only what a measured overlap audit shows is unclaimed | the audit, plus a split-corpus provenance story | smallest true surface; the graft manifest's hashes make it auditable | Canvas owns a subset; the remainder stays quarry |
| **D** | **Repoint to a successor** — declare the Halftone contracts the successor and mark the corpus superseded | writing the succession explicitly; SS updates one `context_ref` | one canonical home; census-clean | Canvas states a succession it has not yet verified |

**A note on B and D, because they look similar and are not.** B leaves the archive reference
standing as *a reference to archived material* — SO-7 correct, and it will be re-flagged by every
future fleet census forever. D asserts that something in-vault **supersedes** it, which is a claim
about coverage that **no one has measured yet.** Option D without the §3 audit is the same shape of
error as F-P3-2, where our index reported an adoption as a refusal for five weeks because nobody
opened the object.

## 4. What the sitting should measure before choosing

1. **The overlap.** 12 archived docs vs the in-vault comic contracts + `visual_dna_schema/`. Which
   of the ~2619 lines are *already* expressed in shipped contracts, and which are unclaimed?
   Nobody has run this. It decides between A, C and D on evidence rather than instinct.
2. **The Prism dependency.** SS's wrapper says *"the Prism single-panel work will want it."* Is
   that still true in September, or did Prism's needs change? SS holds this fact; we do not.
3. **The nine files.** Regenerate through today's `comic_generator` (canonical `_reserved`, current
   Standard) or leave them as archived-producer output with an honest note? SS's own §4 principle
   from the `toEnd` acceptance applies and points at *regenerate*: *"conformance debt on archival
   files re-surfaces in every future fleet census."* But regeneration is not a conformance fix — it
   changes the artifacts — so it is not the same call, and their *"revival of the archive: no"* half
   may point the other way. **This is exactly why it is joint.**
4. **Who maintains the result.** Option A moves 2619 lines onto Canvas's maintenance surface. That
   is a real cost and it should be named out loud before it is accepted, not discovered later.

## 5. State at close

- **Decision: OPEN.** Not ruled at P5, by agreement.
- **Nothing was written into `ScienceStanley.aDNA`** for this dossier, and nothing into
  `Archive.aDNA` — the corpus was read, counted and line-measured, never touched.
- **Blueprint closed carrying this**, recorded in `STATE.md` as a named watch item with SS as the
  joint decision-owner and *"flag us when you want the sitting"* as the trigger.
- SS was told the dossier exists, in memo #15 (the `toEnd` handover), which is the same file that
  discharges the other half of their 2026-09-08 reply.
