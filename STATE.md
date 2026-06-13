---
type: state
created: 2026-06-06
updated: 2026-06-12
status: active
last_edited_by: agent_stanley
last_session: session_stanley_20260612_220328_p2_ratify_p3
tags: [state, governance, canvas, genesis]
---

# Operational State

Dynamic operational snapshot for cold-start orientation. Updated each session.

## Current Phase

**Genesis-planning — Operation Cartography. P2 RATIFIED + P3 (Conformance & Federation) DELIVERABLES COMPLETE 2026-06-12 — HELD at the P3 exit gate.**
`how/campaigns/campaign_canvas_genesis_planning/campaign_canvas_genesis_planning.md`

P0 (2026-06-06) → P1 cleared → **P2 ratified 2026-06-12** (operator signed off: D2 extract / D3 schema-absorb+federated / D6 governance + the 5 specs are `ratified`; Δ2 stays an open LIP) → **P3 executed 2026-06-12** (conformance suite + federation contract + reference `.lattice.yaml` + `iii/` wrapper scaffold). **Operator reviews the consumer-integration story to clear the P3 gate; P4 does not open until then** (SO-1). Planning campaign — specs + contracts only, no runtime (C3).

## ▶ Resume Here — P3 exit gate (operator reviews the consumer story)

P3 deliverables are **authored and HELD at the gate**. The operator reviews the **end-to-end consumer-integration story**:
1. **Format vs. quality split:** [[what/specs/spec_conformance_suite|spec_conformance_suite]] checks *format* (Core/Extended/aDNA-Native + degradation D-1..D-3; validator → `canvas_std`); the [[iii/CLAUDE|iii/ wrapper]] routes *quality* (VR1–VR5 + canvas-visual trap schema — **owned here**, III runs the engines).
2. **Federation:** [[what/specs/spec_federation_contract|spec_federation_contract]] (sf_forge pattern; `canvas/` wrapper + `federation_ref` + 5-stage gates) with **3 worked consumers** — CanvasForge (post-D2 extraction), the LF-successor (D3 federated producer), and a net-new "letter" producer. Reference shape: `what/lattices/examples/example_canvas_v2.lattice.yaml`.

**On sign-off →** open **P4** (execution-campaign charter: build `canvas_std`, migrate CanvasForge via deprecation shim, stand up the LF-successor + ≥1 net-new consumer, parity/regression gates). Do not open P4 without the gate (SO-1).

**Ratified inputs (P2):** the v2.0.0 spec set + `adr_001` (extract) / `adr_002` (A-schema+federated; absorb/C set aside) / `adr_003` (governance). **Open:** the Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]], keep-as-view default). Reference impl `what/code/canvas_std/` declared-not-built (C3; P4). III pin v0.4.0 confirm-at-wiring.

## Parked — execution-campaign candidates (no gate change)

- **2026-06-07** — `[[how/campaigns/campaign_canvas_genesis_planning/missions/mission_deck_generator_canvas_pilot|mission_deck_generator_canvas_pilot]]` + `[[how/backlog/idea_deck_generator_canvas_pilot|idea_deck_generator_canvas_pilot]]`: a graph→canvas-object **deck generator** (Lattice Protocol technical brief as pilot; persona-III + accuracy-guardrail method captured), migrated from an `aDNALabs.aDNA` deck-building process. **Parked** — feeds the P4 execution charter; informs D2/D4/D7. Opens no phase, builds no code (C3). Operation Cartography itself is **unchanged** (P0-ratified / P1-awaiting-go).

## What's Done (this session — P2 ratify + P3, 2026-06-12)

- **Ratified the P2 set** (operator gate "Ratify all → P3"): flipped `adr_001/002/003` + the 5 specs `proposed`→`ratified`; resolved D2 (extract) / D3 (A-schema + B-federated; absorb/C set aside) / D6 / D7 (keep-as-view, Δ2 = open LIP); updated the decision register + `what/specs/AGENTS.md`.
- **Executed P3:** `spec_conformance_suite` (C-/E-/A- check sets + degradation tests D-1..D-3 + validator contract) · `spec_federation_contract` (sf_forge pattern; `canvas/` wrapper + federation_ref + 5-stage gates; **3 worked consumers** — CanvasForge / LF-successor / net-new letter) · `what/lattices/examples/example_canvas_v2.lattice.yaml` (reference stub) · `iii/CLAUDE.md` wrapper scaffold + empty learning store (VR1–VR5 + trap schema owned here, III engines upstream).
- Tracking: `mission_p3_conformance_federation` + `canvas_genesis_planning_p3_aar` (4/4 validated); campaign (P2/P3 rows, Decision Points → ratified, P3 phase AAR, mission_count→3); this STATE.

## Verified Ground Truth (anchors)

- Substrate already exports **PDF** (`canvas_core/pdf_export.py`, ADR-010) + **Google Docs** (`canvas_core/gdoc_export.py`, ADR-011) — the "anything-2D" thesis is grounded in shipped code.
- **Canvas Standard v1.0.0** at `CanvasForge.aDNA/what/context/advanced_canvas/` (standard + roundtrip); invariants real (`_lattice_meta` required, `_reserved` extension carrier, type→color/shape, `toEnd:"arrow"`, YAML-authoritative). `CanvasBuilder` has `read_back/diff/merge/validate/compute_sync_hash`.
- **LIP process** real: `lattice-labs/how/governance/lips/lip_0001_lip_process.md` (latest LIP-0007 ISS, 2026-05-30) → D6 mechanism.
- **Extraction-shim precedent**: `lattice-protocol/extensions/canvas/__init__.py` → `canvasforge.canvas_core` (model for D2).
- **SiteForge forge pattern** (`sf_forge_pattern_spec.md`): federation_ref + graft_manifest + `version_policy: minor` + 5-stage gates (C7).
- **LiteratureForge seam** real (`spec_visual_contract.md` V1–V8 + X1–X14; 5-part `spec_genre_submodule.md`); Amendment-02 Document-DNA engine **complements** (D3).

## Active Blockers

- None blocking. **Next gate:** operator reviews the consumer-integration story at the **P3 exit gate** (one phase per gate, SO-1).

## Next Steps

1. ✅ P0 (2026-06-06) · ✅ P1 cleared · ✅ **P2 ratified** (D2 extract / D3 schema-absorb+federated / D6 + 5 specs) — 2026-06-12.
2. ✅ P3 executed 2026-06-12 (conformance suite + federation contract + reference stub + `iii/` wrapper) — **HELD at the P3 exit gate**.
3. **P3 gate:** operator reviews the end-to-end consumer story (format-vs-quality split; 3 worked consumers) → on approval, open **P4** (execution-campaign charter: build `canvas_std`, migrate CanvasForge via shim, LF-successor, ≥1 net-new consumer, parity gates).
4. Forward: P4 execution charter → P5 harmonization plan. (Δ2 canvas-as-primitive LIP is an open, separate track.)

## Notes

- Inherited template example ADRs (`adr_001/002/003`) and the example campaign `campaign_adna_workspace_upgrade/` are generic-aDNA scaffold, NOT Canvas-canonical. The Canvas ADR namespace begins at `adr_000`; D2–D7 are minted as real ADRs in P2 (carried as stubs in `decision_register_genesis.md` until then). Reconcile/renumber the inherited examples in P1.
