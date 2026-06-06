---
type: state
created: 2026-06-06
updated: 2026-06-06
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260606_p0_genesis_skeleton
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Genesis-planning — Operation Cartography. P0 RATIFIED 2026-06-06; P1 ready (awaiting operator go).**
`how/campaigns/campaign_canvas_genesis_planning/campaign_canvas_genesis_planning.md`

Canvas.aDNA was forked 2026-06-06 (from `.adna` via `skill_project_fork`) and seeded to a P0 skeleton. **P0 gate cleared by operator 2026-06-06:** persona **Mondrian**; category **Platform.aDNA (standard-bearer), Option P** — Canvas.aDNA ships the Standard's runnable reference tooling (validators · round-trip converters · conformance harness; code-as-WHAT-object home `what/code/canvas_std/`, **declared not built**); scope boundary **confirmed**. This is a **planning** campaign — no runtime, no code migration, no breaking changes to CanvasForge/LiteratureForge.

## ▶ Resume Here — open P1 on operator go

P0 is **ratified**. The next gate is the operator's **go to open P1 (Source inventory & fork baseline)** —
a 2–3 session mission that catalogs Canvas Standard v1.0.0, the `CanvasBuilder` constants, the
`advanced_canvas/` corpus (~22 files), the Round-Trip Protocol, the graft_manifest, and the LF
visual/format/genre specs, labels each **KEEP / EXTEND / SUPERSEDE / DEFER-TO-PRODUCER**, and **pins the
upstream Advanced Canvas baseline version** (brief cites v5.6.6 — confirm). Phase gates are human gates;
do not open P1 without operator approval.

**Carry into P1/P2 (from the P0 lock):** Platform vault+code split — declare the `what/code/canvas_std/`
reference-impl home (don't build it, C3); Option P **tilts D2 toward extracting** the standard out of
CanvasForge (CanvasForge → producer). **Δ2** (D7) still open: canvas is today a *view of the lattice
primitive* (Decision 9), not a 4th primitive — elevating it needs a LIP (P2 + out-of-scope core change).

## What's Done (this session)

- Forked `Canvas.aDNA/` (full triad, fresh git) via `skill_project_fork` (C1).
- Tuned `CLAUDE.md` (Mondrian provisional identity + thesis + scope), `MANIFEST.md`, this `STATE.md`.
- Authored `how/campaigns/campaign_canvas_genesis_planning/campaign_canvas_genesis_planning.md` (Operation Cartography P0–P5, human-gated).
- Authored `what/decisions/adr_000_canvas_identity.md` (status: proposed) + `what/decisions/decision_register_genesis.md` (D1–D7 stubs).
- Recorded naming/persona exceptions in `who/coordination/coord_2026_06_06_naming_persona_exceptions.md`.
- Added a one-line routing row for Canvas.aDNA to the workspace router (`~/lattice/CLAUDE.md`).

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip); invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for D2).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3).

## Active Blockers

- None blocking. **Next gate:** operator go to open **P1** (one phase per gate, SO-1).

## Next Steps

1. ✅ Operator locked P0 (persona Mondrian · category Platform/Option P · scope confirmed) — 2026-06-06.
2. **On operator go → open P1** — source inventory + fork baseline (catalog v1.0.0 + `CanvasBuilder` constants + `advanced_canvas/` corpus; label KEEP/EXTEND/SUPERSEDE/DEFER-TO-PRODUCER; pin upstream Advanced Canvas version).
3. Forward: P2 Standard spec (heaviest gate) → P3 conformance + federation → P4 execution charter → P5 harmonization plan.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
