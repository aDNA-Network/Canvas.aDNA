---
type: doc
title: "Comic authoring contract — the ComicInput schema an author writes, and what the pipeline does with it"
created: 2026-08-09
updated: 2026-08-09
last_edited_by: agent_mondrian
status: active
audience: "comic spec AUTHORS (a human or agent writing in.yaml); first-light authors on the dev lane"
tags: [doc, comic, authoring, contract, comicinput, schema, print, dpi, halftone, h6, t3]
---

# Comic Authoring Contract

> **What this is.** The written contract for the **input** side of the comic pipeline: the YAML/JSON an author
> writes, field by field, and what each field causes downstream. Its sibling
> [`comic_prompt_contract.md`](comic_prompt_contract.md) faces render-side *consumers* (what the producer
> emits); this one faces *authors* (what you feed it).
>
> **Scope is contract-only**, by the operator's 2026-07-07 lock: schema + worked example + doctrine pointers.
> There is deliberately **no agentic story→spec skill** here — turning a story into a spec is a later wave.
>
> Authority: [`adr_008_comic_render_doctrine.md`](../decisions/adr_008_comic_render_doctrine.md). Normative
> code: `what/production/comic_generator/src/comic_generator/model.py` (`ComicInput` L176; `from_dict` L287;
> `load_comic` L402). Worked example:
> `what/production/comic_generator/examples/science_stanley_mini_issue.yaml`. **The code is the schema** — where
> this doc and `model.py` disagree, `model.py` wins and this doc is the bug.

## 1. The shape

```yaml
title: "Science Stanley — Mini Issue"   # required
id: science_stanley_mini                # required — becomes comic_id everywhere downstream
version: "0.1.0"                        # required
art_style: ghibli                       # comic-wide default style prefix
negative_suffix: ""                     # Layer-6 override; empty → the engine default

characters: [...]      # the character bible
spreads:    [...]      # optional structural overlay
color_script: [...]    # per-spread lighting
story_state:  [...]    # per-spread character presence/mood
refs:         [...]    # declarative wikilinks to context objects
pages:        [...]    # required, ≥1
```

`load_comic()` accepts `.yaml`/`.yml`/`.json`. An **empty overlay set still builds** — the engine falls back to
mechanism defaults, so a minimal comic is `title` + `id` + `version` + one page with one panel.

## 2. Pages and panels

```yaml
pages:
  - number: 1                # 1-based, required
    layout_type: splash      # grid | splash | spread   (default: grid)
    spread_number: 1         # keys color_script + story_state
    art_style: ""            # per-page override of the comic default
    panels:
      - panel_type: splash   # establishing | dialogue | action | close_up | splash | transition
        scene: "Stanley steps off the lighthouse stair into the fog."
        characters: [Stanley]        # matched case-insensitively against the bible
        image_path: ""               # see §3
        aspect_ratio: ""             # see §5
        row: 0
        col: 0
        span_rows: 3                 # a full-page panel spans the whole grid
        span_cols: 2
        bleed: true                  # full-bleed intent → promotes at compose
        # optional prompt overrides
        camera_angle: ""
        mood: ""
        balloon_space: ""
        style_override: ""
        compositional_nuance: ""
        compositional_intent: ""
        spatial_layout: ""           # a comic_panel_layout Mermaid string
```

**Validation you will actually hit** (all raise at load unless noted):

| Rule | Where |
|---|---|
| `panel_type` must be one of the six | `Panel.__post_init__` |
| `layout_type` must be `grid`/`splash`/`spread` | `Page.__post_init__` |
| a page must have ≥1 panel; a comic must have ≥1 page | `Page`/`ComicInput.__post_init__` |
| `layout_type: splash` with >1 panel **warns**, does not fail | `Page.__post_init__` — legal but almost always an authoring mistake |
| a missing `image_path` **warns** at `load_comic`; `--strict-paths` makes it fatal | `validate_image_paths` L382 |

## 3. `image_path` — the one field that changes the node type

- **empty** → the panel becomes a `text` placeholder carrying the scene excerpt, `qualities.status: prompt_only`.
  This is the normal authoring state: you are writing a spec, not supplying art.
- **set** → the panel becomes a baseline `file` node, `qualities.status: rendered`.

Relative paths resolve against the **input file's directory**. A path that does not exist still produces a valid
canvas with a dangling `file` reference — deliberately, so a spec stays buildable while art is in flight.

## 4. Characters — the bible, and the asset channel

```yaml
characters:
  - name: Stanley
    descriptor: "wiry, mid-40s, salt-stained canvas coat, perpetual squint"
    trigger_word: null          # PAIR-GATED with lora_ref — see below
    lora_ref: null
    reference_images:
      - "ScienceStanley.aDNA/what/visual_dna/characters/stanley/refs/portrait_01.png"
```

`descriptor` is **prompt text** (the Layer-2 character block). The three asset fields are **not** prompt text —
they ride into `qualities.characters`, the structured channel the render bridge lifts into its manifest.

