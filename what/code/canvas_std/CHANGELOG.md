# Changelog — adna-canvas-std

All notable changes to the reference implementation and the **aDNA Canvas Standard** it implements.

**Two version scopes** (they advance independently):

- **Standard version** (`STANDARD_VERSION`) — heads each release entry below. History:
  **2.0.0** (Keystone) → **2.0.1** (LIP-queue errata B1/B2/B3) → **2.0.2** (Atelier errata AT-1/AT-2) →
  **[2.1.0 — reserved]** → **2.2.0** (Armature — the leg-3 interaction layer).
  The **2.1.0 slot is reserved** for the in-review **LIP-0008** (A-5 "derived surface = pure metadata" relaxation):
  the Standard jumped 2.0.2 → 2.2.0 at Armature, so 2.1.0 is held pending LIP-0008's disposition
  (see `what/decisions/lip_queue_disposition.md`; reconciled in Operation Beacon Phase B4).
- **Package version** (`__version__`, currently `0.1.0`) — the pip package; advances on its own cadence. The
  `## [0.1.0]` entry below is the **package** skeleton (Keystone E0.1), not a Standard release.

## [2.2.0] — 2026-06-23 (Operation Armature P2 — I-* wired into the harness + the interaction_version cut)

The **first deliberate edit to `canvas_std` since Operation Keystone** — bounded to the two purposes `adr_007`
authorizes (the firewall lifts only for P2; P0/P1/P3 stay git-diff 0). Builds on Standard v2.0.2 (the AT-1/AT-2
errata cut). The P2 exit gate is **full-regression-green**, not git-diff 0 (`adr_007` §3).

### Added (I-* interaction conformance — spec_interface_surface §9.1)
- `reserved.py`: **`validate_interaction(reserved, doc)`** — the `I-1`/`I-2`/`I-3` family for the leg-3
  `_reserved.interaction` overlay (well-formed overlay; per-affordance anchor resolution + closed `kind` enum +
  `options`-iff-`choice`; per-response declared-affordance + kind-consistent value). **Doc-path only** (no
  `ContextGraph` import — the dependency stays one-way); reuses the node/anchor substrate `validate_reserved` already
  builds and does **not** re-run `validate_anchors` (no double A-5). Adds `AFFORDANCE_KINDS` + a 2-part-tolerant
  `_INTERACTION_SEMVER` (distinct from the 3-part `_SEMVER`).
- `validate.py`: dispatch `validate_interaction` on the aDNA-Native path (after `validate_reserved`); surfaces through
  `validate_suite` + the `canvas-std` CLI with no further wiring. Re-exported from `__init__`.
- `tests/fixtures/adna_interaction.canvas` (all four affordance kinds; one label-anchored affordance) + a manifest
  entry; `tests/test_interaction.py` (valid e2e; I-2 orphan; I-3 bad value; D-1 strip→Core; the no-double-A-5 guard;
  the CLI validates the golden). **Suite: 105 passed / 10 skipped; `ruff` clean.**
- The consumer `canvas_context.validate_interaction_block` becomes a **thin delegate** to this function (one source of
  truth); **no producer regression** (brief 10 · deck 16 · document 37 · diagram 36 · comic 87 · letter 17 · post 20).

### Standard release v2.2.0 CUT 2026-06-23 (operator-authorized at the P1→P2 gate, adr_007)
- `interaction_version 1.0` graduated into a Standard version. Bumped `2.0.2 → 2.2.0` at: `STANDARD_VERSION`
  (`__init__.py`), schema `title` + `x-standard-version` (**kept `$id`** — structural schema unchanged), `conformance.py`
  (×3), `test_smoke.py` (×2) + `test_conformance.py` (×1), the 9 `what/specs/spec_*.md` `standard_version` frontmatters
  + the `spec_federation_contract` example. Flipped the `spec_conformance_suite §4.1` + `spec_interface_surface §9.1/§10`
  forward-pointers ("forward-pointed / deferred" → "implemented in `canvas_std`"). **v2.1.0 reserved for in-review LIP-0008.**
