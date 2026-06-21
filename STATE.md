---
type: state
created: 2026-06-06
updated: 2026-06-20
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260620_200612_lip_queue_closeout
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

> ✅ **OPERATION KEYSTONE COMPLETE (2026-06-20).** The aDNA Canvas Standard v2.0.0 shipped as running infrastructure
> (reference impl + parity-gated floor migration + 3 in-vault consumers, no regression); E6 validated + cutover
> confirmed + campaign closed (operator disposition: complete-with-PT-P5-tail). **Authoritative close record:**
> `how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md` §Completion Summary + §Campaign AAR. **Open tail
> → PT P5 + LIP queue:** `how/campaigns/campaign_canvas_genesis/missions/artifacts/e6_3_handoff_register.md`. The
> dense sections below are retained as build history.

## Current Phase

**Operation Cartography (genesis planning) CLOSED 2026-06-13 ✅. Now in EXECUTION — **Operation Keystone COMPLETE (2026-06-20)**; PHASES E0+E1+E2 ✅ (reference impl + tooling) + E3 ✅ (CanvasForge migration) + E4 ✅ (E4.3 `brief_consumer` 10/10 + E4.4 `deck_generator` 16/16; E4.1/E4.2 carried as D3-gated debt). 🔓 **PHASE E5 OPENED 2026-06-19** (operator-authorized E4→E5 gate crossing: "Advance to E5" + "Ratify ADR-004"); **E5.1 ✅ DONE** — Canvas `iii/` wrapper activated (III pin **v0.5.0**) + first real canvas review on both consumers (**0 High / 0 Med** structural; pixel/VR1 PT-P5-gated). **ADR-004 ratified.** ✅ E5→E6 crossed + **PHASE E6 COMPLETE 2026-06-20** (E6.1 parity GREEN · E6.2 cutover confirmed · E6.3 AAR; campaign CLOSED); E5.2 (federation rollout) handed to PT P5; the **D3 touch for E4.1/E4.2 is RESOLVED** (`adr_005` ratified 2026-06-19). **🔨 E4.1 ✅ DONE 2026-06-19** (`document_generator`, 18/18). **🔨 E4.2 ✅ DONE 2026-06-20 — PHASE E4 COMPLETE** — LF format/visual contracts (F1–F7/V1–V8/X1–X14) → declarative `_reserved` metadata + per-genre `GENRE_PROFILES`; **first `region`-class use**; **section-level reflow closes the bulk of `CANVAS-L-002`** (residual → PT P5). `document_generator` **37/37**, `ruff` clean; no regression (46/8 · 10 · 16); `canvas_std` untouched (firewall git-diff 0); structural `iii/` review **0 High / 0 Med**. No gate advanced.**
`how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md`

Operation Cartography (P0–P5) ratified the **aDNA Canvas Standard v2.0.0** + contracts + build charter, then **closed at the operator gate**. The operator **activated Operation Keystone** (the build). **E0** (skeleton + KEEP floor + golden fixtures) · **E1** (reference engine) · **E2** (conformance harness + v2.0.0 **JSON Schema** + the **`canvas-std` CLI**) built the reference implementation (`pytest` 46/8, `ruff` clean). **E3** (parity-gated CanvasForge migration) is now **COMPLETE** — E3.1 `canvas/` wrapper + E3.2 constants-only `canvas_core`→`canvas_std` deprecation shim + E3.3 parity gate (**GREEN**) + **E3.4 full cutover (2026-06-14)**: CanvasForge single-sources the Standard from Canvas.aDNA v2.0.0; the embedded v1.0.0 framing is superseded; the shim stays through its grace window (removal at E6.2). **🔓 E4 OPENED 2026-06-19** (operator-authorized E3→E4 crossing) — table reconciled to in-vault production; **E4.3 + E4.4 ✅ built + green** (`brief_consumer` + `deck_generator` on `canvas_std`); **⛔ now HELD at the E4→E5 phase gate (human gate).** *(Planning history: `campaign_canvas_genesis_planning/`.)*

