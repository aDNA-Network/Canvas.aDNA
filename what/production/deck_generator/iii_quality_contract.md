---
type: context
created: 2026-06-19
updated: 2026-06-19
status: active
last_edited_by: agent_stanley
tags: [canvas, deck, quality, iii, contract, keystone, e4_4, persona-review, accuracy]
---

# Deck Quality Contract — persona-III inspect + accuracy gates (Keystone E4.4)

This captures the deck-generator pilot's reusable **method** as a **contract**, not an engine. It is the spec the
deck generator conforms to and that an `iii/` wrapper wires to. Per Canvas doctrine, **the engines stay in their
owning vaults** — the review/scoring engine is **III** (consumed via an `iii/` wrapper, C6), the render loop +
24-criterion scoring live in the absorbed `canvas_presentation` (**PT-P5-gated**), and image generation is ComfyUI.
The deck generator (`build_deck`) produces a conformant deck **object**; *this contract* governs how that object is
**reviewed and accuracy-gated** when an engine is wired up.

> **Status:** contract only. The `iii/` wrapper + the running review loop are wired at **E5.1** (III pin confirm) and
> the pixel-render review at **PT P5** (when `canvas_presentation` lands). Nothing here imports an engine.

## 1. Persona-diverse III inspect panel (5 lenses)

Each rendered/structural slide is inspected through **five independent lenses**; findings are logged by
`module_iii_inspect_visual` severity; the deck iterates to **0 High / 0 Med across all personas** before ship.

| Lens | Asks |
|------|------|
| **Domain architect** | Is the technical substance correct and current for this audience? |
| **Quantitative/rigor** | Are numbers, units, baselines, and comparisons sound (see §2)? |
| **Skeptical executive** | Does each slide earn its place; is the through-line and the ask clear? |
| **Information designer** | One idea per slide; legible hierarchy; signal-to-ink; containment. |
| **Accuracy auditor** | Every claim traced to a source path; synthesis marked as synthesis (§2). |

*(The lenses are audience-parameterized — e.g., the pilot used web3/DLT-architect + cryptoeconomics for a Lattice
Protocol deck. The panel composition is a producer choice; the contract is "≥1 rigor lens + 1 accuracy lens, always.")*

**Contract:** the deck generator emits, per slide, the `component_types` + `panel_link` metadata an `iii/` review
needs (a `semantic_type` per node, a `reading_order`/`sequence` structure, and the `context_object.refs` source set).
The review engine (III) consumes this; the generator does not score itself.

## 2. Accuracy guardrails (verify-or-omit + GRAPH-GAP)

- **Verify-or-omit:** every quantitative claim must trace to a verifiable source path, or it is **omitted** — never
  approximated. *(Pilot win: an auditor caught a "21.5× accuracy" figure that was 21.5% absolute from a 1.0%
  baseline → omitted.)*
- **Mark synthesis as synthesis:** inferred/aggregated statements are labeled, not presented as sourced fact.
- **GRAPH-GAP register:** anything the source graph cannot support is logged in a register (not silently filled),
  feeding back as graph work or an explicit "out of scope" note.

**Contract surface:** these gates operate over `context_object.refs` + per-node provenance. A future
`deck-generator` option SHOULD accept per-claim source refs (slide/bullet → ref) so the auditor lens is mechanical;
until then refs are deck-level (`context_object.refs`).

## 3. Where this binds (conformance points)

| Stage | Owner | Gate |
|-------|-------|------|
| Build the deck object | `deck_generator` (this vault) | v2.0.0 aDNA-Native conformance (already enforced by `canvas_std`) |
| Structural review (one-idea-per-slide, hierarchy, refs present) | III via `iii/` wrapper (E5.1) | 0 High / 0 Med across lenses |
| Pixel render + 24-criterion scoring + hard gates (pending-image, overlap, containment) | `canvas_presentation` (PT-P5) | render loop green |
| Accuracy (verify-or-omit, GRAPH-GAP) | accuracy-auditor lens | 0 unverified quantitative claims |

## 4. Non-goals (doctrine)
- **No engine here.** This file specifies contracts; it imports nothing and runs nothing (substrate-neutrality, C8).
- **No re-implementation** of III's review or `canvas_presentation`'s scoring (C6) — wire to them, don't fork them.

## Related
- Pilot + method: `how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot.md`.
- The generator: `src/deck_generator/` (`build_deck`). The Standard: `what/code/canvas_std/`.
- Wiring: Keystone **E5.1** (`iii/` wrapper + III pin) · **PT P5** (`canvas_presentation` render/scoring).
