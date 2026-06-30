# adna-canvas-std

Reference implementation of the **aDNA Canvas Standard v2.2.0** — the runnable tooling Canvas.aDNA ships as the
standard-bearer Platform (Option P): **validators · round-trip converters · conformance harness**.

> **Status: complete + current to Standard v2.2.0.** The reference implementation is functional — schema floor,
> validators, round-trip converters, `_reserved` validators (incl. the v2.2.0 `interaction` layer), and the
> conformance harness + `canvas-std` CLI are all live; no stubs remain. `pytest` **105 passed / 10 skipped**,
> `ruff` clean. Validated against all in-vault consumers (no regression). See `CHANGELOG.md` for the build log.

## What it is

The Standard is an agentic-context-native fork of Obsidian Advanced Canvas (v5.6.6) / JSON Canvas 1.0. This
package is its reference tooling. The normative specs live in the vault at `Canvas.aDNA/what/specs/`:

| Module | Implements | Spec |
|--------|-----------|------|
| `canvas_std.schema` | the KEEP floor — enums, node/edge schema, profiles | `spec_adna_canvas_standard` §4–§6, `p1_fork_baseline` §3 |
| `canvas_std.validate` | `validate(doc, level)`, `strip(doc)` | `spec_adna_canvas_standard` §10, `spec_conformance_suite` |
| `canvas_std.roundtrip` | `to_canvas`/`from_canvas`, `compute_sync_hash`, `diff`, `merge` | `spec_roundtrip_protocol_v2` |
| `canvas_std.reserved` | `_reserved` block validators (component_types / panel_link / context_object) | `spec_component_model`, `spec_panel_link_semantics`, `spec_context_object` |
| `canvas_std.conformance` | the Core/Extended/aDNA-Native harness + report + CLI | `spec_conformance_suite` |

## Install / develop

```bash
pip install -e ".[dev]"
make test     # pytest (105 passed / 10 skipped)
make lint     # ruff
```

## Versioning

`__version__` is the **package** version (`0.1.0`). `STANDARD_VERSION` is the **Standard** version this
package implements (`"2.2.0"`). They are intentionally distinct (a P2 finding).

## Provenance

Extracted (Operation Keystone) from `CanvasForge.aDNA/what/code/canvas_core/` per `adr_001` (D2 = extract).
Governed by the aDNA Canvas Standard (LIP process, `adr_003`).
