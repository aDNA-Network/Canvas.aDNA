---
type: state
created: 2026-06-06
updated: 2026-06-19
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260619_231005_keystone_e4_1_lf_successor
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Operation Cartography (genesis planning) CLOSED 2026-06-13 ✅. Now in EXECUTION — Operation Keystone ACTIVE; PHASES E0+E1+E2 ✅ (reference impl + tooling) + E3 ✅ (CanvasForge migration) + E4 ✅ (E4.3 `brief_consumer` 10/10 + E4.4 `deck_generator` 16/16; E4.1/E4.2 carried as D3-gated debt). 🔓 **PHASE E5 OPENED 2026-06-19** (operator-authorized E4→E5 gate crossing: "Advance to E5" + "Ratify ADR-004"); **E5.1 ✅ DONE** — Canvas `iii/` wrapper activated (III pin **v0.5.0**) + first real canvas review on both consumers (**0 High / 0 Med** structural; pixel/VR1 PT-P5-gated). **ADR-004 ratified.** ⛔ Now HELD at the E5→E6 boundary (human gate); E5.2 (federation rollout) is partly PT-P5-coupled; the **D3 touch for E4.1/E4.2 is RESOLVED** (`adr_005` ratified 2026-06-19). **🔨 E4.1 ✅ DONE 2026-06-19** — `document_generator` (the in-vault long-form LF-successor) built + green (**18/18**, `ruff` clean) on `canvas_std`; structural `iii/` review **0 High / 0 Med**; first use of the `code` component. **E4.2** (LF visual/format-contract migration) is the next mission, unscheduled. No gate advanced.**
`how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md`

Operation Cartography (P0–P5) ratified the **aDNA Canvas Standard v2.0.0** + contracts + build charter, then **closed at the operator gate**. The operator **activated Operation Keystone** (the build). **E0** (skeleton + KEEP floor + golden fixtures) · **E1** (reference engine) · **E2** (conformance harness + v2.0.0 **JSON Schema** + the **`canvas-std` CLI**) built the reference implementation (`pytest` 46/8, `ruff` clean). **E3** (parity-gated CanvasForge migration) is now **COMPLETE** — E3.1 `canvas/` wrapper + E3.2 constants-only `canvas_core`→`canvas_std` deprecation shim + E3.3 parity gate (**GREEN**) + **E3.4 full cutover (2026-06-14)**: CanvasForge single-sources the Standard from Canvas.aDNA v2.0.0; the embedded v1.0.0 framing is superseded; the shim stays through its grace window (removal at E6.2). **🔓 E4 OPENED 2026-06-19** (operator-authorized E3→E4 crossing) — table reconciled to in-vault production; **E4.3 + E4.4 ✅ built + green** (`brief_consumer` + `deck_generator` on `canvas_std`); **⛔ now HELD at the E4→E5 phase gate (human gate).** *(Planning history: `campaign_canvas_genesis_planning/`.)*

