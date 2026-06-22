---
plan_id: mission_a2_comic_build
type: plan
title: "A2 — Build comic_generator on canvas_std (C-1..C-4)"
owner: stanley
status: completed
campaign_id: campaign_canvas_production
campaign_phase: 2
campaign_mission_number: 3
mission_class: implementation
created: 2026-06-21
updated: 2026-06-21
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, production, atelier, comic, build]
---

# Mission: A2 — Build `comic_generator` on `canvas_std` (C-1..C-4)

**Campaign**: [[how/campaigns/campaign_canvas_production/campaign_canvas_production|campaign_canvas_production]]
**Phase**: 2 — Comic producer (the larger build)
**Mission**: 3 of 5 (A2.1–A2.4 folded as objectives C-1..C-4)

## Goal

Build `what/production/comic_generator/` — a net-new, self-contained producer on `canvas_std` that turns a
substrate-free `ComicInput` into a multi-page/spread v2.0.0 **aDNA-Native** `.canvas`, structurally the
`document_generator` pattern with a 2D panel-grid interior. The bulk ports from the legacy `canvas_comic` engine
(6-layer prompt assembly · color-script · panel-grid layout); only the canvas construction is rewritten. Panels emit
image **prompts as `_reserved` metadata** — the producer never renders (ComfyUI owns pixels). Completes the comic
production layer Canvas absorbed at pt09.

## Exit Gate (= A2→A3 phase gate, HUMAN)

- Full `comic_generator` suite green (~45–55 tests); `ruff` clean.
- A worked example (a short multi-page/spread mini-issue) builds + validates **aDNA-Native** + degrades (D-1/D-2/D-3).
- Image-prompt boundary preserved: no rendering, no ComfyUI import, no image I/O; prompts live in
  `component_types[panel].qualities.image_prompt`.
- No regression (`canvas_std` 80/10 · brief 10 · deck 16 · document 37 · diagram 36).
- `canvas_std` firewall git-diff 0.
- `iii_quality_contract.md` present (full comic contract).
- **HOLD** for operator before A3 (validation & close).

## Objectives

### C-1. Scaffold + ported content layer
- **Status**: completed
- **Description**: Package skeleton (mirror `document_generator`); substrate-free `model.py` (`ComicInput`/`Page`/`Panel`/`Spread`); PORT `style.py` (tables), `prompt.py` (6-layer assembly as pure fns + local `ImagePrompt`), `panel_layout.py` (mermaid panel-grid), `rlhf_hints.py` (gated/dormant) from the quarry (theme/CanvasBuilder coupling stripped). Land the ported pure-function tests (`test_prompt_assembly`, `test_panel_layout`, `test_model_neutrality`) green.
- **Files**: `what/production/comic_generator/{pyproject.toml,src/comic_generator/{model,style,prompt,panel_layout,rlhf_hints}.py,tests/...}`
- **Depends on**: A1 (pattern proven)

### C-2. Canvas construction (the rewrite)
- **Status**: completed
- **Description**: `layout.py` (print-spec → integer geometry; grid/splash/spread), `panels.py` (panel → `file`/`text` `image`-class node + component_types incl. `qualities.image_prompt`), `consume.py` (`build_comic`: assemble source → `to_canvas` → enrich `_reserved`). Conformance passes aDNA-Native.
- **Files**: `src/comic_generator/{layout,panels,consume}.py`
- **Depends on**: C-1

### C-3. Conformance hardening + CLI + example
- **Status**: completed
- **Description**: `test_conformance`/`test_roundtrip`/`test_degradation`/`test_components`/`test_panel_coverage`; CLI `comic-generator build`; worked example mini-issue (`.yaml` + `.canvas`); no-regression run across all suites.
- **Files**: `src/comic_generator/__main__.py`, `tests/...`, `examples/...`
- **Depends on**: C-2

### C-4. Quality contract + docs
- **Status**: completed
- **Description**: `iii_quality_contract.md` (full comic — visual-narrative coherence · character consistency · composition/panel hierarchy + rigor + accuracy); README/AGENTS; note the `profiles_used: [...,comic]` federation-wrapper addition (CanvasForge-side, not here).
- **Files**: `comic_generator/{iii_quality_contract.md,README.md,AGENTS.md}`
- **Depends on**: C-3

## Campaign Context

### Previous Mission Outputs
- A1.1 proved the producer pattern + the `_reserved`/canvas-mapping conventions on `canvas_std` (diagram_generator 36/36).

### Next Mission Inputs
- A3.1 cross-producer validation runs all 5 production suites + structural `iii/` review of both new examples; logs the diagram `PL_EXTENT_UNITS` erratum (+ any comic erratum) to the LIP queue.

