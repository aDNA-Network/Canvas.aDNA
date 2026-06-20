---
type: state
created: 2026-06-06
updated: 2026-06-19
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260619_174121_keystone_e4_4_deck_generator
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Operation Cartography (genesis planning) CLOSED 2026-06-13 ✅. Now in EXECUTION — Operation Keystone ACTIVE; PHASES E0+E1+E2 ✅ (reference impl + tooling) + PHASE E3 ✅ COMPLETE 2026-06-14 (CanvasForge migrated onto `canvas_std`, parity-gated). 🔓 **PHASE E4 OPENED 2026-06-19** (operator-authorized E3→E4 gate crossing) + reconciled to in-vault production (pt09); **E4.3 ✅ + E4.4 ✅ DONE** — two net-new consumers (`brief_consumer` + `deck_generator`) built + green on `canvas_std`. ⛔ Now HELD at the E4→E5 boundary (human gate); E4.1/E4.2 gated on a D3 governed touch.**
`how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md`

Operation Cartography (P0–P5) ratified the **aDNA Canvas Standard v2.0.0** + contracts + build charter, then **closed at the operator gate**. The operator **activated Operation Keystone** (the build). **E0** (skeleton + KEEP floor + golden fixtures) · **E1** (reference engine) · **E2** (conformance harness + v2.0.0 **JSON Schema** + the **`canvas-std` CLI**) built the reference implementation (`pytest` 46/8, `ruff` clean). **E3** (parity-gated CanvasForge migration) is now **COMPLETE** — E3.1 `canvas/` wrapper + E3.2 constants-only `canvas_core`→`canvas_std` deprecation shim + E3.3 parity gate (**GREEN**) + **E3.4 full cutover (2026-06-14)**: CanvasForge single-sources the Standard from Canvas.aDNA v2.0.0; the embedded v1.0.0 framing is superseded; the shim stays through its grace window (removal at E6.2). **🔓 E4 OPENED 2026-06-19** (operator-authorized E3→E4 crossing) — table reconciled to in-vault production; **E4.3 + E4.4 ✅ built + green** (`brief_consumer` + `deck_generator` on `canvas_std`); **⛔ now HELD at the E4→E5 phase gate (human gate).** *(Planning history: `campaign_canvas_genesis_planning/`.)*

