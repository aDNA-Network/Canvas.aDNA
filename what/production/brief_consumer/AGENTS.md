# AGENTS.md — brief_consumer (Canvas.aDNA / what/production/)

**Scope:** the reference net-new consumer built at Operation Keystone **E4.3** — a structured brief → a
v2.0.0-conformant `.canvas`. This is **producer code** on the `what/production/` shelf, not the Standard.

## Load this when
- Working on the brief consumer, or building another net-new consumer (use this as the pattern).
- Touching the `what/production/` shelf.

## Rules
- **Never edit `what/code/canvas_std/` from here.** The consumer *imports* `canvas_std` (the Standard's lean,
  zero-dependency reference library) and must never modify it (substrate-neutrality / C8). Depend on installed
  `adna-canvas-std` (ADR-004 §4).
- **The four properties are the contract** (see `tests/`): conformance @ aDNA-Native, round-trip (`compute_sync_hash`
  stable), degradation (`strip` → Core/Extended-valid), no-regression on `canvas_std`'s own suite.
- **`to_canvas` only injects `_reserved.sync`.** The consumer enriches `_reserved` to aDNA-Native
  (`adna_version`, `conformance_level`, `component_types`, `semantic_bindings`, `panel_link` — exactly one canonical
  surface, `context_object`). See `consume.build_brief`.
- **Layout is producer-side.** `to_canvas` emits default geometry; `layout.py` owns the real (integer) coordinates.

## Pointers
- The mission: `how/campaigns/campaign_canvas_genesis/missions/mission_e4_3_net_new_consumer.md`.
- The Standard API: `what/code/canvas_std/src/canvas_std/__init__.py` (+ `roundtrip.py` source contract; `reserved.py`
  A-* checks).
- Siting decision: `what/decisions/adr_004_production_code_layout.md`. Shelf marker: `what/production/README.md`.
