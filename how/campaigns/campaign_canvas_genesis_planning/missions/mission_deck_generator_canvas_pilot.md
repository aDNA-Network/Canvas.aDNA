---
plan_id: mission_deck_generator_canvas_pilot
type: plan
title: "Deck Generator — graph→canvas-object pilot (Lattice Protocol)"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis_planning
campaign_phase: P4-candidate
campaign_mission_number: null
mission_class: reconnaissance
created: 2026-06-07
updated: 2026-06-21
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, deck, generator, pilot, execution-candidate, parked]
---

# Mission: Deck Generator — graph→canvas-object pilot (Lattice Protocol)

**Campaign**: [[how/campaigns/campaign_canvas_genesis_planning/campaign_canvas_genesis_planning|Operation Cartography]]
**Phase**: **Pre-P4 — execution-campaign candidate (PARKED, `status: planned`)**
**Mission**: backlog/recon · feeds the P4 execution-campaign charter

> **Parked, not active.** This is a captured pilot + scoped build-mission spec for the *future* execution
> campaign (`campaign_canvas_genesis`). It **opens no phase and builds no code now** (campaign hard constraint
> **C3**: no runtime/no code this campaign). It exists so the proven graph→deck **method** and its worked
> exemplar are not lost between the genesis-planning campaign and the build. Origin: a deck-building process
> run in `aDNALabs.aDNA` (Berthier) 2026-06-05/07, migrated here per operator direction 2026-06-07.

## Goal

Scope a **deck generator** whose output is a **canvas object** (JSON Canvas, per the aDNA Canvas Standard),
turning an aDNA context graph into a presentation. Use the just-built **Lattice Protocol technical brief** as
the worked pilot of "a graph → the Canvas.aDNA system → a canvas object," and fold in the **method** the pilot
proved (persona-diverse III cycles + accuracy guardrails). When the execution campaign runs, this becomes a
concrete reference deck-generator + a conformance test case for the v2.0.0 Standard.

## Method captured from the pilot (the reusable IP)

The pilot (a 33-slide board deck + an 8-slide technical brief) established a repeatable pipeline beyond what
the producers encode today:

1. **Graph retrieval → deck spine.** Traverse the context graph; assemble a one-idea-per-slide spine with
   every claim traced to a source path. (Pilot: aDNALabs/Lattice graph → 4-act board deck + 8-topic brief.)
2. **Render loop.** Build → render to per-slide images → *see* the slides (LibreOffice + Poppler). Visual
   verification, not just structural QA. (Pilot toolchain: PptxGenJS + LibreOffice + Imagen + python-pptx;
   the canvas path would render via CanvasForge / Obsidian instead.)
3. **Persona-diverse III inspect/improve cycles.** Inspect each rendered slide through **5 lenses** — web3/DLT
   architect · cryptoeconomics · skeptical CTO · information designer · accuracy auditor — log findings by
   `module_iii_inspect_visual` severity, fix, re-render, iterate to **0 High / 0 Med across all personas**.
4. **Accuracy guardrails.** **Verify-or-omit** every quantitative claim; mark synthesis as synthesis; keep a
   **GRAPH-GAP register**. The headline win: the accuracy auditor caught a "21.5× accuracy" figure that
   Lattice's *own* III review had flagged as misleading (21.5% absolute from a 1.0% baseline) → **omitted**.

**This method is the contribution to layer onto CanvasForge's existing generator** — encode the persona-III
panel + accuracy gates into the canvas pipeline's quality loop (consumed from III via the `iii/` wrapper, C6).

## Prior art (catalog — KEEP / EXTEND / SUPERSEDE)

| Asset | Path | Disposition |
|-------|------|-------------|
| CanvasForge presentation pipeline (7-stage lattice, 16 slide types, 24-criterion scoring, Imagen `PendingImage`, R11 gate, tokyo_night/science_stanley themes) | `CanvasForge.aDNA/what/code/canvas_presentation/` + `what/lattices/lattice_presentation_canvas.lattice.yaml` | **KEEP** — the generator core; the deck generator is a producer over this |
| Graph→canvas at scale (NetworkX → 4 `.canvas` files) | `LAVentureGraph.aDNA/scripts/m09_canvas_generator.py` | **KEEP** — proof graph→canvas works; reuse layout/coloring patterns |
| JSON-Canvas spec + lattice↔canvas round-trip | `Canvas.aDNA/what/lattices/canvas_yaml_interop.md` · `…/tools/lattice2canvas.py` · `canvas2lattice.py` | **KEEP** — the output format + round-trip contract |
| Canvas identity / standard authority | `Canvas.aDNA/what/decisions/adr_000_canvas_identity.md` | **KEEP** — the standard the generator conforms to (v2.0.0) |
| Persona-III + accuracy-guardrail method | this mission §Method + the pilot's `III_review_brief.md` | **EXTEND** — net-new; encode into the canvas quality loop |
| pptx render-loop toolchain (PptxGenJS + LibreOffice + Imagen) | `aDNALabs.aDNA/how/presentations/*/build/` | **SUPERSEDE** (path) — pptx is the pilot path; the generator targets `.canvas` (see §The fork) |

## The fork: `.pptx` (built) vs `.canvas` (target)

