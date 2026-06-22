---
plan_id: mission_p2_letter
type: plan
title: "P2 — letter_generator (warm-up; pilots the scaffold)"
owner: stanley
status: completed
campaign_id: campaign_canvas_palette
campaign_phase: 2
campaign_mission_number: 3
mission_class: build
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, production, palette, letter, producer]
---

# Mission: P2 — letter_generator (warm-up; pilots the scaffold)

**Campaign**: [[how/campaigns/campaign_canvas_palette/campaign_canvas_palette|campaign_canvas_palette]]
**Phase**: 2 — Letter producer
**Mission**: 3 of 5

## Goal

Build `what/production/letter_generator/` by cloning `_scaffold` and following `skill_canvas_producer_build.md` — a
one-page letter producer (`§6.3` geometry: single canonical surface, one `region` `{flow: vertical, pagination: paged,
extent: {unit: pages, max: 1}}`, `profile: document`), emitting **aDNA-Native** (D3). This doubles as the factory's
**live acceptance test**: if the skill/scaffold are awkward, harden them here before P3.

## Exit Gate (P2→P3, HUMAN)

Full letter four+1 suite green + `ruff` clean; worked example validates `adna_native [OK]` and degrades (D-1/D-2/D-3);
`git diff --stat -- what/code/canvas_std/` empty; AAR GO; any factory friction folded back into the skill/scaffold.
**HELD before P3 (post).**

## Objectives

### 1. Clone + implement letter_generator
- **Status**: completed
- **Session**: session_stanley_20260622_000541_palette_p2_letter
- **Description**: Clone `_scaffold` → `letter_generator` (rename `__producer__`); `model.py` (Letter: letterhead, date, recipient block, salutation, body paragraphs, closing, signature, refs); `consume.py` (single `letter_root` surface; interior baseline `text` nodes per block; one paged region `{unit: pages, max: 1}`; `profile: document`; aDNA-Native enrich); `layout.py` (deterministic vertical stack); `__main__.py` CLI.
- **Files**: `what/production/letter_generator/**`
- **Depends on**: none

### 2. Tests + worked example
- **Status**: completed
- **Session**: session_stanley_20260622_000541_palette_p2_letter
- **Description**: The four+1 suite (conformance · round-trip · degradation · components + a letter-coverage test + model-neutrality), real assertions (remove scaffold skips); a worked `examples/<x>.yaml` + built `.canvas`. venv + `pytest` green; `ruff` clean; `canvas-std validate` → `adna_native [OK]`.
- **Files**: `what/production/letter_generator/tests/**`, `examples/**`
- **Depends on**: 1

### 3. Verify + factory feedback
- **Status**: completed
- **Session**: session_stanley_20260622_000541_palette_p2_letter
- **Description**: Firewall `git diff --stat -- what/code/canvas_std/` empty; degradation report all-True; fold any skill/scaffold friction back into P1 artifacts. HOLD at P2→P3.
- **Files**: `how/skills/skill_canvas_producer_build.md` / `what/production/_scaffold/` (only if friction found)
- **Depends on**: 1, 2

## Campaign Context

### Previous Mission Outputs
- P1 shipped the factory (`skill_canvas_producer_build.md` + `_scaffold`). P0 fixed letter level = `adna_native` (D3), name = `letter_generator` (D5).

### Next Mission Inputs
- P3 (post) builds on the same factory; letter validates the single-surface path; post adds the multi-panel/thread path.

## Notes

Letter is the smallest producer (single page, single surface) — the warm-up. `§6.3` geometry is adopted; the only
design choice already settled is `adna_native` over the §6.3 `extended` sketch (D3). Firewall: never edit `canvas_std`.

## Completion Summary

### Deliverables
- **`what/production/letter_generator/`** — net-new one-page-letter producer on `canvas_std`: substrate-free `model.py` (`Letter` + `load_letter`), `consume.py` (`build_letter`: `letter_root` canonical surface + per-block baseline `text` nodes + `reading_order` edges + one paged region `{unit: pages, max: 1}`, `profile: document`), deterministic `layout.py`, `letter-generator` CLI.
- **Suite green: 17 passed**, `ruff` clean; worked example (`examples/example_letter.yaml` → `example_letter.canvas`, 10 nodes / 8 edges) validates **`adna_native [OK]`** + degrades (D-1/D-2/D-3 True); **`canvas_std` firewall git-diff 0.**
- Letter-specific `README.md` / `AGENTS.md` / `iii_quality_contract.md` (lenses: correctness · tone/register · legibility · rigor · accuracy).

### Descoped
- None. (`§6.3` `extended` minimal sketch not used — D3 chose `adna_native` for family uniformity.)

### Key Findings
- **The factory works end-to-end:** a conformant producer was built by cloning `_scaffold` + following `skill_canvas_producer_build.md`, with **zero `canvas_std` touch**. The single-surface path (root group + paged region + reading_order chain) is the cheapest producer shape yet.
- All component tokens checked against `canvas_std/reserved.py` (`text`/`panel` ∈ `COMPONENT_CLASSES`; component `semantic_type` is free-form/uniun-checked) — no enum fights, no LIP needed.

### Scope Changes
- The P2 build was started by a delegated build agent that hit a session limit mid-run; the persona completed the rename (`pyproject` + tests), the missing `test_letter.py`, the worked example, and the venv/green run. No design change.

## AAR

- **Worked**: the scaffold + skill produced a green producer fast; the module-level `pytest.skip` template pattern made the half-finished clone safe (no false greens — the unrenamed tests were *skipped*, not silently passing).
- **Didn't**: the delegated build agent ran out of budget before finishing the rename + example + venv — a reminder that producer builds should be sized to a single agent budget or checkpointed.
- **Finding**: the factory needs no changes — the only gap was an interrupted run, not a tooling flaw; the README's `grep -rl __producer__ | xargs sed` one-liner catches every placeholder when actually run.
- **Change**: none to the factory; letter is now the canonical single-surface exemplar alongside deck/diagram.
- **Follow-up**: P3 — `post_generator` (single + thread; the multi-panel path) ([[how/campaigns/campaign_canvas_palette/missions/mission_p3_post|mission]]).
