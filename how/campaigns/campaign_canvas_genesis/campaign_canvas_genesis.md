---
campaign_id: campaign_canvas_genesis
type: campaign
title: "Operation Keystone — aDNA Canvas Standard v2.0.0, execution (build & migrate)"
owner: stanley
status: active
activated: 2026-06-13
phase_count: 7
mission_count: 22
estimated_sessions: "20-30"
estimation_class: build-broad
priority: high
created: 2026-06-12
updated: 2026-06-19
last_edited_by: agent_stanley
predecessor: campaign_canvas_genesis_planning
tags: [campaign, execution, build, canvas, standard, platform]
---

# Campaign: Operation Keystone (execution)

> **EXECUTION campaign — the build plan.** Authored as the **P4 deliverable** of Operation Cartography
> (`campaign_canvas_genesis_planning`). **🔄 ACTIVATED 2026-06-13** (operator, at the Cartography close gate) —
> `status: active`; **E0.1 in progress.** It is the keystone that makes the v2.0.0 Standard load-bearing: it
> builds the `canvas_std` reference implementation and migrates the producers onto it. Unlike the planning
> campaign, **this campaign builds runtime + migrates code** — every producer migration is parity-gated.

## Goal

Ship the **ratified aDNA Canvas Standard v2.0.0** as running infrastructure: a `canvas_std` reference
implementation (validators · round-trip converters · conformance harness) per Option P, a published schema +
conformance CLI, CanvasForge migrated to consume the Standard via `federation_ref` behind a deprecation shim, the
LiteratureForge-successor stood up as a federated producer, and ≥1 net-new consumer — all with **no output
regression** against locked baselines.

## Context

Operation Cartography (planning) ratified: the v2.0.0 spec set (`spec_adna_canvas_standard` + component model /
panel-link / round-trip v2 / context-object), `adr_001` (**D2 = extract**), `adr_002` (**D3 = schema-absorb +
federated pipeline**), `adr_003` (**D6 governance**), and the P3 conformance + federation contracts. This campaign
executes those contracts. Builds on the verbatim KEEP floor (the `CanvasBuilder` constants + schema) extracted
from `CanvasForge.aDNA/what/code/canvas_core/core.py`, and mirrors the working `lattice-protocol→canvasforge`
extraction-shim precedent.

## Scope

### In Scope (BUILD — gated)
- Build `what/code/canvas_std/` (the reference impl): validators, round-trip converters (`to_canvas`/`from_canvas`
  aliasing `build`/`read_back`), `_reserved` schema validators, conformance harness, degradation tests.
- Publish the v2.0.0 JSON Schema + a conformance CLI; register v2.0.0.
- Migrate CanvasForge onto `canvas_std` (federation_ref + deprecation shim); stand up the LF-successor producer;
  build ≥1 net-new consumer. Parity/regression gates; cutover + rollback.

### Out of Scope
- Re-deciding any ratified ADR/spec (D2–D7 are settled; changes go through the LIP process, `adr_003`).
- The Δ2 canvas-as-primitive elevation (separate open LIP, `lip_draft_canvas_as_primitive`).
- New Standard features beyond v2.0.0 (minor bumps via the governed process).

## Phases & Missions

> Missions kept thin until phase entry (SO-3). Phase deliverables are binding; objectives authored at entry.
> Phase gates are human gates (SO-1). **E3 is the highest-risk phase (parity-gated CanvasForge migration).**

### Phase E0 — Bootstrap `canvas_std`
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| E0.1 | Stand up `what/code/canvas_std/` package skeleton (layout, packaging, CI, license) | 1 | ✅ **done 2026-06-13** ([[how/campaigns/campaign_canvas_genesis/missions/mission_e0_1_canvas_std_skeleton\|mission]]) |
| E0.2 | Port the KEEP floor verbatim — 10 `VALID_*` enums + node/edge schema + `TYPE_MAPPING`/`EDGE_TYPE_MAPPING` (lattice profile) | 1-2 | ✅ **done 2026-06-13** ([[how/campaigns/campaign_canvas_genesis/missions/mission_e0_2_keep_floor\|mission]]) |
| E0.3 | Golden-canvas fixtures + test harness (Core/Extended/aDNA-Native + degradation) | 1 | ✅ **done 2026-06-13** ([[how/campaigns/campaign_canvas_genesis/missions/mission_e0_3_fixtures\|mission]]) |