> **⊕ pt09 (Production Tidy, 2026-06-17) — CanvasForge absorbed into Canvas.** `CanvasForge.aDNA` merged in (reverses E3.4); **Hermes merged into Mondrian**; Canvas now owns Standard **+** production (deck/comic/diagram) at `what/production/`. **Governance merge only** — code (`canvas_core`/`canvas_comic`/`canvas_presentation`) + ~8 consumer wrappers relocate/refederate at PT **P5** (shim-covered interim; `canvas_core→canvas_std` shim folds into the merge, Home §C #29). **Keystone reshape:** the "CanvasForge as a *separate* federated producer" premise is folded — **Mondrian reconciles the E4 phase plan** (net-new consumer + LF-successor now in-vault) at its next Keystone session; no gate auto-advances. Memo: `Home.aDNA/how/campaigns/campaign_production_tidy/coordination_drafts/coord_draft_hestia_to_mondrian_hermes_canvasforge_merge.md`. Archived source: `Archive.aDNA/CanvasForge.aDNA/`. **[2026-06-19] E4 code-layout reconciliation resolved on paper** — [[what/decisions/adr_004_production_code_layout|ADR-004]] (proposed) pins `canvas_core` → `what/production/canvas_core/` (import unchanged; env `CANVAS_CORE_HOME`; `canvas_std` resolves via installed `adna-canvas-std`), **answering Hestia's substrate-path memo → Hearthstone P3 unblocked** (reply: `who/coordination/coord_2026_06_19_mondrian_to_hestia_canvas_substrate_path_reply.md`), and folding the 2 parked follow-ups into the P5 relocation contract. **E3→E4 stays HELD; no code moves; operator ratifies adr_004.** **Loop closed (2026-06-19):** Hestia actioned same-day — exemplar **staged** (fallthrough resolver auto-flips at P5) + acked; Home §C **#39** env-var alias (`CANVASFORGE_CODE`→`CANVAS_CORE_HOME`) registered. **Forward-ref → ping Hestia when the PT P5 relocation is scheduled** (she re-verifies + drops the interim archive branch). *Wind-down housekeeping: MANIFEST de-drifted to Keystone-current; lightweight AAR filed on the session; campaign log + adr_004 P5-checklist updated.*

## ▶ Resume Here — ✅ KEYSTONE COMPLETE + LIP QUEUE CLOSED (v2.0.1 cut + pushed 2026-06-20); tail → B4 LIP + PT P5

**Phase E5 is OPEN (2026-06-19, operator-authorized E4→E5 crossing — "Advance to E5" + "Ratify ADR-004"); E5.1 is
DONE.** (E0–E2 reference impl + E3 CanvasForge cutover + E4 consumers are complete history; the `canvas_core` shim
stays live to the E-D2 window 2027-06-13, retired at E6.2.) **E4 closed-with-deferral:** E4.3 (`brief_consumer` 10/10)
+ E4.4 (`deck_generator` 16/16) done; **E4.1/E4.2 (LF-successor) — D3 touch RESOLVED:** `adr_002`'s Option-B
*federated* leg is superseded by **[[what/decisions/adr_005_lf_successor_in_vault|adr_005]]** (**ratified 2026-06-19**
→ in-vault `what/production/`; the Option-A schema leg stands). **E4.1 + E4.2 are now BUILT — PHASE E4 COMPLETE** (operator
opened E4.1/E4.2 at the E5 hold, SO-3, 2026-06-19; built E4.1 same day, **E4.2 on 2026-06-20**): **`document_generator`**
— the in-vault long-form LF-successor — is green (**37/37**) on `canvas_std`, structural `iii/` review 0 High/0 Med
(`iii/feedback_2026_06_20_document_generator_e4_2.md`). **E4.2 done:** the LF format/visual contracts ride the `.canvas`
as declarative `_reserved` metadata + per-genre `GENRE_PROFILES`; first `region`-class use; section-level reflow closes
the bulk of `CANVAS-L-002`.

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

**E4.2 — LF visual/format contracts + reflow (DONE 2026-06-20; full envelope, operator go):**
- **Contracts as declarative metadata** — `spec_format_contract` F1–F7 + `spec_visual_contract` V1–V8/X1–X14 (scavenged
  from `Archive.aDNA/LiteratureForge.aDNA/what/specs/`) now ride `document_generator`'s `.canvas` in `_reserved`
  (`semantic_bindings.{genre,format,visual}` + `brand_style_pack_ref` + derived `panel_link.surfaces`), driven by a
  5-entry **`GENRE_PROFILES`** registry (whitepaper + grant worked; research/blog/exec stubbed) + per-figure `asset`
  overrides. The genre/writing pipeline stays producer-side; `canvas_std` schema **untouched** (firewall git-diff 0).
- **First use of the `region` component class** — derived-surface backing markers + the `rgn_subclass` region (X12).
- **Reflow / auto-pagination (section-level) closes the bulk of `CANVAS-L-002`** — whitepaper 2→5 pages, grant 1→4,
  every emitted page ≤ `CONTENT_H`; a non-overflowing no-genre doc is **byte-identical to E4.1** (golden-locked). Narrow
  residual (a single section taller than a page) flagged `oversized_overflow` → PT P5.
- **Green:** `document_generator` **37/37** (18 + 19 new), `ruff` clean; CLI + `canvas-std validate` → `adna_native
  [OK]` + D-1/D-2/D-3; no regression (`canvas_std` 46/8 · `brief_consumer` 10 · `deck_generator` 16); `model.py`
  AST-guarded substrate-neutral. Structural `iii/` review **0 High / 0 Med** (`iii/feedback_2026_06_20_document_generator_e4_2.md`);
  `CANVAS-L-002` → addressed; **1 new spec-gap erratum candidate** (derived-surface backing node) + sequence-unit
  erratum sharpened → LIP queue. Mission:
  [[how/campaigns/campaign_canvas_genesis/missions/mission_e4_2_lf_contracts|mission_e4_2]] (completed). **Phase E4 complete.**

**Next: ✅ PHASE E6 COMPLETE — OPERATION KEYSTONE CLOSED (2026-06-20).** E6.1 cross-system parity **GREEN**; E6.2
cutover confirmed at the Standard/floor level (rollback intact; shim retire scheduled 2027-06-13); E6.3 handoff
register + context graduation + Campaign AAR. **Open tail → PT P5** (E5.2 federation rollout = the ~8
producer-wrapper refederations + `canvas_core` relocation + v2.0.0 registration; the 55 federation-integration test
reds are this work made concrete) **+ LIP queue** (4 spec-gap errata, `adr_003`) **+ optional** Δ2 LIP (E5.3).
Authoritative close: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] §Completion
Summary; tail: `how/campaigns/campaign_canvas_genesis/missions/artifacts/e6_3_handoff_register.md`.

