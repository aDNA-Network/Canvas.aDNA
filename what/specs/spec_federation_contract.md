---
type: spec
spec_id: spec_federation_contract
title: "aDNA Canvas federation contract — how producers consume the Standard"
standard_version: "2.0.1"
status: ratified
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
phase: P3
conforms_to: "SiteForge.aDNA/what/artifacts/sf_forge_pattern_spec.md"
tags: [spec, canvas, federation, forge-pattern, genesis, p3]
---

# aDNA Canvas Federation Contract

> **Status: RATIFIED 2026-06-12 (operator, P2 gate) — P3 deliverable, HELD at the P3 exit gate.** Defines how a
> producer consumes the aDNA Canvas Standard, conforming to the **SiteForge forge pattern**
> (`SiteForge.aDNA/what/artifacts/sf_forge_pattern_spec.md`). Pull-based, agent-time context loading; **no runtime
> linking**. Worked for CanvasForge + an LF-successor + a net-new producer. RFC 2119 keywords.

## 1. Model

Canvas.aDNA is the **standard-bearer**: it owns the spec set + the `canvas_std` reference tooling (Option P). A
**producer** (CanvasForge, an LF-successor, ComfyForge, SiteForge, or a net-new 2D-output vault) consumes the
Standard via a **`canvas/` wrapper directory** in the producer vault. Federation is **design-time** — the
producer's agent loads the Standard at session time (local FS / git / registry); there is no API call.

## 2. The `canvas/` consumer wrapper

2.1. A producer that emits aDNA canvases **MUST** carry a `canvas/` wrapper containing `CLAUDE.md` with a
`federation_ref` block. Canonical field set (extends the sf_forge core additively):
```yaml
federation_ref:
  source_vault:       Canvas.aDNA
  source_path:        ~/aDNA/Canvas.aDNA
  source_spec:        what/specs/spec_adna_canvas_standard.md      # the normative core
  source_impl:        what/code/canvas_std/                        # reference validator/converters (Option P)
  version:            "2.0.1"
  version_policy:     minor                                        # minor | locked  (§3)
  conformance_target: extended | adna_native                      # the level this producer commits to emit
  specs_used:                                                      # the spec modules consumed
    - what/specs/spec_component_model.md
    - what/specs/spec_panel_link_semantics.md
    - what/specs/spec_roundtrip_protocol_v2.md
    - what/specs/spec_conformance_suite.md
    - what/specs/spec_context_object.md          # if the producer registers canvases as context
  profiles_used:      [ lattice, deck, … ]                         # semantic_bindings profiles (spec_component_model §4)
  local_extensions:   [ ]                                          # producer-specific overlays (never edits to Standard)
```

2.2. **graft vs reference** (sf_forge decision tree): a `.lattice.yaml` or the spec set is **referenced** via
`federation_ref` (never copied). A non-lattice context file the producer's agent must *read* at session time is a
**graft** (copied with provenance in `canvas/graft_manifest.yaml`: `id`, `source_vault: Canvas.aDNA`,
`graft_date`, `source_sha`, `topics[]`). Anything not read at session time is a **doc pointer**.

## 3. Version policy