> **Build progress (2026-06-13) — PHASE E0 COMPLETE ✅:** E0.1 skeleton · E0.2 verbatim KEEP floor (`schema.py`,
> `is_floor_loaded()`→True) · E0.3 golden fixtures (`tests/fixtures/`: core/extended/aDNA-native + a negative,
> a `manifest.json`, and `test_fixtures.py` — now-checkable assertions pass; `validate`/`strip` xfail-until-E1).
> **Next: phase E1** — implement validators / round-trip / `_reserved` validators / conformance harness against
> the frozen API + the golden fixtures (E1.1 Core/Extended validate first). *(HELD at the E0→E1 phase boundary
> for an operator check-in.)*

### Phase E1 — Reference implementation
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| E1.1 | Validator (C-*/E-* checks per `spec_conformance_suite`; A-* deferred to E1.4) | 2 | ✅ **done 2026-06-13** ([[how/campaigns/campaign_canvas_genesis/missions/mission_e1_1_validate\|mission]]) |
| E1.2 | Round-trip converters (`to_canvas`=`build`, `from_canvas`=`read_back`) + `compute_sync_hash` | 2 | ✅ **done 2026-06-13** |
| E1.3 | Advisory reverse path — `diff` / `merge` (3-way) / `preserve_positions` | 1-2 | ✅ **done 2026-06-13** |
| E1.4 | `_reserved` schema validators (component_types / semantic_bindings / panel_link / context_object) → A-* checks | 2 | ✅ **done 2026-06-13** |
| E1.5 | Degradation (`strip`) + D-1..D-3 tests as a first-class suite | 1 | ✅ **done 2026-06-13** (closes E1) |

> **Build progress (2026-06-13) — PHASE E1 COMPLETE ✅ (reference engine done):** E1.1 `validate` (Core/Extended/
> aDNA-Native, C-*/E-*/A-*) · E1.2 round-trip (`to_canvas`/`from_canvas`/`compute_sync_hash`) · E1.3 `diff`/`merge`/
> `preserve_positions` · E1.4 `_reserved` validators · E1.5 `strip` + degradation (D-1..D-3). The golden-fixture
> xfails are retired; **`pytest` = 30 passed / 4 skipped, `ruff` clean** (run in `.venv`). Only `validate_suite`
> (E2.1) + the CLI (E2.3) remain stubbed. **Next: phase E2** — conformance harness + publish v2.0.0 schema + CLI.
> *(HELD at the E1→E2 phase boundary for an operator check-in.)*

### Phase E2 — Conformance suite + publish
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| E2.1 | Conformance harness `validate_suite(doc, declared) → ConformanceReport` | 1-2 | ✅ **done 2026-06-13** |
| E2.2 | Canonical conformance corpus (per-level + degradation fixtures) | 1 | ✅ **done 2026-06-13** |
| E2.3 | Publish v2.0.0 JSON Schema + conformance CLI; register v2.0.0 | 1-2 | ✅ **done 2026-06-13** (closes E2; registry → E5) |

> **Build progress (2026-06-13) — PHASE E2 COMPLETE ✅ (reference impl + tooling done):** E2.1 `validate_suite →
> ConformanceReport` · E2.2 conformance corpus (`test_conformance.py`) · E2.3 the v2.0.0 **JSON Schema**
> (`src/canvas_std/data/adna_canvas_v2.schema.json`, loadable via `json_schema()`) + the **`canvas-std` CLI**
> (`validate`/`schema`; auto-level-detect; exit 0/1). `pytest` 46 pass / 8 skip, `ruff` clean — **no stubs
> remain.** Registry/federation registration deferred to E5 rollout. **The reference implementation is complete.**
> **⛔ HELD at the E2→E3 phase boundary** — E3 is the parity-gated CanvasForge migration (operator gate; parity
> vs Wilhelm 8.80 / Issue 01 8.43). Do not start E3 without the operator.

