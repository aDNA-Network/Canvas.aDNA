---
type: decision
adr_id: "007"
title: "Leg-3 firewall touch — wiring I-* into canvas_std + the interaction_version Standard-version cut"
status: accepted
created: 2026-06-22
updated: 2026-06-22
signed_by: stanley
supersedes:
superseded_by:
campaign_id: campaign_canvas_armature
tags: [adr, canvas, armature, leg3, interface, runtime, firewall, conformance, interaction, versioning]
---

# ADR-007: Leg-3 firewall touch — I-* into `canvas_std` + the `interaction_version` Standard-version cut

## Status

**Ratified 2026-06-22** (operator, Operation Armature **P0→P1 gate**, `campaign_canvas_armature`) — accepted with the P0
decision record (decision **D3**, at the agent's recommendation). This is now the **binding instrument** that authorizes
the *first* edit to `canvas_std` since Operation Keystone — bounded to Phase **P2**, behind the **P1→P2** human gate. It
does **not** authorize any code change until P2; P0/P1 stay `canvas_std` git-diff 0.

## Context

Every Canvas campaign to date — Keystone, Atelier, Palette, Salon — held the `canvas_std` reference tree at **git-diff
0**. Salon's **D6** made that an explicit, ratified choice for leg 2: the context loader was built as a read-only
sibling (`canvas_context`) rather than an extension of `canvas_std`, *preserving* the firewall. Salon then realized the
leg-3 interaction conformance family (`I-1/I-2/I-3/I-D`) **in that same consumer** (`canvas_context`'s
`validate_interaction_block`) and **forward-pointed** the harness wiring + the Standard-version cut to the leg-3 runtime
build:

- [[spec_conformance_suite]] §4.1 (ratified, Salon P3): "the reference validator **implementation is forward-pointed**
  (built with a leg-3 reference reader, as the leg-2 loader was at Salon P2)… the **formal Standard-version cut is
  deferred** (operator/FA at a deliberate release)."
- [[spec_interface_surface]] §9.1/§10 (ratified, Salon P3): the `I-*` family is "to be added to the suite **at
  ratification**" and the reference reader is "**forward-pointed**"; §10.2 keeps the POC a read-only consumer extension,
  "preserving the `canvas_std` firewall (D6)… A full leg-3 *build* is deferred to a follow-on charter."
- The Salon Completion Summary §Descoped: "**Wiring `I-*` into the `canvas_std` harness** — the family is realized in the
  consumer; harness-wiring + the formal Standard-version cut for `interaction_version 1.0` are deferred to the runtime
  build."

Operation Armature **is** that runtime build. To make `I-*` a **real Standard conformance check** — validated by the
`canvas-std` CLI on any interaction-bearing canvas, not just by consumer code — and to graduate `interaction_version
1.0` (which today rides `_reserved.interaction` additively at `standard_version 2.0.2`) into a **Standard version**, the
runtime must, for the first time, **edit `canvas_std`**. The operator chose this at the planning gate (decision-record
D3, via AskUserQuestion): **lift the firewall** for this bounded purpose, the deliberate inverse of Salon's D6.

This ADR records the lift as a citable instrument: *what* may be touched, *why* it is in `canvas_std`'s legitimate
remit, *how* it stays bounded, and *what replaces* the git-diff-0 gate while it is lifted.

## Decision

### 1. Lift the firewall — bounded to P2, for two purposes only

In Phase **P2** (and **no other phase**), `canvas_std` may be edited for exactly two purposes:

1. **Wire `I-1/I-2/I-3` into the validator.** Add `validate_interaction` to `canvas_std/validate.py`'s aDNA-Native
   (`A-*`) path so the harness checks `_reserved.interaction` per [[spec_interface_surface]] §4/§9 — **reusing the
   existing `canvas_std.reserved.validate_anchors`** for I-2's anchor resolution (the substrate Salon already built).
   Surface it through `conformance.validate_suite` + the `canvas-std` CLI; add **one interaction-bearing golden** (all
   four affordance kinds) to `canvas_std/tests`. The consumer's `validate_interaction_block` becomes a **thin
   delegate/re-export** of the `canvas_std` implementation (no duplicated logic).
2. **Cut `interaction_version 1.0` into a Standard version.** Bump `STANDARD_VERSION`, the schema `x-standard-version`,
   the CLI banner, `conformance.py`, and the spec frontmatters per the decision-record **D6** coordination (default:
   **v2.2.0**, reserving v2.1.0 for the in-review LIP-0008); flip the `spec_conformance_suite §4.1` +
   `spec_interface_surface §10` forward-pointers from "forward-pointed" → "implemented."

### 2. This is within `canvas_std`'s legitimate remit

[[adr_000_canvas_identity]] §3 already assigns `canvas_std` the role of the Standard's **reference tooling** —
"validators · round-trip converters · conformance harness." A conformance check (`I-*`) and a version cut are exactly
that. This ADR does **not** widen `canvas_std`'s remit; it **exercises** it for the interaction layer for the first time.
The boundary of [[adr_006_canvas_surface_boundary]] is unchanged: **no** rendering engine, capture runtime, transport,
or cross-surface routing enters `canvas_std` — only conformance checks + the version cut.

### 3. The gate changes while the firewall is lifted

For P0/P1/P3 the firewall check is unchanged: `git status -s -- what/code/canvas_std/` **clean** (git-diff 0). For the
**P2 exit gate only**, that check is **replaced** by **full regression**:

- `canvas_std` suite green (82/10 **+** the new `I-*` rows + the interaction golden);
- `canvas_context` green (50+; the consumer now delegating to the harness);
- all **7 producer** suites green (305) — no regression in any consumer of `canvas_std`;
- **degradation D-1..D-3 green on the interaction golden** — `strip(doc)` (which removes *all* `_reserved`, including
  `_reserved.interaction`) still yields a valid Core/Obsidian canvas (round-trip-to-baseline, [[spec_interface_surface]]
  §8.2). The interaction layer stays **additive** — no baseline overload ([[spec_adna_canvas_standard]] §11.3).

### 4. Governance of the version cut

The `I-*` family was **already ratified into the spec** at Salon P3, and the spec's ratification Q7 authorized "the
operator cuts the Standard version at a deliberate release." Per [[adr_003_standard_governance]] §2, the **normative
decision is therefore already made** (LIP-track complete at Salon P3); P2 is its **implementation** + the authorized cut
— maintainer-discretion territory, **not** a new normative change requiring its own LIP (decision-record **D6**). It is
nonetheless an operator-countersigned release at the P2 gate, coordinated with the in-review **LIP-0008** (→ v2.1.0).

## Consequences

### Positive
- **`I-*` becomes a first-class Standard conformance check** — any producer or consumer can validate an interaction
  surface with the `canvas-std` CLI, closing the leg-3 thesis (the family is no longer consumer-only code).
- **`interaction_version 1.0` graduates into a real Standard version** — the deliberate release the spec's Q7 deferred.
- **One source of truth for I-*** — the consumer delegates to the harness; no duplicated validation logic.

### Negative
- **Ends the perfect git-diff-0 firewall record** (6 campaigns). Mitigated: the touch is isolated to one phase + two
  purposes, behind its own ADR + the P1→P2 gate, with full-regression as the exit criterion (not git-diff 0).
- **Accepts regression risk** across 82 `canvas_std` tests + 7 producers + `canvas_context`. Mitigated: the P2 gate is
  full regression green + D-1..D-3 on an interaction golden; P1 (the larger build) stays firewall-clean so the risky
  edit is small and reviewable.

### Neutral
- Does **not** re-open canvas-as-primitive (Δ2 / LIP-0009) — the interaction layer rides `_reserved`, no core-primitive
  change.
- Extends, and does not supersede, [[adr_006_canvas_surface_boundary]] (boundary unchanged) and
  [[adr_000_canvas_identity]] §3 (this is `canvas_std`'s reference-tooling remit, exercised on the interaction layer).
- The **governed round-trip write** (Armature P1) is *not* a `canvas_std` edit — it is a read-only consumer of
  `canvas_std.roundtrip`; this ADR governs only the P2 harness touch.

## Related
- [[adr_006_canvas_surface_boundary]] (the binding boundary — unchanged) · [[adr_003_standard_governance]] (§2 LIP vs
  maintainer discretion; §3 version levels) · [[adr_000_canvas_identity]] (§3 `canvas_std` owns reference tooling) ·
  [[spec_interface_surface]] (§9.1 the `I-*` family; §10 the forward-pointed reader) · [[spec_conformance_suite]] (§4.1
  forward-pointer; §5 D-1..D-3) · [[spec_roundtrip_protocol_v2]] (the P1 write the runtime reuses, governed separately) ·
  `campaign_canvas_armature.md` (P2 the firewall phase) · `missions/artifacts/p0_decision_record.md` (D3 + D6) ·
  `../../how/backlog/idea_campaign_leg3_interface_runtime.md` (the Salon follow-on this campaign graduates).
