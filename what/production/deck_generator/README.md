# deck-generator — reference deck consumer (Keystone E4.4)

The **second net-new consumer** of the **aDNA Canvas Standard v2.0.0**, and the worked build of the parked
deck-generator pilot. It turns a structured **deck spec** (slides) into a v2.0.0-conformant **deck `.canvas`** where
**each slide is a group node** — proven **end-to-end on `canvas_std` alone**: aDNA-Native conformance, round-trip
stability, degradation to a valid baseline Obsidian canvas, and faithful **image / table** components.

## What it extends over the brief consumer

`brief_consumer` (E4.3) proved the single-page pattern. The deck generator extends it to:
- **Multiple regions** — each slide is a `panel_link.region`; the **deck is the single canonical surface**
  (A-5: exactly one `role: canonical`).
- **`sequence` edges** — slides are chained by a `sequence` panel-link (acyclicity is validated), plus
  `reading_order` within each slide.
- **`isStartNode`** on the first slide (the Extended layer; a KEEP from Advanced Canvas).
- **`image` + `table` component classes** — image → a `file`/`link` node (`degrades_to`), table → a `text` node
  (markdown). The brief consumer exercised neither.

> **canvas_std is a validator + round-tripper, not a renderer.** "End-to-end" = a conformant, round-trippable,
> degradable deck **object**. The render-to-PDF/PNG loop + the 24-criterion scoring **engine** are the absorbed
> `canvas_presentation`'s job — **PT-P5-gated** — and the persona-III + accuracy gates are captured here as a
> *contract* (`iii_quality_contract.md`), with the engine staying in III (C6/C8).

## Use

```bash
deck-generator build examples/canvas_standard_deck.yaml examples/canvas_standard_deck.canvas
canvas-std validate examples/canvas_standard_deck.canvas        # -> level_reached=adna_native [OK]
```

```python
from deck_generator import build_deck, load_deck
doc = build_deck(load_deck("examples/canvas_standard_deck.yaml"))   # -> a v2.0.0 aDNA-Native deck .canvas dict
```

## Layout

```
src/deck_generator/
  model.py     # DeckInput / Slide + load_deck — substrate-free domain model
  slides.py    # slide-type -> interior nodes (title/content/section/image/table/quote)
  layout.py    # deterministic slide-row geometry (integers; 16:9 slides)
  consume.py   # DeckInput -> canvas_std source contract -> to_canvas -> enrich _reserved to aDNA-Native
  __main__.py  # deck-generator CLI
examples/      # a self-referential deck ABOUT the Standard + the generated .canvas
iii_quality_contract.md   # persona-III + accuracy gates as iii/-wrapper contracts (engine in III; render P5-gated)
tests/         # conformance · round-trip · degradation · components (image/table)
```

## Develop / test

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ../../code/canvas_std        # the Standard (zero-dep) first
pip install -e ".[dev]"
python -m pytest -q && ruff check .
```

Governed by the aDNA Canvas Standard (LIP process, `adr_003`); sited per `adr_004_production_code_layout`.
Slide-model lineage (KEEP reference, not a dependency): `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_presentation/`.
