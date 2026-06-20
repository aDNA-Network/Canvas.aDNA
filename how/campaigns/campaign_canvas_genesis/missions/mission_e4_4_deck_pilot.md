---
plan_id: mission_e4_4_deck_pilot
type: plan
title: "E4.4 — Deck-generator pilot as a worked build (deck .canvas on canvas_std)"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 4
campaign_mission_number: 4
mission_class: build
created: 2026-06-19
updated: 2026-06-19
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, e4, deck, generator, build, canvas_std, production]
---

> **STATUS: completed 2026-06-19** (session `session_stanley_20260619_174121_keystone_e4_4_deck_generator`).
> Promotes the parked deck-generator pilot into a worked build — `deck_generator` built + green. See Completion
> Summary + AAR below.

# Mission: E4.4 — Deck-generator pilot (worked build)

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]]
**Phase**: 4 — net-new consumer + LF-successor (in-vault, pt09-reshaped) · **Mission**: E4.4 (second build of the phase)

## Goal

Realize the parked graph/structured→canvas-object **deck generator** as a runnable build on `canvas_std`: a deck spec
→ a v2.0.0 **aDNA-Native deck `.canvas`** where **each slide is a group node**. Reuse the E4.3 `brief_consumer`
pattern and **extend** it — multiple slide regions, a `sequence` chain, `isStartNode`, and the **`image` + `table`
component classes** the brief didn't exercise. Capture the pilot's persona-III + accuracy-gate **method** as an
`iii/`-wrapper *contract*. The render-to-PDF/PNG loop + 24-criterion scoring **engine** stay **PT-P5-gated**.

## Exit Gate
- `what/production/deck_generator/` — a packaged consumer producing a conformant deck `.canvas` (slides = groups).
- **Conformance:** `validate(doc, ADNA_NATIVE) == []`; `validate_suite` `meets_declared` + `level_reached == adna_native`;
  exactly one canonical surface (`deck_root`); one `panel_link.region` per slide (`extent.unit: "slides"`).
- **Round-trip:** `compute_sync_hash` stable across `to_canvas(from_canvas(doc))`; the `sequence` chain is acyclic
  (A-5) and linear (N-1 edges).
- **Degradation:** `strip(doc)` Core+Extended-valid (incl. `isStartNode`); no `_reserved` (D-1/D-2/D-3).
- **Components:** image → file/link (`degrades_to`), table → text — both carry + degrade faithfully.
- **Green:** `pytest` + `ruff` clean; `canvas-std validate` `[OK]`; `canvas_std` 46/8 + `brief_consumer` 10/10 unchanged.
- Committed with a `Keystone E4.4 —` message.

## Objectives

### 1. Build the deck generator
- **Status**: completed · **Description**: `what/production/deck_generator/` — `model` (DeckInput/Slide + load_deck),
  `slides` (6 KEEP slide types → interior nodes), `layout` (deterministic 16:9 slide-row), `consume` (`build_deck`:
  source contract → `to_canvas` → `_reserved` aDNA-Native), `__main__` CLI. · **Files**: `src/deck_generator/**`

### 2. Worked deck + artifact
- **Status**: completed · **Description**: `examples/canvas_standard_deck.yaml` (self-referential 6-slide deck
  exercising every slide type) + generated `examples/canvas_standard_deck.canvas` (6 slides / 21 nodes / 13 edges;
  deterministic). · **Files**: `examples/*`

### 3. Tests + CLI + no-regression
- **Status**: completed · **Description**: `tests/` — conformance, round-trip, degradation, **components**. `pytest`
  16/16, `ruff` clean (package `.venv`); `canvas-std validate` `adna_native [OK]` + D-1/D-2/D-3; `canvas_std` 46/8 +
  `brief_consumer` 10/10 unchanged. · **Files**: `tests/*`

### 4. Quality contract (persona-III + accuracy)
- **Status**: completed · **Description**: `iii_quality_contract.md` — the 5-lens persona-III inspect panel +
  verify-or-omit / GRAPH-GAP gates as `iii/`-wrapper contracts (engine in III, C6; render/scoring PT-P5-gated).
  · **Files**: `iii_quality_contract.md`

## Campaign Context

### Previous Mission Outputs
- E4.3 (`brief_consumer`) established the consumer pattern (source contract → `to_canvas` → `_reserved` enrichment;
  the four-property test contract; `what/production/` siting + `adna-canvas-std` dependency). E4.4 reuses + extends it.

