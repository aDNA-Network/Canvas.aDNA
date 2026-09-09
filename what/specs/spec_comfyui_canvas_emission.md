---
type: specification
spec_id: comfyui_canvas_emission
title: "ComfyUI Canvas Emission — variant-selection boards + tuning surfaces as aDNA-Native canvases"
version: "0.2"
status: draft
created: 2026-08-22
updated: 2026-09-08
last_edited_by: agent_mondrian
authored_in: "Operation Blueprint P0 (charter artifact); Canvas's side implemented at P4 (2026-09-08)"
counterpart: "ComfyUI.aDNA (Vulcan) — restart-campaign canvas-emission phase implements the driver side"
depends_on:
  - what/specs/spec_canvas_review_surface.md (v1.0, ratified — the affordance grammar this reuses)
  - what/specs/spec_rlhf_seam.md (capture → Schema-A + III routing)
  - canvas_std interaction layer v2.2.0 (adr_007; I-1/I-2/I-3)
  - adr_010_artifact_corpus_policy.md (images live on the data plane / artifacts shelf)
tags: [spec, comfyui, canvas_emission, variant_selection, tuning_surface, interaction, rlhf, seam]
---

# ComfyUI Canvas Emission v0.1 (draft)

## Thesis

ComfyUI-driven imagery should be **authored, reviewed, and tuned through canvas surfaces**. The
substrate already exists on both sides: Canvas's v2.2.0 `_reserved.interaction` overlay (choice /
input / annotation / action affordances) + the ratified review-surface spec + the working
`review_canvas.py`/`review_collect.py` pilot — and ComfyUI's own declared intents: the
`canvas_json` media type, the visual-inspection doctrine's *"contact sheet / Canvas surface"*
clause, and the never-implemented `lattice_variant_selection` board scaffold ("follows the comic
pipeline's variant selection board pattern"). This spec binds them.

**Boundary (unchanged):** "Canvas dispatches, it does not diffuse." Pixels, models, and workflows
are Vulcan's; canvases and interaction schemas are Mondrian's. The seam is *files + HTTP*, never
shared code.

## §1 The two surfaces

### §1.1 Variant-selection board (satisfies Vulcan SO-5: human-gated selection)

An aDNA-Native canvas presenting one generation run's variants for a human verdict.

- **Nodes**: one `file` node per variant (referencing data-plane paths — never embedded bytes,
  per adr_010); a run-header text node; per-variant caption nodes.
- **`_reserved.interaction`** (v2.2.0 grammar): a `choice` affordance per selection slot
  (options = the variant ids; multi-variant runs = one choice per panel/slot); optional
  `annotation` affordances for free-text critique; verdicts land as **sidecar responses** exactly
  as the ratified review-surface spec defines — the `review_collect` path then routes to Schema-A
  (`SelectionRecord`) + the III store per `spec_rlhf_seam` (reject vocabulary still gated on
  Argus, `REJECT_VOCABULARY_CONFIRMED`).
- **Provenance floor (per variant, in node metadata)**: `workflow` (the SO-10-versioned workflow
  JSON name), `model` (registry id — a real one; defaults describe absence, never a model name),
  `seed`, `denoise`, `lora_refs[]` (empty when LoRA-less), `source_backend`.
- This board **is the HR pilot's second consumer** — the first consumer reviewed SS style variants;
  this one reviews ComfyUI runs. Same collector, same idempotency, same `{kind: ai}`/human
  attribution discipline.

### §1.2 Tuning surface (canvas as the knob panel)

A canvas over one variant (or a small set) whose interaction overlay carries **`input`**
affordances bound to re-render parameters — `denoise` · `steps` · `cfg` · prompt-delta ·
optional `lora_strength` — plus one **`action`** affordance (`re_render`) whose response is a
*request record*, not an execution: the driver (ComfyUI side, or Canvas's `comic_render` chain)
polls/collects request records and dispatches new runs, producing a new board (§1.1). The canvas
never talks to `:8188` itself; the human never edits workflow JSON.

## §2 Who builds what

| Side | Owns |
|---|---|
| **Canvas (Blueprint P4)** | The board/tuning **builders** (extending `canvas_core/rlhf/review_canvas.py`) consuming a run manifest (§3); the interaction schemas; collection + routing (`review_collect`); conformance (validate + visual gate). |
| **ComfyUI (restart campaign)** | The **run manifest** emission after each generation batch (§3) — implementing `lattice_variant_selection` as "emit manifest → board appears"; the re-render dispatcher consuming §1.2 request records; SO-2 registry truth for the provenance floor. |
| **Either** | May emit the canvas *directly* (using `canvas_std` as a library) instead of via manifest — the canvas contract (§1) is the interface; the manifest (§3) is the convenience path. |

## §3 Run manifest v0.1 (the convenience interface)

One JSON file per generation run, beside the variants:

```json
{
  "run_id": "…", "created": "…", "driver": "comfyui|comic_render|other",
  "slots": [{
    "slot_id": "…",
    "variants": [{
      "variant_id": "…", "path": "relative/to/manifest.png",
      "workflow": "workflow_comic_panel_refine.json", "model": "sdxl_base_1.0",
      "seed": 12345, "denoise": 0.4, "lora_refs": [], "source_backend": "comfy"
    }]
  }]
}
```

Additive evolution only in 0.x; consumers ignore unknown keys.

### §3a Executable fixtures — the contract, in a form that can be run against (added v0.2)

Canvas's consumer shipped first, so the manifest interface is pinned by **fixtures rather than
prose**. An emitter that satisfies these satisfies the seam:
`what/production/canvas_core/tests/fixtures/run_manifests/`

| Fixture | Asserts |
|---|---|
| `well_formed.json` | the happy path — 2 slots, 3 + 2 variants, full provenance floor |
| `partially_failed.json` | a variant whose image never landed is **excluded and named**; a slot that loses all of them is reported, not vanished |
| `unknown_keys.json` | keys from a newer emitter are **ignored and reported**, never fatal |
| `missing_provenance.json` | a floor gap is `<absent>`, **never back-filled from a sibling variant** |
| `print_size.json` | a 2062×3150 page sizes into its cell instead of overflowing it |

Three behaviours worth stating outright, because each was a defect before it was a rule:

1. **`path` is relative to the manifest** (the manifest travels with its pixels) — but a canvas
   file node is resolved against the **vault root**, so the consumer converts. An emitter need not
   care; a *different* consumer must.
2. **The filesystem outranks the run record.** A variant is reviewable iff its image exists. A
   half-failed batch still produces a board of what landed.
3. **Absence is explicit.** `"model"` missing ≠ `"model": "unknown"`. The `SelectionRecord` this
   board feeds outlives the board, and a variant attributed to the wrong model poisons the corpus
   quietly.

## §4 Sequencing

1. **This draft** rides memo #14 to Vulcan and feeds the ComfyUI restart charter's
   canvas-emission phase (Session 3).
2. **Blueprint P4** builds Canvas's side against fixture manifests (offline, venue-independent).
3. First live board = the **H4 carried chain's** refine run (spend-gated) — one run produces the
   variants, the manifest, the board, and the HR-second-consumer evidence in a single pass.
4. v1.0 cut requires: both sides shipped · one full live loop (generate → board → human verdict →
   Schema-A record) · §7.7 sign-off on any contract change this draft's review surfaces.

## §5 What this spec does NOT do

No `canvas_std` change — the v2.2.0 interaction layer already carries everything §1 needs (that
is the point: the leg-3 runtime was built for exactly this class of consumer). No ComfyUI code in
Canvas; no canvas code requirements on ComfyUI beyond a JSON manifest. No auto-selection — the
choice affordance *is* the SO-5 human gate, now with a substrate.
