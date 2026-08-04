---
type: doc
doc_id: canvas_authoring_guidance
title: "Canvas authoring guidance — the numbers that make a canvas readable in Obsidian"
standard_version: "2.3.0"
status: active
created: 2026-08-03
updated: 2026-08-03
last_edited_by: agent_mondrian
provenance: "Halftone HV (gap G7). Constants Obsidian-CSS-derived; absorbed with credit from Oration.aDNA canvas_fit_check.py (Robert Kennedy, coord 2026-08-03), validated against two operator-observed failures. Companion code: what/production/canvas_core/text_metrics.py (OBSIDIAN_*) + traps/ + traps/cli.py."
tags: [doc, canvas, authoring, guidance, visual_fidelity, obsidian, hv]
---

# Canvas Authoring Guidance — the real numbers

> **Why this exists.** `canvas-std validate` proves schema conformance and *nothing about whether a canvas
> reads* — by design (the Standard is substrate-neutral). A 53-node canvas passed `[OK]` and rendered with ~20/23
> text nodes clipped mid-sentence (Oration M-R5, 2026-08-03). Nothing in any aDNA document carried these numbers
> before. Now they live here, they are machine-checked by **`canvas-visual-check`**, and the ship gate requires an
> **agent-confirmed Obsidian render** (`spec_federation_contract` §4 Amendment 1).

## The geometry you are actually fighting

Obsidian renders a canvas text node's content in `display: flex; flex-direction: column` with
`padding: 0 24px`. Flex means **margins do not collapse** — a heading's margin-top and the following paragraph's
margin-top both apply in full. At the fleet defaults (`--font-text-size: 16px`, `--body-line-height: 1.6`):

| quantity | value |
|---|---|
| usable width | `node_width − 48px` |
| body line | 25.6px |
| paragraph margin (top **and** bottom, non-collapsing) | 14.4px |
| prose density | ~8.1px/char (Inter 16px mixed case) |
| safe fill | plan for **90%** of node height, never 100% |

**Lead cost** — the vertical price of a node's first block *before any body text renders*:

| lead | cost | note |
|---|---|---|
| `#` | 56.7px | |
| `##` | **98.9px** | the Oration killer: in a 320×110 node, 11px remained for body |
| `###` | 74.8px | |
| `####` | 42.6px | |
| `**bold**` | **40.0px** | reads as a title; saves 2+ body lines vs `##` |
| plain | 0px | |

## The five rules

1. **Never `#`/`##`/`###` to title a canvas text node.** Use a `**bold**` lead (40.0px vs 98.9px).
   *(Trap: CV-LEAD-COST-01.)*
2. **Fit the text to the box**: `chars ≤ (W − 48) × (0.90·H − P) / 208`, where `P` is the lead cost above
   (the 208 ≈ 8.1px/char × 25.6px line). When in doubt, run the checker — it reports the **required height** per
   failing node. *(Trap: CV-TEXT-BOUNDS-01, Obsidian-calibrated.)*
3. **Group labels: ≤ width/25 chars (ALL CAPS) or width/22 (mixed case).** Labels never wrap, hard-ellipsise,
   and — because of `--zoom-multiplier` — get *worse as you zoom out*. *(Trap: CV-GROUP-LABEL-01.)*
4. **Edge labels: ≤ 20 chars, or omit.** The label box is opaque, pinned to the edge midpoint, and cannot be
   moved; past ~33 chars it wraps into a box bigger than most nodes and covers whatever is beneath it. 83% of
   fleet edges carry no label — that practice is correct. *(Trap: CV-EDGE-LABEL-01, incl. collision geometry.)*
5. **File nodes render the target's Properties table** unless the vault sets
   `.obsidian/app.json → propertiesInDocument: "hidden"` — a frontmatter-bearing target becomes ~80% YAML table.
   Size cards for the embed header (35px) + the target's H1 at 2.3em, or they clip their own title.
   *(Trap: CV-FILE-PROPS-01.)*

## The three checks, in order — none substitutes for another

| check | proves | command |
|---|---|---|
| 1. Schema | conformance to the Standard | `canvas-std validate <file.canvas>` |
| 2. Visual fit | the geometry above | `python -m canvas_core.traps.cli <file.canvas>` *(from `what/production/`)*; from any other vault use the batteries-included venv: `<Canvas.aDNA>/what/production/canvas_core/.venv/bin/python <Canvas.aDNA>/what/production/canvas_core/traps/cli.py <file.canvas>` — `--strict` to fail on medium findings, `--json` for machines, `--vault-root` if auto-detection (nearest `.obsidian`) misses |
| 3. Sight | it actually reads | open in live Obsidian → screenshot → **the agent reads the image and judges it** (`what/context/context_canvas_visual_in_the_loop.md`; Home.aDNA `canvas_visual_loop.py` is the worked harness) |

## Known limitations & expected findings

- `canvas_core/html_renderer.py` models a `file` node as image-or-placeholder only — the HTML/Playwright render
  loop is **blind by construction** to the Properties-table failure mode. CV-FILE-PROPS-01 covers it statically;
  the renderer fix is a deferred follow-up (Halftone HV close notes).
- **Print-geometry comics pack panels edge-to-edge by design** (ComixWellspring trim, deterministic integer grid) —
  expect CV-GROUP-PADDING-01 / CV-NODE-DENSITY-01 findings on comic pages and **review them rather than
  auto-failing**; the comic pipeline (Halftone H2+) interprets these against its print spec. The aesthetic
  breathing-room thresholds are tuned for information canvases.
- CV-PENDING-01 firing on a `status: prompt_only` comic is **correct** — it is telling you the pipeline
  dead-ends at rendering, which is exactly Operation Halftone's G1.

## Consumers

Producers: `skill_canvas_producer_build.md` steps 5–6 bind checks 1–3 into the build. Consumer vaults (via the
`canvas/` federation wrapper): stage 2/3 of the 5-stage gate (`spec_federation_contract` §4). Hand-authoring a
canvas *without* a wrapper? Run all three checks anyway — the incident that created this doc did not have a
wrapper, which is exactly how it skipped every gate.
