---
type: context
created: 2026-06-13
updated: 2026-06-13
status: active
last_edited_by: agent_stanley
quality_tier: graduated
source_campaign: campaign_canvas_genesis_planning
tags: [context, doctrine, standard, platform, federation, reusable]
---

# Context — Canvas Standard Doctrine (graduated from Operation Cartography)

Durable, reusable knowledge promoted at the close of the genesis-planning campaign. These three doctrines are
not Canvas-specific trivia — they generalize to any **standard-bearer Platform** vault.

## 1. Additive fork discipline — "fork, don't drift"

When forking an upstream format into an agentic-context-native standard, carry **every** aDNA-native extension in
a single namespaced block (here `_reserved`) over an unchanged baseline. Never add a top-level field or a new
enum token to the baseline. The payoff is a **one-line degradation invariant**: `validate(strip(doc))` passes the
baseline schema, so the fork degrades to a valid upstream file *by construction* rather than by a retrofitted
compatibility pass. Pin the upstream baseline at the **as-derived** version (provenance over recency); track the
drift to current as an additive-absorption backlog, never a baseline reset.

## 2. Standard-bearer inversion — "framework owns the engine, the standard-bearer owns the contract"

The usual consumer↔framework posture inverts for a standard-bearer. A normal consumer inherits both the contract
and the engine from a framework. A **standard-bearer** that owns a domain standard inherits the *engine* from the
framework (e.g. III's `module_iii_inspect_visual` + review skill) but **owns the _contract_** the engine runs (the
VR1–VR5 rubric + the trap schema). Encode this in the `iii/` (or other framework) wrapper: reference the engine,
assert ownership of the contract. Producers downstream then inherit the contract from the standard-bearer and the
engine from the framework — a clean three-way split that keeps the framework modality-agnostic.

## 3. Convergent planning cadence — each phase is a transform of the prior

The five-phase genesis-planning cadence is a pipeline where each artifact is a deterministic transform of the
last, so upfront rigor compounds:

`inventory (classify sources) → spec (consolidate the KEEP/EXTEND set) → contract (how consumers bind) →
execution charter (sequence the build) → harmonization (the inverse of the inventory: per-source disposition)`.

A verbatim-grounded source inventory at the start makes the impact matrix at the end nearly mechanical. The
operational pattern that made it work: **scout real precedents before authoring** (read the actual corpus, the
sf_forge spec, a live `iii/` wrapper) so specs are *conformant*, not invented — then synthesize.

## Provenance
Operation Cartography (`campaign_canvas_genesis_planning`, P0–P5, 2026-06-06 → 2026-06-13). See the campaign's
Completion Summary + Campaign AAR, and the ratified v2.0.0 spec set (`what/specs/`) + `adr_000..003`.
