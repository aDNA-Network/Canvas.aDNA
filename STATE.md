---
type: state
created: 2026-06-06
updated: 2026-08-03
status: active
last_edited_by: agent_mondrian
last_session: session_stanley_20260803_224918_halftone_h2_bridge
tags: [state, governance, canvas, halftone, visual_fidelity, rlhf_surface, federation, standard]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

> **▶ 2026-08-03 (late) — 🟢 H2 EXECUTED: the render bridge is REAL · all four operator asks cleared (Mondrian, `session_stanley_20260803_224918_halftone_h2_bridge`).** Four rulings at plan approval: **H2 gate GO** (approval = the gate, HV precedent) · **all 5 memo GOs** (delivered same session: Kennedy→Oration · Noether→LatticeProtocol · Callisto→Bearly · Berthier→aDNALabs [**dev-lane annex RATIFIED** by that GO] · Hestia→Home; per-send, files-only, no target-vault commits) · **parity push GO — EXECUTED** (`master → origin` at `9d22561`, gitleaks clean; Luke's PR flow unblocked) · **open decision #5 ruled: `issue.rendered.canvas` = derived artifact**. **H2 build**: NEW `what/production/comic_render/` (producer idiom; 9 modules + `comic-render` CLI; **72 tests**; own `.venv`): manifest v0.1 with first-class **`render_chain`** (chain, not switch) · extract (staleness-guarded) · `backends/fake` (**pure-Python PNG, zero PIL** — deterministic, location-independent bytes) + additive `RefineClient` protocol · chain dispatch+refine (idempotent; **budget_cap enforced before the first call**) · **Schema-A-only** select (fake runs corpus-isolated under `runs/…/selections/`) · write-back-to-NEW-file (topology + `_reserved.sync` **byte-identical, asserted**; ANCHOR_REF_KEYS guarded) · stage-6 validate (aDNA-Native + D-1/2/3 + files + DPI) · PrintExporter compose shim (**R5 canvas-absolute→bleed remap, golden ±1px**; full-page→full-bleed promotion) · inverted AST no-diffusion guard. **E2E offline proof**: mini-issue fixture → 27 fake variants → 9 selections → rendered canvas revalidates (`c56c73c08428f621` unchanged) → **4 composited 2062×3150 page JPGs**; hybrid generate→refine chain proven; re-runs = zero new work. **Amended exit executed**: `canvas-visual-check` clean-running (found + fixed a REAL HV-trap gap: CV-FILE-PROPS-01 crashed on binary targets — the fleet's first image file nodes; hardened + 3 regression tests → canvas_core **787/3**) + **agent-confirmed render** (pages read + confirmed; recorded in the mission). NEW signal recorded for H3: **aspect drift** (declared `3:4` vs authored 663×1025 geometry → ~10–14% cover-crop; `CV-IMAGE-ASPECT-RATIO-01` caught it). Suites: producers 236 · canvas_std 115/10 · cert 11/11 · **firewall diff 0**.
>
> **▶ 2026-08-03 — 🟢 HALFTONE SCOPE AMENDED (+HV/+HR/+HF) · HV EXECUTED · intake wave cleared (Mondrian, `session_stanley_20260803_213854_halftone_amendment_hv`).** Operator folded three phases into Halftone (plan approval = the HV gate): **HV visual-fidelity rail — EXECUTED**: `canvas-visual-check` CLI (`canvas_core/traps/cli.py`) over the trap pack · 4 new geometry traps (`CV-LEAD-COST-01`/`CV-GROUP-LABEL-01`/`CV-EDGE-LABEL-01` [first edge-geometry trap]/`CV-FILE-PROPS-01`) · `text_metrics.py` **Obsidian-CSS calibration** (Kennedy's `canvas_fit_check.py` absorbed with credit; `CV-TEXT-BOUNDS-01` overflow now calibrated) · **agent-confirmed-render doctrine ADOPTED** (`skill_canvas_producer_build` + `spec_federation_contract` §4 **Amendment 1**, operator-ratified; **closes HOME-CV-3**) · `canvas_reviewers.yaml` **1.1.0** · `what/docs/canvas_authoring_guidance.md`. Trigger: the **Oration M-R5 incident** (a canvas passed `canvas-std [OK]` and rendered unreadable; Kennedy coord 2026-08-03 — intake ask executed same-day, backlog idea filed as `accepted/graduated`). **HR** (G9, RLHF review surface — Meta Bind capture → Schema-A + III; pattern + working pilot over real images; dispatch contract-only pending Bearly P5 evidence) + **HF** (G8, federation census/index + staged refederation memos; ~6 wrappers still CanvasForge-targeting, no index — the incident's enabling condition) chartered, open at their own gates. **Verification:** canvas_core **784 passed/3 skipped** (own `.venv` reconstituted — the suite was runnable in NO venv since the pt09-P5 relocation) · producers **236** · `canvas_std` **115/10** untouched · certification **11/11** · firewall diff **0**. **Hygiene:** stale 07-09 session filed → `history/2026-07/` (Hestia W8 + Callisto §3 flags cleared) · CLAUDE.md persona drift fixed (Berthier→Mondrian) · STATE lower half rewritten current (stale Keystone sections → state archive, verbatim). **5 reply memos staged `staged_pending_GO`** (Kennedy ack · Callisto [H5 LoRA-less = **untested**, now an H5 exit criterion; HR seam named] · Berthier [dev-lane annex → `halftone_dev_lanes.md`; Luke = cloud lane H3 + first-light H6] · Noether G4-relabel ack · Hestia HOME-CV-3 disposition) — **deliveries are per-send operator GOs**.
>
> **▶ 2026-07-09 — 🟢 OPERATION HALFTONE CHARTERED — comic system: review → render bridge → E2E pipeline (Mondrian, `session_stanley_20260709_135234_halftone_charter_h1`).** *(Amended 2026-08-03 — phases now H0–H6 + HV/HR/HF; see the banner above + the campaign master.)* A three-track comic-system review (code · governance/specs · workflow) found **a well-built spec→canvas producer (comic_generator, 87 tests) whose pipeline dead-ends at rendering — zero comics ever rendered** (G1: no prompt→image bridge; ComfyUI.aDNA has no comic workflow, GPU node unreachable, LoRAs `PENDING_TRAINING`; the only precedent called Imagen 4 directly). Operator locked (2026-07-07): **full program T0–T4+G** · **hybrid backend — Gemini/Imagen generates → output seeds ComfyUI img2img/refine** (matches inherited CanvasForge ADR-003: Imagen = production substrate, ComfyForge = style-transfer engine; cloud primary, Vulcan coord memo never blocking) · **T3 authoring = contract-only**. Boundary: **"Canvas dispatches, it does not diffuse"** (AST-guarded; `canvas_std` untouched all campaign). Chartered `campaign_canvas_halftone` (phases **H0–H6**: H1 producer hardening [`prompt_layers` + validation] + ADR port + prompt contract → H2 `what/production/comic_render/` bridge offline [manifest v0.1 w/ `render_chain` · write-back-to-NEW-file, sync_hash-safe by construction] → **H3 first REAL rendered page** [SPEND gate + eye-gate — the fleet's first] → H4 Vulcan seam/interop memo → H5 VisualDNA auto-compose → H6 authoring contract + print E2E + governance close). Review artifacts: `how/campaigns/campaign_canvas_halftone/missions/artifacts/halftone_{gap_register,roadmap}.md`. Phase gates human (SO-1); H3 additionally spend-gated. **Executing H0+H1** in this session.
>
> **▶ STANDARD PINS + OPEN TAIL (live).** Canvas Standard **v2.3.0** · `canvas_std` **115/10** · certification **11/11** · firewall clean. **Open tail (non-blocking): D3 Rosetta registrar ack** (`#needs-human`) — on ack, flip `adr_003` Amendment 1 + `lip_registry` "pending" → ratified. *(Hoisted 2026-08-03 from the closed 2026-07-02 Beacon banner, which held the only copy; that banner is archived at `how/state_archive_20260803.md`.)*

> *(Closed campaign banners / build history relocated verbatim 2026-08-03 → [`how/state_archive_20260803.md`](how/state_archive_20260803.md) — nothing deleted, SO-3/SO-7. Second pass same day: the Keystone-era lower-half sections joined it when this file was rewritten Halftone-current.)*

## ▶ Resume Here — 🟢 **OPERATION HALFTONE** (live; phases H0–H6 + HV/HR/HF)

**H0 ✅ · H1 ✅ · HV ✅ · H2 ✅ (2026-08-03) — HOLDING at →H3** (SO-1; H3 is additionally **SPEND-gated + eye-gated**).
H3 = `backends/gemini.py` + the **first REAL rendered page in the fleet's history** (registry slot + chain executor
+ budget enforcement already in place; M-SB-D2 first-light convergence per the **ratified** dev-lane annex — Luke
leads the cloud lane under Mondrian review). **H5** (VisualDNA compose) now parallel-eligible after H2; **HR**
parallel-eligible; **HF** any order, sonnet-eligible. Read: `how/campaigns/campaign_canvas_halftone/` (master +
CLAUDE.md) → `missions/mission_h2_render_bridge.md` (verification + the 3 recorded findings) →
`missions/artifacts/halftone_{gap_register,roadmap}.md`.

**Awaiting the operator (surface at next contact):**
1. **H2→H3 gate call + SPEND parameters** (roadmap open decision #1): model tier · variants/panel (rec. 3) ·
   budget cap (manifest-enforced, proven) · credential name via the Home broker (`GEMINI_API_KEY`-class,
   names-only). Plus the **aspect-policy ruling** (mission finding #1): request geometry-derived aspect vs
   producer emits geometry-consistent ratios — decide before real spend.
2. *(Standing, non-blocking)* **D3 Rosetta registrar ack** `#needs-human`.

*(Resolved 2026-08-03 at the H2 plan approval: all 5 memo GOs — delivered · parity push — executed `→ 9d22561` ·
H2 gate — executed · decision #5 — derived artifact. The H2 changeset itself is committed locally, NOT pushed —
next parity push is its own GO.)*

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds E4.4 as a worked build; informs D2/D4/D7. Opens no phase, builds no code until E4. *(Fulfilled in spirit by Keystone E4.4; kept for the method capture.)*

## Current Phase

**Operation Halftone (live).** History: Cartography → Keystone (v2.0.x shipped) → Palette → Salon → Armature →
Lodestar → Beacon (v2.3.0; LIP queue drained) → **Halftone** (chartered 2026-07-09; **amended 2026-08-03** +HV/HR/HF).
Done: H0 charter · H1 producer hardening (comic 87→100; `adr_008` + prompt contract) · **HV visual-fidelity rail**
(CLI + 4 traps + calibration + doctrine adoption + reviewers 1.1.0 + guidance) · **H2 render bridge**
(`comic_render` 0.1.0 — 9 modules + CLI, 72 tests, offline E2E to composited pages; dev-lane annex ratified).
Open: **H3** (first real page, at gate; SPEND+eye gates; M-SB-D2 convergence; aspect-policy ruling first) →
H4 (Vulcan seam; wrapper already delivered `comfyui/` 0.2.0 @ `a8a4356`; `RefineClient` protocol ready) →
H5 (VisualDNA compose; **LoRA-less exit criterion**; parallel-eligible NOW) → HR · HF → H6 (close).

## What's Done (this session — 2026-08-03 late, H2 + the four asks)

- **Operator asks cleared**: 5 memos **delivered** (Canvas-side copies flipped `sent`; Berthier GO **ratified**
  `halftone_dev_lanes.md`) · **parity push executed** (`3e95533..9d22561 master → origin`, gitleaks clean) ·
  H2 gate ruled (plan approval) · decision #5 ruled (**derived artifact**).
- **H2 build — NEW `what/production/comic_render/`** (producer idiom; dep `adna-canvas-std` only; guarded
  self-bootstrap for the unpackaged `canvas_core`): `manifest.py` (v0.1 + `render_chain`) · `extract.py` ·
  `backends/{base,fake}` (+`RefineClient` additive protocol; pure-PNG fake, no PIL) · `dispatch.py` (chain
  executor; budget cap pre-enforced) · `select.py` (Schema-A only) · `writeback.py` (NEW-file; invariants
  asserted) · `validate.py` (stage-6 gate) · `compose.py` (R5 shim) · `cli.py` (`plan|dispatch|refine|select|
  write-back|validate|compose` + `run --until`) · `png_meta.py`/`vault.py` utils · AGENTS.md ·
  iii_quality_contract.md · README · own `.venv` · **72 tests + ruff clean**.
- **canvas_core hardening**: CV-FILE-PROPS-01 binary-target fix (media = existence-only; utf-8 crash on the
  fleet's first image file nodes) + 3 regression tests → **787/3**.
- **Amended exit executed**: visual-check on `mini_issue.rendered.canvas` (expected geometry classes only; NEW
  aspect-drift signal recorded for H3) + agent-confirmed render of the composited pages (mission-recorded).
- **Verification**: comic_render 72 · producers 236 · canvas_core 787/3 · canvas_std 115/10 · cert 11/11 ·
  firewall diff 0. Full E2E CLI proof incl. hybrid chain; idempotent re-runs; cross-directory reproducibility.

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
- **Deferred by design:** HR dispatch-side (awaits Bearly P5 evidence) · Home harness graduation
  (`canvas_visual_loop` → `canvas_core`, adoption-path step 2 — rule at H2/HR) · `html_renderer` file-node preview
  fix (static trap covers it) · `canvas_core` console-script packaging.

## Next Steps

1. **Operator**: the H3 gate + SPEND parameters + aspect-policy ruling (Resume-Here #1); registrar ack when it lands.
2. **H3** (on gate): `backends/gemini.py` (credential via the Home broker, names-only) → live render the
   mini-issue splash → operator eye-gate → the fleet's first real composited page. Luke leads the cloud lane
   (ratified annex); M-SB-D2 first-light spec is the preferred subject, Mondrian's mini-issue the fallback.
3. **H5** (parallel-eligible now): VisualDNA compose (`compose_input.py`; manifest `characters[]` is already in
   the v0.1 contract) — **LoRA-less exercised + tested** is the exit criterion; notify Bearly at close.
4. **HR** (own gate; parallel-eligible): `spec_canvas_review_surface.md` + the Meta Bind pilot over real images
   (ComfyUI SS variants; roadmap §6) + collector → Schema-A + III.
5. **HF** (own gate; sonnet-eligible): census + `how/federation/federation_index.md` (fold `comfyui/`) + staged
   refederation memos (roadmap §7).
6. **H4** (after H3 proves gemini): bind `RefineClient` to Vulcan's `comic_panel_refine`; prove the
   gemini→comfy chain once (the executor + protocol are ready).
7. **H6**: authoring contract · print E2E (spread compose lands here) · RLHF seam doc · `canvas_comic`
   disposition · campaign AAR.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
