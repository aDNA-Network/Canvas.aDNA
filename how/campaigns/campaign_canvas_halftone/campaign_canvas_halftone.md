---
campaign_id: campaign_canvas_halftone
type: campaign
title: "Operation Halftone — comic system: review → render bridge → end-to-end pipeline"
owner: stanley
status: active
estimated_sessions: "8-13"
phase_count: 10
mission_count: 3
priority: high
predecessor: campaign_canvas_beacon
created: 2026-07-09
updated: 2026-08-03
last_edited_by: agent_mondrian
status_history: "active (2026-07-09 — chartered from the operator-approved comic-system review; scope=full program T0–T4+G · backend=hybrid Gemini→ComfyUI-refine · T3=contract-only); amended (2026-08-03 — operator scope amendment: +HV visual-fidelity rail · +HR RLHF review surface · +HF federation index/memos; HV executed at plan approval)"
tags: [campaign, canvas, halftone, comic, producer, render, bridge, comfyui, gemini, visualdna, print, governance, visual_fidelity, rlhf_surface, metabind, federation]
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

**Amended 2026-08-03:** the campaign additionally carries the canvas **quality rails** — visual fidelity (**HV**:
the Kennedy/Oration `canvas-std-[OK]-but-unreadable` intake), the operator **RLHF review surface** (**HR**: Meta
Bind controls on canvas → interaction runtime → Schema-A/III), and **federation hygiene** (**HF**: census + index +
staged refederation memos) — so what the pipeline ships is inspectable, reviewable, and consumable fleet-wide.

## Decisions locked (operator, 2026-07-07)

| Decision | Choice |
|----------|--------|
| **Scope** | Full program — T0–T4 + governance rail, this one gated campaign. |
| **Backend** | **Hybrid, interoperating**: Gemini/Imagen **generates**; output **seeds ComfyUI img2img/refine** (style-unification · LoRA-when-trained · upscale). Honors inherited CanvasForge ADR-003 (Imagen = production substrate; ComfyForge = style-transfer engine). Cloud path primary today; ComfyUI rides a Vulcan coord memo, **never blocking**. |
| **T3 authoring** | Contract-only — Canvas ships the ComicInput authoring contract; the agentic story→spec skill is a later wave / SS-Prism consumer. |
| **Boundary** | **"Canvas dispatches, it does not diffuse."** No render engines in-vault (AST-guarded); pixels/models/workflows are Vulcan's. `what/code/canvas_std/` untouched the whole campaign (firewall git-diff 0). |

## Scope amendment locked (operator, 2026-08-03)

