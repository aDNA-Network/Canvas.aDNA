---
type: artifact
artifact_type: roadmap
campaign_id: campaign_canvas_halftone
title: "Halftone roadmap — render-bridge architecture + tier plan"
created: 2026-07-09
updated: 2026-08-03
last_edited_by: agent_mondrian
status: active
tags: [artifact, roadmap, comic, render-bridge, manifest, backends, halftone, visual_fidelity, rlhf_surface, federation]
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
| **HV** | G7 rail | 1 · visual-check CLI + geometry traps + calibration + doctrine adoption + reviewer registration + authoring guidance (§5) | — *(executed 2026-08-03 at plan approval)* |
| H2 | T1.1 | 1 · bridge offline (fake E2E → composited page; sync_hash-unchanged golden; **exit += `canvas-visual-check` + agent-confirmed render**) | H1, HV |
| H3 | T1.2 | 1 · gemini adapter + **first real rendered page** (SPEND gate + eye-gate; M-SB-D2 first-light convergence — dev-lane annex) | H2 |
| H4 | T1.3 | 1 · Vulcan seam (wrapper delivered 2026-08-03) + contract fixtures/mocked tests + gemini→comfy chain proven | H2 (ack non-blocking) |
| H5 | T2 | 1–2 · VisualDNA compose (bundles → ComicInput + manifest `characters[]`; **exit += LoRA-less compose exercised + tested**) | H2 (parallel-eligible) |
| **HR** | G9 | 1–2 · review-surface spec + Meta Bind pilot over real images + collector; dispatch contract-stub only (§6) | HV (parallel-eligible; not blocked by H2/H3) |
| **HF** | G8 | 1 · federation census + index + staged refederation memos (§7) — `executor_tier: sonnet` eligible | — (any order; deliveries per-send GO) |
| H6 | T3′ + T4 + G | 1–2 · authoring contract · full-issue print E2E (geometry shim golden · CMYK · DPI policy) · RLHF seam doc (anchored by HR + Bearly evidence) · canvas_comic disposition · dev-lane ratification record · close | H3, HR |

**Minimum path to the first rendered page: H1 → H2 → H3** (2–3 sessions; HV done).

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
6. **HR pilot subject timing** — rec.: pilot on existing ComfyUI SS variant images (read-only consumption; records
   stay Canvas-side) so HR needn't wait for H3; re-run the surface on the first H3 renders as the second consumer.
   *(gate: HR open)*
7. **HF delivery GOs** — each staged refederation memo is a separate per-send GO (Rule 10); operator may batch.
   Bundling the Vulcan courtesy-ack with the HF index memo is recommended. *(gate: HF close)*

## 5. HV — the visual-fidelity rail *(added 2026-08-03; executed at plan approval)*

**Thesis (Kennedy intake):** `canvas-std validate` is schema-only *by design*; nothing filled the visual gap, so
`[OK]` misled authors. HV fills it on the production shelf (firewall intact):

- **CLI** `what/production/canvas_core/traps/cli.py` — "`canvas-visual-check`", the sibling of `canvas-std
  validate`. Runnable `python -m canvas_core.traps.cli <file.canvas>…` (direct-path bootstrap for other vaults;
  console-script packaging = follow-up). Args: `--json` · `--strict` (findings ≥ medium also fail) · `--vault-root`
  (file-resolution traps). Human output carries **required-height fix hints** (tell how to fix, not just that you
  failed). Exit nonzero on high/critical.
- **New traps** (registry + per-trap test, existing convention): `CV-LEAD-COST-01` (`##`/`###` lead in text nodes —
  98.9/74.8px vs 40.0px for `**bold**`) · `CV-GROUP-LABEL-01` (label chars vs `width/25` CAPS · `width/22` mixed) ·
  `CV-EDGE-LABEL-01` (first edge-geometry trap; >20 chars fails; 83% of fleet edges already carry no label) ·
  `CV-FILE-PROPS-01` (file-node target resolves + Properties-table exposure unless `propertiesInDocument: hidden`).
