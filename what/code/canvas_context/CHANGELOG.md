# Changelog — adna-canvas-context

All notable changes to the leg-2 reference context-loader.

## [0.1.0] — 2026-06-22

Initial implementation — Operation Salon P2 (leg-2 proof). Reference realization of
`spec_canvas_context_loading.md` (ratified 2026-06-22).

### Added
- `model.py` — the context-graph record shapes (spec §3): `ContextGraph`, `Component`, `Panel`, `Relation`, `Ref`,
  `Surface`, `Conformance`.
- `loader.py` — `load_context_graph()` implementing the normative **L1–L7** load pipeline (spec §4): parse & validate
  (refuse Core-invalid) → baseline graph → additive `_reserved` overlay → context identity → ref classification →
  advisory staleness → **no rendering**. Cycle-safe recursive resolution.
- `resolver.py` — the abstract `Resolver` contract (spec §5) + `DefaultPathResolver` for in-vault wikilinks;
  `federation_ref` returns a descriptor (transport deferred).
- `traversal.py` — the reading-order walk (kind ∈ {reading_order, sequence} from `isStartNode`; geometry fallback)
  behind the §6 read-only traversal primitives.
- `tests/` — `test_loader.py`, `test_traversal.py`, and `test_pilot.py` (the leg-2 proof: loads
  `document_generator/examples/canvas_standard_whitepaper.canvas` as a context graph without rendering).

### Notes
- Read-only consumer of `canvas_std`'s public API (D6 firewall — `canvas_std` untouched).
- Bounded by ADR-006: a contract realization + reference loader, never a runtime/transport/router.
