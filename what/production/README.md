---
type: context
created: 2026-06-17
updated: 2026-06-22
status: active
last_edited_by: agent_stanley
tags: [canvas, production, deck, comic, diagram, letter, post, palette, pt09, canvasforge_merge]
---

# Canvas.aDNA — Production Layers

Producers that turn a domain spec into a v2.0.0 **aDNA-Native** `.canvas` on the immutable `canvas_std` reference
implementation (`what/code/canvas_std/`), under the two-shelf firewall (ADR-004): this shelf may carry deps and
mutate; `canvas_std` is never edited. Image generation stays in ComfyUI; quality review in III; render/pixel scoring in
`canvas_presentation` (PT-P5). Build a new one with the factory: `how/skills/skill_canvas_producer_build.md` + clone
`_scaffold/`.

## Live in-vault producers (on `canvas_std`)

| Producer | Output | Surface shape | Tests | Campaign |
|---|---|---|---|---|
| `brief_consumer/` | single-page brief | single surface | 10 | Keystone E4.3 |
| `deck_generator/` | slide deck | slides = groups; sequence | 16 | Keystone E4.4 |
| `document_generator/` | long-form document (paper) | multi-page; reflow | 37 | Keystone E4.1/E4.2 |
| `diagram_generator/` | 5 diagram types (graph) | single surface + derived Mermaid | 36 | Atelier A1 |
| `comic_generator/` | multi-page comic | spreads/pages; image prompts | 87 | Atelier A2 |
| `letter_generator/` | one-page letter | single surface; one paged region | 17 | Palette P2 |
| `post_generator/` | social post / thread | single surface; sequence thread | 20 | Palette P3 |

**Sweep (2026-06-22):** 7 producers = 223 + `canvas_std` 82 = **305 passed** (+10 skipped); `canvas_std` firewall
git-diff 0. The thesis output list (paper · deck · comic · letter · post; + diagram + brief) is covered.

- **`_scaffold/`** — the copy-me producer skeleton (not a producer; excluded from the sweep). Clone it per
  `how/skills/skill_canvas_producer_build.md`. Pattern: `what/context/context_canvas_producer_pattern.md`.

## Legacy CanvasForge engines → relocate at PT P5 (Hestia)

**Origin:** Canvas absorbed the CanvasForge production layers at Production Tidy **pt09** (2026-06-17), reversing the
E3.4 split (Hermes → Mondrian). pt09 was a **governance merge**; the legacy *engines* (distinct from the net-new
`*_generator` producers above) relocate from the archive in Production Tidy **P5**:

| Layer | Code (relocates P5 → here) | P5 source location |
|---|---|---|
| deck render | `canvas_presentation/` | `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_presentation/` |
| comic engine | `canvas_comic/` (9 py) | `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_comic/` |
| diagram + core | `canvas_core/` (80 py) | `Archive.aDNA/CanvasForge.aDNA/what/code/canvas_core/` |

**In-code shim:** `canvasforge.canvas_core → canvas_std` (deprecation re-export, grace to 2027-06-13; Home.aDNA §C #29,
owner Mondrian). **Consumer wrappers:** ~8 vaults / ~11 wrappers federate to `CanvasForge.aDNA`; they resolve via the
merge-archive shim until **P5 wrapper-refederation** repoints them to Canvas. Producer knowledge (typography · color ·
composition · scoring · courier-loop) is preserved verbatim in `Archive.aDNA/CanvasForge.aDNA/` — a quarry to port
from, not a runtime dependency for the `*_generator` producers above (which are net-new on `canvas_std`).
