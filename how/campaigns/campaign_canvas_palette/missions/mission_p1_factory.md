---
plan_id: mission_p1_factory
type: plan
title: "P1 — Producer factory: skill_canvas_producer_build + what/production/_scaffold"
owner: stanley
status: completed
campaign_id: campaign_canvas_palette
campaign_phase: 1
campaign_mission_number: 2
mission_class: build
created: 2026-06-21
updated: 2026-06-21
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, production, palette, factory, skill, scaffold]
---

# Mission: P1 — Producer factory (skill + scaffold)

**Campaign**: [[how/campaigns/campaign_canvas_palette/campaign_canvas_palette|campaign_canvas_palette]]
**Phase**: 1 — Factory hardening
**Mission**: 2 of 5

## Goal

Graduate the proven-5× producer pattern into reusable tooling so every future producer is fill-in-the-blanks:
(1) `how/skills/skill_canvas_producer_build.md` — an `agent` skill operationalizing `context_canvas_producer_pattern.md`
into a step-by-step runbook; (2) `what/production/_scaffold/` — an inert copy-me producer skeleton at producer depth.
P2 (letter) is the factory's acceptance test — it must build by following the skill + cloning the scaffold.

## Exit Gate (P1→P2, HUMAN)

Skill reads as a faithful runbook of the pattern doc (4-step pipeline · package shape · four+1 suite · venv recipe ·
conformance-vocabulary checklist · firewall/`iii` gate); `_scaffold` is structurally complete with TODO-stubbed
`src`/`tests` and excluded from the cross-producer sweep; `git diff --stat -- what/code/canvas_std/` empty; AAR GO.
**HELD before P2.**

## Objectives

### 1. Author `skill_canvas_producer_build.md`
- **Status**: completed
- **Session**: session_stanley_20260621_234513_palette_p1_factory
- **Description**: Write the agent skill via `template_skill.md`, sourced from `what/context/context_canvas_producer_pattern.md`. Steps: pick surface shape (single vs multi-page) → clone `_scaffold` → substrate-free `model.py` → `consume.py` source contract → `to_canvas` + `_reserved` enrich → four+1 tests → venv + run → `canvas-std validate` → firewall + `iii/` gate. Include the conformance-vocabulary checklist + anti-patterns.
- **Files**: `how/skills/skill_canvas_producer_build.md`
- **Depends on**: none

### 2. Build `what/production/_scaffold/`
- **Status**: completed
- **Session**: session_stanley_20260621_234513_palette_p1_factory
- **Description**: Inert copy-me skeleton at producer depth (so `../../code/canvas_std` paths stay valid): `pyproject.toml`, `README.md`, `AGENTS.md`, `iii_quality_contract.md`, `.gitignore`, `src/__PRODUCER__/{model,consume,layout,__main__,__init__}.py` (TODO-stubbed), `tests/{conftest,test_conformance,test_roundtrip,test_degradation,test_components,test_model_neutrality}.py` (TODO stubs), `examples/.gitkeep`. Stub tests skip (no false failures); README documents the clone-and-rename recipe.
- **Files**: `what/production/_scaffold/**`
- **Depends on**: none

### 3. Verify
- **Status**: completed
- **Session**: session_stanley_20260621_234513_palette_p1_factory
- **Description**: Confirm scaffold structure complete; relative paths valid; `_scaffold` excluded from the named-producer sweep; firewall `git diff --stat -- what/code/canvas_std/` empty. (Full clone test is P2.)
- **Files**: (verification only)
- **Depends on**: 1, 2

## Campaign Context

### Previous Mission Outputs
- P0.1 ratified the 6 decisions (D2 fixes the factory homes + scaffold-at-producer-depth).

### Next Mission Inputs
- P2 (letter) clones `_scaffold` → `letter_generator` by following the skill — the factory's acceptance test.

## Notes

The skill + scaffold encode `context_canvas_producer_pattern.md` (the mature pattern doc graduated at Atelier A3) +
the conformance vocabulary from `what/code/canvas_std/src/canvas_std/{reserved,schema,conformance}.py`. No edit to
`canvas_std` (firewall). `_scaffold` placeholder package dir name `__producer__` is renamed on clone.

## Completion Summary

### Deliverables
- **`how/skills/skill_canvas_producer_build.md`** — agent skill (runbook): when-to-use, inputs, the 6-step procedure (clone → model → consume → tests → venv/run → firewall/`iii` gate), the conformance-vocabulary checklist, 7 anti-patterns, outputs + verification. Authored from `context_canvas_producer_pattern.md` + the verified `canvas_std` API.
- **`what/production/_scaffold/`** (17 files) — inert copy-me producer skeleton at producer depth: `pyproject.toml`/`README.md`/`AGENTS.md`/`iii_quality_contract.md`/`.gitignore` + `src/__producer__/{__init__,model,consume,layout,__main__}.py` (TODO-stubbed; `consume.py` carries the canonical 4-step contract verbatim) + `tests/` six-file "four+1" (module-level `pytest.skip` so the template never reports a false failure) + `examples/.gitkeep`.

### Descoped
- None. (Optional poster/one-pager remain P4-if-budget per D6.)

### Key Findings
- `py_compile` clean across all 11 scaffold `.py`; firewall git-diff 0; `_scaffold` (underscore) sorts apart from the 5 named producers so the cross-producer sweep never collects it.
- Placing the scaffold at `what/production/_scaffold/` (D2) means the `../../code/canvas_std` editable-install path is correct the instant it's cloned — no path surgery, the one real fragility the retrospective flagged.

### Scope Changes
- None.

## AAR

- **Worked**: cloning the real diagram_generator's pyproject/consume/test shapes into the scaffold gave a high-fidelity template fast; module-level `pytest.skip` makes the stubs inert without deleting the useful copy-guide code beneath.
- **Didn't**: n/a — no execution surprises; the scaffold isn't run in CI (P2's clone is its live acceptance test).
- **Finding**: the producer pattern compressed into a skill + scaffold with zero Standard touch — the factory is pure tooling on the production shelf.
- **Change**: none — pattern transferred 1:1 from the pattern doc.
- **Follow-up**: P2 — clone `_scaffold` → `letter_generator` (the factory's acceptance test) ([[how/campaigns/campaign_canvas_palette/missions/mission_p2_letter|mission]]).