- Fixtures' `_reserved.adna_version` stays `2.0.0` (a 2.0.0-authored canvas remains valid under the 2.2.0 validator —
  the interaction layer is additive; D-1..D-3 round-trip-to-baseline hold on the interaction golden).

## [2.0.2] — 2026-06-21 (Atelier errata AT-1/AT-2 — Standard v2.0.2, editorial PATCH)

Editorial clarifications drained from Operation Atelier (`adr_003 §2` maintainer-discretion, no LIP) — **no
validator-behavior change**; both make explicit what the reference implementation already did. *(Back-filled in
Operation Beacon B3/R2.2 — the AT-1/AT-2 cut originally bumped version strings only, leaving this entry missing.)*

### Clarified (spec errata — `spec_panel_link_semantics §4/§5.2/§6`)
- **AT-1** — `extent` is **OPTIONAL**: a non-paginated single-surface region (`pagination: "none"`, e.g. a
  diagram/graph) legitimately omits it. No `graph`/`nodes` extent unit added (a node-graph is sized by content,
  not paged).
- **AT-2** — the region `surface` subclass label is an **OPEN, producer-defined vocabulary**. No enum added (a
  closed enum would force a LIP per new producer type).
- Doc-comments in `reserved.py`; 2 regression tests (`test_anchors.py::test_at1_*` / `test_at2_*`). Validator
  logic untouched (`reserved.py` diff = comments only).

### Standard release v2.0.2 CUT 2026-06-21 (operator-authorized)
- Bumped `2.0.1 → 2.0.2` mirroring the v2.0.1 sites (`STANDARD_VERSION`, schema `title` + `x-standard-version`
  [**kept `$id`** — structural schema unchanged], `conformance.py`, `test_smoke`/`test_conformance`, the 7 spec
  `standard_version` frontmatters + the `spec_federation_contract` example). Fixtures' `_reserved.adna_version`
  stays `2.0.0`. **Suite: `pytest` 82 passed / 10 skipped; `ruff` clean.** Errata queue B1–B4 + AT-1/AT-2 fully drained.

## [2.0.1] — 2026-06-20 (LIP queue errata — B1 + B3 + B2; Standard v2.0.1)
### Added (LIP queue B1 — anchor-layer validator)
- `reserved.py`: `validate_anchors(reserved, node_ids)` — the `spec_panel_link_semantics` §5.3/§6 anchor layer
  (`naming_convention.label_form` ∈ {descriptive,legacy} + string `migration_rule`; `orphan_detector.mode` ∈
  {label_ref,src_cited} + `threshold` ∈ [0,1]; every `panel_link.anchors` entry + every explicit component
  anchor-reference (`qualities` key ∈ {ref,anchor,anchor_ref,cites,for}) resolves — **no orphaned anchors**).
  Wired into `validate_reserved`. Constants `NC_LABEL_FORMS` / `OD_MODES` / `ANCHOR_REF_KEYS`. The orphan-*traversal*
  engine stays producer-side (C8).
- `tests/fixtures/adna_anchored.canvas` (valid) + `adna_orphan_anchor.canvas` (negative — orphan ref) + manifest
  entries; `tests/test_anchors.py` (12 unit + e2e). **Suite: `pytest` 70 passed / 10 skipped; `ruff` clean.** No
  consumer regression (`document_generator` 37 / `deck_generator` 16 / `brief_consumer` 10; all 4 example canvases [OK]).
- Closes LIP-queue **B1** (Keystone handoff §B). Spec errata applied: `spec_panel_link_semantics` §5.3/§6 (anchor
  model) + §4/§5.1 (**B3** pagination-construct clarification).
