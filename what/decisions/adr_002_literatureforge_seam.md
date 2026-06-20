---
type: decision
adr_id: "002"
title: "LiteratureForge seam — document-AS-canvas at the schema layer; pipeline stays a federated producer"
status: ratified
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
signed_by: Stanley (operator) — P2 gate 2026-06-12
supersedes:
superseded_by: "adr_005 (Option-B federated-pipeline leg only — pt09 reshape; the Option-A schema-absorb leg stands)"
resolves: D3
phase: P2
tags: [adr, canvas, standard, literatureforge, seam, federation, genesis, d3]
---

# ADR-002: LiteratureForge Seam (D3)

> **⚠ Partially superseded (2026-06-19) — [[adr_005_lf_successor_in_vault|ADR-005]] (ratified 2026-06-19).** pt09
> (2026-06-17) merged CanvasForge into Canvas, so the **Option-B *federated*-pipeline leg below is overtaken by
> events**: the LF-successor is now built **in-vault** (`what/production/`), per ADR-005 (the "separate
> scope-reopening ADR" this ADR's §Consequences prescribed). **The Option-A schema-absorb leg (§Decision 1) stands
> unchanged** — the LF contracts already live in `canvas_std`. This ADR keeps `status: ratified` for that live leg.

## Status

**Ratified** — 2026-06-12 (Stanley, operator) at the **P2 exit gate**. Drafted at P2; couples to
[[adr_001_canvasforge_relationship]] (D2). **Ratified outcome: A-schema-absorb + B-federated-pipeline** (the
recommended substrate-neutral split). The operator's earlier *"absorb"* lean (2026-06-07) — Option C, the
two-faced platform — was **considered and set aside** at the gate; it remains documented in §Decision as a future
scope-reopening path should consumer evidence later warrant it.

## Context

LiteratureForge (Thoth, wound down → `Archive.aDNA/`) left three specs ([[p1_source_inventory]] §D): a
**visual-contract** (V1–V8 + X1–X14; routes visuals to canvas/raster engines), a **format-contract** (F1–F7;
ordered/order-locked `sections`, `output_surfaces`, `round_trip_surface`), and a **genre-submodule** (the 5-part
writing bundle). The thesis question: is a long-form **document** expressible *as a canvas*?

**P1 signal (decisive):** the LF format-spec's `round_trip_surface` **already cross-references the Canvas
Round-Trip Protocol** — the two are *already* contractually coupled. And the evidence cleanly separates two
layers: the **schema/contract layer** (substrate classification, ordered sections = reading-order/flow,
output-surfaces, naming/orphan link-checking, brand-style-pack federation) is canvas-native and wants to live in
the Standard; the **writing-pipeline layer** (trap-packs, reviewer-voice scoring, the generate→review lifecycle,
genre register) is producer logic no canvas Standard should hold.

## Decision

Resolve D3 as a **two-layer** answer:

1. **Schema layer → document-AS-canvas (Option A).** The Standard expresses a document as a canvas: long-form
   structure becomes **panel/link semantics** (reading-order / flow / pagination / region — [[adr_003_standard_governance]]'s
   conformance levels apply; specified in `spec_panel_link_semantics.md`), and the LF visual/format **contracts**
   are absorbed into the component model (`spec_component_model.md`) and round-trip v2. The editable
   `round_trip_surface` unifies with the Standard's authoritative-source ↔ view model.

2. **Pipeline layer → federated producer (Option B), recommended over absorb (Option C).** The writing-composition
   pipeline (genre submodule, trap-packs, reviewer voices, reward rubrics) lives in an **LF-successor producer**
   that federates against the Standard via a `federation_ref` wrapper — **symmetric with D2** ([[adr_001_canvasforge_relationship]]:
   CanvasForge is also a pure producer). This **preserves Canvas.aDNA's substrate-neutrality** (C8): the Standard
   face stays producer-neutral; Canvas does not grow a writing pipeline.

**The operator's fork at the gate — B vs C for the pipeline home:**
- **(B) federated peer (recommended).** LF-successor is a separate producer. Canvas stays a single-faced
  standard-bearer. Substrate-neutrality intact; uniform with D2. Cost: a document's *composition* lives outside
  Canvas (but its *schema* lives inside).
- **(C) absorb — two-faced platform** *(operator's prior lean).* Canvas grows a **producer face** that absorbs LF's
  pipeline (Thoth as a composition sub-persona), per `aDNALabs.aDNA/what/migration/decision_literatureforge_canvas_subsumption.md`.
  This **re-opens the P0 Option-P scope** ([[adr_000_canvas_identity]] §1) — Canvas becomes standard-bearer *and*
  producer. Two sub-forks then arise: producer scope (LF-only vs all-producers incl. CanvasForge/ComfyForge —
  couples to D2) and a substrate-neutrality firewall to keep the Standard face producer-neutral.

**Recommendation: A (schema) + B (pipeline federated).** It captures everything the P1 evidence shows wants to
live in the Standard (the contracts) without compromising substrate-neutrality, and it keeps the architecture
uniform with the D2 extraction. If the operator prioritizes recentering *all* 2D-output creation in Canvas, **C**
is the documented alternative — but it is a larger, scope-reopening commitment.

## Consequences

### Positive (A+B)
- Documents become first-class canvases at the schema layer; the existing round-trip coupling is honored, not duplicated.
- Substrate-neutrality preserved; D2/D3 symmetric (both producers federate against one Standard).

### Negative / Risk
- If the operator later wants absorb (C), that is a separate scope-reopening ADR (superseding this one's pipeline clause).
- The LF-successor producer must be stood up (or its specs re-homed) — tracked as an execution-campaign item, not now (C3).

### Neutral
- Either way, the **schema absorption (A)** is identical — `spec_component_model.md` + `spec_panel_link_semantics.md`
  + round-trip v2 absorb the LF contracts regardless of where the pipeline ends up.

## Related
- [[adr_001_canvasforge_relationship]] (D2 symmetry) · [[adr_003_standard_governance]] · [[p1_source_inventory]] §D ·
  `spec_panel_link_semantics.md` · `spec_component_model.md` ·
  `aDNALabs.aDNA/what/migration/decision_literatureforge_canvas_subsumption.md` (absorb rationale + preservation inventory).
