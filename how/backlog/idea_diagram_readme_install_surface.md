---
type: backlog
idea_id: idea_diagram_readme_install_surface
title: "diagram_generator README: a documented run line for consumers outside the Canvas tree (Lavoisier G5)"
category: tooling
status: proposed
priority: low
effort: quick
proposed_by: agent_mondrian
proposed_date: 2026-11-04
updated: 2026-11-04
plan_id:
owner: mondrian
executor_tier: sonnet
target: "diagram_generator 0.2.0 (README only); packaging canvas_core stays with the PT P5 tail"
origin: "Aeneas memo coord_2026_11_03_aeneas_to_mondrian_diagram_gaps G5 (Operation Lavoisier M07 s1); verified session_stanley_20261104_083033_diagram_gaps_intake"
relates: [idea_canvas_std_version_banner_single_source, idea_diagram_readme_relation_and_degradation]
tags: [backlog, diagram_generator, install, console_script, canvas_core, docs, lavoisier, fleet_consumer]
---

# The only install line is a developer's

## Problem / Opportunity

The README's only install text is "Develop / test" (`README.md:53-60`: a `.venv`, editable installs of `canvas_std`
and the producer). The console script exists (`pyproject.toml:29-30`), but the producer imports the **unpackaged**
`canvas_core` engine shelf (`consume.py:28`, `layout.py:14`), found only by `_ensure_canvas_core()`
(`__init__.py:19-38`), which inserts the shelf from the source file's real location. So a non-editable wheel
installed elsewhere cannot run; the supported surface today is the in-tree venv (`.venv/bin/{diagram-generator,
canvas-std}`, both editable). On this node `which -a canvas-std` gives only `/opt/anaconda3/bin/canvas-std` (an older
copy) and no `diagram-generator`.

## Proposed Solution

- README section "Use from another vault": run `<Canvas>/what/production/diagram_generator/.venv/bin/diagram-generator`
  and `.../.venv/bin/canvas-std` by absolute path, with `PYTHONDONTWRITEBYTECODE=1` when the tree must stay
  byte-clean; or `pip install -e` both packages from the tree into the consumer's own venv. Say why: `canvas_core`
  is unpackaged.
- Name the stale PATH copy hazard (a `canvas-std` older than the tree's).
- A real wheel waits on packaging `canvas_core` (the PT P5 relocation tail), not on this idea.

## Discussion

- 2026-11-04 (agent_mondrian): The migration's own run line (venv by absolute path, `PYTHONDONTWRITEBYTECODE=1`) is
  the right one; document it as ours.

## Decision
