---
campaign_id: campaign_canvas_genesis_planning
type: campaign
title: "Operation Cartography — aDNA Canvas Standard, genesis planning"
owner: stanley
status: in_progress
phase_count: 6
mission_count: 0
estimated_sessions: "8-14"
estimation_class: governance-broad
priority: high
created: 2026-06-06
updated: 2026-06-06
last_edited_by: agent_stanley
tags: [campaign, genesis, planning, canvas, standard, framework]
---

# Campaign: Operation Cartography

> **Genesis-PLANNING campaign.** Produces (1) the forked-and-extended Standard spec, (2) the vault
> scaffold, and (3) an execution-campaign charter a later session runs to build it. **No runtime is
> built and no code is migrated here.** Phase gates are human gates — never auto-advance (SO-1).

## Goal

When this campaign is complete, Canvas.aDNA owns a ratified **aDNA Canvas Standard v2.0.0** specification
(forked from Obsidian Advanced Canvas / JSON Canvas, agentic-context-native), a conformance + federation
contract, and an approved **execution-campaign charter**. CanvasForge and LiteratureForge have a clear,
parity-preserving path to consume the Standard as producers. Canvas is positioned as a first-class context
object + interaction surface + universal 2D output substrate — with the standard-vs-runtime split resolved.

## Context

Two systems today both assemble positioned text + images + components: **CanvasForge** (Hermes — canvas as
spatial substrate; decks/comics) and **LiteratureForge** (Thoth — document forge; text-first, visuals routed
out to canvas). The thesis (operator architect brief, 2026-06-06): a *canvas* is a near-universal **output
primitive**, and forking Advanced Canvas into an agentic-context-native standard makes canvas a core context
object, a human/AI + human/human interaction surface, and the shared substrate for any two-dimensional output.
Canvas.aDNA becomes the standard-bearer; CanvasForge + LiteratureForge become producers.

Builds on: Canvas Standard v1.0.0 (`CanvasForge.aDNA/what/context/advanced_canvas/`), the lattice-protocol→
canvasforge extraction-shim precedent, the SiteForge forge pattern, the III consumer-federation pattern, the
LIP process (`lattice-labs/how/governance/lips/lip_0001_lip_process.md`), and the LiteratureForge visual-spec
seam (`spec_visual_contract.md`). Genesis skeleton + this charter authored at P0 (2026-06-06).

## Scope

### In Scope

- The forked **aDNA Canvas Standard v2.0.0** spec: file format, component model, panel/link semantics,
  round-trip protocol v2, context-object model, conformance levels, Obsidian degradation contract.
- Conformance-suite **spec** + federation contract (SiteForge forge pattern) + an `iii/` wrapper scaffold.
- The **execution-campaign charter** (build/migrate/validate) + an ecosystem harmonization plan.
- ADRs resolving D1–D7 (identity, CanvasForge relationship, LiteratureForge seam, component model, panel/link
  semantics, versioning/governance, context-object/primitive status).

### Out of Scope

- Building the runtime, writing validators/converters as runnable code, migrating `canvas_core`.
- Re-pointing the SS/CC consumer wrappers; superseding CanvasForge; touching the aDNA core primitive set.
- Any breaking change to CanvasForge or LiteratureForge. (All deferred to the execution campaign, gated.)

### Subsumes

| Plan/Mission | Status at Subsumption | Tasks Absorbed By |
|-------------|----------------------|-------------------|
| (none) | — | — |

## Phases & Missions

> Missions are chartered per-phase as each gate opens (kept thin until then, SO-3 context budget). Phase
> deliverables below are binding; mission decomposition is authored at phase entry.

### Phase P0: Charter & Persona Lock  ← **current; HELD at gate**

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| p0 | Charter + `adr_000_canvas_identity` + governance skeleton | 1 | — | in_progress |

**Deliverables:** this charter · `what/decisions/adr_000_canvas_identity.md` (category Δ1 / persona / mission /
scope boundary / upstream baseline + compatibility contract / v2.0.0 proposal) · `decision_register_genesis.md`
(D1–D7) · tuned governance · router row.
**Phase exit gate (operator):** lock **persona**, **category** (incl. Δ1 runtime split), **scope boundary**.

