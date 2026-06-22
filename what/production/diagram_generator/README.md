# diagram-generator — reference diagram consumer (Operation Atelier A1)

A net-new consumer of the **aDNA Canvas Standard v2.0.0**, and the worked port of CanvasForge's Mermaid generators.
It turns a structured **diagram spec** (a typed graph: flowchart · sequence · class · state · gantt) into a
v2.0.0-conformant **diagram `.canvas`** — proven **end-to-end on `canvas_std` alone**: aDNA-Native conformance,
round-trip stability, degradation to a valid baseline Obsidian canvas, and faithful **shape / code** components.

## The mapping (hybrid, native-primary)

- The whole diagram is **one `group` node = `diagram_root` = the single canonical surface** (A-5: exactly one
  `role: canonical`).
- Each diagram node → an interior baseline **`text`** node. Its Mermaid shape rides **only** in
  `_reserved.component_types[*].qualities.shape` (`class: "shape"`, `degrades_to: "text"`) — we **never** set baseline
  `styleAttributes.shape`, because the canvas `VALID_SHAPES` enum lacks rect/round/stadium (setting it would fail
  E-2/D-2).
- Each diagram edge → a baseline edge with a panel-link `kind`. **`gantt` task order → `sequence`** (a linear, acyclic
  chain — the only acyclicity-checked kind); **all other types → `dependency`**, so a flowchart or state diagram
  **with a cycle still validates**.
- PLUS one derived **`mermaid_src`** node (`class: "code"`, `qualities.language: "mermaid"`, `degrades_to: "text"`)
  carrying the generated Mermaid source — the render-fidelity twin of the native graph.

> **canvas_std is a validator + round-tripper, not a renderer.** "End-to-end" = a conformant, round-trippable,
> degradable diagram **object**. Pixel/layout-render scoring is **PT-P5-gated**; the persona-III + accuracy gates are
> captured as a *contract* (`iii_quality_contract.md`), with the review engine staying in III (C6/C8).

## Use

```bash
diagram-generator build examples/canvas_standard_flow.yaml examples/canvas_standard_flow.canvas
canvas-std validate examples/canvas_standard_flow.canvas        # -> level_reached=adna_native [OK]
```

```python
from diagram_generator import build_diagram, load_diagram
doc = build_diagram(load_diagram("examples/canvas_standard_flow.yaml"))   # -> a v2.0.0 aDNA-Native diagram .canvas
```

## Layout

```
src/diagram_generator/
  model.py     # DiagramInput / DiagramNode / DiagramEdge + load_diagram — substrate-free domain model
  mermaid.py   # PORTED Mermaid syntax generators (flowchart/sequence/class/state/gantt) — theme coupling stripped
  diagrams.py  # diagram-node -> interior baseline node + its shape component entry (the slides.py analog)
  layout.py    # deterministic layered integer geometry (ranks; rows for TD/BT, columns for LR/RL)
  consume.py   # DiagramInput -> canvas_std source contract -> to_canvas -> enrich _reserved to aDNA-Native
  __main__.py  # diagram-generator CLI
examples/      # a self-referential flowchart ABOUT the generator + the generated .canvas
iii_quality_contract.md   # correctness/legibility/render-fidelity + rigor/accuracy lenses (engine in III; render P5)
tests/         # conformance · round-trip (incl. a cyclic flowchart) · degradation (shape-enum trap) · components · types
```

## Develop / test

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ../../code/canvas_std        # the Standard (zero-dep) first; provides adna-canvas-std + the canvas-std CLI
pip install -e ".[dev]"
python -m pytest -q && ruff check src tests
```

Governed by the aDNA Canvas Standard (LIP process, `adr_003`); sited per `adr_004_production_code_layout`.
Mermaid-generator lineage (KEEP reference, not a dependency): `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_core/mermaid.py`.
