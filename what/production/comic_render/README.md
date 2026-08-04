# comic-render — the Halftone render bridge

Closes the gap the 2026-07 comic-system review found (**G1**): a well-built spec→canvas producer
whose pipeline dead-ended at rendering. This package takes a built `issue.canvas` (from
`comic_generator` — file-shaped handoff, never imported) through to composited print pages:

```
issue.canvas ──[plan]──▶ issue.render_manifest.json      (extract; staleness-guarded)
manifest ──[dispatch]──▶ runs/<comic_id>/<panel>_v{n}.png (generate backend: fake | gemini | comfy)
variants ──[refine]────▶ runs/<comic_id>/refined/*.png    (optional chain stage; img2img seeded)
outputs ──[select]─────▶ Schema-A SelectionRecord per panel
manifest ──[write-back]▶ issue.rendered.canvas            (NEW file; input immutable; sync_hash unchanged)
rendered ──[validate]──▶ conformance + degradation + files + DPI (the stage-6 gate)
rendered ──[compose]───▶ runs/<comic_id>/pages/*.jpg      (canvas_core PrintExporter shim)
```

**Boundary — "Canvas dispatches, it does not diffuse":** HTTP dispatch clients are welcome;
torch/diffusers/local pipelines are forbidden; PIL is reached only through `canvas_core.print`.
Enforced by the AST guard in `tests/test_boundary.py`.

## Quick start (offline, zero network)

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ../../code/canvas_std -e '.[dev,env]'
comic-render run --until compose path/to/issue.canvas          # whole pipeline, fake backend
comic-render plan issue.canvas --chain "generate:fake,refine:fake@0.4"   # hybrid chain
python -m pytest -q && ruff check src tests
```

The manifest sidecar is the resumable state; every stage is idempotent (re-runs skip completed
work). `gemini` (first real pixels, SPEND-gated) lands at Halftone H3; `comfy` (the Vulcan
`comic_panel_refine` seam) at H4; VisualDNA character compose at H5.

`issue.rendered.canvas` is a **derived artifact** (operator ruling 2026-08-03): the YAML source +
producer stay authoritative — re-render, don't merge back.

## Layout

Producer idiom: `pyproject.toml` · `src/comic_render/` · `tests/` · `AGENTS.md` ·
`iii_quality_contract.md`. Depends on `adna-canvas-std` (editable); reaches the unpackaged
`canvas_core` via the production-shelf `sys.path` (pytest `pythonpath` + a guarded bootstrap in
`__init__.py`). The `env` extra carries canvas_core's own import-surface deps (pillow, pyyaml,
google-api-python-client) — comic_render source never imports them.
