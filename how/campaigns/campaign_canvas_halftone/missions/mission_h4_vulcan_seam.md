---
type: mission
mission_id: mission_h4_vulcan_seam
campaign_id: campaign_canvas_halftone
phase: H4
status: completed                  # all six stated exit criteria met; the LIVE chain proof was scoped as deferred → H3
owner: stanley
persona: Mondrian
executor_tier: opus
token_budget_estimated: "1 session — 1 substrate extension + 1 new bridge module + chain-parser edit + ~17 tests + fixtures + 1 staged memo + records"
created: 2026-08-06
updated: 2026-08-06
last_edited_by: agent_mondrian
relates: ["halftone_roadmap.md §1 (backends · render_chain) + §2 H4 row + §4 open decision #2", "halftone_gap_register.md G1", "coord_2026_08_03_vulcan_to_mondrian_comfyui_wrapper_created.md", "how/federation/comfyui/CLAUDE.md"]
tags: [mission, halftone, h4, vulcan, comfyui, refine, img2img, render_chain, seam]
---

# Mission: H4 — the Vulcan seam (ComfyUI refine, offline/mocked)

## Intent

Make the operator-locked **hybrid backend** real on the Canvas side. The chain is already
first-class (`RenderStage`, `dispatch.run_refine`), and `RefineClient` was authored at H2 as an
additive protocol — but `make_refine_client("comfy")` still raises `NotImplementedError`. H4
implements the ComfyUI half: img2img refine over the existing `ComfyForgeTier1Adapter`, proven
against mocked HTTP with fixtures that double as the contract with Vulcan.

**Gate**: the 2026-08-06 plan approval (HV/H2/H5 precedent). **H3 is not a prerequisite** — the
refine seam needs no Gemini pixels; only "prove the gemini→comfy chain live once" joins H3.

**Boundary held**: "Canvas dispatches, it does not diffuse." The bridge's inverted AST guard
(`test_boundary.py`) forbids top-level `comfy*` imports and its comment pins the intent — *the H4
seam is an HTTP adapter living in `canvas_core`*. So img2img mechanics land in the substrate; the
bridge module is a thin manifest-shaped binding.

## Objectives