The pilot was built on the **`.pptx`** path (PptxGenJS → LibreOffice render). Canvas.aDNA's primitive is the
**`.canvas`** object (group nodes = slides; text/file/link interior nodes; navigation edges; `_reserved`
metadata). There is **no bridge** between the two, and none is needed: the graph→canvas path is **direct and
already proven** (CanvasForge + LAVentureGraph). **Recommendation:** realize the deck generator on the canvas
path; treat the pptx pilot purely as proof-of-concept + the source of the method. Do **not** build a
pptx→canvas converter.

## Pilot reference (exemplar — referenced, not copied)

- Worked exemplar: `aDNALabs.aDNA/how/presentations/lattice_dlt_technical_brief/lattice_dlt_technical_brief.pptx`
  (8-slide technical brief) + `…/lattice_web3_board_deck/lattice_protocol_web3_board_deck.pptx` (33-slide board deck).
- Method evidence: each deck's `III_review_brief.md` / `III_review.md` (persona scorecards) + `GRAPH_GAPS_brief.md` / `GRAPH_GAPS.md`.
- Decks remain in `aDNALabs.aDNA` as archived pilot artifacts (SO-7); this mission references them by path.

## Scoped objectives (PARKED — for the execution campaign)

> All `status: planned`. Authored only when the operator opens the execution campaign; sequenced after the v2.0.0 spec (P2).

### 1. Catalog the CanvasForge generator against the method
- **Status**: planned · **Description**: map CanvasForge `canvas_presentation` (builder, layout, scoring, image lifecycle, R11) against the pilot's 4-step method; identify what to KEEP/EXTEND. · **Files**: an analysis doc under the execution campaign.
### 2. Design the canvas-object deck-generator contract
- **Status**: planned · **Description**: input (context graph / lattice + brief) → process (graph→spine→canvas nodes/edges; auto-layout; component typing per D4) → output (`.canvas` conforming to v2.0.0). · **Depends on**: 1.
### 3. Encode persona-III + accuracy gates into the quality loop
- **Status**: planned · **Description**: specify the 5-persona inspect panel + verify-or-omit/GRAPH-GAP gates as III `iii/`-wrapper contracts (engines stay in III/CanvasForge, C6/C8). · **Depends on**: 2.
### 4. Round-trip the pilot to a canvas object + exports
- **Status**: planned · **Description**: regenerate the Lattice brief as a `.canvas` object; round-trip to PDF / Google Docs via CanvasForge exporters; compare fidelity to the pptx pilot. · **Depends on**: 3.
### 5. Feed conformance + decisions
- **Status**: planned · **Description**: use the generated canvas as a conformance test case (P3 suite); supply evidence to **D2/D4/D7**. · **Depends on**: 4.

## Exit Gate

(For the future execution-campaign mission, not this campaign.) A canvas-object deck generator produces a
v2.0.0-conformant `.canvas` for the Lattice brief; the persona-III + accuracy gates run as `iii/`-wrapper
contracts; round-trip to PDF/GDoc verified; conformance + D2/D4/D7 evidence filed.

## Campaign Context

### Previous Mission Outputs
- P0 (`adr_000_canvas_identity`, decision register D1–D7, charter). The pilot itself (external, `aDNALabs.aDNA`).

### Next Mission Inputs
- Feeds **P4** (execution-campaign charter, `campaign_canvas_genesis`) as a candidate build mission; informs **D2/D4/D7** at P2.

## Notes

- Respects **C3** (no build now), **C6** (quality loops via `iii/` wrapper — don't re-implement engines),
  **C8** (substrate-neutrality — generator logic is a producer concern, not the standard-bearer).
- The standard-bearer owns the *contract* the generator conforms to; the generator itself is producer code
  (CanvasForge), consistent with the Canvas.aDNA / producer split.

## Completion Summary

**`completed` 2026-06-21** (reconciled in the post-Keystone backlog triage). The mission's core goal — *a canvas-object
deck generator producing a v2.0.0-conformant `.canvas` from a graph/spec* — was **delivered by Operation Keystone phase
E4.4**: `deck_generator` shipped green (**16/16**) at `what/production/deck_generator/`, on `canvas_std` alone. The
captured persona-III + accuracy-guardrail **method** (§Method) was the reusable IP this recon mission existed to
preserve; it informed the E4 consumer work and the `iii/` quality wrapper (E5.1).

**Premise reshaped by PT pt09 (2026-06-17):** the original "deck generator as a *producer over CanvasForge's
`canvas_presentation`" framing (objectives 1–5, prior-art KEEP table) was superseded when CanvasForge was absorbed into
Canvas.aDNA — production is now **in-vault** (`what/production/`), so E4.4 built the generator directly rather than as
an external producer. The granular pre-pt09 objectives (CanvasForge cataloging, pptx round-trip comparison) were not
executed as written; the goal they served was met by the in-vault path. No further build is owed.

## AAR

- **Worked:** capturing the graph→deck method + worked exemplar as a parked recon mission preserved the IP across the
  planning→build boundary; E4.4 built on it cleanly.
- **Didn't:** the detailed objectives 1–5 were authored against the pre-pt09 "producer over CanvasForge" architecture,
  which the merge invalidated before they ran.
- **Finding:** parked recon missions that pin a specific *architecture* (vs. a goal) risk going stale when the org
  topology shifts; the goal survived, the scoped steps did not.
- **Change:** reconciled to `completed` (goal fulfilled by E4.4) rather than re-scoping dead objectives.
- **Follow-up:** none for the deck path. The comic/diagram production layers absorbed at pt09 are net-new candidates
  for a future campaign, tracked separately — not this mission.
