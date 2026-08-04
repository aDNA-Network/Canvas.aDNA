---
type: artifact
artifact_type: gap_register
campaign_id: campaign_canvas_halftone
title: "Halftone gap register — the comic system, reviewed end-to-end"
created: 2026-07-09
updated: 2026-08-03
last_edited_by: agent_mondrian
status: active
tags: [artifact, review, comic, gap-register, halftone, visual_fidelity, federation, rlhf]
---

# Halftone Gap Register — comic system review (2026-07-07/09)

> Three-track read-only review: **code** (comic_generator + canvas_comic + canvas_core internals) ·
> **governance/specs** (campaign history, spec coverage, process) · **end-to-end workflow** (cross-vault seams,
> consumers, actual outputs). Verdict: **a well-built spec→canvas producer whose pipeline dead-ends at rendering.
> Zero comics have ever been rendered.** Gap IDs G1–G6 are the campaign's work register; **G7–G9 added at the
> 2026-08-03 operator scope amendment** (Kennedy/Oration intake · federation census · RLHF-surface assembly).

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

### G7 🟠 Visual fidelity — `canvas-std [OK]` on an unreadable canvas *(added 2026-08-03)*

The schema validator is right to be schema-only (substrate-neutrality) — but **nothing fills the visual gap**, so
`[OK]` reads to an author as "this canvas is good." Evidence (Kennedy memo,
`who/coordination/coord_2026_08_03_kennedy_to_mondrian_canvas_visual_fidelity.md`):
- **The incident**: Oration's `canvas_oration_map.canvas` (53 nodes, built for a live Richard Greene review) passed
  `canvas-std 2.3.0 … [OK]` and rendered with **~20/23 text nodes clipped mid-sentence**, group labels ellipsised,
  edge labels as opaque boxes over other nodes, file cards ~80% YAML Properties table.
- **Root cause is Obsidian geometry, not schema**: canvas text nodes are `display:flex; flex-direction:column` —
  margins don't collapse; a `##` lead costs **98.9px** (### 74.8px · `**bold**` 40.0px) before any body text; a
  320×110 node had 11px left.
- **The machinery exists, unwired**: `what/production/canvas_core/traps/` — 9 implemented traps incl.
  `CV-TEXT-BOUNDS-01` — but `run_all_traps` has only internal call sites; **no CLI, no skill/doc mention, absent
  from `canvas_reviewers.yaml`**. An author following the documented path never encounters them.
- **The doctrine exists, un-adopted**: `what/context/context_canvas_visual_in_the_loop.md` ("no canvas ships
  without an agent-confirmed Obsidian screenshot") — its adoption step 1 was never executed; **HOME-CV-3 open
  since 2026-06-24**. Had it been wired, the canvas could not have shipped.
- **Four fleet-wide uncovered checks**: edge-label geometry (edges never geometrically evaluated) · group-label
  width truncation · file-node Properties-table preview (`html_renderer.py` ~1550–1576 is blind by construction) ·
  `text_metrics.py` calibration (hardcoded `font_size=16.0`, never Obsidian-derived).
- **Contributed fix**: Kennedy's `canvas_fit_check.py` (Obsidian-CSS-derived constants; reproduced the failure
  exactly — 22 TEXT-FIT + 8 GROUP-LABEL fails on the broken map, 65 passed/0 fails on the reworked one).
→ **Fix: HV** (CLI + new traps + calibration + doctrine adoption + reviewer registration + authoring guidance).

### G8 🟡 Federation drift — the contract is ratified, adoption is partial *(added 2026-08-03)*

- `spec_federation_contract.md` (RATIFIED 2026-06-12) mandates a `canvas/` wrapper + 5-stage gate (stage 3 =
  `canvas_std` conformance · stage 4 = III review) for every producer emitting aDNA canvases. Reality: **~14
  wrappers target Canvas.aDNA at drifting pins** (1.0 → 2.3.0; only Emacs is clean at v2.3.0), **~6 still target
  legacy CanvasForge.aDNA** (ZenZachary ×3 · Astro · SiteForge · SuperLeague), and the Keystone **E5.2 rollout
  tail never ran** (PT-P5-coupled from the start).
- **No federation index exists** — the wrapper set is discoverable only by filesystem scan; Vulcan's new
  `how/federation/comfyui/` wrapper (0.2.0 @ `a8a4356`, 2026-08-03) has nowhere to be indexed.
- **The G7 incident's enabling condition**: Oration has **no canvas wrapper at all** (`how/federation/` = git + iii
  only), so its canvas bypassed stages 3–5 entirely.
→ **Fix: HF** (census + Canvas-side index + staged per-vault refederation memos; deliveries per-send GO).

### G9 🟠 RLHF surface — every layer exists, nothing is assembled *(added 2026-08-03)*

No operator-facing capture surface exists, though all five layers are live:
- **Canvas grammar + runtime**: interaction v1.0 (`_reserved.interaction`; affordance kinds
  `input|choice|annotation|action`; the golden fixture already declares `approve`/`mark_reviewed`); append-only
  `apply_response`; advisory-reverse writes.
- **Store + bridge**: `canvas_core/rlhf/` Schema-A `SelectionRecord` (13 live records) + `iii_bridge.py`
  (III ADR-005 signal channel); comic RLHF hints threaded E2E at H1 (default-inert).
- **Render surface**: Meta Bind + Advanced Canvas fleet-wide (lean-9 Tier-1) — but **zero
  buttonTemplates/inputFieldTemplates configured**, `enableJs: false` (deliberate posture; capture must work
  without JS — INPUT fields / `updateMetadata` buttons writing sidecar frontmatter).
- **Precedent**: Bearly's dry-run (`Bearly.aDNA/what/specs/spec_bearly_rlhf_canvas.md` — nine controls mapped to
  affordance kinds; `loop_log.jsonl`; placeholder pixels; P5 real-pixel slice gated) + III's image-eval
  **Finding G** (4-persona agentic consensus mismatched operator preference — the argument FOR human buttons) +
  ComfyUI's standing order "variant selection is human-gated" with no interactive surface to do it on.
- **The seam**: button → dispatch → fresh generation → linked child node is unshipped on **both** standards
  (Callisto 2026-07-28 §2); Bearly P5 will send prototype evidence.
→ **Fix: HR** (capture-side spec + working pilot over real images; dispatch contract-only) **+ H6** (seam doc).

## Cross-checks that came back CLEAN (no action)

- **Write-back safety**: `canvas_std` sync_hash is **topology-only** (`roundtrip.py:30` — sorted node ids +
  `fromNode->toNode` pairs); flipping a panel `text→file` + `status→rendered` revalidates with an unchanged hash.
  The bridge's new-file write-back is safe by construction (never add/remove nodes/edges; avoid `ANCHOR_REF_KEYS`
  as top-level qualities keys).
- **Spec coverage**: every structural comic concept the producer uses has Standard vocabulary; speech-bubbles/
  bleeds/character-bible remain producer-side metadata patterns **by design** (substrate-neutrality), not spec gaps.
- **Firewall**: the entire comic system lives in `what/production/`; no `canvas_std` change is needed anywhere in
  this campaign.
