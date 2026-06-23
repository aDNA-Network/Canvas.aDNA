# AGENTS.md — `canvas_context` (leg-2 reference loader + leg-3 interaction surface)

Code-as-WHAT object under `Canvas.aDNA/what/code/`. Built in **Operation Salon P2** (leg-2 loader, reference impl of
`what/specs/spec_canvas_context_loading.md`); extended in **Salon P4** with the leg-3 interaction surface
(`interaction.py`, reference impl of `what/specs/spec_interface_surface.md` §3.1 + the `I-*` family). Persona: **Mondrian**.

## What this is

- **Leg 2 (read-as-context):** a loader that turns a `.canvas` into a navigable **`ContextGraph`** — with **no
  rendering**. A read-only **consumer** of `canvas_std`'s public API.
- **Leg 3 (interaction surface):** a thin, additive **read-only extension** that *composes* the `ContextGraph` (an
  `InteractionSurface` *has-a* `ContextGraph`) + a pure append-only `apply_response` fold — realizing the
  `read → act → re-read` loop. It is **not** a capture runtime, renderer, or transport (ADR-006 §2 / spec §10.2).

## Hard rules (read before editing)

- **Firewall (D6).** `canvas_std` is **immutable**. This package imports it **read-only** (public API +
  `canvas_std.reserved` enums); the dependency is one-way (`canvas_context → canvas_std`). Never edit, never
  editable-install into, the `canvas_std` tree. Verify `git status -s -- ../canvas_std/` is clean after any work here.
- **No rendering (spec §4 L7).** No rasterizer, image generator, video/frame decoder, or layout-to-pixels. `file` /
  `image` / `video` components are carried **by reference** only.
- **No transport, no routing.** Federation fetch is the resolver's/federation layer's job; cross-surface routing is
  the OIP layer's. The loader exposes refs and delegates (spec §5; ADR-006 §2–§3).
- **`_reserved` is additive.** A canvas without `_reserved` MUST still load (degradation, spec §8). `_reserved` lives
  at `doc["metadata"]["frontmatter"]["_reserved"]`.

## Map

| File | Spec section | Role |
|------|--------------|------|
| `src/canvas_context/model.py` | §3 | `ContextGraph` + `Component` / `Panel` / `Relation` / `Ref` / `Surface` / `Conformance` |
| `src/canvas_context/loader.py` | §4 | `load_context_graph()` — the normative L1–L7 pipeline |
| `src/canvas_context/resolver.py` | §5 | `Resolver` protocol + `DefaultPathResolver` (in-vault wikilink) |
| `src/canvas_context/traversal.py` | §6 | the reading-order walk behind `ContextGraph.reading_order()` |
| `src/canvas_context/interaction.py` | `spec_interface_surface` §3.1/§4/§8.2/§9.1 | **leg 3** — `load_interaction_surface()` + `InteractionSurface` (read) · `apply_response()` (append-only fold) · `validate_interaction_block()` (I-1/I-2/I-3) · `strip_interaction()` + `is_round_trip_safe()` (I-D) |
| `tests/test_pilot.py` | §9.1 | the leg-2 proof — loads a real producer `.canvas` as context, no rendering |
| `tests/test_interaction*.py` | leg-3 §9.1 | I-1/I-2/I-3 conformance · the read→act→re-read loop proof · I-D round-trip-to-baseline |
| `tests/pilot_interaction_loop.py` + `tests/fixtures/` | leg-3 §10.2 | the runnable on-disk loop demo + the interaction-bearing golden (`interaction_review.canvas`, all 4 affordance kinds) |

## Run

```
PYTHONDONTWRITEBYTECODE=1 ../canvas_std/.venv/bin/python -m pytest -q
```

## Conformance

A conformant loader satisfies `spec_canvas_context_loading.md` §9 (8 MUST / 3 SHOULD / 1 MAY). The suite reuses the
`canvas_std` golden fixtures + a real `document_generator` output.
