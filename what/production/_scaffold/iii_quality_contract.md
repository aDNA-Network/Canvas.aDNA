---
type: context
created: 2026-06-21
updated: 2026-06-21
status: active
last_edited_by: agent_stanley
tags: [canvas, production, scaffold, quality, iii, contract, template]
---

# <Producer> Quality Contract — persona-III inspect + accuracy gates  (TEMPLATE)

> **TODO(clone):** rename `<Producer>`; tailor the lenses to your domain; delete this banner.

Captures the producer's reusable review **method** as a **contract**, not an engine. It is the spec the producer
conforms to and that an `iii/` wrapper wires to. Per Canvas doctrine the engines stay in their owning vaults — review/
scoring is **III** (consumed via an `iii/` wrapper, C6); pixel/render scoring is **PT-P5-gated**. The producer emits a
conformant **object** + the metadata a review needs; it never scores itself (substrate-neutrality, C8 — this file
imports nothing).

## 1. Persona-diverse III inspect panel (lenses)

Inspect each artifact through independent lenses; log findings by severity; iterate to **0 High / 0 Med** before ship.
Panel composition is a producer choice; the contract is **"≥1 rigor lens + 1 accuracy lens, always."**

| Lens | Asks |
|------|------|
| **Correctness** | TODO(clone): does the artifact faithfully represent its source/intent? |
| **Legibility (information designer)** | TODO(clone): does the layout read naturally; do labels/text fit; is it uncluttered? |
| **<domain lens>** | TODO(clone): the domain-specific quality question (e.g. tone for a letter, hook/length for a post). |
| **Quantitative / rigor** | TODO(clone): any numbers/dates/limits sound? (mandatory for quantitative output) |
| **Accuracy auditor** | Every claim traced to a source path; synthesis marked as synthesis (§2). |

## 2. Accuracy guardrails (verify-or-omit + GAP register)

- **Verify-or-omit:** every factual datum traces to a verifiable source path, or it is omitted — never invented.
- **Mark synthesis as synthesis:** inferred content is labeled, not presented as sourced fact.
- **GAP register:** anything the source cannot support is logged (not silently emitted), feeding back as work.

**Contract surface:** these gates operate over `context_object.refs` + per-node `component_types`. The producer emits
the `component_types` + `panel_link` an `iii/` review needs; it does not score itself.

## 3. Where this binds (conformance points)

| Stage | Owner | Gate |
|-------|-------|------|
| Build the object | this producer | v2.0.0 aDNA-Native conformance (enforced by `canvas_std`) |
| Structural review | III via `iii/` wrapper | 0 High / 0 Med across lenses |
| Pixel/render scoring | render engine (PT-P5) | render loop green |
| Accuracy | accuracy-auditor + rigor lenses | 0 unverified data |

## 4. Non-goals (doctrine)
- **No engine here** — specifies contracts; imports/runs nothing (C8).
- **No re-implementation** of III's review or any render engine (C6) — wire to them, don't fork them.

## Related
- The generator: `src/<producer>/`. The Standard: `what/code/canvas_std/`.
- Sibling contracts: `what/production/{deck_generator,diagram_generator,comic_generator}/iii_quality_contract.md`.
