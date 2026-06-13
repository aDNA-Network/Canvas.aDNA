---
type: state
created: 2026-06-06
updated: 2026-06-12
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260612_211907_p1_source_inventory
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Genesis-planning — Operation Cartography. P1 CLEARED 2026-06-12; P2 (Standard Specification) CHARTERED — awaiting operator go to execute.**
`how/campaigns/campaign_canvas_genesis_planning/campaign_canvas_genesis_planning.md`

P0 ratified 2026-06-06 (persona **Mondrian**; category **Platform/Option P**; scope confirmed — `adr_000`). **P1 executed + gate-cleared 2026-06-12** — classification ratified, **PIN-A locked** (Advanced Canvas v5.6.6 + JSON Canvas 1.0), scaffold archived (`adr_001+` freed). **P2 chartered** ([[how/campaigns/campaign_canvas_genesis_planning/missions/mission_p2_standard_spec|mission_p2_standard_spec]]): 3 foundational ADRs (D2/D3/D6) + 5 specs, **not executing until operator go** (SO-1). Planning campaign — specs + ADRs only, no runtime (C3).

## ▶ Resume Here — operator go to EXECUTE P2

P1 is **closed**. P2 is **chartered and held** — read [[how/campaigns/campaign_canvas_genesis_planning/missions/mission_p2_standard_spec|the P2 charter]]: 8 objectives in dependency order — O1 D2/CanvasForge ADR → O2 D3/LiteratureForge ADR → O3 D6/governance ADR → **◆ checkpoint α** → O4 normative `spec_adna_canvas_standard.md` → O5 component model (D4) → O6 panel/link (D5) → O7 round-trip v2 → O8 context-object (D7/Δ2 via LIP). Exit gate: operator signs off on the v2.0.0 spec + D2/D3.

**On operator go → execute P2**, starting with the three foundational ADRs (recommended internal **checkpoint α** after O1–O3 before the specs build on them). Proposed numbering D2→`adr_001`, D3→`adr_002`, D6→`adr_003` (namespace freed at P1). Do not author P2 ADRs/specs without the go (SO-1).

**Locked inputs (P1):** PIN-A baseline; KEEP floor (schema A1 + round-trip A2 + 10 `VALID_*` enums B1); the `_reserved` extension map (key schemas minted at P2); the C4 degradation contract; alias `build()`/`read_back()`→`to_canvas`/`from_canvas` at extraction. **Δ2** (D7/O8) routes through a LIP — do **not** touch the aDNA core primitive set (out of scope).

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds the P4 execution charter; informs D2/D4/D7. Opens no phase, builds no code (C3). Operation Cartography itself is **unchanged** (P0-ratified / P1-awaiting-go).

## What's Done (this session — P1, 2026-06-12)

- Opened P1; ran 4 parallel read-and-classify subagents over the source corpus (advanced_canvas standard/schema/roundtrip/graft · `core.py` constants+exports · 15 design docs · 3 LF specs).
- Authored **`p1_source_inventory.md`** — 28 source rows labeled KEEP/EXTEND/SUPERSEDE/DEFER-TO-PRODUCER (+ 4 archived scaffold), with the verbatim constants/invariants grounding each label.
- Authored **`p1_fork_baseline.md`** — 7 inherited invariants + 10 `VALID_*` enums + `TYPE_MAPPING`/`EDGE_TYPE_MAPPING` (verbatim); the additive `_reserved` extension map; the C4 degradation contract; **PIN-A** upstream recommendation (v5.6.6 confirmed at source).
- Reconciled the inherited scaffold: `git mv` `adr_001/002/003` + `campaign_adna_workspace_upgrade/` → `_inherited_scaffold/` holders (+ banners; history preserved); freed `adr_001+`; updated `decision_register_genesis.md`.
- Authored `mission_p1_source_inventory.md` (tracker) + `canvas_genesis_planning_p1_aar.md` (5/5 validated); updated the campaign doc (P1 row + delivered block + P1 phase AAR + Notes) and this STATE.

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip); invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for D2).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3).

## Active Blockers

- None blocking. **Next gate:** operator go to **execute** the chartered P2 (one phase per gate, SO-1).

## Next Steps

1. ✅ P0 locked 2026-06-06 (Mondrian · Platform/Option P · scope confirmed).
2. ✅ P1 executed + gate-cleared 2026-06-12 (classification ratified; PIN-A locked; scaffold archived; `adr_001+` freed).
3. ✅ P2 chartered 2026-06-12 ([[how/campaigns/campaign_canvas_genesis_planning/missions/mission_p2_standard_spec|mission_p2_standard_spec]]) — **awaiting operator go to execute**.
4. **On go → execute P2:** 3 foundational ADRs (D2/D3/D6) → ◆ checkpoint α → 5 specs; operator signs off on the v2.0.0 spec + D2/D3 at the P2 exit gate.
5. Forward: P3 conformance + federation → P4 execution charter → P5 harmonization plan.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
