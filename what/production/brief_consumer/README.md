# brief-consumer — reference net-new consumer (Keystone E4.3)

The **first net-new consumer** of the **aDNA Canvas Standard v2.0.0**. It turns a structured one-page **technical
brief** (sections → headings / body / sources) into a v2.0.0-conformant **`.canvas`** — proven **end-to-end on
`canvas_std` alone**: conformance at **aDNA-Native**, **round-trip** stability, and **degradation** to a valid
baseline Obsidian canvas.

## Why it exists

It makes the v2.0.0 Standard **load-bearing against a real consumer** (Operation Keystone E4.3) and is the **first
resident of `what/production/`** — exercising the `adna-canvas-std` dependency contract (ADR-004 §4) *before* the
heavier PT-P5 `canvas_core` relocation lands in this same directory.

It is a **producer**, not part of the Standard: `canvas_std` (the lean, zero-dependency reference library) stays
untouched; this package *imports* it. That is the two-shelf split — `what/code/` (the Standard) vs `what/production/`
(producers / engines).

> **canvas_std is a validator + round-tripper, not a renderer.** "End-to-end" here means a conformant,
> round-trippable, degradable `.canvas` **object**. Pixel rendering (PDF/PNG) is the absorbed `canvas_presentation`
> engine's job (lands at PT P5). What this consumer genuinely owns: **input→source mapping** (semantic typing per the
> component model) and **layout** (the producer-side geometry `to_canvas` deliberately leaves at defaults).

## Use

```bash
# in a venv with adna-canvas-std + this package installed editable
brief-consumer build examples/canvas_standard_brief.yaml examples/canvas_standard_brief.canvas
canvas-std validate examples/canvas_standard_brief.canvas        # independent conformance check (exit 0)
```

```python
from brief_consumer import build_brief, load_brief
doc = build_brief(load_brief("examples/canvas_standard_brief.yaml"))   # -> a v2.0.0 aDNA-Native .canvas dict
```

## Layout

```
src/brief_consumer/
  model.py     # BriefInput / Section / Source + load_brief (yaml|json) — substrate-free domain model
  layout.py    # deterministic vertical-stack geometry (integers; the producer-side x/y/w/h)
  consume.py   # BriefInput -> canvas_std source contract -> to_canvas -> enrich _reserved to aDNA-Native
  __main__.py  # brief-consumer CLI
examples/      # a self-referential one-pager ABOUT the Standard + the generated .canvas
tests/         # conformance (aDNA-Native) · round-trip (sync-hash stable) · degradation (strip -> Core/Extended)
```

## Develop / test

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ../../code/canvas_std        # the Standard (zero-dep) first, so adna-canvas-std is satisfied
pip install -e ".[dev]"
python -m pytest -q && ruff check .
```

Governed by the aDNA Canvas Standard (LIP process, `adr_003`); sited per `adr_004_production_code_layout`.
