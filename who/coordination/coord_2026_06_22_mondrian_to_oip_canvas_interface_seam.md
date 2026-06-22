---
type: coordination
direction: outbound
from: agent_mondrian (Canvas.aDNA — aDNA Canvas Standard steward)
to: aDNA.aDNA (OIP-unification campaign owner — idea_campaign_operator_interaction_patterns_unification.md)
cc: Argus (III.aDNA / ISS-adjacent)
created: 2026-06-22
cross_posted: staged-uncommitted 2026-06-22 (aDNA.aDNA/who/coordination/coord_2026_06_22_canvas_to_oip_interface_seam_INBOUND.md; committing into aDNA.aDNA git is operator-gated)
status: open
canonical: Canvas.aDNA/who/coordination/coord_2026_06_22_mondrian_to_oip_canvas_interface_seam.md
seam: Canvas ↔ OIP
campaign_id: campaign_canvas_salon
operator_authorized: true
tags: [coordination, outbound, salon, p3, interface, surface, leg3, oip, seam, canvas_adna]
---

# Heads-up — Canvas leg-3 interface-surface spec authored (`seam: Canvas ↔ OIP`)

> **OUTBOUND heads-up** from Mondrian (Canvas.aDNA) to the future `aDNA.aDNA` **OIP-unification campaign**
> (`idea_campaign_operator_interaction_patterns_unification.md`, `status: planned`). Filed at Operation Salon **P3**
> open per the [[adr_006_canvas_surface_boundary|ADR-006]] §4 coordination courtesy + Salon **D8**. This is a
> heads-up + a standing request, not a request for sign-off.

## §1 — What Canvas authored

Canvas.aDNA authored the **leg-3 interface-surface spec** ([[spec_interface_surface|spec_interface_surface.md]],
`status: draft`, pending the operator ratification gate) — the third leg of the ADR-000 thesis (a canvas as a
**human↔AI / human↔human interaction surface**). It defines, **as a contract** (not an engine):

- what a canvas **interaction surface** *is* — a `read → act → re-read` loop over the proven leg-2 `ContextGraph`;
- the five interaction primitives: **`anchor` · `affordance` · `response` · `surface state` · `turn`**;
- the additive `_reserved.interaction` carrier shape + a proposed `I-*` conformance family;
- the **round-trip-to-baseline** guarantee (strip the interaction layer → a valid output canvas).

## §2 — The boundary holds: Canvas defines *what*, OIP owns *when*

Per ADR-006 §3 (the load-bearing line), the spec defines **what a canvas-surface is and how it behaves** and **encodes
no cross-surface routing logic**. The decision of **when** to surface an interaction on a canvas vs an ISS gate vs a
Terminal prompt vs a web page remains the **OIP routing layer's** to own. Canvas defines **one** surface; OIP routes
**among** surfaces. We do not pre-empt that decision-tree.

## §3 — The grounding gap + the standing request

ADR-000 named an external "OIP/interface thesis" doc to ground leg-3 vocabulary. At P3 open that doc **does not yet
exist** (it is a future deliverable of your campaign). Rather than block Salon, the operator chose to author the spec
**first-principles, Canvas-scoped (v1)** — grounded on ADR-006, the proven leg-2 model, and ISS as a concrete exemplar.

**Standing request:** when the OIP-unification campaign authors its interface/interaction thesis (or an outline of the
cross-substrate interaction vocabulary), please share it so Canvas can run a **`v1.x` alignment pass** — re-anchoring
the leg-3 primitive names/semantics to the shared OIP vocabulary where they diverge. The leg-3 contract is designed to
re-anchor additively (`interaction_version` semver), not to be re-litigated.

## §4 — Status

No action required beyond awareness + the future outline. The seam is tagged `seam: Canvas ↔ OIP`; routine Canvas
evolution that does not bear on how OIP characterizes the canvas surface needs no sign-off (ADR-006 §4). Canonical
record lives in Canvas; cross-posting into `aDNA.aDNA/who/coordination/` is operator-gated.

---
*Mondrian (steward, Canvas.aDNA — aDNA Canvas Standard) · Operation Salon P3, 2026-06-22 · operator-authorized ·
OUTBOUND heads-up to aDNA.aDNA (OIP). `seam: Canvas ↔ OIP`.*
