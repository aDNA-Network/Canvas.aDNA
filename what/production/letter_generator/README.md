# letter_generator

A net-new in-vault producer of the **aDNA Canvas Standard** (Operation Palette, P2). Turns a one-page **letter** spec
into a v2.0.0 **aDNA-Native** `.canvas` that degrades to a valid Obsidian canvas. Built on the `canvas_std` reference
implementation; the Standard is never modified (ADR-004 two-shelf firewall). Built by following
`how/skills/skill_canvas_producer_build.md` — the first producer off the `_scaffold` factory.

## What it produces

A single canonical surface (`letter_root` group) holding a top-to-bottom column of baseline `text` blocks —
letterhead, date, recipient, salutation, one node per body paragraph, closing, signature — chained with
`reading_order` panel-link edges. One paged region (`flow: vertical`, `pagination: paged`, `extent: {unit: pages,
max: 1}`), `semantic_bindings.profile = "document"`. Rich block roles ride in
`_reserved.component_types[*].semantic_type` (free-form) with `class: "text"` and `degrades_to: "text"`, so stripping
`_reserved` yields a plain, valid Obsidian canvas. (Shape adopted from `spec_federation_contract §6.3`.)

## Usage

```sh
python3 -m venv .venv
.venv/bin/pip install -e ../../code/canvas_std && .venv/bin/pip install pyyaml
PYTHONPATH=src .venv/bin/python -m letter_generator build examples/example_letter.yaml out.canvas
.venv/bin/canvas-std validate out.canvas      # -> adna_native [OK]
```

Input is a YAML/JSON mapping: `title`, `id`, optional `version`, `sender` (list), `date`, `recipient` (list),
`salutation`, `body` (list of paragraphs), `closing`, `signature` (list), `refs` (list). Empty blocks are dropped.
See `examples/example_letter.yaml`.

## Develop / test

```sh
.venv/bin/pip install pytest ruff
PYTHONPATH=src .venv/bin/python -m pytest tests -q
.venv/bin/ruff check src tests
git diff --stat -- ../../code/canvas_std/    # MUST be empty (firewall)
```

## Layout

- `src/letter_generator/model.py` — substrate-free `Letter` + `load_letter` (imports no `canvas_std`).
- `src/letter_generator/consume.py` — `build_letter(Letter) -> .canvas` dict (the 4-step contract).
- `src/letter_generator/layout.py` — deterministic vertical-stack geometry.
- `src/letter_generator/__main__.py` — the `letter-generator build` CLI.
- `tests/` — the "four+1" suite (conformance · round-trip · degradation · components · `test_letter` coverage +
  model-neutrality).
- `iii_quality_contract.md` — the review/accuracy contract (a contract, not an engine; wired via the `iii/` wrapper).

## Doctrine
Never edit `canvas_std` (firewall). Profile stays producer-side. The producer emits a conformant object + metadata; it
does not render or score itself (quality → III; pixels → ComfyUI). Pattern: `what/context/context_canvas_producer_pattern.md`.
