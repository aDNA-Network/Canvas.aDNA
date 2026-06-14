---
type: state
created: 2026-06-06
updated: 2026-06-13
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260613_182344_keystone_e1_1
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Operation Cartography (genesis planning) CLOSED 2026-06-13 ✅. Now in EXECUTION — Operation Keystone ACTIVE; E0 ✅ + E1.1 (validate) ✅; E1.2 next.**
`how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md`

Operation Cartography (P0–P5) ratified the **aDNA Canvas Standard v2.0.0** + contracts + build charter, then **closed at the operator gate** (context graduation → `context_canvas_standard_doctrine`). The operator **activated Operation Keystone** (the build). **Phase E0 complete** (skeleton + verbatim KEEP floor + golden fixtures/harness). **Phase E1 (reference impl) underway — E1.1 ✅:** `validate(doc, level)` implements the Core + Extended checks in `validate.py` against the KEEP floor + fixtures (core/extended/negative `validate` xfails now PASS; aDNA-Native raises until E1.4). **Building is in scope** (C3 lifted); producer migrations are parity-gated. *(Planning history: `campaign_canvas_genesis_planning/`.)*

## ▶ Resume Here — Operation Keystone E1.2 (round-trip converters)

**Phase E0 done; E1.1 done** — `validate()` Core/Extended is live and verified (core/extended fixtures pass,
negative rejects on C-4, aDNA-Native raises until E1.4). **Next mission: E1.2** — implement the round-trip
converters in `src/canvas_std/roundtrip.py`: `to_canvas` (=`build`) forward source→view, `from_canvas`
(=`read_back`) advisory view→source draft, and `compute_sync_hash` (16-hex SHA-256 over sorted node ids + sorted
`from→to` edges) per `spec_roundtrip_protocol_v2` §3–§4. Then E1.3 (`diff`/`merge`), E1.4 (`_reserved` validators
→ A-* checks; flips the `adna_native` validate-xfail), E1.5 (`strip` + the D-1..D-3 degradation tests → flips the
degradation xfails). Each landed mission auto-flips its `xfail` in `tests/test_fixtures.py` to PASS.

**Build hygiene:** `cd what/code/canvas_std && make install` to get `pytest` (system Python 3.14 lacks it; E0 was
verified via direct `PYTHONPATH=src python3` runs). Keystone phase gates stay human gates — **E3** (CanvasForge
migration; parity vs Wilhelm 8.80 / Issue 01 8.43) + **E6** (cutover) are load-bearing; **do not start E3 without
the operator.** Tracking: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active).

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]); III/SiteForge upstream notes; III pin confirm at E5.1.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds the P4 execution charter; informs D2/D4/D7. Opens no phase, builds no code (C3). Operation Cartography itself is **unchanged** (P0-ratified / P1-awaiting-go).

## What's Done (this session — Keystone E1.1, 2026-06-13)

- **E1.1:** implemented `validate(doc, level)` Core (C-1..C-5) + Extended (E-1..E-4) in `what/code/canvas_std/src/canvas_std/validate.py` against the KEEP floor; monotone levels; **C-4 requires an explicit `toEnd`** (omitted → reject). aDNA-Native delegates A-* to `reserved.py` (NotImplementedError until E1.4); `strip` stays E1.5.
- Updated `test_smoke.py` (`validate` removed from NotImplemented-stubs + liveness check). **Verified** via direct run: core/extended fixtures validate clean, negative rejects on C-4, aDNA-Native valid@Extended / raises@aDNA-Native, a broken doc surfaces C-2/C-3/C-4. The core/extended/negative `validate` xfails in `test_fixtures.py` now PASS.
- + `mission_e1_1_validate`; CHANGELOG. Keystone E1.1 ✅ / E1.2 next.
- *(Earlier this run: Cartography closed + Keystone activated; E0.1–E0.3 bootstrap.)*

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip); invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for D2).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3).

## Active Blockers

- None blocking. **Next:** Keystone E1.2 (round-trip converters). `pytest` not in system Python — `make install` to run the suite. Load-bearing gates ahead: E3 + E6 (operator).

## Next Steps

1. ✅ **Operation Cartography CLOSED** 2026-06-13 — Standard v2.0.0 ratified across P0–P5; context graduated.
2. ✅ **Keystone** — E0 (bootstrap: skeleton + KEEP floor + fixtures/harness) + **E1.1 `validate` Core/Extended** done.
3. **Next: E1.2** — round-trip converters (`to_canvas`/`from_canvas`/`compute_sync_hash` in `roundtrip.py`); then E1.3 `diff`/`merge` → E1.4 `_reserved` validators (flips the `adna_native` xfail) → E1.5 `strip` + degradation (flips the degradation xfails).
4. Ahead: E2 publish v2.0.0 schema+CLI · **E3 CanvasForge migration (parity-gated, highest-risk; operator gate)** · E4 LF-successor + net-new · E5 rollout + `iii/` wiring · E6 cutover. Side-tracks: Δ2 LIP; III/SiteForge upstream notes.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
