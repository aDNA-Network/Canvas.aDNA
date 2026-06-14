---
plan_id: mission_e1_1_validate
type: plan
title: "E1.1 — Implement validate() for Core + Extended"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 1
campaign_mission_number: 4
mission_class: implementation
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, execution, e1, canvas_std, validate]
---

# Mission: E1.1 — `validate()` for Core + Extended

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|campaign_canvas_genesis]] (Operation Keystone)
**Phase**: E1 — Reference implementation (first mission) · **Mission**: E1.1 (depends on E0.1–E0.3)

> First behavior mission. Implements the **Core (C-*)** and **Extended (E-*)** checks of
> `spec_conformance_suite` in `validate.py`, against the KEEP-floor enums (E0.2) and the golden fixtures (E0.3).
> aDNA-Native (A-*) delegates to `reserved.py` (still `NotImplementedError` → E1.4); `strip()` stays E1.5.

## Goal

`validate(doc, level)` returns `[]` for the `core_minimal` + `extended_styled` fixtures, a non-empty error list
for `invalid_missing_arrow` (C-4), and raises `NotImplementedError` for `adna_native` (the A-* layer is E1.4).
The Core/Extended `validate` xfails in `test_fixtures.py` flip to PASS.

## Objectives

### 1. Core checks (C-1..C-5)
- **Status**: completed — nodes/edges arrays; node id-unique + type∈enum + integer geometry; edge required fields
  + sides∈enum + endpoints resolve; **C-4 every edge carries `toEnd` ∈ `VALID_ENDS`** (missing → reject, per I4 /
  the v1.0.0 "always include toEnd:arrow" requirement); color ∈ `VALID_COLORS` or `#`-hex.

### 2. Extended checks (E-1..E-4)
- **Status**: completed — `styleAttributes` shape/border/textAlign ∈ enums; edge path/arrow/pathfinding ∈ enums;
  `isStartNode`/`collapsed` boolean. Monotone over Core.

### 3. Wire levels + update smoke test
- **Status**: completed — `validate` runs Core, then Extended (Extended/aDNA-Native), then A-* (aDNA-Native →
  `NotImplementedError` until E1.4). Removed `validate` from the smoke test's NotImplemented-stub list.

## Notes
- **C-4 interpretation:** an edge that omits `toEnd` is rejected (the v1.0.0 requirement + the negative fixture);
  an explicit `toEnd:"none"` is permitted (undirected). Documented in `validate.py`.
- aDNA-Native validation intentionally raises until E1.4 — honest partial state; the fixture xfail stays xfailed
  for `adna_native` until then.

## Completion Summary
### Deliverables
- `validate.py` Core+Extended implemented; smoke test updated; core/extended fixture validate-xfails → PASS.

## AAR
- **Worked**: the KEEP-floor enums (E0.2) + golden fixtures (E0.3) made `validate` a direct spec-to-code mapping with a ready test corpus — the xfail→pass flip is the acceptance signal.
- **Didn't**: n/a.
- **Finding**: keeping aDNA-Native raising (not silently passing) until E1.4 prevents a false "valid" on unchecked `_reserved`.
- **Change**: none.
- **Follow-up**: E1.2 — `to_canvas`/`from_canvas`/`compute_sync_hash` in `roundtrip.py`.
