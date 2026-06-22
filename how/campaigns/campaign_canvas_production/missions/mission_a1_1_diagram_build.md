---
plan_id: mission_a1_1_diagram_build
type: plan
title: "A1.1 — Build diagram_generator (all 5 types) on canvas_std"
owner: stanley
status: completed
campaign_id: campaign_canvas_production
campaign_phase: 1
campaign_mission_number: 2
mission_class: implementation
created: 2026-06-21
updated: 2026-06-21
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, production, atelier, diagram, build]
---

# Mission: A1.1 — Build `diagram_generator` (all 5 types) on `canvas_std`

**Campaign**: [[how/campaigns/campaign_canvas_production/campaign_canvas_production|campaign_canvas_production]]
**Phase**: 1 — Diagram producer (warm-up)
**Mission**: 2 of 8 (A1.2 folded in)

## Goal

Build `what/production/diagram_generator/` — a net-new, self-contained producer on the already-shipped `canvas_std`
that turns a substrate-free `DiagramInput` into a v2.0.0 **aDNA-Native** `.canvas`, mirroring the `deck_generator`
pattern. Native nodes+edges are canonical; a single derived Mermaid `code` node carries the regenerable source. Ports
the 5 Mermaid syntax generators from the archived quarry (theme coupling stripped). When complete, the diagram
production layer Canvas absorbed at pt09 is real and green, and the campaign can proceed to comic (A2).

## Exit Gate (= A1→A2 phase gate, HUMAN)

- Full `diagram_generator` test suite green (~16–22 tests); `ruff` clean.
- Every diagram type (flowchart, sequence, class_diagram, state_diagram, gantt) builds + validates **aDNA-Native**
  (`canvas-std validate … → adna_native [OK]`) and degrades clean (D-1/D-2/D-3).
- A worked example committed (`.yaml` + generated `.canvas`).
- No regression in the other suites (`canvas_std` 80/10 · brief 10 · deck 16 · document 37).
- `canvas_std` firewall git-diff 0.
- `iii_quality_contract.md` present (light diagram contract per D1).
- **HOLD** for operator before opening A2 (comic).

## Objectives

### 1. Skeleton + model + ported syntax + flowchart/sequence end-to-end
- **Status**: completed
- **Session**: session_stanley_20260621_194755_a1_diagram_build
- **Description**: Clone the deck_generator package shape; write substrate-free `model.py` (`DiagramInput`/`DiagramNode`/`DiagramEdge` + `load_diagram`); port `mermaid.py` (5 generators + `validate()`, theme stripped) from the quarry; write `diagrams.py` (per-type canvas builders), `layout.py` (integer graph geometry), `consume.py` (assemble source → `to_canvas` → enrich `_reserved`), `__main__.py` CLI. Get **flowchart + sequence** building + validating aDNA-Native end-to-end.
- **Files**: `what/production/diagram_generator/{pyproject.toml,README.md,AGENTS.md,src/diagram_generator/*.py}`
- **Depends on**: A0.1 (ratified)

### 2. Remaining types + full test suite + example + quality contract
- **Status**: completed
- **Session**: session_stanley_20260621_194755_a1_diagram_build
- **Description**: Add class_diagram / state_diagram / gantt builders; full test suite (conformance · round-trip incl. a cyclic flowchart · degradation incl. no-out-of-enum-shape · components · per-type coverage); a worked example (`.yaml` + `.canvas`); `iii_quality_contract.md` (light). Run no-regression across all suites; confirm firewall git-diff 0.
- **Files**: `what/production/diagram_generator/{tests/*,examples/*,iii_quality_contract.md}`
- **Depends on**: 1

## Campaign Context

### Previous Mission Outputs
- A0.1 ratified the 6 contract/profile decisions (defaults): light quality contract, producer-side `diagram` profile (no LIP), shape-enum safe path, all-5 types (flowchart+sequence first), Operation Atelier codename.

### Next Mission Inputs
- A2 (comic) reuses this producer's established pattern + the canvas-mapping/`_reserved` conventions proven here.

## Notes

**Load-bearing guardrails (from the approved plan + verified against `canvas_std`):**
- `canvas_std` is **immutable** — never edit `what/code/canvas_std/`; verify `git diff --stat -- what/code/canvas_std/` empty.
- **Shape-enum trap:** `VALID_SHAPES` lacks `rect/round/stadium`; carry Mermaid shapes in `_reserved…qualities.shape`, baseline node `type:"text"`, never set baseline `styleAttributes.shape`.
- **A-5 acyclicity:** flowchart/state edges = `dependency`/`reading_order` (may cycle); `sequence` only for gantt/linear (acyclic).
- **One canonical surface** (A-5): the diagram root group. **Profiles producer-side:** `{"profile":"diagram"}`, no inline out-of-enum bindings.
- **Quarry, not dependency:** port from `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_core/mermaid.py`; the producer must not import `canvas_core`.

Full design (package layout, canvas mapping rationale, port-vs-new, `_reserved` enrichment, test list) in the approved
plan `~/.claude/plans/please-read-the-claude-md-lovely-star.md` (§"Diagram producer").

## Completion Summary

### Deliverables
- `what/production/diagram_generator/` — a net-new producer on `canvas_std` (~656 src LOC across 7 modules): substrate-free `model.py`, ported `mermaid.py` (5 generators, theme stripped), `diagrams.py`, `layout.py`, `consume.py`, `__main__.py` CLI, `__init__.py`; `pyproject.toml`, `README.md`, `AGENTS.md`, `iii_quality_contract.md` (light).
- All 5 diagram types (flowchart · sequence · class_diagram · state_diagram · gantt) build + validate **aDNA-Native** + degrade (D-1/D-2/D-3). Suite **36/36**, `ruff` clean. Worked example committed (`examples/canvas_standard_flow.{yaml,canvas}`).
- Hybrid native-primary mapping: native nodes+edges canonical (one `diagram_root` canonical surface) + a derived `code` node carrying the regenerated Mermaid source.

### Descoped
- None (A1.2 folded in — all 5 types delivered in one mission).

### Key Findings
- The shape-enum trap held cleanly: shapes ride `_reserved…qualities.shape`, baseline nodes are `text`, no `styleAttributes.shape` set → E-2 + D-2 green. Cyclic flowchart/state diagrams validate because non-gantt edges use `dependency` (not the acyclicity-checked `sequence`).
- **Spec-gap erratum candidate (→ A3.1 LIP queue, `adr_003`):** `PL_EXTENT_UNITS = {words,pages,slides}` has no diagram/graph unit, so a diagram `region` cannot express `extent` (the producer omits it; valid since `extent` is optional). Worth a Standard erratum: add a graph/diagram extent unit, or document that single-surface graph regions legitimately omit `extent`.

### Scope Changes
- A1.2 folded into A1.1 at activation (one diagram-build mission).

## AAR

- **Worked**: Cloning the `deck_generator` pattern + porting the quarry's Mermaid generators produced a faithful, fully green producer fast; native-primary mapping round-trips with a meaningful sync-hash.
- **Didn't**: Nothing blocked — the one friction (no diagram `extent` unit) is a Standard gap, captured as an erratum candidate, not a producer defect.
- **Finding**: A diagram is the substrate's home turf (nodes + typed edges), so conformance was natural; the only Standard-side rough edge is `PL_EXTENT_UNITS`.
- **Change**: none.
- **Follow-up**: A2 — comic producer ([[how/campaigns/campaign_canvas_production/campaign_canvas_production|campaign]] Phase A2); erratum candidate → A3.1 LIP queue.
