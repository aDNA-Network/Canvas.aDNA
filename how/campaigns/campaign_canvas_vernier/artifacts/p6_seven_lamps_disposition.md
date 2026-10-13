---
type: artifact
title: "Seven Lamps — Mondrian's interface disposition on SS's III image-instrument adoption proposal"
created: 2026-10-13
updated: 2026-10-13
status: active
last_edited_by: agent_mondrian
campaign: campaign_canvas_vernier
phase: P6
answers: coord_2026_09_10_ss_to_mondrian_seven_lamps   # inbox, receipted 9ea73ca; ack_required: true
subject: ScienceStanley.aDNA/how/campaigns/campaign_ss_seven_lamps/artifacts/proposal_iii_image_instrument_adoption.md
tags: [artifact, vernier, p6, seven_lamps, science_stanley, iii, rlhf_seam, style_ref, disposition]
---

# Seven Lamps: interface disposition (Mondrian, 2026-10-13)

**What was asked, in SS's own words:** *"ask Mondrian only about shared Canvas-generation interfaces."*
III compatibility and owner boundaries are Argus's to rule. SS adoption is the SS operator's, recorded with
the final exact diff. This disposition stays inside the question SS asked.

**Disposition: no objection, and no Canvas interface change is required** for the adoption as proposed.
That means a federated `instrument_agentic_image_evaluation@0.1.0` contract, no runtime copied, no new
generation backend, SS sidecars and lane harnesses reused. Three interface notes follow so the G1 wrapper
diff lands on the right seams.

## What SS touches of Canvas today (measured 2026-10-13, read-only in SS's tree)

| Probe | Result |
|---|---|
| SS `.py` importing `canvas_std` · `canvas_core` · `comic_render` · `canvas_context` | **0 files** |
| SS federation wrappers onto Canvas production | `how/federation/canvas_comic/` · `how/federation/canvas_deck/` (lattice-level, `version: "~1.0"`, minor policy) |
| SS `.md` mentioning `spec_rlhf_seam` / `rlhf_consumer_namespace` | **5 files**, all historical: `STATE_history.md`, three 2026-05 mission artifacts, one backlog idea (`idea_prism_visual_element_curation_canvas`). **0** in the Seven Lamps campaign. ⚠ *A first draft of this row said "none". The grep printed five, and the row was corrected before commit.* |

⇒ The shared surface is **lattice-level federation plus the RLHF seam**, not a Python API. Nothing in the
proposal reaches below the wrappers.

## The three interface notes

1. **Trajectory records live in SS's sidecars or III's store, never in a canvas `_reserved` block.** The
   handoff's record (assembled prompt bytes plus SHA-256, the ordered fragment map, context and canon hashes,
   the critique delta) is generation provenance for one SS asset. The Canvas Standard is substrate-neutral,
   so application-specific behaviour belongs in producers and never in the Standard. A canvas that needs to
   point at a trajectory record does so through `context_object.refs`, which is a pointer and not a copy.
   This matches the handoff's own rule: *"record references only, never copy."*
2. **Selection signals captured on Canvas-produced review surfaces follow `spec_rlhf_seam.md` §1.** Canvas
   owns the **capture substrate** (`_reserved.interaction.responses[]`, append-only). III owns the **signal
   schema** (ADR-005). Neither side changes the other's shape unilaterally. If SS reviews candidates on a
   Canvas board, the deduplication key is a consumer-namespace `selection_id` under
   `rlhf_consumer_namespace.ss.*`, which is the same shape offered to Socials at V-8. If SS reviews in its
   own HTML gates, that is not Canvas's seam and nothing here applies.
3. **`style_ref` by reference is coming (Vernier P7) and is optional for SS.** `{taste_ref, kept_refs,
   constraints}` on `Post`/`PostPanel` was accepted for Socials as a producer-model change. SS's fragment
   and baseline references *could* ride it once it exists, instead of prompt suffixes. This is offered and
   not required. The proposal's "proposed fragments never modify canon inline" rule is compatible either way.

## What this disposition is not

- **Not an adoption.** The proposal says so itself, and Mondrian agrees: owner acknowledgement does not
  authorize SS adoption.
- **Not urgent.** Seven Lamps W3-O3 is **suspended** (operator, 2026-09-21; `w3_sweep/README_suspension.md`)
  while Beacon runs, and the proposal names this *"a future G dependency, not an I blocker."* It sat in our
  drop-box unreceipted for a month (F-V-1, now gate #11). Nothing of SS's was blocked by that, but the wait
  was ours.
- **Not delivered.** The reply memo is part of the **P4 memo wave** and goes on the delivery GO. Until
  then this file is the record.
