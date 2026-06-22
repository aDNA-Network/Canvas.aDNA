---
type: context
created: 2026-06-22
updated: 2026-06-22
status: active
last_edited_by: agent_stanley
tags: [canvas, letter, quality, iii, contract, palette, p2, persona-review, accuracy]
---

# Letter Quality Contract — persona-III inspect + accuracy gates (Operation Palette P2)

Captures the letter-generator's review **method** as a **contract**, not an engine. It is the spec the producer
conforms to and that an `iii/` wrapper wires to. Per Canvas doctrine the engines stay in their owning vaults — review/
scoring is **III** (consumed via an `iii/` wrapper, C6); pixel/layout-render scoring is **PT-P5-gated**. The letter
generator (`build_letter`) produces a conformant **object**; *this contract* governs how that object is **reviewed and
accuracy-gated**. Nothing here imports an engine (substrate-neutrality, C8).

> **Status:** contract only. The `iii/` wrapper + running review loop are wired at the campaign's structural review (P4).

## 1. Persona-diverse III inspect panel (lenses)

Each letter is inspected through independent lenses; findings logged by severity; the letter iterates to **0 High /
0 Med** before ship. Panel composition is a producer choice; the contract is **"≥1 rigor lens + 1 accuracy lens,
always."**

| Lens | Asks |
|------|------|
| **Correctness** | Are all required blocks present and in reading order (salutation before body before closing/signature)? Does the recipient/date/sender match the brief? |
| **Tone / register** | Is the register appropriate to the recipient and purpose (formal/cordial/persuasive)? Consistent voice; no contradictions between salutation, body, and closing? |
| **Legibility (information designer)** | Does the single-page column read top-to-bottom cleanly? Do blocks fit one page (`extent.max == 1`)? Is paragraph length reasonable? |
| **Rigor** | Any dates, names, figures, or commitments stated precisely and consistently (e.g. the date block matches any in-body date)? |
| **Accuracy auditor** | Every factual claim (names, titles, dates, attributed facts) traced to a source path; synthesis marked as synthesis (§2). |

## 2. Accuracy guardrails (verify-or-omit + GAP register)

- **Verify-or-omit:** every factual datum (recipient name/title, dates, cited facts) traces to a verifiable source, or
  it is omitted — never invented or approximated.
- **Mark synthesis as synthesis:** inferred/softened claims are labeled, not presented as sourced fact.
- **GAP register:** anything the source cannot support is logged (not silently written into the letter).

**Contract surface:** these gates operate over `context_object.refs` + per-block `component_types`. The generator emits,
per block, the `component_types` (`class: text` + `semantic_type`) and `panel_link` (reading_order edges, the
`letter_root` region, the single canonical surface) an `iii/` review needs; the generator does not score itself.

## 3. Where this binds (conformance points)

| Stage | Owner | Gate |
|-------|-------|------|
| Build the letter object | `letter_generator` (this vault) | v2.0.0 aDNA-Native conformance (enforced by `canvas_std`) |
| Structural review (correctness, tone, legibility, refs) | III via `iii/` wrapper | 0 High / 0 Med across lenses |
| Pixel/layout render + overflow scoring | render engine (PT-P5) | render loop green |
| Accuracy (verify-or-omit, GAP) | accuracy-auditor + rigor lenses | 0 unverified facts |

## 4. Non-goals (doctrine)
- **No engine here.** Specifies contracts; imports/runs nothing (C8).
- **No re-implementation** of III's review or any render engine (C6) — wire to them, don't fork them.

## Related
- The generator: `src/letter_generator/` (`build_letter`). The Standard: `what/code/canvas_std/`.
- Sibling contracts: `what/production/{deck_generator,diagram_generator}/iii_quality_contract.md`.
- Shape source: `what/specs/spec_federation_contract.md §6.3`.
