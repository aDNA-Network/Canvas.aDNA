---
plan_id: mission_e2_1_conformance_harness
type: plan
title: "E2.1 — Conformance harness (validate_suite → ConformanceReport)"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 2
campaign_mission_number: 9
mission_class: implementation
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, execution, e2, canvas_std, conformance]
---

# Mission: E2.1 — Conformance harness

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|campaign_canvas_genesis]] (Operation Keystone) · **Phase**: E2 · **Mission**: E2.1 (depends on E1)

> Implements `validate_suite(doc, declared) → ConformanceReport` in `conformance.py` (spec_conformance_suite §1,§7).

## Objectives
- **`validate_suite`** — completed. Runs `validate` at each level (monotone) to compute `level_reached`; records `passed` levels + `failed` records (`{id, msg}`) at the declared level; attaches the D-1..D-3 `degradation` report for aDNA-Native.
- **`ConformanceReport`** — completed. `ok` + `meets_declared` properties.

## Notes
- `STANDARD_VERSION` lazy-imported inside `validate_suite` to avoid an import cycle during package init.
- A clean Core doc reaches `level_reached = extended` (it satisfies Extended's checks vacuously) — expected.
- Only the `canvas-std` CLI (`_cli`, E2.3) remains stubbed. `pytest` 31 passed / 4 skipped; `ruff` clean.

## AAR
- **Worked**: `validate_suite` is a thin composition over `validate` + `degradation_report` — the engine did the work, the harness just orchestrates + shapes the report.
- **Didn't**: n/a.
- **Finding**: parsing the error-string prefix (`"C-4: ..."`) into `failed[].id` gives a structured report without changing `validate`'s simple list-of-strings contract.
- **Follow-up**: E2.2 — the canonical conformance corpus + a `validate_suite` harness test over it.