| Decision | Choice |
|----------|--------|
| **Structure** | Fold into Halftone (no sibling campaign): **+HV** visual-fidelity rail · **+HR** RLHF review surface · **+HF** federation index/memos. Gap register extends G7–G9. |
| **HV** | Executes at plan approval (2026-08-03 plan = the HV gate): `canvas-visual-check` CLI over the existing `canvas_core/traps/` + Kennedy's `canvas_fit_check.py` calibration (absorbed with credit) · new geometry traps (lead-cost · group-label · edge-label · file-props) · agent-confirmed-render doctrine adoption (closes HOME-CV-3) · reviewer registration (`canvas_reviewers.yaml` 1.1.0) · `what/docs/canvas_authoring_guidance.md`. Firewall holds — everything lives on the production shelf. |
| **HR** | **Pattern + working pilot**: canonical spec (Meta Bind controls ↔ interaction-runtime affordances; capture-side = frontmatter verdicts → collector → Schema-A `SelectionRecord` + III store; `enableJs: false` preserved) + a working review canvas over **real images** (ComfyUI SS variants now; H3 renders when they land). **Dispatch-side stays contract-only** (named seam per Callisto 2026-07-28) pending Bearly P5 evidence. |
| **HF** | Federation census + Canvas-side index (folds Vulcan's `comfyui/` wrapper, 0.2.0 @ `a8a4356`) + **staged** per-vault refederation memos for the ~6 stale CanvasForge-targeting wrappers; every delivery is a per-send operator GO (Rule 10). |

## Phases (human-gated; never auto-advance — SO-1)

| Phase | Tier | What | Gate |
|-------|------|------|------|
| **H0** | — | Charter + file the review artifacts (gap register · roadmap) + STATE reconcile. | rides H1's session |
| **H1** | T0+G1 | **Producer hardening** — `qualities.prompt_layers` (incl. separate `negative` channel; configurable suffix) · validation (image_path exists · spread refs · splash guard · story_state chars) · RLHF-hints tests · full-span test · Mermaid-dup note. **Governance 1** — port quarry ADRs (provider-strategy · dual-prompt · prompt-construction) + write `what/docs/comic_prompt_contract.md`. | SITREP + HOLD |
| **HV** | G7 rail | **Visual-fidelity rail** *(added 2026-08-03; executed at plan approval)* — `canvas-visual-check` CLI (`canvas_core/traps/cli.py`) over the trap pack · new geometry traps (CV-LEAD-COST-01 · CV-GROUP-LABEL-01 · CV-EDGE-LABEL-01 · CV-FILE-PROPS-01) · `text_metrics.py` Obsidian-CSS calibration (Kennedy's `canvas_fit_check.py` absorbed) · **agent-confirmed-render doctrine adopted** (producer skill + federation contract; closes HOME-CV-3) · `canvas_reviewers.yaml` 1.1.0 · `what/docs/canvas_authoring_guidance.md`. Firewall holds (production shelf only). | plan approval 2026-08-03 = gate; SITREP at close |
| **H2** | T1.1 | **Render bridge, offline** — new `what/production/comic_render/` (manifest v0.1 w/ `render_chain` · extract · backends/{fake} · dispatch · select · write-back-to-NEW-file · validate · compose shim · CLI · AST no-diffusion guard). Exit: fake-rendered mini-issue page composites; rendered canvas revalidates, sync_hash unchanged. **Exit amended (2026-08-03):** composited outputs additionally pass `canvas-visual-check` + an agent-confirmed Obsidian render (HV rail). | SITREP + HOLD |
| **H3** | T1.2 | **First REAL rendered page** — `backends/gemini.py` (credential via Home broker); **SPEND GATE** (model tier · variants · budget cap) → live render mini-issue splash → operator eye-gate → composited page JPG. *(2026-08-03: first-light convergence — aDNALabs M-SB-D2 may supply the page spec via Luke's cloud lane; see `missions/artifacts/halftone_dev_lanes.md`.)* | SPEND GATE + eye-gate |
| **H4** | T1.3 | **Vulcan seam + interop** — contract fixtures + mocked tests · flag-gated live path · prove gemini→comfy refine chain once. **Amended (2026-08-03):** Vulcan's consumer wrapper is already delivered (`how/federation/comfyui/`, 0.2.0 @ `a8a4356`, 2026-08-03) — fold its follow-ups: adjust `skills_used`/`workflows_used` at the first render session · decide the archived LoRA-dispatch-runner rehoming · index the wrapper (HF). | SITREP + HOLD |
| **H5** | T2 | **VisualDNA auto-compose** — `compose_input.py`: bundles → enriched ComicInput + manifest `characters[]` (trigger words · lora_refs · reference images); reference conditioning; LoRA into refine when trained. *(Parallel-eligible after H2.)* **Exit amended (2026-08-03):** **LoRA-less compose (reference-images-only) exercised + tested** — Bearly's *required* path (rights-HELD LoRA; Callisto 2026-07-28 §1, currently untested); notify Bearly at close. | SITREP + HOLD |
| **HR** | G9 | **RLHF review surface** *(added 2026-08-03; parallel-eligible after HV)* — `what/specs/spec_canvas_review_surface.md`: Meta Bind controls ↔ interaction-runtime affordance kinds (`input\|choice\|annotation\|action`; Bearly §3 nine-control mapping as informative precedent); capture-side architecture = frontmatter verdicts on sidecar notes (`enableJs: false` preserved) → agent collector → Schema-A `SelectionRecord` (`canvas_core/rlhf/`) + III store (`iii_bridge.py`) · **working pilot** review canvas over real images (ComfyUI SS variants now; H3 renders when they land) · **dispatch-side = named contract stub only** (the Callisto seam) pending Bearly P5 evidence · feeds H6's RLHF seam doc. | SITREP + HOLD |
| **HF** | G8 | **Federation hygiene** *(added 2026-08-03; sonnet-eligible, any order)* — fleet canvas-wrapper census · Canvas-side federation index (folds `comfyui/` + the ~14 live canvas wrappers) · **staged** refederation memos for the ~6 CanvasForge-targeting wrappers + version-drift notes; **every delivery = per-send operator GO** (Rule 10). | SITREP + HOLD; deliveries per-send GO |
| **H6** | T3′+T4+G | **Authoring contract** (`comic_authoring_contract.md`) · **print E2E** (full mini-issue compose · geometry golden test · CMYK · DPI policy) · **governance close** (RLHF seam doc = Lodestar R4.2, **anchored by HR's spec + Bearly P5 evidence** · canvas_comic disposition · dev-lane ratification record) · campaign AAR + close. | SITREP + close gate |

## Firewall & discipline

- `what/code/canvas_std/` — **zero touches expected all campaign**; verify `git diff --stat -- what/code/canvas_std/` empty at every gate.
- After every producer/bridge change: full production suite (7 producers 223 + comic deltas) + `canvas_std` 115/10 unaffected.
- `comic_render` boundary: AST guard — HTTP dispatch clients OK; torch/diffusers/local pipelines NEVER; PIL only via `canvas_core.print`.
- Cross-vault: ComfyUI/VisualDNA/SS touches are coord memos or read-only consumption (Rule 10). Spend (H3) is operator-gated with a budget cap.
- Reuse, don't reinvent: `canvas_core/image_generation.py` (`ImageClient`/`ImagePrompt`/`ImagenWiring`) · `comfyforge_adapter.py` · `print.py` · `rlhf/` Schema-A.

## Missions

- → `missions/mission_h1_producer_hardening.md` (H0+H1 — completed 2026-07-09).
- → `missions/mission_hv_visual_fidelity.md` (HV — created + executed at the 2026-08-03 scope amendment).
- H2–H6 + HR/HF missions are created when their phase opens (never pre-spawn past a HOLD).
- Dev-lane annex (second developer, Luke — Berthier S105): `missions/artifacts/halftone_dev_lanes.md` (draft;
  operator ratification rides the reply-memo GO).

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
