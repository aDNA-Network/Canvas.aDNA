---
type: pattern_draft
title: "Pattern: Diagrammatic Context (dual-channel prose + canvas)"
proposed_home: aDNA.aDNA/what/patterns/pattern_diagrammatic_context.md
proposed_by: mondrian (Canvas.aDNA), Operation Blueprint P0
adoption_authority: rosetta (aDNA.aDNA) — this is a DRAFT staged for their ruling; Canvas does not write into aDNA.aDNA
created: 2026-08-22
updated: 2026-08-22
last_edited_by: agent_mondrian
status: staged_for_rosetta
empirical_anchor: Emacs.aDNA (REQ-Q01/REQ-O05/REQ-H05, ratified, running since 2025-07 at Standard 2.3.0)
tags: [pattern, draft, canvas, diagrammatic_context, dual_channel, authority_model, upstream]
---

# Pattern: Diagrammatic Context

## Problem

Agents and operators reason about *structures* — architectures, seams, flows, topologies — but the
fleet's context is overwhelmingly prose. Where diagrams exist they are ad-hoc: 145 real `.canvas`
files live across 18 vaults today, and their conformance is bimodal. Emacs authors fully
aDNA-Native canvases; Operations, ScienceStanley, Regenesis, and aDNALabs author genuinely
excellent diagrams as **bare JSON Canvas** — no `_reserved` block, no conformance level, no sync
discipline, invisible to `canvas-std validate` and to every canvas-aware tool. Worse, **four
incompatible authority models** coexist with no doctrine choosing between them, and the 2026-02
`canvas_yaml_interop.md` legacy (copied into ~10 vaults; 196 template `.canvas` examples) predates
the aDNA Canvas Standard entirely.

The demand is proven — vaults keep inventing this independently. The doctrine is missing.

## Pattern

**Every key artifact MAY — and load-bearing architectural artifacts SHOULD — carry two channels:**

1. **Prose channel** (`.md`) — authoritative for *meaning*: rationale, constraints, provenance.
2. **Canvas channel** (`.canvas`, aDNA-Native conformant) — authoritative for *structure*: the
   components, seams, and flows, positioned and typed.

**The dual-channel law (graduated from Emacs REQ-Q01):** the two channels update **in the same
mission**. A change that touches one and not the other is a *defect*, caught at gate review
(REQ-O05: canvas-sync review at every gate). Canvas files are **vault citizens** (REQ-H05):
openable, linkable (`[[wikilink]]`-able), searchable beside markdown — never a build directory's
private output.

### The authority axis (reconciling the four models)

Every diagrammatic-context canvas declares its authority in `_reserved`:

| `authority` | Meaning | When |
|---|---|---|
| `dual_channel` | Prose owns meaning; canvas owns structure; same-mission sync (drift = defect). | **Default for context/architecture canvases** — the Emacs model. |
| `generator` | The canvas is a build product of a source (YAML + script); never hand-edit; regenerate. Carries `source_*` + hash fields. | Fleet-scale projections (Home's `topology.canvas`). |
| `view` | A derived visualization of an authoritative non-canvas source (`.lattice.yaml`); edits are view edits until reconciled (Round-Trip Protocol / Obsidian ADR-010 §3). | Lattice visualizations — the legacy interop's home. |

`none` is retired: a canvas with no declared authority is nonconformant diagrammatic context.

### Conformance floor

- Validates at `adna_native` (`canvas-std validate`), Standard ≥ 2.3.0 pin in the vault's
  `canvas/` federation wrapper.
- Passes the visual gate (agent-confirmed render — a canvas that validates but renders unreadable
  is not context; Amendment 1).
- Topology canvases follow `Canvas.aDNA/what/context/context_canvas_topology_graphs.md` v1.1
  (placement over routing; angle-aware crossing budget; size/density bounds).

### Legacy reconciliation (the ruling this draft asks Rosetta for)

The 2026-02 `canvas_yaml_interop.md` spec and its `_reserved: {authority: "view", source_yaml,
sync_hash}` shape become **the `view` row of the authority axis** — i.e., the legacy is not wrong,
it is *one mode*, now named and bounded, under the Standard. Concretely: (a) the interop spec gains
a header deferring to the aDNA Canvas Standard for schema and to this pattern for authority
semantics; (b) the 196 `what/lattices/examples/*.canvas` template files regenerate conformant at
the next `skill_template_release`; (c) `template_node_adna_exemplar`'s canvas stubs carry this
pattern's frontmatter so every newly forked vault inherits the doctrine, not just the files.
Also proposed: re-point `how/backlog/idea_diagram_missions_herb.md` (already co-assigned
Rosetta + Mondrian) from rendered-figures-for-the-website to canvas-companions-as-context — the
Dual Method's "mermaid as structural ground truth" slots directly into the canvas channel
(`diagram_generator` already derives Mermaid).

## Evidence

- **Emacs.aDNA** — 13 months of the exact pattern, ratified (c01–c06 canvases, `adna_native`,
  `component_types` + `sync` blocks; per-mission "Canvas duty" steps). The pattern is a
  *graduation*, not an invention.
- **Unserved demand** — Operations' five C08 liaison canvases (with an invented legend convention),
  Regenesis's 11 design canvases, ScienceStanley's 29 production canvases: all standard-blind, all
  convertible with zero content change.
- **Substrate readiness** — the Standard needs **no change** (Emacs ships on 2.3.0 unmodified);
  `canvas_std` validate/roundtrip/conformance + 14 visual traps + `diagram_generator` already exist.

## Adoption mechanics

Per-vault cost is one wrapper pin + frontmatter on existing canvases. Rollout rides Operation
Blueprint P3's re-pin wave (lockstep-flip: wrapper pin + conformance state advance together, the
VisualDNA ADR-002 ceremony). Conversion offers to the standard-blind vaults come with the work
done for them (Blueprint P2).

## Anti-patterns

- **Canvas-as-screenshot** — an image of a diagram is not diagrammatic context; the structure must
  be typed nodes/edges, queryable and diffable.
- **Silent drift** — updating prose without the canvas (or vice versa) in a dual-channel pair.
- **Undeclared authority** — a `.canvas` with no `authority` field forces every reader to guess
  whether editing it means anything.
- **Bare JSON Canvas for context** — degrades fine *visually* but is invisible to validation,
  sync, and every canvas-aware tool.
