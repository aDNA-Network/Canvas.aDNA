---
type: decision
adr_id: "001"
title: "CanvasForge relationship — extract the Standard, CanvasForge becomes a pure producer"
status: proposed
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
signed_by:
supersedes:
superseded_by:
resolves: D2
phase: P2
tags: [adr, canvas, standard, canvasforge, federation, genesis, d2]
---

# ADR-001: CanvasForge Relationship (D2)

## Status

**Proposed** — drafted at P2 (Operation Cartography). **Operator ratifies at the P2 exit gate** (one of the two
gate sign-offs: v2.0.0 spec + D2/D3). Couples to [[adr_002_literatureforge_seam]] (D3) and the P0 Option-P lock
([[adr_000_canvas_identity]] §1).

## Context

CanvasForge (Hermes) today **embeds** the Canvas Standard v1.0.0 inside its `canvas_core` substrate: the
`CanvasBuilder` class carries the schema enums, the semantic mappings, the round-trip machinery, and the
validator. Canvas.aDNA was created (P0) to own that Standard as a standard-bearer Platform that **ships its
reference tooling** (Option P, `what/code/canvas_std/`, declared-not-built). D2 asks where the reference
validators/converters live and what CanvasForge becomes.

**P1 evidence** ([[p1_source_inventory]] §B): the `CanvasBuilder` surface splits cleanly into a **normative core**
(`build`/`read_back`/`diff`/`merge`/`validate`/`compute_sync_hash`/`preserve_positions` + `add_semantic_node/edge`
+ node/edge model + `_lattice_meta` injector) and **application convenience** (`layout_*`, `selection_board`,
`save`, accessors). The boundary is real, not aspirational. A working precedent exists: `lattice-protocol/
extensions/canvas/__init__.py` is a deprecated extraction-shim that re-exports `from canvasforge.canvas_core import *`.

## Decision

**Option A — extract the Standard OUT of CanvasForge.** The standard machinery (schema, `VALID_*` enums, the
generalized semantic taxonomy, validators, round-trip converters, conformance harness) lives in Canvas.aDNA at
`what/code/canvas_std/` (built in the execution campaign). **CanvasForge becomes a pure producer** that consumes
the Standard via a `federation_ref` wrapper and retains only producer-side convenience (`layout_*`,
`selection_board`, deck/comic composition, the export engines).

**Considered and rejected:**
- **Option B** (Canvas.aDNA owns spec + conformance; CanvasForge keeps `CanvasBuilder` as the canonical
  reference impl, version-pinned). *Rejected:* leaves the normative engine inside a producer, contradicting the
  Option-P lock that Canvas.aDNA *ships* the reference tooling; forces every other producer to depend on
  CanvasForge rather than on the Standard; re-creates the embedding problem one level up.
- **Option C** (reject — leave embedded). *Rejected:* fails the unification thesis outright; no standard-bearer,
  no clean federation story, producers keep re-deriving canvas semantics.

**Migration shape (execution-campaign / P4 — NOT this campaign):** mirror the lattice-protocol precedent — extract
`canvas_std`, publish it, repoint `canvasforge.canvas_core` at it behind a **deprecation shim** with a grace
window, and gate the cutover on **parity/regression** against locked output baselines (Wilhelm 8.80 / Issue 01
8.43). No code moves in Operation Cartography (C3).

## Consequences

### Positive
- One standard-bearer; every producer (CanvasForge, LF-successor, ComfyForge, SiteForge) federates against the
  same Standard, not against a sibling producer.
- Realizes Option P: the reference tooling has a real home and a real extraction target (P1 §B ★ rows).
- Clean symmetry for D3 — if LF's successor is also a pure producer, the architecture is uniform.

### Negative
- The extraction is a multi-phase, parity-gated migration (real cost, deferred to P4; risk owned there).
- A deprecation window where both the shim and the extracted package coexist (managed per the shim precedent).

### Neutral
- Producer-side convenience (`layout_*`, `selection_board`, exports) is unaffected — it was never the Standard.

## Related
- [[adr_000_canvas_identity]] §1 (Option P cascade → extraction) · [[adr_002_literatureforge_seam]] (D3 symmetry) ·
  [[adr_003_standard_governance]] (D6) · [[p1_source_inventory]] §B · [[p1_fork_baseline]] §3 (extraction map) ·
  `lattice-protocol/extensions/canvas/__init__.py` (precedent) · `SiteForge.aDNA/what/artifacts/sf_forge_pattern_spec.md`.
