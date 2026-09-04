---
type: skill
skill_type: agent
created: 2026-09-04
updated: 2026-09-04
status: active
category: authoring
trigger: "Giving a prose artifact (context guide, ADR, spec, architecture doc) a conformant .canvas channel beside it — the dual-channel diagrammatic-context pattern"
last_edited_by: agent_mondrian
tags: [skill, canvas, diagrammatic_context, dual_channel, authoring, diagram_generator, blueprint]
---

# Skill: Author a Context Diagram (the dual-channel rail)

Give a prose artifact a **canvas channel**: prose owns *meaning*, the canvas owns *structure*, and
the two update in the same mission. Built on `diagram_generator`; proven 2× in Operation Blueprint P2
(`context_canvas_surface_legs`, `adr_004_production_code_layout`).

This skill is the **runbook**. The pattern is
`how/campaigns/campaign_canvas_blueprint/artifacts/draft_pattern_diagrammatic_context.md` (staged to
Rosetta; not yet ratified). The companion for building a *new producer* is
`skill_canvas_producer_build.md` — **this skill builds no producer**, it authors a canvas with one.

## When to use

A prose artifact whose subject is a **structure**: an architecture, a seam, a dependency graph, a
lifecycle, a decision with a topology. Load-bearing architectural artifacts SHOULD carry a canvas
channel; anything key MAY.

**Not** for: a canvas that is a build product of a machine source (that is `authority: generator`) ·
a visualization of an authoritative `.lattice.yaml` (that is `authority: view` — `adr_011`) · a 2D
*output* artifact like a deck or letter (that is a producer — `skill_canvas_producer_build.md`) ·
prose whose subject is genuinely a narrative. **A diagram of an argument is not diagrammatic
context.** If you cannot name the nodes and the edges without inventing them, do not draw it.

## Inputs

- The prose channel (`.md`) — already written; this rail never invents the content.
- `diagram_generator` (`what/production/diagram_generator/`) and the runner env below.

## Procedure

### 1. Write the spec YAML **beside the prose**

`<artifact>.diagram.yaml`, in the same directory as `<artifact>.md`. Both files are vault citizens
(REQ-H05) — openable, `[[wikilink]]`-able, searchable. Never a build directory.

```yaml
title: "…"                      # becomes the `#### ` title node AND the group label
id: "urn:adna:canvas:<leg>:<name>"
version: "1.0.0"                # ⚠ A-7 requires SEMVER
diagram_type: flowchart         # flowchart | sequence | class_diagram | state_diagram | gantt
direction: TD

authority: dual_channel         # the authority axis — see below
prose: what/context/<artifact>.md   # vault-relative; appended to context_object.refs as a wikilink

refs: ["[[adr_000_canvas_identity]]"]
nodes: [{ id: a, label: "…", shape: rect }]
edges: [{ from: a, to: b, label: "…" }]
```

**Version mapping.** `context_version: "1.1"` in prose frontmatter is **not semver** and A-7 rejects
it. Map `X.Y` → `X.Y.0`. An ADR with no version field starts at `1.0.0`.

**`authority` is required for context canvases** and the producer validates the enum
(`dual_channel` / `generator` / `view`). ⚠ `canvas_std` does **not** know this key (F-B1-2) — the
producer-side check is currently the only enforcement anywhere, which is exactly why you declare it
in the YAML rather than hand-editing it into the JSON afterwards. `prose:` is legal **only** under
`dual_channel`, because a prose pair is what `dual_channel` means.

### 2. Build

```sh
cd ~/aDNA/Canvas.aDNA
export PYTHONPATH=what/production/diagram_generator/src
/opt/anaconda3/bin/python -m diagram_generator build \
    what/context/<artifact>.diagram.yaml what/context/<artifact>.canvas
```

### 3. The three gates — in this order, none optional

```sh
# (a) SCHEMA — note the underscore; the CLI rejects `adna-native`
/opt/anaconda3/bin/canvas-std validate what/context/<artifact>.canvas --level adna_native

# (b) VISUAL FIT (machine) — the Obsidian-calibrated geometry traps
/opt/anaconda3/bin/python what/production/canvas_core/traps/cli.py \
    what/context/<artifact>.canvas --strict