> **⊕ pt09 (Production Tidy, 2026-06-17) — CanvasForge absorbed into Canvas.** `CanvasForge.aDNA` merged in (reverses E3.4); **Hermes merged into Mondrian**; Canvas now owns Standard **+** production (deck/comic/diagram) at `what/production/`. **Governance merge only** — code (`canvas_core`/`canvas_comic`/`canvas_presentation`) + ~8 consumer wrappers relocate/refederate at PT **P5** (shim-covered interim; `canvas_core→canvas_std` shim folds into the merge, Home §C #29). **Keystone reshape:** the "CanvasForge as a *separate* federated producer" premise is folded — **Mondrian reconciles the E4 phase plan** (net-new consumer + LF-successor now in-vault) at its next Keystone session; no gate auto-advances. Memo: `Home.aDNA/how/campaigns/campaign_production_tidy/coordination_drafts/coord_draft_hestia_to_mondrian_hermes_canvasforge_merge.md`. Archived source: `Archive.aDNA/CanvasForge.aDNA/`. **[2026-06-19] E4 code-layout reconciliation resolved on paper** — [[what/decisions/adr_004_production_code_layout|ADR-004]] (proposed) pins `canvas_core` → `what/production/canvas_core/` (import unchanged; env `CANVAS_CORE_HOME`; `canvas_std` resolves via installed `adna-canvas-std`), **answering Hestia's substrate-path memo → Hearthstone P3 unblocked** (reply: `who/coordination/coord_2026_06_19_mondrian_to_hestia_canvas_substrate_path_reply.md`), and folding the 2 parked follow-ups into the P5 relocation contract. **E3→E4 stays HELD; no code moves; operator ratifies adr_004.** **Loop closed (2026-06-19):** Hestia actioned same-day — exemplar **staged** (fallthrough resolver auto-flips at P5) + acked; Home §C **#39** env-var alias (`CANVASFORGE_CODE`→`CANVAS_CORE_HOME`) registered. **Forward-ref → ping Hestia when the PT P5 relocation is scheduled** (she re-verifies + drops the interim archive branch). *Wind-down housekeeping: MANIFEST de-drifted to Keystone-current; lightweight AAR filed on the session; campaign log + adr_004 P5-checklist updated.*

## ▶ Resume Here — E5 OPEN; E5.1 + E4.1 DONE; ⛔ HELD at E5→E6 (human gate)

**Phase E5 is OPEN (2026-06-19, operator-authorized E4→E5 crossing — "Advance to E5" + "Ratify ADR-004"); E5.1 is
DONE.** (E0–E2 reference impl + E3 CanvasForge cutover + E4 consumers are complete history; the `canvas_core` shim
stays live to the E-D2 window 2027-06-13, retired at E6.2.) **E4 closed-with-deferral:** E4.3 (`brief_consumer` 10/10)
+ E4.4 (`deck_generator` 16/16) done; **E4.1/E4.2 (LF-successor) — D3 touch RESOLVED:** `adr_002`'s Option-B
*federated* leg is superseded by **[[what/decisions/adr_005_lf_successor_in_vault|adr_005]]** (**ratified 2026-06-19**
→ in-vault `what/production/`; the Option-A schema leg stands). **E4.1 is now BUILT** (operator opened E4.1/E4.2 at the
E5 hold, SO-3, 2026-06-19): **`document_generator`** — the in-vault long-form LF-successor — is green (18/18) on
`canvas_std`, structural `iii/` review 0 High/0 Med (`iii/feedback_2026_06_19_document_generator.md`). **E4.2** (visual/
format-contract migration) remains the next mission — unblocked, unscheduled.

**E5.1 — `iii/` wrapper wired + first real canvas review (DONE 2026-06-19):**
- **Wrapper activated** — `iii/CLAUDE.md` scaffold → **active**; III pin **confirmed v0.5.0** (commit `0f06aa6`, oracle
  lattice 1.2.6) vs `III.aDNA/MANIFEST.md` (minor bump reviewed per III ADR-002 §3; siblings VideoForge/CanvasForge/wga
  already @ v0.5.0; stale router "v0.4.0" superseded). New `iii/what/context/` files — `canvas_reviewers.yaml` (5-lens
  panel) + `canvas_iii_learning_store.jsonl`; `reviewer_registry` extension added (existing ADR-002 §1a kind — no amendment).
- **First real review** — structural III review of both consumers' example canvases → **0 High / 0 Med** across the
  lenses; **3 Low + 1 GRAPH-GAP** tracked as errata; `CANVAS-L-001` (citation-label-dropped) accumulated **local**.
  **Pixel/VR1 explicitly PT-P5-gated** (deferred, not passed). Artifact: `iii/feedback_2026_06_19_canvas_consumers.md`.
  Mission: [[how/campaigns/campaign_canvas_genesis/missions/mission_e5_1_iii_wiring|mission_e5_1]].
- **ADR-004 ratified** (operator countersign at the gate) — binds the PT P5 relocation target; NOT authorization to
  move code (relocation = PT P5).
- No regression: `canvas_std` 46/8 · `brief_consumer` 10/10 · `deck_generator` 16/16; `ruff` clean; both examples `[OK]`.

**E4.1 — LF-successor built (DONE 2026-06-19):**
- **`document_generator`** (3rd in-vault consumer; `what/production/document_generator/`) — a structured long-form
  document spec → a v2.0.0 aDNA-Native **multi-page** `.canvas` (pages = group nodes; `profile: long_document`;
  `sequence` across pages, `reading_order` within, `adjacency` prose→citations). On `canvas_std` alone (zero PT-P5 dep,
  per `adr_005`); the genre/writing pipeline stays producer-side (E4.2+).
- **First use of the `code` component class**; figure→file/link, table, caption, blockquote, list, citations all carry +
  degrade. Worked example: a self-referential whitepaper about the Standard (2 pages / 27 nodes / 23 edges).
- **Green:** `document_generator` **18/18**, `ruff` clean; CLI `document-generator build` + `canvas-std validate` →
  `adna_native [OK]` + D-1/D-2/D-3.
- **Structural `iii/` review → 0 High / 0 Med** (pixel/VR1 PT-P5-gated): 2 Low (`CANVAS-L-001` recurrence freq→2;
  `CANVAS-L-002` layout-overflow) + 1 GRAPH-GAP + **3 spec-gap erratum candidates** (see Open side-tracks). Artifact:
  `iii/feedback_2026_06_19_document_generator.md`. Mission:
  [[how/campaigns/campaign_canvas_genesis/missions/mission_e4_1_lf_successor|mission_e4_1]] (completed).

**Next: ⛔ E5→E6 is a PHASE gate (human gate) — do NOT auto-advance.** Remaining E5 = **E5.2** (federation rollout to
ComfyUI/Astro — the ~8 producer-wrapper refederations are **PT-P5-coupled**, i.e. land at the `canvas_core`
relocation) + **E5.3** (optional Δ2 LIP). Then E6 (cross-system parity + shim retirement E6.2 + campaign AAR E6.3).
**Carried debt cleared:** E4.1/E4.2 (LF-successor) — **D3 touch RESOLVED** (`adr_005` ratified 2026-06-19; in-vault, supersedes `adr_002` Option-B → unblocked, unscheduled). Chartered:
[[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] §Phases E5–E6.

**Open follow-ups → contracted as PT P5 items in [[what/decisions/adr_004_production_code_layout|ADR-004]] (ratified
2026-06-19):** (1) **FU1 — canvas/-routing Standing Order** (route `what/production/` standard-consumption through
`canvas/`, mirroring `iii/`) at the P5 refederation — **not** an edit to the archived "do-not-resume" CanvasForge
`CLAUDE.md`. (2) **FU2 — round-trip-function dedup** (validate/diff/merge/round-trip → `canvas_std`) at `canvas_core`
relocation (once co-located with `canvas_std`), gated by `e3_3_parity_check.py` (baseline `3ce4d341` unchanged).

**Build hygiene:** Canvas.aDNA's `canvas_std` suite: `.venv` at `what/code/canvas_std` (46/8). **E4 consumer suites
(gitignored `.venv` per package, `adna-canvas-std` editable): `what/production/brief_consumer/` → 10/10;
`what/production/deck_generator/` → 16/16; `what/production/document_generator/` → 18/18; all `ruff` clean.** The CanvasForge suite (KEEP reference) runs in the
gitignored `.venv` at `CanvasForge.aDNA/what/code/` → 900/3. Tracking:
[[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active).

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]) → E5.3; the
3 Low review errata (citation provenance; link-label carry; deck slide order) at a generator pass; III/Astro upstream
notes. **E4.1 spec-gap erratum candidates → LIP queue (`adr_003`):** (1) orphan-anchor + `naming_convention` validator
absent — `spec_panel_link_semantics §5.3/§6` mandates the check but `canvas_std/reserved.py::validate_panel_link` lacks
it (headline); (2) no dedicated `quote`/`blockquote` or `footnote` component class (long-form rides on `text` +
`semantic_type`); (3) `sequence`-unit ambiguity for paginated multi-section docs (§5.1 section-panels vs the page-centric
chain used by `document_generator`; `region` class left unexercised). Detail: `iii/feedback_2026_06_19_document_generator.md`.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds E4.4 as a worked build; informs D2/D4/D7. Opens no phase, builds no code until E4.

## What's Done (this session — Keystone E4.1 LF-successor build, mid-E5, 2026-06-19)

- **E4.1 OPENED + BUILT** (operator opened E4.1/E4.2 at the E5 hold, SO-3). Authored E4.1 mission objectives +
  acceptance criteria, then built **`document_generator`** — the in-vault long-form LF-successor — at
  `what/production/document_generator/` (model/layout/blocks/consume/__main__/__init__ + whitepaper example + 5 test
  files + README + iii_quality_contract). A document spec → a v2.0.0 aDNA-Native **multi-page** `.canvas`
  (`profile: long_document`; pages = group nodes; `sequence` across pages, `reading_order` within, `adjacency`
  prose→citations). On `canvas_std` alone (zero PT-P5 dep, per `adr_005`); the genre pipeline stays producer-side.
- **Green + verified:** `document_generator` **18/18**, `ruff` clean; CLI build + `canvas-std validate` →
  `adna_native [OK]` + D-1/D-2/D-3; **first use of the `code` component class**. No regression (`canvas_std` 46/8 ·
  `brief_consumer` 10/10 · `deck_generator` 16/16).
- **Structural `iii/` review → 0 High / 0 Med** (pixel/VR1 PT-P5-gated): 2 Low + 1 GRAPH-GAP + 3 spec-gap erratum
  candidates (orphan-anchor validator absent · no `quote`/`footnote` class · `sequence`-unit ambiguity §5.1). `CANVAS-L-001`
  bumped freq→2 (2 sessions); `CANVAS-L-002` added. Artifact: `iii/feedback_2026_06_19_document_generator.md`.
- **No gate advanced** (E5→E6 stays the human gate). **E4.2** (LF visual/format-contract migration) is the next mission.
- *(Prior session: D3 governed touch — `adr_005` ratified, LF-successor in-vault, E4.1/E4.2 unblocked. Earlier:
  Cartography closed; Keystone E0–E2 46/8; E3.1–E3.4 cutover; E4.3/E4.4 consumers; E4→E5 crossed; ADR-004 ratified;
  E5.1 `iii/` wrapper active @ v0.5.0 + first review.)*

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip) — **superseded 2026-06-14 (E3.4)**: now carries supersession banners → Canvas.aDNA v2.0.0. Invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for the E3.2 shim).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3) — feeds E4.

