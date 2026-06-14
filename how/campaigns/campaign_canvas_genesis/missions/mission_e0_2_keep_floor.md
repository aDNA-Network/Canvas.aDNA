---
plan_id: mission_e0_2_keep_floor
type: plan
title: "E0.2 — Port the verbatim KEEP floor into schema.py"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 0
campaign_mission_number: 2
mission_class: implementation
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, execution, e0, canvas_std, keep-floor]
---

# Mission: E0.2 — Port the verbatim KEEP floor

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|campaign_canvas_genesis]] (Operation Keystone)
**Phase**: E0 — Bootstrap `canvas_std` · **Mission**: E0.2 (depends on E0.1)

> Transcribe the **verbatim** KEEP floor from `p1_fork_baseline.md` §3 (itself a verbatim extraction of
> `CanvasForge.canvas_core.core.py`) into `src/canvas_std/schema.py`. **No values are invented** — fidelity to the
> baseline is what guarantees a valid aDNA canvas degrades to a valid Obsidian canvas.

## Goal

`schema.py` carries the 10 `VALID_*` enums, the node/edge required-field sets, and the built-in `lattice`
semantic profile (`TYPE_MAPPING` 8 entries + `EDGE_TYPE_MAPPING` 5 entries), exactly as ratified.
`schema.is_floor_loaded()` returns `True`; the smoke test asserts the floor + spot-checks key values.

## Objectives

### 1. Port the enums + required fields + lattice profile (verbatim)
- **Status**: completed — all 10 `VALID_*` enums, `NODE_REQUIRED_FIELDS`/`EDGE_REQUIRED_FIELDS`, `TYPE_MAPPING`,
  `EDGE_TYPE_MAPPING` transcribed from `p1_fork_baseline` §3.

### 2. Extend the smoke test
- **Status**: completed — assert `is_floor_loaded()`; spot-check `module→{"4",predefined-process,file}`,
  `optional→{dotted,triangle-outline,…,arrow}`, enum membership.

## Notes
- `VALID_COLORS` = the 7 string slots `"0".."6"`; `validate()` additionally accepts `#`-hex (handled in
  `validate.py` at E1.1, not as an enum member here).
- Profile value keys mirror the legacy `core.py`: nodes `{color, shape, node_type}`; edges
  `{path_style, arrow, from_end, to_end}`.

## Completion Summary
### Deliverables
- `schema.py` populated with the verbatim KEEP floor; smoke test green (floor loaded + spot-checks).

## AAR
- **Worked**: P1's verbatim capture made this a direct transcription — no re-derivation, no upstream re-read.
- **Didn't**: n/a.
- **Finding**: keeping the legacy value-key names (`node_type`, `path_style`) eases the E3 CanvasForge extraction parity check.
- **Change**: none.
- **Follow-up**: E0.3 — golden-canvas fixtures + the test harness scaffold.
