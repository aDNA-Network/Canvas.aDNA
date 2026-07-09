---
type: artifact
artifact_type: gap_register
campaign_id: campaign_canvas_halftone
title: "Halftone gap register — the comic system, reviewed end-to-end"
created: 2026-07-09
updated: 2026-07-09
last_edited_by: agent_mondrian
status: active
tags: [artifact, review, comic, gap-register, halftone]
---

# Halftone Gap Register — comic system review (2026-07-07/09)

> Three-track read-only review: **code** (comic_generator + canvas_comic + canvas_core internals) ·
> **governance/specs** (campaign history, spec coverage, process) · **end-to-end workflow** (cross-vault seams,
> consumers, actual outputs). Verdict: **a well-built spec→canvas producer whose pipeline dead-ends at rendering.
> Zero comics have ever been rendered.** Gap IDs G1–G6 are the campaign's work register.

## What works (the keep list)

- **`what/production/comic_generator/`** (Atelier A2, 2026-06-21; **87 tests, 8 files**): YAML `ComicInput`
  (pages/panels/spreads/characters/color_script/story_state) → aDNA-Native `.canvas`. Data-driven (zero baked
  instance data — the legacy engine's hardcoded Science-Stanley constants became input), substrate-neutral content
  layer (AST-guarded: `tests/test_model_neutrality.py`), deterministic integer print geometry (ComixWellspring
  663×1025 trim, 2×3 grid — `layout.py`), 6-layer prompt assembly (`prompt.py`: style/character/scene/camera/
  lighting/negations) + Mermaid spatial dual-prompts (`panel_layout.py`) emitted into
  `_reserved.component_types[*].qualities.{image_prompt,dual_prompt}`; `qualities.status: prompt_only|rendered`;
  round-trip stable; degradation D-1/2/3 proven.
- **Reusable substrate already in-vault** (`what/production/canvas_core/`):
  - `image_generation.py` — **`ImageClient` protocol** (`generate_image(prompt, output_path, style, aspect_ratio,
    image_size, model) -> dict`) + `ImagePrompt` + `ImagenWiring` (variant fan-out, selection canvases, sidecar audits).
  - `comfyforge_adapter.py` — a **working ComfyUI HTTP client** (POST `/prompt` → poll `/history/{id}` → GET
    `/view`, health-check circuit breaker) conforming to `ImageClient`.
  - `print.py` — **PrintExporter** (~400 LOC; page compositing, RGB→CMYK, 300 DPI, ComixWellspring spec; tests green).
  - `rlhf/` — Schema-A `SelectionRecord` store, **13 live records**; III bridge.
- **Governance clean**: producer pattern proven 7×; AT-1/AT-2 errata (both surfaced BY the comic/diagram build)
  resolved in v2.0.2; LIP queue drained at v2.3.0; comic spec vocabulary (panel/page/spread/sequence/reading_order/
  adjacency/surface) fully covered by `spec_panel_link_semantics` + `spec_component_model`.

## The gaps

### G1 🔴 No prompt→image bridge (the pipeline dead-ends at Step 4 of 6)

Nothing extracts prompts from a `.canvas` and renders them. Evidence:
- `comic_generator` emits prompts only (`panels.py` — `qualities.image_prompt`, `status: "prompt_only"`); by design +
  AST guard it can never render.
- **ComfyUI.aDNA has no comic workflow**: `workflows/production/` + `workflows/lora/` are empty; `model_registry.yaml`
  `loras: []`; the GPU node (Anduril, 10.42.0.8) is recorded unreachable; the vault is mid re-genesis (M03 human-gated;
  M04 = LoRA resume blocked).
- The only render precedent is the archived demo (`Archive.aDNA/CanvasForge.aDNA/what/artifacts/mvp_comic/`
  `mvp_comic_demo.py`) calling **Google Imagen 4 directly** — not ComfyUI, not canvas-driven.
- `canvas_core/print.py` (compositing) has consequently **never run on real rendered images**.
- Net: **zero finished comics exist in any vault** — only `.canvas` structural artifacts + audit JSONs.
→ **Fix: H2–H4** (the `comic_render` bridge; hybrid Gemini-generate → ComfyUI-refine chain).

### G2 🟠 VisualDNA never composed into comics

- VisualDNA bundles exist (Stanley `v0.3.1`: text_prompt, 6 reference images, palette, invariants
  "purple turtleneck always", `lora_refs`; ZenZachary VDP-03 `v0.1.1`) — but `comic_generator`'s
  `character_registry` kwarg is a manual dict; nothing loads bundles automatically; LoRA trigger words never reach a prompt.
- Reality check: the Stanley `lora_refs` are **`status: PENDING_TRAINING`, `trained_at: null`** (trigger word
  reserved, weights unelected) — the "trained LoRA" belief is stale. ComfyUI registry confirms `loras: []`.
→ **Fix: H5** (`compose_input.py` — bundles → enriched ComicInput + manifest `characters[]`; reference-image
conditioning now, LoRA into the refine stage when trained).

### G3 🟠 No story→spec authoring path

- Hand-writing ≈80 lines YAML/page; a 32-page issue ≈ 2,500 lines of structured data.
- `ScienceStanley.aDNA`'s "GraphicNovelForge" wrapper is governance-only (voice gates, R11 human gates on pages
  2/21/30) — **no runnable code**; their Undiagnosed Day 2026 comic is stuck in mock mode; SS Prism (ratified
  charter) plans to consume the comic engine.
