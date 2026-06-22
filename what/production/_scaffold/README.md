# `_scaffold` — copy-me template for a new canvas producer

This is **not a producer** — it is the inert skeleton you clone to start a new in-vault producer on `canvas_std`.
It is excluded from the cross-producer test sweep. Full method: `how/skills/skill_canvas_producer_build.md`
(the runbook) + `what/context/context_canvas_producer_pattern.md` (the pattern). It lives at producer depth
(`what/production/<name>/`) so the `../../code/canvas_std` relative paths below stay valid on clone.

## Clone recipe

```sh
# 1. copy the skeleton (from what/production/)
cp -R _scaffold <name>_generator           # e.g. letter_generator

# 2. rename the package dir + every placeholder token
cd <name>_generator
git mv src/__producer__ src/<name>_generator
grep -rl __producer__ . | xargs sed -i '' 's/__producer__/<name>_generator/g'   # macOS sed
#   (replace __PRODUCER__ display tokens + TODO(clone) lines by hand)

# 3. make the venv + install the Standard editable (provides the adna-canvas-std import + the canvas-std CLI)
python3 -m venv .venv
.venv/bin/pip install -e ../../code/canvas_std
.venv/bin/pip install pyyaml

# 4. fill in model.py / consume.py / layout.py / tests (remove the module-level skips), then:
PYTHONPATH=src .venv/bin/python -m pytest tests -q
.venv/bin/canvas-std validate examples/<worked>.canvas      # -> "<level> [OK]"
```

## The pipeline (every producer, four steps)

1. **`model.py`** — substrate-free domain model (dataclasses + `load_*`). Imports **no** `canvas_std`
   (a `test_model_neutrality.py` AST-guards this).
2. **`consume.py`** — assemble a `canvas_std` **source contract** `{name, version, nodes, edges}`; a containing
   `group` node is the single canonical surface.
3. **`consume.py` (cont.)** — `doc = to_canvas(source)`, then enrich `doc[...]["_reserved"]`:
   `adna_version` · `conformance_level` · `component_types` · `semantic_bindings={"profile": ...}` ·
   `panel_link={edges, regions, surfaces}` · `context_object`.
4. **`tests/`** — the "four+1" suite (conformance · round-trip · degradation · components + a domain-coverage test
   + model-neutrality). Route quality through the `iii/` wrapper; never render or score inside the producer (C8).

## Conformance vocabulary (do not fight the enums)

- `BASELINE_TYPES = {text, file, group, link}` — every `degrades_to` is one of these.
- `PL_EDGE_KINDS = {sequence, reading_order, adjacency, dependency}` — **only `sequence` is acyclicity-checked**
  (use it only for strictly linear chains; use `dependency`/`reading_order` for anything that can cycle).
- `PL_EXTENT_UNITS = {words, pages, slides}` — omit `extent` when none fits (a non-paginated region sets
  `pagination: none`).
- `VALID_SHAPES` is small — carry rich shape vocab in `qualities.shape`, keep baseline `type: "text"`.
- **A-5:** exactly one `surfaces[]` entry with `role: "canonical"`, and its `id` must resolve to a node.

## Firewall

A producer **never** edits `what/code/canvas_std/`. Verify `git diff --stat -- what/code/canvas_std/` is empty at
every gate (ADR-004 two-shelf).