**Open follow-ups → contracted as PT P5 items in [[what/decisions/adr_004_production_code_layout|ADR-004]] (ratified
2026-06-19):** (1) **FU1 — canvas/-routing Standing Order** (route `what/production/` standard-consumption through
`canvas/`, mirroring `iii/`) at the P5 refederation — **not** an edit to the archived "do-not-resume" CanvasForge
`CLAUDE.md`. (2) **FU2 — round-trip-function dedup** (validate/diff/merge/round-trip → `canvas_std`) at `canvas_core`
relocation (once co-located with `canvas_std`), gated by `e3_3_parity_check.py` (baseline `3ce4d341` unchanged).

**Build hygiene:** Canvas.aDNA's `canvas_std` suite: `.venv` at `what/code/canvas_std` (46/8). **E4 consumer suites
(gitignored `.venv` per package, `adna-canvas-std` editable): `what/production/brief_consumer/` → 10/10;
`what/production/deck_generator/` → 16/16; `what/production/document_generator/` → 37/37 (E4.2: 18 + 19 new); all `ruff` clean.** The CanvasForge suite (KEEP reference) runs in the
gitignored `.venv` at `CanvasForge.aDNA/what/code/` → 900/3. Tracking:
[[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active).

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]) → E5.3; the
3 Low review errata (citation provenance; link-label carry; deck slide order) at a generator pass; III/Astro upstream
notes. **E4.1 spec-gap erratum candidates → LIP queue (`adr_003`):** (1) orphan-anchor + `naming_convention` validator
absent — `spec_panel_link_semantics §5.3/§6` mandates the check but `canvas_std/reserved.py::validate_panel_link` lacks
it (headline); (2) no dedicated `quote`/`blockquote` or `footnote` component class (long-form rides on `text` +
`semantic_type`); (3) `sequence`-unit ambiguity for paginated multi-section docs (§5.1 section-panels vs the page-centric
chain used by `document_generator`). Detail: `iii/feedback_2026_06_19_document_generator.md`. **E4.2 update
(2026-06-20):** (4) **NEW** — a *derived* `panel_link.surface` (html / funder_portal) has no content region, so the
producer must mint a synthetic `region`-class backing node to satisfy A-5; should the Standard allow a surface-as-pure-
metadata declaration? (surface-model erratum). Erratum (3) is **sharpened** — E4.2 now **exercises the `region` class**
(for surface/subclass markers), while pagination still rides page-`panel` nodes, so "which construct owns pagination —
`region` or page-`panel`?" is now concrete. `CANVAS-L-002` (layout overflow) **addressed by E4.2 section-level reflow**
(narrow residual → PT P5). Detail: `iii/feedback_2026_06_20_document_generator_e4_2.md`.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds E4.4 as a worked build; informs D2/D4/D7. Opens no phase, builds no code until E4.

