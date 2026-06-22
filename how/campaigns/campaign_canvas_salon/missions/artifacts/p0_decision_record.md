---
type: decision_record
created: 2026-06-22
updated: 2026-06-22
status: ratified
last_edited_by: agent_stanley
campaign_id: campaign_canvas_salon
mission: mission_p0_charter_boundary
tags: [canvas, salon, surface, decision, p0, boundary, context_object, interface]
---

# P0 Decision Record — canvas-as-surface charter + boundary (Operation Salon)

**Purpose:** resolve the eight governance/scope questions that gate the leg-2 (context-object) and leg-3 (interface-
surface) work, **before any spec or code**. Each decision carries a doctrine-aligned **recommended default** + rationale
+ the alternative considered. The operator ratifies (accept / edit) at the **P0→P1 gate**; ratification **activates**
Operation Salon (`status: active`) and authorizes Phase P1 (the leg-2 loading-protocol spec). Ratifying this record also
accepts the **phase arc P0–P5** as charted in `campaign_canvas_salon.md`.

> **Foundation (confirmed this session):** Leg 1 is proven ×7 (Palette). Leg 2 — [[what/specs/spec_context_object|spec_context_object.md]]
> (D7, ratified) defines the `_reserved.context_object` metadata (`id`/`version`/`refs`/`summary`) and says a canvas
> **SHOULD** be loadable/traversable without rendering, but **does not define the loading/traversal protocol** ("how").
> Leg 3 is **greenfield** — no interface-surface spec exists; ADR-000 names an external **"OIP/interface thesis"** doc
> **not in this vault**; a *future* `aDNA.aDNA` **OIP-unification campaign** owns cross-surface **routing**. `adr_006`
> confirmed as the next free ADR number; `campaign_canvas_salon` does not collide with an existing slug.

---

## D1 — Codename / slug

**Recommended: Operation Salon / `campaign_canvas_salon`.** A *salon* carries an apt double meaning for the two legs:
an **exhibition surface** where work is displayed and read (leg 2 — canvas as readable context) **and** a **gathering of
minds** where parties meet and converse (leg 3 — canvas as human↔AI / human↔human interface). Art-historically of a
piece with Mondrian. Complements Keystone (reference impl), Atelier (production studio), and Palette (output family).

*Alternatives considered:* **Atrium** (a shared meeting space — strong on leg 3, weak on leg 2); **Loom** (weaving
ref-threads — strong on leg 2, weak on leg 3). Cosmetic; a rename is a one-line `git mv` before P1.

---

## D2 — Campaign type

**Recommended: planning / proving campaign (the Cartography model), not a direct build.** Cartography (P0–P5) chartered
and specified before Keystone built; this campaign mirrors that: it produces a boundary ADR, the leg-2 protocol + a
*reference* loader pilot, the leg-3 spec, and a follow-on charter — and HOLDs at every gate. Legs 2 & 3 are too
under-specified (leg-2 "how" missing; leg-3 greenfield + cross-vault-entangled) to charge straight into a runtime build.

*Alternative:* a direct build campaign (E-phases) that ships a leg-2 loader + a leg-3 runtime. Rejected as default —
"orient first, gate always": specifying and bounding precedes building when the design space is open.

---

## D3 — Leg sequencing

**Recommended: leg 2 first (spec → impl → pilot), then leg 3 (spec).** Leg 2 already has a ratified metadata spec, so
its remaining work is concrete and provable (author the "how" → build a loader → load a known-good producer `.canvas`).
That proof yields the readable-context substrate the leg-3 interface naturally builds on (an interaction surface is, in
part, a context object you can also write to). Leg 3, being greenfield + dependent on an external doc, comes after.

*Alternative:* leg 3 first (spec the interface vision, then make context-loading serve it). Rejected — it front-loads
the riskiest, least-grounded work and would likely stall on the missing OIP doc.

---

## D4 — Leg-3 depth in this campaign

**Recommended: spec-only (defer the leg-3 *build* to a follow-on); the P4 POC is a stretch, taken only if budget
remains.** Leg 3 is greenfield and its vocabulary depends on the external OIP/interface thesis doc; committing to a
runtime build now would over-extend into cross-vault territory the OIP campaign owns. Producing a ratified
interface-surface **spec** (P3) + an optional minimal **POC** (P4) is the right, bounded unit of proof; a full leg-3
build campaign is chartered at P5 if warranted.

*Alternative:* commit a leg-3 runtime build in-campaign. Rejected — premature (no spec yet, external dependency, OIP
boundary still settling).

---

## D5 — Leg-2 spec home

