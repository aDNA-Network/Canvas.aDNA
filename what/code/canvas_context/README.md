# adna-canvas-context

Reference **context-loader** for the aDNA Canvas Standard — loads a `.canvas` document as a navigable
**context graph** *without rendering it*. This is the leg-2 reference implementation of the
[`spec_canvas_context_loading`](../../specs/spec_canvas_context_loading.md) protocol (Operation Salon P2).

A canvas has a dual nature: it can be **rendered as output** (a 2D artifact) *and* **read as context** (a structured
object an agent loads to understand a domain). `canvas_std` owns the render/round-trip face; **`canvas_context` owns
the read-as-context face** — parse → build a baseline graph → overlay the `_reserved` semantic layers → resolve the
context identity, references, and reading order → expose a read-only traversal API. No rasterizer, no media decoder,
no transport, no router (bounded by [ADR-006](../../decisions/adr_006_canvas_surface_boundary.md)).

## Install / run (firewall-safe)

`canvas_context` is a **read-only consumer** of `canvas_std`'s public API (D6 firewall: it never edits or installs
into the `canvas_std` tree). In dev/test the dependency is resolved via pytest's `pythonpath`:

```
# from what/code/canvas_context/ — uses canvas_std's venv for pytest; PYTHONDONTWRITEBYTECODE keeps canvas_std pristine
PYTHONDONTWRITEBYTECODE=1 ../canvas_std/.venv/bin/python -m pytest -q
```

## Usage

```python
from canvas_context import load_context_graph, DefaultPathResolver

g = load_context_graph("path/to/doc.canvas")          # parse + validate + build, no rendering
g.identity()                                           # {"id": "urn:adna:canvas:...", "version": "0.1.0"}
g.summary()                                            # agent-facing summary, or None
g.conformance()                                        # {"declared": "...", "reached": "...", "stale": bool}
g.reading_order()                                      # ordered node-id walk (document order), no geometry needed
g.refs()                                               # outbound context references (wikilink / federation_ref)
g.neighbors("node_id", kind="reading_order")           # typed adjacency

# in-vault wikilink resolution (cross-vault federation_ref returns a descriptor, never transported):
g.resolve(g.refs()[0], DefaultPathResolver(vault_root="/path/to/Canvas.aDNA"))
```

## Layout

```
src/canvas_context/
  model.py       # the context-graph record shapes (spec §3)
  loader.py      # the normative L1–L7 load pipeline (spec §4) — load_context_graph()
  resolver.py    # the abstract Resolver contract + DefaultPathResolver (spec §5)
  traversal.py   # the reading-order walk used by the §6 primitives
tests/           # loader · traversal · pilot (loads a real producer .canvas as context)
```

## Boundary

This package is a **contract realization + a reference loader**, not a runtime. Rendering → producers / Astro;
federation transport → the federation layer; cross-surface routing → the future OIP layer; gate runtimes → ISS.
See `spec_canvas_context_loading.md` §11 and ADR-006.
