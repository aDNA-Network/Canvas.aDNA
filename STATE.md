---
type: state
created: 2026-06-06
updated: 2026-06-13
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260613_184540_keystone_e2
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Operation Cartography (genesis planning) CLOSED 2026-06-13 ✅. Now in EXECUTION — Operation Keystone ACTIVE; PHASES E0+E1+E2 ✅ — reference impl + tooling COMPLETE; ⛔ HELD at the E2→E3 boundary (E3 = operator-gated CanvasForge migration).**
`how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md`

Operation Cartography (P0–P5) ratified the **aDNA Canvas Standard v2.0.0** + contracts + build charter, then **closed at the operator gate**. The operator **activated Operation Keystone** (the build). **E0** (skeleton + KEEP floor + golden fixtures) · **E1** (reference engine: `validate` all levels, `strip`+degradation, round-trip, `diff`/`merge`, `_reserved` validators) · **E2** (conformance harness `validate_suite`, conformance corpus, the v2.0.0 **JSON Schema** + the **`canvas-std` CLI**) — **all complete. `pytest` 46 passed / 8 skipped, `ruff` clean; no stubs remain** in `what/code/canvas_std/`. **The reference implementation is built.** Next is **E3** — the parity-gated CanvasForge migration, a **human gate**. *(Planning history: `campaign_canvas_genesis_planning/`.)*

## ▶ Resume Here — ⛔ Operator gate before E3 (CanvasForge migration)

**The reference implementation is complete** — E0+E1+E2 done; `what/code/canvas_std/` ships `validate` /
`validate_suite` / `strip` / round-trip / `diff`/`merge` / the `_reserved` validators / the v2.0.0 JSON Schema /
the `canvas-std` CLI, with `pytest` 46 pass / 8 skip and `ruff` clean (no stubs). **HELD at the E2→E3 boundary.**

**Next phase: E3 — the parity-gated CanvasForge migration (HUMAN GATE — needs operator go).** E3.1 introduce the
`canvas/` federation wrapper in `CanvasForge.aDNA`; E3.2 repoint `canvas_core` → `canvas_std` behind a deprecation
shim (mirror `lattice-protocol/extensions/canvas/__init__.py`); E3.3 the **parity/regression gate** — no
CanvasForge output regresses vs the locked baselines **Wilhelm 8.80 / Issue 01 8.43**; E3.4 cutover criteria +
rollback + retire the embedded v1.0.0 framing. **This phase touches another vault (CanvasForge) and is
reversible-but-consequential — do NOT start E3 without the operator.** After E3: E4 (LF-successor + net-new
consumer) · E5 (rollout + `iii/` wiring + registry registration) · E6 (cutover).

**Build hygiene:** the suite runs in a `.venv` (`cd what/code/canvas_std && make install && make test`; system
Python 3.14 lacks pytest). `.venv`/`*.egg-info`/`__pycache__` gitignored. Tracking: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active).

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]); III/SiteForge upstream notes; III pin confirm at E5.1.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds the P4 execution charter; informs D2/D4/D7. Opens no phase, builds no code (C3). Operation Cartography itself is **unchanged** (P0-ratified / P1-awaiting-go).

## What's Done (this session — Keystone Phase E2, 2026-06-13)

- **Finished Phase E2 (conformance + publish)** in three committed missions: E2.1 conformance harness (`validate_suite` → `ConformanceReport`) · E2.2 conformance corpus (6 fixtures incl. 2 boundary cases + `test_conformance.py`) · E2.3 the v2.0.0 **JSON Schema** (`data/adna_canvas_v2.schema.json` + `json_schema()`) + the **`canvas-std` CLI** (`validate`/`schema`, auto-level-detect, exit 0/1).
- **The reference implementation is complete — no stubs remain.** `pytest` 46 passed / 8 skipped, `ruff` clean. CLI verified end to end.
- + `mission_e2_1..e2_3`; CHANGELOG. **⛔ HELD at the E2→E3 boundary.**
- *(Earlier this run: Cartography closed + Keystone activated; E0 bootstrap + E1 reference engine.)*

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip); invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for D2).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3).

## Active Blockers

- None blocking. **⛔ HELD at the E2→E3 boundary** — E3 (CanvasForge migration) is a human gate; do not start without the operator. The suite runs in a `.venv` (`make install`).

## Next Steps

1. ✅ **Operation Cartography CLOSED** 2026-06-13 — Standard v2.0.0 ratified across P0–P5; context graduated.
2. ✅ **Keystone E0 + E1 + E2 COMPLETE** — the reference impl + tooling is built (`pytest` 46 pass / 8 skip, `ruff` clean; `canvas-std` CLI + v2.0.0 JSON Schema live; no stubs).
3. **⛔ Operator gate before E3** — the parity-gated CanvasForge migration: E3.1 `canvas/` wrapper → E3.2 `canvas_core`→`canvas_std` deprecation shim → E3.3 parity gate vs **Wilhelm 8.80 / Issue 01 8.43** → E3.4 cutover/rollback. Touches `CanvasForge.aDNA`; needs operator go.
4. After E3: E4 (LF-successor + net-new consumer) · E5 (rollout + `iii/` wiring + registry registration) · E6 (cutover). Side-tracks: Δ2 LIP; III/SiteForge upstream notes.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
