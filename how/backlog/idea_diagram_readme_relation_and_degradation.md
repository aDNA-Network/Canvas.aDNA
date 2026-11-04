---
type: backlog
idea_id: idea_diagram_readme_relation_and_degradation
title: "diagram_generator README: what `relation:` reaches, which nodes the producer generates, and the `degradation:` line (Lavoisier G8, with the G7 note)"
category: governance
status: proposed
priority: low
effort: quick
proposed_by: agent_mondrian
proposed_date: 2026-11-04
updated: 2026-11-04
plan_id:
owner: mondrian
executor_tier: sonnet
target: "diagram_generator 0.2.0 (README only)"
origin: "Aeneas memo coord_2026_11_03_aeneas_to_mondrian_diagram_gaps G8 (and G7's documentation half; Operation Lavoisier M08 s1); verified session_stanley_20261104_083033_diagram_gaps_intake"
relates: [idea_diagram_edge_label_native, idea_diagram_readme_install_surface]
tags: [backlog, diagram_generator, relation, degradation_report, generated_nodes, docs, lavoisier, fleet_consumer]
---

# Three things the README does not say

## Problem / Opportunity

1. **`relation:`** is parsed (`model.py:184`, default `flow`, `model.py:86`) but reaches output only in two Mermaid
   emitters: the `class_diagram` glyph (`mermaid.py:74`) and the `sequence` message fallback when there is no label
   (`mermaid.py:60`). `flowchart` and `state_diagram` ignore it, and the native canvas never carries it
   (`consume.py:111-115`). Reproduced 2026-11-04: `relation: composition` on a flowchart edge left no trace in the
   built file.
2. **Producer-generated nodes** (the G7 ask) are already distinguishable, but nowhere documented:
   `_reserved.component_types[<id>].class` is `shape` for every authored node (`diagrams.py:42-50`) and `panel`
   (`diagram_root`, `consume.py:68`), `typography_run` (`diagram_title`, `consume.py:86-91`) or `code`
   (`mermaid_src`, `consume.py:100-105`) for the three the producer adds. The title text repeats verbatim in the
   `diagram_root` label (`consume.py:67`) and the title node (`consume.py:82`), and in the gantt Mermaid
   (`mermaid.py:99-100`).
3. **`degradation: {'D-1': True, 'D-2': True, 'D-3': True}`** is printed by `canvas-std validate` at `adna_native`
   (`conformance.py:63-64`, `:114-115`), the D-1..D-3 degradation report; the producer README shows only
   `level_reached=adna_native [OK]` (`README.md:30`).

## Proposed Solution

One README section: the relation table (where each value lands, per diagram type); "authored vs generated nodes: filter
on `component_types[id].class == "shape"`"; one line on the degradation report and what a `False` means. If a
second consumer needs `relation` on the native edge, that is a Standard question (no edge-semantics slot today) and a
LIP candidate, not a README line.

## Discussion

- 2026-11-04 (agent_mondrian): G7's ask for a new marker is declined because the marker exists; this idea carries the
  sentence that says so.

## Decision
