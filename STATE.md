---
type: state
created: 2026-06-06
updated: 2026-06-13
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260613_193008_keystone_e3_open
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Operation Cartography (genesis planning) CLOSED 2026-06-13 ✅. Now in EXECUTION — Operation Keystone ACTIVE; PHASES E0+E1+E2 ✅ (reference impl + tooling COMPLETE); 🔄 PHASE E3 OPEN (operator-authorized 2026-06-13) — CanvasForge migration; all 4 missions chartered; E3.1 (canvas/ wrapper) in progress.**
`how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md`

Operation Cartography (P0–P5) ratified the **aDNA Canvas Standard v2.0.0** + contracts + build charter, then **closed at the operator gate**. The operator **activated Operation Keystone** (the build). **E0** (skeleton + KEEP floor + golden fixtures) · **E1** (reference engine: `validate` all levels, `strip`+degradation, round-trip, `diff`/`merge`, `_reserved` validators) · **E2** (conformance harness `validate_suite`, conformance corpus, the v2.0.0 **JSON Schema** + the **`canvas-std` CLI**) — **all complete. `pytest` 46 passed / 8 skipped, `ruff` clean; no stubs remain** in `what/code/canvas_std/`. **The reference implementation is built.** **The operator authorized crossing the E2→E3 gate 2026-06-13** — E3 (parity-gated CanvasForge migration) is open, all four missions chartered, E3.1 in progress. *(Planning history: `campaign_canvas_genesis_planning/`.)*

## ▶ Resume Here — 🔄 Phase E3 open; E3.2 (`canvas_core` shim) is next

**E3 is OPEN** (operator-authorized 2026-06-13). **E3.1** — the additive `canvas/` federation wrapper in
`CanvasForge.aDNA` (`federation_ref` → Canvas.aDNA v2.0.0 + `graft_manifest.yaml`; **no code repoint**) — is
complete this session, and the LP↔Canvas seam is formalized two-sided (Mondrian's countersign). The `canvas_std`
reference impl (E0+E1+E2) is complete and green (`pytest` 46 pass / 8 skip, `ruff` clean, no stubs).

**Next: E3.2 — repoint `canvasforge.canvas_core` → `canvas_std` behind a deprecation shim** (mirror
`lattice-protocol/extensions/canvas/__init__.py`: re-export + `DeprecationWarning` + `DEPRECATED_STUB` marker; both
paths live during the E-D2 grace window, default 12mo). This is the **first consequential code change** of E3 —
producer engines (`layout_*`, `selection_board`, `pdf_export`, `gdoc_export`, deck/comic composition) stay
producer-side; only the reference `canvas_core` logic federates. Then **E3.3** the parity gate (no regression vs
**Wilhelm 8.80 / Issue 01 8.43**; VR1–VR5 ≥ baseline; baseline `3ce4d341` UNCHANGED) → **E3.4** cutover
(operator-gated) + rollback rehearsal + retire the embedded v1.0.0 framing. After E3: E4 (LF-successor + net-new
consumer) · E5 (rollout + `iii/` wiring + registry) · E6 (cutover). Chartered:
[[how/campaigns/campaign_canvas_genesis/missions/mission_e3_2_canvas_core_shim|E3.2]] ·
[[how/campaigns/campaign_canvas_genesis/missions/mission_e3_3_parity_gate|E3.3]] ·
[[how/campaigns/campaign_canvas_genesis/missions/mission_e3_4_cutover|E3.4]].

**Build hygiene:** the suite runs in a `.venv` (`cd what/code/canvas_std && make install && make test`; system
Python 3.14 lacks pytest). `.venv`/`*.egg-info`/`__pycache__` gitignored. Tracking: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active).

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]); III/SiteForge upstream notes; III pin confirm at E5.1.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds the P4 execution charter; informs D2/D4/D7. Opens no phase, builds no code (C3). Operation Cartography itself is **unchanged** (P0-ratified / P1-awaiting-go).

## What's Done (this session — Keystone E3 open + LP seam countersign, 2026-06-13)

- **Countersigned the LP↔Canvas seam memo** (Mondrian → Noether): canonical `who/coordination/coord_2026_06_13_mondrian_countersign_lp_canvas_seam.md` + cross-posts to LP (inbound) / CanvasForge (cc) / aDNA.aDNA (cc). Seam now **two-sided/formalized** — standard stewardship = Canvas, G4 provenance = LP, code home = CanvasForge. Committed in 4 repos (Canvas b83d5b8 · LP 957d7a3 · CanvasForge 690e382 · aDNA.aDNA 2444283); **pushes deferred** (local-commit-accumulate convention; all repos already ahead of origin).
- **Opened Phase E3** (operator-authorized E2→E3 gate crossing): chartered 4 missions (`mission_e3_1..e3_4`); campaign-doc E3 table → status format + phase-open callout.
- **E3.1 (canvas/ wrapper) complete**: `CanvasForge.aDNA/canvas/` — `CLAUDE.md` (`federation_ref` → Canvas.aDNA v2.0.0, `conformance_target: adna_native`, producer engines as `local_extensions`) + `graft_manifest.yaml` (`grafts: []`). **Additive only** — `canvas_core` untouched, baseline `3ce4d341` intact.
- *(Prior this run: Cartography closed; Keystone E0+E1+E2 — reference impl complete, `pytest` 46/8.)*

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip); invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for D2).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3).

## Active Blockers

- None blocking. E3 is open (operator-authorized); E3.1 done, **E3.2 (`canvas_core` shim) begins next session** — the first consequential code change (parity-gated downstream at E3.3). The suite runs in a `.venv` (`make install`).
- **Pushes pending operator decision** — 4 repos hold local coord/charter/wrapper commits ahead of origin (workspace runs local-commit-accumulate; Noether's own P4.M2 cross-posts were "no push"). Push when ready.

## Next Steps

1. ✅ **Operation Cartography CLOSED** 2026-06-13; **Keystone E0+E1+E2 COMPLETE** — reference impl + tooling built (`pytest` 46/8, `ruff` clean; no stubs).
2. ✅ **LP↔Canvas seam countersigned** 2026-06-13 — two-sided/formalized (4-repo cross-post).
3. ✅ **Phase E3 OPENED** (operator-authorized) + **E3.1 done** — `canvas/` federation wrapper in CanvasForge (additive; baseline `3ce4d341` intact).
4. **→ E3.2 (next session)** — `canvas_core` → `canvas_std` deprecation shim (mirror lattice-protocol precedent; decide E-D2 grace window). Then E3.3 parity gate (**Wilhelm 8.80 / Issue 01 8.43**) → E3.4 cutover (operator-gated). After E3: E4 · E5 (`iii/` wiring + registry) · E6.
5. **Operator decision pending:** push the 4 repos' local commits (countersign + charter + wrapper), or keep accumulating per convention.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
