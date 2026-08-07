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
work). `gemini` (first real pixels, SPEND-gated) lands at Halftone H3; VisualDNA character compose
landed at H5; `comfy` refine landed at **H4** (below).

## The render chain

```
<stage>:<backend>[@denoise][/workflow]   comma-separated, ordered
```

```bash
--chain "generate:fake"                                    # default; offline
--chain "generate:fake,refine:fake@0.4"                    # chain proof, no network
--chain "generate:gemini,refine:comfy@0.4/comic_panel_refine"   # the production hybrid
```

The hybrid is a **chain, not a switch**: the cloud backend generates, ComfyUI refines its output
(img2img). `comfy` is a refine backend only — asking for `generate:comfy` raises, because the cloud
backend is the production substrate (inherited ADR-003).

### The `comfy` refine backend (H4 — the Vulcan seam)

| Knob | Default | Notes |
|------|---------|-------|
| `COMIC_RENDER_COMFY_ENDPOINT` | `http://localhost:8188` | the L1-local endpoint `how/federation/comfyui/` declares |
| `COMIC_RENDER_COMFY_WORKFLOW_DIR` | unset | dir of named workflow templates; point it at ComfyUI.aDNA's `what/workflows/` once `comic_panel_refine` exists |
| `/workflow` in the chain | none | names a template in that dir; **unresolvable ⇒ built-in img2img graph** (`workflow_source: builtin`), never a failure |

The negative channel travels as its own node (never concatenated), and a panel's pair-gated
`characters[]` entry (H5) becomes a `LoraLoader` plus a trigger token on the positive prompt.
ComfyUI mechanics live in `canvas_core.comfyforge_adapter` — the boundary guard's stated intent —
so `backends/comfy.py` stays a thin manifest-shaped binding. The recorded HTTP contract is in
`tests/fixtures/comfy/`; a live smoke exists behind `-m network`.

> **Refining a `fake` panel looks broken and isn't.** The fake backend emits flat solid-colour
> PNGs. img2img at a production denoise (~0.4) preserves the seed's structure — and a solid colour
> *has* none, so you get a flat field back and may conclude the seam is broken. It isn't: at
> denoise ≥0.9 the same call renders the prompt properly (verified live 2026-08-07). In the real
> chain the seed is a cloud-generated panel with real structure, where 0.4 is correct. If you are
> smoke-testing `generate:fake,refine:comfy`, raise the denoise or seed from a real image.

`issue.rendered.canvas` is a **derived artifact** (operator ruling 2026-08-03): the YAML source +
producer stay authoritative — re-render, don't merge back.

## Layout

Producer idiom: `pyproject.toml` · `src/comic_render/` · `tests/` · `AGENTS.md` ·
`iii_quality_contract.md`. Depends on `adna-canvas-std` (editable); reaches the unpackaged
`canvas_core` via the production-shelf `sys.path` (pytest `pythonpath` + a guarded bootstrap in
`__init__.py`). The `env` extra carries canvas_core's own import-surface deps (pillow, pyyaml,
google-api-python-client) — comic_render source never imports them.
