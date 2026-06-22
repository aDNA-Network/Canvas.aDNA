---
type: skill
skill_type: agent
created: 2026-06-21
updated: 2026-06-21
status: active
category: development
trigger: "Building a new in-vault canvas producer (a generator that turns a domain spec into a v2.0.0 aDNA-Native .canvas) on canvas_std"
last_edited_by: agent_stanley
tags: [skill, canvas, producer, scaffold, canvas_std, factory, palette]
---

# Skill: Build a Canvas Producer

Turn a domain spec into a v2.0.0 **aDNA-Native** `.canvas` by cloning `what/production/_scaffold/` and filling in the
four-step pipeline. Proven 5× (`brief_consumer`, `deck_generator`, `document_generator`, `diagram_generator`,
`comic_generator`). This skill is the **runbook**; `what/context/context_canvas_producer_pattern.md` is the **pattern**
(principles + worked mappings). Graduated in Operation Palette P1.

## When to use

A new 2D output layer needs a producer (letter, post, poster, one-pager, résumé, newsletter, …). **Not** for: editing
the Standard (LIP via `adr_003`); image rendering (ComfyUI); web (Astro); render/pixel scoring (`canvas_presentation`,
PT-P5). If you'd need a new baseline field or enum value, stop — that's a LIP, not a producer.

## Inputs

- A domain you can model as plain data (a `model.py` dataclass) + an example spec.
- The installed Standard: `what/code/canvas_std/` (provides the `adna-canvas-std` import + the `canvas-std` CLI).
- A ratified producer name (`<name>_generator`) and a producer-side profile name.

## Procedure

### 1. Clone the scaffold
```sh
cd what/production
cp -R _scaffold <name>_generator && cd <name>_generator
git mv src/__producer__ src/<name>_generator
grep -rl __producer__ . | xargs sed -i '' 's/__producer__/<name>_generator/g'   # macOS sed; Linux: sed -i
```
Update `pyproject.toml` (`name`, description, keywords, `[project.scripts]`) and clear the `TODO(clone)` markers as you
go. Pick the exemplar closest to your domain: `deck_generator` (single-surface), `document_generator` (multi-page),
`diagram_generator` (smallest/cleanest).

### 2. `model.py` — substrate-free domain model
Dataclasses + `load_input()` (YAML/JSON → model). **Import no `canvas_std` in this file** — `test_model_neutrality.py`
AST-guards it. This is the only canvas-agnostic layer.

### 3. `consume.py` — assemble the source contract, then enrich
The canonical four steps (see the scaffold `consume.py` for the exact shape):
1. build `source = {"name": id, "version": v, "nodes": [...], "edges": [...]}` — interior nodes use **baseline types**
   (`text`/`file`/`group`/`link`); a containing `group` node is the **single canonical surface**.
2. `doc = to_canvas(source)` (sets explicit edge `toEnd` + `_reserved.sync`).
3. set any Advanced fields post-hoc on the node dict (e.g. `isStartNode` on page 0).
4. enrich `doc["metadata"]["frontmatter"]["_reserved"]`: `adna_version="2.0.0"`, `conformance_level="adna_native"`,
   `component_types` (per node `{class, semantic_type?, degrades_to, qualities?}`), `semantic_bindings={"profile": "<name>"}`
   (bare, producer-side), `panel_link={"edges":{eid:{kind}}, "regions":{gid:{flow,pagination,extent?,surface?}},
   "surfaces":[{id,role}]}`, `context_object={"id","version","refs"}`.

Domain → canvas shapes that worked: **single-surface** (brief/deck/diagram) — one `group` surface + interior nodes;
**multi-page** (document/comic) — root `group` → page/spread `group`s each with a `region` (`extent.unit: pages`) →
interior nodes, `sequence` across pages (acyclic, `isStartNode` on page 0), `reading_order` within; **media interior** —
an `image`-class node whose payload (the prompt) rides in `qualities.image_prompt` (the producer never renders).

