---
idea_id: idea_deck_generator_canvas_pilot
type: backlog
title: "Deck Generator — graph→canvas-object pilot (Lattice Protocol)"
category: pipeline
status: implemented
priority: high
effort: plan
proposed_by: agent_stanley
proposed_date: 2026-06-07
created: 2026-06-07
updated: 2026-06-21
last_edited_by: agent_stanley
plan_id: mission_deck_generator_canvas_pilot
tags: [backlog, canvas, deck, generator, pilot, graph-to-canvas, lattice-protocol]
---

# Deck Generator — graph→canvas-object pilot (Lattice Protocol)

## Problem / Opportunity

A board-grade slide deck and a dense technical brief on the Lattice Protocol were just hand-built in
`aDNALabs.aDNA` by an agent: retrieving from the aDNA context graph, composing a slide spine, rendering,
and iterating. That work **proves a repeatable pattern — a graph → a deck** — but it was produced ad-hoc
on the `.pptx` path (PptxGenJS), which is a **fork with no bridge to the canvas path** Canvas.aDNA owns.

Canvas.aDNA's thesis is that a deck is one instance of the universal 2D output primitive — a **canvas
object**. CanvasForge already has a graph→`.canvas` deck pipeline; LAVentureGraph already does graph→canvas
at scale. What the pilot adds, and what no producer yet encodes, is a **method**: persona-diverse III
inspect/improve cycles + hard **accuracy guardrails** (verify-or-omit, GRAPH-GAP discipline). Capturing this
now — before it's lost — gives the future execution campaign a concrete, proven pilot to build the
standard-conformant deck generator around.

## Proposed Solution

Author a **parked planning mission** ([[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]])
that scopes a canvas-object deck generator on the **canvas path** (leveraging CanvasForge's
`canvas_presentation` pipeline + the Canvas Standard), folding in the persona-III + accuracy-guardrail method
the pilot proved. The Lattice technical brief is the worked exemplar of "graph → Canvas.aDNA system →
canvas object." **No build now** (campaign constraint C3) — this is an execution-campaign candidate feeding P4.

## Discussion

- 2026-06-07 (agent_stanley): Pilot artifacts (referenced, not copied) live at
  `aDNALabs.aDNA/how/presentations/lattice_dlt_technical_brief/` and `…/lattice_web3_board_deck/`; method
  evidence in their `III_review_brief.md` + `GRAPH_GAPS_brief.md`.
- Prior art to reuse: CanvasForge `what/code/canvas_presentation/` (7-stage lattice, 16 slide types,
  24-criterion scoring, Imagen `PendingImage` lifecycle, R11 gate); LAVentureGraph `scripts/m09_canvas_generator.py`;
  Canvas.aDNA `what/lattices/canvas_yaml_interop.md` + `lattice2canvas.py`/`canvas2lattice.py`.
- Ties to decisions: **D2** (CanvasForge relationship — the generator is a *producer* consuming the Standard),
  **D4** (component model — the generator exercises node/panel/link typing), **D7** (canvas-as-primitive — a
  deck generator is evidence canvas is a deployable output primitive, not just a view).

## Decision

**`implemented` 2026-06-21** (post-Keystone backlog triage). The parked pilot was **fulfilled by Operation Keystone
phase E4.4** — `deck_generator`, a graph/spec → v2.0.0 aDNA-Native deck `.canvas` consumer built on `canvas_std`
alone, shipped green (**16/16**) at `what/production/deck_generator/`. The persona-III + accuracy-guardrail method this
idea captured fed the E4 consumer work; the worked Lattice technical-brief exemplar informed D2/D4/D7. Linked planning
mission `mission_deck_generator_canvas_pilot` reconciled to `completed` (fulfilled-by-E4.4) the same day. No further
build is owed; the optional comic/diagram production layers absorbed at pt09 remain net-new candidates for a future
campaign, not this idea.
