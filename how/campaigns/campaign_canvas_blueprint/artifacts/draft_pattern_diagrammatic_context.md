---
type: pattern_draft
title: "Pattern: Diagrammatic Context (dual-channel prose + canvas)"
proposed_home: aDNA.aDNA/what/patterns/pattern_diagrammatic_context.md
proposed_by: mondrian (Canvas.aDNA), Operation Blueprint P0
adoption_authority: rosetta (aDNA.aDNA) — this is a DRAFT staged for their ruling; Canvas does not write into aDNA.aDNA
created: 2026-08-22
updated: 2026-08-24
last_edited_by: agent_mondrian
status: staged_for_rosetta
errata: "E1 (2026-08-24, Blueprint P1) — legacy-corpus diagnosis corrected by measurement; see §Erratum E1. Count (196) unchanged."
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
`canvas_yaml_interop.md` legacy (69 copies, 50 of them in live vaults; **196** template `.canvas`
examples across 46 vaults) predates the aDNA Canvas Standard entirely.

> **⚠ Erratum E1 applies to this paragraph.** The *hand-authored* diagrams above are bare JSON
> Canvas as described. The **196 template-shipped** files are **not** — they carry a `_reserved`
> block written to a non-canonical path. See §Erratum E1 before ruling on the legacy.

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
it is *one mode*, now named and bounded, under the Standard. **Measurement (E1) strengthens this:
the legacy already emits exactly that quartet in all 196 template files — it is not a shape to be
mapped onto the `view` row, it *is* the `view` row, written to a path the validator does not read.**
Concretely: (a) the interop spec gains a header deferring to the aDNA Canvas Standard for schema and
to this pattern for authority semantics; (b) the 196 `what/lattices/examples/*.canvas` template files
**relocate** their existing `_reserved` block from `metadata._reserved` to the canonical
`metadata.frontmatter._reserved`, gain `adna_version` + `conformance_level`, and have their stub sync
values populated — no node or edge changes — at the next `skill_template_release`; (c)
`template_node_adna_exemplar`'s canvas stubs carry this pattern's frontmatter so every newly forked
vault inherits the doctrine, not just the files.
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
  convertible with zero content change. *(These are the genuinely bare ones; the template-shipped
  196 are a different case — E1.)*
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
- **`_reserved` off the canonical path** — a block at `metadata._reserved` (or anywhere but
  `metadata.frontmatter._reserved`) is *present and unread*: it looks conformant to a human reader
  and is invisible to `canvas_std`. This is the failure mode E1 found in 196 files, and it is worse
  than a missing block because it hides behind a green `[OK]` at `core`.

---

## Erratum E1 — legacy-corpus diagnosis corrected (2026-08-24, Blueprint P1)

This draft and its delivery memo (#9, 2026-08-22) were authored from a fleet survey. Re-measuring
before ruling corrected the diagnosis. **The count was right; the cause was not.**

| As drafted | Measured 2026-08-24 | |
|---|---|---|
| **196** template `.canvas` files | **196** real files / **46** live vaults (+74 archived, SO-7) | ✅ correct |
| "bare JSON Canvas — no `_reserved` block" | **196/196 carry** `{authority: "view", source_yaml, last_sync, sync_hash}` | ❌ wrong |
| "invisible to `canvas-std validate`" | true — but by **placement**, not absence | ⚠️ right effect, wrong cause |

**Root cause:** the legacy writes to `metadata._reserved`; the Standard's canonical path is
`metadata.frontmatter._reserved` (`what/docs/canvas_producer_quickstart.md:46`; named in A-2's own
error text). `canvas_std` reads the canonical path, finds nothing, reports `declared=core`.

```
$ canvas-std validate what/lattices/examples/template_architecture.canvas
  declared=core  level_reached=extended  [OK]
$ canvas-std validate … --level adna_native
  declared=adna_native  level_reached=extended  [FAIL]
  - A-2: aDNA-Native canvas requires a populated metadata.frontmatter._reserved block
```

Green at `extended`; fails `adna_native` on **A-2 alone**. Sync fields are unpopulated in all four
(`sync_hash` `"sha256:none"` ×3 / `"sha256:pending"` ×1; `source_yaml` empty in three) — the `view`
contract was declared but never enforced.

**Effect on the ask:** it shrinks. Not "reconcile two systems" but "relocate a block and add two
identity fields," lossless and mechanical — and the files are byte-identical fleet-wide
(`template_architecture.canvas` → `md5 f9459bc3cbb21391fe28dd76d3e44902`), so it is one `.adna` edit
plus a release, not a 46-vault sweep. Delivered to Rosetta as
`coord_2026_08_24_mondrian_to_rosetta_census_erratum.md`. Canvas's own ruling on the substance:
`what/decisions/adr_011_legacy_canvas_interop_reconciliation.md`.
