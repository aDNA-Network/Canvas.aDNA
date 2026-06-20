---
plan_id: mission_e4_3_net_new_consumer
type: plan
title: "E4.3 — Net-new consumer end-to-end (the brief consumer) on canvas_std"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 4
campaign_mission_number: 3
mission_class: build
created: 2026-06-19
updated: 2026-06-19
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, e4, consumer, build, canvas_std, production]
---

> **STATUS: completed 2026-06-19** (session `session_stanley_20260619_170825_keystone_e4_open_consumer`).
> First build under the operator-authorized E3→E4 gate crossing — `brief_consumer` built + green. See Completion
> Summary + AAR below.

# Mission: E4.3 — Net-new consumer end-to-end (the "brief" consumer)

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]]
**Phase**: 4 — net-new consumer + LF-successor (in-vault, pt09-reshaped)
**Mission**: E4.3 (first build of the phase)

## Goal

Build the **first net-new consumer** of the aDNA Canvas Standard v2.0.0: a runnable **reference "brief" consumer**
that maps a structured one-page technical brief (sections → headings/body/sources) into a **v2.0.0-conformant
`.canvas`**, proven **end-to-end on `canvas_std` alone** — conformance at **aDNA-Native** (`validate` /
`validate_suite`), **round-trip** stability (`to_canvas`/`from_canvas` / `compute_sync_hash`), and **degradation**
to a valid baseline Obsidian canvas (`strip` → Core-valid). This makes the v2.0.0 Standard **load-bearing against a
real consumer** and directly de-risks the campaign's "net-new consumer reveals a spec gap" risk. **Zero PT-P5
dependency** (it imports `canvas_std`, not the absorbed `canvas_core`).

The consumer is a **producer**, not part of the lean Standard library, so it is sited on the **`what/production/`**
shelf (ADR-004's two-shelf split). It becomes the **first in-vault `what/production/` resident**, exercising the
**`adna-canvas-std` dependency contract** (ADR-004 §4) *before* the heavier P5 `canvas_core` relocation — de-risking P5.

## Exit Gate

- `what/production/brief_consumer/` exists: a packaged consumer (`pyproject.toml` depending on `adna-canvas-std`),
  `src/brief_consumer/` (`model` · `layout` · `consume` + public `build_brief`), a dog-food `examples/` input + a
  committed generated `.canvas`, and a `tests/` suite.
- **Conformance:** `validate(doc, ADNA_NATIVE) == []`; `validate_suite(doc, "adna_native").meets_declared` True;
  `level_reached == adna_native`.
- **Round-trip:** `compute_sync_hash(doc)` equals `_reserved.sync.sync_hash`, and is stable across
  `to_canvas(from_canvas(doc))` (topology preserved; positions are view-authority).
- **Degradation:** `strip(doc)` is **Core- and Extended-valid** (D-1/D-2) and carries no `_reserved` (D-3) — a valid
  baseline Obsidian canvas ("fork, don't drift").
- **Green:** `pytest` green + `ruff` clean in the package `.venv`; the `canvas-std validate` CLI passes on the
  generated artifact; **`canvas_std`'s own suite still 46/8** (the consumer is additive — imports `canvas_std`, never
  edits it).
- Committed with a `Keystone E4.3 —` message (push deferred per the operator batch convention).

## Objectives

### 1. Scaffold the `brief_consumer` package
- **Status**: completed
- **Description**: `what/production/brief_consumer/` — `pyproject.toml` (`dependencies = [adna-canvas-std, pyyaml]`;
  ruff+pytest dev extras; mirror `canvas_std`'s packaging), `README.md` + `AGENTS.md` (reference-consumer framing +
  the federation/standard-consumption note), `src/brief_consumer/{__init__,model,layout,consume}.py`.
- **Files**: `what/production/brief_consumer/**`
- **Depends on**: none

