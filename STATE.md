---
type: state
created: 2026-06-06
updated: 2026-06-13
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260613_205753_keystone_e3_2_shim
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Operation Cartography (genesis planning) CLOSED 2026-06-13 ✅. Now in EXECUTION — Operation Keystone ACTIVE; PHASES E0+E1+E2 ✅ (reference impl + tooling COMPLETE); 🔄 PHASE E3 OPEN (operator-authorized 2026-06-13) — CanvasForge migration; E3.1 (canvas/ wrapper) ✅ + E3.2 (canvas_core→canvas_std deprecation shim) ✅; ⛔ E3.3 (parity gate — operator gate) NEXT.**
`how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md`

Operation Cartography (P0–P5) ratified the **aDNA Canvas Standard v2.0.0** + contracts + build charter, then **closed at the operator gate**. The operator **activated Operation Keystone** (the build). **E0** (skeleton + KEEP floor + golden fixtures) · **E1** (reference engine: `validate` all levels, `strip`+degradation, round-trip, `diff`/`merge`, `_reserved` validators) · **E2** (conformance harness `validate_suite`, conformance corpus, the v2.0.0 **JSON Schema** + the **`canvas-std` CLI**) — **all complete. `pytest` 46 passed / 8 skipped, `ruff` clean; no stubs remain** in `what/code/canvas_std/`. **The reference implementation is built.** **The operator authorized crossing the E2→E3 gate 2026-06-13** — E3 (parity-gated CanvasForge migration) is open; **E3.1 (canvas/ wrapper) + E3.2 (constants-only canvas_core→canvas_std deprecation shim) are complete**; **E3.3 (the parity gate) is next and is an operator gate**. *(Planning history: `campaign_canvas_genesis_planning/`.)*

## ▶ Resume Here — ⛔ Phase E3 open; E3.3 (parity gate) is next — OPERATOR GATE

**E3 is OPEN** (operator-authorized 2026-06-13). **E3.1** (additive `canvas/` federation wrapper) and **E3.2**
(the constants-only `canvas_core`→`canvas_std` deprecation shim) are **complete**. CanvasForge's Standard floor
(the 10 `VALID_*` enums + `TYPE_MAPPING` + `EDGE_TYPE_MAPPING`, as `CanvasBuilder` class attributes) now resolves
from `canvas_std.schema` (SSOT, object-identical) behind a `DeprecationWarning` (stacklevel=2) + `# DEPRECATED_STUB
Canvas.aDNA` marker — mirroring the `lattice-protocol/extensions/canvas/__init__.py` precedent. CanvasForge suite
**green at parity** (canonical 900/3 skip; full tree 957/5 skip; baseline `3ce4d341` intact); `canvas_std` own
suite unregressed (46/8). **E-D2 grace window = 12mo** (expiry 2027-06-13; registered Home.aDNA §C). **Test env**:
gitignored `.venv` at `CanvasForge.aDNA/what/code/` with `adna-canvas-std` editable-installed (+ `pytest
pytest-timeout pyyaml pillow google-api-python-client`).

**Next: E3.3 — the parity/regression gate (⛔ OPERATOR GATE; do NOT start without the operator).** Regenerate
CanvasForge's locked reference outputs *through* `canvas_std` (via this shim) and prove no regression vs **Wilhelm
8.80 / Issue 01 8.43** (VR1–VR5 ≥ baseline; baseline `3ce4d341` stays UNCHANGED until a green gate). If E3.3 is
green, the round-trip **function** repoint (descoped from E3.2 per the constants-only decision) can follow. Then
**E3.4** cutover (operator-gated) + rollback rehearsal + retire the embedded v1.0.0 framing. After E3: E4
(LF-successor + net-new consumer) · E5 (rollout + `iii/` wiring + registry) · E6 (cutover + shim retirement).
Chartered: [[how/campaigns/campaign_canvas_genesis/missions/mission_e3_3_parity_gate|E3.3]] ·
[[how/campaigns/campaign_canvas_genesis/missions/mission_e3_4_cutover|E3.4]].

**Build hygiene:** the suite runs in a `.venv` (`cd what/code/canvas_std && make install && make test`; system
Python 3.14 lacks pytest). `.venv`/`*.egg-info`/`__pycache__` gitignored. Tracking: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active).

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]); III/SiteForge upstream notes; III pin confirm at E5.1.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds the P4 execution charter; informs D2/D4/D7. Opens no phase, builds no code (C3). Operation Cartography itself is **unchanged** (P0-ratified / P1-awaiting-go).

