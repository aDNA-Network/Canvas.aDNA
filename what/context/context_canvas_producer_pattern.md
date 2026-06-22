---
type: context
subtype: context_guide
created: 2026-06-21
updated: 2026-06-21
status: active
last_edited_by: agent_stanley
context_version: "1.0"
token_estimate: ~2600
quality_score: 4.2
signal_density: 4
actionability: 5
coverage_uniformity: 4
source_diversity: 4
cross_topic_coherence: 4
freshness_category: stable
tags: [context, canvas, producer, pattern, consume, reserved, guide, atelier, keystone]
---

# Canvas Producer Pattern

How to build a new in-vault producer on the `canvas_std` reference impl — a generator that turns a domain spec into a
v2.0.0 **aDNA-Native** `.canvas`. The pattern is proven **5×**: `brief_consumer`, `deck_generator`,
`document_generator` (Keystone E4) + `diagram_generator`, `comic_generator` (Operation Atelier A1/A2). Use it for any
future canvas output layer (poster, letter, post, …).

## Key Principles

1. **Two-shelf firewall.** `what/code/canvas_std/` is the immutable Standard; producers live on `what/production/` and
   depend on the *installed* `adna-canvas-std`. A producer NEVER edits `canvas_std` — verify `git diff --stat --
   what/code/canvas_std/` is empty at every gate. (ADR-004.)
2. **One pipeline, every producer.** Substrate-free domain model → `consume.py` assembles a `canvas_std` **source
   contract** → `to_canvas(source)` → enrich `_reserved` to aDNA-Native. Same four steps every time.
3. **Substrate-neutral model layer.** `model.py` (+ any ported content/logic modules) import **no** `canvas_std` —
   AST-guard it with a `test_model_neutrality.py`. Only `consume.py`/`panels.py`/`blocks.py` touch the substrate.
4. **Specify contracts, not engines (C8).** Quality review stays in III (via the `iii/` wrapper); image generation
   stays in ComfyUI; render/scoring stays in `canvas_presentation` (PT-P5). A producer emits a conformant *object* +
   the metadata those engines consume — it does not score or render itself.
5. **Profiles are producer-side.** Declare a bare `{"profile": "<name>"}` in `_reserved.semantic_bindings`. Do NOT
   register a profile as a built-in in `canvas_std.schema` (that touches the immutable substrate → a LIP).
6. **Quarry, don't depend.** When porting from legacy/archived code, copy the canvas-agnostic logic in; never import the
   archived package or depend on a PT-P5 relocation.

## Recommendations

**Package shape (clone `deck_generator` for single-surface, `document_generator` for multi-page):**
```
what/production/<name>/
  pyproject.toml        # name "<name>"; deps ["adna-canvas-std","pyyaml>=6"]; [project.scripts] <name>="<name>.__main__:main"; pytest pythonpath=["src"]; ruff line-length 100
  README.md  AGENTS.md  iii_quality_contract.md  .gitignore   # .gitignore: .venv/ __pycache__/ *.egg-info/ .pytest_cache/ .ruff_cache/ *.pyc
  src/<name>/  model.py  [domain builders].py  layout.py  consume.py  __main__.py  __init__.py
  examples/  <worked>.yaml + <worked>.canvas   tests/  conftest.py + the "four+1" suites
```

**The `consume.py` contract (verbatim shape across all 5 producers):**
1. assemble `source = {"name": id, "version": v, "nodes": [...], "edges": [...]}` — nodes are
   `{"id","type":"group"|"text"|"file"|"link","text"/"label"/"file":...,"x","y","width","height"}`; a containing
   `group` node is the **single canonical surface**.
2. `doc = to_canvas(source)` — sets explicit edge `toEnd` + `_reserved.sync`.
3. set Advanced fields post-hoc on the node dict (e.g. `isStartNode` on the first page).
4. enrich `doc["metadata"]["frontmatter"]["_reserved"]`: `adna_version="2.0.0"`, `conformance_level="adna_native"`,
   `component_types` (per node: `{class, semantic_type?, degrades_to, qualities?}`), `semantic_bindings={"profile":...}`,
   `panel_link={"edges":{eid:{kind}}, "regions":{gid:{flow,pagination,extent?,surface?}}, "surfaces":[{id,role}]}`,
   `context_object={"id","version","refs"}`.

**Conformance vocabulary (verified against `canvas_std/reserved.py` + `schema.py`):**
- `BASELINE_TYPES = {text, file, group, link}` — every `degrades_to` must be one of these.
- `PL_EDGE_KINDS = {sequence, reading_order, adjacency, dependency}` — **only `sequence` is acyclicity-checked**, so
  use `sequence` only for strictly linear order (slide/page chains, gantt); use `dependency`/`reading_order` for
  graphs that can cycle (flowchart, state machine, panel grids).
