---
type: context
created: 2026-06-19
updated: 2026-06-19
last_edited_by: agent_stanley
tags: [canvas, document, long-form, quality, iii, contract, keystone, e4_1, persona-review, accuracy]
---

# Document Quality Contract — persona-III inspect + accuracy gates (Keystone E4.1)

This captures the document-generator's reusable **method** as a **contract**, not an engine. It is the spec the
generator conforms to and that the `iii/` wrapper wires to. Per Canvas doctrine, **the engines stay in their owning
vaults** — the review/scoring engine is **III** (consumed via the `iii/` wrapper, C6), the render loop + pixel scoring
live in the absorbed `canvas_presentation` (**PT-P5-gated**), and image generation is ComfyUI. The generator
(`build_document`) produces a conformant document **object**; *this contract* governs how that object is **reviewed
and accuracy-gated**.

> **Status:** contract + structural review live (E5.1 wired the `iii/` wrapper, III pin v0.5.0). The **pixel-render**
> review (long-form typography, page breaks, figure placement) waits for **PT P5** (`canvas_presentation`). Nothing
> here imports an engine.

## 1. Persona-diverse III inspect panel (5 lenses)

Each section/page is inspected through **five independent lenses**; findings are logged by severity; the document
iterates to **0 High / 0 Med across all personas** before ship.

| Lens | Asks |
|------|------|
| **Domain architect** | Is the technical substance correct and current for this audience? |
| **Quantitative/rigor** | Are numbers, units, baselines, and comparisons sound (see §2)? |
| **Skeptical executive** | Does each section earn its place; is the through-line and the claim clear? |
| **Information designer** | One idea per section; legible heading hierarchy; signal-to-ink; figure/caption pairing. |
| **Accuracy auditor** | Every claim traced to a source path; synthesis marked as synthesis (§2). |

*(The panel composition is a producer choice; the contract is "≥1 rigor lens + 1 accuracy lens, always." Lenses are
audience-parameterized.)*

**Contract:** the generator emits, per node, the `component_types` + `panel_link` metadata an `iii/` review needs
(a `semantic_type` per node, a `reading_order`/`sequence` structure, and the `context_object.refs` source set). The
review engine (III) consumes this; the generator does not score itself.

## 2. Accuracy guardrails (verify-or-omit + GRAPH-GAP)

- **Verify-or-omit:** every quantitative claim must trace to a verifiable source path, or it is **omitted** — never
  approximated.
- **Mark synthesis as synthesis:** inferred/aggregated statements are labeled, not presented as sourced fact.
- **GRAPH-GAP register:** anything the source graph cannot support is logged in a register (not silently filled).

**Contract surface:** these gates operate over `context_object.refs` + per-section citations (`adjacency` from prose
to `link`/`citation` nodes). A future `document-generator` option SHOULD accept per-claim source refs so the auditor
lens is mechanical; until then refs are section-level (`sources:`) + document-level (`context_object.refs`).

## 3. Where this binds (conformance points)

| Stage | Owner | Gate |
|-------|-------|------|
| Build the document object | `document_generator` (this vault) | v2.0.0 aDNA-Native conformance (enforced by `canvas_std`) |
| Structural review (heading hierarchy, one-idea-per-section, citations present, figure↔caption pairing) | III via `iii/` wrapper (E5.1) | 0 High / 0 Med across lenses |
| Pixel render + long-form scoring (typography, page breaks, orphan/widow, figure placement) | `canvas_presentation` (PT-P5) | render loop green |
| Accuracy (verify-or-omit, GRAPH-GAP) | accuracy-auditor lens | 0 unverified quantitative claims |

## 4. Non-goals (doctrine)
- **No engine here.** This file specifies contracts; it imports nothing and runs nothing (substrate-neutrality, C8).
- **No re-implementation** of III's review or `canvas_presentation`'s scoring (C6) — wire to them, don't fork them.
- **No genre pipeline here.** Trap-packs, reviewer voices, reward rubrics, and per-genre format/visual contracts are
  producer-side config migrated in **E4.2** — out of scope for the E4.1 skeleton.

## Related
- Mission: `how/campaigns/campaign_canvas_genesis/missions/mission_e4_1_lf_successor.md`.
- The generator: `src/document_generator/` (`build_document`). The Standard: `what/code/canvas_std/`.
- Wiring: Keystone **E5.1** (`iii/` wrapper + III pin) · **PT P5** (`canvas_presentation` render/scoring).
- LF quarry (E4.2 migration source): `Archive.aDNA/LiteratureForge.aDNA/what/specs/`.