## Active Blockers

- **None blocking E5.1** (done + green). **E5→E6 is the human gate** — do not auto-advance. Remaining E5 = **E5.2**
  (federation rollout — the ~8 producer-wrapper refederations are **PT-P5-coupled**) + **E5.3** (optional Δ2 LIP).
- **✅ E4.1 BUILT this session** (operator opened E4.1/E4.2 at the E5 hold, SO-3). `document_generator` (in-vault
  LF-successor) green **18/18** on `canvas_std`; structural `iii/` review 0 High/0 Med. **E4.2** (LF visual/format-contract
  migration) is the next mission — unblocked (D3 touch `adr_005` ratified; in-vault), unscheduled, blocked only by E4.1
  (now done). 3 spec-gap erratum candidates filed to the LIP queue (see Open side-tracks).
- **ADR-004 / ADR-005: ✅ ratified 2026-06-19** — no longer blockers. (Code relocation still PT P5.)
- **Pushes:** prior batches pushed through `5aecb0b` (D3 touch). The **E4.1 batch** (new `document_generator` package +
  example + tests + `iii/` feedback + learning-store bump + mission AAR + campaign + STATE + session) is committed
  locally; **push held for operator authorization** per the batch convention (verify `@{u}..HEAD` authorship).

## Next Steps

