---
type: artifact
artifact_type: roadmap
campaign_id: campaign_canvas_halftone
title: "Halftone roadmap — render-bridge architecture + tier plan"
created: 2026-07-09
updated: 2026-07-09
last_edited_by: agent_mondrian
status: active
tags: [artifact, roadmap, comic, render-bridge, manifest, backends, halftone]
---

# Halftone Roadmap — the bridge architecture + tier plan

> Companion to `halftone_gap_register.md`. This is the build design the operator approved (2026-07-09); decisions
> locked 2026-07-07: **full program** · **hybrid backend (Gemini generates → seeds ComfyUI refine)** ·
> **T3 authoring = contract-only**. Boundary: **"Canvas dispatches, it does not diffuse."**

## 1. The render bridge — `what/production/comic_render/` (H2–H4)

A new sibling package on the production shelf (producer idiom: `pyproject.toml` · `src/` · `tests/` · `AGENTS.md` ·
`iii_quality_contract.md`). NOT inside `comic_generator` (its no-render-import AST guard is a ratified Atelier
invariant) and NOT `canvas_presentation` (deck-scoped by declaration). Imports `canvas_core` (substrate) +
`canvas_std` (validation); never imports `comic_generator` (file-shaped handoff via `.canvas`).

```
in.yaml ──comic-generator build──▶ issue.canvas                      (existing producer, untouched)
issue.canvas ──[1 plan]──▶ issue.render_manifest.json                (extract + validate; staleness-guarded)
manifest ──[2 dispatch: generate]──▶ runs/<comic_id>/<panel>_v{n}.png (backend: gemini | comfy | fake)
generate output ──[3 refine (optional)]──▶ refined/*.png             (comfy img2img seeded by generate; LoRA slot; upscale)
variants ──[4 select]──▶ chosen per panel + Schema-A SelectionRecord
manifest+images ──[5 write-back]──▶ issue.rendered.canvas            (NEW file; input immutable)
issue.rendered.canvas ──[6 validate]──▶ canvas_std validate_suite + bridge checks
issue.rendered.canvas ──[7 compose]──▶ page JPGs                     (PrintExporter shim; geometry remap)
```

CLI: `comic-render plan|dispatch|refine|select|write-back|validate|compose <canvas>` + `run --until <stage>`.
The manifest JSON sidecar is the resumable state; **every stage is idempotent** (dispatch skips panels with
existing variants; write-back skips `status: rendered`).

Modules: `manifest.py` · `extract.py` · `backends/{fake,gemini,comfy}.py` · `dispatch.py` · `select.py` ·
`writeback.py` · `compose.py` · `cli.py`.

### Render manifest v0.1

Header: `comic_id` · `source_canvas` · `source_sync_hash` (re-plan if the canvas changed) · `backend_policy
{default_chain, allow_fallback}` · `budget_cap`.

Per panel:

| Field | Source / semantics |
|-------|--------------------|
| `panel_id`, `page_number`, `reading_index` | node id · page group · `reading_order` chain |
| `status` | `qualities.status` (`prompt_only` \| `rendered` \| `skip`) |
| `prompt_text` | `qualities.image_prompt` (assembled 6-layer) |
| `prompt_layers` | `qualities.prompt_layers` (H1) — incl. the **separate `negative` channel** |
| `dual_prompt?`, `spatial_layout?`, `compositional_intent?` | qualities (dual-prompt is the text payload where present) |
| `aspect_ratio`, `target_px {w,h}` | qualities · panel geometry → print px (drives model tier + DPI policy) |
| `characters[] {name, trigger_word?, lora_ref?, reference_images[]?}` | H5 VisualDNA compose |
| `seed` | default `sha256(comic_id + panel_id)` → int (reproducible); overridable |
| `variant_count`, `output_dir`, `existing_image_path?` | policy |
| **`render_chain`** | ordered stages — e.g. `[{stage: generate, backend: gemini}, {stage: refine, backend: comfy, workflow: comic_panel_refine, seed_image: <generate output>, denoise: 0.4}]`. **The hybrid interop is a first-class chain, not a backend switch.** |

### Backends — the existing `ImageClient` protocol, never a new abstraction

- `canvas_core/image_generation.py` already ships `ImageClient` + `ImagePrompt` + `ImagenWiring` (variant fan-out +
  Schema-A-adjacent audit records) — the bridge reuses it wholesale.
- **`fake`** — deterministic solid-PNG stub; the default everywhere in tests (whole pipeline provable offline).
- **`gemini`** — first real pixels (H3; precedent `latlab.mcp.image.server.GeminiImageClient`; credential via the
  Home.aDNA broker). Honors ported ADR: Imagen = the v1.0 production substrate.
