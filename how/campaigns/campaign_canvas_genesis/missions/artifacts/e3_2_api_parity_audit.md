---
type: artifact
artifact_class: audit
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
mission: mission_e3_2_canvas_core_shim
campaign: campaign_canvas_genesis
tags: [artifact, audit, keystone, e3, parity, canvasforge, canvas_std]
---

# E3.2 — API-parity audit: `canvas_std` covers the `canvas_core` floor (constants-only scope)

**Purpose** (mission objective 1): before repointing, prove `canvas_std` covers the reference surface CanvasForge
consumes, at the operator-chosen **constants-only** scope (the 10 `VALID_*` enums + `TYPE_MAPPING` + `EDGE_TYPE_MAPPING`).
Round-trip *functions* are out of scope this mission (they repoint after the E3.3 parity gate proves behavioral
equivalence).

## Where the floor lives (corrects the exploration summary)

The floor constants in CanvasForge are **`CanvasBuilder` class attributes**, not module-level constants:
`CanvasForge.aDNA/what/code/canvas_core/core.py` lines 46–117, inside `class CanvasBuilder:`. They are read via
`self.VALID_*` / `self.TYPE_MAPPING` in methods (e.g. core.py:296, 396, 753, 771, 778, 781, 818) and via
`CanvasBuilder.VALID_*` in tests (test_core.py:41–46). In `canvas_std` the same names are **module-level** in
`canvas_std.schema`. Repoint mechanism: reassign each `CanvasBuilder` class attribute to the corresponding
`canvas_std.schema` object — `self.X` and `CanvasBuilder.X` both follow, with object identity preserved.

## Coverage + byte-identity (the load-bearing check)

| Symbol | CanvasForge `CanvasBuilder` | `canvas_std.schema` | Value-identical? |
|--------|------------------------------|----------------------|------------------|
| `VALID_NODE_TYPES` | core.py:76 | schema.py:18 | ✅ |
| `VALID_SHAPES` | core.py:46 | schema.py:20 | ✅ |
| `VALID_BORDERS` | core.py:58 | schema.py:24 | ✅ |
| `VALID_TEXT_ALIGN` | core.py:59 | schema.py:26 | ✅ |
| `VALID_COLORS` | core.py:60 | schema.py:28 | ✅ |
| `VALID_PATH_STYLES` | core.py:61 | schema.py:30 | ✅ |
| `VALID_ARROWS` | core.py:62 | schema.py:32 | ✅ |
| `VALID_PATHFINDING` | core.py:74 | schema.py:45 | ✅ |
| `VALID_SIDES` | core.py:75 | schema.py:47 | ✅ |
| `VALID_ENDS` | core.py:77 | schema.py:49 | ✅ |
| `TYPE_MAPPING` (8 keys) | core.py:80 | schema.py:60 | ✅ |
| `EDGE_TYPE_MAPPING` (5 keys) | core.py:92 | schema.py:72 | ✅ |

Frozensets compare order-independently; the two mappings match key-for-key and value-for-value. **All 12 are
value-identical** — expected, since `canvas_std.schema` is the verbatim E0.2 port of this exact block. **No gaps;
no `canvas_std`-side fix required before repointing.**

## Correctness checks

- **Mutation**: `grep` across `CanvasForge.aDNA/what/code` (ex-tests) for in-place writes to `TYPE_MAPPING` /
  `EDGE_TYPE_MAPPING` (subscript-assign / `.update` / `.setdefault` / `.pop` / `del`) → **NONE**. The mappings are
  read-only at runtime, so sharing `canvas_std`'s dict objects across the seam is safe (no defensive copy needed).
- **External class access**: no producer reads `CanvasBuilder.VALID_*` / `.TYPE_MAPPING` at class level (tests do —
  that's coverage). All producer use is via `self.` on an instance.
- **Module-level imports of the floor from `canvas_core.core`**: NONE (only `VALID_ROLES` — a CF-specific role
  enum in `config_substrate.py`, not a floor symbol — is imported by producers; unaffected).
- **`canvas_std`-only names** (`SEMANTIC_PROFILES` / `EDGE_PROFILES` / `*_REQUIRED_FIELDS`): not referenced in
  CanvasForge → not part of this repoint.

## Import mechanism (operator decision: editable install)

`adna-canvas-std` installed editable into a gitignored py3.12 venv at `CanvasForge.aDNA/what/code/.venv`
(`pip install -e Canvas.aDNA/what/code/canvas_std`, zero deps). Confirmed: `canvas_std.schema.is_floor_loaded()`
→ `True`, `STANDARD_VERSION` → `2.0.0`. Test-env extras installed: `pytest pytest-timeout pyyaml pillow`
(`pillow` was the only collection-blocking dep; all 28 collection errors were `No module named 'PIL'`).

## Differential parity baseline (pre-shim)

Canonical suite `pytest canvas_core/tests/ canvas_comic/tests/ tests/test_federation_validation.py`:
**897 passed · 3 failed · 3 skipped** (4.23s). The 3 failures are `test_gdoc_export.py::TestImageFidelity`
(Drive image-upload fidelity — pre-existing, env-limited, unrelated to the floor). **Parity criterion for the
shim: the post-shim run must reproduce this set exactly** (897 passed, same 3 gdoc failures, 3 skipped) — no new
failure, no regression in the 897.

## Verdict

**PASS — no blockers.** `canvas_std` fully covers the constants-only reference surface with byte-identity; the
repoint is a safe class-attribute reassignment, reversible by revert. Proceed to objective 2 (install the shim).