| # | Objective | Status |
|---|-----------|--------|
| **O1** | `canvas_core/comfyforge_adapter.py` — `_upload_image` (`POST /upload/image`) · `_build_img2img_workflow` (LoadImage → VAEEncode → KSampler with denoise<1.0 · **separate negative CLIPTextEncode**, never concatenated · optional LoraLoader slot · optional upscale) · `refine_image(...)` matching `RefineClient` exactly · `ComfyForgeConfig.workflow_dir` · `_resolve_refine_workflow` + `_patch_workflow_template` (named template, **degrades to built-in**) · `_refine_seed` (deterministic — refine is part of a reproducible run, unlike generate's wall-clock seed) | ✅ |
| **O2** | `comic_render/backends/comfy.py` (NEW) — `ComfyRefineClient`: manifest-shaped mapping only (negative · denoise · workflow name · `lora_ref`→bare LoRA filename · trigger-word injection · `model_name` · `cost_per_image = 0.0`); registry flip in `backends/__init__.py` | ✅ |
| **O3** | `comic_render/extract.py:parse_chain` — `<stage>:<backend>[@denoise][/workflow]`, backward compatible | ✅ |
| **O4** | Contract fixtures `comic_render/tests/fixtures/comfy/` (system_stats · upload · prompt · history · `comic_panel_refine.json` request shape + README) | ✅ |
| **O5** | `test_backends_comfy.py` (18) + `test_backends.py` gating split — protocol · workflow shape · upload→LoadImage · error paths · **the chain proof** + idempotency + LoRA threading | ✅ |
| **O6** | Live path — `@pytest.mark.network` smoke, `health_check`-gated; markers declared in `comic_render/pyproject.toml` (the shelf `pytest.ini` does not apply when running from the package dir) | ✅ |
| **O7** | Staged Vulcan memo (`comic_panel_refine` ask + endpoint question + open decision #2 recommendation) · wrapper follow-up **#1 closed** · **#2 recommendation** written | ✅ |
| **O8** | Records + verification — README/AGENTS, campaign master + CLAUDE.md, roadmap §1/§4, federation index, STATE, full suites, firewall diff 0, AAR | ✅ |

## Live verification against a real ComfyUI (2026-08-07 — item 0)

Run on **L1** (`~/ComfyUI` 0.24.1, MPS, `sd_xl_base_1.0.safetensors`) — no Anduril, no Gemini,
**zero spend**. It exposed **three** things the mocked suite could not, which is the whole argument
for having done it:

| # | Defect | Why mocks could never catch it |
|---|--------|-------------------------------|
| **L1** | `_poll_history` used `timeout_s` (a **30s HTTP-request** timeout) as the **generation** deadline. A 20-step SDXL img2img samples ~35s on MPS, so the adapter abandoned jobs the server went on to finish. Pre-existing since M-3-05; inherited, not introduced by H4. **Fix:** `generation_timeout_s` (600s) split from `timeout_s`. | mocked polls return instantly |
| **L2** | Identical graphs hit ComfyUI's **result cache** → `status: success`, every node `execution_cached`, and **empty outputs** → download found nothing. The deterministic refine seed made this the *common* case. **Fix:** `filename_prefix` derives from the output filename (also gives server-side traceability); the empty-outputs error now names the cache. | a mock has no result cache |
| **L3** | `DEFAULT_UPSCALE_MODEL` was a guessed `RealESRGAN_x2.pth`; the installed weight is `RealESRGAN_x4plus.pth`. | a mock accepts any model name |

**Four paths then verified green, and the images were *looked at*** (the HV agent-confirmed-render
doctrine — not just asserted):

| Path | Result |
|------|--------|
| Built-in img2img graph | 36s cold sample → a correct cel-shaded lighthouse on a basalt cliff |
| **Vulcan's REAL `workflow_img2img.json`**, patched by node class | 42s → `source=template:workflow_img2img`, a correct copper diving bell. **The patch convention holds against his actual file** — node 3 positive, 4 negative, 5 LoadImage, 7 KSampler |
| LoRA slot with a real weight (`lora_ss_ghibli_probe_v0-000004`) | 46s → loads and conditions cleanly. Rendered a *generic bearded scientist, not Stanley* — an independent corroboration of Vulcan's own **F-M04-B** ("identity locks to a WRONG attractor"). Wiring proven; likeness is his retrain |
| Upscale (`RealESRGAN_x4plus`) | 1024² → **4096²**. Materially over-solves roadmap **R7** (full-bleed 2K ≈ 195 DPI, under the 200 threshold) |

**Operational finding (documented in `comic_render/README.md`):** refining a **`fake`** panel looks
broken and isn't. The fake backend emits flat solid-colour PNGs; img2img at a production denoise
(~0.4) preserves seed structure, and a solid colour has none — so you get a flat field back. At
denoise ≥0.9 the identical call renders the prompt properly. In the real chain the seed is a
structured cloud panel where 0.4 is correct. Worth knowing before someone reads mush as a broken seam.

Regression after the fixes: canvas_core **819 → 824/3** (5 new regression tests pinning L1/L2/L3),
comic_render **92/1**, firewall diff **0**, ruff clean.

## Findings

1. **Endpoint policy belongs to the bridge, not the substrate** *(design refinement from the approved plan)*.
   The plan proposed flipping `ComfyForgeConfig.endpoint` to the wrapper's L1-local value. Two existing tests
   assert the documented Anduril-mesh default, and `canvas_core` is substrate shared with other consumers —
   so the default stayed, and `backends/comfy.py` resolves `COMIC_RENDER_COMFY_ENDPOINT` → else L1-local.
   Better separation: the substrate keeps its contract, the consumer owns its policy.
2. **`RefineClient` needed one additive parameter to carry the LoRA.** The protocol's call signature has no
   panel context, so H5's pair-gated `characters[]` entry could not reach the graph. Added `lora=None` to the
   protocol + both clients + `dispatch.run_refine` (`_lora_for`). The fake records it without honoring it,
   which is what makes the threading testable offline.
3. **The trigger word must be injected at dispatch.** Prompt contract §1a deliberately keeps `trigger_word`
   out of the assembled prompt text — it is dispatch-side conditioning. `apply_trigger_word` prepends it only
   when absent; the pair-gate guarantees it never emits an inert token for an untrained LoRA.
4. **`canvas-visual-check` on the rendered mini-issue is NOT clean — and was not clean before H4.** Source
   fixture: 24 findings; rendered: 18. Exactly **one** finding is new (`CV-NODE-DENSITY-01` on the splash
   page at `fill_ratio=1.00`) and it describes the intended geometry — a full-page splash fills its page.
   Seven findings disappear (text nodes → file nodes). **Recorded for H6:** the trap pack's padding/density
   heuristics are calibrated for knowledge canvases; comic pages legitimately pack flush. The rail should
   grow a comic-domain profile, or comic canvases should declare an exemption — not a defect either way, but
   it means "visual-check clean" is not currently a meaningful gate for comic output.
5. **Node ids are numeric strings.** Template patching sorts them numerically — lexical order puts `"10"`
   before `"6"` and would have swapped the positive and negative prompts. Regression-tested.

## Exit criteria

1. `refine:comfy` is a real backend: `make_refine_client("comfy")` returns a working client.
2. The **fake→comfy chain** runs green through `run_refine` against mocked HTTP, idempotently.
3. Boundary guard green — the new module trips no diffusion import.
4. Firewall `git diff --stat -- what/code/canvas_std/` empty.
5. No regressions: `canvas_core` 800/3 baseline · producers 259 · `canvas_std` 115/10 · cert 11/11.
6. The Vulcan ask is **staged**, not sent (Rule 10; per-send GO at the gate).

## Deferred (recorded, not dropped)

- **Live gemini→comfy chain proof** → joins H3 (Luke's cloud lane).
- **Live ComfyUI run** → the `network`-marked smoke, run the day a node is reachable.
- **Open decision #2** (bundle the LoRA-training-completion ask with the memo?) → operator's, at the gate.
- **LoRA-dispatch-runner rehoming** → recommendation written here; the call is the operator's.

## Verification (2026-08-06)

| Suite | Result |
|-------|--------|
| `comic_render` | **92 passed / 1 skipped** (73 → 92; the skip is the `network` live smoke) |
| `canvas_core` | **819 passed / 3 skipped** (800 → 819) |
| Cross-producer sweep | **259** — unchanged (brief 10 · deck 16 · document 37 · diagram 36 · comic 123 · letter 17 · post 20) |
| `canvas_std` | **115 / 10 skipped** — untouched |
| Certification | **11/11 fixtures agree** |
| **Firewall** | `git diff --stat -- what/code/canvas_std/` → **0 lines** |
| Boundary guard | green (`test_boundary.py` — the new module reaches ComfyUI only via `canvas_core`) |
| `ruff` | `comic_render` clean; `canvas_core` no new findings vs the HEAD baseline (one baseline `F401` resolved; the one added `BLE001` mirrors `generate_image`'s deliberate error-to-result contract) |

**E2E offline proof** (`--chain "generate:fake,refine:comfy@0.4/comic_panel_refine"`, mocked HTTP):
9 panels → 18 fake variants → **18 comfy refines** → 9 Schema-A selections → `mini_issue.rendered.canvas`
validating `adna_native` + D-1/2/3 + 9 files + DPI → **4 composited pages**, `sync_hash c56c73c08428f621`
byte-identical to source. The named workflow travelled from the chain spec to the submitted graph.

## AAR

- **Worked** — H2's groundwork paid off exactly as designed: `RefineClient` was already an additive protocol
  and `run_refine` already chained idempotently, so H4 was a *fill-in*, not a redesign. Building the mocked
  HTTP contract from committed fixtures (rather than ad-hoc MagicMocks) means the fixtures double as the
  artifact Vulcan is asked to satisfy.
- **Didn't** — the plan's endpoint-default flip was wrong (would have broken two honest substrate tests for
  a policy that belongs to the consumer); corrected in flight, recorded as finding #1.
- **Finding** — `canvas-visual-check` is not a meaningful gate for comic output today (finding #4): the trap
  pack's knowledge-canvas heuristics fire on legitimately flush-packed comic pages. H6 should decide between
  a comic-domain profile and a declared exemption.
- **Change** — `AGENTS.md` rule 7 codifies the placement precedent: protocol mechanics live in `canvas_core`,
  `backends/*.py` stays a thin mapping. That is what keeps the no-diffusion import list strict.
- **Follow-up** — the live gemini→comfy chain proof joins **H3** (Luke's lane); the Vulcan memo awaits a
  per-send GO; wrapper follow-up #2 awaits the operator/Vulcan call.
