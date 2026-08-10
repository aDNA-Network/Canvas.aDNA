---
type: state
created: 2026-06-06
updated: 2026-08-09
status: active
last_edited_by: agent_mondrian
last_session: session_stanley_20260809_211323_halftone_h6_offline
tags: [state, governance, canvas, halftone, visual_fidelity, rlhf_surface, federation, standard, comfyui, refine]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

> **▶ 2026-08-09 — 🟢 H6 OFFLINE HALF EXECUTED: four defects, all of one family — code that was written, looked correct, and had never run the path it claimed (Mondrian, `session_stanley_20260809_211323_halftone_h6_offline`).** Operator opened the H6 lane at plan approval (= the gate, HV/H2/H4/H5 precedent) and ruled three things with it: **include print E2E** · **`canvas_comic` = reader-only freeze now** (open decision #3) · **RLHF routing = both sinks with a named boundary** (open decision #4). The trigger was housekeeping: **three Callisto memos had been sitting untracked in `who/coordination/` across sessions**, and the 2026-08-07 one **discharged the Bearly P5 evidence dependency** that HR's dispatch contract and H6's RLHF seam doc had been explicitly parked behind. The parked work was buildable the moment someone read the inbox. **Ground truth also corrected the H3 story: `GEMINI_API_KEY` is present on this node** (Keychain + exported env, name only) — H3 is held by **ruling**, not blocked by credential. **The four defects: (1) `export_spread` was UNREACHABLE** — a correct two-page-spread exporter has sat in `canvas_core/print.py` since the CanvasForge lineage, but `export_all` only ever called `export_page`, so every spread would have exported as two independent pages each fitting the whole 4124px image into one 2062px page, **squashed 2:1 and silent**; **(2) CMYK was MACHINE-DEPENDENT** — `_convert_to_cmyk` fell through a bare `except: pass` to Pillow's soft convert, so the same canvas produced different bytes depending on whether the host had ColorSync profiles, with nothing in the result, report or logs saying which; *this node has the profiles, which is exactly why it stayed invisible*; **(3) `RLHF_SIGNAL_TYPE_REJECT` was declared and never emitted** — combined with Schema-A structurally requiring a pick, a reject-only review pass produced **no signal at all**, and "none of these six is acceptable" is a stronger signal than "this one is best"; **(4) the visual-check gate always failed on comics** — all 24 findings came from exactly three knowledge-canvas *aesthetic* traps, none a defect. **Delivered:** `spec_rlhf_seam.md` (`proposed` — Canvas owns the capture substrate / III owns the signal schema; store heterogeneity normative; **ISS-vs-III resolved as a scope conflation**, two objects sharing one word, no ownership moved; decision #4 ruled; implementation **S-1..S-4 deliberately unbuilt** while the spec is unratified) · **`review_dispatch_contract v0` BOUND** (six clauses — **D5** refusal-atomicity adopted from Callisto's `F-S030-1` **credited by name**, **D6** venue boundary from ADR-007 mode L; **dispatcher deliberately NOT built** — the venue has not run a batch) · **`--profile knowledge-canvas|comic|all`** (comic **24→0** source, **21→3** rendered, and all 3 survivors are `CV-IMAGE-ASPECT-RATIO-01`, the trap that caught the real H2 drift — noise dropped, signal kept, with a test asserting no profile may ever drop a correctness trap) · **print E2E** (spread compose lands, the H6-deferred test **inverted not deleted**; colour policy resolved once at construction and always named; **DPI policy written down** — 300 target, 200 floor, warn-never-block because R7's ~195 is a legitimate proof page, spreads measured against the COMBINED target: verified live at 195 on one page vs **112** across two) · `comic_authoring_contract.md` (T3′; every command run before documenting — the first draft had the build flags wrong) · **`adr_009`** canvas_comic disposition. **The doctrine earned its keep a third time:** the first spread render passed *every* assertion — two 2062×3150 halves, correct page count — on **two flat green rectangles**, because the fake backend emits solid colour and a solid colour splits identically however you cut it; a structured source (gradient · centre seam · L/R markers · ruler ticks) proved the split, and **the markers being round** is the actual proof, since the pre-H6 double-fit would have squashed them. Suites: canvas_core 824→**841/3** · comic_render 92→**94/1** · producers **259** · `canvas_std` **115/10** · cert **11/11** · **firewall diff 0** · E2E `sync_hash c56c73c08428f621` byte-identical. **H6 is `status: partial` — the campaign close was NOT taken, because H3 has never run.**
>
> **▶ 2026-08-07 — 🟢 H4 LIVE-VERIFIED on L1 · Vulcan memo DELIVERED · parity push · tier default applied (Mondrian, `session_stanley_20260807_h4_live_verify_and_gate_items`).** The operator approved a recommendation set whose first item I proposed after checking ground truth rather than the campaign files: **`~/ComfyUI` is a real install on this node** (0.24.1, MPS, `sd_xl_base_1.0.safetensors` — the exact checkpoint the built-in graph defaults to), so H4's refine seam was testable **today, with no Anduril, no Gemini and zero spend**. "H4 is mocked until H3" was never true. **The live run found three defects the mocked suite could not**: **(L1, INHERITED — fleet-relevant)** `_poll_history` used `timeout_s`, a **30s HTTP-request** timeout, as the **generation** deadline — a 20-step SDXL img2img samples ~35s on MPS, so the adapter abandoned jobs the server went on to finish; present since M-3-05, so any other `ComfyForgeTier1Adapter` consumer had the same silent ceiling (fix: `generation_timeout_s` 600s, split); **(L2)** identical graphs hit ComfyUI's **result cache** → `success` + every node `execution_cached` + **empty outputs** → download found nothing, which H4's own deterministic seed made the *common* case (fix: `filename_prefix` derives from the output filename; the error now names the cache); **(L3)** `DEFAULT_UPSCALE_MODEL` was a guessed `RealESRGAN_x2.pth` vs the installed `x4plus`. **Four paths then verified green with the images LOOKED AT** (HV agent-confirmed-render doctrine): built-in graph → a correct cel-shaded lighthouse · **Vulcan's REAL `workflow_img2img.json`** patched by node class → a correct copper diving bell, **the convention holds against his actual file** · LoRA slot with a real weight → loads + conditions cleanly, rendering a generic bearded scientist **not Stanley**, an independent corroboration of his own **F-M04-B** · upscale `x4plus` → 1024²→**4096²**, over-solving roadmap **R7**. **The doctrine earned its keep again:** the first live result passed *every* automated assertion — success · correct dims · 383KB · differs-from-seed — on **a picture of nothing** (a flat purple field); only looking revealed it, and it diagnosed to the fake backend's solid-colour seed (img2img at denoise 0.4 preserves structure a solid colour hasn't got; at 1.0 the same call rendered the prompt correctly) — **not** a pipeline fault, documented in the README so nobody later reads mush as a broken seam. +5 regression tests → canvas_core **824/3** · comic_render **92/1** · firewall **0** · ruff clean. **Item 1 EXECUTED**: the Vulcan `comic_panel_refine` memo **delivered** (files-only, zero commits in his tree, Rule 10) — rewritten around the verified facts, so the ask shrank to "your existing workflow **plus** a LoRA slot and upscale", and it carries the inherited-timeout warning + the F-M04-B corroboration as courtesy. **Roadmap open decision #2 RULED: do not bundle the LoRA-training-completion ask** (his M04 already published *no production weight*; the blocker is F-M03-J hardware needing physical intervention — it would land back on the operator, not him). **Item 2**: wrapper follow-up #2 recommendation (leave the LoRA runner archived) rides that memo. **Item 3 EXECUTED**: parity push. **Inbound actioned**: Berthier/Operation Hearth `hm_m8` — `executor_tier_default: fable` applied to the halftone charter after independently auditing their slate read (accurate: 4 fable · 1 opus · 1 sonnet · h1 untyped); summon-only is right in front of H3's spend gate. **Still open: the HR review pass** (all six sidecar verdicts remain `null`).
>
> **▶ 2026-08-06 — 🟢 H4 EXECUTED (offline half): the Vulcan seam is REAL — `refine:comfy` is a working backend (Mondrian, `session_stanley_20260806_201701_halftone_h4_vulcan_seam`).** Operator opened the H4 lane at plan approval (= the gate, HV/H2/H5 precedent) after ruling out the two alternatives (H6-partial print pass · HR close-out); push posture = **batch at close**. The hybrid backend the operator locked in July is now wired end-to-end on the Canvas side, **with zero dependence on H3**: **substrate** — `canvas_core/comfyforge_adapter.py` gained `refine_image()` beside `generate_image()` (multipart `POST /upload/image` · built-in SDXL **img2img** graph `LoadImage→VAEEncode→KSampler@denoise<1.0` with the **negative in its own `CLIPTextEncode`**, never concatenated · optional `LoraLoader` + RealESRGAN upscale · **deterministic** refine seed, unlike generate's wall-clock one · named-template patching by node class that **degrades to the built-in graph** when `comic_panel_refine` is absent upstream — so a missing Vulcan workflow never blocks); **bridge** — NEW `comic_render/backends/comfy.py`, a thin manifest-shaped binding (the placement the boundary guard's own comment specifies: "the H4 seam is an HTTP adapter living in `canvas_core`"), registry flipped, `generate:comfy` **deliberately still raises** (ComfyUI is the *refine* engine; the cloud backend is the production substrate, ADR-003); **chain syntax** extended to `<stage>:<backend>[@denoise][/workflow]`, backward compatible; **`RefineClient` gained an additive `lora`** — `dispatch.run_refine` lifts H5's pair-gated `characters[]` entry and the binding injects the trigger token only when absent, **closing roadmap R3's "LoRA re-enters via the refine chain when trained"**. **Offline E2E chain proof**: 9 panels → 18 fake variants → **18 mocked-comfy refines** → 9 Schema-A selections → rendered canvas revalidates (`c56c73c08428f621` byte-identical) → **4 composited pages**. Suites: comic_render 73→**92/1skip** · canvas_core 800→**819/3** · producers **259** unchanged · `canvas_std` **115/10** · cert **11/11** · **firewall diff 0** · boundary guard green. `comic_render/tests/fixtures/comfy/` is **the contract with Vulcan** (diff a real capture against it and the delta is the integration work); live smoke behind `-m network`. **Wrapper follow-up #1 CLOSED** (`skills_used`/`workflows_used` → actual consumption + `workflows_requested` + endpoint override env); **#2 recommendation staged** (leave the archived LoRA-dispatch runner archived — it solved dispatch-side *training*, Vulcan's and Anduril-gated). **Vulcan `comic_panel_refine` memo STAGED** (`staged_pending_GO` — roadmap open decision #2 is the operator's at this gate). **Honest finding recorded (→ H6):** `canvas-visual-check` on the rendered mini-issue is *not* clean — but it wasn't before H4 either (source 24 findings → rendered 18; exactly one new, and it describes a full-page splash correctly filling its page). The trap pack's padding/density heuristics are calibrated for knowledge canvases; comic pages legitimately pack flush. **H4 remainder: the gemini→comfy chain proven LIVE — joins H3.**
>
> **▶ 2026-08-04 (night) — 🟢 HR GATE 2/3: THE AGENT-CONFIRMED RENDER EXECUTED — and it caught two live failures (Mondrian, `session_stanley_20260804_174045_halftone_hr_render_confirm`).** The doctrine paid for itself twice in one gate item. **Catch #1: the vault was in Obsidian restricted mode** — no per-vault trust key in app Local Storage; NO community plugin had ever loaded on this node's Canvas window; Meta Bind syntax painted as raw `INPUT[...]` code spans — **the surface's interactive layer had never rendered, anywhere, ever** (schema [OK] + visual-check 0 the whole time — neither rail can see it). Operator flipped community plugins ON (verified: leveldb trust key + vault reload + live paint; a first ~18:00 flip attempt hadn't persisted — re-ruled and re-executed ~22:22). **Catch #2: `defect_tags` multiSelect rendered `[META_BIND_ERROR]`** — block-only in Meta Bind 1.4.x, the builder emitted it inline; fixed (`review_canvas.py` → fenced ```meta-bind block, constraint in the docstring), pilot rebuilt deterministic (overwrite guard clean), revalidated (`adna_native` [OK] · visual-check 0 · review tests 13 · canvas_core **800/3** · ruff clean · firewall diff 0). **Confirmed live on real Obsidian 1.13.4:** all 8 controls as real widgets in note view AND **the full interactive layer inside canvas file-node embeds** (no degradation — the review UX works directly on the canvas). **Buttons-vs-toggles RESOLVED:** both idioms render (toggles = boolean intent flags · button = one-shot regenerate); the ratified spec's table stands, no errata (the spec never pinned emission form). Hygiene: two Jun-29 `.obsidian` strays added per tracked-sibling policy + notebook-navigator schema churn committed. **Remaining HR gate item (1): the operator's review pass** — the canvas is open in front of them. Local commits only; origin stays `4984ecf` (push = operator-gated batch).
>
> **▶ 2026-08-04 (late) — 🟢 THE GO WAVE EXECUTED: all six memos DELIVERED · `spec_canvas_review_surface` v1.0 RATIFIED · parity push → origin (Mondrian, `session_stanley_20260804_165801_halftone_go_wave`).** Plan approval = the batch GO (H2 precedent): **six deliveries** (Callisto H5-close notify [the written commitment fulfilled: LoRA-less = YES] · Pygmalion ZZ 3-wrapper refit · Astro refit+rename · Janus light · Kennedy **Oration adopt-a-wrapper** [the G7 structural closure] · Vulcan ack [#3 satisfied]) — files-only into target `who/coordination/`, recipients' copies carry `sent`, **zero target-vault commits** (Rule 10). **HR gate 1/3 closed**: the spec is **ratified** (§7.7: stanley · 2026-08-04 · accepted); remaining = **agent-confirmed Obsidian render** (link handed to the operator) + the operator's real review pass (at leisure; collector idempotent). **Parity push executed** (`master → origin`; gitleaks clean) — **Luke's H3 lane is UNBLOCKED** (comic_render + the pre-ruled spend params + the ratified annex are now public). D3 registrar ack stays standing (no nudge memo, by ruling). Canvas posture: **waiting** — Luke's H3 · Bearly's P5 evidence · the two HR gate leftovers; no Mondrian-executable build work open.
>
> **▶ 2026-08-04 — 🟢 THE PARALLEL TRIO LANDED: H5 EXECUTED · HR BUILT (gate-pending) · HF EXECUTED — H3 held for Luke with spend params PRE-RULED (Mondrian, `session_stanley_20260804_115855_halftone_h5_hr_hf`).** Operator rulings at plan approval (= the H5/HR/HF gates, HV/H2 precedent): phase selection H5+HR+HF · **H3 NOT opened — held for Luke's cloud lane** with parameters pre-ruled (**Gemini pro-image class · 3 variants/panel · $5 cap · `GEMINI_API_KEY` via the Home broker · aspect = geometry-derived** [mission_h2 finding #1]; recorded in the campaign H3 row + roadmap §4 #1) · `app.json` `propertiesInDocument: "hidden"` consented. **H5 (`comic_generator/compose_input.py`)**: VisualDNA bundles → enriched ComicInput → per-panel `qualities.characters` → the H2-reserved manifest lift (**zero `comic_render` src changes**). **Exit criterion proven by the named test** `test_lora_less_compose_reference_images_only` — Stanley-like (PENDING_TRAINING · `entries:` mapping · bundle-dir-relative) AND Bearly-like (`lora_refs: []` rights-HELD · vault-root-relative · `canonical: false`) fixtures + live-bundle smokes; **pair-gate** (trigger⇔lora from one `TRAINED\|VALIDATED` entry or neither); canonical-FIRST selection + `--ref-category`; workspace-root-relative emission; argparse CLI (`build` byte-compatible · `compose` · `build --bundle`); prompt-contract **§1a amendment**. comic 100→**123** · sweep **259** · comic_render **73**. **HR**: `spec_canvas_review_surface.md` (**draft** — ratification at the gate; Meta Bind ↔ affordance kinds; Bearly's nine controls informative; **dispatch = `review_dispatch_contract v0` NAMED STUB**, the Callisto seam) + `canvas_core/rlhf/review_canvas.py` → **REAL pilot** `what/artifacts/review_surface_pilot/` (6 SS variants — premise corrected: they live in-vault at `style_registry/ss_character/`, NOT in ComfyUI.aDNA; `adna_native` [OK] D-1/2/3 green; **`canvas-visual-check` 0 findings** after the rail corrected the first-draft geometry, 10 medium → rework → 0) + `review_collect.py` (three sinks: append-only `apply_response` via guarded `canvas_context` bootstrap · Schema-A per approval → the real corpus · III accumulate; **4-layer idempotency** incl. ledger-loss self-heal via the canvas-`at` fallback clock; `{kind: ai}` attribution — simulated verdicts never forged as human) + `iii_bridge` store-default repointed to the live `canvas_iii_learning_store.jsonl`. canvas_core 787→**800/3**; CLI plumbing E2E proven on a scratchpad copy. **HF**: census artifact (21 wrappers; **mechanism correction** — all six "CanvasForge-targeting" wrappers already carry `source_vault: Canvas.aDNA`; drift is `wrapper_for`/`substrate_pin`/prose/runtime-paths; only Emacs clean at 2.3.0; Home's runtime import via the archive shim = highest functional risk; Oration = NO wrapper, the G7 enabling condition) + **NEW `how/federation/federation_index.md`** (living registry; Vulcan follow-up **#3 satisfied**; standing drift ledger) + **5 memos `staged_pending_GO`** (Pygmalion ZZ-refit ×3 · Astro refit+rename [SiteForge alias lands once] · Janus light · Kennedy **adopt-a-wrapper** [the G7 structural closure] · Vulcan ack). Suites: comic_generator **123** · producers **259** · comic_render **73** · canvas_core **800/3** · canvas_std **115/10** · cert **11/11** · **firewall diff 0** (canvas_std AND canvas_context). 5 local commits; **origin still `9d22561` — 6 ahead; parity push = its own GO (Luke's H3 lane is blocked on it)**.
>
> **▶ 2026-08-03 (late) — 🟢 H2 EXECUTED: the render bridge is REAL · all four operator asks cleared (Mondrian, `session_stanley_20260803_224918_halftone_h2_bridge`).** Four rulings at plan approval: **H2 gate GO** (approval = the gate, HV precedent) · **all 5 memo GOs** (delivered same session: Kennedy→Oration · Noether→LatticeProtocol · Callisto→Bearly · Berthier→aDNALabs [**dev-lane annex RATIFIED** by that GO] · Hestia→Home; per-send, files-only, no target-vault commits) · **parity push GO — EXECUTED** (`master → origin` at `9d22561`, gitleaks clean; Luke's PR flow unblocked) · **open decision #5 ruled: `issue.rendered.canvas` = derived artifact**. **H2 build**: NEW `what/production/comic_render/` (producer idiom; 9 modules + `comic-render` CLI; **72 tests**; own `.venv`): manifest v0.1 with first-class **`render_chain`** (chain, not switch) · extract (staleness-guarded) · `backends/fake` (**pure-Python PNG, zero PIL** — deterministic, location-independent bytes) + additive `RefineClient` protocol · chain dispatch+refine (idempotent; **budget_cap enforced before the first call**) · **Schema-A-only** select (fake runs corpus-isolated under `runs/…/selections/`) · write-back-to-NEW-file (topology + `_reserved.sync` **byte-identical, asserted**; ANCHOR_REF_KEYS guarded) · stage-6 validate (aDNA-Native + D-1/2/3 + files + DPI) · PrintExporter compose shim (**R5 canvas-absolute→bleed remap, golden ±1px**; full-page→full-bleed promotion) · inverted AST no-diffusion guard. **E2E offline proof**: mini-issue fixture → 27 fake variants → 9 selections → rendered canvas revalidates (`c56c73c08428f621` unchanged) → **4 composited 2062×3150 page JPGs**; hybrid generate→refine chain proven; re-runs = zero new work. **Amended exit executed**: `canvas-visual-check` clean-running (found + fixed a REAL HV-trap gap: CV-FILE-PROPS-01 crashed on binary targets — the fleet's first image file nodes; hardened + 3 regression tests → canvas_core **787/3**) + **agent-confirmed render** (pages read + confirmed; recorded in the mission). NEW signal recorded for H3: **aspect drift** (declared `3:4` vs authored 663×1025 geometry → ~10–14% cover-crop; `CV-IMAGE-ASPECT-RATIO-01` caught it). Suites: producers 236 · canvas_std 115/10 · cert 11/11 · **firewall diff 0**.
>
> **▶ 2026-08-03 — 🟢 HALFTONE SCOPE AMENDED (+HV/+HR/+HF) · HV EXECUTED · intake wave cleared (Mondrian, `session_stanley_20260803_213854_halftone_amendment_hv`).** Operator folded three phases into Halftone (plan approval = the HV gate): **HV visual-fidelity rail — EXECUTED**: `canvas-visual-check` CLI (`canvas_core/traps/cli.py`) over the trap pack · 4 new geometry traps (`CV-LEAD-COST-01`/`CV-GROUP-LABEL-01`/`CV-EDGE-LABEL-01` [first edge-geometry trap]/`CV-FILE-PROPS-01`) · `text_metrics.py` **Obsidian-CSS calibration** (Kennedy's `canvas_fit_check.py` absorbed with credit; `CV-TEXT-BOUNDS-01` overflow now calibrated) · **agent-confirmed-render doctrine ADOPTED** (`skill_canvas_producer_build` + `spec_federation_contract` §4 **Amendment 1**, operator-ratified; **closes HOME-CV-3**) · `canvas_reviewers.yaml` **1.1.0** · `what/docs/canvas_authoring_guidance.md`. Trigger: the **Oration M-R5 incident** (a canvas passed `canvas-std [OK]` and rendered unreadable; Kennedy coord 2026-08-03 — intake ask executed same-day, backlog idea filed as `accepted/graduated`). **HR** (G9, RLHF review surface — Meta Bind capture → Schema-A + III; pattern + working pilot over real images; dispatch contract-only pending Bearly P5 evidence) + **HF** (G8, federation census/index + staged refederation memos; ~6 wrappers still CanvasForge-targeting, no index — the incident's enabling condition) chartered, open at their own gates. **Verification:** canvas_core **784 passed/3 skipped** (own `.venv` reconstituted — the suite was runnable in NO venv since the pt09-P5 relocation) · producers **236** · `canvas_std` **115/10** untouched · certification **11/11** · firewall diff **0**. **Hygiene:** stale 07-09 session filed → `history/2026-07/` (Hestia W8 + Callisto §3 flags cleared) · CLAUDE.md persona drift fixed (Berthier→Mondrian) · STATE lower half rewritten current (stale Keystone sections → state archive, verbatim). **5 reply memos staged `staged_pending_GO`** (Kennedy ack · Callisto [H5 LoRA-less = **untested**, now an H5 exit criterion; HR seam named] · Berthier [dev-lane annex → `halftone_dev_lanes.md`; Luke = cloud lane H3 + first-light H6] · Noether G4-relabel ack · Hestia HOME-CV-3 disposition) — **deliveries are per-send operator GOs**.
>
> **▶ 2026-07-09 — 🟢 OPERATION HALFTONE CHARTERED — comic system: review → render bridge → E2E pipeline (Mondrian, `session_stanley_20260709_135234_halftone_charter_h1`).** *(Amended 2026-08-03 — phases now H0–H6 + HV/HR/HF; see the banner above + the campaign master.)* A three-track comic-system review (code · governance/specs · workflow) found **a well-built spec→canvas producer (comic_generator, 87 tests) whose pipeline dead-ends at rendering — zero comics ever rendered** (G1: no prompt→image bridge; ComfyUI.aDNA has no comic workflow, GPU node unreachable, LoRAs `PENDING_TRAINING`; the only precedent called Imagen 4 directly). Operator locked (2026-07-07): **full program T0–T4+G** · **hybrid backend — Gemini/Imagen generates → output seeds ComfyUI img2img/refine** (matches inherited CanvasForge ADR-003: Imagen = production substrate, ComfyForge = style-transfer engine; cloud primary, Vulcan coord memo never blocking) · **T3 authoring = contract-only**. Boundary: **"Canvas dispatches, it does not diffuse"** (AST-guarded; `canvas_std` untouched all campaign). Chartered `campaign_canvas_halftone` (phases **H0–H6**: H1 producer hardening [`prompt_layers` + validation] + ADR port + prompt contract → H2 `what/production/comic_render/` bridge offline [manifest v0.1 w/ `render_chain` · write-back-to-NEW-file, sync_hash-safe by construction] → **H3 first REAL rendered page** [SPEND gate + eye-gate — the fleet's first] → H4 Vulcan seam/interop memo → H5 VisualDNA auto-compose → H6 authoring contract + print E2E + governance close). Review artifacts: `how/campaigns/campaign_canvas_halftone/missions/artifacts/halftone_{gap_register,roadmap}.md`. Phase gates human (SO-1); H3 additionally spend-gated. **Executing H0+H1** in this session.
>
> **▶ STANDARD PINS + OPEN TAIL (live).** Canvas Standard **v2.3.0** · `canvas_std` **115/10** · certification **11/11** · firewall clean. **Open tail (non-blocking): D3 Rosetta registrar ack** (`#needs-human`) — on ack, flip `adr_003` Amendment 1 + `lip_registry` "pending" → ratified. *(Hoisted 2026-08-03 from the closed 2026-07-02 Beacon banner, which held the only copy; that banner is archived at `how/state_archive_20260803.md`.)*

> *(Closed campaign banners / build history relocated verbatim 2026-08-03 → [`how/state_archive_20260803.md`](how/state_archive_20260803.md) — nothing deleted, SO-3/SO-7. Second pass same day: the Keystone-era lower-half sections joined it when this file was rewritten Halftone-current.)*

## ▶ Resume Here — 🟢 **OPERATION HALFTONE** (live; phases H0–H6 + HV/HR/HF)

**H0 ✅ · H1 ✅ · HV ✅ · H2 ✅ · H5 ✅ · HF ✅ · H4 ✅ (offline half) · H6 ✅ (offline half, `partial`) ·
HR 🟡 built (gate 2/3 closed — spec ratified · render agent-confirmed) — H3 HELD for Luke's cloud lane**
(spend params **PRE-RULED** 2026-08-04: Gemini pro-image class · 3 variants/panel · $5 cap · `GEMINI_API_KEY`
via the Home broker · aspect = geometry-derived; the gate call itself stays open; his lane is UNBLOCKED).

**H3 is now the ONLY thing standing between Halftone and its close.** Everything else that could be built
without real pixels is built. H3: `backends/gemini.py` + the geometry-aspect ruling in `extract.py` → live
render → operator eye-gate → the fleet's first composited page. **One live
`--chain "generate:gemini,refine:comfy@0.4/comic_panel_refine"` run closes H3 *and* H4's remainder** (the
refine half is built, tested and live-verified against a real ComfyUI). Then H6 re-opens for the campaign
AAR + close with the real-pixel evidence the offline pass could not produce.

> ⚠️ **Correcting a standing assumption:** `GEMINI_API_KEY` **is present on this node** (Keychain entry +
> exported env var; name only, value never read — checked 2026-08-09). H3 is held by the **2026-08-04 lane
> ruling**, not blocked by a missing credential. If the operator would rather Mondrian take H3 than hold it
> for Luke, nothing technical is in the way — only the spend gate and the lane call, both theirs.

Read: `how/campaigns/campaign_canvas_halftone/` (master + CLAUDE.md) →
`missions/mission_{h6_close,h4_vulcan_seam,h5_visualdna_compose,hr_review_surface,hf_federation_hygiene}.md` →
`what/specs/spec_rlhf_seam.md` → `how/federation/federation_index.md`.

**Awaiting the operator (surface at next contact):**
1. **HR gate leftover (1 of 3 — the last)**: **your real review pass** on
   `what/artifacts/review_surface_pilot/ss_variant_review.canvas` (open in Obsidian — all 8 controls are
   live, in note view and inside the canvas embeds; set verdicts, save; then Mondrian runs
   `review_collect --approver stanley` per the pilot README — idempotent, at leisure). *(Re-checked
   2026-08-09: all six sidecar verdicts still `null` — the pass hasn't happened yet.)*
2. **Three H6 ratifications pending your §7.7 signature** (all `proposed`, none blocking):
   **`spec_rlhf_seam.md`** (the capture/signal boundary + the reject→III ruling — its implementation
   S-1..S-4 is deliberately held until you sign, so signing is what unblocks it) ·
   **`spec_canvas_review_surface` §6 amendment** (dispatch contract D1–D6; it does *not* ride the plan
   approval as its signature, because the plan approved *writing* the clauses and a signature cannot precede
   its text) · **`adr_009`** (`canvas_comic` freeze).
3. **One staged memo awaiting a per-send GO**: `coord_2026_08_09_mondrian_to_callisto_dispatch_contract_bound.md`
   (tells Callisto their `F-S030-1` became clause D5, credited).
4. **Awaiting Vulcan's reply** (non-blocking, no action owed by us): the `comic_panel_refine` workflow ·
   the endpoint question · his call on wrapper follow-up **#2**. **Nothing blocks** — an unresolvable
   workflow degrades to the built-in graph, which is live-verified.
5. *(Standing, non-blocking)* **D3 Rosetta registrar ack** `#needs-human` (nudge memo available on request).

*(Resolved 2026-08-09 at plan approval: H6 offline lane opened · print E2E **in scope** · roadmap open
decision **#3 RULED** [`canvas_comic` = reader-only freeze now, archive after H3 → `adr_009`] · open decision
**#4 RULED** [RLHF routing = both sinks, boundary named, reject → III from `responses[]`] · three Callisto
memos **ACTIONED** · dev-lane pointer corrected [the annex was ratified 2026-08-03 all along; the campaign
CLAUDE.md row was the stale thing]. Resolved 2026-08-07: item 0 live verification — EXECUTED · Vulcan memo —
**DELIVERED** · roadmap open decision **#2 RULED** [do not bundle the LoRA-training ask] · parity push —
**EXECUTED** · Berthier's `executor_tier_default: fable` — **APPLIED**. Resolved 2026-08-06 at plan approval: H4 opened [lane chosen
over H6-partial and HR close-out] · push posture = batch at close. Resolved 2026-08-04 at the GO wave: all
six memo deliveries — EXECUTED · parity push — EXECUTED [Luke's H3 lane unblocked] ·
`spec_canvas_review_surface` v1.0 — RATIFIED.)*

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds E4.4 as a worked build; informs D2/D4/D7. Opens no phase, builds no code until E4. *(Fulfilled in spirit by Keystone E4.4; kept for the method capture.)*

## Current Phase

**Operation Halftone (live).** History: Cartography → Keystone (v2.0.x shipped) → Palette → Salon → Armature →
Lodestar → Beacon (v2.3.0; LIP queue drained) → **Halftone** (chartered 2026-07-09; **amended 2026-08-03** +HV/HR/HF).
Done: H0 charter · H1 producer hardening (comic 87→100; `adr_008` + prompt contract) · **HV visual-fidelity rail**
(CLI + 4 traps + calibration + doctrine adoption + reviewers 1.1.0 + guidance) · **H2 render bridge**
(`comic_render` 0.1.0 — offline E2E to composited pages; dev-lane annex ratified) · **H5 VisualDNA compose**
(2026-08-04 — LoRA-less exercised + tested, the exit criterion; comic 123) · **HF federation hygiene**
(2026-08-04 — census + `federation_index.md` + 5 staged memos). **H4 Vulcan seam** (2026-08-06 — `refine:comfy` real; img2img
on the existing adapter + thin binding + chain `/workflow` syntax + the pair-gated LoRA slot; offline E2E
chain proof to 4 composited pages; comic_render **92/1**, canvas_core **819/3**; the LIVE chain proof joins
H3). **HR built, gate 2/3 closed** (spec **RATIFIED** [GO wave] ·
render **agent-confirmed** [2026-08-04 `_174045`: two live catches — restricted mode + multiSelect
block-only; all 8 controls live incl. inside canvas embeds]; remaining = the operator's
review pass). **H6 offline half** (2026-08-09 — `status: partial`: RLHF seam spec · dispatch contract v0
bound · comic visual-check profile · print E2E [spread compose reachable, CMYK deterministic, DPI policy] ·
authoring contract · `adr_009`; canvas_core **841/3**, comic_render **94/1**). Open: **H3 — the only phase
left before the close** (Luke's cloud lane; params pre-ruled; one live run closes H3 *and* H4's remainder)
→ **H6 re-open** for the campaign AAR + close.

## What's Done (session `_211323` — 2026-08-09, H6 the offline half)

- **Gate rulings recorded**: H6 offline lane opened at plan approval; print E2E in scope; open decisions
  **#3** (`canvas_comic` freeze) and **#4** (RLHF routing) **RULED**.
- **O1 intake**: three Callisto memos landed as-delivered (byte-unchanged, own commit) then **actioned** with
  disposition blocks; reply memo **staged** (`staged_pending_GO`); `federation_index` Bearly row corrected —
  empty wrapper, but our busiest live consumer.
- **O2** `what/specs/spec_rlhf_seam.md` (NEW, `proposed`) + `spec_interface_surface` §2 qualified + a stale
  `iii_bridge` docstring corrected to ground truth (it claimed 4 store entries; the live store holds a
  `_meta` line + 2 `CANVAS-L-*` pattern entries and **zero** RLHF signals).
- **O3** `spec_canvas_review_surface` §6: stub → **six clauses D1–D6**; amendment `proposed`, and explicitly
  **not** riding the plan approval as its signature.
- **O4** `traps/cli.py` `--profile` (+8 tests incl. one asserting **no profile may ever drop a correctness
  trap**); authoring-guidance note replaced advice with mechanism.
- **O5** `print.py` + `compose.py`: spread compose reachable · colour policy resolved once and always named ·
  DPI policy written down · `test_print.py`'s **first** CMYK and composite tests (+9).
- **O6** `what/docs/comic_authoring_contract.md` (NEW) + a `what/docs/AGENTS.md` index row and an honest flag
  that the index predates this vault's own docs.
- **O7** `adr_009` · `mission_h6_close.md` (`partial`, with AAR) · campaign master/CLAUDE.md/roadmap/STATE.
- **Verification**: canvas_core **841/3** · comic_render **94/1** · canvas_comic **99** · producers **259** ·
  canvas_std **115/10** · cert **11/11** · **firewall diff 0** · ruff clean on changed files · E2E
  `sync_hash c56c73c08428f621` byte-identical → 4 pages · `--cmyk` a real ICC separation · spread split
  **confirmed by looking**, after it first passed every assertion on a picture of nothing.

## What's Done (session `_201701` — 2026-08-06, H4 the Vulcan seam)

- **Gate ruling recorded**: H4 opened at plan approval (lane chosen over H6-partial + HR close-out); push
  posture = batch at close.
- **Substrate**: `canvas_core/comfyforge_adapter.py` + `refine_image` · `_upload_image` (multipart) ·
  `_build_img2img_workflow` (separate negative node · optional LoRA + upscale) · `_resolve_refine_workflow` /
  `_patch_workflow_template` (numeric node-id ordering; degrades to built-in) · `_refine_seed` (deterministic)
  · `ComfyForgeConfig.workflow_dir`. **20 new tests** → canvas_core **819/3**.
- **Bridge**: NEW `comic_render/backends/comfy.py` (thin binding; `COMIC_RENDER_COMFY_ENDPOINT` → else the
  wrapper's `l1_local`; trigger-word injection; `cost_per_image = 0.0`) · registry flip (`generate:comfy`
  still raises, by design) · `parse_chain` `/workflow` · `RefineClient.lora` + `dispatch._lora_for`.
  **18 new tests + fixtures** → comic_render **92/1skip**.
- **Contract fixtures** `comic_render/tests/fixtures/comfy/` (4 recorded responses + the
  `comic_panel_refine.json` request shape + README) — the artifact Vulcan's workflow gets diffed against.
- **Coordination**: Vulcan `comic_panel_refine` memo **staged** (`staged_pending_GO`) · wrapper follow-up #1
  **closed** · #2 recommendation written · `federation_index.md` row updated.
- **Verification**: comic_render **92/1** · canvas_core **819/3** · producers **259** · canvas_std **115/10** ·
  cert **11/11** · ruff no new findings · **firewall diff 0** · boundary guard green · offline E2E chain proof
  (sync_hash `c56c73c08428f621` unchanged → 4 composited pages).
- **Finding for H6**: `canvas-visual-check` isn't a meaningful gate for comic output yet (knowledge-canvas
  heuristics vs flush-packed comic pages) — source 24 findings → rendered 18, one new and it's correct.

## What's Done (session `_115855` — 2026-08-04, the H5+HR+HF trio)

- **Gate rulings recorded**: phases H5+HR+HF opened (plan approval = gates) · H3 held for Luke + spend params
  pre-ruled (pro-image · 3var · $5 · `GEMINI_API_KEY` · geometry-aspect) → campaign H3 row + roadmap §4 #1.
- **H5**: `comic_generator/compose_input.py` (bundle parsing across all 4 live `lora_refs` shapes ·
  **pair-gate** · canonical-FIRST refs · both path conventions → workspace-root-relative · descriptor chain ·
  direction-safe matching · raw-dict enrichment + idempotent provenance) · `CharacterDescriptor` +3 asset
  fields · `qualities.characters` emission (omitted-when-empty) · argparse CLI · prompt-contract §1a ·
  **23 new tests incl. the named exit-criterion test + live smokes** · staged Callisto notify.
- **HR**: `spec_canvas_review_surface.md` (draft) + `review_canvas.py` (REAL 6-variant pilot; `adna_native`
  [OK]; visual-check 10-medium→rework→**0**) + `review_collect.py` (three sinks · 4-layer idempotency ·
  ledger-loss self-heal · `{kind: ai}` attribution) + `iii_bridge` live-store repoint + 13 tests + CLI
  plumbing E2E; `app.json` hidden-properties key (consented); pilot uncommitted-by-policy (artifacts
  gitignored; deterministic rebuild = `python -m canvas_core.rlhf.review_canvas`).
- **HF**: census artifact (21 wrappers; mechanism correction) · `how/federation/federation_index.md` (NEW;
  Vulcan #3 satisfied; drift ledger) · 5 memos `staged_pending_GO`.
- **Verification**: comic_generator **123** · producers **259** · comic_render **73** · canvas_core **800/3** ·
  canvas_std **115/10** · cert **11/11** · ruff clean · **firewall diff 0**. 6 commits local; origin `9d22561`.

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip) — **superseded 2026-06-14 (E3.4)**: now carries supersession banners → Canvas.aDNA v2.0.0. Invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism; Canvas LIP home stood up at `who/governance/lips/` (Beacon).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7) — now carrying **Amendment 1's visual gate** on the Canvas side.
- **Visual reality is machine-checked**: `canvas_core/traps/` (13 implemented/graduated, 8 geometric) + `canvas-visual-check` + the agent-confirmed-render doctrine (adopted). Schema ≠ fit ≠ sight.

## Active Blockers

- **None blocking.** Pending operator decisions are listed under **Resume Here** (memo GOs · parity push · H2 gate ·
  D3 registrar ack `#needs-human` non-blocking).
- **PT-P5 residual (Mondrian's calls, non-blocking):** `what/artifacts/` git-tracking policy · III consumer
  re-accounting (drop/repoint archived CanvasForge → Argus) · `canvas_core→canvas_std` §C #29 + `CANVASFORGE_CODE`
  §C #39 shim ref-sweeps (grace 2027-06-13).
- **Deferred by design:** H4's **live** gemini→comfy chain proof (joins H3 — the offline half is done) ·
  ~~HR dispatch-side (awaits Bearly P5 evidence)~~ → **evidence LANDED 2026-08-07, contract BOUND 2026-08-09**
  (`review_dispatch_contract v0`, six clauses; the *dispatcher* stays unbuilt by ruling, not by dependency) ·
  reject→III implementation S-1..S-4 (held until `spec_rlhf_seam` is ratified) · `CV-COMIC-STYLE-01`
  (needs H3 pixels to calibrate) · `what/docs/` index full refresh · Home harness graduation
  (`canvas_visual_loop` → `canvas_core`, adoption-path step 2 — rule at H2/HR) · `html_renderer` file-node preview
  fix (static trap covers it) · `canvas_core` console-script packaging.

## Next Steps

1. **Operator**: three §7.7 ratifications (`spec_rlhf_seam` · the dispatch-contract amendment · `adr_009`) ·
   the Callisto memo GO · the push GO · the HR review pass · **the H3 gate call** (and, with it, whether H3
   stays Luke's lane — the credential is present on this node either way); registrar ack when it lands.
2. **H3** — now the only phase between Halftone and its close: `backends/gemini.py` (credential via the Home
   broker, names-only) + the geometry-derived aspect ruling in `extract.py` → live render the mini-issue
   splash → operator eye-gate → the fleet's first real composited page. M-SB-D2 first-light spec is the
   preferred subject, Mondrian's mini-issue the fallback. **One live
   `--chain "generate:gemini,refine:comfy@0.4/comic_panel_refine"` run also closes H4's remainder.**
3. **H6 re-open** (after H3): campaign AAR + close · real-pixel DPI evidence · `CV-COMIC-STYLE-01`
   calibration · the HR pilot's second consumer · `canvas_comic` archive (per `adr_009`) · S-1..S-4
   reject→III implementation once the seam spec is signed.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
