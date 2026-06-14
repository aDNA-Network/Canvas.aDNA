# Changelog — adna-canvas-std

All notable changes to the reference implementation. The package version is distinct from the Standard version
it implements (`STANDARD_VERSION`).

## [Unreleased]
### Added (E1.5 — strip + degradation; Phase E1 complete)
- `validate.py`: `strip(doc)` (deep-copy, removes `metadata.frontmatter._reserved` — the C4 op; original
  untouched) + `degradation_report(doc)` (D-1 Core-valid · D-2 Extended-valid · D-3 no `_reserved`). Exported.
- `test_fixtures.py`: retired the `validate`/`strip` `xfail` markers (behavior now real). `__init__.py` reordered
  (re-exports before constants) for ruff. **Full suite: `pytest` 30 passed / 4 skipped; `ruff` clean.**
- **Phase E1 (reference engine) complete.** Remaining stubs: `validate_suite` (E2.1), `canvas-std` CLI (E2.3).

### Added (E1.4 — _reserved validators / A-* checks)
- `reserved.py`: `validate_reserved(reserved, doc)` (A-2 adna_version/conformance_level, A-6 sync/16-hex hash) +
  `validate_component_types` (§7: keys resolve, class ∈ 14-class taxonomy, degrades_to ∈ baseline),
  `validate_panel_link` (§6: kinds/ids resolve, enums, exactly-one-canonical-surface, sequence acyclicity),
  `_validate_semantic_bindings` / `_validate_context_object`. Constants: `COMPONENT_CLASSES`, `PL_*`.
- `validate()` aDNA-Native branch wired to `validate_reserved` (requires a populated `_reserved`). The
  `adna_native` validate-xfail in `test_fixtures.py` now PASSES.

### Added (E1.3 — diff / merge / preserve_positions)
- `roundtrip.py`: `diff(a, b)` (structured topology/position diff), `preserve_positions(target, reference)` (G1),
  `merge(source, canvas, strategy)` (three-way: canvas owns topology + positions, source owns semantics;
  `yaml_wins`/`canvas_wins`; conflicts flagged as records, not exceptions). `preserve_positions` exported.
- `test_smoke.py`: `diff`/`merge` removed from the stub list (only `strip` remains) + a diff liveness check.

### Added (E1.2 — round-trip converters)
- `roundtrip.py`: `compute_sync_hash` (16-hex SHA-256 over sorted node ids + `fromNode->toNode` pairs),
  `to_canvas` (forward source->view: applies the `lattice` profile, explicit `toEnd`, injects `_reserved.sync`;
  default geometry — layout is producer-side), `from_canvas` (advisory view->source draft; topology + best-effort
  semantic-type recovery; `_draft: true`). `diff`/`merge` remain stubbed (E1.3).
- `test_smoke.py`: `to_canvas`/`from_canvas`/`compute_sync_hash` removed from the stub list + a round-trip liveness test.

### Added (E1.1 — validate Core/Extended)
- `validate.py`: implemented `validate(doc, level)` Core (C-1..C-5) + Extended (E-1..E-4) checks against the
  KEEP floor; monotone (aDNA-Native ⊃ Extended ⊃ Core). C-4 = explicit `toEnd` required (omitted → reject).
  aDNA-Native delegates A-* to `reserved.validate_reserved` (NotImplementedError until E1.4). `strip` stays E1.5.
- `test_smoke.py`: `validate` removed from the NotImplemented-stub list + a liveness check added. The core /
  extended / negative `validate` xfails in `test_fixtures.py` now PASS.

### Added (E0.3 — golden fixtures + harness)
- `tests/fixtures/`: `core_minimal.canvas`, `extended_styled.canvas`, `adna_native.canvas` (populated `_reserved`
  + `_lattice_meta`; doubles as the degradation case), `invalid_missing_arrow.canvas` (negative), `manifest.json`.
- `tests/test_fixtures.py`: now-checkable assertions (JSON shape, required fields, declared level) + `validate`/
  `strip` assertions marked `xfail(strict=False)` until E1 (they auto-flip to PASS when E1 lands). **Phase E0 complete.**

### Added (E0.2 — verbatim KEEP floor)
- `schema.py`: the 10 `VALID_*` enums, `NODE_REQUIRED_FIELDS`/`EDGE_REQUIRED_FIELDS`, and the built-in `lattice`
  semantic profile (`TYPE_MAPPING` 8 entries + `EDGE_TYPE_MAPPING` 5 entries) — transcribed verbatim from
  `p1_fork_baseline` §3. `SEMANTIC_PROFILES`/`EDGE_PROFILES` registries (new profiles register additively).
- Smoke test: floor-loaded assertion + lattice-profile spot-checks + token-within-§6-enum degradation-safety check.

## [0.1.0] — 2026-06-13 (Operation Keystone E0.1)
### Added
- Package skeleton: `pyproject.toml` (hatchling, Python ≥3.11, src-layout), MIT `LICENSE`, `Makefile` (test/lint).
- Public API stubs matching the ratified specs: `schema`, `validate`, `roundtrip`, `reserved`, `conformance`.
- `STANDARD_VERSION = "2.0.0"`; `to_canvas`/`from_canvas` aliases baked in.
- Smoke test asserting the API surface + Standard version.

### Notes
- Behavior is not implemented (stubs raise `NotImplementedError`). E0.2 ports the KEEP floor; E1 implements.
