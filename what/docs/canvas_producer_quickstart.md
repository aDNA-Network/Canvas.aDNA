---
type: context
created: 2026-06-30
updated: 2026-06-30
status: active
last_edited_by: agent_mondrian
tags: [docs, quickstart, producer, canvas_std, canvas, adoption]
---

# Producer Quickstart — build a canvas producer in ~15 minutes

A **producer** turns a domain spec (a deck outline, a letter, a diagram) into a conformant aDNA `.canvas` on
top of `canvas_std`. It **never renders and never scores** — it emits a validated canvas + the metadata a
renderer or a quality review needs. Proven 7× in-vault (`brief` · `deck` · `document` · `diagram` · `comic` ·
`letter` · `post`).

This is the fast path. The full runbook is [`how/skills/skill_canvas_producer_build.md`](../../how/skills/skill_canvas_producer_build.md);
the design principles are [`what/context/context_canvas_producer_pattern.md`](../context/context_canvas_producer_pattern.md).

## Prerequisites

- Python 3.10+.
- The reference implementation: `what/code/canvas_std/` (provides the `adna-canvas-std` import + the `canvas-std` CLI).
- A domain you can model as plain data, and one example spec.

## 1 — Clone the scaffold

```sh
cd what/production
cp -R _scaffold <name>_generator && cd <name>_generator
git mv src/__producer__ src/<name>_generator
grep -rl __producer__ . | xargs sed -i '' 's/__producer__/<name>_generator/g'   # macOS sed; Linux: sed -i
```

Pick the exemplar closest to your domain: **`deck_generator`** (single surface), **`document_generator`**
(multi-page), **`diagram_generator`** (smallest / cleanest).

## 2 — The four-step pipeline

1. **`model.py`** — a substrate-free domain model (dataclasses + `load_input()`). **Import no `canvas_std`
   here** — a `test_model_neutrality.py` AST-guards it. This is the only canvas-agnostic layer.
2. **`consume.py` — build the source contract.** `source = {"name", "version", "nodes": [...], "edges": [...]}`;
   interior nodes use **baseline types** (`text`/`file`/`group`/`link`); a containing `group` node is the
   **single canonical surface**.
3. **`consume.py` — convert + enrich.** `doc = to_canvas(source)`, then fill
   `doc["metadata"]["frontmatter"]["_reserved"]`: `adna_version` · `conformance_level="adna_native"` ·
   `component_types` (per node `{class, degrades_to, qualities?}`) · `semantic_bindings={"profile": "<name>"}` ·
   `panel_link={edges, regions, surfaces}` · `context_object={id, version, refs}`.
4. **`tests/` — the "four + 1" suite.** `test_conformance` (`validate(doc, ADNA_NATIVE) == []`) ·
   `test_roundtrip` (`compute_sync_hash` stable) · `test_degradation` (`degradation_report` all-True; `strip` →
   Core/Extended valid) · `test_components` (`degrades_to` ∈ baseline) · a domain-coverage test · the
   model-neutrality guard. Add a worked example to `examples/`.

## 3 — Run it

```sh
python3 -m venv .venv
.venv/bin/pip install -e ../../code/canvas_std && .venv/bin/pip install pyyaml
PYTHONPATH=src .venv/bin/python -m pytest tests -q          # all green
.venv/bin/<name>_generator build examples/<x>.yaml examples/<x>.canvas
.venv/bin/canvas-std validate examples/<x>.canvas          # → "adna_native [OK]"
```

## Conformance vocabulary — don't fight the enums

- `BASELINE_TYPES = {text, file, group, link}` — every `degrades_to` is one of these.
- `PL_EDGE_KINDS = {sequence, reading_order, adjacency, dependency}` — **only `sequence` is acyclicity-checked**
  (use it for strictly linear chains; use `dependency`/`reading_order`/`adjacency` for anything that can cycle).
- `PL_EXTENT_UNITS = {words, pages, slides}` — omit `extent` when none fits; a non-paginated region sets
  `pagination: "none"`.
- `VALID_SHAPES` is small — carry rich shape vocab in `qualities.shape`, keep the baseline `type: "text"`.
- **A-5:** exactly one `surfaces[]` entry with `role: "canonical"`, and its `id` must resolve to a node.
- `surface` labels are an **open, producer-defined vocabulary** — validators never reject unknown tokens.

## The two rules that never bend

- **Firewall (two-shelf, ADR-004):** a producer **never edits `what/code/canvas_std/`**. Verify
  `git diff --stat -- what/code/canvas_std/` is empty at every step. If you think you need a new baseline field
  or enum, **stop — that's a LIP** (`adr_003`), not a producer change.
- **No rendering, no scoring inside the producer.** Emit metadata; wire quality to the `iii/` review wrapper and
  pixels to ComfyUI / `canvas_presentation`.

## Common traps

1. Editing `canvas_std` to make a producer pass → fix the producer or file a LIP.
2. Setting baseline `styleAttributes.shape` from rich vocab → use `qualities.shape`.
3. Tagging a cyclic graph's edges `sequence` → use `dependency`/`reading_order`.
4. Importing an archived/quarry package instead of porting the logic → couples you to a relocation.
5. Registering a profile in `canvas_std.schema` → keep profiles producer-side.

## Done when

A new `what/production/<name>_generator/` with a green "four + 1" suite, `ruff` clean, a worked example that
validates `adna_native [OK]` and degrades to a valid Obsidian canvas, an `iii_quality_contract.md`, and
`canvas_std` git-diff 0.
