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
| `spec_interface_surface.md` | leg-3 (Salon P3) | Canvas as a **human↔AI / human↔human interaction surface** — the `read → act → re-read` loop over the leg-2 `ContextGraph`; 5 primitives (`anchor`·`affordance`·`response`·`surface state`·`turn`); additive `_reserved.interaction` shape + the **`I-*`** conformance family; round-trip-to-baseline. `status: **ratified**` (Salon P3, 2026-06-22) — **spec-only** (D4), bounded by `adr_006`; **`I-*` folded into `spec_conformance_suite` §4.1** (additive/optional; `interaction_version 1.0`; Standard-version cut deferred) |
| `spec_canvas_review_surface.md` | G9 (Halftone HR) | The **operator RLHF review surface**: Meta Bind controls (frontmatter capture, `enableJs: false`) ↔ the leg-3 affordance kinds; sidecar schema; the three-sink collector contract (append-only `responses[]` + Schema-A + III, layered idempotency, honest `{kind: ai}` attribution); **dispatch = `review_dispatch_contract v0`** — the Callisto seam; **stub bound 2026-08-09** (H6) into six clauses D1–D6, adding **D5** refusal atomicity (`F-S030-1`, credited to Bearly) + **D6** venue boundary (pull-not-push · two-consent spend · verify-on-arrival); still **contract-only**, no dispatcher, amendment `proposed`. Reference impl `canvas_core/rlhf/{review_canvas,review_collect}.py` + pilot `what/artifacts/review_surface_pilot/`. `status: **ratified**` (operator, 2026-08-04 — the GO-wave plan approval was the §7.7 signature) |
| `spec_rlhf_seam.md` | G6 · Lodestar R4.2 (Halftone H6) | The **ownership boundary** between the two RLHF record systems: **Canvas owns the capture substrate** (`_reserved.interaction.responses[]` — total, append-only, provenance) · **III owns the signal schema** (ADR-005 learning store — selective, interpreted). Rules store **heterogeneity** (discriminate on consumer-namespace `selection_id`, never line position); resolves the **ISS-vs-III contradiction** as a scope conflation (two objects, one word — no ownership moved); rules **open decision #4**: a reject routes to III as `rlhf_signal_type: reject` derived from `responses[]`, Schema-A stays approval-only. Implementation named as S-1..S-4, **deliberately unbuilt** while `proposed`. `status: **proposed**` (§7.7 pending operator) |

## Provenance

Built on the accepted P1 deliverables (`…/campaign_canvas_genesis_planning/missions/p1_source_inventory.md`,
`p1_fork_baseline.md`) and the three P2 foundational ADRs (`what/decisions/adr_001…003`). Baseline pinned PIN-A
(Advanced Canvas v5.6.6 + JSON Canvas 1.0).

## Naming
`spec_<topic>.md`, snake_case, normative voice (RFC-2119 MUST/SHOULD/MAY). Each carries a `conformance` note.
