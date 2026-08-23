---
campaign_id: campaign_canvas_blueprint
type: campaign
title: "Operation Blueprint — canvas as the fleet's diagrammatic-context substrate + the ComfyUI canvas seam"
owner: stanley
status: active
estimated_sessions: "6-10"
phase_count: 6
mission_count: "4 planned (created at phase-open)"
priority: high
executor_tier_default: fable
predecessor: campaign_canvas_halftone
created: 2026-08-22
updated: 2026-08-22
last_edited_by: agent_mondrian
status_history: "active (2026-08-22 — chartered as Session 2 of the operator-approved 3-session plan [plan approval 2026-08-22 = the charter gate]; name 'Blueprint' is the operator's to amend)"
tags: [campaign, canvas, blueprint, diagrammatic_context, dual_channel, federation, repin, comfyui, canvas_emission, interaction, rlhf_surface]
---

# Campaign: Operation Blueprint

> Named for the drawing that *is* the specification. Halftone proved the canvas as an **output**
> (real printed pages); Salon/Armature proved it as a **context object** and **interface surface**.
> Blueprint makes those proofs *fleet doctrine*: every key object, spec, or architecture in any
> graph can carry a conformant `.canvas` channel beside its prose — and ComfyUI-driven imagery is
> authored, reviewed, and tuned **through** canvas surfaces, not beside them.

## Goal

1. **Diagrammatic context as fleet doctrine.** Graduate the dual-channel pattern Emacs.aDNA
   independently ratified and has run for 13 months (REQ-Q01: prose + conformant `.canvas` for key
   artifacts, updated in the same mission; REQ-O05: canvas-sync review at gates; REQ-H05: canvas
   files are vault citizens) into an `aDNA.aDNA` pattern — reconciling the four authority models
   found in the wild (`view` / `generator` / dual-channel / none) and the two unreconciled canvas
   systems (the 2026-02 `canvas_yaml_interop` legacy in ~10 vaults + 196 template `.canvas` files
   vs the Standard at 2.3.0).
2. **The federation surface catches up.** 5 wrappers are 1–2 majors stale; 3 still named
   `canvasforge/`. A re-pin wave using VisualDNA's lockstep-flip mechanics brings every consumer
   to 2.3.0-current — the natural forcing function being the new doctrine they'll want.
3. **ComfyUI emits canvas objects.** The variant-selection board and the tuning surface become
   aDNA-Native canvases carrying the v2.2.0 `_reserved.interaction` overlay — Vulcan's SO-5
   human-gated selection gets a substrate, Canvas's HR pilot gets its second consumer, and the
   carried H4 live chain finally runs.

## Locked decisions (operator, at plan approval 2026-08-22)

| Decision | Choice |
|---|---|
| **Charter shape** | One successor campaign (Halftone closed first). This charter session also authors the two cross-session artifacts the plan names (the pattern draft → Rosetta; the emission spec → Vulcan/Session 3) — **plan approval was their gate**; all other phase work HOLDs. |
| **Schema posture** | **Default: no `canvas_std` change.** Emacs ships dual-channel on 2.3.0 unmodified; P1 assesses whether any gap truly needs a LIP-0010, and only a LIP (its own §7.7 gate) may touch the firewall. `git diff --stat -- what/code/canvas_std/` = 0 is a standing order otherwise. |
| **Corpus policy** | `adr_010` (gitignored / canonical on-node / backup-registered) governs all campaign artifacts. |
| **Memo GO** | Memos #9–#14 of the plan manifest are pre-authorized; per-phase deliveries still land only when their phase opens. |
| **Spend** | **Not granted.** The P4 live chain run requests its own authorization when reached. |

## Phases (human-gated; never auto-advance — SO-1)

