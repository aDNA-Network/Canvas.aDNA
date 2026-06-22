---
type: decision
adr_id: "006"
title: "Canvas-as-surface boundary — what Canvas owns vs ISS / Astro / Terminal / OIP"
status: ratified
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
signed_by: stanley
supersedes:
superseded_by:
campaign_id: campaign_canvas_salon
tags: [adr, canvas, surface, boundary, context_object, interface, iss, astro, terminal, oip, seam]
---

# ADR-006: Canvas-as-surface boundary

## Status

**Ratified 2026-06-22** (operator, P0→P1 gate of Operation Salon, `campaign_canvas_salon`). This ADR was decision
**D7** of the P0 decision record; ratified with the rest of the record (all defaults), it activated the campaign
(`status: active`) and opened Phase P1. It is now a **binding boundary** for the leg-2/leg-3 work — the citable fence
the campaign builds within.

## Context

The Canvas thesis ([[adr_000_canvas_identity|ADR-000]] §Context) names a canvas as three things: *(a)* an **output
primitive**, *(b)* a first-class **context object**, *(c)* a **human↔AI / human↔human interaction surface**. Operation
Palette proved (a) — 7 producers. Operation Salon takes on (b) and (c). Two of those — the *context-object* read face
and the *interface-surface* face — are what we collectively call **canvas-as-surface**.

Before building either, Canvas.aDNA must answer a boundary question, because canvas-as-surface visibly overlaps three
existing systems and one *future* one:

- **ISS** (Intelligence/Interaction Surface; governed in `aDNA.aDNA`, SO-8) — agent-authored **operator decision
  gates** rendered as rich **HTML surfaces** with a 4-tier round-trip. An interaction surface today.
- **Astro.aDNA** — **web production**: takes branding + content and renders/deploys a **website** (a Forge that
  *consumes* the Canvas Standard).
- **Terminal.aDNA** — the **CLI/TUI** chief-of-staff surface for a node; can open/reference artifacts.
- **OIP** (Operator Interaction Patterns) — a *future* `aDNA.aDNA` unification campaign
  (`idea_campaign_operator_interaction_patterns_unification.md`) that will define **when** an agent reaches for Canvas
  vs ISS vs Terminal vs a custom web page — the **cross-surface routing** layer.

