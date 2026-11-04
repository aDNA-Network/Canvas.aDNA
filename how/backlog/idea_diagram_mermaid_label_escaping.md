---
type: backlog
idea_id: idea_diagram_mermaid_label_escaping
title: "diagram_generator: inner `\"` (and `|` in edge labels) reach the Mermaid source unescaped, and nothing catches it (Lavoisier G6)"
category: pipeline
status: proposed
priority: high
effort: session
proposed_by: agent_mondrian
proposed_date: 2026-11-04
updated: 2026-11-04
plan_id:
owner: mondrian
executor_tier: opus
target: "diagram_generator 0.2.0 (producer-only; with G1)"
origin: "Aeneas memo coord_2026_11_03_aeneas_to_mondrian_diagram_gaps G6 (Operation Lavoisier M08 s1: 5 of 20 canvases); verified session_stanley_20261104_083033_diagram_gaps_intake"
relates: [idea_diagram_edge_label_native]
tags: [backlog, diagram_generator, mermaid, escaping, render_fidelity, lavoisier, fleet_consumer]
---

# The Mermaid twin can be invalid while every gate is green

## Problem / Opportunity

`mermaid.py:45` writes `f'    {node.id}{left}"{node.label}"{right}'` with no escaping, so a label containing `"`
breaks the quoted string. Reproduced 2026-11-04: label `Alpha ("never bind")` emitted as
`a["Alpha ("never bind")"]`. Found on the same probe: an edge label containing `|` (`mermaid.py:48`,
`-->|{edge.label}|`) emitted `b -->|feeds|pipe| c`, also invalid. `build` and `canvas-std validate` both pass because the
native canvas is unaffected, and the ported `mermaid.validate` (`mermaid.py:126-166`) checks only the type line and
bracket balance, so it cannot see either fault.

## Proposed Solution

- One `_esc()` in `mermaid.py` applied to node labels (`"` → `#quot;`) and flowchart edge labels (`|` → `#124;`,
  `"` → `#quot;`); audit the other emitters (`sequence` `:60-61`, `class_diagram` `:75-76`, `state_diagram` `:89-90`)
  for their own delimiters (`:` and newlines) in the same pass.
- Tests: a label with `"`, `|`, `:` per diagram type; the native text node keeps the original characters (escaping
  is Mermaid-only).
- Optional: teach `validate()` to flag an odd count of `"` inside a node bracket.

## Discussion

- 2026-11-04 (agent_mondrian): The migration worked round it with single quotes. Ships with G1 in 0.2.0.

## Decision