### Phase E3 — CanvasForge migration (parity-gated) ⚠️ highest risk
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| E3.1 | Introduce the `canvas/` federation wrapper in CanvasForge (federation_ref + graft) | 1 | ✅ **done 2026-06-13** ([[how/campaigns/campaign_canvas_genesis/missions/mission_e3_1_canvasforge_wrapper\|mission]]) |
| E3.2 | Repoint `canvas_core` → `canvas_std` behind a **deprecation shim** (mirror lattice-protocol precedent) | 2-3 | ✅ **done 2026-06-13** (constants-only; suite green at parity) ([[how/campaigns/campaign_canvas_genesis/missions/mission_e3_2_canvas_core_shim\|mission]]) |
| E3.3 | **Parity/regression gate** — no CanvasForge output regresses vs locked baselines (Wilhelm 8.80 / Issue 01 8.43) | 2 | ✅ **done 2026-06-13 — GREEN** (deterministic structural proof; shim output-neutral) ([[how/campaigns/campaign_canvas_genesis/missions/mission_e3_3_parity_gate\|mission]]) |
| E3.4 | Cutover criteria + rollback rehearsal; retire the embedded v1.0.0 framing (supersede) | 1-2 | ✅ **done 2026-06-14** — full cutover; v1.0.0 framing superseded; shim retire scheduled E6.2 ([[how/campaigns/campaign_canvas_genesis/missions/mission_e3_4_cutover\|mission]]) |

> **Phase progress (2026-06-13) — PHASE E3 OPENED 🔄 (operator-authorized gate crossing); E3.1 ✅ done:** the
> operator approved crossing the E2→E3 human gate; all four E3 missions are chartered (SO-3). **E3.1 is complete** —
> the additive `canvas/` federation wrapper landed in `CanvasForge.aDNA` (`federation_ref` → Canvas.aDNA v2.0.0 +
> `graft_manifest.yaml`; commit `7bb833f`; `canvas_core` untouched, baseline `3ce4d341` intact). The LP↔Canvas seam
> was formalized two-sided the same day (Mondrian's countersign of Noether's seam memo), so the shim work (E3.2) — a
> §3.3 "seam-touching" change — proceeded on a settled contract. **E3.2 ✅ done 2026-06-13** — the constants-only
> `canvas_core`→`canvas_std` deprecation shim landed (the 10 `VALID_*` enums + `TYPE_MAPPING`/`EDGE_TYPE_MAPPING`
> rebound to `canvas_std.schema` behind a `DeprecationWarning` + `DEPRECATED_STUB` marker; CanvasForge suite green
> at parity — 957 passed / 5 skipped, baseline `3ce4d341` intact; E-D2 = 12mo, registered Home.aDNA §C). **E3.3
> (the load-bearing parity gate — Wilhelm 8.80 / Issue 01 8.43) is ✅ GREEN 2026-06-13** — the shim is proven
> output-neutral by a deterministic structural proof (A/B normalized-canvas SHA identical shim-ON vs shim-OFF
> `aa675665…`; 0 federated-floor rejects; baseline `3ce4d341` untouched; suite 900/3). **E3.4 ✅ done 2026-06-14** —
> full cutover (operator-gated): cutover criteria met, rollback rehearsed net-zero, the embedded v1.0.0 framing
> superseded (banners; archive-never-delete), shim retirement scheduled at E6.2. **PHASE E3 COMPLETE. ⛔ HELD at the
> E3→E4 boundary** — E4 (LF-successor + net-new consumer) is the next phase and is a human gate.

