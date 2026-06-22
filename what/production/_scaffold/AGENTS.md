---
type: directory_index
created: 2026-06-21
updated: 2026-06-21
last_edited_by: agent_stanley
tags: [directory_index, canvas, production, scaffold, producer]
---

# `_scaffold/` — new-producer template (not a producer)

Clone this to start a new canvas producer on `canvas_std`. **Not a producer**; excluded from the cross-producer
sweep; ships no `.venv`. The package dir is the placeholder `src/__producer__/` (rename on clone).

- **Runbook:** `how/skills/skill_canvas_producer_build.md` — step-by-step (clone → model → consume → tests → verify).
- **Pattern:** `what/context/context_canvas_producer_pattern.md` — the principles + worked mappings.
- **Clone recipe + pipeline + conformance vocabulary:** `README.md` (this dir).
- **Exemplars to copy from:** `what/production/deck_generator/` (single-surface), `what/production/document_generator/`
  (multi-page), `what/production/diagram_generator/` (smallest/cleanest).

Standing rules (SO): never edit `what/code/canvas_std/` (firewall, git-diff 0 at every gate); profiles stay
producer-side (`{"profile": "<name>"}`, never registered in `canvas_std.schema`); producers emit metadata, never
render or score (C8 — quality via the `iii/` wrapper, pixels via ComfyUI).

Stub `src/`/`tests/` files carry `TODO(clone)` markers; test modules `pytest.skip(..., allow_module_level=True)` so
the template never reports a false failure. Remove the skips as you implement.
