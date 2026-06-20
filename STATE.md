---
type: state
created: 2026-06-06
updated: 2026-06-19
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260619_170825_keystone_e4_open_consumer
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Operation Cartography (genesis planning) CLOSED 2026-06-13 ✅. Now in EXECUTION — Operation Keystone ACTIVE; PHASES E0+E1+E2 ✅ (reference impl + tooling) + PHASE E3 ✅ COMPLETE 2026-06-14 (CanvasForge migrated onto `canvas_std`, parity-gated). 🔓 **PHASE E4 OPENED 2026-06-19** (operator-authorized E3→E4 gate crossing) + reconciled to in-vault production (pt09); **E4.3 ✅ DONE** — first net-new consumer built + green. ⛔ Now HELD at the E4→E5 boundary (human gate).**
`how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md`

Operation Cartography (P0–P5) ratified the **aDNA Canvas Standard v2.0.0** + contracts + build charter, then **closed at the operator gate**. The operator **activated Operation Keystone** (the build). **E0** (skeleton + KEEP floor + golden fixtures) · **E1** (reference engine) · **E2** (conformance harness + v2.0.0 **JSON Schema** + the **`canvas-std` CLI**) built the reference implementation (`pytest` 46/8, `ruff` clean). **E3** (parity-gated CanvasForge migration) is now **COMPLETE** — E3.1 `canvas/` wrapper + E3.2 constants-only `canvas_core`→`canvas_std` deprecation shim + E3.3 parity gate (**GREEN**) + **E3.4 full cutover (2026-06-14)**: CanvasForge single-sources the Standard from Canvas.aDNA v2.0.0; the embedded v1.0.0 framing is superseded; the shim stays through its grace window (removal at E6.2). **🔓 E4 OPENED 2026-06-19** (operator-authorized E3→E4 crossing) — table reconciled to in-vault production; **E4.3 (first net-new consumer) ✅ built + green**; **⛔ now HELD at the E4→E5 phase gate (human gate).** *(Planning history: `campaign_canvas_genesis_planning/`.)*

