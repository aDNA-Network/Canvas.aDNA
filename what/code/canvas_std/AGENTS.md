---
type: directory_index
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [directory_index, code, canvas_std, reference-impl]
---

# what/code/canvas_std/ — reference implementation (code-as-WHAT-object)

The runnable reference tooling for the aDNA Canvas Standard v2.0.0 (Option P; single-repo code-as-WHAT-object per
the VideoForge Amendment-1 precedent). Built by **Operation Keystone** (`how/campaigns/campaign_canvas_genesis/`).

## Status
- **E0.1 (this mission):** skeleton — packaging + API stubs + smoke test. ✅
- **E0.2:** port the verbatim KEEP floor into `schema.py`.
- **E1:** implement validators / round-trip / `_reserved` validators / conformance harness.
- **E2:** conformance corpus + publish v2.0.0 JSON Schema + CLI.

## Discipline
- This is the **single source of truth** for the Standard's machinery. Producers (CanvasForge, LF-successor)
  consume it via `federation_ref` — they never copy it (`spec_federation_contract`).
- The public API surface is **frozen at E0.1**; E0.2/E1 fill behavior without changing signatures (so the
  conformance vocabulary and the API stay in lockstep — a P2 finding).
- Stubs raise `NotImplementedError` naming the owning E-phase. Do not delete a stub; implement it.
- Standard-version vs package-version: `STANDARD_VERSION` (the spec, "2.0.0") ≠ `__version__` (the package).

## Layout
```
canvas_std/
├── pyproject.toml · LICENSE · README.md · CHANGELOG.md · Makefile
├── src/canvas_std/{__init__,schema,validate,roundtrip,reserved,conformance}.py
└── tests/test_smoke.py
```
