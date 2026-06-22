# AGENTS.md — comic_generator (Canvas.aDNA / what/production/)

**Scope:** the reference comic consumer built at Operation Atelier **A2** — a comic spec → a v2.0.0-conformant
multi-page comic `.canvas` (pages = group nodes carrying a 2D panel grid; panels carry image PROMPTS as metadata).
**Producer code** on the `what/production/` shelf, not the Standard. Structurally `document_generator` (multi-page)
with a panel-grid interior; the bulk is PORTED from the CanvasForge `canvas_comic` quarry.

## Load this when
- Working on the comic generator, or building another paginated/panel-grid consumer.

## Rules
- **Never edit `what/code/canvas_std/` from here** — import it (the installed `adna-canvas-std`), never modify it (C8).
- **NEVER render images.** The producer emits image PROMPTS as `_reserved.component_types[*].qualities.image_prompt`
  metadata ONLY — no ComfyUI import, no image I/O, no pixel generation anywhere in the package (enforced by
  `tests/test_model_neutrality.py::test_no_module_imports_an_image_render_engine`). Already-rendered image *paths* are
  accepted as optional input → a `file` node with `status: "rendered"`; otherwise a `text` placeholder with
  `status: "prompt_only"`.
- **Self-contained on `canvas_std`.** Do NOT import `canvas_core` or anything under `Archive.aDNA/`. The archived
  `canvas_comic` is a **KEEP-reference quarry** that was *ported* here (`model`/`style`/`prompt`/`panel_layout`/
  `rlhf_hints`); the `CanvasBuilder` / `ContextPack` / `canvas_core.ImagePrompt` couplings were dropped.
- **Data-driven (scope D5).** `style.py` carries the canvas-agnostic *mechanism* (templates, Wood keywords, act
  lighting, styles); the *instance data* (character bible, color script, story state, per-page art-style) rides on
  `ComicInput`, never as module constants. The Science-Stanley run is the worked EXAMPLE, not engine state.
- **The comic contract** (load-bearing): `comic_root` = the **single canonical surface** (A-5: exactly one
  `role: canonical`); one `region` per spread (`flow: horizontal`, `extent.unit: pages`, max 2) + per page
  (`extent.unit: pages`, max 1) + the comic_root region. **There is no `panels` extent unit** — comics paginate in
  `pages` (`PL_EXTENT_UNITS = {words, pages, slides}`).
- **Edge-kind mapping** (respect A-5 acyclicity — only `sequence` is checked): pages → `sequence` (linear, acyclic;
  `isStartNode` on page 0); within a page → `reading_order` (the panel Z-path); gutter neighbours → `adjacency`.
- **`image` components degrade to baseline.** `degrades_to` ∈ {text, file, group, link}; an `image` panel degrades to
  `file` (rendered) or `text` (prompt-only). The Mermaid spatial grammar / aspect / status ride ONLY in `qualities`.
- **`to_canvas` injects only `_reserved.sync`** — `consume.build_comic` enriches `_reserved` to aDNA-Native. Source
  nodes carry **no** `semantic_type` (so `to_canvas`'s `lattice` profile injects no color/shape onto baseline nodes).
- **Layout is producer-side** (`layout.py` integer print geometry; `panels.py` interior nodes). Deterministic + integer.

## Pointers
- Sibling pattern: `what/production/document_generator/` (pages = group nodes; the multi-page precedent) +
  `what/production/diagram_generator/` (the `_reserved` enrichment + venv recipe just before this one).
- Standard API: `what/code/canvas_std/src/canvas_std/` (`roundtrip.py` source contract; `reserved.py` A-* + `PL_*`).
- Quarry (ported, **not** imported): `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_comic/`.
- Quality contract: `iii_quality_contract.md`. The `profiles_used:[...,comic]` federation addition is CanvasForge-side.