## What's Done (this session — Keystone E3.2 constants-only shim, 2026-06-13)

- **E3.2 complete — CanvasForge floor repointed to `canvas_std` behind a deprecation shim** (operator scope: **constants-only** + **editable install**). `CanvasForge.aDNA/what/code/canvas_core/core.py`: the 10 `VALID_*` enums + `TYPE_MAPPING` + `EDGE_TYPE_MAPPING` (`CanvasBuilder` class attributes) now bind to `canvas_std.schema` objects (verified `is`-identical) behind `warnings.warn(..., DeprecationWarning, stacklevel=2)` + `# DEPRECATED_STUB Canvas.aDNA`. Producer engines + `CanvasBuilder` logic untouched; baseline `3ce4d341` intact. Mirrors the `lattice-protocol/extensions/canvas/__init__.py` extraction-shim precedent.
- **API-parity audit** (`how/campaigns/campaign_canvas_genesis/missions/artifacts/e3_2_api_parity_audit.md`): all 12 floor constants byte-identical (verbatim E0.2 port); no in-place mutation of the mappings → safe to share `canvas_std` objects; no module-level floor imports in CanvasForge. **PASS / no blockers.**
- **Suite green at parity** (differential pre→post-shim): canonical `pytest canvas_core/tests/ canvas_comic/tests/ tests/test_federation_validation.py` → **900 passed / 3 skip / 0 fail**; complete tree (incl. `canvas_presentation`) **957 / 5 / 0**; only delta vs baseline = +1 `DeprecationWarning`. `canvas_std` own suite **46/8** unregressed. Test env = gitignored `.venv` at `what/code/` + editable `adna-canvas-std` (+ pytest/pytest-timeout/pyyaml/pillow/google-api-python-client).
- **E-D2 = 12 months** (expiry 2027-06-13) + **shim registered** in `Home.aDNA/.../disposition_ledger_v2.md` §C (count 17→18; class `deprecation (in-code re-export)`; owner Mondrian + Hermes; retire @ E6).
- *(Prior runs: Cartography closed; Keystone E0+E1+E2 reference impl complete (`pytest` 46/8); E3 opened + E3.1 `canvas/` wrapper + LP↔Canvas seam countersign — all pushed 2026-06-13.)*

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip); invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for D2).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3).

## Active Blockers

- **None blocking.** E3 is open (operator-authorized); E3.1 + E3.2 done. **E3.3 (parity gate) is the next mission and is an OPERATOR GATE** — do not start without the operator (it regenerates locked outputs and proves no regression vs Wilhelm 8.80 / Issue 01 8.43). CanvasForge tests run in the gitignored `.venv` at `what/code/` (`adna-canvas-std` editable-installed).
- **Pushes — PENDING operator-gated batch (2026-06-13).** This session's commits are **local**: Canvas.aDNA (mission/audit/STATE/campaign + session), CanvasForge.aDNA (`core.py` shim), Home.aDNA (§C ledger). Push as a batch on operator go (workspace push-scope discipline; check `@{u}..HEAD` authorship before pushing shared vaults).

## Next Steps

1. ✅ **Operation Cartography CLOSED** + **Keystone E0+E1+E2 COMPLETE** (reference impl + tooling; `pytest` 46/8, `ruff` clean).
2. ✅ **Phase E3 OPENED** (operator-authorized) + **E3.1 (canvas/ wrapper)** + **LP↔Canvas seam countersign** — all pushed 2026-06-13.
3. ✅ **E3.2 COMPLETE** 2026-06-13 — constants-only `canvas_core`→`canvas_std` deprecation shim; CanvasForge suite green at parity (957/5; baseline `3ce4d341` intact); E-D2 = 12mo + Home.aDNA §C registration.
4. **→ E3.3 (next session) — PARITY GATE, ⛔ OPERATOR GATE.** Regenerate CanvasForge locked outputs *through* `canvas_std` (via the shim); prove no regression vs **Wilhelm 8.80 / Issue 01 8.43** (VR1–VR5 ≥ baseline; baseline unchanged until green). Do **not** start without the operator. Green → optional round-trip-**function** repoint (descoped from E3.2), then **E3.4** cutover (operator-gated). After E3: E4 · E5 (`iii/` wiring + registry) · E6 (cutover + shim retirement).
5. **Pushes — PENDING operator-gated batch.** E3.2 commits (Canvas.aDNA · CanvasForge.aDNA · Home.aDNA) are local; push as a batch on operator go.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
