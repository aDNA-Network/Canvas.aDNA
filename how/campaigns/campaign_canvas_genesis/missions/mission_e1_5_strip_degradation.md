---
plan_id: mission_e1_5_strip_degradation
type: plan
title: "E1.5 — strip + the D-1..D-3 degradation tests (closes Phase E1)"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 1
campaign_mission_number: 8
mission_class: implementation
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, execution, e1, canvas_std, degradation]
---

# Mission: E1.5 — strip + degradation (closes Phase E1)

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|campaign_canvas_genesis]] (Operation Keystone) · **Phase**: E1 (final mission) · **Mission**: E1.5

> Implements `strip()` (the C4 degradation op) + a `degradation_report()` (D-1..D-3) in `validate.py`, retires the
> `xfail` markers in `test_fixtures.py`, and brings the **full pytest suite green** — closing Phase E1.

## Objectives
- **`strip(doc)`** — completed. Deep-copies + removes `metadata.frontmatter._reserved`; the original is untouched.
- **`degradation_report(doc)`** — completed. D-1 (`validate(strip,CORE)==[]`), D-2 (Extended-valid), D-3 (no `_reserved`).
- **Retire fixture xfails + green suite** — completed. `test_fixtures.py` `validate`/`strip` xfails removed (behavior now real); `pytest` = **30 passed, 4 skipped**; `ruff` clean.

## Notes
- After E1.5 the only stubs left are `validate_suite` (E2.1) + the `canvas-std` CLI (E2.3) — Phase E2.
- Ran the real suite in a `.venv` (`make install`); system Python 3.14 lacks pytest. `.venv` is gitignored.

## AAR
- **Worked**: the E0.3 golden fixtures + the xfail-then-retire pattern gave the whole engine a single, honest green-suite acceptance — every E1 sub-mission flipped its own fixture assertion.
- **Didn't**: had to reorder `__init__.py` (constants after re-exports) to satisfy ruff E402 — import-safe since submodules only import `schema`.
- **Finding**: `strip` deep-copies so degradation never mutates the source — the report is side-effect-free.
- **Change**: none.
- **Follow-up**: **E1→E2 phase boundary — check in.** Then E2.1 (the conformance harness `validate_suite`).