> **Phase progress (2026-06-19) — pt09 reshape reconciled; Hestia loop closed (no gate change):** pt09 (2026-06-17)
> folded the "CanvasForge as a *separate* federated producer" premise; **[[what/decisions/adr_004_production_code_layout|ADR-004]] (proposed 2026-06-19)**
> resolves the E4 **code-layout** reconciliation — `canvas_core` → `Canvas.aDNA/what/production/canvas_core/` (import
> kept; env `CANVAS_CORE_HOME`; depends on installed `adna-canvas-std`), answering Hestia's substrate-path memo.
> **Hearthstone P3 unblocked + loop closed** — Hestia staged the exemplar same-day and acked (Home §C #39 env-var
> alias registered). The two former E3.4 follow-ups (canvas/-routing SO; round-trip-function dedup) are now
> **contracted PT P5 items** in ADR-004's checklist. **Still ⛔ HELD at E3→E4** — this resolved the *layout*, not the
> gate; no code moved.

> **🔓 PHASE E4 OPENED (2026-06-19) — operator-authorized E3→E4 gate crossing; E4 table reconciled to in-vault
> production (pt09).** The operator authorized crossing the E3→E4 human gate and selected the **net-new consumer
> (E4.3)** as the first build thread (planning gate + plan approval, 2026-06-19). The E4/E5 plan is reconciled to the
> post-pt09 reality (the *federated-producer* topology is folded; production is in-vault):
> - **E4.1 / E4.2 (LF-successor):** reframed *federated → **in-vault*** — pt09 absorbed production into Canvas and
>   LiteratureForge was wound down (its assets are a Canvas quarry), so the successor is an in-vault production layer,
>   not a separate federated vault. **⚠ Governance flag:** `adr_002` (D3) ratified *"schema-absorb + **federated**
>   pipeline"*; the in-vault reality supersedes the *federated* leg. This needs a **governed touch** (an `adr_002`
>   amendment or a new ADR via the `adr_003` LIP process) before E4.1/E4.2 are *built* — **flagged, not resolved here**
>   (the operator chose E4.3). Charter-stubbed only.
> - **E4.3 (net-new consumer):** **🔄 in progress (this session).** Unchanged by pt09 and buildable now on `canvas_std`
>   alone (zero PT-P5 dependency) — `[[how/campaigns/campaign_canvas_genesis/missions/mission_e4_3_net_new_consumer|mission_e4_3]]`.
> - **E4.4 (deck pilot):** steps 1–3 buildable on `canvas_std`; **step-4 render loop is PT-P5-gated** (needs
>   `canvas_presentation`, which lands at PT P5). Charter-stubbed.
> - **E5.2:** stale producer names corrected — **ComfyForge → ComfyUI**, **SiteForge → Astro** (renamed PT pt06/pt07);
>   the federation-rollout premise still holds (they remain consumers federating against Canvas).
>
> **Human-gate discipline:** only **E3→E4** was authorized — **E4→E5 remains a future human gate; do not auto-advance.**

> **Phase progress (2026-06-19 PM) — E4.3 + E4.4 DONE (both green):** two runnable consumers now sit on the
> `what/production/` shelf, proven on `canvas_std` alone (zero PT-P5 dependency): **`brief_consumer`** (E4.3 —
> single-page brief → aDNA-Native `.canvas`; 10/10) and **`deck_generator`** (E4.4 — multi-slide deck → aDNA-Native
> `.canvas`; slides = groups, deck = the one canonical surface, `sequence` chain, **image + table** components; 16/16).
> `canvas_std` itself unchanged (46/8). The deck's persona-III + accuracy method is captured as a contract
> (`deck_generator/iii_quality_contract.md`; wired at E5.1). **Remaining E4 = E4.1/E4.2 (LF-successor), ⛔ gated on the
> D3 governed touch.** Still ⛔ HELD at **E4→E5**.