### 2. Implement the consumer (model · layout · consume)
- **Status**: completed
- **Description**: `model.BriefInput` (title/id/version/refs + sections[{heading, body, sources[]}]) + `load_brief`;
  `layout` (deterministic vertical-stack geometry — the producer-side x/y/w/h `to_canvas` leaves at defaults);
  `consume.build_brief(brief) -> dict`: assemble the `canvas_std` **source contract** (group page + heading/body
  text nodes + source link nodes; reading_order + adjacency edges) → `to_canvas` → **enrich `_reserved` to
  aDNA-Native** (adna_version, conformance_level, component_types, semantic_bindings, panel_link with exactly one
  canonical surface, context_object). A `brief-consumer` console entry generates the artifact.
- **Files**: `src/brief_consumer/{model,layout,consume,__init__}.py`, `__main__`/console script
- **Depends on**: 1

### 3. Author the dog-food input + generate the artifact
- **Status**: completed
- **Description**: `examples/canvas_standard_brief.yaml` — a real one-page brief **about the aDNA Canvas Standard**
  (self-referential; fully in-vault). Generate + commit `examples/canvas_standard_brief.canvas`.
- **Files**: `examples/canvas_standard_brief.yaml`, `examples/canvas_standard_brief.canvas`
- **Depends on**: 2

### 4. Test green + CLI cross-check + no-regression
- **Status**: completed
- **Description**: `tests/` — conformance (aDNA-Native), round-trip (sync-hash stable), degradation (strip→Core/
  Extended-valid). `pytest` green + `ruff` clean in a `.venv` (canvas_std + brief_consumer editable). `canvas-std
  validate examples/…canvas` exit 0. Re-confirm `canvas_std` suite 46/8.
- **Files**: `tests/test_conformance.py`, `tests/test_roundtrip.py`, `tests/test_degradation.py`
- **Depends on**: 3

### 5. Spec-gap probe → errata candidates
- **Status**: completed
- **Description**: record anything the brief domain could not express cleanly (multi-line body, figure, citation,
  table) as **v2.0.x errata candidates** (governed via the `adr_003` LIP process) — the campaign's stated intent, not
  a blocker. File in the mission Completion Summary / backlog.
- **Depends on**: 2-4

## Campaign Context

### Previous Mission Outputs
- E0–E2 delivered the complete `canvas_std` reference impl (`what/code/canvas_std/`): `to_canvas`/`from_canvas`,
  `validate`/`ConformanceLevel`, `validate_suite`/`ConformanceReport`, `strip`/`degradation_report`,
  `compute_sync_hash`, the v2.0.0 JSON Schema + the `canvas-std` CLI. This consumer is the first external caller of
  that public API.
- pt09 + ADR-004 sited Canvas production on `what/production/`; this consumer is its first resident.

### Next Mission Inputs
- E4.4 (deck-generator pilot) reuses this consumer's source-contract + layout + `_reserved`-enrichment pattern;
  its step-4 render loop is PT-P5-gated. E4.1/E4.2 (LF-successor, in-vault) are gated on the D3 governed touch.

## Notes

- **canvas_std is a validator + round-tripper, not a renderer** — "end-to-end" here = a conformant, round-trippable,
  degradable `.canvas` **object**; pixel rendering (PDF/PNG) is the absorbed `canvas_presentation` engine's job
  (PT-P5-gated). The consumer owns the genuine producer value: **input→source mapping (semantic typing)** + **layout**.
- **Doctrine:** substrate-neutrality (C8) — the consumer is producer code; `canvas_std` is untouched. The consumer
  depends on installed `adna-canvas-std` (ADR-004 §4), mirroring how `canvas_core` will resolve post-P5.
- **Coordination:** a new `what/production/` resident appears **before** the PT P5 `canvas_core` relocation into the
  same dir — courtesy heads-up to Hestia; no collision (new package, not one of the three relocating ones).

## Completion Summary

Completed 2026-06-19 in session `session_stanley_20260619_170825_keystone_e4_open_consumer`.

### Deliverables
- [x] `what/production/brief_consumer/` — packaged consumer (`pyproject.toml` → `dependencies = [adna-canvas-std,
  pyyaml]`; ruff+pytest), `README.md` + `AGENTS.md`, `.gitignore`. **First `what/production/` resident.**
