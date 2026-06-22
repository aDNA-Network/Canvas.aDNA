# post_generator

A net-new in-vault producer of the **aDNA Canvas Standard** (Operation Palette, P3). Turns a social-**post** spec —
a single post or a thread — into a v2.0.0 **aDNA-Native** `.canvas` that degrades to a valid Obsidian canvas. Built on
`canvas_std` (never modified — ADR-004 two-shelf firewall) by following `how/skills/skill_canvas_producer_build.md`.

## What it produces

One canonical surface (`post_root` group) holding post panels. Each panel's copy is a baseline `text` node (`post{i}`);
a thread chains them with `sequence` panel-link edges (linear, acyclic; `isStartNode` on `post0`). An optional image
rides as a **separate** `image`-class node (`img{i}`, a baseline `text` placeholder) whose prompt is carried in
`qualities.image_prompt` and tied to its post by an `adjacency` edge — **the producer never renders** (ComfyUI owns
pixels). The platform profile (char budget + aspect) rides in `component_types[post_root].qualities`; `semantic_bindings`
stays the bare `{"profile": "post"}`. Region: `{flow: vertical, pagination: none}` (a post is not paginated, so no
`extent`).

## Usage

```sh
python3 -m venv .venv
.venv/bin/pip install -e ../../code/canvas_std && .venv/bin/pip install pyyaml
PYTHONPATH=src .venv/bin/python -m post_generator build examples/example_post_thread.yaml out.canvas
.venv/bin/canvas-std validate out.canvas      # -> adna_native [OK]
```

Input is a YAML/JSON mapping: `title`, `id`, `platform` (`twitter`/`x`/`linkedin`/`instagram`), optional `version`,
`refs`, and either a top-level `text` (single-post shorthand) or a `panels` list of `{text, image_prompt?, alt?}`.
See `examples/example_post_single.yaml` and `examples/example_post_thread.yaml`.

## Develop / test

```sh
.venv/bin/pip install pytest ruff
PYTHONPATH=src .venv/bin/python -m pytest tests -q
.venv/bin/ruff check src tests
git diff --stat -- ../../code/canvas_std/    # MUST be empty (firewall)
```

## Layout
- `src/post_generator/model.py` — substrate-free `Post`/`PostPanel` + `PLATFORM_PROFILES` + `load_post` (no `canvas_std`).
- `src/post_generator/consume.py` — `build_post(Post) -> .canvas` dict (the 4-step contract).
- `src/post_generator/layout.py` — deterministic vertical-card geometry.
- `src/post_generator/__main__.py` — the `post-generator build` CLI.
- `tests/` — four+1 suite + `test_post` coverage (single vs thread, sequence chain, image-as-metadata, platform).
- `iii_quality_contract.md` — the review/accuracy contract (wired via the `iii/` wrapper; not in-producer).

## Doctrine
Never edit `canvas_std` (firewall). Profile + platform table stay producer-side. The producer emits a conformant object
+ metadata; it does not render or score itself (quality → III; pixels → ComfyUI). Pattern:
`what/context/context_canvas_producer_pattern.md`.
