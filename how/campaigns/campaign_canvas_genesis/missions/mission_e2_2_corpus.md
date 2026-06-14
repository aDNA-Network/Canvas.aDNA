---
plan_id: mission_e2_2_corpus
type: plan
title: "E2.2 — Canonical conformance corpus + harness test"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 2
campaign_mission_number: 10
mission_class: implementation
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, execution, e2, canvas_std, conformance, corpus]
---

# Mission: E2.2 — Conformance corpus

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|campaign_canvas_genesis]] (Operation Keystone) · **Phase**: E2 · **Mission**: E2.2 (depends on E2.1)

> The canonical conformance corpus: the golden fixtures + two boundary cases + a `validate_suite` harness test
> asserting `level_reached` + `ok` per fixture.

## Objectives
- **Boundary fixtures** — completed. `core_only_bad_shape.canvas` (valid Core, bad Extended shape → reaches Core only) + `adna_bad_reserved.canvas` (Extended-valid, wrong `_reserved.conformance_level` → reaches Extended).
- **Manifest** — completed. Added `expected_level_reached` + `expected_ok` to all 6 entries.
- **`test_conformance.py`** — completed. Runs `validate_suite` over the corpus; asserts level_reached/ok/failed + degradation-only-for-aDNA-Native.

## Notes
- Updated `test_fixtures.py` so the "declares clean conformance_level" check skips deliberately-broken aDNA fixtures.
- Suite now: **`pytest` 46 passed / 8 skipped; `ruff` clean.**

## AAR
- **Worked**: the two boundary fixtures pin the monotone level logic (reaches-Core-only, reaches-Extended-only) — exactly the cases a single happy-path fixture can't exercise.
- **Didn't**: n/a.
- **Finding**: a deliberately-broken aDNA fixture needs the "clean conformance_level" assertion gated on `expected_valid` — broken fixtures legitimately carry wrong metadata.
- **Follow-up**: E2.3 — publish the v2.0.0 JSON Schema + the `canvas-std` CLI (last E2 mission).
