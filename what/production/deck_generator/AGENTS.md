# AGENTS.md — deck_generator (Canvas.aDNA / what/production/)

**Scope:** the reference deck consumer built at Operation Keystone **E4.4** — a deck spec → a v2.0.0-conformant deck
`.canvas` (slides = group nodes). **Producer code** on the `what/production/` shelf, not the Standard.

## Load this when
- Working on the deck generator, or building another multi-region (slides/pages) consumer.

## Rules
- **Never edit `what/code/canvas_std/` from here** — import it (the installed `adna-canvas-std`), never modify it
  (C8). The `canvas_presentation` engine in the CanvasForge archive is **KEEP-reference only** (P5-gated; do not import).
- **The deck contract** (load-bearing): `deck_root` group = the **single canonical surface** (A-5: exactly one
  `role: canonical`); each slide = a nested group declared as a `panel_link.region` (`extent.unit: "slides"`);
  slides chained by **`sequence`** edges (acyclic) + `reading_order` within slides.
- **The four+1 properties are the contract** (see `tests/`): conformance @ aDNA-Native, round-trip (`compute_sync_hash`
  stable; sequence acyclic), degradation (`strip` → Core/Extended-valid), **components** (image→file/link, table→text),
  and no-regression on `canvas_std` + `brief_consumer`.
- **`to_canvas` injects only `_reserved.sync`** — `consume.build_deck` enriches `_reserved` to aDNA-Native.
- **Layout is producer-side** (`layout.py` / `slides.py` own the integer geometry).

## Pointers
- Mission: `how/campaigns/campaign_canvas_genesis/missions/mission_e4_4_deck_pilot.md`.
- Sibling pattern: `what/production/brief_consumer/` (E4.3 — the single-page precedent).
- Standard API: `what/code/canvas_std/src/canvas_std/` (`roundtrip.py` source contract; `reserved.py` A-* + `PL_*`).
- Component model: `what/specs/spec_component_model.md`. Quality contract: `iii_quality_contract.md`.