## Notes

**Canvas model (spec_panel_link_semantics):** issue = `comic_root` group (one canonical surface); spread = nested group
+ `region` (`flow: horizontal`, `extent.unit: pages, max: 2`); page = nested group + `region` (`extent.unit: pages,
max: 1`, the sequenced reading unit); panel = `image`-class `file`/`text` node. Edges: `sequence` over pages (acyclic,
from `isStartNode`), `reading_order` within a page, `adjacency` for gutter neighbors. **`extent.unit ∈
{words,pages,slides}` — use `pages`, NOT `panels`.**

**Guardrails:** `canvas_std` immutable (firewall git-diff 0); quarry = port-from, no `canvas_core` import;
`{"profile":"comic"}` producer-side (named in `spec_federation_contract §6.1`); **no rendering** — prompts in
`qualities.image_prompt`. **Scope (D5, ratified):** data-driven engine; SS issue → `examples/` only; drop the legacy
`ContextPack` file gate (→ `context_object.refs`); RLHF dormant; page/spread counts from input.

Full design (port-vs-rebuild table, canvas mapping, image boundary, `_reserved`, tests, objectives, quality contract)
in the approved plan `~/.claude/plans/please-read-the-claude-md-lovely-star.md` (§"Comic producer").

## Completion Summary

### Deliverables
- `what/production/comic_generator/` — the 5th in-vault producer (~1,790 src LOC, 9 modules + 9 test files / ~1,084 test LOC): substrate-free `model.py`; PORTED `style.py` (tables/lookups, mechanism only), `prompt.py` (6-layer assembly as pure fns + local `ImagePrompt`, `ContextPack` gate dropped), `panel_layout.py` (mermaid panel-grid near-verbatim), `rlhf_hints.py` (dormant); REWRITTEN `layout.py`/`panels.py`/`consume.py` (canvas construction on `canvas_std`).
- Multi-page/spread aDNA-Native `.canvas`: `comic_root` group = one canonical surface; spread + page nested-group `region`s (`extent.unit: pages`); panels = `image`-class `file`/`text` nodes; `sequence` (pages, acyclic) / `reading_order` (page Z-path) / `adjacency` (gutters) edges; `isStartNode` on page 0.
- **Image boundary preserved** — the assembled 6-layer prompt (+ `dual_prompt`) rides in `component_types[panel].qualities.image_prompt`; no rendering, no ComfyUI/torch/PIL import. Worked example: a 4-page / 2-spread Science-Stanley mini-issue (data in `examples/`, not baked into the engine).
- **Verified independently:** comic **87/87** + ruff clean; CLI build+validate `adna_native [OK]` + degradation D-1/D-2/D-3; **no regression** (canvas_std 80/10 · brief 10 · deck 16 · document 37 · diagram 36); `canvas_std` firewall git-diff 0. `iii_quality_contract.md` (full comic) shipped.

### Descoped
- Legacy `ComicProductionAdapter` (multi-stage orchestration) + `ComicReport.review()` scoring (→ became the quality-contract dimensions) + the `PendingPanel`/variant image machine — all out of scope (CanvasForge/ComfyUI concerns).

### Key Findings
- The comic exercised the nested-group region model (spread→page→panel) deeper than `document_generator` and it held cleanly; the image-prompt-as-`qualities`-metadata pattern keeps the ComfyUI boundary crisp.
- **Minor note (A3.1):** `panel_link.surface` is free-form (not enum-checked); the producer used `"comic_page"`. If the Standard later enumerates surface tokens, a `comic_page`/`print_page` value is a candidate — low priority.

### Scope Changes
- D5 honored: data-driven engine (characters/color-script/story-state from `ComicInput`); SS instance data lives in `examples/` only. `dual_prompt` added as a passthrough quality (renderer convenience).

## AAR

- **Worked**: ~60% of the build was a clean port of canvas-agnostic logic (prompt assembly, panel-grid layout, tables); only the canvas construction was rewritten, so a large producer landed green fast.
- **Didn't**: a few legacy tests didn't port (they exercised `CanvasBuilder`/`ImageClient` plumbing that no longer exists) — replaced by the new conformance/coverage suites; no functional loss.
- **Finding**: a comic reduces cleanly to the same grammar as a document (groups + regions + typed edges) + an `image` interior; the Standard needed no new feature.
- **Change**: none.
- **Follow-up**: A3 — validation & close ([[how/campaigns/campaign_canvas_production/campaign_canvas_production|campaign]] Phase A3); surface-token note + the diagram `PL_EXTENT_UNITS` erratum → A3.1 LIP queue.
