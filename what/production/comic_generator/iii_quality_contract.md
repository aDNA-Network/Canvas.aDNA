---
type: context
created: 2026-06-21
updated: 2026-06-21
status: active
last_edited_by: agent_stanley
tags: [canvas, comic, quality, iii, contract, atelier, a2, persona-review, accuracy]
---

# Comic Quality Contract — persona-III inspect + accuracy gates (Operation Atelier A2)

This captures the comic-generator's reusable **method** as a **contract**, not an engine. It is the spec the comic
generator conforms to and that an `iii/` wrapper wires to. Per Canvas doctrine, **the engines stay in their owning
vaults** — the review/scoring engine is **III** (consumed via an `iii/` wrapper, C6), the pixel render + per-panel
scoring live in **ComfyUI** + the absorbed `canvas_presentation` (**PT-P5-gated**), and image generation is ComfyUI.
The comic generator (`build_comic`) produces a conformant comic **object** carrying each panel's image **PROMPT** as
metadata; *this contract* governs how that object is **reviewed and accuracy-gated** when an engine is wired up.

> **Status:** contract only. The `iii/` wrapper + the running review loop are wired at **E5.1** (III pin confirm); the
> pixel-render + per-panel scoring at **PT P5** (when `canvas_presentation` + the ComfyUI render path land). Nothing
> here imports an engine or renders a pixel. The generator **does not score itself** — it emits the metadata a review
> needs.

> **Source of the measurable dimensions.** The legacy CanvasForge `ComicReport.review()` rubric (structural / content
> / production / quality scoring, the 6-dimension `quality_review` weights) is the **source of the measurable
> dimensions below** — it is NOT shipped code (the producer carries no `review()` method; scoring is III/`canvas_
> presentation`). The dimensions are restated here as contract lenses.

## 1. Persona-diverse III inspect panel (5 lenses)

Each rendered/structural page is inspected through **five independent lenses**; findings are logged by
`module_iii_inspect_visual` severity; the comic iterates to **0 High / 0 Med across all personas** before ship.

| Lens | Asks |
|------|------|
| **Visual-narrative coherence** | Does the page read as a story — panel-to-panel flow, beat clarity, scene continuity across the `sequence` chain? Do `reading_order` + `adjacency` match the intended eye path? |
| **Character consistency** | Is each character on-model across panels (the character-bible descriptor honored; story-state mood/pose continuous between spreads)? |
| **Composition / panel hierarchy** | One beat per panel; legible focal point; gutter rhythm; balloon space reserved where declared; splash/spread panels earn their scale. |
| **Quantitative / rigor** | Page-count band; panel coverage; color-script continuity; aspect-ratio fit (see §2). |
| **Accuracy auditor** | Every story/world fact traced to a source (the storyboard / character-bible / color-script refs); synthesis marked as synthesis (§3). |

*(The lenses are audience-parameterized — a kids' explainer comic and a clinical-education comic weight them
differently. The panel composition is a producer choice; the contract is "≥1 rigor lens + 1 accuracy lens, always.")*

**Contract:** the comic generator emits, per panel, the `component_types` + `panel_link` metadata an `iii/` review
needs — a `semantic_type` per node (`comic`/`spread`/`page`/panel-type), the `reading_order`/`sequence`/`adjacency`
structure, the per-panel `qualities.image_prompt` (+ `dual_prompt`, `spatial_layout`, `aspect_ratio`, `status`), and
the `context_object.refs` source set. The review engine (III) consumes this; the generator does not score itself.

## 2. Quantitative gates (the measurable dimensions; restated from the legacy rubric)

These operate over the structural metadata the generator emits — **no engine here**:

- **Page-count band** — pages fall in the genre's expected band (the legacy rubric used 28–34 for a standard issue;
  the band is a producer/genre parameter, not a Standard rule). Out-of-band → a logged finding, not a hard fail.
- **Panel coverage** — every page carries ≥1 panel; every panel carries a non-empty `qualities.image_prompt` **and**
  an `aspect_ratio`. *(Enforced structurally by `tests/test_panel_coverage.py`.)*
- **Color-script continuity** — no gaps in the per-spread color-script sequence (a spread referenced by a page resolves
  to a `color_script` row); lighting reads continuously across adjacent spreads.
- **Reading-path coverage** — every multi-panel page's `reading_order` visits each panel once; the `sequence` chain
  spans all pages and is acyclic. *(Enforced by `tests/test_panel_coverage.py` + `test_roundtrip.py`.)*
- **Character-presence balance** — characters appear across the content pages at the genre's expected density (the
  legacy rubric's ≥70% content-page coverage); supplied via the story-state overlay.

## 3. Accuracy guardrails (verify-or-omit + GRAPH-GAP)

- **Verify-or-omit:** every story/world fact a panel asserts must trace to a verifiable source (the storyboard /
  character-bible / color-script in `context_object.refs`), or it is **omitted** — never invented to fill a beat.
- **Mark synthesis as synthesis:** inferred/aggregated narrative is labeled, not presented as canon.
- **GRAPH-GAP register:** anything the source material cannot support is logged in a register (not silently filled),
  feeding back as storyboard/bible work or an explicit "out of scope" note.

**Contract surface:** these gates operate over `context_object.refs` + per-panel provenance. A future `comic-generator`
option SHOULD accept per-panel source refs (panel → ref) so the auditor lens is mechanical; until then refs are
comic-level (`context_object.refs`).

## 4. Where this binds (conformance points)

| Stage | Owner | Gate |
|-------|-------|------|
| Build the comic object (panels carry PROMPTS, not pixels) | `comic_generator` (this vault) | v2.0.0 aDNA-Native conformance (already enforced by `canvas_std`) |
| Structural review (narrative flow, character consistency, hierarchy, refs present) | III via `iii/` wrapper (E5.1) | 0 High / 0 Med across lenses |
| Image generation (the panel PROMPTS → pixels) | **ComfyUI** | per-panel render path |
| Pixel render + per-panel scoring + hard gates (pending-image, balloon overlap, on-model) | `canvas_presentation` (PT-P5) | render loop green |
| Accuracy (verify-or-omit, GRAPH-GAP) | accuracy-auditor lens | 0 unverified story facts |

## 5. Non-goals (doctrine)
- **No engine here.** This file specifies contracts; it imports nothing and runs nothing (substrate-neutrality, C8).
- **No pixels here.** The producer emits PROMPTS only — image generation is ComfyUI; pixel scoring is
  `canvas_presentation` (PT-P5). The producer never renders.
- **No re-implementation** of III's review or `canvas_presentation`'s scoring (C6) — wire to them, don't fork them.
- **No `review()` in the producer.** The legacy `ComicReport.review()` rubric is the *source of the measurable
  dimensions* (§2), not shipped code.

## Related
- The generator: `src/comic_generator/` (`build_comic`). The Standard: `what/code/canvas_std/`.
- Sibling contracts: `../deck_generator/iii_quality_contract.md` · `../document_generator/iii_quality_contract.md` ·
  `../diagram_generator/iii_quality_contract.md`.
- Wiring: **E5.1** (`iii/` wrapper + III pin) · **PT P5** (`canvas_presentation` render/scoring + ComfyUI render path).
- Comic-engine lineage (KEEP reference, not a dependency): `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_comic/`
  (`comic.py` `ComicReport.review()` = the rubric source; `_rlhf_hints.py`; `mermaid_layout.py`).