> **⊕ pt09 (Production Tidy, 2026-06-17) — CanvasForge absorbed into Canvas.** `CanvasForge.aDNA` merged in (reverses E3.4); **Hermes merged into Mondrian**; Canvas now owns Standard **+** production (deck/comic/diagram) at `what/production/`. **Governance merge only** — code (`canvas_core`/`canvas_comic`/`canvas_presentation`) + ~8 consumer wrappers relocate/refederate at PT **P5** (shim-covered interim; `canvas_core→canvas_std` shim folds into the merge, Home §C #29). **Keystone reshape:** the "CanvasForge as a *separate* federated producer" premise is folded — **Mondrian reconciles the E4 phase plan** (net-new consumer + LF-successor now in-vault) at its next Keystone session; no gate auto-advances. Memo: `Home.aDNA/how/campaigns/campaign_production_tidy/coordination_drafts/coord_draft_hestia_to_mondrian_hermes_canvasforge_merge.md`. Archived source: `Archive.aDNA/CanvasForge.aDNA/`. **[2026-06-19] E4 code-layout reconciliation resolved on paper** — [[what/decisions/adr_004_production_code_layout|ADR-004]] (proposed) pins `canvas_core` → `what/production/canvas_core/` (import unchanged; env `CANVAS_CORE_HOME`; `canvas_std` resolves via installed `adna-canvas-std`), **answering Hestia's substrate-path memo → Hearthstone P3 unblocked** (reply: `who/coordination/coord_2026_06_19_mondrian_to_hestia_canvas_substrate_path_reply.md`), and folding the 2 parked follow-ups into the P5 relocation contract. **E3→E4 stays HELD; no code moves; operator ratifies adr_004.** **Loop closed (2026-06-19):** Hestia actioned same-day — exemplar **staged** (fallthrough resolver auto-flips at P5) + acked; Home §C **#39** env-var alias (`CANVASFORGE_CODE`→`CANVAS_CORE_HOME`) registered. **Forward-ref → ping Hestia when the PT P5 relocation is scheduled** (she re-verifies + drops the interim archive branch). *Wind-down housekeeping: MANIFEST de-drifted to Keystone-current; lightweight AAR filed on the session; campaign log + adr_004 P5-checklist updated.*

## ▶ Resume Here — 🔓 Phase E4 OPENED; E4.3 + E4.4 DONE; ⛔ HELD at E4→E5 (human gate)

**Phase E4 is OPEN (2026-06-19, operator-authorized E3→E4 crossing); E4.3 + E4.4 are DONE.** (E0–E2 reference impl + E3
CanvasForge cutover are complete history; the `canvas_core` shim stays live to the E-D2 window 2027-06-13, retired at
E6.2.) At the gate crossing the **E4/E5 table was reconciled to in-vault production** (pt09 folded the
*federated-producer* premise): E4.1/E4.2 (LF-successor) reframed *federated→in-vault* + **⚠ flagged for a governed D3
touch** (`adr_002` ratified a *federated* pipeline; needs an amendment / new ADR via the `adr_003` LIP **before**
E4.1/E4.2 build); E4.4 step-4 render is **PT-P5-gated**; E5.2 names corrected (ComfyForge→ComfyUI, SiteForge→Astro).

**E4.3 + E4.4 — two net-new consumers, BUILT + GREEN, on `canvas_std` alone (zero PT-P5 dependency):**
- **E4.3 `what/production/brief_consumer/`** — single-page brief → aDNA-Native `.canvas`; `pytest` **10/10**;
  deterministic 14-node artifact. The **first `what/production/` resident** (exercises the ADR-004 §4
  `adna-canvas-std` dependency contract → de-risks the P5 relocation).
  Mission: [[how/campaigns/campaign_canvas_genesis/missions/mission_e4_3_net_new_consumer|mission_e4_3]].
- **E4.4 `what/production/deck_generator/`** — multi-slide deck → aDNA-Native `.canvas` (slides = group nodes;
  `deck_root` = the one canonical surface; `sequence` chain; **image + table** components; `isStartNode`); `pytest`
  **16/16**; deterministic 6-slide/21-node artifact. Persona-III + accuracy method captured as a contract
  (`deck_generator/iii_quality_contract.md`, wired at E5.1).
  Mission: [[how/campaigns/campaign_canvas_genesis/missions/mission_e4_4_deck_pilot|mission_e4_4]].
- Both: `ruff` clean · `canvas-std validate` `adna_native [OK]` + D-1/D-2/D-3. **`canvas_std` itself unchanged (46/8).**

**Next: ⛔ E4→E5 is a PHASE gate (human gate) — do NOT auto-advance.** Remaining E4 = **E4.1/E4.2** (LF-successor
in-vault) — **⛔ gated on the D3 governed touch** (`adr_002` amendment / new ADR via the `adr_003` LIP). After E4: E5
(federation rollout + `iii/` wiring + registry) · E6 (cross-system parity + shim retirement E6.2 + campaign AAR E6.3).
Chartered: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] §Phases E4–E6.

**Open follow-ups → now contracted as PT P5 items in [[what/decisions/adr_004_production_code_layout|ADR-004]]**
(both partially OBE post-pt09; folded into the P5 relocation contract 2026-06-19, no gate change): (1) **FU1 —
canvas/-routing Standing Order**, reframed as Canvas *production* governance (route `what/production/` standard-
consumption through `canvas/`, mirroring `iii/`) at the P5 refederation — **not** an edit to the archived
"do-not-resume" CanvasForge `CLAUDE.md`. (2) **FU2 — round-trip-function dedup** (validate/diff/merge/round-trip →
`canvas_std`) at `canvas_core` relocation (once co-located with `canvas_std`), gated by `e3_3_parity_check.py`
(baseline `3ce4d341` unchanged).

**Build hygiene:** the CanvasForge suite runs in the gitignored `.venv` at `CanvasForge.aDNA/what/code/`
(`adna-canvas-std` editable; `.venv/bin/python -m pytest canvas_core/tests/ canvas_comic/tests/ tests/test_federation_validation.py -q` → 900/3). Canvas.aDNA's own `canvas_std` suite: `.venv` at `what/code/canvas_std` (46/8). **E4 consumer suites (gitignored `.venv` per package, `adna-canvas-std` editable): `what/production/brief_consumer/` → 10/10; `what/production/deck_generator/` → 16/16; both `ruff` clean.** Tracking: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active).

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]); III/SiteForge upstream notes; III pin confirm at E5.1.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds E4.4 as a worked build; informs D2/D4/D7. Opens no phase, builds no code until E4.

