# AGENTS.md — diagram_generator (Canvas.aDNA / what/production/)

**Scope:** the reference diagram consumer built at Operation Atelier **A1** — a diagram spec → a v2.0.0-conformant
diagram `.canvas` (a native typed graph on one canonical surface + a derived Mermaid `code` node). **Producer code** on
the `what/production/` shelf, not the Standard.

## Load this when
- Working on the diagram generator, or building another graph/typed-relation consumer.

## Rules
- **Never edit `what/code/canvas_std/` from here** — import it (the installed `adna-canvas-std`), never modify it
  (C8). The `canvas_core` Mermaid module in the CanvasForge archive is a **KEEP-reference quarry** that was *ported*
  here (`mermaid.py`, theme coupling stripped); do not import it.
- **The diagram contract** (load-bearing): `diagram_root` group = the **single canonical surface** (A-5: exactly one
  `role: canonical`); the whole graph is one `panel_link.region`. Diagram nodes are baseline `text` nodes whose
  Mermaid shape rides **only** in `_reserved.component_types[*].qualities.shape` — **never** baseline
  `styleAttributes.shape` (the `VALID_SHAPES` enum lacks rect/round/stadium → E-2/D-2 trap).
- **Edge-kind mapping** (respect A-5 acyclicity): `gantt` → `sequence` (linear, acyclic); **everything else** →
  `dependency` (cycles permitted — a cyclic flowchart/state diagram MUST validate).
- **The four+1 properties are the contract** (see `tests/`): conformance @ aDNA-Native, round-trip
  (`compute_sync_hash` stable; a cyclic flowchart round-trips), degradation (`strip` → Core/Extended-valid; NO
  out-of-enum `styleAttributes.shape`), **components** (shape→text, mermaid_src→code/text), and per-diagram-type kinds.
- **`to_canvas` injects only `_reserved.sync`** — `consume.build_diagram` enriches `_reserved` to aDNA-Native. Diagram
  source nodes carry **no** `semantic_type` (so `to_canvas`'s `lattice` profile injects no color/shape).
- **Layout is producer-side** (`layout.py` ranks; `diagrams.py` interior text). Geometry is integer + deterministic.

## Pointers
- Sibling pattern: `what/production/deck_generator/` (slides = group nodes; the multi-region precedent).
- Standard API: `what/code/canvas_std/src/canvas_std/` (`roundtrip.py` source contract; `reserved.py` A-* + `PL_*`).
- Quarry (ported, not imported): `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_core/mermaid.py`.
- Quality contract: `iii_quality_contract.md`.