### Next Mission Inputs
- E5.1 wires the `iii/` wrapper to the quality contract (III pin confirm). PT P5 lands `canvas_presentation` → the
  render loop + the external Lattice-brief fidelity comparison (deferred). E4.1/E4.2 remain gated on the D3 touch.

## Notes
- **canvas_std is a validator + round-tripper, not a renderer** — E4.4 ships a conformant deck *object*, not pixels.
- **The A-5 single-canonical-surface rule** shaped the design: slides are *regions*; the deck is the lone canonical
  *surface*. Sequence acyclicity is validator-enforced.
- Slide-model lineage (KEEP reference, not imported): `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_presentation/`.

## Completion Summary

Completed 2026-06-19 in session `session_stanley_20260619_174121_keystone_e4_4_deck_generator`.

### Deliverables
- [x] `what/production/deck_generator/` — packaged consumer (`adna-canvas-std` + `pyyaml`); `model`/`slides`/`layout`/
  `consume`/`__main__` + `__init__`; README/AGENTS/.gitignore.
- [x] `examples/canvas_standard_deck.{yaml,canvas}` — self-referential 6-slide deck (title · content · table · image ·
  content · quote); generated artifact **6 slides / 21 nodes / 13 edges**, deterministic.
- [x] `iii_quality_contract.md` — the persona-III + accuracy method as `iii/`-wrapper contracts.
- [x] `tests/` — **16 passed**, `ruff` clean; `canvas-std validate` → `level_reached=adna_native [OK]`, degradation
  `{D-1,D-2,D-3}=True`; no regression (`canvas_std` 46/8, `brief_consumer` 10/10).

### Key findings
- **The brief pattern generalizes cleanly to multi-region.** Slides-as-groups + one canonical deck surface + per-slide
  regions + a `sequence` chain validated at aDNA-Native first try; the only post-`to_canvas` touch is `isStartNode`
  (an Advanced-Canvas field the round-trip layer doesn't carry from source — same shape as the brief's heading color).
- **Image + table degrade faithfully** — image → file/link node (`degrades_to`), table → markdown text node; both
  survive `strip` as valid baseline nodes. `component_types.qualities` is additive (the validator ignores it).

### Spec-gap probe (objective implicit)
- **No gap blocked the deck.** **Latent notes (not errata):** (1) **speaker notes** have no home in the component
  model yet (a `caption`/`code` class is the nearest; a `notes` semantic_type may be worth a v2.0.x errata); (2)
  **per-claim provenance** is deck-level (`context_object.refs`) — a per-node ref map would make the accuracy-auditor
  lens mechanical (noted in `iii_quality_contract.md` §2); (3) slide **transitions/animation** are out of the static
  substrate's scope (correctly a producer/render concern). Filed as observations for E5/PT-P5, no change proposed now.

## AAR

- **Worked**: Reusing the E4.3 pattern made this fast — same source-contract → `to_canvas` → `_reserved`-enrichment
  spine, extended to multi-region. Grounding the A-5 `panel_link` rules first (exactly one canonical surface;
  `sequence` acyclicity; `extent.unit: "slides"`) meant the deck validated aDNA-Native on the first full run (16/16).
- **Didn't**: No renderer (canvas_std validates/round-trips, doesn't rasterize) — pixel render + scoring stay
  PT-P5-gated; the persona-III method is captured as a *contract*, wired at E5.1, not run here.
- **Finding**: Two consumers now share an identical authoring spine (source contract + `_reserved` enrichment +
  the four-property test contract) — a future `adna_canvas_authoring` helper could factor it once a 3rd consumer
  appears (premature at n=2). Image/table proved the component model carries rich types with clean degradation.
- **Change**: Established the **multi-region** consumer pattern (deck = canonical surface; sub-units = regions +
  `sequence`) as the reuse template for any paged/sequenced output (slides, chapters, comic pages).
- **Follow-up**: E5.1 wires `iii/` to `iii_quality_contract.md`; PT P5 adds the render loop + the external Lattice-brief
  fidelity comparison; consider the speaker-notes / per-claim-ref errata at the next spec pass. ⛔ E4→E5 stays a gate;
  E4.1/E4.2 stay gated on the D3 touch.