## What's Done (this session — Keystone E4.2 LF contracts + reflow, mid-E5, 2026-06-20)

- **E4.2 OPENED + BUILT (full envelope — operator chose "Build E4.2" + "Include reflow").** Authored E4.2 objectives +
  acceptance criteria, then extended `document_generator` across four modules: **`model.py`** (frozen substrate-neutral
  FormatContract F1–F7 / AssetVisual V1–V8 / CrossAssetVisual X1–X14 / GenreProfile + a 5-entry `GENRE_PROFILES`
  registry; `Document.genre`/`Block.asset`/`Section.section_kind`), **`layout.py`** (`CONTENT_H`, shared content-unit
  height fns, `paginate()` section-level reflow), **`blocks.py`/`consume.py`** (declarative F/V/X → `_reserved`; per-asset
  V-qualities on figures; first `region`-class use; conditional emission so a no-genre doc is E4.1-identical).
- **Examples + tests:** whitepaper example now carries `genre: whitepaper` + a figure `asset` override (regenerated,
  2→5 pages); new `grant_proposal.yaml` (1 model page → 4 canvas pages, reflow demo); **19 new tests** (`test_contracts`
  + `test_region_class` + `test_reflow` + `test_model_neutrality`) + a frozen no-contract golden.
- **Green + verified:** `document_generator` **37/37** (18 + 19), `ruff` clean; CLI `document-generator build
  grant_proposal.yaml` → `canvas-std validate` → `adna_native [OK]` + D-1/D-2/D-3. **No regression** (`canvas_std` 46/8 ·
  `brief_consumer` 10/10 · `deck_generator` 16/16); **`canvas_std` git-diff 0** (two-shelf firewall held); `model.py`
  AST-guarded against any `canvas_std` import.
- **`CANVAS-L-002` addressed** by section-level reflow (residual → PT P5); structural `iii/` review **0 High / 0 Med**
  (`iii/feedback_2026_06_20_document_generator_e4_2.md`); **1 new spec-gap erratum candidate** (derived-surface backing
  node) + the prior sequence-unit erratum **sharpened** (region now exercised) → LIP queue.
- **No gate advanced** (E5→E6 stays the human gate). **PHASE E4 COMPLETE** (E4.1–E4.4 all done).
- *(Prior session: E4.1 built — `document_generator` 18/18, first `code`-component use. Earlier: D3 touch `adr_005`
  ratified; Cartography closed; Keystone E0–E2 46/8; E3.1–E3.4 cutover; E4.3/E4.4 consumers; E4→E5 crossed; ADR-004
  ratified; E5.1 `iii/` wrapper active @ v0.5.0 + first review.)*

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip) — **superseded 2026-06-14 (E3.4)**: now carries supersession banners → Canvas.aDNA v2.0.0. Invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for the E3.2 shim).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3) — feeds E4.

## Active Blockers

- **None — OPERATION KEYSTONE COMPLETE (2026-06-20).** Core deliverable shipped + green; no Keystone work remains.
- **Deferred (not blockers) → PT P5:** E5.2 federation rollout + the ~8 consumer-wrapper refederations (the 55
  `test_federation_validation.py` reds — all relocation `FileNotFoundError`, **not** a floor/Standard regression) +
  `canvas_core` relocation (ADR-004) + v2.0.0 registry registration + FU1/FU2 + parity re-baseline + the
  `CANVAS-L-002` residual + shim-retirement execution (2027-06-13). Register: `e6_3_handoff_register.md` §A.
