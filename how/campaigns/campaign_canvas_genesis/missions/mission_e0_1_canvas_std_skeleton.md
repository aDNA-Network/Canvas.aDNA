---
plan_id: mission_e0_1_canvas_std_skeleton
type: plan
title: "E0.1 — Stand up the canvas_std package skeleton"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 0
campaign_mission_number: 1
mission_class: implementation
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, execution, e0, canvas_std]
---

# Mission: E0.1 — `canvas_std` package skeleton

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|campaign_canvas_genesis]] (Operation Keystone)
**Phase**: E0 — Bootstrap `canvas_std`
**Mission**: E0.1 (first mission of the execution campaign)

> First build mission. Stands up the reference-implementation home at `what/code/canvas_std/` (Option P): layout,
> packaging, CI targets, license, and **stub modules declaring the API surface** — the actual logic is filled by
> E0.2 (port the KEEP floor) and E1 (implement). Resolves **E-D1** (language/runtime/packaging).

## Goal

A clean, installable, test-passing Python package skeleton whose public API matches the ratified spec set, so E0.2
and E1 fill in behavior against a fixed surface. No standard logic is implemented yet — stubs raise
`NotImplementedError` pointing at the owning E-phase.

## E-D1 resolved (language / runtime / packaging)
- **Python ≥ 3.11**, **src-layout**, PEP 621 `pyproject.toml` (hatchling backend). Rationale: the extracted
  source (`CanvasForge.canvas_core`) is Python; zero-friction extraction.
- Dev tooling: **pytest** (tests) + **ruff** (lint) wired via a `Makefile` (the local "CI"); a repo-level CI hook
  is wired at E2.3 (publish).
- License **MIT** (matches the FAIR convention). Package `adna-canvas-std`; import `canvas_std`. Package version
  starts `0.1.0`; the **Standard** version it implements is `STANDARD_VERSION = "2.0.0"` (distinct).

## Objectives

### 1. Package + packaging + license + CI targets
- **Status**: completed — `pyproject.toml`, `LICENSE` (MIT), `README.md`, `CHANGELOG.md`, `Makefile`, `AGENTS.md`.

### 2. API-surface stub modules
- **Status**: completed — `src/canvas_std/{__init__,schema,validate,roundtrip,reserved,conformance}.py`; signatures
  match the specs (`validate`/`strip`, `to_canvas`/`from_canvas`, `compute_sync_hash`/`diff`/`merge`, `_reserved`
  validators, conformance harness); bodies raise `NotImplementedError` with the owning E-phase.

### 3. Smoke test
- **Status**: completed — `tests/test_smoke.py`: imports the package, asserts `STANDARD_VERSION == "2.0.0"` and the
  public API exists; documents the NotImplemented contract.

## Notes
- The `to_canvas`/`from_canvas` aliasing (P1 finding) is baked into `roundtrip.py` from the start so the API
  vocabulary matches the conformance spec.
- E0.2 fills `schema.py` with the **verbatim KEEP floor** (the 10 `VALID_*` enums + node/edge schema +
  `TYPE_MAPPING`/`EDGE_TYPE_MAPPING`) from `p1_fork_baseline.md` §3.

## Completion Summary

### Deliverables
- A `pip install -e .`-able `adna-canvas-std` skeleton with a passing smoke test and the full public API stubbed.

## AAR

- **Worked**: the ratified specs gave an exact API surface to stub — E0.2/E1 now fill behavior against a frozen contract.
- **Didn't**: system Python 3.14 has no `pytest` — verified the smoke assertions via a direct `python3` run instead (5/5 stubs raise `NotImplementedError`; versions + levels + empty-floor asserted). Install `pytest` (`make install`) before E1 for the real test loop.
- **Finding**: pinning `STANDARD_VERSION` as a constant (distinct from the package version) prevents the
  spec-version / impl-version confusion flagged in P2.
- **Change**: none.
- **Follow-up**: E0.2 — port the verbatim KEEP floor into `schema.py`.
