---
plan_id: mission_e1_4_reserved
type: plan
title: "E1.4 — _reserved schema validators (A-* checks)"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 1
campaign_mission_number: 7
mission_class: implementation
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, execution, e1, canvas_std, reserved, conformance]
---

# Mission: E1.4 — `_reserved` validators (A-* checks)

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|campaign_canvas_genesis]] (Operation Keystone) · **Phase**: E1 · **Mission**: E1.4 (depends on E1.1)

> Implements `reserved.py` (the aDNA-Native A-* checks) + wires it into `validate()`. Flips the `adna_native`
> validate-xfail in `test_fixtures.py` to PASS.

## Objectives
- **`validate_reserved(reserved, doc)`** — completed. A-2 (adna_version semver + conformance_level), A-6 (sync + 16-hex hash), and delegation to the component/panel-link/context-object sub-validators.
- **`validate_component_types`** — completed. spec_component_model §7: keys resolve, `class` ∈ 14-class taxonomy, `degrades_to` ∈ baseline.
- **`validate_panel_link`** — completed. spec_panel_link_semantics §6: kind/region/surface ids resolve, enums, **exactly one canonical surface**, **sequence acyclicity** (DFS cycle-detect).
- **`_validate_semantic_bindings` / `_validate_context_object`** — completed. §6 tokens; semver version; well-formed refs.

## Notes
- `validate()` aDNA-Native branch now requires a populated `_reserved` and calls `validate_reserved(block, doc)`.
- Constants added: `COMPONENT_CLASSES`, `BASELINE_TYPES`, `PL_EDGE_KINDS`/`PL_FLOW`/`PL_PAGINATION`/`PL_EXTENT_UNITS`.

## AAR
- **Worked**: each sub-spec mapped to a focused sub-validator; the golden aDNA-Native fixture exercises every one in a single document, so one xfail→pass flip proves the whole A-* layer.
- **Didn't**: hash↔source matching (A-6) is structural-only here; the round-trip layer owns the real staleness check.
- **Finding**: a flagged conflict/cycle as a returned error (not an exception) keeps `validate()` total — callers always get a list.
- **Follow-up**: E1.5 — `strip` + the D-1..D-3 degradation tests (flips the last fixture xfails; closes Phase E1).