- **Calibration**: `text_metrics.py` gains Obsidian-CSS-derived constants (from Kennedy's `canvas_fit_check.py`,
  validated against the observed failure: predicted 43%/44% shown vs operator-observed ~51%/"half"); the fit rule
  `chars ≤ (W−48)(0.90·H − P)/208`.
- **Doctrine adoption** (the never-taken step): `skill_canvas_producer_build.md` validate step += visual-check +
  **agent-confirmed Obsidian render**; `spec_federation_contract.md` dated amendment (stage gains the visual gate);
  `context_canvas_visual_in_the_loop.md` adoption step marked executed → **HOME-CV-3 dispositioned**.
- **Registration**: `canvas_reviewers.yaml` → 1.1.0; geometric traps join `trap_applicability.structural_now`.
- **Guidance**: `what/docs/canvas_authoring_guidance.md` — the five authoring rules with real numbers; documents the
  `html_renderer.py` file-node blindness as a known limitation (renderer fix deferred; the static trap covers it).

## 6. HR — the RLHF review surface *(added 2026-08-03; capture-side build, dispatch contract-only)*

**Thesis:** every layer exists (interaction runtime v1.0 · Schema-A + `iii_bridge` · Meta Bind fleet-wide · Bearly
dry-run precedent · III Finding G "agentic consensus ≠ operator preference") — HR assembles them into a working
operator surface. `enableJs: false` is preserved throughout.

```
image variants ──pilot builder──▶ review .canvas (image node + sidecar-note node per variant, linked)
sidecar note  ──Meta Bind INPUT / updateMetadata BUTTON──▶ frontmatter verdicts {verdict, rating, defect_tags[], note}
frontmatter   ──collector (canvas_core/rlhf/review_collect.py)──▶ interaction apply_response (append-only)
                                                                + Schema-A SelectionRecord + III learning-store JSONL
regenerate    ──── contract stub ONLY (the Callisto dispatch seam; await Bearly P5 evidence) ────
```

- **Spec** `what/specs/spec_canvas_review_surface.md` — the canonical Meta Bind ↔ affordance mapping:
  approve/reject → `choice` · rating → `choice` · defect tags (controlled vocab) → `choice` (multi) · free note →
  `annotation` · prompt edit → `input` · regenerate/pin/escalate → `action` (captured as intent flags; dispatch
  deferred). Bearly `spec_bearly_rlhf_canvas.md` §3 (nine controls) is the informative precedent; ISS remains the
  sibling surface for flat rich-context gates; surface-choice routing = the future OIP layer's call.
- **Pilot**: real images (ComfyUI SS variants now — read-only consumption; H3 renders when they land); verdicts
  land as Schema-A records beside the existing 13; III store via the existing bridge (ADR-005 signal shape).
- **Feeds H6**: the RLHF seam doc (Lodestar R4.2) anchors on this spec + Bearly's evidence; open decision #4
  (III store vs `interaction.responses`) resolves there — capture keeps Schema-A either way.

## 7. HF — federation hygiene *(added 2026-08-03; mechanical, `executor_tier: sonnet` eligible)*

- **Census**: filesystem scan of `*/how/federation/canvas*` (+ legacy `canvasforge`) — at amendment time: **~14
  wrappers target Canvas.aDNA** (pins drifting 1.0→2.3.0; Emacs clean at v2.3.0) · **~6 target legacy
  CanvasForge.aDNA** (ZenZachary ×3 · Astro · SiteForge · SuperLeague) · Oration has **none** (the G7 enabling
  condition).
- **Index**: `how/federation/federation_index.md` (Canvas-side; consumers + wrappers + pins + last-verified) —
  folds Vulcan's `comfyui/` wrapper (0.2.0 @ `a8a4356`) per his memo's follow-up #3.
- **Staged memos**: one per stale/missing wrapper (refederation ask: `source_vault → Canvas.aDNA`, pin to v2.3.0,
  5-stage gate pointer, `canvas-visual-check` in stage guidance; Oration additionally: adopt a wrapper). All
  `staged_pending_GO`; **deliveries are per-send operator GO** — Canvas never writes another vault.
