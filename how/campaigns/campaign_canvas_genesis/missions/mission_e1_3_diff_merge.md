---
plan_id: mission_e1_3_diff_merge
type: plan
title: "E1.3 — Advisory reverse path: diff / merge / preserve_positions"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 1
campaign_mission_number: 6
mission_class: implementation
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, execution, e1, canvas_std, roundtrip, merge]
---

# Mission: E1.3 — diff / merge / preserve_positions

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|campaign_canvas_genesis]] (Operation Keystone) · **Phase**: E1 · **Mission**: E1.3 (depends on E1.2)

> Implements the advisory reverse-path helpers in `roundtrip.py` (spec_roundtrip_protocol_v2 §5).

## Objectives
- **`diff(a, b)`** — completed. Structured topology/position diff: nodes added/removed/modified, positions_changed, edges added/removed, topology_changed.
- **`preserve_positions(target, reference)`** — completed. Copies x/y/w/h from reference onto matching node ids (G1; positions survive forward regen).
- **`merge(source, canvas, strategy)`** — completed. Three-way: canvas owns topology + positions, source owns semantics; `yaml_wins` (default) / `canvas_wins`; conflicts flagged; bad strategy rejected.

## Notes
- Authority matrix honored verbatim (KEEP): source semantics win, canvas positions win, conflicts → human review.
- `preserve_positions` exported from `canvas_std`; smoke test gains a diff/merge liveness check.

## AAR
- **Worked**: `merge` reuses `from_canvas` to recover canvas semantics, so the three-way logic stayed small + testable.
- **Didn't**: n/a.
- **Finding**: representing a merge conflict as a flagged record (not an exception) keeps the reverse path advisory — the human resolves, the tool never auto-picks silently.
- **Follow-up**: E1.4 — `_reserved` validators (A-* checks); flips the `adna_native` validate-xfail.
