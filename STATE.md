---
type: state
created: 2026-06-06
updated: 2026-06-19
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260619_124648_keystone_substrate_path_unblock
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Operation Cartography (genesis planning) CLOSED 2026-06-13 ✅. Now in EXECUTION — Operation Keystone ACTIVE; PHASES E0+E1+E2 ✅ (reference impl + tooling) + 🟢 **PHASE E3 ✅ COMPLETE 2026-06-14** (CanvasForge migrated onto `canvas_std`, parity-gated): E3.1 (canvas/ wrapper) · E3.2 (deprecation shim) · E3.3 (parity gate GREEN) · **E3.4 (full cutover ✅)**. ⛔ HELD at the E3→E4 boundary (human gate) — E4 = LF-successor + net-new consumer.**
`how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md`

Operation Cartography (P0–P5) ratified the **aDNA Canvas Standard v2.0.0** + contracts + build charter, then **closed at the operator gate**. The operator **activated Operation Keystone** (the build). **E0** (skeleton + KEEP floor + golden fixtures) · **E1** (reference engine) · **E2** (conformance harness + v2.0.0 **JSON Schema** + the **`canvas-std` CLI**) built the reference implementation (`pytest` 46/8, `ruff` clean). **E3** (parity-gated CanvasForge migration) is now **COMPLETE** — E3.1 `canvas/` wrapper + E3.2 constants-only `canvas_core`→`canvas_std` deprecation shim + E3.3 parity gate (**GREEN**) + **E3.4 full cutover (2026-06-14)**: CanvasForge single-sources the Standard from Canvas.aDNA v2.0.0; the embedded v1.0.0 framing is superseded; the shim stays through its grace window (removal at E6.2). **⛔ HELD at the E3→E4 phase gate (human gate).** *(Planning history: `campaign_canvas_genesis_planning/`.)*

> **⊕ pt09 (Production Tidy, 2026-06-17) — CanvasForge absorbed into Canvas.** `CanvasForge.aDNA` merged in (reverses E3.4); **Hermes merged into Mondrian**; Canvas now owns Standard **+** production (deck/comic/diagram) at `what/production/`. **Governance merge only** — code (`canvas_core`/`canvas_comic`/`canvas_presentation`) + ~8 consumer wrappers relocate/refederate at PT **P5** (shim-covered interim; `canvas_core→canvas_std` shim folds into the merge, Home §C #29). **Keystone reshape:** the "CanvasForge as a *separate* federated producer" premise is folded — **Mondrian reconciles the E4 phase plan** (net-new consumer + LF-successor now in-vault) at its next Keystone session; no gate auto-advances. Memo: `Home.aDNA/how/campaigns/campaign_production_tidy/coordination_drafts/coord_draft_hestia_to_mondrian_hermes_canvasforge_merge.md`. Archived source: `Archive.aDNA/CanvasForge.aDNA/`. **[2026-06-19] E4 code-layout reconciliation resolved on paper** — [[what/decisions/adr_004_production_code_layout|ADR-004]] (proposed) pins `canvas_core` → `what/production/canvas_core/` (import unchanged; env `CANVAS_CORE_HOME`; `canvas_std` resolves via installed `adna-canvas-std`), **answering Hestia's substrate-path memo → Hearthstone P3 unblocked** (reply: `who/coordination/coord_2026_06_19_mondrian_to_hestia_canvas_substrate_path_reply.md`), and folding the 2 parked follow-ups into the P5 relocation contract. **E3→E4 stays HELD; no code moves; operator ratifies adr_004.** **Loop closed (2026-06-19):** Hestia actioned same-day — exemplar **staged** (fallthrough resolver auto-flips at P5) + acked; Home §C **#39** env-var alias (`CANVASFORGE_CODE`→`CANVAS_CORE_HOME`) registered. **Forward-ref → ping Hestia when the PT P5 relocation is scheduled** (she re-verifies + drops the interim archive branch). *Wind-down housekeeping: MANIFEST de-drifted to Keystone-current; lightweight AAR filed on the session; campaign log + adr_004 P5-checklist updated.*

## ▶ Resume Here — ⛔ Phase E3 COMPLETE; HELD at E3→E4 (human gate)

**Phase E3 (CanvasForge migration) is COMPLETE** as of 2026-06-14. The full cutover landed (operator-authorized):
CanvasForge now **single-sources** the aDNA Canvas Standard from **Canvas.aDNA v2.0.0** via the `canvas/` wrapper +
the `canvas_core`→`canvas_std` constants shim; the embedded **Canvas Standard v1.0.0 framing is superseded** (5
supersession banners + a directory routing banner across `CanvasForge.aDNA/what/context/advanced_canvas/`;
archive-never-delete, SO-6). Cutover criteria all MET; **rollback rehearsed net-zero** (revert the shim → embedded
floor 900/3 green; restore HEAD → shim back; baseline `3ce4d341` intact in both states). CanvasForge suite 900/3.
Evidence: `missions/artifacts/e3_4_cutover_criteria.md` + `e3_4_rollback_rehearsal.md`. The `canvas_core` shim stays
live through the **E-D2 grace window (2027-06-13)**; ref-sweep-zero + Mondrian/Hermes owner-ack + removal execute at
**E6.2** (scheduled in the Home.aDNA §C ledger).

**Next: ⛔ E3→E4 is a PHASE gate (human gate) — do NOT open E4 without the operator.** E4 = stand up the
LiteratureForge-successor as a federated producer (E4.1–E4.2), build ≥1 net-new consumer end-to-end (E4.3), and the
parked deck-generator pilot as a worked build (E4.4). After E4: E5 (federation rollout + `iii/` wiring + registry) ·
E6 (cross-system parity + final cutover/shim retirement at E6.2 + campaign AAR at E6.3). Chartered:
[[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] §Phases E4–E6.

**Open follow-ups → now contracted as PT P5 items in [[what/decisions/adr_004_production_code_layout|ADR-004]]**
(both partially OBE post-pt09; folded into the P5 relocation contract 2026-06-19, no gate change): (1) **FU1 —
canvas/-routing Standing Order**, reframed as Canvas *production* governance (route `what/production/` standard-
consumption through `canvas/`, mirroring `iii/`) at the P5 refederation — **not** an edit to the archived
"do-not-resume" CanvasForge `CLAUDE.md`. (2) **FU2 — round-trip-function dedup** (validate/diff/merge/round-trip →
`canvas_std`) at `canvas_core` relocation (once co-located with `canvas_std`), gated by `e3_3_parity_check.py`
(baseline `3ce4d341` unchanged).

**Build hygiene:** the CanvasForge suite runs in the gitignored `.venv` at `CanvasForge.aDNA/what/code/`
(`adna-canvas-std` editable; `.venv/bin/python -m pytest canvas_core/tests/ canvas_comic/tests/ tests/test_federation_validation.py -q` → 900/3). Canvas.aDNA's own `canvas_std` suite: `.venv` at `what/code/canvas_std`. Tracking: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active).

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]); III/SiteForge upstream notes; III pin confirm at E5.1.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds E4.4 as a worked build; informs D2/D4/D7. Opens no phase, builds no code until E4.

