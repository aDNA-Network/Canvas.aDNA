---
type: doc
title: "Comic prompt contract — the 6-layer assembly, prompt_layers channels, and dual-prompt wrapper"
created: 2026-07-09
updated: 2026-07-09
last_edited_by: agent_mondrian
status: active
audience: "render-side consumers (ComfyUI.aDNA / Vulcan; the comic_render bridge; any external renderer)"
tags: [doc, comic, prompt, contract, dual-prompt, prompt-layers, negative, render, halftone]
---

# Comic Prompt Contract

> **What this is.** The written contract for the image directives the comic producer emits — precise enough for a
> render-side consumer (a ComfyUI workflow author, the `comic_render` bridge, a cloud adapter) to build against
> without reading producer source. Authority: [`adr_008_comic_render_doctrine.md`](../decisions/adr_008_comic_render_doctrine.md)
> (which adopts the CanvasForge dual-prompt + prompt-construction decisions). Emitting code:
> `what/production/comic_generator/src/comic_generator/{prompt,panel_layout,panels}.py`.
> The producer emits **prompt TEXT only** — it never renders; pixels belong to the render chain.

## 1. Where prompts live in a `.canvas`

Every comic panel is a baseline node whose component entry carries the directives:

```
metadata.frontmatter._reserved.component_types[<panel_node_id>] = {
  "class": "image",
  "semantic_type": "<panel_type>",          # establishing | dialogue | action | close_up | splash | transition
  "degrades_to": "text" | "file",
  "qualities": {
    "substrate": "raster",
    "aspect_ratio": "1:1" | "3:4" | "16:9" | "9:16" | "4:3",
    "image_prompt": "<assembled 6-layer single-prompt text>",
    "prompt_layers": { ... },               # §3 — the structured per-channel breakdown
    "dual_prompt": "<PART 1/2[/3] wrapped form>",   # §4
    "spatial_layout": "<mermaid comic_panel_layout>",   # present iff the panel declared one
    "compositional_intent": "<free text>",              # present iff declared (PART 3 anchor)
    "panel_type": "<panel_type>",
    "status": "prompt_only" | "rendered"
  }
}
```

A renderer consumes `prompt_only` panels; a `rendered` panel already has a baseline `file` node pointing at its
image. (The `comic_render` manifest — Halftone H2 — extracts exactly these fields per panel.)

## 2. The 6-layer assembly (`image_prompt`)

The single-prompt text is the non-empty layers, **in this order, joined by blank lines**:

| # | Layer | Source | Notes |
|---|-------|--------|-------|
| 1 | `style` | panel `style_override` > page `art_style` > comic `art_style`, via `STYLE_PREFIXES` | e.g. Ghibli / pixel / transition prefix paragraphs |
| 2 | `characters` | character bible descriptor per named character + story-state mood/pose merge (+ optional RLHF hint parenthetical) | empty when the panel names no characters |
| 3 | `scene` | the panel's free-text `scene` | the author's beat |
| 4 | `camera` | panel-type template camera (or explicit `camera_angle`) + Wally-Wood keywords + balloon-space clause + optional `(compositional nuance: …)` (+ optional RLHF hint) | template keyed by `panel_type` |
| 5 | `lighting` | spread color-script (`<lighting> lighting, dominant <hex>` + mood) > act default (`ACT_LIGHTING`) > `"ambient lighting"` | never empty |
| 6 | `negative` | `ComicInput.negative_suffix` override, else the engine default (`style.NEGATIVE_SUFFIX` — no photorealism, no legible real text, …) | see §3 for the separate channel |

Invariant: `image_prompt == "\n\n".join(v for v in prompt_layers.values() if v)` — the assembled form and the
structured form never disagree.

## 3. `prompt_layers` — the per-channel contract *(Halftone H1)*

```json
"prompt_layers": {
  "style":      "<layer 1 text>",
  "characters": "<layer 2 text or ''>",
  "scene":      "<layer 3 text or ''>",
  "camera":     "<layer 4 text or ''>",
  "lighting":   "<layer 5 text>",
  "negative":   "<layer 6 text>"
}
```

- Keys are fixed, in canonical order; an absent layer is an **empty string**, never a missing key.
- **The `negative` channel is the load-bearing one for render backends with a distinct negative input**
  (ComfyUI's negative CLIP encode): feed `negative` there and compose the positive from the other five channels
  (`"\n\n".join` of the non-empty non-negative layers) — do NOT string-strip the assembled `image_prompt`.
  Single-prompt backends (Imagen/Gemini) use `image_prompt` (or `dual_prompt`) as-is: the negative is phrased as
  in-prompt exclusions by design.
- The negative is **instance data**: `ComicInput.negative_suffix` overrides the default wholesale (an empty
  override field means "use the engine default"), so e.g. a photorealistic register supplies its own negative.

## 4. The dual-prompt wrapper (`dual_prompt`)

When present, `dual_prompt` is the segmented form for spatially-guided generation:

```
<wrapper preamble — instructs the model how to read the segments; V2 when PART 3 present>

[PART 1: TEXT DESCRIPTION]
<the §2 assembled text>

[PART 2: SPATIAL LAYOUT]           # present iff the panel declared spatial_layout
<mermaid comic_panel_layout — TOP/MID/BOT balloon/subject/ground zones, node depth
 (foreground|midground|background), framing, relations: left-of|right-of|above|below|contains|overlaps|speaks>

[PART 3: COMPOSITIONAL INTENT]     # present iff compositional_intent declared
<free-text anchor, e.g. composition_naturalness — a tie-breaker, NOT literal content to render>
```

Rules for renderers: the wrapper + segment markers are **instructions, not visible content** — never render the
marker text; PART 2 is authoritative for spatial arrangement when it conflicts with PART 1 phrasing; PART 3 selects
among readings PART 1+2 both admit. Parse/serialize reference: `panel_layout.parse_panel_layout` /
`serialize_panel_layout` (round-trip idempotent).

## 5. Aspect ratios

`aspect_ratio` ∈ `{1:1, 3:4, 16:9, 9:16, 4:3}` — explicit per panel, else derived: splash / full-bleed-span →
`3:4` (full_page) · wider-than-tall span → `16:9` · taller-than-wide → `3:4` · else `1:1`. ComfyUI pixel mapping is
adapter-internal (the existing `ComfyForgeTier1Adapter` carries an aspect→pixel map); print target sizes come from
the panel's geometry (the render manifest's `target_px`), not from this ratio alone.

## 6. Forward contract (the render bridge)

The Halftone H2 **render manifest** carries, per panel: `prompt_text` (=`image_prompt`), `prompt_layers` (incl.
`negative`), `dual_prompt?`, `aspect_ratio`, `target_px`, seed, and a **`render_chain`** — ordered stages, e.g.
`generate` (Gemini/Imagen; single-prompt form) → `refine` (ComfyUI img2img seeded by the generate output; positive
from the non-negative channels + trigger words, negative from the `negative` channel; LoRA slot; upscale). The ask
to ComfyUI.aDNA (a `comic_panel_refine` workflow taking `{image, positive, negative, denoise, seed, loras[]}`)
binds to **this document**.