## What's Done (this session — Keystone E4.4 deck generator, 2026-06-19 evening)

- **Step 0:** pushed the E4.3 batch (`b0388a3` → origin/master) per the operator batch convention.
- **E4.4 BUILT + GREEN** — `what/production/deck_generator/` (second `what/production/` resident): `model`+`slides`+`layout`+`consume` (DeckInput → `canvas_std` source contract → `to_canvas` → `_reserved` aDNA-Native) + `deck-generator` CLI + self-referential 6-slide example + `iii_quality_contract.md`. **Extends E4.3:** slides = group nodes, `deck_root` = the one canonical surface (A-5), `sequence` chain (acyclic), `isStartNode`, and the **image + table** component classes the brief didn't exercise. **Proof:** `pytest` 16/16 · `ruff` clean · `canvas-std validate` `adna_native [OK]` + D-1/D-2/D-3 · deterministic 6-slide/21-node artifact · no regression (`canvas_std` 46/8, `brief_consumer` 10/10).
- **Governance:** promoted `mission_e4_4_deck_pilot` (stub → full + completed + AAR); campaign-doc E4 table — E4.3 + E4.4 marked done, E4.1/E4.2 ⛔ D3-gated; phase-progress note added.
- *(Prior: Cartography closed; Keystone E0–E2 (46/8); E3.1–E3.4 cutover; 2026-06-19 AM substrate-path adr_004; PM E4 open + E4.3 `brief_consumer`.)*

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip) — **superseded 2026-06-14 (E3.4)**: now carries supersession banners → Canvas.aDNA v2.0.0. Invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for the E3.2 shim).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3) — feeds E4.

## Active Blockers

- **None blocking E4.3/E4.4** (both done + green). **E4→E5 is the human gate** — do not auto-advance. Remaining E4 = **E4.1/E4.2 (LF-successor), ⛔ gated on a D3 governed touch** (`adr_002` ratified a *federated* pipeline; pt09 made it in-vault — needs an amendment / new ADR via the `adr_003` LIP before build). *(E4.4's step-4 render loop is PT-P5-gated but E4.4 itself is DONE — it ships a conformant deck object, not pixels.)*
- **ADR-004 still awaits operator ratification** (proposed → ratified + `signed_by`) — prepared, operator's countersign (orthogonal to the consumers, which need only `canvas_std`).
- **Pushes:** the E4.3 batch (`b0388a3`) is **pushed** (origin/master). The **E4.4 batch** (`deck_generator/` package + example `.canvas` + mission + campaign + STATE + session) is committed locally; per the operator's "push and move forward" it is pushed on close (verify `@{u}..HEAD` authorship).

## Next Steps

1. ✅ Cartography CLOSED + Keystone E0–E2 (46/8) + E3.1–E3.4 cutover + E4 OPENED.
2. ✅ **E4.3 + E4.4 DONE 2026-06-19** — `brief_consumer` (10/10) + `deck_generator` (16/16) built + green on `canvas_std`; `adna_native [OK]`; no regression.
3. **→ ⛔ E4→E5 PHASE GATE (human gate).** Do not auto-advance. Remaining E4 = **E4.1/E4.2** (LF-successor in-vault), **⛔ gated on the D3 governed touch** (`adr_002` amendment / new ADR via `adr_003` LIP). Likely next: either do the **D3 touch** (unblock E4.1/E4.2) or take the **E4→E5 gate** (federation rollout + `iii/` wiring, incl. wiring `deck_generator/iii_quality_contract.md`).
4. **ADR-004 awaits operator ratification** (proposed → ratified + `signed_by`) — prepared; say the word and I flip it. The two FU items (FU1 canvas/-routing; FU2 round-trip dedup) stay contracted PT P5 items.
5. **Pushes:** E4.3 batch (`b0388a3`) pushed; the **E4.4 batch** pushed on close (operator "push and move forward").
6. **PT P5 watch:** ping Hestia when the `canvas_core` relocation is scheduled. **Two `what/production/` residents** (`brief_consumer/` + `deck_generator/`) now exist ahead of P5 — courtesy heads-up to Hestia (no collision; new packages).

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
