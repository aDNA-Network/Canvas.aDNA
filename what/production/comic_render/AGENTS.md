# AGENTS.md — comic_render (the Halftone render bridge)

Read this before touching anything in this directory.

## What this is

The H2+ render bridge: `issue.canvas` → render manifest → dispatched variants → Schema-A
selection → `issue.rendered.canvas` (NEW file) → composited print pages. Built under
`campaign_canvas_halftone`; architecture source of truth =
`how/campaigns/campaign_canvas_halftone/missions/artifacts/halftone_roadmap.md` §1.

## Hard rules (campaign standing orders)

1. **"Canvas dispatches, it does not diffuse."** HTTP dispatch clients MAY be imported;
   torch/diffusers/comfy-local/cv2/imageio NEVER; PIL only via `canvas_core.print`. The AST guard
   (`tests/test_boundary.py`) fails loudly — do not weaken it.
2. **Never import `comic_generator`.** The producer hands off file-shaped via `.canvas`. Tests use
   the committed fixture, not a producer call.
3. **Write-back never mutates the input.** Output is always a NEW `issue.rendered.canvas`; nodes
   and edges are never added/removed (the topology-only sync hash must come out identical —
   asserted in `writeback.py`); `_reserved.sync` stays byte-identical; the five
   `ANCHOR_REF_KEYS` (`ref/anchor/anchor_ref/cites/for`) never appear as qualities keys.
4. **Reuse the substrate, never re-abstract it**: `ImageClient`/`ImagenWiring`
   (`canvas_core/image_generation.py`) for generate + variant paths; `RefineClient`
   (`backends/base.py`) is the ONLY additive protocol; `PrintExporter` for compose;
   `canvas_core.rlhf` **Schema-A only** for selection records (never `ImagenWiring`'s Schema-B
   sidecar — the III bridge skips it).
5. **`what/code/canvas_std/` is read-only** (campaign firewall — `git diff --stat` empty at every
   gate).
6. **Spend is operator-gated**: `budget_cap` enforcement in `dispatch.py` is load-bearing; the
   `gemini` backend (H3) must not land without the SPEND-gate plumbing intact.

## Working here

- Own venv: `python -m venv .venv && pip install -e ../../code/canvas_std -e '.[dev,env]'`.
- Run tests from THIS directory: `python -m pytest -q` (pyproject `pythonpath = ["src", ".."]`
  reaches the unpackaged `canvas_core`).
- The manifest sidecar is resumable state — every stage idempotent; keep it that way.
- After any change: this suite green + `comic_generator` suite unaffected + full producer sweep +
  firewall check (see the campaign CLAUDE.md).
