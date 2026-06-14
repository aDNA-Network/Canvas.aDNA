# Changelog — adna-canvas-std

All notable changes to the reference implementation. The package version is distinct from the Standard version
it implements (`STANDARD_VERSION`).

## [Unreleased]
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
