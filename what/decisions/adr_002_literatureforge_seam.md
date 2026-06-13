---
type: decision
adr_id: "002"
title: "LiteratureForge seam — document-AS-canvas at the schema layer; pipeline stays a federated producer"
status: proposed
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
signed_by:
supersedes:
superseded_by:
resolves: D3
phase: P2
tags: [adr, canvas, standard, literatureforge, seam, federation, genesis, d3]
---

# ADR-002: LiteratureForge Seam (D3)

## Status

**Proposed** — drafted at P2. **Operator ratifies at the P2 exit gate** (this is the second of the two gate
sign-offs). Couples to [[adr_001_canvasforge_relationship]] (D2). ⚠️ **Operator-input note:** the operator gave
*"absorb"* as a starting point (2026-06-07, pre-campaign). P1 evidence now suggests a substrate-neutral split;
this ADR presents both and recommends — the operator's call at the gate.

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