**Recommended: a NEW spec, `what/specs/spec_canvas_context_loading.md`, that references and stabilizes
`spec_context_object.md`.** The ratified context-object spec defines the metadata and *declares* loadability; the new
spec supplies the **protocol** it left unspecified (how an agent resolves `context_object` + `refs` + `summary`, parses
panel/component/edge structure into a traversable graph, and resolves wikilinks/`federation_ref`). Keeping it separate
preserves the ratified spec unchanged and gives the protocol its own version surface.

*Alternative:* amend `spec_context_object.md` in place. Rejected as default — it re-opens a ratified spec for a
substantial addition; a referencing companion spec is cleaner and lower-risk. (Trivial to merge later if desired.)

---

## D6 — Leg-2 impl placement + firewall posture  *(the load-bearing decision)*

**Recommended: build the loader as a NEW sibling package (`what/code/canvas_context/`) that imports `canvas_std`
read-only — the `canvas_std` firewall stays intact (git-diff 0).** `canvas_std` has been frozen since Keystone; 82
tests and 7 producers depend on it. A read-only sibling loader proves leg 2 without risking that surface, and can be
**folded into `canvas_std` later** at a deliberate Standard release if the loader graduates to core reference tooling.

*Alternative:* extend `canvas_std` directly (treat the loader as a sanctioned reference-impl capability — which, per
ADR-000 §3, `canvas_std` legitimately owns: "validators · round-trip converters · conformance harness"). This is
defensible — leg-2 loading **is** Standard reference tooling, not a producer — but it **deliberately lifts the
frozen-since-Keystone firewall** and accepts regression risk across the dependent suites. Surfaced as an explicit
operator choice precisely because it changes that guarantee. If chosen, the firewall check is replaced by full
regression of `canvas_std` + all 7 producer suites at each gate.

---

## D7 — Boundary ADR (`adr_006`)

**Recommended: accept `adr_006_canvas_surface_boundary` as drafted.** Canvas-as-surface owns the substrate-neutral
**data model + contracts** (context-loading + interface-surface) and conformance — **not** engines/runtimes/transport,
and **not** cross-surface routing. Boundary fixed vs **ISS** (gate runtime), **Astro** (web), **Terminal** (CLI/TUI),
and the future **OIP** (routing), on the LP↔Canvas stewardship-split model + a heads-up coordination courtesy.

*Alternative:* widen Canvas's claim to include a leg-3 interaction *runtime* (not just the contract), or narrow it to
leg 2 only. Rejected — the former collides with ISS/OIP; the latter abandons leg 3, which is the point of the campaign.

---

## D8 — Cross-vault coordination posture

**Recommended: send heads-up memos now (at open) to `aDNA.aDNA` (OIP) + Argus/ISS; formalize the seam at P3.** Because
leg 3 sits adjacent to the OIP routing layer and the ISS gate surface, an early heads-up keeps the leg-3 spec coherent
with both and surfaces the OIP/interface thesis doc (needed for P3). The formal two-sided seam (LP↔Canvas style) lands
when the leg-3 spec is concrete, at P3.

*Alternative:* defer all coordination to P3. Rejected as default — early notice de-risks the P3 doc dependency and
avoids surprising neighbours; it costs one memo.

---

## Ratification

| # | Decision | Default | Operator disposition |
|---|----------|---------|----------------------|
| D1 | Codename / slug | Operation Salon / `campaign_canvas_salon` | **ratified** (default) |
| D2 | Campaign type | Planning / proving (Cartography model) | **ratified** (default) |
| D3 | Leg sequencing | Leg 2 first (spec→impl→pilot), then leg 3 spec | **ratified** (default) |
| D4 | Leg-3 depth | Spec-only; P4 POC stretch; build → follow-on | **ratified** (default) |
| D5 | Leg-2 spec home | New `spec_canvas_context_loading.md` (keep `spec_context_object.md` stable) | **ratified** (default) |
| D6 | Leg-2 impl + firewall | New sibling `canvas_context` (firewall preserved) vs extend `canvas_std` (firewall lifted) | **ratified** — new sibling `canvas_context` (firewall preserved) |
| D7 | Boundary ADR | Accept `adr_006` as drafted | **ratified** (default) |
| D8 | Coordination posture | Heads-up memos now; formal seam at P3 | **ratified** (default) |

> **✅ RATIFIED 2026-06-22 (operator, P0→P1 gate).** All eight decisions accepted at their doctrine-aligned defaults
> (D6 = the firewall-preserving sibling `canvas_context`). This activates Operation Salon (`status: active`) and opens
> Phase P1. Recorded in `session_stanley_20260622_140033_salon_p0_ratify_p1_spec`.

On ratification: set this record **and** `adr_006` `status: ratified`; update the campaign Decision Points; complete
mission P0.1 (+AAR); set the campaign `status: active`; and open Phase P1 (author the P1 mission — the leg-2
loading/traversal protocol spec, home per D5, firewall posture per D6). **← actioned this session.**
