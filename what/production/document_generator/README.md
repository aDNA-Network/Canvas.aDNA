# document-generator — reference long-form consumer (Keystone E4.1, the LF-successor)

The **third net-new consumer** of the **aDNA Canvas Standard v2.0.0**, and the in-vault successor to the wound-down
LiteratureForge. It turns a structured **document spec** (ordered pages of ordered sections) into a v2.0.0-conformant
**multi-page `.canvas`** where **each page is a group node** — proven **end-to-end on `canvas_std` alone**: aDNA-Native
conformance, round-trip stability, degradation to a valid baseline Obsidian canvas, and a faithful long-form
component set.

## What it extends over the brief + deck consumers

`brief_consumer` (E4.3) proved the single-page document; `deck_generator` (E4.4) proved the multi-region deck. The
document generator is the **long-form** profile:
- **`profile: long_document`** — distinct from the brief's single-page `document`.
- **Pagination** — a `doc_root` canonical surface enclosing per-page `panel_link.region`s (`pagination: paged`,
  `extent.unit: pages`); the document carries a `words` extent (the LF `length_window`). The pages are chained by a
  `sequence` panel-link; sections read by a `reading_order` chain; citations attach by `adjacency`.
- **The full document element set** — heading (`typography_run`), body/list (`text`), figure (`image` → `file`/`link`)
  + `caption`, `table`, **`code`** (the first consumer to exercise the `code` component class), and blockquote
  (`text`, `quote`). `isStartNode` marks page 1.

> **canvas_std is a validator + round-tripper, not a renderer.** "End-to-end" = a conformant, round-trippable,
> degradable document **object**. The genre/writing pipeline (trap-packs, reviewer voices, reward rubrics) and the
> visual/format contracts are **producer-side** and land in **E4.2** (the LF-contract migration) — never in the
> Standard. Pixel render + scoring is **PT-P5-gated** (the absorbed `canvas_presentation`); structural review is
> wired via the `iii/` wrapper (`iii_quality_contract.md`).

## Use

```bash
document-generator build examples/canvas_standard_whitepaper.yaml examples/canvas_standard_whitepaper.canvas
canvas-std validate examples/canvas_standard_whitepaper.canvas      # -> level_reached=adna_native [OK]
```

```python
from document_generator import build_document, load_document
doc = build_document(load_document("examples/canvas_standard_whitepaper.yaml"))  # -> a v2.0.0 aDNA-Native .canvas dict
```

## Layout

```
src/document_generator/
  model.py     # Document / Page / Section / Block / Source + load_document — substrate-free domain model
  blocks.py    # page builder: section + block -> interior nodes (heading/body/figure/caption/table/code/quote/list/citation)
  layout.py    # deterministic page-column geometry (integers; US-Letter pages stacked vertically)
  consume.py   # Document -> canvas_std source contract -> to_canvas -> enrich _reserved to aDNA-Native
  __main__.py  # document-generator CLI
examples/      # a self-referential whitepaper ABOUT the Standard + the generated .canvas
iii_quality_contract.md   # persona-III + accuracy gates as iii/-wrapper contracts (engine in III; render P5-gated)
tests/         # conformance · round-trip · degradation · components (code/figure/table/caption)
```

## Develop / test

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ../../code/canvas_std        # the Standard (zero-dep) first
pip install -e ".[dev]"
python -m pytest -q && ruff check .
```

Governed by the aDNA Canvas Standard (LIP process, `adr_003`); sited per `adr_004_production_code_layout`; in-vault
per `adr_005_lf_successor_in_vault`. LF quarry (KEEP reference, not a dependency, migrated in E4.2):
`Archive.aDNA/LiteratureForge.aDNA/what/specs/` (`spec_format_contract`, `spec_visual_contract`, `spec_genre_submodule`).