### Phase P1: Source Inventory & Fork Baseline

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| p1 | Source inventory + fork baseline | 2-3 | P0 lock | planned |

**Deliverables:** `p1_source_inventory.md` (catalog v1.0.0 doc, `CanvasBuilder` constants — `VALID_*`,
`TYPE_MAPPING`, `EDGE_TYPE_MAPPING`; the `advanced_canvas/` corpus ~22 files; Round-Trip Protocol;
graft_manifest; LF visual/format/genre specs) labeled **KEEP / EXTEND / SUPERSEDE / DEFER-TO-PRODUCER**;
`p1_fork_baseline.md` (what v2.0.0 inherits from Advanced Canvas + v1.0.0; the additive `_reserved` extension
map; **pin upstream Advanced Canvas version** — brief cites v5.6.6, confirm).
**Phase exit gate:** operator reviews the KEEP/EXTEND/SUPERSEDE classification.

### Phase P2: Standard Specification (core deliverable)

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| p2 | v2.0.0 spec + component model + panel/link + round-trip v2 + context-object | 3-4 | P1 | planned |

**Deliverables (in `what/specs/` + `what/decisions/`):** `spec_adna_canvas_standard.md` (normative v2.0.0;
JSON shape; `_reserved` extension block; `_lattice_meta`; node/edge schemas; conformance levels
Core/Extended/aDNA-Native; validation rules; Obsidian degradation contract) · `spec_component_model.md` (D4) ·
`spec_panel_link_semantics.md` (D5) · `spec_roundtrip_protocol_v2.md` · `spec_context_object.md` (D7) ·
ADRs resolving **D2/D3/D6**.
**Phase exit gate (heaviest):** operator signs off on the v2.0.0 spec + D2/D3 decisions.

### Phase P3: Conformance & Federation Contract

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| p3 | Conformance-suite spec + federation contract + `iii/` wrapper scaffold | 2 | P2 | planned |

**Deliverables:** `spec_conformance_suite.md` (Core/Extended/aDNA-Native checks; validator contract — location
resolved per D1/D2) · `spec_federation_contract.md` (sf_forge pattern: federation_ref + graft + version_policy
+ wrapper discipline; worked for CanvasForge + LiteratureForge + ≥1 net-new consumer) · reference
`.lattice.yaml` stub · `iii/CLAUDE.md` wrapper scaffold (federation_ref to III/Argus; specifies VR1–VR5 /
trap-pack / R11 **contracts** — engines stay in CanvasForge).
**Phase exit gate:** operator reviews the consumer-integration story end to end.

### Phase P4: Execution-Campaign Charter (the real output)

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| p4 | Author `campaign_canvas_genesis` build charter (15–25 missions) | 2 | P3 | planned |

**Deliverables:** `how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md` — extract/own the Standard
per D2; publish v2.0.0 schema + validators per the D1 split; conformance suite; migrate CanvasForge to consume
via `federation_ref` (deprecation-shim mirroring the lattice-protocol precedent); LF unification-seam migration
(D3); ≥1 net-new consumer (web/paper/letter); parity/regression gates (no CanvasForge/LiteratureForge output
regresses); cutover criteria + rollback + parity references.
**Phase exit gate:** operator approves the execution charter.

### Phase P5: Ecosystem Harmonization Plan

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| p5 | Harmonization plan + AAR | 1-2 | P4 | planned |

**Deliverables:** `p5_harmonization_plan.md` — file-by-file impact matrix across CanvasForge, LiteratureForge,
SiteForge, VisualDNA, III, and the SS/CC consumer wrappers; deprecation-shim strategy v1.0.0→v2.0.0;
upstream-contribution / LIP notes; router-row finalize; genesis-planning AAR + retro.
**Phase exit gate:** operator closes genesis planning; authorizes (or schedules) the execution campaign.

## Decision Points

