---
plan_id: mission_e2_3_publish
type: plan
title: "E2.3 — Publish the v2.0.0 JSON Schema + the canvas-std CLI (closes E2)"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 2
campaign_mission_number: 11
mission_class: implementation
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, execution, e2, canvas_std, publish, cli, schema]
---

# Mission: E2.3 — Publish (JSON Schema + CLI)

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|campaign_canvas_genesis]] (Operation Keystone) · **Phase**: E2 (final mission) · **Mission**: E2.3

> Publishes the v2.0.0 JSON Schema + the `canvas-std` CLI. Closes Phase E2 — the reference impl + tooling is
> complete (no stubs remain). **Held at the E2→E3 boundary** (before the operator-gated CanvasForge migration).

## Objectives
- **v2.0.0 JSON Schema** — completed. `src/canvas_std/data/adna_canvas_v2.schema.json` (draft 2020-12): the
  structural node/edge floor + enums + the `_reserved` carrier. `json_schema()` loads it (importlib.resources).
- **`canvas-std` CLI** — completed. `_cli` in `conformance.py`: `validate <file> [--level …] [--json]`
  (auto-detects level from `_reserved.conformance_level`; exit 0 ok / 1 fail) + `schema` (prints the schema).
  Wired via pyproject `[project.scripts]`.
- **Register v2.0.0** — the JSON Schema is the published artifact; registry/federation registration is an **E5
  rollout** step (deferred), noted here.

## Notes
- The JSON Schema is the *structural* contract; semantic checks (C-4, id resolution, sequence-acyclicity,
  exactly-one-canonical-surface) stay in the validator — JSON Schema can't express them. The schema notes this.
- Verified: `canvas-std validate adna_native.canvas` → OK (exit 0); negative → C-4 FAIL (exit 1); `schema` prints.
  `pytest` 46 passed / 8 skipped; `ruff` clean.

## AAR
- **Worked**: shipping the schema as package data + an importlib.resources loader makes `canvas-std schema` work in both editable + wheel installs; the CLI is a thin wrapper over `validate_suite`.
- **Didn't**: full registry registration deferred to E5 (federation rollout) — it's a cross-vault step, not a local publish.
- **Finding**: auto-detecting the conformance level from `_reserved.conformance_level` makes the CLI ergonomic (no `--level` needed for aDNA-Native docs).
- **Follow-up**: **E2→E3 phase boundary — HOLD for the operator.** E3 is the parity-gated CanvasForge migration (human gate).
