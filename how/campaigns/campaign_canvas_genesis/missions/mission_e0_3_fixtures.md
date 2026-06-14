---
plan_id: mission_e0_3_fixtures
type: plan
title: "E0.3 — Golden-canvas fixtures + test-harness scaffold"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 0
campaign_mission_number: 3
mission_class: implementation
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, execution, e0, canvas_std, fixtures, conformance]
---

# Mission: E0.3 — Golden fixtures + harness

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|campaign_canvas_genesis]] (Operation Keystone)
**Phase**: E0 — Bootstrap `canvas_std` (final mission) · **Mission**: E0.3 (depends on E0.1, E0.2)

> A small known-good canvas corpus + a manifest + the pytest harness that E1 fills in. The harness asserts what is
> checkable now (well-formed JSON, declared level, baseline shape) and **xfails** the `validate`/`strip` assertions
> until E1 implements them — so the suite stays green and the contract is ready.

## Goal

Golden fixtures at each conformance level + degradation + a negative case, a `manifest.json` describing expected
validity/level, and `tests/test_fixtures.py` exercising them. Completes E0; E1 implements behavior against this.

## Objectives

### 1. Golden-canvas fixtures
- **Status**: completed — `tests/fixtures/`: `core_minimal.canvas`, `extended_styled.canvas`,
  `adna_native.canvas` (populated `_reserved` + `_lattice_meta`), `invalid_missing_arrow.canvas` (negative).

### 2. Fixture manifest
- **Status**: completed — `tests/fixtures/manifest.json`: per-fixture `path` · `declared_level` · `expected_valid`
  · `degrades_to` · `note`.

### 3. Pytest harness scaffold
- **Status**: completed — `tests/test_fixtures.py`: loads each fixture (well-formed JSON), checks declared level +
  baseline node/edge shape; `validate()`/`strip()` assertions are `xfail(strict=False)` pending E1.

## Notes
- Fixtures are authored to the ratified specs (node/edge floor §4–§6; `_reserved` §7; `_lattice_meta` §8).
- `adna_native.canvas` doubles as the **degradation** case: `strip()` must drop `metadata.frontmatter._reserved`
  and the result must validate at `extended` (the E1.5 / D-1 target).

## Completion Summary
### Deliverables
- 4 fixtures + `manifest.json` + `test_fixtures.py`; **E0 bootstrap phase complete** (E0.1–E0.3 ✅).

## AAR
- **Worked**: authoring fixtures straight from the ratified specs gave the validator (E1) a concrete target before a line of validation logic exists — test-first by construction.
- **Didn't**: behavior can't be asserted yet (stubs) — harness xfails the validate/strip checks until E1; chose xfail over skip so they auto-surface when E1 lands.
- **Finding**: the aDNA-Native fixture is the single most load-bearing artifact — it exercises every `_reserved` sub-schema + the degradation contract in one document.
- **Change**: none.
- **Follow-up**: **E0 phase boundary — check in.** Then E1.1 (validate Core/Extended) against these fixtures.