**The pair gate (Halftone H5, and it is load-bearing):** `trigger_word` and `lora_ref` travel **as a pair or not
at all**. A trigger token with no trained weight behind it is inert at best and actively harmful at worst — it
spends prompt attention on a word the model has never seen. `compose_input.select_lora` enforces this; you cannot
author your way around it.

**LoRA-less is a first-class path**, not a degraded one. Set `lora_refs: []` and supply `reference_images` only —
this is the required path for any character whose likeness rights are held rather than owned, and it is exercised
and tested (`test_lora_less_compose_reference_images_only`). Reference paths are **workspace-root-relative**
(`<Vault>.aDNA/…`).

Auto-compose from a VisualDNA bundle is available instead of hand-authoring this block:
`comic-generator compose --bundle <bundle.yaml>` (see `compose_input.py`).

## 5. Aspect ratio, geometry, and DPI — what print will do to you

`aspect_ratio` accepts a named key: `standard` (1:1) · `tall` (3:4) · `wide` (16:9) · `full_page` (3:4) ·
`splash` (9:16) · `spread` (4:3) — `style.ASPECT_RATIOS`.

**Know this before you author a splash:** the declared ratio and the panel's *authored geometry* are two
different things, and when they disagree the geometry wins at compose time. A panel declared `tall` (3:4) but
authored at 663×1025 is really 0.647 — a ~14% crop. `CV-IMAGE-ASPECT-RATIO-01` catches it; H3's
geometry-derived aspect ruling makes the pipeline snap requests to the true geometry instead.

**DPI policy** (`canvas_core/print.py`):

| | |
|---|---|
| Target | **300 DPI** — every page composites and saves at 300 |
| Floor | **200 DPI** effective (`source_px / target_px × 300`) |
| Below the floor | **warn, never block** |
| Spreads | measured against the **combined two-page** target |

Warn-never-block is deliberate: a 2048px cloud generation on a full-bleed page lands at ~195 effective DPI, and
that is a perfectly reasonable proof page. The same source measures 195 across one page and **112** across a
spread — so a spread needs roughly twice the source resolution to hold the same quality. If you author a
two-page spread, ask for the biggest generation you can, or plan on the refine chain's upscale.

**Colour:** compose defaults to RGB. `--cmyk` produces a colour-managed ICC separation and **refuses** if the
profiles are absent rather than silently approximating (`--on-missing-profile rgb` to degrade with the reason
recorded). There is no silent soft-convert.

## 6. Spreads, colour script, story state

```yaml
spreads:
  - { number: 1, pages: [1, 2] }

color_script:
  - { spread: 1, dominant: "#1b3a5c", accent: "#e8b04b", lighting: "low fog-diffused", mood: "held breath", act: "I" }

story_state:
  - spread: 1
    world: "the fog has not lifted in nine days"
    characters:
      stanley: { present: true, mood: "wary", pose: "one hand on the rail" }
```

`color_script` is the Layer-5 lighting source; `story_state` merges a mood/pose suffix onto the character's
descriptor for that spread. Both key on **spread number**, so a page only receives them if it declares
`spread_number`.

A `spreads:` entry is a structural grouping. A **two-page spread panel** — one image crossing the gutter — is
authored as a panel wider than a single page; compose splits it at centre into two printed pages (H6). Page
count is unchanged: a spread is still two pages on press.

## 7. Building

```bash
# spec → canvas  (input and output are POSITIONAL, in that order)
comic-generator build in.yaml issue.canvas
comic-generator build in.yaml issue.canvas --strict-paths     # missing image_path is fatal

# with VisualDNA auto-compose (repeatable; NAME= binds a bundle to one character)
comic-generator build --bundle bearly.yaml in.yaml issue.canvas
comic-generator compose --bundle bearly.yaml in.yaml enriched.yaml \
    --ref-category portraits --ref-category series_panels

# canvas → rendered, composited pages
comic-render run issue.canvas --until compose
```

*(Bearly's invocation of record is the two `--ref-category` flags above: the default categories reach only 1
reference on their bundle, those two reach 12.)*

Then the three checks, none of which substitutes for another
([`canvas_authoring_guidance.md`](canvas_authoring_guidance.md)):

1. `canvas-std validate issue.canvas` — schema
2. `python -m canvas_core.traps.cli issue.canvas --profile comic` — geometry (**use `--profile comic`**; the
   default knowledge-canvas profile fails every conformant comic page by design)
3. **Look at it.** Open the render and read the image. The H4 live run passed every automated assertion on a
   picture of nothing; the H6 spread split passed every assertion on two flat green rectangles. Assertions
   cannot see.

## 8. Forward contract

What an author writes here becomes: `qualities.image_prompt` + `prompt_layers` (→
[`comic_prompt_contract.md`](comic_prompt_contract.md)) · `qualities.characters` (→ the render manifest's asset
channel) · panel geometry (→ the print placement) · `status` (→ what the render bridge will dispatch).

**Not covered here, by design:** how prompts are assembled from these fields (prompt contract §2), what the
render chain does (`comic_render/README.md`), and how a story becomes a spec (a later wave — T3 is contract-only).
