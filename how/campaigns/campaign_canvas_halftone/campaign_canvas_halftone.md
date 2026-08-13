---
campaign_id: campaign_canvas_halftone
type: campaign
title: "Operation Halftone — comic system: review → render bridge → end-to-end pipeline"
owner: stanley
status: active
estimated_sessions: "8-13"
phase_count: 10
mission_count: 6
priority: high
# Charter-altitude default for missions that type no executor_tier of their own (ADR-025 §2 chain;
# Berthier/Operation Hearth hm_m8 memo 2026-08-06, applied on operator ruling 2026-08-07). Chosen
# from THIS campaign's own slate — 4 fable / 1 opus / 1 sonnet — and it fits what remains: H3 is
# spend-gated and outward-facing, H6 is governance close. fable stays summon-only (§3), so an
# untyped card composes a brief instead of auto-spawning — correct in front of a spend gate.
executor_tier_default: fable
predecessor: campaign_canvas_beacon
created: 2026-07-09
updated: 2026-08-06
last_edited_by: agent_mondrian
status_history: "active (2026-07-09 — chartered from the operator-approved comic-system review; scope=full program T0–T4+G · backend=hybrid Gemini→ComfyUI-refine · T3=contract-only); amended (2026-08-03 — operator scope amendment: +HV visual-fidelity rail · +HR RLHF review surface · +HF federation index/memos; HV executed at plan approval); h5_hr_hf_opened (2026-08-04 — plan approval = their gates; H3 held for Luke's cloud lane, spend params pre-ruled); h4_opened (2026-08-06 — plan approval = the gate; offline/mocked half executed, the LIVE gemini→comfy chain proof deferred to H3); h3_opened (2026-08-09 — plan approval = the gate + the spend gate + the dev-lane §3a reassignment to Mondrian; three §7.7 ratifications signed; build complete); h3_rendered (2026-08-10 — the 'blocked on billing' call was a MISDIAGNOSIS [wrong credential read while a funded Vertex lane sat unused]; Operation Rosetta Stone corrected it and H3 RENDERED: 27 images, $3.618, 4 pages, 0 warnings. Eye-gate presented, unruled; campaign close still held on it)"
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
| **H3** | T1.2 | **First REAL rendered page** — `backends/gemini.py` (credential via Home broker); **SPEND GATE** (model tier · variants · budget cap) → live render mini-issue splash → operator eye-gate → composited page JPG. *(2026-08-03: first-light convergence — aDNALabs M-SB-D2 may supply the page spec via Luke's cloud lane; see `missions/artifacts/halftone_dev_lanes.md`.)* *(2026-08-04: spend params **PRE-RULED** at the H5/HR/HF gate surfacing — **Gemini pro-image class** [exact ID + live pricing verified before dispatch] · **3 variants/panel** · **$5 cap** · **`GEMINI_API_KEY`** via the Home broker · **aspect = geometry-derived** [mission_h2 finding #1 ruling: extract snaps each panel's true w/h to the nearest backend-supported ratio; manifest records declared + effective; implement at H3 open]. The **gate call itself remains open** — phase held for Luke's cloud lane.)* *(**OPENED + PARTIALLY EXECUTED 2026-08-09** — `mission_h3_first_light`, `status: partial`. Plan approval opened the phase, opened the **spend gate** for the same session, and reassigned H3 **in full to Mondrian** (dev-lane annex **§3a + Amendment 1** — amended in the open, not overwritten; no `luke/*` branch had ever been created). **Built**: geometry-derived aspect (`aspect.py` + `extract.py` + additive manifest fields `effective_aspect_ratio`/`aspect_snap_error`, declared never overwritten) · **`backends/gemini.py`** + registry flip + `cloud` extra + live-capture fixtures. **Reported BLOCKED at the live run** (`429 RESOURCE_EXHAUSTED`) — ⚠️ **that was a MISDIAGNOSIS**: the backend read `GEMINI_API_KEY` (**C05**, documented credit-empty and out of the render chain) while the **funded Vertex SA C63** sat working on the same node; retrying three models re-tested one dead lane, not three. **RENDERED 2026-08-10** after Operation Rosetta Stone corrected credential resolution: **27 images · $3.618 · 4 pages × 2062×3150 · 0 warnings** · `sync_hash c56c73c08428f621` byte-identical. Mid-run, a second `RESOURCE_EXHAUSTED` proved to be a **rate limit** (5 images, then recovery on retry) — backoff went into the shared layer. **Eye-gate presented, not yet ruled; H4's remainder still open (the run was generate-only).** **Verified spend ready for the gate**: `gemini-3-pro-image` @ **$0.134/image 2K** × 27 = **$3.62** inside the $5 cap. **F-H3-1 (fleet-relevant)**: the whole `imagen-4.0-*` family is **deprecated, shutdown 2026-08-17** — and `adna_lab`'s `GeminiImageClient`, the fleet's reference, targets exactly it; this backend uses `generate_content` + `response_modalities=['Image']` instead. **F-H3-2**: the real aspect menu is **14 entries, not 5**, obtained free from the service's own 400 — the splash snaps to **2:3 (residual 0.030)** rather than 9:16 (0.140). comic_render 94→**154/2** · canvas_core 841→**863/3** · firewall diff 0.)* | SPEND GATE + eye-gate |
| **H4** | T1.3 | **Vulcan seam + interop** — contract fixtures + mocked tests · flag-gated live path · prove gemini→comfy refine chain once. **Amended (2026-08-03):** Vulcan's consumer wrapper is already delivered (`how/federation/comfyui/`, 0.2.0 @ `a8a4356`, 2026-08-03) — fold its follow-ups: adjust `skills_used`/`workflows_used` at the first render session · decide the archived LoRA-dispatch-runner rehoming · index the wrapper (HF). *(**EXECUTED offline 2026-08-06** — `mission_h4_vulcan_seam`, opened at that day's plan approval: `refine:comfy` is a real backend — img2img in `canvas_core/comfyforge_adapter.py` (`refine_image` · `/upload/image` · separate-negative graph · LoRA slot · optional upscale · deterministic seed · named-template patching that **degrades to the built-in graph**), thin binding `comic_render/backends/comfy.py`, chain syntax `<stage>:<backend>[@denoise][/workflow]`, `RefineClient` extended with the pair-gated `lora` (dispatch lifts it from `characters[]`). **Chain proven offline E2E** on the mini-issue: 9 panels → 18 fake variants → 18 mocked-comfy refines → 9 selections → rendered canvas revalidates (`c56c73c08428f621` unchanged) → 4 composited pages. comic_render 73→**92/1skip** · canvas_core 800→**819/3** · fixtures `tests/fixtures/comfy/` = the contract with Vulcan · live smoke `-m network`. Follow-up **#1 closed** (wrapper `skills_used`/`workflows_used` → actual consumption); **#2 recommendation = leave the LoRA runner archived** (operator/Vulcan call). **Remaining at H4: the gemini→comfy chain proven LIVE — joins H3** (Luke's lane).)* | SITREP + HOLD |
| **H5** | T2 | **VisualDNA auto-compose** — `compose_input.py`: bundles → enriched ComicInput + manifest `characters[]` (trigger words · lora_refs · reference images); reference conditioning; LoRA into refine when trained. *(Parallel-eligible after H2.)* **Exit amended (2026-08-03):** **LoRA-less compose (reference-images-only) exercised + tested** — Bearly's *required* path (rights-HELD LoRA; Callisto 2026-07-28 §1, currently untested); notify Bearly at close. *(**EXECUTED 2026-08-04** — `mission_h5_visualdna_compose`: exit criterion proven by the named test against both live bundle shapes + live smokes; compose lives in `comic_generator` [AST-guard-driven placement]; Callisto notify STAGED pending GO.)* | SITREP + HOLD |
| **HR** | G9 | **RLHF review surface** *(added 2026-08-03; parallel-eligible after HV)* — `what/specs/spec_canvas_review_surface.md`: Meta Bind controls ↔ interaction-runtime affordance kinds (`input\|choice\|annotation\|action`; Bearly §3 nine-control mapping as informative precedent); capture-side architecture = frontmatter verdicts on sidecar notes (`enableJs: false` preserved) → agent collector → Schema-A `SelectionRecord` (`canvas_core/rlhf/`) + III store (`iii_bridge.py`) · **working pilot** review canvas over real images (ComfyUI SS variants now; H3 renders when they land) · **dispatch-side = named contract stub only** (the Callisto seam) pending Bearly P5 evidence · feeds H6's RLHF seam doc. *(**BUILT 2026-08-04** — `mission_hr_review_surface`: spec draft + pilot [premise corrected: the variant images are in-vault at `style_registry/ss_character/`, not in ComfyUI.aDNA] + collector. **Gate 2/3 closed**: spec **RATIFIED** [GO wave, §7.7] · render **agent-confirmed** [session `_174045` — the gate item caught + fixed two live failures: vault-in-restricted-mode {the interactive layer had never rendered on this node} and multiSelect-inline → `[META_BIND_ERROR]` {block-only in Meta Bind; builder fixed, pilot rebuilt, 800/3}; all 8 controls live incl. inside canvas embeds; buttons-vs-toggles resolved — both idioms render, ratified table stands]; **remaining: the operator's review pass**.)* | SITREP + HOLD |
| **HF** | G8 | **Federation hygiene** *(added 2026-08-03; sonnet-eligible, any order)* — fleet canvas-wrapper census · Canvas-side federation index (folds `comfyui/` + the ~14 live canvas wrappers) · **staged** refederation memos for the ~6 CanvasForge-targeting wrappers + version-drift notes; **every delivery = per-send operator GO** (Rule 10). *(**EXECUTED 2026-08-04** — `mission_hf_federation_hygiene`: census artifact + `federation_index.md` [Vulcan #3 satisfied] + 5 staged memos incl. the Oration adopt-a-wrapper ask; mechanism correction recorded — drift is identity/pin/prose/paths, `source_vault` already clean fleet-wide.)* | SITREP + HOLD; deliveries per-send GO |
| **H6** | T3′+T4+G | **Authoring contract** (`comic_authoring_contract.md`) · **print E2E** (full mini-issue compose · geometry golden test · CMYK · DPI policy) · **governance close** (RLHF seam doc = Lodestar R4.2, **anchored by HR's spec + Bearly P5 evidence** · canvas_comic disposition · dev-lane ratification record) · campaign AAR + close. *(**OFFLINE HALF EXECUTED 2026-08-09** — `mission_h6_close`, `status: partial`, opened at that day's plan approval. The trigger: three unconsumed Callisto memos in `who/coordination/`, one of which **discharged the Bearly P5 evidence dependency** the RLHF work was parked behind. Delivered: `spec_rlhf_seam.md` [Canvas owns the capture substrate / III owns the signal schema; store heterogeneity ruled; ISS-vs-III resolved as a scope conflation; **open decision #4 RULED** — reject → III as `rlhf_signal_type: reject` derived from `responses[]`, Schema-A stays approval-only; implementation S-1..S-4 deliberately unbuilt while `proposed`] · **`review_dispatch_contract v0` BOUND** [six clauses; **D5** refusal-atomicity from Callisto's `F-S030-1`, credited; **D6** venue boundary from ADR-007 mode L; still contract-only, dispatcher deliberately NOT built — the mode-L venue has not run a batch] · **`--profile knowledge-canvas\|comic\|all`** [H4 finding #4: all 24 findings came from three aesthetic traps, none a defect; comic 24→0 source, 21→3 rendered, and all 3 survivors are `CV-IMAGE-ASPECT-RATIO-01`] · **print E2E** [`export_spread` was written, correct and **unreachable** — every spread would have squashed 2:1 silently; CMYK's silent soft-convert made output **machine-dependent** — both fixed, DPI policy written down] · `comic_authoring_contract.md` [T3′ contract-only; every command run before documenting — the first draft had the build flags wrong] · **`adr_009`** canvas_comic = reader-only freeze now / archive after H3. Suites: canvas_core 824→**841/3** · comic_render 92→**94/1** [H6-deferred test **inverted**] · producers **259** · canvas_std **115/10** · cert **11/11** · **firewall diff 0**. **Campaign close NOT taken — H3 has never run.**)* | SITREP + close gate |

## Firewall & discipline

- `what/code/canvas_std/` — **zero touches expected all campaign**; verify `git diff --stat -- what/code/canvas_std/` empty at every gate.
- After every producer/bridge change: full production suite (7 producers 223 + comic deltas) + `canvas_std` 115/10 unaffected.
- `comic_render` boundary: AST guard — HTTP dispatch clients OK; torch/diffusers/local pipelines NEVER; PIL only via `canvas_core.print`.
- Cross-vault: ComfyUI/VisualDNA/SS touches are coord memos or read-only consumption (Rule 10). Spend (H3) is operator-gated with a budget cap.
- Reuse, don't reinvent: `canvas_core/image_generation.py` (`ImageClient`/`ImagePrompt`/`ImagenWiring`) · `comfyforge_adapter.py` · `print.py` · `rlhf/` Schema-A.

## Missions

- → `missions/mission_h1_producer_hardening.md` (H0+H1 — completed 2026-07-09).
- → `missions/mission_hv_visual_fidelity.md` (HV — created + executed at the 2026-08-03 scope amendment).
- → `missions/mission_h2_render_bridge.md` (H2 — completed 2026-08-03; gate = the H2 plan approval,
  which also ruled open decision #5 = **derived artifact** and ratified the dev-lane annex).
- → `missions/mission_h5_visualdna_compose.md` (H5 — opened 2026-08-04; gate = plan approval).
- → `missions/mission_hr_review_surface.md` (HR — opened 2026-08-04; gate = plan approval).
- → `missions/mission_hf_federation_hygiene.md` (HF — opened 2026-08-04; gate = plan approval).
- → `missions/mission_h4_vulcan_seam.md` (H4 — opened 2026-08-06; gate = plan approval; offline/mocked half
  executed, the live chain proof joins H3).
- → `missions/mission_h6_close.md` (H6 — opened 2026-08-09; gate = plan approval; **`status: partial`** — the
  offline half executed, the campaign close waits on H3).
- H3's mission is created when its phase opens (never pre-spawn past a HOLD); H3 is **held for Luke's
  cloud lane** (2026-08-04 ruling; spend params pre-ruled in the H3 row + roadmap §4 #1). *(Ground truth
  2026-08-09: `GEMINI_API_KEY` **is present on this node** — Keychain entry + exported env, name only. H3 is
  held by **ruling**, not blocked by credential.)*
- Dev-lane annex (second developer, Luke — Berthier S105): `missions/artifacts/halftone_dev_lanes.md`
  (**ratified 2026-08-03**).

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