> **⊕ pt09 (Production Tidy, 2026-06-17) — CanvasForge absorbed into Canvas.** `CanvasForge.aDNA` merged in (reverses E3.4); **Hermes merged into Mondrian**; Canvas now owns Standard **+** production (deck/comic/diagram) at `what/production/`. **Governance merge only** — code (`canvas_core`/`canvas_comic`/`canvas_presentation`) + ~8 consumer wrappers relocate/refederate at PT **P5** (shim-covered interim; `canvas_core→canvas_std` shim folds into the merge, Home §C #29). **Keystone reshape:** the "CanvasForge as a *separate* federated producer" premise is folded — **Mondrian reconciles the E4 phase plan** (net-new consumer + LF-successor now in-vault) at its next Keystone session; no gate auto-advances. Memo: `Home.aDNA/how/campaigns/campaign_production_tidy/coordination_drafts/coord_draft_hestia_to_mondrian_hermes_canvasforge_merge.md`. Archived source: `Archive.aDNA/CanvasForge.aDNA/`. **[2026-06-19] E4 code-layout reconciliation resolved on paper** — [[what/decisions/adr_004_production_code_layout|ADR-004]] (proposed) pins `canvas_core` → `what/production/canvas_core/` (import unchanged; env `CANVAS_CORE_HOME`; `canvas_std` resolves via installed `adna-canvas-std`), **answering Hestia's substrate-path memo → Hearthstone P3 unblocked** (reply: `who/coordination/coord_2026_06_19_mondrian_to_hestia_canvas_substrate_path_reply.md`), and folding the 2 parked follow-ups into the P5 relocation contract. **E3→E4 stays HELD; no code moves; operator ratifies adr_004.** **Loop closed (2026-06-19):** Hestia actioned same-day — exemplar **staged** (fallthrough resolver auto-flips at P5) + acked; Home §C **#39** env-var alias (`CANVASFORGE_CODE`→`CANVAS_CORE_HOME`) registered. **Forward-ref → ping Hestia when the PT P5 relocation is scheduled** (she re-verifies + drops the interim archive branch). *Wind-down housekeeping: MANIFEST de-drifted to Keystone-current; lightweight AAR filed on the session; campaign log + adr_004 P5-checklist updated.*

## ▶ Resume Here — 🔓 Phase E4 OPENED; E4.3 DONE; ⛔ HELD at E4→E5 (human gate)

**Phase E4 is OPEN (2026-06-19, operator-authorized E3→E4 crossing) and E4.3 is DONE.** (E0–E2 reference impl + E3
CanvasForge cutover are complete history; the `canvas_core` shim stays live to the E-D2 window 2027-06-13, retired at
E6.2.) At the gate crossing the **E4/E5 table was reconciled to in-vault production** (pt09 folded the
*federated-producer* premise): E4.1/E4.2 (LF-successor) reframed *federated→in-vault* + **⚠ flagged for a governed D3
touch** (`adr_002` ratified a *federated* pipeline; needs an amendment / new ADR via the `adr_003` LIP **before**
E4.1/E4.2 build); E4.4 step-4 render is **PT-P5-gated**; E5.2 names corrected (ComfyForge→ComfyUI, SiteForge→Astro).

**E4.3 — first net-new consumer, BUILT + GREEN.** `what/production/brief_consumer/` — a reference "brief" consumer
that maps a structured one-page brief → a v2.0.0 **aDNA-Native** `.canvas`, proven end-to-end on **`canvas_std` alone**
(zero PT-P5 dependency): `pytest` **10/10**, `ruff` clean; `canvas-std validate` → `level_reached=adna_native [OK]`,
degradation D-1/D-2/D-3 all True; the self-referential dog-food artifact (`examples/canvas_standard_brief.canvas`, 14
nodes/12 edges) regenerates deterministically; **`canvas_std`'s own suite still 46/8** (consumer is additive). It is
the **first `what/production/` resident**, exercising the ADR-004 §4 `adna-canvas-std` dependency contract before the
P5 `canvas_core` relocation. Mission: [[how/campaigns/campaign_canvas_genesis/missions/mission_e4_3_net_new_consumer|mission_e4_3]].

**Next: ⛔ E4→E5 is a PHASE gate (human gate) — do NOT auto-advance.** Remaining E4 threads (all HELD): E4.1/E4.2
(LF-successor in-vault — **gated on the D3 governed touch**); E4.4 (deck pilot — steps 1–3 on `canvas_std`; step-4
render PT-P5-gated). After E4: E5 (federation rollout + `iii/` wiring + registry) · E6 (cross-system parity + shim
retirement E6.2 + campaign AAR E6.3). Chartered:
[[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] §Phases E4–E6.

**Open follow-ups → now contracted as PT P5 items in [[what/decisions/adr_004_production_code_layout|ADR-004]]**
(both partially OBE post-pt09; folded into the P5 relocation contract 2026-06-19, no gate change): (1) **FU1 —
canvas/-routing Standing Order**, reframed as Canvas *production* governance (route `what/production/` standard-
consumption through `canvas/`, mirroring `iii/`) at the P5 refederation — **not** an edit to the archived
"do-not-resume" CanvasForge `CLAUDE.md`. (2) **FU2 — round-trip-function dedup** (validate/diff/merge/round-trip →
`canvas_std`) at `canvas_core` relocation (once co-located with `canvas_std`), gated by `e3_3_parity_check.py`
(baseline `3ce4d341` unchanged).

**Build hygiene:** the CanvasForge suite runs in the gitignored `.venv` at `CanvasForge.aDNA/what/code/`
(`adna-canvas-std` editable; `.venv/bin/python -m pytest canvas_core/tests/ canvas_comic/tests/ tests/test_federation_validation.py -q` → 900/3). Canvas.aDNA's own `canvas_std` suite: `.venv` at `what/code/canvas_std` (46/8). **E4.3 `brief_consumer` suite: gitignored `.venv` at `what/production/brief_consumer/` (`adna-canvas-std` + `brief-consumer` editable; `.venv/bin/python -m pytest -q` → 10/10; `.venv/bin/ruff check .` clean).** Tracking: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active).

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]); III/SiteForge upstream notes; III pin confirm at E5.1.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds E4.4 as a worked build; informs D2/D4/D7. Opens no phase, builds no code until E4.

## What's Done (this session — Keystone E4 open + E4.3 build, 2026-06-19 PM)

