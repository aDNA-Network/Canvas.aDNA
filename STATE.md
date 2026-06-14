---
type: state
created: 2026-06-06
updated: 2026-06-13
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260613_215108_keystone_e3_3_parity
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Operation Cartography (genesis planning) CLOSED 2026-06-13 ✅. Now in EXECUTION — Operation Keystone ACTIVE; PHASES E0+E1+E2 ✅ (reference impl + tooling COMPLETE); 🔄 PHASE E3 OPEN (operator-authorized 2026-06-13) — CanvasForge migration; E3.1 (canvas/ wrapper) ✅ + E3.2 (canvas_core→canvas_std deprecation shim) ✅ + E3.3 (parity gate) ✅ **GREEN**; ⛔ E3.4 (cutover — operator gate) NEXT.**
`how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md`

Operation Cartography (P0–P5) ratified the **aDNA Canvas Standard v2.0.0** + contracts + build charter, then **closed at the operator gate**. The operator **activated Operation Keystone** (the build). **E0** (skeleton + KEEP floor + golden fixtures) · **E1** (reference engine: `validate` all levels, `strip`+degradation, round-trip, `diff`/`merge`, `_reserved` validators) · **E2** (conformance harness `validate_suite`, conformance corpus, the v2.0.0 **JSON Schema** + the **`canvas-std` CLI**) — **all complete. `pytest` 46 passed / 8 skipped, `ruff` clean; no stubs remain** in `what/code/canvas_std/`. **The reference implementation is built.** **The operator authorized crossing the E2→E3 gate 2026-06-13** — E3 (parity-gated CanvasForge migration) is open; **E3.1 (canvas/ wrapper) + E3.2 (constants-only canvas_core→canvas_std deprecation shim) + E3.3 (parity gate — GREEN) are complete**; **E3.4 (cutover) is next and is an operator gate**. *(Planning history: `campaign_canvas_genesis_planning/`.)*

## ▶ Resume Here — ⛔ Phase E3 open; E3.4 (cutover) is next — OPERATOR GATE

**E3 is OPEN** (operator-authorized 2026-06-13). **E3.1** (canvas/ wrapper) + **E3.2** (constants-only
`canvas_core`→`canvas_std` deprecation shim) + **E3.3** (parity gate — **GREEN**) are **complete**. The E3.2 shim
is proven **output-neutral** by a deterministic structural proof (operator-chosen Approach A): rebuilding the
Wilhelm parity deck through the shim **shim-ON vs shim-OFF** yields an **identical** normalized-canvas SHA
(`aa675665…`); 0 federated-floor rejects on the rebuilt deck (56 nodes) + committed comic (11 nodes); baseline
`3ce4d341` UNCHANGED; CanvasForge suite 900/3. Evidence: `missions/artifacts/e3_3_parity_{report,verdict}.md` +
the reusable `e3_3_parity_check.py`. **E3.2 is pushed** (Canvas.aDNA `38265f1`, CanvasForge `1a51801`).

**Next: E3.4 — cutover (⛔ OPERATOR GATE; do NOT start without the operator).** Per the charter: define cutover
criteria + **rollback rehearsal** (revert `1a51801` → the shim keeps the old path working) + retire the embedded
v1.0.0 framing (supersede). E3.3 GREEN is the cutover precondition. The round-trip-**function** repoint descoped
from E3.2 may also run now that constants parity is proven (its own parity pass via `e3_3_parity_check.py`). After
E3: E4 (LF-successor + net-new consumer) · E5 (rollout + `iii/` wiring + registry) · E6 (cutover + shim
retirement). Test env: gitignored `.venv` at `CanvasForge.aDNA/what/code/` (`adna-canvas-std` editable). Chartered:
[[how/campaigns/campaign_canvas_genesis/missions/mission_e3_4_cutover|E3.4]].

**Build hygiene:** the suite runs in a `.venv` (`cd what/code/canvas_std && make install && make test`; system
Python 3.14 lacks pytest). `.venv`/`*.egg-info`/`__pycache__` gitignored. Tracking: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active).

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]); III/SiteForge upstream notes; III pin confirm at E5.1.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds the P4 execution charter; informs D2/D4/D7. Opens no phase, builds no code (C3). Operation Cartography itself is **unchanged** (P0-ratified / P1-awaiting-go).

