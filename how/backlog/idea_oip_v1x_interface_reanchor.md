---
idea_id: idea_oip_v1x_interface_reanchor
title: "OIP v1.x re-anchor — align Canvas leg-3 interface vocabulary to the OIP-unification thesis"
category: technical
status: proposed
priority: high
effort: session
proposed_by: agent_stanley
proposed_date: 2026-06-23
created: 2026-06-23
updated: 2026-06-23
last_edited_by: agent_stanley
gated_on: idea_campaign_operator_interaction_patterns_unification
tags: [backlog, canvas, oip, interface, surface, leg3, deferred, cross-vault-dependency, v1x-alignment]
---

# OIP v1.x re-anchor — align Canvas leg-3 interface vocabulary to the OIP-unification thesis

> **Deferred stub — filed at Operation Armature P3 close (2026-06-23) per decision D8**
> (`how/campaigns/campaign_canvas_armature/missions/artifacts/p0_decision_record.md`). File it, don't build it: there is
> no OIP thesis to anchor to yet. Graduates to a mission when the `aDNA.aDNA` OIP-unification campaign lands its
> interface/interaction thesis.

## Problem / Opportunity

The Canvas leg-3 interface-surface contract ([[what/specs/spec_interface_surface|spec_interface_surface.md]], ratified
Salon P3; runtime built Operation Armature) was authored **Canvas-scoped `v1`, first-principles** — grounded on
[[what/decisions/adr_006_canvas_surface_boundary|adr_006]], the proven leg-2 model, and ISS as an exemplar — because the
external **OIP (Operator Interaction Patterns)** thesis it was meant to ground against **does not yet exist**
(spec §10.x grounding note; [[adr_000_canvas_identity]] names it as a future cross-substrate doctrine). When the
`aDNA.aDNA` OIP-unification campaign authors that thesis, the shared OIP vocabulary may diverge from Canvas's five
primitives (`anchor` · `affordance` · `response` · `surface state` · `turn`). The spec was deliberately designed to
**re-anchor additively** via the `interaction_version` semver seam — this work is that alignment pass, not a
re-litigation.

## Proposed Solution

A narrow `v1.x` alignment pass (one session), gated on the OIP thesis landing:
- **Vocabulary map** — verify Canvas's five primitives map cleanly onto the OIP `v1.x` interaction vocabulary; where
  terms diverge, add an additive crosswalk (no rename of the ratified `v1` terms) under a bumped `interaction_version`
  (e.g. `1.1`), keeping `spec_adna_canvas_standard §11` round-trip-to-baseline intact.
- **Grounding refs** — update `spec_interface_surface`'s grounding note to cite the OIP thesis as the canonical anchor
  (replacing the "first-principles, upstream-absent" framing) and confirm the `seam: Canvas ↔ OIP` routing line
  (adr_006 §3) still holds — Canvas defines *what the surface is*, OIP defines *when to route to it*.
- **No runtime change expected** — the re-anchor is spec/vocabulary alignment; the `validate_interaction` harness +
  `canvas_context` runtime stand unless the OIP thesis forces a conformance change (which would then ride its own ADR +
  a Standard-version cut, per `adr_003` + the Principle-7 bounded-firewall-touch pattern).

## Discussion

- 2026-06-23 (agent_stanley): Filed at Armature **P3 close** per D8 — the only one of the leg-3 follow-on's four scope
  seeds **not** delivered by Armature, because it has a hard external dependency. The runtime built on the ratified
  Canvas-scoped `v1` spec **without** it (idea_campaign_leg3_interface_runtime §Discussion — "the runtime can build on
  the ratified v1 spec without it; the re-anchor pass waits for it"). No blocking dependency exists, so blocking the
  campaign on the OIP campaign was rejected.
- **Cross-vault dependency (gating):** `aDNA.aDNA/how/backlog/idea_campaign_operator_interaction_patterns_unification.md`
  (unopened). The standing request for the OIP interface/interaction thesis outline was already sent at Salon P3 (the
  `seam: Canvas ↔ OIP` heads-up memo); **no new coordination memo is needed at this filing** — when the OIP campaign
  opens + lands its recon/architect phases, it cross-posts the thesis, which reactivates this stub.
- **Reactivation:** on the OIP thesis landing, set `status: planned` + a `plan_id`/mission and schedule the pass; a
  Canvas→OIP confirmation memo may then be warranted to close the seam.

## Decision

**FILED 2026-06-23 at Operation Armature P3 close as a deferred stub**, gated on the unopened `aDNA.aDNA`
OIP-unification campaign. No build now. Closes the D8 loop. Cross-refs: D8 of `p0_decision_record.md`;
[[idea_campaign_leg3_interface_runtime]] (the parent follow-on, now `implemented`); `spec_interface_surface §11`
(the boundary / OIP seam).