## What's Done (this session — Keystone E3.4 full cutover, 2026-06-14)

- **E3.4 cutover ✅ COMPLETE** (operator-authorized full cutover) — **Phase E3 CLOSED**. Four objectives:
  1. **Cutover criteria** documented + all 6 MET (`artifacts/e3_4_cutover_criteria.md`): parity GREEN (E3.3) · suite 900/3 · iii ≥ baseline by construction · baseline `3ce4d341` locked · rollback rehearsed · operator gate.
  2. **Rollback rehearsed net-zero** (`artifacts/e3_4_rollback_rehearsal.md`): HEAD==`1a51801`, so revert the shim → embedded floor self-contained + **900/3 green** (no consumer breakage); restore HEAD → shim back; tree clean; baseline intact both states.
  3. **v1.0.0 framing superseded** (CanvasForge): 5 supersession banners (`…_standard/_schema/_roundtrip/_validation_results/_tooling_gaps.md`) + directory routing banner (`advanced_canvas/AGENTS.md`); `canvas/CLAUDE.md` → cutover-active. Design-craft files (typography/color/composition/…) left intact (producer knowledge, not the Standard). Archive-never-delete. Suite unchanged 900/3.
  4. **Shim retirement scheduled**: Home.aDNA §C ledger row marked E3.4-green + dated row note; remaining conditions (ref-sweep-zero + Mondrian/Hermes owner-ack) execute at E6.2. Home.aDNA local (Rule 4).
- *(Prior: Cartography closed; Keystone E0+E1+E2 reference impl 46/8; E3.1 wrapper + E3.2 shim + E3.3 parity GREEN.)*

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip) — **superseded 2026-06-14 (E3.4)**: now carries supersession banners → Canvas.aDNA v2.0.0. Invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for the E3.2 shim).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3) — feeds E4.

## Active Blockers

- **None blocking.** Phase E3 COMPLETE. **E3→E4 is a human gate** — do not open E4 (LF-successor + net-new consumer) without the operator. CanvasForge tests run in the gitignored `.venv` at `what/code/` (`adna-canvas-std` editable).
- **Pushes:** the E3.4 close batch (Canvas.aDNA: 2 artifacts + mission + STATE + campaign + session; CanvasForge.aDNA: 6 banner/context files + `canvas/CLAUDE.md`) is **pending push per the operator batch convention** — confirm before pushing; check `@{u}..HEAD` authorship. **[+2026-06-19] the substrate-path batch (adr_004 + Hestia reply + STATE + session) joins this pending batch.** Home.aDNA §C ledger update stays **local** (Rule 4); the Home courtesy cross-file is Home-local too.

## Next Steps

1. ✅ Cartography CLOSED + Keystone E0+E1+E2 (reference impl 46/8, `ruff` clean) + E3.1/E3.2/E3.3.
2. ✅ **E3.4 COMPLETE 2026-06-14** — full cutover; CanvasForge single-sources v2.0.0; v1.0.0 framing superseded; rollback rehearsed net-zero; shim retire scheduled E6.2. **PHASE E3 COMPLETE.**
3. **→ ⛔ E3→E4 PHASE GATE (human gate).** Do not open E4 without the operator. E4 = LF-successor federated producer (E4.1–E4.2) + ≥1 net-new consumer (E4.3) + deck-generator pilot (E4.4).
4. **Follow-ups → contracted PT P5 items** ([[what/decisions/adr_004_production_code_layout|ADR-004]], 2026-06-19): FU1 canvas/-routing as production governance (at P5 refederation); FU2 round-trip dedup → `canvas_std` (at relocation, gated by `e3_3_parity_check.py`).
5. **Pushes:** E3.4 close batch **+ the 2026-06-19 substrate-path batch** pending → push per operator batch; Home.aDNA local.
6. **adr_004 awaits operator ratification** (proposed → ratified + `signed_by`). **Hestia DONE** (2026-06-19) — exemplar staged + acked; both Home-local ledger updates filed (§C #39 alias); **loop closed**. **→ Ping Hestia when the PT P5 relocation is scheduled** (re-verify + drop interim archive branch).

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
