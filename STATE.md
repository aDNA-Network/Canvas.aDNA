---
type: state
created: 2026-06-06
updated: 2026-06-12
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260612_214547_p2_standard_spec
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Genesis-planning — Operation Cartography. P2 (Standard Specification) DRAFTS COMPLETE 2026-06-12 — HELD at the P2 exit gate (heaviest; awaiting operator sign-off).**
`how/campaigns/campaign_canvas_genesis_planning/campaign_canvas_genesis_planning.md`

P0 ratified 2026-06-06 (Mondrian; Platform/Option P). P1 cleared 2026-06-12 (classification ratified; PIN-A locked; scaffold archived). **P2 executed 2026-06-12 (full push)** — 3 foundational ADRs (D2/D3/D6) + 5 normative specs + the Δ2 LIP draft, all `status: proposed`. **Operator signs off on the v2.0.0 spec + the D2/D3 decisions to clear the gate; nothing flips to `ratified` and P3 does not open until then** (SO-1). Planning campaign — specs + ADRs only, no runtime (C3).

## ▶ Resume Here — P2 exit gate (operator sign-off)

P2 drafts are **authored and HELD at the gate** (all `status: proposed`). The operator signs off on **two things**:
1. **D2 + D3 (review FIRST — they gate everything downstream):** D2 [[what/decisions/adr_001_canvasforge_relationship|adr_001]] recommends **Option A (extract** → CanvasForge pure producer); D3 [[what/decisions/adr_002_literatureforge_seam|adr_002]] recommends **A-schema + B-federated-pipeline** (the operator's prior **absorb/C** is documented as the alternative fork).
2. **The v2.0.0 spec set:** [[what/specs/spec_adna_canvas_standard|spec_adna_canvas_standard]] (normative core) + [[what/specs/spec_component_model|component model D4]] + [[what/specs/spec_panel_link_semantics|panel/link D5]] + [[what/specs/spec_roundtrip_protocol_v2|round-trip v2]] + [[what/specs/spec_context_object|context-object D7]]; plus D6 [[what/decisions/adr_003_standard_governance|adr_003]] + Δ2 [[what/decisions/lip_draft_canvas_as_primitive|LIP draft]] (keep-as-view).

**On sign-off →** flip ADRs/specs `proposed`→`ratified`, then open **P3** (conformance suite + federation contract + `iii/` wrapper). Do not flip/advance without the gate (SO-1).

**Locked inputs (P1, unchanged):** PIN-A baseline; KEEP floor (schema + round-trip + 10 `VALID_*` enums); the `_reserved` extension carrier; the C4 degradation contract. Reference impl (`what/code/canvas_std/`) declared-not-built (C3; execution campaign P4). **Δ2** stays a LIP — the aDNA core primitive set is untouched.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds the P4 execution charter; informs D2/D4/D7. Opens no phase, builds no code (C3). Operation Cartography itself is **unchanged** (P0-ratified / P1-awaiting-go).

## What's Done (this session — P2 full push, 2026-06-12)

- Executed P2 (full push, operator's choice): authored 3 foundational ADRs + 5 normative specs + 1 LIP draft, all `status: proposed`, cross-consistent.
- **ADRs** (`what/decisions/`): `adr_001_canvasforge_relationship` (D2 → A/extract), `adr_002_literatureforge_seam` (D3 → A-schema + B-pipeline; absorb=C documented), `adr_003_standard_governance` (D6 → v2.0.0 + LIP + 3 conformance levels + version_policy minor).
- **Specs** (`what/specs/` + `AGENTS.md`): `spec_adna_canvas_standard` (normative core; supersedes embedded v1.0.0; C4 degradation §11), `spec_component_model` (D4; 12-class taxonomy, `lattice` profile KEEP, LF visual-contract absorbed), `spec_panel_link_semantics` (D5; reading-path edges + regions, non-breaking), `spec_roundtrip_protocol_v2` (generalized source↔view), `spec_context_object` (D7; keep-as-view) + `lip_draft_canvas_as_primitive` (Δ2 → lattice-labs LIP process).
- Tracking: mission_p2 completion summary + AAR; `canvas_genesis_planning_p2_aar.md` (8/8 validated, GO pending gate); campaign (P2 row + Decision Points D2/D3/D6/D7 + P2 phase AAR); decision register; this STATE.

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip); invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for D2).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3).

## Active Blockers

- None blocking. **Next gate:** operator sign-off on the v2.0.0 spec + D2/D3 at the **P2 exit gate** (one phase per gate, SO-1).

## Next Steps

1. ✅ P0 locked 2026-06-06 (Mondrian · Platform/Option P · scope confirmed).
2. ✅ P1 executed + gate-cleared 2026-06-12 (classification ratified; PIN-A locked; scaffold archived; `adr_001+` freed).
3. ✅ P2 executed 2026-06-12 (full push) — 3 ADRs + 5 specs + Δ2 LIP draft, all `proposed`; **HELD at the P2 exit gate**.
4. **P2 gate:** operator reviews D2 + D3 first, then the v2.0.0 spec set → on sign-off, flip `proposed`→`ratified`, open **P3** (conformance suite + federation contract + `iii/` wrapper).
5. Forward: P4 execution charter → P5 harmonization plan.

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
