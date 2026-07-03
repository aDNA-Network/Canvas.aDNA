---
type: directory_index
created: 2026-07-02
updated: 2026-07-02
last_edited_by: agent_mondrian
tags: [directory_index, governance, lip]
---

# who/governance/lips/ — Lattice Improvement Proposals (Agent Reference)

## Purpose

The **LIP governance home for the aDNA Canvas Standard**. Normative changes to the Standard ride a Lattice Improvement
Proposal (proposal → review → ratify), per `lip_0001_lip_process.md` and `what/decisions/adr_003_standard_governance.md`
§2. Stood up at Operation Beacon Phase B4 (2026-07-02) when the predecessor home (`lattice-labs/how/governance/lips/`)
was archived reader-only.

## Key Files

| File | Purpose |
|------|---------|
| `lip_0001_lip_process.md` | The LIP process itself (CC0) — types, lifecycle, numbering, review. Canvas-local working copy of the global process. |
| `lip_template.md` | Copy-me skeleton for a new LIP (CC0). |
| `lip_registry.md` | Canvas-scoped index of stewarded LIPs (LIP-0008, LIP-0009) under global numbers. |
| `lip_0008_derived_surface_pure_metadata.md` | Standard LIP — `panel_link` A-5 relaxation (Accepted; lands v2.3.0). |
| `lip_0009_canvas_as_primitive.md` | Standard LIP — canvas-as-primitive evaluation (Final; Option V). |

## Conventions

- **Naming**: `lip_NNNN_short_slug.md` (four-digit global number, underscores only).
- **Numbering**: global sequence, registrar = **aDNA.aDNA** (D3, handshake pending — `who/coordination/coord_2026_07_02_lip_registrar_handshake.md`). Never re-number a migrated LIP.
- **Authority**: Phase 0 — Founding Architect (operator) accepts/declares Final. Review ≥ 7 days.
- **License**: LIPs are CC0 (public domain). Keep the Copyright section.
- **Archive discipline**: the predecessor copies at `Archive.aDNA/lattice-labs/how/governance/lips/` are **reader-only** (SO-6). Never write there; migrate a live copy here instead.

## Load/Skip Decision

**Load when**: proposing/ratifying a normative change to the Canvas Standard; advancing a LIP's status; auditing governance provenance.
**Skip when**: routine producer/spec work that doesn't change a normative rule (those ride editorial PATCH at maintainer discretion per `adr_003` §2).

## Cross-References

- [adr_003_standard_governance](../../../what/decisions/adr_003_standard_governance.md) — binds the change process to this home.
- [lip_queue_disposition](../../../what/decisions/lip_queue_disposition.md) — errata triage feeding the LIP queue.
- [who/governance/AGENTS](../AGENTS.md) — parent governance index.
