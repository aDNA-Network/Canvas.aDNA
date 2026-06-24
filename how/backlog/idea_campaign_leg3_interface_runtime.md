---
idea_id: idea_campaign_leg3_interface_runtime
title: "Leg-3 Interface Runtime — canvas-as-surface build (Salon follow-on)"
category: technical
status: implemented
priority: high
effort: plan
proposed_by: agent_stanley
proposed_date: 2026-06-22
created: 2026-06-22
updated: 2026-06-23
last_edited_by: agent_stanley
plan_id: campaign_canvas_armature
tags: [backlog, canvas, salon, leg3, interface, surface, runtime, interaction, follow-on]
---

# Leg-3 Interface Runtime — canvas-as-surface build (Salon follow-on)

## Problem / Opportunity

Operation Salon (closed 2026-06-22) **RATIFIED** the leg-3 interface-surface spec
([[what/specs/spec_interface_surface|spec_interface_surface.md]]) and **DEMONSTRATED** the `read → act → re-read` loop
with a minimal read-only POC (`what/code/canvas_context/interaction.py` v0.2.0). But the POC is **deliberately not a
runtime**: `apply_response` is a pure view-only append-fold; the `I-*` conformance family lives in the `canvas_context`
consumer (not the `canvas_std` harness); the governed `.lattice.yaml` round-trip write is out of scope; and
`interaction_version 1.0` (additive in `_reserved.interaction`) was never cut as a Standard version. Salon's charter
(D4) scoped leg 3 **spec-only** and explicitly deferred the build to a follow-on. **This is that follow-on** — turn the
ratified spec + demonstrated loop into a real, governed leg-3 interaction runtime, completing the interface leg of the
vault's three-leg thesis.

## Proposed Solution

A future execution campaign (Cartography→Keystone model) that builds the leg-3 runtime on the proven leg-2 substrate.
Scope seed, carried from Salon P4 + the campaign Completion Summary §Descoped:

- **Governed round-trip write** — promote `apply_response` from a view-only fold to an **authoritative write** back to
  `.lattice.yaml` per [[what/specs/spec_roundtrip_protocol_v2|spec_roundtrip_protocol_v2]] (the POC stayed read-only;
  the runtime closes the write while preserving the round-trip-to-baseline property).
- **`I-*` into the `canvas_std` harness** — wire the `I-1/I-2/I-3/I-D` conformance family (today realized in the
  consumer) into the Standard's conformance harness. **This is the first leg-3 touch of the `canvas_std` firewall** —
  a ratifiable decision (as D6 was for leg 2), not an assumption.
- **Formal Standard-version cut** — graduate `interaction_version 1.0` into a Standard-version bump (the version cut was
  deferred at P3 ratification).
- **OIP `v1.x` re-anchor** — when the future `aDNA.aDNA` OIP-unification campaign lands its interface/interaction
  thesis, run a `v1.x` alignment pass on `spec_interface_surface` (the spec was authored Canvas-scoped v1 with this
  seam designed in via `interaction_version` semver — additive, not re-litigated).
- **Capture + turn lifecycle** — an operator-annotation ingest path, the turn lifecycle, and the affordance-execution
  boundary vs ISS — coordinated, not absorbed.

## Discussion

- 2026-06-22 (agent_stanley): Filed at Operation Salon **P5 close** as the campaign's committed follow-on. Operator
  chose **backlog idea stub** depth (not a full charter directory) — matches how Salon itself incubated from a Palette
  candidate-note. Graduates to a campaign on operator commit (set `status: planned` + `plan_id`).
- **Cross-vault dependency (gating):** the OIP re-anchor depends on the future `aDNA.aDNA` OIP-unification campaign
  (`idea_campaign_operator_interaction_patterns_unification.md`), which is unopened. The runtime can build on the
  ratified Canvas-scoped v1 spec without it; the re-anchor pass waits for it.
- **ISS seam (clean):** Canvas owns the affordance / anchor / response / turn **grammar**; ISS owns the gate **engine**
  that may consume it (D8 memo `who/coordination/coord_2026_06_22_mondrian_to_iss_canvas_interface_seam.md`). The
  runtime must hold this boundary (ADR-006).
- **Prior art to reuse:** `what/code/canvas_context/interaction.py` (the POC reader + append-fold reducer);
  `spec_interface_surface.md` (ratified contract); `spec_conformance_suite.md §4.1` (the `I-*` family);
  `spec_roundtrip_protocol_v2.md` (the governed write); `what/context/context_canvas_surface_legs.md` (the graduated
  compose-not-extend / view-fold patterns).

## Decision

**GRADUATED 2026-06-22 → `campaign_canvas_armature` (Operation Armature).** The operator committed at the Salon-close
follow-on; the campaign was chartered + ratified (P0→P1 gate) as a 4-phase build (P0 charter → P1 governed
advisory-reverse write runtime → P2 the `canvas_std` firewall touch + `interaction_version` Standard-version cut, gated
by `adr_007` → P3 close). `status: planned`, `plan_id: campaign_canvas_armature`. The OIP `v1.x` re-anchor remains a
deferred sub-item (D8 — filed as its own stub at the Armature P3 close, gated on the future `aDNA.aDNA` OIP campaign).
Mark `implemented` at the Armature P3 close.

**✅ IMPLEMENTED 2026-06-23 (Operation Armature P3 close).** All four core scope seeds delivered: (1) the **governed
round-trip write** landed at P1 as the *advisory-reverse* path (`canvas_context/reconcile.py` — a reviewed `_draft`,
never a silent authoritative write; the on-disk source is byte-unchanged, honoring `spec_roundtrip_protocol_v2 §1.2`);
(2) **`I-*` wired into the `canvas_std` harness** at P2 under ratified `adr_007` (`reserved.validate_interaction` on the
aDNA-Native `validate()` path + CLI; the consumer is now a thin delegate); (3) **`interaction_version 1.0` cut into
Standard v2.2.0** at P2. Scope refinements vs the seed: the *write* is **advisory** (a reviewed draft) per
`spec_roundtrip_protocol_v2 §1.2`, not an unconditional authoritative write (D4); **capture / turn-lifecycle** stayed a
thin pilot path, the gate engine remaining ISS's (D7). The **OIP `v1.x` re-anchor** is carried forward as its own
deferred stub → [[idea_oip_v1x_interface_reanchor]] (D8; gated on the unopened `aDNA.aDNA` OIP-unification campaign).
Full regression green throughout (`canvas_std` 105/10 · `canvas_context` 58 · 7 producers 223).