Without a fixed boundary, the leg-2/leg-3 work risks re-implementing ISS, drifting into web production, or pre-empting
the OIP routing layer. ADR-000 already sketches the answer ("Does NOT own: producer pipelines · rendering runtimes ·
image generation"); this ADR extends that test to the *surface* legs and records it as a citable boundary. The model is
the already-formalized **LP↔Canvas seam**
(`who/coordination/coord_2026_06_13_mondrian_countersign_lp_canvas_seam.md`): a **stewardship split** (stewardship ≠
implementation ≠ routing) plus a **heads-up coordination courtesy** on seam-touching changes.

## Decision

### 1. What canvas-as-surface owns: the data model + contracts, substrate-neutral

Canvas.aDNA owns the **substrate-neutral data model and contracts** for a canvas used as a context object and as an
interaction surface — and **nothing downstream of them**:

- the canvas **schema** and the `_reserved` extension carrier (already owned);
- the **context-object** metadata + the **loading/traversal contract** (leg 2 — the "how" Salon P1/P2 supplies);
- the **interface-surface contract** (leg 3 — Salon P3): what an interaction surface *is*, its interaction
  primitives, and its conformance rules — **as a contract, not an engine**;
- the **conformance suite** that validates the above.

Canvas owns *what a canvas-surface is*. It does **not** own any rendering engine, capture runtime, transport, or the
decision of *when* to use a canvas rather than another surface.

### 2. The boundary table

| System | Owns | Where the Canvas boundary falls |
|---|---|---|
| **Canvas.aDNA** *(this)* | The 2D canvas **data model** + the **context-loading** and **interface-surface contracts** (substrate-neutral) + conformance | Canvas defines **what a canvas-surface IS** (schema, semantics, contracts). It ships a *reference* loader (Salon P2), not a product runtime. |
| **ISS** *(aDNA.aDNA)* | Operator **decision-gate** authoring + **HTML rendering** + the 4-tier round-trip submission | ISS owns gate *capture + rendering + transport*. A gate may one day be **authored on a canvas archetype** (Canvas owns that artifact grammar), but ISS owns the gate runtime. No overlap if Canvas stays "grammar", ISS stays "gate engine". |
| **Astro.aDNA** | The **web-publication pipeline** (canvas/branding → deployed website) | Astro **consumes** a canvas as input; its output is a **website**, not a canvas. Canvas never renders HTML/CSS/JS. |
| **Terminal.aDNA** | **CLI/TUI** node orchestration; opening/referencing artifacts | Terminal **navigates/opens** canvases; it does not define their structure. Integration is artifact-passing. |
| **OIP** *(future, aDNA.aDNA)* | The **cross-surface routing** decision-tree (Canvas vs ISS vs Terminal vs web) | OIP routes **among** surfaces; Canvas defines **one** surface. Canvas must not encode routing logic. |

### 3. Routing is explicitly not Canvas's

The decision of **when** to surface an interaction on a canvas versus an ISS gate, a Terminal prompt, or a web page is
the **OIP routing layer's** responsibility (future `aDNA.aDNA` campaign). The Salon leg-3 spec defines *what a
canvas-surface is and how it behaves*; it **must not** encode a cross-surface routing decision-tree. Keeping these
separate is the load-bearing line of this ADR — it is what prevents Salon from over-reaching into cross-vault
territory.

### 4. Coordination rule (heads-up courtesy)

Mirroring the LP↔Canvas seam §3.3: any **interface-surface** standard change that would (a) bear on how the OIP
routing layer characterizes the canvas surface, or (b) affect how ISS gates are authored on a canvas archetype, gets a
**heads-up** to `aDNA.aDNA` (OIP) and Argus/ISS through the coordination channel, tagged `seam: Canvas ↔ OIP` /
`seam: Canvas ↔ ISS`. Routine evolution that touches neither needs no external sign-off. (Salon D8 sets when the first
such memos go out — default: at open, formalized at P3.)

## Consequences

### Positive
- The leg-2/leg-3 work has a citable fence: build *contracts + a reference loader*, not engines, transports, or routers.
- Neighbours keep their turf — ISS (gate runtime), Astro (web), Terminal (CLI/TUI), OIP (routing) — with no land-grab.
- The future OIP campaign can layer routing **on top of** a clearly-bounded canvas surface rather than negotiating the
  boundary mid-flight.

### Negative
- Leg 3 stays a **contract** here, so the satisfying "interactive demo" is, at most, the P4 stretch POC — the boundary
  intentionally defers the runtime to a follow-on.
- A real dependency remains on the external **OIP/interface thesis** doc (named in ADR-000, not in this vault) to
  ground the leg-3 spec's vocabulary; if it cannot be acquired, P3 may have to defer (Salon risk register).

### Neutral
- This ADR does **not** touch the canvas-as-primitive question (Δ2 / LIP-0009); that stays on its own LIP track.
- It extends, and does not supersede, ADR-000 §3's substrate-neutrality test — it applies that test to the surface legs.

## Related
- [[adr_000_canvas_identity]] (the three-leg thesis + substrate-neutrality test) · `campaign_canvas_salon.md` ·
  [[spec_context_object]] (leg-2 metadata; the loading "how" is the Salon P1 gap) ·
  `who/coordination/coord_2026_06_13_mondrian_countersign_lp_canvas_seam.md` (the stewardship-split model) ·
  `aDNA.aDNA/how/skills/skill_create_iss.md` + `adr_028_iss_architecture.md` (ISS) · `Astro.aDNA/CLAUDE.md` (web) ·
  `Terminal.aDNA/CLAUDE.md` (CLI/TUI) · `aDNA.aDNA/how/backlog/idea_campaign_operator_interaction_patterns_unification.md` (OIP).