- **B2 (ride-on-text, PATCH).** `spec_component_model` §4.4 registers the canonical long-form `semantic_type`
  values (`quote`/`block_quote`/`footnote`/`attribution`) on `class: text` — no new taxonomy class (Mondrian
  reduction); `reserved.py` gains the informational `LONGFORM_SEMANTIC_TYPES` registry (no validator rejects other
  values); `tests/fixtures/adna_longform_quote.canvas` + `tests/test_longform.py` lock the convention (a footnote's
  `qualities.ref` resolves via `validate_anchors`, B1). Closes LIP-queue **B2** (operator chose option (ii)).
  **Suite: `pytest` 80 passed / 10 skipped; `ruff` clean.** No consumer regression (`document_generator` 37 /
  `deck_generator` 16 / `brief_consumer` 10; all 5 example/corpus canvases [OK]).
- **Standard release v2.0.1 CUT 2026-06-20 (operator authorized).** Bumped in one shot → `STANDARD_VERSION`
  (`__init__.py`), schema `title` + `x-standard-version` (kept `$id` — structural schema unchanged),
  `conformance.py` CLI/doc strings, `test_smoke.py` (×2) + `test_conformance.py` (×1) assertions, the 7
  `what/specs/spec_*.md` `standard_version` frontmatters, and the `spec_federation_contract.md` §2.1 example, all
  `2.0.0` → `2.0.1`. (Fixtures' `_reserved.adna_version` stays `2.0.0` — a 2.0.0-authored canvas remains valid
  under the 2.0.1 validator. Spec doc *titles* name the v2.0.x line and stay as prose.)

### Added (E2.3 — publish: JSON Schema + CLI; Phase E2 complete)
- `src/canvas_std/data/adna_canvas_v2.schema.json`: the v2.0.0 JSON Schema (draft 2020-12; structural floor +
  enums + `_reserved` carrier). `conformance.json_schema()` loads it (importlib.resources). Exported.
- `conformance._cli`: the `canvas-std` CLI -- `validate <file> [--level …] [--json]` (auto-detects level from
  `_reserved.conformance_level`; exit 0/1) + `schema`. Wired via pyproject `[project.scripts]`.
- **Phase E2 (reference impl + tooling) complete -- no stubs remain.** `pytest` 46 passed / 8 skipped; `ruff`
  clean. Registry/federation registration deferred to E5 (rollout).

### Added (E2.2 — conformance corpus)
- `tests/fixtures/`: `core_only_bad_shape.canvas` (reaches Core only) + `adna_bad_reserved.canvas` (reaches
  Extended only); `manifest.json` gains `expected_level_reached` + `expected_ok`.
- `tests/test_conformance.py`: runs `validate_suite` over the corpus (level_reached / ok / degradation).
  Suite: `pytest` 46 passed / 8 skipped; `ruff` clean.

### Added (E2.1 — conformance harness)
- `conformance.py`: `validate_suite(doc, declared) -> ConformanceReport` (runs C-*/E-*/A-* at each level to find
  `level_reached`; `passed`/`failed` records; D-1..D-3 `degradation`). `ConformanceReport.ok` / `meets_declared`.
- `test_smoke.py`: `validate_suite` live; only the `canvas-std` CLI (`_cli`) remains stubbed.

### Added (E1.5 — strip + degradation; Phase E1 complete)
- `validate.py`: `strip(doc)` (deep-copy, removes `metadata.frontmatter._reserved` — the C4 op; original
  untouched) + `degradation_report(doc)` (D-1 Core-valid · D-2 Extended-valid · D-3 no `_reserved`). Exported.
- `test_fixtures.py`: retired the `validate`/`strip` `xfail` markers (behavior now real). `__init__.py` reordered
  (re-exports before constants) for ruff. **Full suite: `pytest` 30 passed / 4 skipped; `ruff` clean.**
- **Phase E1 (reference engine) complete.** Remaining stubs: `validate_suite` (E2.1), `canvas-std` CLI (E2.3).

### Added (E1.4 — _reserved validators / A-* checks)
- `reserved.py`: `validate_reserved(reserved, doc)` (A-2 adna_version/conformance_level, A-6 sync/16-hex hash) +
  `validate_component_types` (§7: keys resolve, class ∈ 14-class taxonomy, degrades_to ∈ baseline),
  `validate_panel_link` (§6: kinds/ids resolve, enums, exactly-one-canonical-surface, sequence acyclicity),
  `_validate_semantic_bindings` / `_validate_context_object`. Constants: `COMPONENT_CLASSES`, `PL_*`.