### Phase E4 — net-new consumer + LF-successor (in-vault, pt09-reshaped)
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| E4.3 | ≥1 net-new consumer end-to-end (`brief_consumer`) on `canvas_std` — **the first build** | 1-2 | ✅ **done 2026-06-19** ([[how/campaigns/campaign_canvas_genesis/missions/mission_e4_3_net_new_consumer\|mission]]) |
| E4.4 | Deck-generator pilot (`deck_generator`) as a worked build — deck `.canvas` on `canvas_std`; **step-4 render PT-P5-gated** | 1-2 | ✅ **done 2026-06-19** ([[how/campaigns/campaign_canvas_genesis/missions/mission_e4_4_deck_pilot\|mission]]) |
| E4.1 | Stand up the LF-successor **in-vault** producer (D3-B; ⚠ D3 federated→in-vault needs a governed touch): consume component_model + panel_link + round-trip | 2 | ◻ stub (reshaped; ⛔ gated on D3 touch) |
| E4.2 | Migrate LF visual/format contracts (in-vault; genre pipeline stays producer-side) | 1-2 | ◻ stub (reshaped; ⛔ gated on D3 touch) |

### Phase E5 — Federation rollout + quality wiring
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| E5.1 | Wire the `iii/` wrapper (confirm III pin vs `III.aDNA`); run a real canvas review | 1 | ✅ **done 2026-06-19** ([[how/campaigns/campaign_canvas_genesis/missions/mission_e5_1_iii_wiring\|mission]]) |
| E5.2 | Federation rollout to remaining producers (**ComfyUI** / **Astro** as applicable — renamed from ComfyForge/SiteForge at PT pt06/pt07) | 1-2 | ◻ planned (wrapper refederations PT-P5-coupled) |
| E5.3 | *(optional/parallel)* submit the Δ2 canvas-as-primitive LIP | 1 | ◻ optional |

> **🔓 PHASE E5 OPENED (2026-06-19) — operator-authorized E4→E5 gate crossing** (AskUserQuestion: "Advance to E5" +
> "Ratify ADR-004"). **E4 closed-with-deferral:** E4.3 + E4.4 done; **E4.1/E4.2 (LF-successor) carried forward as
> D3-gated debt** (still needs the `adr_002` amendment / new ADR via the `adr_003` LIP **before** build — advancing did
> not resolve it). **E5.1 ✅ done same session** — the Canvas `iii/` wrapper activated (scaffold → active; III pin
> confirmed **v0.5.0** / `0f06aa6` / lattice 1.2.6; `reviewer_registry` + local learning store wired) and the **first
> real canvas review** ran on `brief_consumer` + `deck_generator` → **0 High / 0 Med** (structural; pixel/VR1
> PT-P5-gated), 3 Low + 1 GRAPH-GAP tracked as errata, `CANVAS-L-001` accumulated local. No regression (`canvas_std`
> 46/8, `brief_consumer` 10/10, `deck_generator` 16/16; `ruff` clean). **ADR-004 ratified** (operator countersign).
> Review artifact: `iii/feedback_2026_06_19_canvas_consumers.md` · mission `mission_e5_1_iii_wiring`. **⛔ Next gate:
> E5→E6 (human gate) — do not auto-advance.**

### Phase E6 — Validation & cutover
| # | Mission | Sessions |
|---|---------|----------|
| E6.1 | Cross-system parity validation (all consumers green) | 1 |
| E6.2 | Final cutover + rollback rehearsal; shim retirement schedule | 1 |
| E6.3 | Campaign AAR + handoff; context graduation | 1 |

## Decision Points (mostly inherited — ratified at Cartography)

