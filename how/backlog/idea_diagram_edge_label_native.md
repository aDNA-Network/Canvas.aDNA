---
type: backlog
idea_id: idea_diagram_edge_label_native
title: "diagram_generator: a spec edge `label` reaches only the Mermaid twin, never the native canvas edge (Lavoisier G1)"
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
target: "diagram_generator 0.2.0 (producer-only; no LIP, no Standard change)"
origin: "Aeneas memo coord_2026_11_03_aeneas_to_mondrian_diagram_gaps G1 (Operation Lavoisier M07 s1: 0 of 87 edges carry a label); verified session_stanley_20261104_083033_diagram_gaps_intake"
relates: [idea_diagram_groups_block, idea_diagram_mermaid_label_escaping, idea_diagram_readme_relation_and_degradation]
tags: [backlog, diagram_generator, edge_label, json_canvas_baseline, lavoisier, fleet_consumer]
---

# A relation the native graph cannot show

## Problem / Opportunity

`consume.py:111-115` builds every canvas edge from `{id, fromNode, toNode, fromSide, toSide}` and never reads
`e.label` (stored at `model.py:85`, parsed at `model.py:183`). The label survives only in the `mermaid_src` text
(`mermaid.py:47-48`). A reader of the native graph, or any tool reading the `.canvas`, sees no relation. Reproduced
2026-11-04 on a scratch spec: both edges `['fromNode','fromSide','id','toEnd','toNode','toSide']`.

A second, deeper layer: `canvas_std.to_canvas` builds edges from a fixed key set (`roundtrip.py:88-95`) and would drop an
edge `label` even if the source carried one; `from_canvas` drops it on the way back (`roundtrip.py:142-152`). Nodes copy
`label` (`roundtrip.py:75`, `:137`); edges do not.

## Proposed Solution

- **0.2.0 (producer-only):** after `to_canvas`, set `edge["label"] = e.label` on each canvas edge whose spec edge has a
  label. Edge `label` is baseline JSON Canvas and already in our schema's edge properties
  (`canvas_std/data/adna_canvas_v2.schema.json:63`), so the canvas stays baseline-legal and degrades unchanged.
  `sync_hash` is topology-only (`roundtrip.py:43-46`), so it does not move. Existing canvases change bytes only where a
  spec edge has a label. Tests: a label present on the native edge; absent when the spec has none (byte-identical
  output for label-free specs); round-trip and degradation still green.
- **Deferred to the next `canvas_std` firewall touch (operator-signed):** make `to_canvas`/`from_canvas` carry edge
  `label` like node `label`, so no producer post-step is needed. A firewall touch, not a 0.2.0 item.
- **Not taken here:** carrying `relation:` in `_reserved`. The Standard has no edge-semantics slot (`panel_link.edges`
  holds `kind` only; `component_types` entries degrade to baseline *node* types). A LIP candidate if a second consumer
  asks; recorded under `idea_diagram_readme_relation_and_degradation`.

## Discussion

- 2026-11-04 (agent_mondrian): The migration asks for this first. Build waits on the operator's word (Vernier is the
  active campaign; a producer release outside its charter is his to schedule). A sample spec from the migration (one
  of `Migration.aiDNA/what/diagrams/*.yaml`) would serve as the regression fixture.

## Decision