- **🔓 Phase E4 OPENED** (operator-authorized E3→E4 crossing) + **E4/E5 table reconciled** to in-vault production (pt09): campaign doc carries the "PHASE E4 OPENED" note (E4.1/E4.2 federated→in-vault + **D3 governance flag**; E4.4 step-4 PT-P5-gated; E5.2 ComfyForge→ComfyUI / SiteForge→Astro). D3 reshape flagged in the Decision Points table.
- **Charter (SO-3):** `mission_e4_3_net_new_consumer.md` (full) + thin stubs `mission_e4_1_lf_successor` / `mission_e4_2_lf_contracts` (⛔ gated on the D3 touch) / `mission_e4_4_deck_pilot`.
- **E4.3 BUILT + GREEN** — `what/production/brief_consumer/` (the first `what/production/` resident): `model`+`layout`+`consume` (BriefInput → `canvas_std` source contract → `to_canvas` → `_reserved` enriched to aDNA-Native) + `brief-consumer` CLI + self-referential dog-food example. **Proof:** `pytest` 10/10 · `ruff` clean · `canvas-std validate` → `adna_native [OK]` + D-1/D-2/D-3 True · deterministic 14-node/12-edge artifact · `canvas_std` suite still **46/8** (additive). Depends on installed `adna-canvas-std` (ADR-004 §4) — de-risks the P5 relocation.
- *(Prior: Cartography closed; Keystone E0+E1+E2 reference impl 46/8; E3.1–E3.4 CanvasForge cutover; 2026-06-19 AM substrate-path adr_004.)*

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip) — **superseded 2026-06-14 (E3.4)**: now carries supersession banners → Canvas.aDNA v2.0.0. Invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for the E3.2 shim).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3) — feeds E4.

## Active Blockers

- **None blocking E4.3** (done + green). **E4→E5 is now the human gate** — do not auto-advance. Two E4 threads are HELD: **E4.1/E4.2 (LF-successor) are gated on a D3 governed touch** (`adr_002` ratified a *federated* pipeline; pt09 made it in-vault — needs an amendment / new ADR via the `adr_003` LIP before build); **E4.4 step-4 render is PT-P5-gated** (`canvas_presentation` lands at P5).
- **ADR-004 still awaits operator ratification** (proposed → ratified + `signed_by`) — prepared, operator's countersign (orthogonal to E4.3, which needs only `canvas_std`).
- **Pushes:** prior batches (E3.4 + 2026-06-19 AM substrate-path) are **already pushed** (origin/master up to date). The **E4 batch** (campaign + 4 missions + STATE + session + the `brief_consumer/` package + generated `.canvas`) is committed locally and **pending push per the operator batch convention** — confirm before pushing; check `@{u}..HEAD` authorship.

## Next Steps

1. ✅ Cartography CLOSED + Keystone E0–E2 (reference impl 46/8) + E3.1–E3.4 cutover.
2. ✅ **E4 OPENED + E4.3 DONE 2026-06-19** — gate crossing + table reconciliation; `brief_consumer` built + green (10/10; `adna_native [OK]`; no regression).
3. **→ ⛔ E4→E5 PHASE GATE (human gate).** Do not auto-advance. Remaining E4 (all HELD): **E4.1/E4.2** (gated on the **D3 governed touch** — `adr_002` amendment / new ADR via `adr_003` LIP); **E4.4** deck pilot (steps 1–3 on `canvas_std`; step-4 render PT-P5-gated).
4. **ADR-004 awaits operator ratification** (proposed → ratified + `signed_by`) — prepared; say the word and I flip it. The two FU items (FU1 canvas/-routing; FU2 round-trip dedup) stay contracted PT P5 items.
5. **Pushes:** the **E4 batch** (campaign + 4 missions + STATE + session + `brief_consumer/` + generated `.canvas`) is committed locally, **pending push per the operator batch convention** (prior batches already pushed).
6. **PT P5 watch:** ping Hestia when the `canvas_core` relocation is scheduled (she re-verifies + drops the interim archive branch). A **new `what/production/` resident** (`brief_consumer/`) now exists ahead of P5 — courtesy heads-up to Hestia (no collision; new package).

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