## What's Done (this session — Keystone E3.3 parity gate GREEN + E3.2 push, 2026-06-13)

- **E3.3 parity gate ✅ GREEN** (operator method = deterministic Approach A; no Gemini re-score). Proof chain: (1) static — `core.py` diff is constants→imports only, no method touched; (2) object-identity — 12 floor constants `is`-identical to `canvas_std.schema`; (3) determinism — two shim-ON deck rebuilds give identical normalized SHA; (4) **A/B — shim-ON vs shim-OFF rebuild of the Wilhelm deck → identical `deck_norm_sha256` `aa675665…`** ⇒ shim output-neutral; (5) federated floor accepts rebuilt deck (56 nodes) + committed comic (11 nodes), **0 rejects**; (6) baseline `3ce4d341…` UNCHANGED; (7) suite 900/3. Artifacts: `missions/artifacts/e3_3_parity_{report,verdict}.md` + reusable `e3_3_parity_check.py`. VR1–VR5 ≥ baseline holds **by construction** (output structurally identical → scores unchanged).
- **Pushed the E3.2 batch** (operator-authorized): Canvas.aDNA `be2194e..38265f1` + CanvasForge.aDNA `7bb833f..1a51801` → origin/master. Home.aDNA stays local (Rule 4; §C ledger `c72e9cc` local-only).
- *(Prior this run: **E3.2** — constants-only `canvas_core`→`canvas_std` deprecation shim landed (`CanvasBuilder` floor binds to `canvas_std.schema`; `DeprecationWarning` + `DEPRECATED_STUB`; producers untouched); API-parity audit (byte-identity PASS); E-D2=12mo + Home.aDNA §C registration; suite green at parity. Test env = gitignored `.venv` at `what/code/` + editable `adna-canvas-std`.)*
- *(Earlier: Cartography closed; Keystone E0+E1+E2 reference impl (`pytest` 46/8); E3 opened + E3.1 `canvas/` wrapper + LP↔Canvas seam countersign.)*

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip); invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for D2).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3).

## Active Blockers

- **None blocking.** E3.1 + E3.2 + E3.3 (**GREEN**) done. **E3.4 (cutover) is the next mission and is an OPERATOR GATE** — do not start without the operator (retire the embedded v1.0.0 framing + rollback rehearsal). CanvasForge tests run in the gitignored `.venv` at `what/code/` (`adna-canvas-std` editable-installed).
- **Pushes:** E3.2 batch **pushed** 2026-06-13 (Canvas.aDNA `38265f1`, CanvasForge `1a51801` → origin/master); Home.aDNA §C ledger `c72e9cc` stays **local** (Rule 4). **E3.3 close commit** (Canvas.aDNA: verdict/report/`e3_3_parity_check.py` + mission + STATE + campaign + session) pending this session's close — push per operator batch.

## Next Steps

1. ✅ **Operation Cartography CLOSED** + **Keystone E0+E1+E2 COMPLETE** (reference impl + tooling; `pytest` 46/8, `ruff` clean).
2. ✅ **Phase E3 OPENED** (operator-authorized) + **E3.1 (canvas/ wrapper)** + **LP↔Canvas seam countersign** — all pushed 2026-06-13.
3. ✅ **E3.2 COMPLETE + PUSHED** 2026-06-13 — constants-only `canvas_core`→`canvas_std` deprecation shim; suite green at parity; E-D2 = 12mo + Home.aDNA §C registration.
4. ✅ **E3.3 COMPLETE — GREEN** 2026-06-13 — deterministic structural proof (Approach A): shim **output-neutral** (A/B identical normalized-canvas SHA `aa675665…`; 0 federated-floor rejects; baseline `3ce4d341` untouched; suite 900/3). Artifacts `e3_3_parity_{report,verdict}.md` + `e3_3_parity_check.py`.
5. **→ E3.4 (next session) — CUTOVER, ⛔ OPERATOR GATE.** Cutover criteria + **rollback rehearsal** (revert `1a51801` → shim keeps old path) + retire the embedded v1.0.0 framing. Alongside (optional): the descoped round-trip-**function** repoint, gated by its own parity pass via `e3_3_parity_check.py`. After E3: E4 · E5 (`iii/` wiring + registry) · E6.
6. **Pushes:** E3.2 pushed; E3.3 close commit pending → push per operator batch; Home.aDNA local.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
