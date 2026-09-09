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
updated: 2026-09-08
last_edited_by: agent_mondrian
status_history: "active (2026-08-22 — chartered as Session 2 of the operator-approved 3-session plan [plan approval 2026-08-22 = the charter gate]; name 'Blueprint' is the operator's to amend) · P1 Canvas-owned half shipped 2026-08-24 (mission_b1_doctrine completed complete-with-open-item; b1.5 open pending Rosetta) · P2 rail + dogfood shipped 2026-09-04 (complete-with-open-item; #10/#11 deferred) · P2c producer re-gate added 2026-09-07 as a dated scope amendment (plan approval = the gate) · P2c producer re-gate shipped 2026-09-07 (13 authored surfaces gate clean; layout_fit; deck profile; advisory-trap rule) · P2b conversion offers shipped 2026-09-07 (census re-derived 5→10 and 29→33; one defect class across both vaults = F-HR-1; `conform.py`; memos #10/#11 delivered; `_reserved` tier held on b1.5) · P3 federation re-pin wave shipped 2026-09-08 (census re-derived: 15 wrapper vaults not 14, 10 wrapper-less emitters never enumerated, 6 pin spellings; F-HR-1 collector wiring built; index corrected in both directions; 8 of 9 memos delivered) · P4 build half shipped 2026-09-08 (run_manifest + variant_board + tuning_surface on fixture manifests; the capture instrument ported and the 4x-carried Amendment-1 render gate MET for the first time; live chain still spend-gated) → ▶ P5, HOLD"
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
| **P1** | **Doctrine** (`mission_b1_doctrine`): ✅ **Canvas-owned half SHIPPED 2026-08-24** — census/diagnosis **erratum v2** → Rosetta (the legacy is not bare: 196/196 carry the `view` quartet at the non-canonical `metadata._reserved`; migration **verified** 4/4 → `adna_native [OK]`) · **`adr_011`** rules the reconciliation (`proposed`, §7.7 pending) · **LIP-0010 assessment** — `authority` is normative-but-unvalidated (0/21); Option B recommended, **deferred** on Rosetta's ruling; **no schema change taken** · `--level adna_native` CLI defect fixed. `idea_diagram_missions_herb` re-point already offered inside the draft (Rule 10 — nothing further is Canvas's). | ✅ **complete-with-open-item** — **b1.5 (finalize with Rosetta) OPEN** |
| **P2** | **Authoring rail + dogfood** (mission `b2`): ✅ **rail + dogfood SHIPPED 2026-09-04** — `skill_canvas_context_diagram.md` + Canvas's **first two** dual-channel canvases (the vault shipped zero until now) + a producer-side `authority` passthrough with the only enum check that exists anywhere (F-B1-2). **Building the pattern broke it twice** → erratum **E2** (authority axis mixes meaning-ownership with production-mode; the conformance floor was **unsatisfiable for any knowledge-canvas-profile canvas with a titled group, ~1 month** *(corrected 2026-09-06 → F-P2-6: was "by any canvas for 13 months"; the two traps cannot conflict before `cv_lead_cost_01` was added 2026-08-03, and comic-profile canvases always cleared it)* — two shipped traps contradict, and `diagram_generator`'s own example had been failing since Atelier at ~14% shown). Generator repaired; all three canvases now `--strict` clean. ⛔ **Conversion memos #10/#11 DEFERRED** to a second P2 session (operator ruling at the gate). | ✅ **complete-with-open-item** — E2 **delivery refused** (aDNA.aDNA live lease, no drop-box); dogfood `visual_gate: pending` on Amendment 1 |
| **P2c** | **Producer re-gate** (mission `b2c`) — *added 2026-09-07 as a dated scope amendment, plan approval = the gate.* Discharges `mission_b2`'s follow-up (a), which its own AAR sequenced **ahead of** the P2b conversion memos: 99 findings / 13 HIGH over **7** files / 5 producers, 90% of them the four classes already solved once in `diagram_generator`. Fixed **once** as a shared `canvas_core/layout_fit.py` over the `text_metrics` functions the traps themselves call — producer and trap stop guessing separately. Also: a `deck` profile ruling (8 of deck's 19 are knowledge-board aesthetics a 16:9 slide fails by design — the `comic` precedent), the 3 missing example assets (HIGH, and Canvas is publicly clonable), and F-P2-9 (`CV-LEAD-COST-01`'s fix hint recommends a lead that trips `CV-HIERARCHY-01`). | ✅ **complete-with-open-item** — 13 authored surfaces gate clean per domain profile; Amendment-1 render still carried |
| **P2b** | **Conversion offers** (mission `b2b`) — the deferred half of P2, opened 2026-09-07 once P2c had made our own shelf pass the gate the offers ask others to adopt. **The census re-derived and both figures were wrong:** Operations **10** files not 5 (two copies; the *projection* is the failing one, and it is gitignored by its owner), ScienceStanley **33** not 29 **in three classes** — of which **9 are Canvas's own output** from the `canvas_comic` producer we archived (F-P2b-3). **40 of the 41 conformance errors across both vaults are one class** (C-4, missing explicit `toEnd`) — the **F-HR-1** Obsidian-re-save signature Canvas diagnosed in its own vault on 2026-08-23 and had carried as internal housekeeping ever since (F-P2b-2). Shipped `canvas_core/conform.py` (+13 tests): `normalize_edges` clears 40/41 mechanically (7 of 8 files → `extended [OK]`), `unresolved_edges` **reports and never repairs** the one real defect (a C-3 dangling edge live in a shipped teaching package). Memos #10/#11 delivered with worked measurements, both vaults read-only throughout. ⛔ The `_reserved` tier of both offers is **held**: no `authority` value fits a hand-authored canvas (F-P2b-5 — I nearly shipped `view`, which is wrong and which `canvas_std` accepts silently). | ✅ **complete-with-open-item** — `_reserved` tier held on `b1.5`; F-HR-1 collector wiring scoped, not built |
| **P3** | **Federation re-pin wave** (mission `b3`): ✅ **SHIPPED 2026-09-08** — and the charter row below was wrong in three of its four clauses, which the phase found by re-deriving rather than reading. **"5 stale"** → **9** materially stale of 15; **"3 misnamed"** ✅ held (the only figure that did); **"memos to 6 vaults"** → the real ask was larger and differently shaped; **"adopt VisualDNA lockstep-flip mechanics"** → ⛔ **`skill_lockstep_flip` was never built** (VisualDNA P4 authored 3 of 8 skills and is still a stub) — **operator-ruled: dropped as a dead referent**, replaced by our own `spec_federation_contract` §3, ours since Keystone. Unstated by the charter and found by measurement: a **15th consumer** (WGS, adopted 2026-08-10, never indexed) · the **G7 gap already closed five weeks earlier** (Oration adopted the day we asked; their reply sat `staged_unsent` in their outbox for 34 days and contained the finding we later rediscovered as F-P2-9 at full cost) · **10 wrapper-less canvas emitters / 49 files** never enumerated, the population the index was structurally unable to see · **six spellings of the pin field**, the structural reason the index drifted silently. Delivered: **8 of 9 memos** (#13 → Rosetta **staged**, live lease, no drop-box). Also shipped: `spec_federation_contract` **§2.1a** (on Kennedy's finding, which had cost them a reversed ruling) and the **F-HR-1 collector wiring** (`canvas_core` 951→958/3). | ✅ **complete-with-open-item** — #13 staged; Seshat's rename ruling `ack_required`; Amendment-1 render carried a 4th time |
| **P4** | **ComfyUI canvas seam** (mission `b4`): ✅ **BUILD HALF SHIPPED 2026-09-08** — `run_manifest.py` (spec §3, five executable fixtures that now *are* the contract ComfyUI's emitter must satisfy) · `variant_board.py` (§1.1, one `choice` **per slot** = Vulcan's SO-5 gate with a substrate; the HR pilot's second consumer and the first surface that can emit through the S-4 gate) · `tuning_surface.py` (§1.2, `input` knobs + one `re_render` action producing a **D1 request record**, with a test that fails if any transport is ever imported). Collector extended for `selection_sidecar` — the plan's *"no new collector needed"* was wrong, and a slot-keyed reject would have appended cleanly to the canvas and reached **no sink**. ⭐ **Objective 0 was the finding**: the Amendment-1 render, carried unmet **four times**, was blocked by a claim that was false when written (**F-P4-1** — a constraint on *whole-screen* capture inherited as a constraint on *capture*). Home's window-scoped instrument, whose own docstring named **this vault** as its D-A destination since 2026-06-02, ported in and credited. Sight then paid for itself immediately: **F-P4-3** (both dogfood canvases render their mermaid channel as raw source behind an un-actioned trust prompt — both machine checks green) and **F-P4-2** (Obsidian **culls node text below a zoom threshold**, so a pin-sharp 3128×1896 capture can contain no readable text at all). ⛩ **F-P4-4** — and a false positive found by sight, "fixed" twice, each fix making the board worse, caught only by re-rendering after the fix. ⛔ **The H4 live chain did NOT run** — spend deliberately not requested (their emitter does not exist; the fixtures prove more than one hand-written manifest would). | ✅ **complete-with-open-item** — live chain still spend-gated; mermaid trust grant is the operator's |
| **P5** | Close: AAR rollup · federation_index refresh · STATE close · carried-tail disposition (`ImagenWiring` panel-path deprecation · `comic_book_design/` ruling). | HOLD |

## Firewall & discipline

- `what/code/canvas_std/` **untouched** unless a ratified LIP says otherwise; diff-0 verified at every gate.
- Cross-vault = coord memos or read-only (Rule 10). The pattern is *offered* to Rosetta, never written into `aDNA.aDNA`; conversions are *offered* to Operations/SS, never performed in their trees.
- Every canvas this campaign ships passes `canvas-std validate --level adna_native` + the agent-confirmed render.
  *(The value is underscored — the CLI rejects `adna-native`; corrected at P1, `mission_b1_doctrine` b1.4.)*
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
| `mission_b1_doctrine` | P1 | ✅ completed (2026-08-24) — complete-with-open-item (b1.5) |
| `mission_b2_authoring_rail` | P2 | ✅ completed (2026-09-04) — complete-with-open-item (E2 delivery refused; `visual_gate: pending`) |
| `mission_b2c_producer_regate` | P2c | ✅ completed (2026-09-07) — complete-with-open-item (Amendment-1 render carried; CV-AUDIENCE-01 calibration deferred) |
| `mission_b2b_conversion_offers` | P2b | ✅ completed (2026-09-07) — complete-with-open-item (`_reserved` tier held on `b1.5`; F-HR-1 collector wiring scoped) |
| `mission_b3_repin_wave` | P3 | ✅ completed (2026-09-08) — complete-with-open-item (#13 staged; Seshat ack; render carried) |
| `mission_b4_comfyui_seam` | P4 | ✅ completed (2026-09-08) — complete-with-open-item (**build half**; live chain held at the spend gate; mermaid trust grant is the operator's) |

## Provenance

Chartered from the 2026-08-22 three-vault review sweep (Canvas · ComfyUI · fleet), which found:
dual-channel already ratified + running in Emacs.aDNA; 145 real `.canvas` files across 18 vaults
with bimodal conformance (Operations 10 / ScienceStanley 29 / Regenesis 11 standard-blind); the
2026-02 lattice-interop legacy never reconciled with the Standard *(P1 measurement refined this: the
196 template files across 46 vaults are **not** bare — they carry the `view` quartet at the
non-canonical `metadata._reserved`; erratum E1 in the draft, ruled in `adr_011`)*; ComfyUI's four pre-declared
canvas attachment points (`canvas_json` media type · lattice↔canvas tooling · "contact sheet /
Canvas surface" doctrine · the `lattice_variant_selection` scaffold). Plan:
`~/.claude/plans/please-read-the-claude-md-serene-spark.md`. Predecessor close:
`campaign_canvas_halftone/` §Completion Summary.
