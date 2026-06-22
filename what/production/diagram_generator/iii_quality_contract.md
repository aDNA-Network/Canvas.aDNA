---
type: context
created: 2026-06-21
updated: 2026-06-21
status: active
last_edited_by: agent_stanley
tags: [canvas, diagram, quality, iii, contract, atelier, a1, persona-review, accuracy]
---

# Diagram Quality Contract — persona-III inspect + accuracy gates (Operation Atelier A1)

This captures the diagram-generator's reusable **method** as a **contract**, not an engine. It is the spec the
diagram generator conforms to and that an `iii/` wrapper wires to. Per Canvas doctrine, **the engines stay in their
owning vaults** — the review/scoring engine is **III** (consumed via an `iii/` wrapper, C6), and pixel/layout-render
scoring is **PT-P5-gated**. The diagram generator (`build_diagram`) produces a conformant diagram **object**; *this
contract* governs how that object is **reviewed and accuracy-gated** when an engine is wired up. Nothing here imports
an engine (substrate-neutrality, C8).

> **Status:** contract only. The `iii/` wrapper + the running review loop are wired at **E5.1** (III pin confirm) and
> the pixel/layout-render review at **PT P5**.

## 1. Persona-diverse III inspect panel (lenses)

Each structural/rendered diagram is inspected through independent lenses; findings are logged by severity; the
diagram iterates to **0 High / 0 Med across all personas** before ship. The panel composition is a producer choice;
the contract is **"≥1 rigor lens + 1 accuracy lens, always"** (mandatory for any quantitative diagram).

| Lens | Asks |
|------|------|
| **Correctness** | Does the graph faithfully represent the relations — no phantom edges, no missing edges, no mis-typed relation? Does each node's role/shape match its semantics? |
| **Legibility (information designer)** | Does the layout read naturally for its `direction`? Do labels fit their nodes? Is the flow uncluttered (signal-to-ink, containment)? |
| **Render fidelity** | Does the derived Mermaid `code` node render the **same** graph as the native typed nodes/edges — same nodes, same edges, same relations? (The two must not drift.) |
| **Quantitative / rigor** | For gantt: are durations, units, and task ordering sound? For class diagrams: are cardinalities and relation glyphs (inherits/composition/aggregation) correct? |
| **Accuracy auditor** | Every claim/relation traced to a source path; synthesis marked as synthesis (§2). |

## 2. Accuracy guardrails (verify-or-omit + GRAPH-GAP)

- **Verify-or-omit:** every quantitative datum (a gantt duration, a class cardinality, an edge that asserts a real
  dependency) must trace to a verifiable source path, or it is **omitted** — never approximated or invented.
- **Mark synthesis as synthesis:** inferred/aggregated relations are labeled, not presented as sourced fact.
- **GRAPH-GAP register:** any relation the source cannot support is logged in a register (not silently drawn),
  feeding back as graph work or an explicit "out of scope" note.

**Contract surface:** these gates operate over `context_object.refs` + per-node component metadata. The generator
emits, per node, the `component_types` (`class` + `semantic_type` + `qualities.shape`) and `panel_link` (edge `kind`s,
the `diagram_root` region, the single canonical surface) an `iii/` review needs; the generator does not score itself.

## 3. Where this binds (conformance points)

| Stage | Owner | Gate |
|-------|-------|------|
| Build the diagram object | `diagram_generator` (this vault) | v2.0.0 aDNA-Native conformance (enforced by `canvas_std`) |
| Render-fidelity (native graph ⇿ derived Mermaid `code` node) | render-fidelity lens | the two describe the same graph |
| Structural review (correctness, legibility, refs present) | III via `iii/` wrapper (E5.1) | 0 High / 0 Med across lenses |
| Pixel/layout render + overlap/containment scoring | render engine (PT-P5) | render loop green |
| Accuracy (verify-or-omit, GRAPH-GAP) | accuracy-auditor + rigor lenses | 0 unverified quantitative data |

## 4. Non-goals (doctrine)
- **No engine here.** This file specifies contracts; it imports nothing and runs nothing (substrate-neutrality, C8).
- **No re-implementation** of III's review or any render/scoring engine (C6) — wire to them, don't fork them.

## Related
- The generator: `src/diagram_generator/` (`build_diagram`). The Standard: `what/code/canvas_std/`.
- Sibling contract: `what/production/deck_generator/iii_quality_contract.md`.
- Wiring: **E5.1** (`iii/` wrapper + III pin) · **PT P5** (render/scoring engine).