→ **Fix (descoped by operator to contract-only): H6** — publish `comic_authoring_contract.md` (schema + worked
example + doctrine pointers); the agentic skill is a later wave / SS-Prism consumer.

### G4 🟠 Print never proven end-to-end

- `PrintExporter` tests are green but no full pipeline run exists (blocked by G1).
- Geometry mismatch to reconcile: `print.py` carries legacy **662.5-unit page-local** constants; `comic_generator`
  emits **663×1025 integer canvas-absolute** coordinates (spread offsets included). Needs a compose shim + golden
  placement test (1px tolerance).
- Effective-DPI risk: 2K cloud output into a 2062×3150 px bleed page ≈ **195 DPI**, under the 200 warning threshold
  → upscale belongs in the refine chain (RealESRGAN is already registered on ComfyUI's side).
→ **Fix: H2 (shim) + H6 (full-issue E2E)**.

### G5 🟡 Producer validation gaps (small, cheap)

| Gap | Site | Failure mode |
|-----|------|--------------|
| `image_path` never checked to exist | `panels.py` / `model.py` | valid `.canvas` with broken file refs |
| `spread_number` refs unvalidated vs declared `spreads[]` | `model.py` (validates unique page numbers only) | implicit spreads mask author error |
| `layout_type: splash` allows N panels silently | `model.py` Page validation | confusing renders |
| `story_state` may reference unknown characters | `prompt.py` (silently ignored) | mood/pose silently dropped |
| RLHF hints dormant + untested | `panels.py` kwargs; no test populates them | code-complete, unproven |
| **Layer-6 negations baked inline** into `image_prompt` | `style.NEGATIVE_SUFFIX` | wrong shape for ComfyUI's separate negative CLIP encode; blocks photorealistic registers |
| full-page-span panel (span 3×2) untested | `layout.py` handles; no explicit test | silent regression risk |
| Mermaid parser duplicated vs `canvas_comic/mermaid_layout.py` | accepted per ADR-004 (port-don't-import) | undocumented — future fixes may fork |

→ **Fix: H1** (all of the above; the `prompt_layers` split is a **contract prerequisite** for the bridge manifest).

### G6 🟡 Governance tail

- The **6-layer prompt structure has no written contract** — opaque to any render-side consumer (ComfyUI/Vulcan
  can't build a workflow against prose that doesn't exist).
- **RLHF seam ownership undocumented** (= Lodestar R4.2): the store + III bridge exist (13 records; Schema A) but the
  leg-3 `interaction.responses` route (Armature runtime) has no documented relationship to it.
- **`canvas_comic` disposition ambiguous**: the legacy engine (99 tests, hardcoded SS constants, `ComicReport`
  scoring) is a frozen quarry whose tests still ride the production suite; no disposition record.
- **Archived CanvasForge ADRs never ported**: `adr_003` image-generation provider strategy ("Imagen = v1.0
  production substrate; ComfyForge = style-transfer engine") · `adr_005` dual-prompt protocol · `adr_008` prompt-
  construction contract · `adr_004/006/007` visual-QA/RLHF — all still only in `Archive.aDNA/CanvasForge.aDNA/`.
→ **Fix: H1 (ADR port + prompt contract) + H6 (RLHF seam doc + canvas_comic disposition)**.

## Cross-checks that came back CLEAN (no action)

- **Write-back safety**: `canvas_std` sync_hash is **topology-only** (`roundtrip.py:30` — sorted node ids +
  `fromNode->toNode` pairs); flipping a panel `text→file` + `status→rendered` revalidates with an unchanged hash.
  The bridge's new-file write-back is safe by construction (never add/remove nodes/edges; avoid `ANCHOR_REF_KEYS`
  as top-level qualities keys).
- **Spec coverage**: every structural comic concept the producer uses has Standard vocabulary; speech-bubbles/
  bleeds/character-bible remain producer-side metadata patterns **by design** (substrate-neutrality), not spec gaps.
- **Firewall**: the entire comic system lives in `what/production/`; no `canvas_std` change is needed anywhere in
  this campaign.
