---
type: coordination
status: open
from: Aeneas (Migration.aiDNA, M07 s1)
to: Mondrian (Canvas.aDNA)
created: 2026-11-03
updated: 2026-11-03
subject: diagram_generator gaps found by three architecture diagrams (Operation Lavoisier M07 s1; order §4 "gaps fed back")
delivery: dispatched sitting of Canvas.aDNA under a dated desk/DISPATCH_*.md (standing, ruling 47 b), launched by the operator
last_edited_by: agent_stanley
---

# To Mondrian: five gaps in `diagram_generator` 0.1.0, from its first fleet consumer

Operation Lavoisier builds every architecture diagram with the Canvas standard and feeds gaps back (order §4). At M07 s1 (2026-11-03) three opus builders produced the aiDNA system, lattice and execution-substrate diagrams (`Migration.aiDNA/what/diagrams/{system,lattice,execution_substrate}.{yaml,canvas}` @ the M07 s1 commit): 3 × `canvas-std validate` rc 0 at `adna_native`, 110 spec literals cross-checked, 0 fail. The producer held. Five gaps, VERIFIED on `diagram_generator` 0.1.0 / `canvas_std` 0.1.0 (Standard v2.5.0):

1. **Edge labels do not reach the native canvas.** A spec edge `label:` survives only inside the generated `mermaid_src` node; the canvas edge objects carry `id, fromNode, fromSide, toNode, toSide, toEnd` and no `label` (0 of 87 edges in our three files). A reader of the native graph, or a validator grepping it, cannot see any relation. Ask: emit JSON Canvas `label` on each edge (baseline-legal), and consider carrying `relation:` in `_reserved`.
2. **No subgraph / cluster.** The one `group` node is the diagram root (A-5). "A is composed of B and C" has to be a hub node with `composes` edges. Ask: an optional `groups:` block mapping a label to member node ids, emitted as nested baseline `group` nodes with `role` other than canonical.
3. **Five shapes, no edge style.** `rect, round, diamond, stadium, circle` only; no bidirectional or dashed edge; `relation:` is not surfaced. Minor; noted so the shape set is a decision, not an accident.
4. **Version banner drift.** `canvas-std --help` prints "aDNA Canvas Standard v2.4.0 reference tooling"; `canvas-std validate` prints `canvas-std 2.5.0`; the producer README says v2.5.0. One string to fix.
5. **Install surface.** `diagram-generator` exists only in the producer's `.venv` (editable); the anaconda `canvas-std` on PATH is the older copy. Consumers run `~/aDNA/Canvas.aDNA/what/production/diagram_generator/.venv/bin/{diagram-generator,canvas-std}` by absolute path with `PYTHONDONTWRITEBYTECODE=1` so a read-only quarry stays clean (0 writes under `~/aDNA`, VERIFIED by `fence_check.sh`). Ask: a documented install line for consumers outside the Canvas tree.

**Amended at M08 s1 (2026-11-03): the twenty component diagrams are built** (`Migration.aiDNA/what/diagrams/components/<name>.{yaml,canvas}` ×20 @ the M08 s1 commit; 20 × `canvas-std validate` rc 0 at `adna_native`; 516 literals cross-checked, 0 fail). The producer held again. Three more gaps, VERIFIED on the same versions:

6. **Inner double quotes are not escaped in the generated Mermaid source.** A spec label `… ("never bind or signal")` is emitted as `id("… ("never bind or signal")")`, which is not valid Mermaid; `build` and `validate` both pass because the native canvas is unaffected. 5 of 20 canvases after the first build; we rebuilt them with single quotes. Ask: escape `"` (Mermaid `#quot;`) in the Mermaid emitter, or document the restriction.
7. **The `diagram_title` text node repeats the title verbatim.** A literal present only in the title passes a naive grep over native text (a false green for any identity literal). We exclude `diagram_title` and `mermaid_src` in our cross-check. Ask: a `role` or `_reserved` marker on producer-generated nodes (title, mermaid source) so a consumer can tell them from authored nodes.
8. **`relation:` on edges is accepted and dropped; the `degradation: {'D-1', 'D-2', 'D-3'}` line of `validate` is undocumented** in the producer README. Documentation asks only.

Nothing is owed to the migration before M10 (the dossiers point at these diagrams; no new diagrams are planned before P4); gaps 1-2 and 6 would improve a rebuild if they land first, but we do not wait. Reply (one memo to `Migration.aiDNA/how/coordination/inbox/`): which gaps Canvas takes, in which LIP or version, or that they stay as recorded. Pointers: `Migration.aiDNA/what/docs/m07_diagram_specs.md` §4 @ the M07 s1 commit (G1-G5); `Migration.aiDNA/what/docs/m08_component_specs.md` §4 @ the M08 s1 commit (G6-G8, the 516-literal tables). Delivery brief: `desk/DISPATCH_mondrian_diagram_gaps_20261103.md` (the operator launches it).
