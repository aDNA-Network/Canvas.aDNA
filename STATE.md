---
type: state
created: 2026-06-06
updated: 2026-06-13
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260613_182952_keystone_e1_finish
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Operation Cartography (genesis planning) CLOSED 2026-06-13 ✅. Now in EXECUTION — Operation Keystone ACTIVE; PHASE E0 ✅ + PHASE E1 ✅ (reference engine done); E2 next.**
`how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md`

Operation Cartography (P0–P5) ratified the **aDNA Canvas Standard v2.0.0** + contracts + build charter, then **closed at the operator gate** (context graduation). The operator **activated Operation Keystone** (the build). **Phase E0 done** (skeleton + KEEP floor + golden fixtures). **Phase E1 (reference engine) COMPLETE:** `validate` (Core/Extended/aDNA-Native), `strip` + degradation, round-trip (`to_canvas`/`from_canvas`/`compute_sync_hash`), `diff`/`merge`/`preserve_positions`, the `_reserved` A-* validators — **`pytest` 30 passed / 4 skipped, `ruff` clean**. Only `validate_suite` (E2.1) + the CLI (E2.3) remain stubbed. **Building is in scope** (C3 lifted); producer migrations are parity-gated. *(Planning history: `campaign_canvas_genesis_planning/`.)*

## ▶ Resume Here — Operation Keystone E2 (conformance harness + publish)

**Phases E0 + E1 are done** — the reference **engine** is complete and green (`validate` all levels, `strip`+
degradation, round-trip, `diff`/`merge`, `_reserved` validators; `pytest` 30 pass / 4 skip; `ruff` clean). **Next
phase: E2** — **E2.1** implement the conformance harness `validate_suite(doc, declared) → ConformanceReport`
(`conformance.py`; runs C-*/E-*/A-* + the D-1..D-3 degradation report; the report shape is already defined) →
**E2.2** the canonical conformance corpus → **E2.3** publish the v2.0.0 JSON Schema + wire the `canvas-std` CLI
(`_cli` in `conformance.py`) + register v2.0.0. `validate_suite` + `_cli` are the only remaining stubs.

**Build hygiene:** the suite runs in a `.venv` (`cd what/code/canvas_std && make install && make test`; system
Python 3.14 lacks pytest). `.venv`/`*.egg-info`/`__pycache__` are gitignored. **After E2 comes E3 — the
parity-gated CanvasForge migration (operator gate; parity vs Wilhelm 8.80 / Issue 01 8.43) — do not start it
without the operator.** Tracking: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active).

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]); III/SiteForge upstream notes; III pin confirm at E5.1.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds the P4 execution charter; informs D2/D4/D7. Opens no phase, builds no code (C3). Operation Cartography itself is **unchanged** (P0-ratified / P1-awaiting-go).

## What's Done (this session — Keystone E1.2–E1.5, Phase E1 complete, 2026-06-13)

- **Finished Phase E1 (reference engine)** in four committed+verified missions: E1.2 round-trip (`to_canvas`/`from_canvas`/`compute_sync_hash`) · E1.3 `diff`/`merge`/`preserve_positions` · E1.4 `_reserved` validators (A-* checks) · E1.5 `strip` + degradation (D-1..D-3).
- Retired the fixture `xfail` markers; reordered `__init__.py` for ruff. Ran the **real suite in a `.venv`** (`make install`): **`pytest` 30 passed / 4 skipped, `ruff` clean**.
- + `mission_e1_2..e1_5`; CHANGELOG. Only `validate_suite` (E2.1) + the CLI (E2.3) remain stubbed. **Phase E1 complete.**
- *(Earlier this run: Cartography closed + Keystone activated; E0 bootstrap + E1.1 validate.)*

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip); invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for D2).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3).

## Active Blockers

- None blocking. **HELD at the E1→E2 phase boundary** for an operator check-in. The suite runs in a `.venv` (`make install`). Load-bearing gate ahead: **E3** CanvasForge migration (operator).

## Next Steps

1. ✅ **Operation Cartography CLOSED** 2026-06-13 — Standard v2.0.0 ratified across P0–P5; context graduated.
2. ✅ **Keystone E0 (bootstrap) + E1 (reference engine) COMPLETE** — `validate`/`strip`/round-trip/`diff`/`merge`/`_reserved` validators; `pytest` 30 pass / 4 skip, `ruff` clean.
3. **Next: Phase E2** — E2.1 conformance harness (`validate_suite` → `ConformanceReport`) → E2.2 conformance corpus → E2.3 publish the v2.0.0 JSON Schema + wire the `canvas-std` CLI + register v2.0.0.
4. Then: **E3 CanvasForge migration (parity-gated, highest-risk; operator gate)** · E4 LF-successor + net-new · E5 rollout + `iii/` wiring · E6 cutover. Side-tracks: Δ2 LIP; III/SiteForge upstream notes.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
