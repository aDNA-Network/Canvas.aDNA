---
type: state
created: 2026-06-06
updated: 2026-06-13
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260613_175037_keystone_e0_3
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Operation Cartography (genesis planning) CLOSED 2026-06-13 ✅. Now in EXECUTION — Operation Keystone ACTIVE; PHASE E0 ✅ COMPLETE (E0.1–E0.3); E1 next.**
`how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md`

Operation Cartography (P0–P5) ratified the **aDNA Canvas Standard v2.0.0** + contracts + build charter, then **closed at the operator gate** (context graduation → `context_canvas_standard_doctrine`). The operator **activated Operation Keystone** (the build). **Phase E0 (bootstrap) complete:** E0.1 skeleton (`adna-canvas-std`, Python ≥3.11) · E0.2 verbatim KEEP floor in `schema.py` (`is_floor_loaded()`→True) · E0.3 golden fixtures + harness (`tests/fixtures/` core/extended/aDNA-native/negative + `manifest.json` + `test_fixtures.py`; checkable assertions pass, `validate`/`strip` xfail-until-E1). **Building is in scope** (C3 lifted); producer migrations are parity-gated. *(Planning history: `campaign_canvas_genesis_planning/`.)*

## ▶ Resume Here — Operation Keystone E1 (implement against the frozen API + fixtures)

**Phase E0 (bootstrap) is complete** — skeleton + verbatim KEEP floor + golden fixtures/harness, all verified
(direct runs). **Next phase: E1** — implement behavior against the frozen API and the E0.3 golden corpus, starting
with **E1.1** (`validate(doc, level)` for Core/Extended → the C-*/E-* checks in `validate.py`; the
`invalid_missing_arrow` fixture must reject, the others pass). Then E1.2 (`to_canvas`/`from_canvas`/
`compute_sync_hash`), E1.3 (`diff`/`merge`), E1.4 (`_reserved` validators → A-* checks), E1.5 (`strip` + the
D-1..D-3 degradation tests). As each lands, the matching `xfail` in `tests/test_fixtures.py` auto-flips to PASS —
a built-in acceptance signal.

**Build hygiene:** `cd what/code/canvas_std && make install` to get `pytest` (system Python 3.14 lacks it; E0 was
verified via direct `PYTHONPATH=src python3` runs). Keystone phase gates stay human gates — **E3** (CanvasForge
migration; parity vs Wilhelm 8.80 / Issue 01 8.43) + **E6** (cutover) are load-bearing; **do not start E3 without
the operator.** Tracking: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active).

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]); III/SiteForge upstream notes; III pin confirm at E5.1.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds the P4 execution charter; informs D2/D4/D7. Opens no phase, builds no code (C3). Operation Cartography itself is **unchanged** (P0-ratified / P1-awaiting-go).

## What's Done (this session — Keystone E0.3, 2026-06-13)

- **E0.3:** authored golden-canvas fixtures under `what/code/canvas_std/tests/fixtures/` — `core_minimal`, `extended_styled`, `adna_native` (populated `_reserved` + `_lattice_meta`; doubles as the degradation case), `invalid_missing_arrow` (negative) + `manifest.json`.
- `tests/test_fixtures.py` harness: now-checkable assertions (JSON shape, required fields, declared level) + `validate`/`strip` marked `xfail(strict=False)` until E1 (auto-flip to PASS when E1 lands). **Verified** via direct run — 4 fixtures well-formed, all checkable assertions pass.
- + `mission_e0_3_fixtures`; CHANGELOG. **Phase E0 complete** (E0.1–E0.3 ✅); E1 next.
- *(Earlier this run: closed Cartography + activated Keystone + E0.1 skeleton; E0.2 KEEP floor.)*

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip); invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for D2).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3).

## Active Blockers

- None blocking. **HELD at the E0→E1 phase boundary** for an operator check-in. `pytest` not in system Python — `make install` before E1. Load-bearing gates ahead: E3 (CanvasForge migration) + E6 (cutover).

## Next Steps

1. ✅ **Operation Cartography CLOSED** 2026-06-13 — Standard v2.0.0 ratified across P0–P5; context graduated.
2. ✅ **Keystone Phase E0 COMPLETE** — E0.1 skeleton · E0.2 verbatim KEEP floor · E0.3 golden fixtures + harness.
3. **Next: Phase E1** — implement validators / round-trip / `_reserved` / conformance against the frozen API + the golden fixtures (E1.1 `validate` Core/Extended first; the negative fixture must reject). Each E1 sub-mission auto-flips its `xfail` fixture test to PASS.
4. Ahead: E2 publish v2.0.0 schema+CLI · **E3 CanvasForge migration (parity-gated, highest-risk; operator gate)** · E4 LF-successor + net-new · E5 rollout + `iii/` wiring · E6 cutover. Side-tracks: Δ2 LIP; III/SiteForge upstream notes.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