- `PL_EXTENT_UNITS = {words, pages, slides}` — there is no `panels`/`graph` unit; omit `extent` when none fits.
- `VALID_SHAPES` is small and does NOT include `rect/round/stadium` — carry rich shape vocab in
  `qualities.shape`, keep the baseline node `type:"text"`, and never set baseline `styleAttributes.shape`.
- **A-5:** exactly one `surfaces[]` entry with `role:"canonical"`, and its `id` must resolve to a node.

**The "four+1" test suite (mirror the existing producers):** `test_conformance` (validate ADNA_NATIVE + one canonical
surface + component_types keys ⊆ node ids) · `test_roundtrip` (`compute_sync_hash` stable; include a cyclic case if the
domain can cycle) · `test_degradation` (D-1/D-2/D-3 all True; strip → Core/Extended valid; assert no out-of-enum
baseline leaked) · `test_components` (classes ∈ `COMPONENT_CLASSES`, `degrades_to` ∈ `BASELINE_TYPES`) · a
domain-coverage test + `test_model_neutrality` (no `canvas_std` import below `consume`).

**venv recipe (per-producer, gitignored):** `python3 -m venv .venv && .venv/bin/pip install -e ../../code/canvas_std
&& .venv/bin/pip install pyyaml`; run `PYTHONPATH=src .venv/bin/python -m pytest tests -q`. Installing `canvas_std`
editable provides both the `adna-canvas-std` import and the `canvas-std` CLI (`canvas-std validate <file>` →
`adna_native [OK]`).

## Examples / Snippets

Minimal enrichment (from `diagram_generator/consume.py`):
```python
source = {"name": d.id, "version": d.version, "nodes": nodes, "edges": edges}
doc = to_canvas(source)
reserved = doc["metadata"]["frontmatter"]["_reserved"]
reserved["adna_version"] = "2.0.0"
reserved["conformance_level"] = "adna_native"
reserved["component_types"] = component_types          # node id -> {class, semantic_type?, degrades_to, qualities?}
reserved["semantic_bindings"] = {"profile": "diagram"} # bare, producer-side
reserved["panel_link"] = {"edges": pl_edges, "regions": {ROOT: {...}}, "surfaces": [{"id": ROOT, "role": "canonical"}]}
reserved["context_object"] = {"id": d.id, "version": d.version, "refs": list(d.refs)}
```

Domain → canvas mappings that worked:
- **Single-surface graph** (diagram): native nodes+edges canonical (one `group` surface) + a derived `code` node for a
  regenerable source (e.g. Mermaid). Edges `dependency` (cycles OK).
- **Multi-page** (document, comic): a root `group` (canonical surface) → page/spread `group`s each carrying a `region`
  (`extent.unit: pages`) → interior nodes; `sequence` across pages (acyclic, `isStartNode` on page 0), `reading_order`
  within, `adjacency` for spatial neighbours.
- **Media interior** (comic image panels): an `image`-class `file`/`text` node; producer-specific payload (the image
  prompt) rides in `qualities.image_prompt` — the producer never renders; ComfyUI owns pixels.

## Anti-Patterns

1. **Editing `canvas_std` to make a producer pass.** The firewall is load-bearing; fix the producer or file a LIP.
2. **Setting baseline `styleAttributes.shape` from rich vocab** → fails E-2/D-2. Use `qualities.shape`.
3. **Tagging a cyclic graph's edges `sequence`** → fails A-5 acyclicity. Use `dependency`/`reading_order`.
4. **Importing the archived/quarry package** instead of porting the logic → couples to a PT-P5 relocation.
5. **Rendering or scoring inside the producer** → violates C8. Emit metadata; wire to III/ComfyUI/`canvas_presentation`.
6. **Registering a profile in `canvas_std.schema`** → touches the immutable substrate. Keep profiles producer-side.

## Sources

- Producers: `what/production/{brief_consumer,deck_generator,document_generator,diagram_generator,comic_generator}/`.
- Contract: `what/code/canvas_std/src/canvas_std/{reserved.py,schema.py,conformance.py}`; specs `what/specs/spec_*.md`.
- Campaigns: Operation Keystone (`campaign_canvas_genesis`, E4) + Operation Atelier (`campaign_canvas_production`, A1/A2).
- Decisions: [[adr_004_production_code_layout]] (two-shelf split) · [[adr_003_standard_governance]] (LIP process).
- Related context: [[context_migration_parity_methodology]] (migrating/relocating a producer) ·
  [[context_canvas_standard_doctrine]] (the Standard itself).