- **LIP queue (`adr_003`) — CLOSED 2026-06-20** (`mission_lip_queue_errata` + closeout `session_…_200612`): **B1 ✅**
  (`validate_anchors`) + **B3 ✅** (pagination clarified) + **B2 ✅** (operator chose ride-on-text — `spec_component_model`
  §4.4 + `LONGFORM_SEMANTIC_TYPES` + `adna_longform_quote` fixture/test) all shipped in **v2.0.1**. **B4** (operator chose
  pure-metadata) is a **MINOR** A-5 relaxation → **direction locked, pending a lattice-labs LIP (≥7-day) → v2.1.0** (no
  code yet). Disposition: `what/decisions/lip_queue_disposition.md`. **Remaining LIP tail = the B4 LIP submission** +
  optional Δ2 LIP (E5.3).
- **v2.0.1 release — CUT 2026-06-20** (operator authorized): B1+B3+B2 at `STANDARD_VERSION=2.0.1` (one-shot bump per
  the disposition); `canvas_std` **80/10** + `ruff` clean; no consumer regression (37/16/10); 4 examples + the B2
  fixture validate `[OK]` (`canvas-std 2.0.1`). Schema `$id` kept at v2.0.0 (structural-unchanged); fixtures'
  `adna_version` stays 2.0.0; spec doc *titles* name the v2.0.x line (prose, unbumped).
- **Shim:** `canvas_core→canvas_std` stays live to the E-D2 window (2027-06-13); retirement scheduled (memo to Hestia
  for Home.aDNA §C — `who/coordination/coord_2026_06_20_mondrian_to_hestia_shim_retirement_schedule.md`).
- **Pushes:** the v2.0.1-cut batch — **`da93bbd` (E6) + `fc1a42d` (LIP queue) + the v2.0.1-cut commit** — **pushed
  2026-06-20** (operator authorized; all `@{u}..HEAD` were operator-authored). Prior batches (`72e3383` E4.2 ·
  `2236405` wind-down) already upstream.

## Next Steps

1. ✅ **OPERATION KEYSTONE COMPLETE (2026-06-20)** — E0–E2 reference impl (46/8) · E3 parity-gated cutover · E4 three
   in-vault consumers (10 · 16 · 37) · E5.1 `iii/` wrapper · **E6 validation & cutover** (E6.1 GREEN · E6.2 confirmed ·
   E6.3 AAR). Campaign `status: completed`.
2. **→ PT P5 (Hestia / production tidy):** when the `canvas_core` relocation is scheduled, execute handoff register §A
   — relocate `canvas_core` (ADR-004), repoint the ~8 consumer wrappers (turns the 55 `test_federation_validation.py`
   reds green), register v2.0.0, re-baseline parity, FU1/FU2, then evaluate the shim ref-sweep for retirement
   (2027-06-13). Ping Mondrian to re-verify the staged exemplar resolver.
3. **LIP queue (`adr_003`) — CLOSED 2026-06-20:** B1 + B3 + **B2** (ride-on-text) shipped in **v2.0.1** (cut + pushed);
   **B4** (pure-metadata) direction-locked. **Only remaining LIP item:** submit the **B4** LIP to
   `lattice-labs/how/governance/lips/` and run the ≥7-day review → land the A-5 relaxation in **v2.1.0** (cross-vault,
   calendar-gated, operator-owned). Disposition: `what/decisions/lip_queue_disposition.md`.
4. **Optional:** submit the Δ2 canvas-as-primitive LIP (E5.3); produce the migration-parity context guide
   (graduation §D).
5. **→ PT P5 (Hestia / production tidy):** unchanged — `canvas_core` relocation + the ~8 wrapper refederations +
   v2.0.0 (or v2.0.1) registry registration + parity re-baseline (handoff register §A).
6. **Push:** ✅ done 2026-06-20 — the v2.0.1-cut batch (E6 `da93bbd` + LIP `fc1a42d` + the cut commit) pushed.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
