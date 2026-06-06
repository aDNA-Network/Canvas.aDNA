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

**Genesis-planning — Operation Cartography, Phase P0 (Charter & Persona Lock).**
`how/campaigns/campaign_canvas_genesis_planning/campaign_canvas_genesis_planning.md`

Canvas.aDNA was forked 2026-06-06 (from `.adna` via `skill_project_fork`) and seeded to a P0 skeleton: governance tuned to the thesis, the Operation Cartography charter authored (P0–P5), and `adr_000_canvas_identity.md` + `decision_register_genesis.md` (D1–D7) drafted. This is a **planning** campaign — no runtime, no code migration, no breaking changes to CanvasForge/LiteratureForge.

## ▶ Resume Here (the P0 gate — `#needs-human`)

The session is **HELD at the P0 gate.** Operator must lock three decisions before P1 opens:

1. **Persona** — provisional **Mondrian** (operator's prior pick); candidates **Seshat** (measurement/records — Thoth's counterpart) and **Mercator** (cartographer — matches "Operation Cartography"). `adr_000` §2.
2. **Category** — provisional **Framework.aDNA**, but **Δ1**: `spec_framework_ecosystem.md` says Frameworks "produce no primary artifact and deploy no runtime"; shipping runnable validators/round-trip tooling pushes toward Platform. Decide where the reference implementation lives. `adr_000` §1 + D1.
3. **Scope boundary** — Standard owns spec/component-model/round-trip/conformance-spec/federation/governance; producers own pipelines/render/image-gen. `adr_000` §3.

Plus note **Δ2** (D7): canvas is today a *view of the lattice primitive* (Decision 9), not a 4th primitive — elevating it needs a LIP.

**On operator lock → open P1 (Source inventory & fork baseline).**

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

- `#needs-human` — P0 gate lock (persona / category / scope). No P1 work until cleared.

## Next Steps

1. Operator locks P0 (persona, category incl. Δ1, scope boundary).
2. Open **P1** — source inventory + fork baseline (catalog v1.0.0 + `CanvasBuilder` constants + `advanced_canvas/` corpus; label KEEP/EXTEND/SUPERSEDE/DEFER-TO-PRODUCER; pin upstream Advanced Canvas version).
3. Forward: P2 Standard spec (heaviest gate) → P3 conformance + federation → P4 execution charter → P5 harmonization plan.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