1. ✅ Cartography CLOSED + Keystone E0–E2 (46/8) + E3 cutover + E4 (E4.3 10/10 + E4.4 16/16) + **E4→E5 crossed**.
2. ✅ **ADR-004 ratified 2026-06-19** (operator countersign) — binds the PT P5 relocation target.
3. ✅ **E5.1 DONE 2026-06-19** — `iii/` wrapper active (III pin v0.5.0) + first real canvas review (0 High / 0 Med
   structural; pixel/VR1 PT-P5-gated); no regression.
4. **→ ⛔ E5→E6 PHASE GATE (human gate).** Do not auto-advance. Remaining E5 = **E5.2** (federation rollout to
   ComfyUI/Astro — the ~8 producer-wrapper refederations are **PT-P5-coupled**) + **E5.3** (optional Δ2 LIP). Likely
   next: hold for the operator — E5.2 is mostly gated on PT P5; E5.3 (the LIP) is operator-discretionary.
5. ✅ **E4.1 DONE 2026-06-19** — `document_generator` (in-vault LF-successor), 18/18, structural `iii/` review 0 High/0
   Med, first `code`-component use. **→ E4.2** (LF visual/format-contract migration: `spec_visual_contract` V1–V8 +
   `spec_format_contract` from `Archive.aDNA/LiteratureForge.aDNA/what/specs/` → producer-side config + per-genre config;
   genre pipeline stays producer-side) is the next mission — unblocked, unscheduled, opened on operator go (SO-3).
6. **Pushes:** prior batches pushed through `5aecb0b`; the **E4.1 batch** is committed locally and **held for operator
   push authorization** (batch convention; verify `@{u}..HEAD`).
7. **PT P5 watch:** ping Hestia when the `canvas_core` relocation is scheduled (she re-verifies the staged exemplar
   resolver). Two `what/production/` residents already precede P5 (no collision).

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
