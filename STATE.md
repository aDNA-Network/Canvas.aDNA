---
type: state
created: 2026-06-06
updated: 2026-06-13
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260613_060751_close_keystone_e0
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Operation Cartography (genesis planning) CLOSED 2026-06-13 ✅. Now in EXECUTION — Operation Keystone ACTIVE; E0.1 ✅ done, E0.2 next.**
`how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md`

Operation Cartography (P0–P5) ratified the **aDNA Canvas Standard v2.0.0** + the conformance/federation contracts + the build charter, then **closed at the operator gate** (context graduation → `context_canvas_standard_doctrine`; `campaign_canvas_genesis_planning` `status: completed`). At the same gate the operator **activated Operation Keystone** (the execution build). **E0.1 ✅** — the `canvas_std` reference-impl skeleton stands up at `what/code/canvas_std/` (Python ≥3.11, frozen public-API stubs, smoke test green). **Building is now in scope** (C3 lifted); producer migrations are parity-gated. *(Planning history: `campaign_canvas_genesis_planning/`.)*

## ▶ Resume Here — Operation Keystone E0.2 (port the KEEP floor)

The Standard is ratified; the reference-impl **skeleton is up** (E0.1 ✅). **Next mission: E0.2** — port the
**verbatim KEEP floor** into `what/code/canvas_std/src/canvas_std/schema.py` (currently empty placeholders):
the 10 `VALID_*` enums + node/edge required-field sets + the `lattice` `TYPE_MAPPING`/`EDGE_TYPE_MAPPING` profile,
transcribed from [[how/campaigns/campaign_canvas_genesis_planning/missions/p1_fork_baseline|p1_fork_baseline]] §3.
`schema.is_floor_loaded()` flips `True` when done. Then **E0.3** (golden-canvas fixtures) → **E1** (implement
`validate`/`strip`, `to_canvas`/`from_canvas`/`compute_sync_hash`/`diff`/`merge`, the `_reserved` validators, the
conformance harness — all against the frozen API).

**Build hygiene:** install dev tooling (`cd what/code/canvas_std && make install`) — system Python 3.14 lacks
`pytest`; E0.1 was verified via a direct run. Keystone phase gates stay human gates (**E3** CanvasForge migration
+ **E6** cutover are load-bearing; parity vs Wilhelm 8.80 / Issue 01 8.43). Tracking:
[[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active) ·
[[how/campaigns/campaign_canvas_genesis/missions/mission_e0_1_canvas_std_skeleton|E0.1 mission]].

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]); III/SiteForge upstream notes; III pin confirm at E5.1.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds the P4 execution charter; informs D2/D4/D7. Opens no phase, builds no code (C3). Operation Cartography itself is **unchanged** (P0-ratified / P1-awaiting-go).

## What's Done (this session — Cartography close + Keystone E0.1, 2026-06-13)

- **Closed Operation Cartography** (operator close gate): context graduation → `what/context/context_canvas_standard_doctrine.md`; flipped `campaign_canvas_genesis_planning` → `status: completed` (Completion Summary + Campaign AAR finalized).
- **Activated Operation Keystone** (`campaign_canvas_genesis` → `status: active`).
- **Executed E0.1:** stood up `what/code/canvas_std/` — the `adna-canvas-std` Python package (src-layout, MIT, `pyproject`/`Makefile`/`README`/`AGENTS`/`CHANGELOG`; frozen public-API stubs across `schema`/`validate`/`roundtrip`/`reserved`/`conformance`; `tests/test_smoke.py`). **Verified:** imports clean (pkg 0.1.0 · Standard 2.0.0), 5/5 stubs raise `NotImplementedError`, levels/versions/empty-floor asserted. + `mission_e0_1_canvas_std_skeleton`.
- Tracking: Keystone E0.1 ✅ / E0.2 next; this STATE.

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip); invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for D2).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3).

## Active Blockers

- None blocking. **Next:** Keystone **E0.2** (port the KEEP floor into `schema.py`). `pytest` not in system Python — `make install` before E1. Load-bearing gates ahead: E3 (CanvasForge migration) + E6 (cutover).

## Next Steps

1. ✅ **Operation Cartography CLOSED** 2026-06-13 — Standard v2.0.0 ratified across P0–P5; context graduated.
2. ✅ **Operation Keystone ACTIVATED** + **E0.1 done** (`canvas_std` skeleton; E-D1 resolved = Python/hatchling).
3. **Next: E0.2** — port the verbatim KEEP floor into `schema.py`; then E0.3 (golden fixtures) → E1 (implement validators/round-trip/_reserved/conformance against the frozen API).
4. Ahead: E2 publish v2.0.0 schema+CLI · **E3 CanvasForge migration (parity-gated, highest-risk)** · E4 LF-successor + net-new consumer · E5 rollout + `iii/` wiring · E6 validation & cutover. Side-tracks: Δ2 LIP; III/SiteForge upstream notes.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