- [x] `src/brief_consumer/` — `model.py` (`BriefInput`/`Section`/`Source` + `load_brief`), `layout.py` (deterministic
  integer vertical-stack geometry), `consume.py` (`build_brief`: source contract → `to_canvas` → `_reserved`
  enriched to aDNA-Native), `__main__.py` (`brief-consumer build` CLI), `__init__.py` (public API).
- [x] `examples/canvas_standard_brief.yaml` (self-referential one-pager about the Standard) + generated
  `examples/canvas_standard_brief.canvas` (14 nodes / 12 edges; deterministic on re-gen).
- [x] `tests/` — conformance (aDNA-Native), round-trip (sync-hash stable + all ids recovered), degradation
  (strip → Core+Extended-valid; D-1/D-2/D-3). **`pytest` 10/10, `ruff` clean** (package `.venv`).
- [x] **Independent CLI cross-check:** `canvas-std validate examples/canvas_standard_brief.canvas` →
  `declared=adna_native level_reached=adna_native [OK]`, degradation `{D-1,D-2,D-3}=True`, exit 0.
- [x] **No regression:** `canvas_std`'s own suite re-confirmed **46 passed / 8 skipped** (the consumer is additive —
  imports `canvas_std`, never edits it).

### Key findings
- **`to_canvas` injects only `_reserved.sync`** — reaching aDNA-Native is the *consumer's* job (enrich `adna_version`/
  `conformance_level`/`component_types`/`semantic_bindings`/`panel_link`/`context_object`). The genuine producer value
  is **input→source mapping + layout** (`to_canvas` emits default geometry by design).
- **The `adna-canvas-std` dependency contract (ADR-004 §4) works** — installing `canvas_std` editable *first*
  satisfies the consumer's `adna-canvas-std` requirement (no PyPI fetch). This de-risks the P5 `canvas_core` relocation.

### Spec-gap probe (objective 5)
- **No spec gap blocked the brief domain.** Headings (typography_run), body (text), citations (link + adjacency),
  a paged canonical region (panel_link) all expressed cleanly + degraded to a valid baseline canvas.
- **Latent note (not an errata):** rich components — `table`, `image` — exist in the component taxonomy but were not
  exercised by this consumer; their `degrades_to` baseline mapping is defined in the schema but untested *by a
  consumer*. Flagged for E4.4 / a future richer consumer to exercise (no v2.0.x change proposed now).

## AAR

- **Worked**: Reading the `canvas_std` internals (`schema`/`reserved`/`validate`/`roundtrip` + the `adna_native`
  golden fixture) *before* writing a line made the aDNA-Native `_reserved` shape unambiguous — the consumer validated
  green on the first full run (10/10), and the independent `canvas-std` CLI agreed. Building the consumer as a pure,
  deterministic function gave a reproducible committed artifact for free.
- **Didn't**: No renderer — "end-to-end" stops at a conformant, round-trippable, degradable `.canvas` *object* (pixel
  render is `canvas_presentation`, PT-P5-gated). The visual is intentionally plain (one color slot on headings); rich
  layout/styling is producer polish for later.
- **Finding**: The two-shelf split holds in practice — a producer with deps (`pyyaml`) sits cleanly on
  `what/production/` while `canvas_std` stays zero-dep on `what/code/`; the dependency resolves exactly as ADR-004 §4
  predicted. The consumer doubles as a live de-risk of the P5 relocation.
- **Change**: Site net-new consumers on `what/production/` (not in `canvas_std`) and depend on installed
  `adna-canvas-std` — established here as the pattern E4.4 / future consumers reuse.
- **Follow-up**: (1) ⛔ E4→E5 stays a human gate. (2) E4.1/E4.2 need the **D3 governed touch** before build.
  (3) E4.4 reuses this source-contract + `_reserved`-enrichment pattern; exercise `table`/`image` components there.
  (4) Courtesy heads-up to **Hestia**: a new `what/production/` resident exists ahead of the PT P5 `canvas_core`
  relocation (no collision).