| # | When | Decision | Status |
|---|------|----------|--------|
| D1 | P0 gate | Category: Framework vs Platform vs Standard-bearer sub-category — where do reference validators/converters live? (Δ1) | pending |
| — | P0 gate | Persona lock (Mondrian / Seshat / Mercator) | pending |
| — | P0 gate | Scope boundary (Standard-owns vs producer-owns) | pending |
| D2 | P2 | CanvasForge relationship: (A) extract Standard out → CanvasForge pure producer; (B) Canvas.aDNA owns spec+conformance, CanvasForge keeps `CanvasBuilder` as reference impl; (C) reject | pending |
| D3 | P2 | LiteratureForge seam: document expressible AS a canvas vs federated peers sharing component schemas (reconcile w/ Amendment-02) | pending |
| D6 | P2 | Versioning & governance: v2.0.0 line + LIP process + conformance levels + version_policy default | pending |
| D7 | P2 | Context-object / primitive status: canvas-as-primitive vs canvas-as-view (Δ2) — LIP path | pending |

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| Δ1 mis-categorization (Framework that ships runtime → really a Platform) | High | Resolve at P0 with explicit Standard-vs-reference-impl split; cite `spec_framework_ecosystem.md`. |
| Standard drift breaks Obsidian round-trip | High | C4 compatibility contract: additive `_reserved` only; degradation test in conformance suite. |
| CanvasForge/LiteratureForge output regression on migration | High | P4 parity/regression gates vs locked baselines (Wilhelm 8.80 / Issue 01 8.43); execution-only, gated. |
| Canvas-as-primitive over-reach into aDNA core (Δ2) | Medium | Treat as a LIP (D7); do not touch the core primitive set in this campaign (out of scope). |
| Scope creep into building during planning | Medium | Hard constraint C3; deliverables are specs + charter only. |

## Verification Strategy

### Per-Mission
| Check | Method | Gate? |
|-------|--------|-------|
| SITREP filed | Session closure protocol | Yes |
| AAR produced (5-line) | AAR protocol | Yes — at mission close |
| Deliverables validated | AAR scorecard | Yes |
| Files committed | `git status` clean | Yes |

### Per-Phase
| Check | Method | Gate? |
|-------|--------|-------|
| Phase exit criteria met | this charter's phase gates | Yes — operator approval |
| Repo-vs-brief deltas surfaced | SITREP (trust-the-repo) | Yes |
| Scope changes documented | this charter | Yes |

## Timeline

| Phase | Missions | Sessions |
|-------|----------|----------|
| P0 Charter | 1 | 1 |
| P1 Inventory | 1 | 2-3 |
| P2 Spec | 1 | 3-4 |
| P3 Conformance/Federation | 1 | 2 |
| P4 Execution charter | 1 | 2 |
| P5 Harmonization | 1 | 1-2 |
| **Total** | **6 phases** | **8-14** |

## Hard Constraints (architect brief C1–C9)

C1 fork via `skill_project_fork` (done). · C2 never modify `.adna/`; router gets a one-line row only. ·
C3 no code migration / no runtime / no breaking changes this campaign. · C4 round-trippable to baseline
Obsidian; aDNA extensions additive in `_reserved`; pin upstream baseline. · C5 preserve v1.0.0 invariants
unless an ADR supersedes; clean successor v2.0.0. · C6 quality loops consumed from III via `iii/` wrapper
(specify contracts, don't re-implement engines). · C7 consumer integration conforms to `sf_forge_pattern_spec.md`;
show CanvasForge + LiteratureForge + ≥1 net-new consumer. · C8 substrate-neutrality — application-specific logic
stays in producers. · C9 every mission ends with SITREP + Next-Session Prompt + 5-line AAR; ISS for operator gates.

## Notes

- Repo verification (2026-06-06) confirmed the brief's anchors and surfaced two deltas (Δ1 category/runtime,
  Δ2 primitive/view) now foregrounded at the P0 gate. Inherited template example ADRs (`adr_001/002/003`) +
  `campaign_adna_workspace_upgrade/` are generic scaffold, reconciled in P1.

## Completion Summary

*Fill out when setting `status: completed`.*

## Campaign AAR

*Mandatory before `status: completed` (see `how/templates/template_aar_lightweight.md`).*
