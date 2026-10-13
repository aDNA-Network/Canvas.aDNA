---
type: backlog
idea_id: idea_imagenwiring_selection_surface_deprecation
title: "Deprecate ImagenWiring's selection-surface cluster — 10 methods, zero call sites, measured; the class itself is live and stays"
created: 2026-09-09
updated: 2026-10-13
status: open   # step 1 (fleet consumer sweep) DONE 2026-10-13 — Vernier P6; steps 2–3 remain
priority: low
origin: "Blueprint P5 close — carried tail from Halftone, premise re-derived and corrected"
executor_tier: sonnet
token_budget_estimated: "one session, mechanical once the consumer sweep is done"
tags: [backlog, deprecation, imagen_wiring, canvas_core, comic_render, schema_b, technical_debt]
---

# ImagenWiring's selection surface is dead — but the class is not, and the carried tail said otherwise

## The tail as it was carried, and why it was wrong in both directions

Halftone handed Blueprint this item, and `STATE.md` carried it verbatim for seven weeks:

> *"legacy panel-side `ImagenWiring` deprecation candidates (**no live caller since the archive**;
> `comic_render` uses **only** `generate_variants`)"*

**Both parenthetical clauses are false as stated**, measured at P5 close:

- *"no live caller"* — `ImagenWiring` is imported and instantiated **live**:
  `what/production/comic_render/src/comic_render/dispatch.py:18,77`. It is also a public export
  (`canvas_core/__init__.py:93,244`).
- *"only `generate_variants`"* — `dispatch.py` uses **two** methods: `generate_variants` **and**
  `prepare_variant_paths`.

⇒ Anyone acting on the tail as written would have gone looking for a dead class, found a live one,
and either stopped (leaving real dead code) or deleted through a live caller. This is the P4 F-P4-1
class again — **a true-ish sentence inherited and never re-derived** — and it is the second instance
this campaign found in its own `STATE.md`.

**The real finding is larger than the tail claimed.** The dead surface is not "the panel path"; it
is the entire **selection-surface cluster**, and it is 10 methods.

## The measurement (2026-09-09, `.method(` call sites across `what/` + `how/`, excluding `_archive/` and the defining module)

| Method | Call sites | Status |
|---|---:|---|
| `generate_variants` | 1 | **LIVE** — `comic_render/dispatch.py` |
| `prepare_variant_paths` | 1 | **LIVE** — `comic_render/dispatch.py` |
| `variant_path` | 0 external | **internal** — called by the two live methods above (`image_generation.py:249,288`) |
| `selection_canvas_path` | 0 | dead |
| `sidecar_path` | 0 | dead |
| `build_panel_selection_canvas` | 0 | dead |
| `build_image_selection_canvas` | 0 | dead |
| `find_survivors` | 0 | dead (internal to two dead `resolve_*` methods) |
| `resolve_panel_with_choice` | 0 | dead |
| `resolve_image_with_choice` | 0 | dead |
| `resolve_panel_from_surviving_files` | 0 | dead |
| `resolve_image_from_surviving_files` | 0 | dead |
| `_enforce_single_survivor` | 0 external | dead (private helper to the dead `resolve_*` pair) |
| `write_selection_record` | 0 | dead — **and actively fenced** (below) |

⚠ **Two name collisions that a careless grep reads as live callers**, recorded so the next person
does not re-derive them:

- `canvas_core/rlhf/selection.py:203` defines its **own** module-level `write_selection_record` —
  the **Schema-A** writer. `ImagenWiring`'s is **Schema-B**. Same name, different function, opposite
  side of a deliberate boundary.
- `iii_bridge.py:223` contains the dict key `"selected_variant_path"`, which a `variant_path`
  substring grep matches. Not a call.

## The strongest evidence that the cluster is dead: something already guards it

`comic_render/tests/test_boundary.py:68` — `test_schema_b_writer_never_imported` walks every module
and asserts the string `write_selection_record` does not appear:

> *"Selection records are Schema-A (`canvas_core.rlhf`) — the Schema-B sidecar writer is off-limits."*

So one of these methods is not merely uncalled; **calling it is a test failure.** The architecture
already moved (Schema-A selection records, `rlhf/` surface, the P4 board) and the old surface was
left standing rather than removed.

## What a session should do

1. **Consumer sweep first.** `ImagenWiring` is a public `canvas_core` export. Sweep for external
   consumers before touching it — federation wrappers, the SS `canvas_comic` wrapper, ComfyUI.
   The measurement above covers *this vault*; it does not cover the fleet.
2. **Deprecate, don't delete, in one pass** — the 10 dead methods get a deprecation marker with a
   named sunset version; the 3 live/internal ones (`generate_variants`, `prepare_variant_paths`,
   `variant_path`) are explicitly excluded and annotated as such so the next reader does not have
   to re-measure.
3. **Sunset in a later pass**, once the deprecation has been through a release.
4. Note that the `resolve_*` / `find_survivors` / `_enforce_single_survivor` group is
   *self-referentially* live — the dead methods call each other. Call-count-based dead-code
   detection will report them as used. Only reachability from a live entry point is decisive.

## ⛩ Step 1 done — the fleet consumer sweep (2026-10-13, Vernier P6, Canvas HEAD `40e4fa5`)

**Population, stated on the face of the number:** every **non-symlink** root directory of `~/aDNA/`
(143 entries − 26 symlink shims = 117), excluding `Archive.aDNA` (archived), `Canvas.aDNA` (the
defining vault, measured above) and `llama.cpp` (upstream), leaves **114 directories swept**. Files are
`*.py` only, with `.venv/` and `site-packages` excluded. Shims are skipped because a shim is a second
name for a directory already counted (Rosetta's 254-vs-282).

| Probe | Result |
|---|---|
| `ImagenWiring` named in any `.py` | **1 file**, `Home.aDNA/what/code/googleai/client.py:7`, and it is a **docstring** saying the variant fan-out *"consumes it with no adapter"*. Not an import and not a call |
| `.<dead-method>(` call sites, all 10 dead names plus `_enforce_single_survivor` | **0** |

⇒ **No external consumer of the selection-surface cluster exists in the fleet on this node.** Step 2
(deprecate with a named sunset, live trio annotated) is now unblocked on evidence. Doing it is a
`canvas_core` change for a session that owns it, not for this sweep.

⚠ **What this sweep cannot see:** dynamic access (`getattr`, string dispatch), consumers on other
nodes, and anything outside `~/aDNA/`. The Home docstring is the one place a future reader might
mistake for a dependency, which is why it is named here.

## Why this is a backlog item and not a P5 act

Deprecating a **live public export** on a campaign's close day, without a fleet consumer sweep, is
a change dressed as housekeeping — SO-2 territory. The value P5 could add was to make the
measurement durable and correct the false premise at source, so that the next session starts from a
true sentence and spends its budget on the sweep instead of re-discovering the map. That is done;
this is the remainder.
