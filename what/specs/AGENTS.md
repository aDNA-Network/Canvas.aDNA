---
type: directory_index
created: 2026-06-12
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [directory_index, specs, canvas, standard]
---

# what/specs/ — Normative aDNA Canvas Standard specifications

The normative specification set for the **aDNA Canvas Standard v2.0.0**, authored in Phase P2 of Operation
Cartography. These are the contracts producers (CanvasForge, ComfyForge, LF-successor, SiteForge) conform to.

> **Status (2026-06-12):** **RATIFIED** at the P2 exit gate (operator). The v2.0.0 spec set + ADRs (D2 extract /
> D3 schema-absorb+federated / D6 governance) are ratified. P3 (conformance suite + federation contract + `iii/`
> wrapper) is in progress; the conformance + federation specs join this folder.

## Contents

| Spec | Resolves | Role |
|------|----------|------|
| `spec_adna_canvas_standard.md` | (supersedes embedded v1.0.0) | Normative core — JSON shape, `_reserved`, `_lattice_meta`, node/edge schemas, conformance levels, validation, degradation contract |
| `spec_component_model.md` | D4 | The `_reserved`-namespaced component taxonomy across all 2D outputs |
| `spec_panel_link_semantics.md` | D5 | Reading-order / flow / pagination / region / sequence for non-DAG outputs |
| `spec_roundtrip_protocol_v2.md` | (generalizes v1.0 round-trip) | Authoritative-source ↔ view; authority matrix; sync-hash |
| `spec_context_object.md` | D7 (Δ2) | Canvas as a first-class context object; routes the primitive question through a LIP |
| `spec_conformance_suite.md` | (P3) | Conformance-level check catalog + golden-fixture suite the validator enforces |
| `spec_federation_contract.md` | (P3) | Producer ↔ Standard consumer-wrapper contract (`federation_ref`) + 5-stage conformance gates |
| `spec_canvas_context_loading.md` | leg-2 (Salon P1) | **Companion to `spec_context_object`** — how an agent loads a `.canvas` as a context graph *without rendering* (L1–L7 load pipeline + traversal primitives + resolver contract). `status: ratified` (Salon P1→P2 gate, 2026-06-22) — reference loader `canvas_context` built at P2 |
| `spec_interface_surface.md` | leg-3 (Salon P3) | Canvas as a **human↔AI / human↔human interaction surface** — the `read → act → re-read` loop over the leg-2 `ContextGraph`; 5 primitives (`anchor`·`affordance`·`response`·`surface state`·`turn`); additive `_reserved.interaction` shape + proposed **`I-*`** conformance family; round-trip-to-baseline. `status: **draft**` (Salon P3, 2026-06-22) — **spec-only** (D4), bounded by `adr_006`; folds `I-*` into `spec_conformance_suite` at ratification |

## Provenance

Built on the accepted P1 deliverables (`…/campaign_canvas_genesis_planning/missions/p1_source_inventory.md`,
`p1_fork_baseline.md`) and the three P2 foundational ADRs (`what/decisions/adr_001…003`). Baseline pinned PIN-A
(Advanced Canvas v5.6.6 + JSON Canvas 1.0).

## Naming
`spec_<topic>.md`, snake_case, normative voice (RFC-2119 MUST/SHOULD/MAY). Each carries a `conformance` note.
