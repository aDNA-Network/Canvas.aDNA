---
type: directory_index
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [directory_index, canvas, production, letter, producer]
---

# `letter_generator/` — one-page letter producer (Operation Palette P2)

A net-new producer on `canvas_std`: a `Letter` spec → a v2.0.0 aDNA-Native one-page-letter `.canvas`. First producer
built off the `_scaffold` factory by following `how/skills/skill_canvas_producer_build.md`.

- **Pipeline:** `model.py` (substrate-free `Letter`) → `consume.py` (`build_letter`: single `letter_root` surface +
  one paged region + reading_order edges) → `_reserved` enrich → aDNA-Native. CLI: `letter-generator build <in> <out>`.
- **Tests:** `tests/` — four+1 suite (`test_conformance`, `test_roundtrip`, `test_degradation`, `test_components`,
  `test_letter`, `test_model_neutrality`). Run: `PYTHONPATH=src .venv/bin/python -m pytest tests -q`.
- **Quality:** `iii_quality_contract.md` (a contract; review via the `iii/` wrapper, not in-producer).

Doctrine (SO): never edit `what/code/canvas_std/` (firewall — `git diff --stat` 0); profile stays producer-side
(`{"profile": "document"}`, never in `canvas_std.schema`); emit metadata, never render/score (C8). Standard:
`what/code/canvas_std/`. Pattern: `what/context/context_canvas_producer_pattern.md`.
