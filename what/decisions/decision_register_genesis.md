---
type: decision
adr_id: "register"
title: "Genesis Decision Register (D1–D7) — pre-ADR stubs"
status: open
created: 2026-06-06
updated: 2026-06-12
last_edited_by: agent_stanley
tags: [adr, decision, register, genesis, canvas]
---

# Genesis Decision Register — D1–D7

Pre-ADR stubs for the load-bearing decisions Operation Cartography must resolve. **Nothing here is ratified.**
Each becomes a real ADR (or is folded into `adr_000`) at the gated phase shown. The inherited template ADRs
(`adr_001/002/003`) were **archived → `_inherited_scaffold/` at P1 (2026-06-12)**, freeing the `adr_001+`
namespace; P2 mints D2/D3/D6 (and the component/panel-link/context-object specs) as real ADRs starting at `adr_001`.

| ID | Decision | Resolve at | Owner ADR (P2) | Status |
|----|----------|-----------|----------------|--------|
| D1 | **Category vs runtime** — Framework-pure vs Platform/hybrid; where reference validators/converters live (Δ1) | P0 | `adr_000` §1 | ✅ **resolved — Option P** (Platform/standard-bearer; vault+code split) 2026-06-06 |
| D2 | **CanvasForge relationship** — extract Standard out (A) vs spec-here/impl-in-CanvasForge (B) vs reject (C) | P2 | `adr_001_canvasforge_relationship` | ✅ **ratified — Option A (extract)** 2026-06-12 |
| D3 | **LiteratureForge seam** — document-AS-canvas vs federated-peers vs **absorb** (operator-directed 2026-06-07 → absorb; ratify at P2) | P2 | `adr_002` → `adr_005` (pipeline reshape) | ✅ **ratified — A-schema + B-federated-pipeline** 2026-06-12 (absorb/C set aside) · ✅ **B-pipeline leg reshaped in-vault by `adr_005`** (pt09; ratified 2026-06-19) — adopts the absorb/C path; **A-schema leg stands** |
| D4 | **Component model** — additive `_reserved`-namespaced taxonomy across all 2D outputs | P2 | `spec_component_model.md` | ✅ **ratified** 2026-06-12 |
| D5 | **Panel/link semantics** — reading-order/pagination/flow/region for non-DAG outputs without breaking graph semantics | P2 | `spec_panel_link_semantics.md` | ✅ **ratified** 2026-06-12 |
| D6 | **Versioning & governance** — v2.0.0 line + LIP process + conformance levels + version_policy default | P2 | `adr_003_standard_governance` | ✅ **ratified — v2.0.0 + LIP + Core/Extended/aDNA-Native** 2026-06-12 |
| D7 | **Context-object / primitive status** — canvas-as-primitive vs canvas-as-view (Δ2); LIP path | P2 | `spec_context_object.md` + LIP | ✅ **ratified keep-as-view** 2026-06-12; Δ2 = open LIP (`lip_draft_canvas_as_primitive`) |

---

## D1 — Category vs runtime (Δ1) — ✅ RESOLVED at P0 (operator, 2026-06-06)

**Locked: Option P.** Canvas.aDNA is a **Platform.aDNA (standard-bearer)** that governs the Standard **and
ships its runnable reference tooling** (validators · round-trip converters · conformance harness) as a
**code-as-WHAT-object** at `what/code/canvas_std/` (built in the execution campaign, not this one). The
pure-Framework definition ("deploy no runtime") therefore does not apply.

Considered and set aside: **Option F** (Framework-pure; reference impl stays in CanvasForge `canvas_core`).

**Cascade:** Option P **tilts D2 toward extraction** — the standard machinery (schema, validators, round-trip)
lives in Canvas.aDNA; CanvasForge becomes a producer consuming it. D2 itself is decided at P2.

## D2 — CanvasForge relationship — resolve at P2

- **(A)** Extract the Standard OUT of CanvasForge; CanvasForge consumes via `federation_ref`, becomes a pure
  producer. *(mirrors the lattice-protocol→canvasforge extraction precedent)*
- **(B)** Canvas.aDNA owns spec + conformance suite; CanvasForge keeps `CanvasBuilder` as the canonical
  reference implementation, pinned to the Standard's version.
- **(C)** Reject — leave embedded (document why it fails the unification thesis).
Score, pick, record rejected. Coupled to D1.

## D3 — LiteratureForge seam — resolve at P2

LF's `spec_visual_contract.md` (V1–V8 + X1–X14) already routes visuals to CanvasForge/ComfyForge; its 5-part
genre submodule is the writing analog of a canvas component spec. Decide: does a long-form document become a
**canvas with flow/reading-order/pagination panel-link semantics**, or do LF and Canvas remain **federated
peers sharing component schemas**? Reconcile with Amendment-02 "Document-DNA engine" (verified to *complement*,
not collide — it is a meta-layer above the submodule, orthogonal to canvas rendering). THE unification ADR.

- **(A) document-AS-canvas** — a document is a canvas with flow/reading-order/pagination panel-link semantics.
- **(B) federated peers** — LF + Canvas stay separate, sharing component schemas via `federation_ref`.
- **(C) absorb** *(operator-directed 2026-06-07 — recommended starting point for the P2 ADR)* — subsume
  LiteratureForge **into** Canvas to recenter all 2D-output creation here. Requires a **superseding ADR re-opening
  P0 Option-P scope**: Canvas → a **two-faced 2D-output platform** (Standard face stays producer-neutral; Producer
  face absorbs LF's composition pipeline, Thoth as composition sub-persona). Two operator forks remain (producer
  scope: LF-only vs all-producers incl. CanvasForge/ComfyForge — couples to **D2**; and the substrate-neutrality
  firewall). Full rationale + preservation inventory + forks:
  `aDNALabs.aDNA/what/migration/decision_literatureforge_canvas_subsumption.md` (migration **WS-7**). **Not ratified
  here** — phase gates are human gates; resolve at P2.

## D4 — Component model — resolve at P2

Additive, `_reserved`-namespaced taxonomy generalizing across outputs: {text, typography-run, image, video,
shape, embed, group/panel, link/edge, table, code, caption, region}. Each component: schema · position/qualities
· aDNA semantic-type binding · visual-DNA hook (`brand_style_pack_ref`) · degradation rule to baseline Obsidian.
Formalize "panel" (= group) and "possibly-linked panels."

## D5 — Panel/link semantics for non-DAG outputs — resolve at P2

Papers/letters/articles need flow + pagination; decks need slide-sequence; comics need page + reading-path;
sites need responsive regions. Express these as typed edges (reading-order/dependency/adjacency/sequence) +
region properties (pagination/flow/responsive) **without breaking lattice-graph semantics**.

## D6 — Versioning & governance — resolve at P2

v2.0.0 successor line; LIP-style change process (real mechanism: `lip_0001_lip_process.md`); conformance levels
**Core / Extended / aDNA-Native**; consumer `version_policy` default **minor**.

## D7 — Context-object / primitive status (Δ2) — resolve at P2 (+ LIP)

How an aDNA canvas is a first-class **context** object: stored, referenced (wikilinks / `federation_ref`),
versioned; read-AS-context vs render-AS-output. **Δ2:** today canvas is a *view/serialization of the `lattice`
primitive* (aDNA Decision 9), not a 4th primitive; the deployable-object set (module/dataset/lattice) is
extensible via `{namespace}_{type}` but elevating canvas to first-class needs a **LIP** + an argument that a
canvas carries semantics beyond "a lattice rendered visually." Do **not** touch the aDNA core primitive set in
this campaign (out of scope).
