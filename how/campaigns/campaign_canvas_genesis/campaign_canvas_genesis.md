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
updated: 2026-06-13
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
| E3.1 | Introduce the `canvas/` federation wrapper in CanvasForge (federation_ref + graft) | 1 | 🔄 **in-progress 2026-06-13** ([[how/campaigns/campaign_canvas_genesis/missions/mission_e3_1_canvasforge_wrapper\|mission]]) |
| E3.2 | Repoint `canvas_core` → `canvas_std` behind a **deprecation shim** (mirror lattice-protocol precedent) | 2-3 | ⏳ chartered ([[how/campaigns/campaign_canvas_genesis/missions/mission_e3_2_canvas_core_shim\|mission]]) |
| E3.3 | **Parity/regression gate** — no CanvasForge output regresses vs locked baselines (Wilhelm 8.80 / Issue 01 8.43) | 2 | ⏳ chartered ([[how/campaigns/campaign_canvas_genesis/missions/mission_e3_3_parity_gate\|mission]]) |
| E3.4 | Cutover criteria + rollback rehearsal; retire the embedded v1.0.0 framing (supersede) | 1-2 | ⏳ chartered ([[how/campaigns/campaign_canvas_genesis/missions/mission_e3_4_cutover\|mission]]) |

> **Phase progress (2026-06-13) — PHASE E3 OPENED 🔄 (operator-authorized gate crossing):** the operator approved
> crossing the E2→E3 human gate; all four E3 missions are chartered (SO-3) and **E3.1 is in-progress** — the
> additive `canvas/` federation wrapper in `CanvasForge.aDNA` (`federation_ref` → Canvas.aDNA v2.0.0, no code
> repoint). The LP↔Canvas seam was formalized two-sided the same day (Mondrian's countersign of Noether's seam
> memo), so the shim work (E3.2) — a §3.3 "seam-touching" change — proceeds on a settled contract. **E3.2 (the
> `canvas_core`→`canvas_std` deprecation shim) is the first consequential code change and begins next session.**
> E3.3 is the load-bearing parity gate (Wilhelm 8.80 / Issue 01 8.43); E3.4 cutover is operator-gated.

### Phase E4 — LF-successor + net-new consumer
| # | Mission | Sessions |
|---|---------|----------|
| E4.1 | Stand up the LF-successor federated producer (D3-B): consume component_model + panel_link + round-trip | 2 |
| E4.2 | Migrate LF visual/format contracts into the consumer wrapper (genre pipeline stays producer-side) | 1-2 |
| E4.3 | ≥1 net-new consumer end-to-end (letter / web / paper) | 1-2 |
| E4.4 | Deck-generator pilot (parked `mission_deck_generator_canvas_pilot`) as a worked build | 1-2 |

### Phase E5 — Federation rollout + quality wiring
| # | Mission | Sessions |
|---|---------|----------|
| E5.1 | Wire the `iii/` wrapper (confirm III pin vs `III.aDNA/STATE.md`); run a real canvas review | 1 |
| E5.2 | Federation rollout to remaining producers (ComfyForge / SiteForge as applicable) | 1-2 |
| E5.3 | *(optional/parallel)* submit the Δ2 canvas-as-primitive LIP | 1 |

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
| D3 | LiteratureForge seam | ✅ ratified — schema-absorb + federated pipeline (`adr_002`) |
| D6 | Governance / versioning | ✅ ratified (`adr_003`) |
| E-D1 | `canvas_std` language/runtime + packaging | at E0.1 |
| E-D2 | Shim grace-window length for CanvasForge | at E3.2 (default 12mo, per lattice-protocol precedent) |
| Δ2 | Canvas-as-primitive | open LIP (separate track) |

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