| # | Decision | Status |
|---|----------|--------|
| D2 | CanvasForge relationship | ✅ ratified — extract (`adr_001`) |
| D3 | LiteratureForge seam | ✅ ratified — schema-absorb + federated pipeline (`adr_002`) · ⚠ **federated leg OBE post-pt09** (successor is in-vault; LF wound down) → needs a governed touch (adr_002 amendment / new ADR via `adr_003` LIP) **before E4.1/E4.2 build**; flagged 2026-06-19 |
| D6 | Governance / versioning | ✅ ratified (`adr_003`) |
| E-D1 | `canvas_std` language/runtime + packaging | at E0.1 |
| E-D2 | Shim grace-window length for CanvasForge | ✅ **12 months** (expiry 2027-06-13) — decided E3.2 2026-06-13; registered Home.aDNA §C |
| Δ2 | Canvas-as-primitive | open LIP (separate track) |
| ADR-004 | PT P5 production-code layout (`canvas_core` → `what/production/`) | ✅ **ratified 2026-06-19** (operator countersign at the E4→E5 gate) — answers Hestia substrate-path memo; pt09 follow-up. Binds the P5 relocation target; ratification is NOT authorization to move code (relocation = PT P5). |

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| CanvasForge output regression on migration | **High** | E3.3 parity gate vs locked baselines (Wilhelm 8.80 / Issue 01 8.43); shim allows rollback; cutover only on green. |
| `canvas_std` ↔ embedded `CanvasBuilder` drift during migration | High | Single source of truth post-extract; shim re-exports; deprecation window with both paths tested. |
| Round-trip fidelity loss (positions / lossy fields) | Medium | E1.2/E1.3 honor the authority matrix + lossy boundary verbatim (KEEP); golden fixtures. |
| LF-successor scope creep (absorb vs federate) | Medium | D3 ratified = federated; pipeline stays producer-side; no two-faced platform unless a new ADR reopens it. |
| Net-new consumer reveals a spec gap | Medium | Treat as a v2.0.x minor (governed process); feeds back to the spec via LIP/errata. |

## Parity / Regression Strategy

Every producer migration (E3, E4) **MUST** pass a parity gate: regenerate the producer's locked reference outputs
through `canvas_std` and diff against the pre-migration baseline (CanvasForge: Wilhelm 8.80, Issue 01 8.43). Visual
quality via the `iii/` VR1–VR5 contract must not drop. A migration cuts over **only** on a green parity gate;
otherwise it rolls back via the shim.

## Cutover & Rollback

- **Shim model:** `canvas_core` re-exports from `canvas_std` (mirror `lattice-protocol/extensions/canvas/__init__.py`).
  Both paths live during the grace window (E-D2; default 12mo).
- **Cutover criteria:** parity green + conformance suite green + `iii/` review ≥ baseline + operator gate.
- **Rollback:** revert the wrapper repoint; the shim keeps the old path working; no consumer breakage.

## Verification Strategy

Per-mission: tests green + AAR + committed. Per-phase: phase exit criteria + operator gate (E3/E6 are the
load-bearing gates). Campaign-level: all consumers parity-green; v2.0.0 published + registered; shim-retirement
scheduled; context graduation run.

## Hard Constraints

- **Build is now in scope** (this is the execution campaign) — but every producer migration is **parity-gated** and
  **reversible** via the shim. No cutover without a green gate + operator approval.
- Never modify `.adna/`. The aDNA core primitive set stays untouched (Δ2 is a separate LIP).
- Ratified ADRs/specs are fixed inputs; changes go through the `adr_003` LIP process, not ad-hoc edits.
- Every mission ends with SITREP + AAR; phase gates are human gates.

## Activation

**✅ ACTIVATED 2026-06-13** (operator, at the Cartography close gate) — `status: active`. E0.1 (canvas_std package
skeleton) is in progress. E0.2+ proceed per the phase plan; phase gates remain human gates (E3/E6 load-bearing).

## Notes

- Codename **Operation Keystone** (the reference impl is the keystone locking the federation arch).
- Mission count (22) and session estimate (20-30) are planning figures; re-baselined at activation.

## Completion Summary

*Fill out at campaign close.*

## Campaign AAR

*Mandatory before `status: completed`.*