| Phase | What | Gate |
|---|---|---|
| **P0** | Charter (this file) + the two charter artifacts: `artifacts/draft_pattern_diagrammatic_context.md` (staged → Rosetta, memo #9) · `what/specs/spec_comfyui_canvas_emission.md` (draft; memo #14 → Vulcan, feeds Session 3's restart-charter). | plan approval 2026-08-22 = the gate |
| **P1** | **Doctrine** (mission `b1` at open): finalize the pattern with Rosetta (their vault, their adoption); rule the legacy-interop reconciliation (proposal: interop spec becomes the `lattice` profile's derived-view rule under the Standard; template examples regenerate conformant at the next template release); re-point `idea_diagram_missions_herb` (already co-assigned to Mondrian) from rendered-figures to canvas-companions; LIP-0010 assessment (default: none needed). | HOLD |
| **P2** | **Authoring rail + dogfood** (mission `b2`): `how/skills/skill_canvas_context_diagram.md` (conformance = `canvas-std validate` + the Amendment-1 visual gate; topology doctrine v1.1 applies); Canvas's own architecture canvases authored dual-channel; conversion-offer memos #10 (Operations — 5 excellent standard-blind C08 canvases) + #11 (ScienceStanley — 29 bare files, wrapper-level fix). | HOLD |
| **P3** | **Federation re-pin wave** (mission `b3`): adopt VisualDNA lockstep-flip mechanics; rule `canvasforge/`→`canvas/` with Seshat (Obsidian spec §4 parked it); re-pin memos #12 to Astro · SuperLeague · ZenZachary · WebForge · Obsidian · Home — **verifying the "unanswered" 2026-08-04 memos at source first** (Estafette found fleet delivery defects; unanswered may mean undelivered); template-propagation memo #13 → Rosetta. | HOLD |
| **P4** | **ComfyUI canvas seam** (mission `b4`): implement Canvas's side of `spec_comfyui_canvas_emission` — the review-surface builder consuming ComfyUI variant runs (**the HR pilot's second consumer**); the tuning-surface affordance binding; **the carried H4 live chain** (`generate:gemini,refine:comfy@0.4/comic_panel_refine`) — **gated on ComfyUI standing (Session 3 venue = `adna_rd_l1` or L1 local) AND a fresh operator spend authorization**. | HOLD + spend gate |
| **P5** | Close: AAR rollup · federation_index refresh · STATE close · carried-tail disposition (`ImagenWiring` panel-path deprecation · `comic_book_design/` ruling). | HOLD |

## Firewall & discipline

- `what/code/canvas_std/` **untouched** unless a ratified LIP says otherwise; diff-0 verified at every gate.
- Cross-vault = coord memos or read-only (Rule 10). The pattern is *offered* to Rosetta, never written into `aDNA.aDNA`; conversions are *offered* to Operations/SS, never performed in their trees.
- Every canvas this campaign ships passes `canvas-std validate --level adna-native` + the agent-confirmed render.
- Per-mission AAR (SO-5) · pushes operator-gated batches · missions created at phase-open, never pre-spawned past a HOLD.

## Risk register

| # | Risk | Posture |
|---|---|---|
| R1 | **Wrapper-drift regression** — a re-pin wave breaks a consumer mid-flip. | Lockstep-flip only (pin + conformance state advance together); 5-stage §3 re-validation for 1.x→2.x hops. |
| R2 | **LIP scope creep** — doctrine work leaks into schema change. | Default no-change locked; only a LIP through its own gate touches the firewall. |
| R3 | **Delivery-defect false negatives** — treating undelivered 2026-08-04 memos as refusals. | Verify at source before any escalation (Estafette F-STAGE-03 precedent). |
| R4 | **ComfyUI venue dependency** — P4's live work waits on Session 3's unstall + `adna_rd_l1` standup. | P4's build half (board builder, spec conformance) is venue-independent; only the live chain waits. |
| R5 | **No production LoRA weight** (Vulcan F-M04-B, Canvas-corroborated). | Non-blocking by design: the refine chain runs LoRA-less; LoRA re-enters via `characters[]` when a weight flips TRAINED. |
| R6 | **Doctrine without adopters** — a pattern nobody converts to. | Emacs is the existing empirical anchor; Operations/SS conversions are offered with the work done for them; the template channel ships it to every new vault. |

## Missions index (created at phase-open)

| Mission | Phase | Status |
|---|---|---|
| `mission_b1_doctrine` | P1 | planned |
| `mission_b2_authoring_rail` | P2 | planned |
| `mission_b3_repin_wave` | P3 | planned |
| `mission_b4_comfyui_seam` | P4 | planned |

## Provenance

Chartered from the 2026-08-22 three-vault review sweep (Canvas · ComfyUI · fleet), which found:
dual-channel already ratified + running in Emacs.aDNA; 145 real `.canvas` files across 18 vaults
with bimodal conformance (Operations 10 / ScienceStanley 29 / Regenesis 11 standard-blind); the
2026-02 lattice-interop legacy never reconciled with the Standard; ComfyUI's four pre-declared
canvas attachment points (`canvas_json` media type · lattice↔canvas tooling · "contact sheet /
Canvas surface" doctrine · the `lattice_variant_selection` scaffold). Plan:
`~/.claude/plans/please-read-the-claude-md-serene-spark.md`. Predecessor close:
`campaign_canvas_halftone/` §Completion Summary.