# (c) AGENT-CONFIRMED RENDER (human-equivalent) — Amendment 1. See the warning below.
```

> **`canvas-std [OK]` is schema, not sight**, and `canvas-visual-check [OK]` is fit, not sight.
> Its own passing output says so: *"neither substitutes for looking at the rendered canvas."*

⚠ **Gate (c) has no safe automated path on a shared workstation — read this before trying.**
Obsidian is a desktop app, so `screencapture` captures **the whole screen**, including whatever
else the operator has open. Attempted at P2: two captures, the second of which recorded a third
party's private messages. **Do not screen-capture a desktop app to satisfy this gate.** Until a
window-scoped capture exists (`Home.aDNA`'s `canvas_visual_loop.py` is the reference implementation
to port), gate (c) is an **operator-performed** step: ask them to open the canvas and confirm it
reads. If they have not, say the canvas is `visual_gate: pending` — never report (b) as if it were (c).

### 4. Keep the pair in sync

The dual-channel law: **both channels update in the same mission.** A change to one and not the
other is a defect, caught at gate review (REQ-O05). Rebuild the canvas from the YAML — never
hand-edit the `.canvas`, and never hand-edit `_reserved`.

## Authoring rules the traps enforce (learned the expensive way)

- **Node labels stay short.** Node boxes are a uniform **220×100**. A label needing more than ~2
  short lines trips `CV-TEXT-BOUNDS-01`. Put the full statement in the prose channel and let the
  node carry the name. *Embedded `\n` in a label is the usual cause.*
- **Never hand-write a `#`/`##`/`###` title into a canvas text node.** `CV-LEAD-COST-01` flags it
  (h2 costs 98.9px of vertical space before one body character renders; the Oration M-R5 incident).
  The generator emits `#### ` for you, which is the **only** lead satisfying both that trap and
  `CV-HIERARCHY-01`'s title-slot requirement — see F-P2-3.
- **Placement, not routing.** Advanced Canvas does not recompute pathfinding for externally-authored
  edges; `pathfindingMethod` emits valid JSON and renders diagonal anyway. Budget readability on
  node placement, edge dimming, and tiered sizing (`context_canvas_topology_graphs.md` v1.1).
- **Stay in the calibrated range.** Crossing-minimisation is the dominant lever at ≲100 nodes and
  *not* significant on large graphs; and a crossing above ~70° costs almost nothing. If a diagram
  wants 40+ nodes, split it — do not tune it.
- **Cycles are fine.** All non-gantt edges emit `dependency`; only `sequence` is acyclicity-checked.

## Anti-patterns

1. **Hand-editing the generated `.canvas`.** The YAML is the source; an edit that survives one
   rebuild and vanishes at the next is worse than no edit.
2. **Declaring `authority` you do not mean** — `dual_channel` asserts a sync obligation. If nobody
   will maintain the pair, the honest declaration is `generator`.
3. **Reporting the machine visual check as the agent-confirmed render.** They are different gates
   and (b) has passed canvases that (c) would reject.
4. **Editing `what/code/canvas_std/`** to make a canvas validate. `git diff --stat` there must be
   **0**; if the Standard genuinely lacks something, that is a LIP (`adr_003`), not an edit.
5. **Extending the component taxonomy.** `heading` is not a `COMPONENT_CLASS` and fails A-3; a title
   is `typography_run` + `semantic_type: title`. Rich vocabulary rides in `qualities`.
6. **Drawing prose that has no structure** — see When to use.

## Outputs

`<artifact>.diagram.yaml` + `<artifact>.canvas` beside `<artifact>.md`; `adna_native [OK]`;
`canvas-visual-check --strict` clean; `_reserved.authority` declared; `canvas_std` git-diff **0**.

## Verification

`canvas-std validate … --level adna_native` → `[OK]` · `traps/cli.py … --strict` → `0 finding(s) [OK]` ·
`_reserved.authority` present and correct · `context_object.refs` ends with the prose `[[wikilink]]` ·
`git diff --stat -- what/code/canvas_std/` empty · gate (c) performed or explicitly recorded pending.

## Related

- Pattern: `campaign_canvas_blueprint/artifacts/draft_pattern_diagrammatic_context.md` (staged → Rosetta)
- Doctrine: `what/context/context_canvas_topology_graphs.md` v1.1 · `context_canvas_visual_in_the_loop.md` ·
  `what/docs/canvas_authoring_guidance.md`
- Decisions: [[adr_011_legacy_canvas_interop_reconciliation]] (the `view` row) · [[adr_003_standard_governance]] (LIP path)
- Sibling: `skill_canvas_producer_build.md` (build a producer, not a canvas)
- Worked examples: `what/context/context_canvas_surface_legs.{diagram.yaml,canvas}` ·
  `what/decisions/adr_004_production_code_layout.{diagram.yaml,canvas}`
