---
type: spec
spec_id: spec_roundtrip_protocol_v2
title: "aDNA Canvas Round-Trip Protocol v2 — authoritative-source ↔ view"
standard_version: "2.5.0"
status: ratified
created: 2026-06-12
updated: 2026-10-16
last_edited_by: agent_mondrian
phase: P2
tags: [spec, canvas, roundtrip, sync, genesis, p2]
---

# aDNA Canvas Round-Trip Protocol v2

> **Status: RATIFIED 2026-06-12 (operator, P2 gate).** Generalizes the v1.0 Round-Trip Protocol (KEEP,
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

3.1. `compute_sync_hash(source)` = SHA-256 over the **topology** (sorted node ids + sorted `from->to` edge pairs),
truncated to 16 hex. It is stored in the `_lattice_meta` group and `_reserved.sync.sync_hash`
([[spec_adna_canvas_standard]] §8). **The payload, byte for byte** (v2.5.0, LIP-0011 §1.1):

```
ids     = sorted(str(node.id) for node in S.nodes)
pairs   = sorted(f"{edge.fromNode}->{edge.toNode}" for edge in S.edges)    # ASCII "->" (0x2D 0x3E)
payload = "\x01".join(ids) + "\x02" + "\x01".join(pairs)                  # U+0001 between items, U+0002 between lists
sync_hash = sha256(payload.encode("utf-8")).hexdigest()[:16]               # lowercase
```

**Test vector (normative):** nodes `a`, `b`; edge `a -> b` ⇒ payload `a\x01b\x02a->b` ⇒ **`097164175d271fb8`**.
⚠ Reading the separators as empty strings gives `5d3a8a0c81db08d9`, which is wrong. Until v2.5.0 the reference
source held them as literal control bytes, which print as nothing; that is how two independent readers got the wrong
hash (F-V-13, LP F-AC-41). Before v2.5.0 this paragraph wrote the arrow as `→`; the bytes have always been ASCII `->`.
A full digest of the source document's bytes is a different question, answered by `sync.source_sha256` (64 hex).

3.2. Before a visual review or a reverse merge, a tool **MUST** compare the canvas's stored hash to
`compute_sync_hash(current source)`. A mismatch means the view is **stale** and **SHOULD** be regenerated from
source before any reverse operation. For a `production: generated` canvas the validator also compares the stored
hash with the canvas's **own** topology and reports a mismatch as an **advisory**
(`canvas_std.advisories()`, [[spec_conformance_suite]] A-6; v2.5.0, D-1 (i)). That check is a proxy: it holds only
for views that preserve the source's nodes and edges, so it is never an error.

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
