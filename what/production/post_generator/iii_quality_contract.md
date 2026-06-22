---
type: context
created: 2026-06-22
updated: 2026-06-22
status: active
last_edited_by: agent_stanley
tags: [canvas, post, social, quality, iii, contract, palette, p3, persona-review, accuracy]
---

# Post Quality Contract — persona-III inspect + accuracy gates (Operation Palette P3)

Captures the post-generator's review **method** as a **contract**, not an engine. It is the spec the producer conforms
to and that an `iii/` wrapper wires to. Per Canvas doctrine the engines stay in their owning vaults — review/scoring is
**III** (via an `iii/` wrapper, C6); image generation is **ComfyUI**; pixel/render scoring is **PT-P5-gated**. The
generator (`build_post`) emits a conformant **object** + the metadata a review needs; it does not score or render itself
(substrate-neutrality, C8 — this file imports nothing).

> **Status:** contract only. The `iii/` wrapper + running review loop are wired at the campaign's structural review (P4).

## 1. Persona-diverse III inspect panel (lenses)

Inspect each post/thread through independent lenses; log findings by severity; iterate to **0 High / 0 Med** before
ship. Panel composition is a producer choice; the contract is **"≥1 rigor lens + 1 accuracy lens, always."**

| Lens | Asks |
|------|------|
| **Correctness** | Does the thread read in order (`sequence` chain, `isStartNode` on panel 0)? Does each panel stand alone yet advance the thread? |
| **Hook / engagement** | Does panel 0 earn the open? Is each panel tight and scannable? |
| **Platform fit** | Is each panel within the platform `char_budget` (advisory)? Does the image `aspect` match the platform? Is the tone right for the channel? |
| **Rigor** | Any claims/numbers precise and consistent across panels? |
| **Accuracy auditor** | Every factual claim traced to a source path; synthesis marked as synthesis (§2). The image is a **prompt**, never a sourced photo. |

## 2. Accuracy guardrails (verify-or-omit + GAP register)

- **Verify-or-omit:** every factual claim traces to a verifiable source, or it is omitted — never invented.
- **Mark synthesis as synthesis:** inferred claims are labeled; image prompts are clearly prompts, not evidence.
- **GAP register:** anything the source cannot support is logged (not silently posted).

**Contract surface:** these gates operate over `context_object.refs` + per-panel `component_types`. The generator emits,
per panel, the `component_types` (`class: text|image` + `semantic_type` + `qualities.image_prompt`/`chars`) and
`panel_link` (the `sequence` thread chain, `adjacency` post→image, the `post_root` region, the single canonical surface)
a review needs; it does not score itself.

## 3. Where this binds (conformance points)

| Stage | Owner | Gate |
|-------|-------|------|
| Build the post object | `post_generator` (this vault) | v2.0.0 aDNA-Native conformance (enforced by `canvas_std`) |
| Image generation | ComfyUI (from `qualities.image_prompt`) | rendered asset matches the prompt + aspect |
| Structural review (correctness, hook, platform fit) | III via `iii/` wrapper | 0 High / 0 Med across lenses |
| Pixel/layout render scoring | render engine (PT-P5) | render loop green |
| Accuracy (verify-or-omit, GAP) | accuracy-auditor + rigor lenses | 0 unverified claims |

## 4. Non-goals (doctrine)
- **No engine here.** Specifies contracts; imports/runs nothing (C8).
- **No rendering or scoring in the producer** (C6/C8) — image generation → ComfyUI; review → III; wire to them.

## Related
- The generator: `src/post_generator/` (`build_post`). The Standard: `what/code/canvas_std/`.
- Sibling contracts: `what/production/{letter_generator,comic_generator,deck_generator}/iii_quality_contract.md`.
