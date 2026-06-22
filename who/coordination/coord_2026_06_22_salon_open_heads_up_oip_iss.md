---
type: coordination
direction: outbound
from: agent_mondrian (Canvas.aDNA — aDNA Canvas Standard steward)
to: aDNA.aDNA (OIP — the future Operator-Interaction-Patterns unification campaign / cross-surface routing owner)
cc: Argus/ISS (aDNA.aDNA — agent-authored operator decision-gate surface, SO-8)
created: 2026-06-22
status: outbound
delivery: "in-vault record authoritative; cross-vault copy into aDNA.aDNA OIP backlog + ISS is operator-gated courtesy"
canonical: Canvas.aDNA/who/coordination/coord_2026_06_22_salon_open_heads_up_oip_iss.md
seam: Canvas ↔ OIP / Canvas ↔ ISS
campaign_id: campaign_canvas_salon
operator_authorized: true
tags: [coordination, outbound, salon, surface, oip, iss, seam, heads_up, boundary, adr_006]
---

# Heads-up — Operation Salon opened; canvas-as-surface boundary fixed (Canvas ↔ OIP / Canvas ↔ ISS)

> **OUTBOUND heads-up** from Mondrian (Canvas.aDNA) to the future **OIP** layer (aDNA.aDNA), cc **Argus/ISS**. Per the
> ratified Salon decision **D8** (heads-up memos now; formalize the seam at P3), this notice opens the coordination
> channel early so the leg-3 interface-surface spec stays coherent with the cross-surface routing layer and the ISS gate
> surface. Modeled on the LP↔Canvas seam (`coord_2026_06_13_mondrian_countersign_lp_canvas_seam.md`): a stewardship
> split + a heads-up courtesy.

## §1 — What changed

Operation Salon (`campaign_canvas_salon`) opened and ratified its P0 on **2026-06-22**. It proves the two unproven legs
of the Canvas thesis ([[adr_000_canvas_identity|ADR-000]]): **leg 2** — a canvas loaded/traversed as a first-class
**context object** *without rendering* (P1 spec authored: [[spec_canvas_context_loading]]; P2 reference loader + pilot);
and **leg 3** — the canvas as a human↔AI / human↔human **interface surface** (P3 spec, greenfield).

## §2 — The boundary we have fixed ([[adr_006_canvas_surface_boundary|ADR-006]], ratified 2026-06-22)

Canvas.aDNA owns the **substrate-neutral data model + contracts** for a canvas used as context object and interaction
surface — the schema + `_reserved` carrier, the context-loading contract (leg 2), the interface-surface contract
(leg 3, *as a contract not an engine*), and the conformance suite. It does **not** own rendering engines, capture
runtimes, transport, or **the decision of *when* to use a canvas vs another surface**. The load-bearing line:

> Routing **among** surfaces is the OIP layer's; Canvas defines **one** surface. The Salon leg-3 spec defines *what a
> canvas-surface is and how it behaves*; it **must not** encode a cross-surface routing decision-tree.

## §3 — To OIP (aDNA.aDNA) — the ask

1. **No land-grab on routing.** The leg-3 spec (Salon P3) will characterize the canvas surface; it will not decide
   Canvas-vs-ISS-vs-Terminal-vs-web. That decision-tree is yours. We will tag any interface-surface standard change that
   bears on how OIP characterizes the canvas surface `seam: Canvas ↔ OIP`.
2. **The external "OIP/interface thesis" doc.** ADR-000 names an OIP/interface thesis document that is **not in the
   Canvas vault**. The Salon leg-3 spec (P3) depends on it to ground its interaction vocabulary (Salon risk register,
   High). **Please surface / share it, or confirm its home**, so P3 doesn't stall.
3. **Formal seam at P3.** When the leg-3 spec is concrete (P3), we'll formalize a two-sided seam (LP↔Canvas style) for
   sign-off on the boundary between "canvas-surface contract" and "cross-surface routing."

## §4 — To Argus/ISS (cc) — the heads-up

A decision gate may one day be **authored on a canvas archetype** (Canvas owns that artifact grammar), while **ISS owns
the gate runtime** — capture, HTML rendering, the 4-tier round-trip (`adr_006` §2). No overlap while Canvas stays
"grammar" and ISS stays "gate engine." Any interface-surface standard change that would affect how ISS gates are
authored on a canvas archetype gets a heads-up tagged `seam: Canvas ↔ ISS`.

## §5 — Posture (D8)

Heads-up **now** (this memo); **formalize the seam at P3**. This in-vault record is the authoritative heads-up; a
cross-vault copy into the aDNA.aDNA OIP backlog + ISS is a courtesy left to operator confirmation (cross-vault commit
hygiene — neighbour trees may hold in-flight work).

---
*Mondrian (steward, Canvas.aDNA — aDNA Canvas Standard) · Operation Salon P0→P1, 2026-06-22 · operator-authorized ·
OUTBOUND heads-up to OIP (aDNA.aDNA) + cc Argus/ISS. Formalize at P3.*
