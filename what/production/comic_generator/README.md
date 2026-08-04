# comic-generator — reference comic consumer (Operation Atelier A2)

A net-new consumer of the **aDNA Canvas Standard v2.0.0**, and the worked port of CanvasForge's comic engine. It turns
a structured **comic spec** (ordered pages, each a 2D grid of panels) into a v2.0.0-conformant **multi-page `.canvas`**
where **each page is a group node carrying a panel grid** — proven **end-to-end on `canvas_std` alone**: aDNA-Native
conformance, round-trip stability, degradation to a valid baseline Obsidian canvas, and a faithful panel/image
component set. Structurally it is the `document_generator` (multi-page) with a **2D panel-grid interior**.

## The mapping (multi-page; panel-grid interior)

- **`comic_root`** is **one `group` node = the single canonical surface** (A-5: exactly one `role: canonical`;
  `class: panel`, `semantic_type: comic`).
- Each **spread** → a `group` (`semantic_type: spread`) carrying a `region` (`flow: horizontal`, `pagination: paged`,
  `extent: {unit: pages, max: 2}`) — a spread holds its 1–2 pages side by side.
- Each **page** → a `group` (`semantic_type: page`) carrying a `region` (`extent: {unit: pages, max: 1}`). **There is
  no `panels` extent unit** in the Standard — comics paginate in **`pages`** (per `spec_panel_link_semantics` §4).
- Each **panel** → a baseline node inside its page: a **`file`** node when an image is already rendered, else a
  **`text`** placeholder (`**Panel <type>**\n\n<scene excerpt>`). In `_reserved.component_types` every panel is
  `class: "image"`, `semantic_type: <panel_type>`, `degrades_to: "file"|"text"`, and its assembled **6-layer image
  PROMPT** rides in `qualities.image_prompt` (+ `dual_prompt`, optional `spatial_layout`, `aspect_ratio`, `status`).
- **Edges:** `sequence` over the pages (a linear, acyclic chain; `isStartNode` on page 1); `reading_order` within a
  page (the panel Z-path: top-to-bottom, left-to-right); `adjacency` for gutter-neighbour panels.

> **Image boundary (hard rule).** This producer **emits image PROMPTS as metadata only** — it renders no pixels,
> imports no ComfyUI, and does no image I/O. Already-rendered image *paths* are accepted as optional input; otherwise
> a panel carries its prompt and a `status: "prompt_only"`. Pixel render + per-panel scoring is **ComfyUI /
> `canvas_presentation` (PT-P5-gated)** — see `iii_quality_contract.md`.

> **Data-driven (ratified scope D5).** The engine carries only the canvas-agnostic **mechanism** (panel-type camera/
> composition templates, Wally-Wood keyword categories, act-lighting defaults, art-style prefixes). The **instance
> data** — a specific character bible, a per-spread color script, a per-spread story state — is supplied through
> `ComicInput`, **not baked into the engine** (the legacy CanvasForge engine hardcoded the Science-Stanley run; here it
> rides on the spec). An empty comic still builds on the mechanism defaults. The worked example uses the
> Science-Stanley characters *as example data*.

## Use

```bash
comic-generator build examples/science_stanley_mini_issue.yaml examples/science_stanley_mini_issue.canvas
canvas-std validate examples/science_stanley_mini_issue.canvas      # -> level_reached=adna_native [OK]
```

```python
from comic_generator import build_comic, load_comic
doc = build_comic(load_comic("examples/science_stanley_mini_issue.yaml"))  # -> a v2.0.0 aDNA-Native .canvas dict
```

### VisualDNA compose (Halftone H5)

```bash
# Enrich the spec with a character bundle's assets (file-shaped, inspectable), then build:
comic-generator compose in.yaml -o in.composed.yaml \
    --bundle ~/aDNA/ScienceStanley.aDNA/what/visual_dna/characters/stanley/stanley.yaml
comic-generator build in.composed.yaml out.canvas

# Or one-shot (explicit name=bundle binding; heuristic display_name/id matching otherwise):
comic-generator build in.yaml out.canvas --bundle stanley=…/stanley.yaml
```

Compose fills empty `descriptor`s from the bundle's text subsets (an authored descriptor always wins), selects
reference images **canonical-first** (default categories `portraits`/`expressions`/`scenes` + any canonical item
elsewhere; `--ref-category` to override — e.g. Bearly's `series_panels`; cap `--max-refs`, default 6), and emits
them workspace-root-relative (`<Vault>.aDNA/…`). The **LoRA pair-gate**: `trigger_word` + `lora_ref` are attached
together only when a bundle entry is `TRAINED`/`VALIDATED` — `PENDING_TRAINING`/rights-HELD bundles compose
**reference-images-only** (both live bundles today). Panels then carry `qualities.characters` (the structured
asset channel the render bridge lifts); the Layer-2 prompt text is unchanged. **Compose before `plan`** — the
render manifest's staleness guard is topology-keyed, so recomposing prompts/assets alone does not invalidate an
existing manifest (delete it or re-`plan` after compose).

## Layout

```
src/comic_generator/
  model.py        # ComicInput / Page / Panel / Spread + the instance overlays + load_comic — substrate-free model
  style.py        # PORTED data tables (panel-type templates / Wood keywords / act-lighting / styles) + lookups (mechanism)
  prompt.py       # PORTED 6-layer prompt assembly as PURE FUNCTIONS + the local ImagePrompt dataclass (no ContextPack gate)
  panel_layout.py # PORTED comic_panel_layout Mermaid parser/serializer + dual-prompt assembly (canvas_core ImagePrompt dropped)
  rlhf_hints.py   # PORTED RLHF hint loader — DORMANT by default (store path optional; no-ops without it)
  layout.py       # deterministic INTEGER print geometry (comic_root > spread > page > panel grid)
  panels.py       # panel -> interior baseline node (file/text) + its image component entry (prompt in qualities)
  consume.py      # ComicInput -> canvas_std source contract -> to_canvas -> enrich _reserved to aDNA-Native
  __main__.py     # comic-generator CLI
examples/         # a SHORT worked mini-issue (4 pages / 2 spreads) + the generated .canvas
iii_quality_contract.md   # visual-narrative/character/composition/rigor/accuracy lenses (engine in III; render P5-gated)
tests/            # conformance · round-trip · degradation · components · panel-coverage · prompt · panel-layout · neutrality
```

## Develop / test

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ../../code/canvas_std        # the Standard (zero-dep) first; provides adna-canvas-std + the canvas-std CLI
pip install -e ".[dev]"
python -m pytest -q && ruff check src tests
```

Governed by the aDNA Canvas Standard (LIP process, `adr_003`); sited per `adr_004_production_code_layout`; in-vault
per `adr_005_lf_successor_in_vault`. Comic-engine lineage (KEEP reference, **not** a dependency — ported FROM, never
imported): `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_comic/` (`comic.py`, `mermaid_layout.py`, `_rlhf_hints.py`).
The `profiles_used: [..., comic]` federation-wrapper addition is **CanvasForge-side** (the `canvas/` wrapper), not here.
