---
type: spec
spec_id: spec_roundtrip_protocol_v2
title: "aDNA Canvas Round-Trip Protocol v2 — authoritative-source ↔ view"
standard_version: "2.0.0"
status: proposed
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
phase: P2
tags: [spec, canvas, roundtrip, sync, genesis, p2]
---

# aDNA Canvas Round-Trip Protocol v2

> **Status: PROPOSED — HELD at the P2 exit gate.** Generalizes the v1.0 Round-Trip Protocol (KEEP,
> [[p1_source_inventory]] §A2) from "`.lattice.yaml` ↔ `.canvas`" to "**authoritative source** ↔ **view**" for
> any 2D output, preserving the v1.0 authority model and sync-hash. RFC 2119 keywords.

## 1. Model

1.1. Every aDNA canvas has an **authoritative source** (the semantic source of truth) and the `.canvas` **view**.
For a lattice canvas the source is the `.lattice.yaml`; for a document it is the **canonical surface**
(`spec_panel_link_semantics.md` §5.2); in general it is the declared authoritative document.

1.2. **Forward** (source → view) is the primary direction and **MUST** be deterministic/automated. **Reverse**
(view → source) is **advisory only**: it produces a draft requiring human review ([[p1_fork_baseline]] I7). A tool
**MUST NOT** silently propagate canvas edits back to the source.

## 2. Authority matrix (KEEP)

| Concern | Authority |
|---------|-----------|
| Topology (which nodes/edges exist), node semantic type/config, edge data-mapping, execution/FAIR/federation | **Source** |
| Node positions (`x`,`y`), dimensions, routing, group/region structure | **View (canvas)** |
| Visual styling (color/shape) | **Convention** — derived from semantic type ([[spec_component_model]] §4) |

## 3. Sync hash (staleness detection, KEEP)

3.1. `compute_sync_hash(source)` = SHA-256 over the **topology** (sorted node ids + sorted `from→to` edge pairs),
truncated to 16 hex. It is stored in the `_lattice_meta` group and `_reserved.sync.sync_hash`
([[spec_adna_canvas_standard]] §8).

3.2. Before a visual review or a reverse merge, a tool **MUST** compare the canvas's stored hash to
`compute_sync_hash(current source)`. A mismatch means the view is **stale** and **SHOULD** be regenerated from
source before any reverse operation.

## 4. Forward path (source → view)

Deterministic generation: build nodes/edges from source topology; apply semantic-type → visual defaults
(profiles, [[spec_component_model]] §4); inject `_lattice_meta` + `_reserved.sync`; preserve existing positions
for unchanged node ids (`preserve_positions`), assigning fresh layout only to new nodes.

## 5. Reverse path (view → source, advisory)

The 7-step advisory workflow (KEEP, [[p1_source_inventory]] §A2):
1. Edit canvas topology (add/move/delete nodes/edges). 2. Export a source **draft** from the canvas. 3. **Diff**
the draft against the current source. 4. **Merge** topology changes (new nodes, removed edges) into the source.
5. **Restore** source-only fields (§6). 6. **Validate** the merged source. 7. **Regenerate** the canvas from the
merged source (preserving new positions).

**Three-way merge rule (KEEP):** when both source and canvas changed since last sync — *source semantic changes
win, canvas position changes win, conflicts are flagged for human resolution.*

## 6. Lossy-by-design boundary (KEEP)

These source fields are **NOT** recoverable from the canvas and **MUST** be restored from source on reverse merge
(step 5): `config`, `data_mapping`, `port`, `execution`, `fair`, `federation` (and any domain analog). The canvas
view carries topology + geometry + visual convention only.

## 7. v1.0 → v2.0 changes

- **Generalized** the authoritative source from `.lattice.yaml` to any authoritative document / canonical surface
  (documents, decks, sites) — the matrix, sync-hash, and merge rules are unchanged (KEEP).
- **Added** the `_reserved.sync` mirror of `_lattice_meta` so non-lattice canvases carry the sync contract
  without requiring a lattice-named meta group.
- **Unchanged:** authority matrix, sync-hash algorithm, advisory reverse direction, lossy boundary.

## 8. Conformance

A conformant tool **MUST**: stamp `sync.sync_hash` on generation; refuse to mark a reverse-merge authoritative
without a human-review step; preserve positions for unchanged ids; restore §6 fields on merge. The reference
converters live in `what/code/canvas_std/` (Option P; built later, [[adr_001_canvasforge_relationship]]).

## 9. Related
- [[spec_adna_canvas_standard]] §3/§8 · [[spec_panel_link_semantics]] §5.2 (canonical surface) ·
  [[p1_fork_baseline]] §2 (I1/I7) · [[p1_source_inventory]] §A2 · `what/code/canvas_std/` (reference impl, P-Option).