`version_policy: minor` (default) — the producer auto-adopts patch/minor; a **major** bump (e.g. 2.x→3.0)
**MUST** trigger re-validation against the conformance suite before adoption. `locked` — no change without
explicit producer action. **Caveat (pre-1.0 producers):** a producer pinning a pre-1.0 dependency by commit uses
`version_policy: tracking` + `pinned_at_commit` (as today's `CanvasForge→ComfyForge` wrapper does); `tracking` is
permitted for transitional consumers but a 2.0.0-conformant producer **SHOULD** pin `minor` once the Standard ships.

## 4. The 5-stage gates (sf_forge), Canvas-specialized

A producer's build of an aDNA canvas **MUST** pass, in order:
1. **Build-time** — the canvas is well-formed JSON; node/edge ids unique.
2. **Runtime** — renders in the producer's engine without error.
3. **Offline** — **format conformance**: `spec_conformance_suite` `validate(doc, conformance_target)` passes,
   including the degradation tests D-1..D-3.
4. **III semantic review** — **output quality** against the canvas review contract (VR1–VR5 + canvas-visual trap
   schema) via the `iii/` wrapper ([[iii/CLAUDE]]). Engines stay in III.aDNA.
5. **Human gate** — producer-side approval before delivery.

Stage 3 (format) is Canvas.aDNA-owned; stage 4 (quality) is III-owned-engine / Canvas-owned-contract; the
producer **cannot skip** either.

## 5. Wrapper discipline (what goes where)

| Lives in **Canvas.aDNA** (referenced, never copied) | Lives in the **producer `canvas/` wrapper** |
|---|---|
| The spec set; the `canvas_std` validator/converters/conformance harness; the `lattice` semantic profile | Producer-specific `semantic_bindings` profiles (deck/comic/letter), layout/composition, rendering engines, brand packs |

A producer **MUST NOT** copy the validator or re-derive the schema; it references them. New expressive needs are
proposed **upstream** (a LIP / a new profile), **never** bolted onto baseline canvas fields (substrate-neutrality,
C8; [[spec_adna_canvas_standard]] §11.3).

## 6. Worked consumers

### 6.1 CanvasForge (producer; post-D2 extraction)
Per [[adr_001_canvasforge_relationship]] (Option A), CanvasForge's `canvas_core` reference logic is **extracted to
`canvas_std`**; CanvasForge keeps `layout_*`, `selection_board`, deck/comic composition, and the PDF/GDoc export
engines. Its `canvas/` wrapper: `source_vault: Canvas.aDNA`, `version_policy: minor`, `conformance_target:
adna_native`, `profiles_used: [lattice, deck, comic]`, `local_extensions: [layout engines, selection board]`.
Migration is parity-gated (execution campaign P4) behind a deprecation shim mirroring the
`lattice-protocol→canvasforge` precedent.

### 6.2 LF-successor (federated producer; per D3 Option B)
Per [[adr_002_literatureforge_seam]] (A-schema + B-pipeline), the LiteratureForge-successor is a **federated
producer**: it consumes `spec_component_model` (document components) + `spec_panel_link_semantics` (ordered
sections / pagination / reading-order) + `spec_roundtrip_protocol_v2` (the canonical surface is the round-trip
authority). It keeps its writing pipeline (genre submodule, trap-packs, reviewer voices) producer-side.
`conformance_target: adna_native`; `profiles_used: [document]`.

### 6.3 Net-new "letter" producer (proof of generality)
A brand-new, minimal producer that emits a one-page **letter** as an aDNA canvas — proving the Standard serves an
output neither CanvasForge nor LF originated. Wrapper: `conformance_target: extended`, `profiles_used: [document]`,
a single `region` panel with `flow: vertical`, `pagination: paged`, `extent: {unit: pages, max: 1}`. No `_reserved`
beyond `panel_link` + `sync` ⇒ degrades to a plain Obsidian canvas. (Reference shape: `example_canvas_v2.lattice.yaml`.)

## 7. Conformance

A conformant producer **MUST**: carry a `canvas/` wrapper with a valid `federation_ref`; emit canvases at its
declared `conformance_target`; attach a `spec_conformance_suite` report to each build (5-stage gate 3); route
quality through the `iii/` wrapper (gate 4). Absence of the wrapper, or copying the validator, is non-conformant.

## 8. Related
- `SiteForge.aDNA/what/artifacts/sf_forge_pattern_spec.md` (the pattern) · [[adr_001_canvasforge_relationship]] · [[adr_002_literatureforge_seam]] · [[spec_conformance_suite]] · [[iii/CLAUDE]] · `what/lattices/examples/example_canvas_v2.lattice.yaml`.