### 4. `tests/` — the "four+1" suite (remove the module-level skips)
`test_conformance` (`validate(doc, ADNA_NATIVE) == []`; `validate_suite` `meets_declared`; one canonical surface;
`component_types` keys ⊆ node ids) · `test_roundtrip` (`compute_sync_hash` stable; cyclic case if the domain cycles) ·
`test_degradation` (`degradation_report` all-True; `strip` → CORE/EXTENDED valid; no out-of-enum baseline leaked) ·
`test_components` (`degrades_to` ∈ baseline) · a domain-coverage test · `test_model_neutrality` (the AST guard). Add a
worked example to `examples/`.

### 5. venv + run
```sh
python3 -m venv .venv
.venv/bin/pip install -e ../../code/canvas_std && .venv/bin/pip install pyyaml
PYTHONPATH=src .venv/bin/python -m pytest tests -q          # all green
.venv/bin/ruff check src tests                              # clean
.venv/bin/<name>_generator build examples/<x>.yaml examples/<x>.canvas
.venv/bin/canvas-std validate examples/<x>.canvas           # -> "adna_native [OK]"
```

### 6. Firewall + quality gate
- **Firewall (load-bearing):** `git diff --stat -- what/code/canvas_std/` MUST be empty. A producer never edits the
  Standard — if you think you must, file a LIP (`adr_003`).
- **Quality:** route the example through the `iii/` wrapper (target 0 High / 0 Med); ship an `iii_quality_contract.md`
  (a contract, not an engine — the producer emits the metadata a review needs and does not score itself, C8).

## Conformance vocabulary (do not fight the enums — verified against `canvas_std/{reserved,schema,conformance}.py`)

- `BASELINE_TYPES = {text, file, group, link}` — every `degrades_to` is one of these.
- `PL_EDGE_KINDS = {sequence, reading_order, adjacency, dependency}` — **only `sequence` is acyclicity-checked**: use it
  for strictly linear chains (slide/page/thread order, gantt); use `dependency`/`reading_order`/`adjacency` for graphs
  that can cycle.
- `PL_EXTENT_UNITS = {words, pages, slides}` — omit `extent` when none fits; a non-paginated region sets
  `pagination: "none"` (AT-1).
- `VALID_SHAPES` is small (no rect/round/stadium) — carry rich shape vocab in `qualities.shape`, keep baseline
  `type: "text"`, never set baseline `styleAttributes.shape`.
- **A-5:** exactly one `surfaces[]` entry with `role: "canonical"`, and its `id` must resolve to a node.
- `surface` labels are an **open, producer-defined vocabulary** (AT-2) — validators never reject unknown tokens.

## Anti-patterns

1. Editing `canvas_std` to make a producer pass (firewall — fix the producer or file a LIP).
2. Setting baseline `styleAttributes.shape` from rich vocab (fails E-2/D-2 — use `qualities.shape`).
3. Tagging a cyclic graph's edges `sequence` (fails A-5 acyclicity — use `dependency`/`reading_order`).
4. Importing an archived/quarry package instead of porting the logic (couples to a PT-P5 relocation).
5. Rendering or scoring inside the producer (violates C8 — emit metadata; wire to III/ComfyUI/`canvas_presentation`).
6. Registering a profile in `canvas_std.schema` (touches the immutable substrate — keep profiles producer-side).
7. Placing the producer anywhere but `what/production/<name>/` (breaks the `../../code/canvas_std` editable install).

## Outputs

A new `what/production/<name>_generator/` — green "four+1" suite, `ruff` clean, a worked example validating
`adna_native [OK]` and degrading to a valid Obsidian canvas, an `iii_quality_contract.md`, and `canvas_std` git-diff 0.

## Verification

`PYTHONPATH=src .venv/bin/python -m pytest tests -q` all green · `canvas-std validate examples/<x>.canvas` →
`adna_native [OK]` · `degradation_report(doc)` all-True · `git diff --stat -- what/code/canvas_std/` empty · structural
`iii/` review 0 High / 0 Med.

## Related
- Pattern: `what/context/context_canvas_producer_pattern.md` · Scaffold: `what/production/_scaffold/`
- Standard: `what/code/canvas_std/src/canvas_std/{reserved,schema,conformance}.py` · Specs: `what/specs/spec_*.md`
- Decisions: [[adr_004_production_code_layout]] (two-shelf) · [[adr_003_standard_governance]] (LIP path)