- `validate()` aDNA-Native branch wired to `validate_reserved` (requires a populated `_reserved`). The
  `adna_native` validate-xfail in `test_fixtures.py` now PASSES.

### Added (E1.3 — diff / merge / preserve_positions)
- `roundtrip.py`: `diff(a, b)` (structured topology/position diff), `preserve_positions(target, reference)` (G1),
  `merge(source, canvas, strategy)` (three-way: canvas owns topology + positions, source owns semantics;
  `yaml_wins`/`canvas_wins`; conflicts flagged as records, not exceptions). `preserve_positions` exported.
- `test_smoke.py`: `diff`/`merge` removed from the stub list (only `strip` remains) + a diff liveness check.

### Added (E1.2 — round-trip converters)
- `roundtrip.py`: `compute_sync_hash` (16-hex SHA-256 over sorted node ids + `fromNode->toNode` pairs),
  `to_canvas` (forward source->view: applies the `lattice` profile, explicit `toEnd`, injects `_reserved.sync`;
  default geometry — layout is producer-side), `from_canvas` (advisory view->source draft; topology + best-effort
  semantic-type recovery; `_draft: true`). `diff`/`merge` remain stubbed (E1.3).
- `test_smoke.py`: `to_canvas`/`from_canvas`/`compute_sync_hash` removed from the stub list + a round-trip liveness test.

### Added (E1.1 — validate Core/Extended)
- `validate.py`: implemented `validate(doc, level)` Core (C-1..C-5) + Extended (E-1..E-4) checks against the
  KEEP floor; monotone (aDNA-Native ⊃ Extended ⊃ Core). C-4 = explicit `toEnd` required (omitted → reject).
  aDNA-Native delegates A-* to `reserved.validate_reserved` (NotImplementedError until E1.4). `strip` stays E1.5.
- `test_smoke.py`: `validate` removed from the NotImplemented-stub list + a liveness check added. The core /
  extended / negative `validate` xfails in `test_fixtures.py` now PASS.

### Added (E0.3 — golden fixtures + harness)
- `tests/fixtures/`: `core_minimal.canvas`, `extended_styled.canvas`, `adna_native.canvas` (populated `_reserved`
  + `_lattice_meta`; doubles as the degradation case), `invalid_missing_arrow.canvas` (negative), `manifest.json`.
- `tests/test_fixtures.py`: now-checkable assertions (JSON shape, required fields, declared level) + `validate`/
  `strip` assertions marked `xfail(strict=False)` until E1 (they auto-flip to PASS when E1 lands). **Phase E0 complete.**

### Added (E0.2 — verbatim KEEP floor)
- `schema.py`: the 10 `VALID_*` enums, `NODE_REQUIRED_FIELDS`/`EDGE_REQUIRED_FIELDS`, and the built-in `lattice`
  semantic profile (`TYPE_MAPPING` 8 entries + `EDGE_TYPE_MAPPING` 5 entries) — transcribed verbatim from
  `p1_fork_baseline` §3. `SEMANTIC_PROFILES`/`EDGE_PROFILES` registries (new profiles register additively).
- Smoke test: floor-loaded assertion + lattice-profile spot-checks + token-within-§6-enum degradation-safety check.

## [0.1.0] — 2026-06-13 (Operation Keystone E0.1)
### Added
- Package skeleton: `pyproject.toml` (hatchling, Python ≥3.11, src-layout), MIT `LICENSE`, `Makefile` (test/lint).
- Public API stubs matching the ratified specs: `schema`, `validate`, `roundtrip`, `reserved`, `conformance`.
- `STANDARD_VERSION = "2.0.0"`; `to_canvas`/`from_canvas` aliases baked in.
- Smoke test asserting the API surface + Standard version.

### Notes
- Behavior is not implemented (stubs raise `NotImplementedError`). E0.2 ports the KEEP floor; E1 implements.