- **`comfy`** — wraps the existing `ComfyForgeTier1Adapter`. The **refine** stage needs an init-image input: extend
  via an optional `RefineClient` protocol (don't break `ImageClient`). Production form binds to Vulcan's
  `comic_panel_refine` workflow (img2img + positive/negative + denoise + LoRA slot + RealESRGAN upscale) — asked in
  the H4 coord memo; a flag-gated experimental path works against any reachable ComfyUI meanwhile.

### Write-back — new file, never mutate

`issue.rendered.canvas`; input immutable. Per rendered panel: node `type text→file` (**vault-relative** path) ·
`component_types[nid].degrades_to → "file"` · `qualities.status → "rendered"` · `qualities.render_provenance
{backend_chain, model, seed, prompt_hash, generated_at, selection_record}`. `_reserved.sync` stays byte-identical —
**safe by construction** (sync_hash is topology-only, `canvas_std/roundtrip.py:30`); never add/remove nodes/edges;
never use `ref/anchor/anchor_ref/cites/for` as top-level qualities keys (`ANCHOR_REF_KEYS` are anchor-checked).
**Stage-6 gate:** `validate_suite` aDNA-Native green + D-1/2/3 green + every `file` path exists + effective-DPI check.

### Boundary guard

AST test (mirror of `comic_generator`'s, inverted): `comic_render` MAY import HTTP dispatch clients; MUST NEVER
import torch/diffusers/local pipelines; PIL only via `canvas_core.print` compositing.

## 2. Tier → phase map

| Phase | Tier | Missions | Depends on |
|-------|------|----------|------------|
| H1 | T0 + G1 | 1–2 · producer hardening (`prompt_layers` = **manifest prerequisite**) + ADR port + prompt contract | — |
| H2 | T1.1 | 1 · bridge offline (fake E2E → composited page; sync_hash-unchanged golden) | H1 |
| H3 | T1.2 | 1 · gemini adapter + **first real rendered page** (SPEND gate + eye-gate) | H2 |
| H4 | T1.3 | 1 · Vulcan coord memo + contract fixtures/mocked tests + gemini→comfy chain proven | H2 (ack non-blocking) |
| H5 | T2 | 1–2 · VisualDNA compose (bundles → ComicInput + manifest `characters[]`) | H2 (parallel-eligible) |
| H6 | T3′ + T4 + G | 1–2 · authoring contract · full-issue print E2E (geometry shim golden · CMYK · DPI policy) · RLHF seam doc · canvas_comic disposition · close | H3 |

**Minimum path to the first rendered page: H1 → H2 → H3** (2–3 sessions).

## 3. Risk register (full)

| # | Risk | L/I | Mitigation |
|---|------|-----|------------|
| R1 | Bridge grows into a render engine (boundary violation) | M/H | AST no-diffusion guard; "dispatch, not diffuse" in the ported ADR + memo |
| R2 | ComfyUI dependency stalls everything | **H (verified)**/H | `ImageClient` seam; gemini generate is primary; nothing blocks on Vulcan's ack |
| R3 | Character likeness drift without LoRA | H/M | H5 text-subsets + reference conditioning; operator set the v0 bar = accept drift; LoRA re-enters via the refine chain when trained |
| R4 | Write-back corrupts round-trip/conformance | **L (verified)**/H | topology-only hash; new-file output; stage-6 revalidation gate |
| R5 | Print geometry mismatch (legacy 662.5 page-local vs 663×1025 canvas-absolute) | M/M | dedicated compose shim; golden placement test (1px tolerance) |
| R6 | Negative-prompt shape mismatch for ComfyUI (Layer 6 inline) | certain w/o fix / M | H1 `prompt_layers` split; contract names the negative channel |
| R7 | Effective-DPI on full-bleed (2K cloud ≈ 195 DPI < 200 threshold) | M/L-M | max-res requests for splash/bleed; upscale in the Vulcan refine ask; accept the warning on the v0 proof page |
| R8 | RLHF record fragmentation (Schema A vs B) | M/L | bridge emits Schema-A `SelectionRecord`s only |
| R9 | Cost blowout at 32-page scale (~150–200 panels × variants) | M/M | `budget_cap` in the manifest header; dispatch enforces; per-run spend report; H3 spend gate |
| R10 | Suite drag / network flake from live backends | L/L | `network`/`slow` markers (already in `what/production/pytest.ini`); `fake` is the default |

## 4. Operator decisions still open (surface at their gates)

1. **H3 spend parameters** — model tier · variants/panel (rec. 3) · budget cap · credential. *(gate: H3)*
2. **Vulcan memo delivery timing** + whether to bundle the LoRA-training-completion ask. *(gate: H4)*
3. **`canvas_comic` disposition** — rec.: reader-only freeze now, archive after H3; port `ComicReport` only if the
   scoring loop revives. *(gate: H6)*
4. **RLHF routing** (III store vs leg-3 `interaction.responses`) — the seam doc (H6) frames it; Schema-A capture
   keeps data either way. *(gate: H6)*
5. **`issue.rendered.canvas` authority** — rec.: derived artifact of the YAML source (producer stays authoritative;
   re-renders cheap). *(gate: H2 write-back design ack)*
