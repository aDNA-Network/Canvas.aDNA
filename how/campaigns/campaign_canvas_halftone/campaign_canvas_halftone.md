---
campaign_id: campaign_canvas_halftone
type: campaign
title: "Operation Halftone — comic system: review → render bridge → end-to-end pipeline"
owner: stanley
status: active
estimated_sessions: "6-10"
phase_count: 7
mission_count: 2
priority: high
predecessor: campaign_canvas_beacon
created: 2026-07-09
updated: 2026-07-09
last_edited_by: agent_mondrian
status_history: "active (2026-07-09 — chartered from the operator-approved comic-system review; scope=full program T0–T4+G · backend=hybrid Gemini→ComfyUI-refine · T3=contract-only)"
tags: [campaign, canvas, halftone, comic, producer, render, bridge, comfyui, gemini, visualdna, print, governance]
---

# Campaign: Operation Halftone — comic system review → full improvement program

> Named for the printing technique that makes comics printable. The comprehensive comic-system review
> (2026-07-07/09, three-track: code · governance/specs · end-to-end workflow) found **a well-built spec→canvas
> producer whose pipeline dead-ends at rendering — zero comics have ever been rendered**. Halftone closes the
> pipeline. Review artifacts (source of truth for gap IDs): `missions/artifacts/halftone_{gap_register,roadmap}.md`.
> Approved plan: `~/.claude/plans/please-read-the-claude-md-snazzy-shore.md`.

## Goal

Take the comic system from "prompts sitting in canvas metadata" to **an end-to-end pipeline that ships actual
rendered, composited, print-ready comic pages** — while hardening the producer, wiring VisualDNA character
consistency, publishing the authoring contract, and closing the governance tail. The proof milestone: **the first
rendered comic page in the fleet's history** (H3).

## Decisions locked (operator, 2026-07-07)

| Decision | Choice |
|----------|--------|
| **Scope** | Full program — T0–T4 + governance rail, this one gated campaign. |
| **Backend** | **Hybrid, interoperating**: Gemini/Imagen **generates**; output **seeds ComfyUI img2img/refine** (style-unification · LoRA-when-trained · upscale). Honors inherited CanvasForge ADR-003 (Imagen = production substrate; ComfyForge = style-transfer engine). Cloud path primary today; ComfyUI rides a Vulcan coord memo, **never blocking**. |
| **T3 authoring** | Contract-only — Canvas ships the ComicInput authoring contract; the agentic story→spec skill is a later wave / SS-Prism consumer. |
| **Boundary** | **"Canvas dispatches, it does not diffuse."** No render engines in-vault (AST-guarded); pixels/models/workflows are Vulcan's. `what/code/canvas_std/` untouched the whole campaign (firewall git-diff 0). |

## Phases (human-gated; never auto-advance — SO-1)

| Phase | Tier | What | Gate |
|-------|------|------|------|
| **H0** | — | Charter + file the review artifacts (gap register · roadmap) + STATE reconcile. | rides H1's session |
| **H1** | T0+G1 | **Producer hardening** — `qualities.prompt_layers` (incl. separate `negative` channel; configurable suffix) · validation (image_path exists · spread refs · splash guard · story_state chars) · RLHF-hints tests · full-span test · Mermaid-dup note. **Governance 1** — port quarry ADRs (provider-strategy · dual-prompt · prompt-construction) + write `what/docs/comic_prompt_contract.md`. | SITREP + HOLD |
| **H2** | T1.1 | **Render bridge, offline** — new `what/production/comic_render/` (manifest v0.1 w/ `render_chain` · extract · backends/{fake} · dispatch · select · write-back-to-NEW-file · validate · compose shim · CLI · AST no-diffusion guard). Exit: fake-rendered mini-issue page composites; rendered canvas revalidates, sync_hash unchanged. | SITREP + HOLD |
| **H3** | T1.2 | **First REAL rendered page** — `backends/gemini.py` (credential via Home broker); **SPEND GATE** (model tier · variants · budget cap) → live render mini-issue splash → operator eye-gate → composited page JPG. | SPEND GATE + eye-gate |
| **H4** | T1.3 | **Vulcan seam + interop** — coord memo (comic-panel generate + `comic_panel_refine` img2img workflows; pending_ack, non-blocking) · contract fixtures + mocked tests · flag-gated live path · prove gemini→comfy refine chain once. | SITREP + HOLD |
| **H5** | T2 | **VisualDNA auto-compose** — `compose_input.py`: bundles → enriched ComicInput + manifest `characters[]` (trigger words · lora_refs · reference images); reference conditioning; LoRA into refine when trained. *(Parallel-eligible after H2.)* | SITREP + HOLD |
| **H6** | T3′+T4+G | **Authoring contract** (`comic_authoring_contract.md`) · **print E2E** (full mini-issue compose · geometry golden test · CMYK · DPI policy) · **governance close** (RLHF seam doc = Lodestar R4.2 · canvas_comic disposition) · campaign AAR + close. | SITREP + close gate |

## Firewall & discipline

- `what/code/canvas_std/` — **zero touches expected all campaign**; verify `git diff --stat -- what/code/canvas_std/` empty at every gate.
- After every producer/bridge change: full production suite (7 producers 223 + comic deltas) + `canvas_std` 115/10 unaffected.
- `comic_render` boundary: AST guard — HTTP dispatch clients OK; torch/diffusers/local pipelines NEVER; PIL only via `canvas_core.print`.
- Cross-vault: ComfyUI/VisualDNA/SS touches are coord memos or read-only consumption (Rule 10). Spend (H3) is operator-gated with a budget cap.
- Reuse, don't reinvent: `canvas_core/image_generation.py` (`ImageClient`/`ImagePrompt`/`ImagenWiring`) · `comfyforge_adapter.py` · `print.py` · `rlhf/` Schema-A.

## Missions

- → `missions/mission_h1_producer_hardening.md` (H0+H1 — created at charter; executing).
- H2–H6 missions are created when their phase opens (never pre-spawn past a HOLD).

## Next-session prompt

> Open `how/campaigns/campaign_canvas_halftone/` (this master + `CLAUDE.md`). Operation Halftone closes the comic
> pipeline (review → render bridge → E2E). Check `STATE.md` for the open phase; source of truth =
> `missions/artifacts/halftone_{gap_register,roadmap}.md` + the approved plan. Execute the open phase's mission.
> Re-run the production suite after any `what/production/` touch; `what/code/canvas_std/` stays untouched
> (firewall). **HOLD at every phase gate** (SO-1); per-mission AAR (SO-5); commits/pushes operator-gated (Git-Ops §3);
> H3 dispatch additionally spend-gated.

## Provenance

Chartered 2026-07-09 from the operator-approved comic-system review (plan approved 2026-07-09; decisions locked
2026-07-07: full program · hybrid backend · T3 contract-only). Predecessor campaign: `campaign_canvas_beacon`
(publish-hardening, completed 2026-07-02). Session: `…_135234_halftone_charter_h1`.
