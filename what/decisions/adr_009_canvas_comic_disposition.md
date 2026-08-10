---
type: decision
adr_id: "009"
title: "canvas_comic disposition — reader-only freeze now, archive after H3"
status: proposed
created: 2026-08-09
updated: 2026-08-09
last_edited_by: agent_mondrian
signed_by:
supersedes:
superseded_by:
phase: halftone-h6
resolves: "gap G6 (canvas_comic disposition ambiguous) · Halftone roadmap §4 open decision #3"
tags: [adr, canvas, canvas_comic, disposition, freeze, archive, legacy, quarry, halftone, h6]
---

# ADR-009 — `canvas_comic` disposition

## Status

**proposed** — operator ruling recorded at the H6 plan gate (2026-08-09); §7.7 signature pending.

## Context

`what/production/canvas_comic/` is the legacy CanvasForge comic engine, relocated to the production shelf at
Production Tidy P5 (`adr_004_production_code_layout.md`). The gap register has carried it as **G6, "disposition
ambiguous"**, since Halftone was chartered: *a frozen quarry whose tests still ride the production suite, with
no disposition record.*

Ground truth as of 2026-08-09:

| | |
|---|---|
| Contents | `comic.py` (~1150 LOC) · `mermaid_layout.py` · `_rlhf_hints.py` · `__init__.py` re-exports |
| Tests | **99 passing** (+11 subtests), riding the shelf-level `pytest.ini` |
| Production importers | **none** — not `comic_generator`, not `comic_render`, not `canvas_core` |
| Other live importers | exactly **one**: `what/production/tests/test_federation_validation.py:50` (`ComicPageBuilder`, `CHARACTER_STANLEY`) |
| Character constants | hardcoded Science Stanley (`CHARACTER_STANLEY`/`_AGENT_STANLEY`/`_HELIX`) — the project-neutrality the successor deliberately does not have |
| Lineage still load-bearing | the trim/bleed geometry mirrored into `canvas_core.print` (credited at `compose.py:10`) |

The successor is real and shipped: `comic_generator` (123 tests, data-driven bible, no hardcoded characters) plus
`comic_render` (94). The legacy engine is not on any production path.

## Decision

**Reader-only freeze now. Archive after H3. No code moves in this pass.**

1. `canvas_comic` is **frozen**: a reader-only quarry. No new features, no refactors, no lint sweeps.
   Maintenance is limited to keeping it *runnable* — a frozen module must not be allowed to rot into a failure.
2. Its **99 tests keep riding the production suite**, deliberately, as a regression net over the geometry
   lineage that `canvas_core.print` inherited. They are the only executable check on that lineage until the
   first real comic is printed.
3. **Archive after H3**, not before. H3 is the first real rendered page; until it exists, the legacy engine is
   the only thing in the vault that has ever composed a comic page for print, and its tests are the only
   evidence the trim/bleed constants are right.
4. `ComicReport` (the scoring loop) is **not ported**. It comes back only if a scoring loop revives — and then
   as a new build against `comic_generator`, not a lift.
5. The single live importer (`test_federation_validation.py:50`) is **left in place** and is the tripwire: when
   archiving, it is the one call site that must be repointed or retired.

## Consequences

**Accepted:**

- The production suite carries 99 tests for a module on no production path. That is the price of the regression
  net, knowingly paid, for one phase.
- 12 pre-existing `ruff` findings (unused imports) in `canvas_comic/tests/test_comic_builder.py` **stay
  unfixed** — lint-cleaning a frozen module is development on something declared frozen. They are recorded here
  so they are not mistaken for new drift.
- The stale path comment at `_rlhf_hints.py:44` (still says `what/code/canvas_comic/`, pre-P5-relocation) is
  likewise left. Recorded, not fixed.

**One maintenance exception already exercised (H6/O5):** `test_comic_builder.py:350` constructed a
`PrintExporter` with the default `cmyk=True`. When H6 made the colour policy refuse un-reproducible CMYK, that
call site would have kept passing on macOS and failed on any host without ColorSync profiles. `cmyk=False` was
made explicit. That is the freeze rule working as intended: *keep it runnable, add nothing.*

**Reversibility:** total. Nothing is deleted; archiving is a move under SO-7 (archive-never-delete).

## Alternatives considered

- **Archive now.** Cleaner shelf immediately, but it removes the geometry regression net *before* H3 has proven
  the constants against real pixels. Rejected on sequencing, not on merit.
- **Record only, change nothing.** Closes G6 on paper without deciding anything. Rejected: the gap was never
  "undocumented", it was "undecided".

## Ratification (§7.7)

| Field | Value |
|-------|-------|
| Decision | `canvas_comic` = reader-only freeze now · archive after H3 · `ComicReport` not ported |
| Ratified by | *(pending — operator)* |
| Date | *(pending)* |
| Status | **proposed** |
