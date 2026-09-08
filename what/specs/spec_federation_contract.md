---
type: spec
spec_id: spec_federation_contract
title: "aDNA Canvas federation contract — how producers consume the Standard"
standard_version: "2.3.0"
status: ratified
created: 2026-06-12
updated: 2026-09-08
last_edited_by: agent_mondrian
phase: P3
conforms_to: "SiteForge.aDNA/what/artifacts/sf_forge_pattern_spec.md"
tags: [spec, canvas, federation, forge-pattern, genesis, p3, conformance_target, declared_vs_reached, kennedy_finding_1]
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
  version:            "2.3.0"
  version_policy:     minor                                        # minor | locked  (§3)
  conformance_target: core | extended | adna_native               # the level this producer commits to emit (§2.1a)
  specs_used:                                                      # the spec modules consumed
    - what/specs/spec_component_model.md
    - what/specs/spec_panel_link_semantics.md
    - what/specs/spec_roundtrip_protocol_v2.md
    - what/specs/spec_conformance_suite.md
    - what/specs/spec_context_object.md          # if the producer registers canvases as context
  profiles_used:      [ lattice, deck, … ]                         # semantic_bindings profiles (spec_component_model §4)
  local_extensions:   [ ]                                          # producer-specific overlays (never edits to Standard)
```

2.1a. **`conformance_target` (a producer commitment) vs `declared` (a document property) — read this before
filling in the field above.** *(Added 2026-09-08, Blueprint P3, on Kennedy's Finding 1 —
`coord_2026_08_04_kennedy_to_mondrian_wrapper_adopted.md`. The finding cost Oration a **reversed ruling**:
planning read `declared=core` as the artifact's *capability*, concluded that declaring `extended` would be a
false claim, and told the operator so. Verification reversed it. The answer was four words further along the
same line of output they had already read.)*

`canvas-std validate` prints two adjacent values that mean **different things**, and they are easy to conflate:

| Printed | Means | Source |
|---|---|---|
| `declared=` | the level this document **says it is** | `metadata.frontmatter._reserved.conformance_level`, **defaulting to `core` when absent** |
| `level_reached=` | the highest level whose checks the document **actually passes** (monotone) | computed from the content |

Three consequences a producer MUST understand:

1. **`declared=core` is not a capability claim.** It is very often just *"this document carries no `_reserved`
   block"*. A canvas can — and routinely does — print `declared=core level_reached=extended [OK]`, which means
   *it satisfies Extended and simply never said so*. Do not read the first value as a ceiling on the second.
2. ⭐ **A document MAY self-declare `extended` without adopting the aDNA-Native layer.** The
   `_reserved.conformance_level` key is read at **every** level and its enum is
   `["core", "extended", "adna_native"]`; the A-1..A-6 aDNA-Native checks run **only** when the declared level
   *is* `adna_native`. So a `_reserved` block containing **nothing but** `conformance_level: "extended"` is
   valid, sufficient, and yields `declared=extended level_reached=extended [OK]`. **Verified 2026-09-08** on a
   minimal document, both with and without the block:
   ```
   _reserved = {"conformance_level": "extended"}  →  declared=extended  level_reached=extended  [OK]
   (byte-identical, no _reserved)                 →  declared=core      level_reached=extended  [OK]
   --level adna_native, same doc                  →  [FAIL] A-2 adna_version · A-2 conformance_level · A-6 sync
   ```
   ⇒ The `_reserved` carrier and aDNA-Native *semantics* are **not** welded together, contrary to the natural
   reading of `spec_context_object`. An Extended producer that wants its documents to say so can do it today,
   with one key, and stays Extended.
3. **`conformance_target` is the producer's commitment, not a document assertion**, and the two are checked in
   different places: the wrapper field is read by humans and by the §4 stage-3 gate; `declared` is read by the
   tool. Where a producer commits to `extended`, stage 3 SHOULD assert **the committed level appears in the
   output** — `exit 0` alone does not distinguish *"passed at the level I promised"* from *"passed at core and
   silently never attempted more"*. Oration's `CANVAS-SCHEMA` predicate does exactly this and is the reference
   implementation of the check.

⛩ **The enum in §2.1 was also wrong** and is corrected above: it read `extended | adna_native`, excluding
`core`, while a large share of real conformant producers legitimately emit at core. *(Kennedy's originally
intended finding was precisely "the §2.1 enum is too short"; they withdrew it when their premise turned out to
be false, and reported the withdrawal rather than silently substituting a better finding. The withdrawn finding
was right anyway — for a reason neither of us had.)*

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
2. **Runtime** — renders in the producer's engine without error. A canvas surfaced to a human in Obsidian
   additionally requires an **agent-confirmed render**: the agent opens it in live Obsidian, captures a
   screenshot, and reads it before shipping (`what/context/context_canvas_visual_in_the_loop.md`). *(Amendment 1)*
3. **Offline** — **format conformance**: `spec_conformance_suite` `validate(doc, conformance_target)` passes,
   including the degradation tests D-1..D-3 — **and visual fit**: `canvas-visual-check`
   (`what/production/canvas_core/traps/cli.py`; the Obsidian-calibrated geometry traps) reports no high/critical
   findings. *(Amendment 1)*
4. **III semantic review** — **output quality** against the canvas review contract (VR1–VR5 + canvas-visual trap
   schema) via the `iii/` wrapper ([[iii/CLAUDE]]). Engines stay in III.aDNA.
5. **Human gate** — producer-side approval before delivery.

Stage 3 (format) is Canvas.aDNA-owned; stage 4 (quality) is III-owned-engine / Canvas-owned-contract; the
producer **cannot skip** either.

> **Amendment 1 (2026-08-03, Halftone HV).** Stages 2/3 extended with the **visual gate**: schema conformance had
> proven insufficient in the field — a canvas validated `[OK]` and shipped unreadable (Oration M-R5; Kennedy
> coord 2026-08-03). Format ≠ fit ≠ sight: `canvas-std validate` (schema) · `canvas-visual-check` (geometry) ·
> the agent-confirmed render (sight) are three distinct, non-substitutable checks. Authoring rules with the
> measured numbers: `what/docs/canvas_authoring_guidance.md`.
>
> Ratification: **decision** Amendment 1 (visual gate into stages 2/3) · **ratified-by** operator (stanley) ·
> **date** 2026-08-03 (plan approval = the HV gate) · **status** accepted.

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
