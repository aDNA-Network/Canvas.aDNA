---
type: backlog
idea_id: idea_diagram_groups_block
title: "diagram_generator: an optional `groups:` block, emitted as nested baseline group nodes (Lavoisier G2)"
category: pipeline
status: proposed
priority: medium
effort: mission
proposed_by: agent_mondrian
proposed_date: 2026-11-04
updated: 2026-11-04
plan_id:
owner: mondrian
executor_tier: opus
target: "diagram_generator 0.3.0 (producer-only; no LIP; needs a layout card and a reviewer seat first)"
origin: "Aeneas memo coord_2026_11_03_aeneas_to_mondrian_diagram_gaps G2 (Operation Lavoisier M07 s1); verified session_stanley_20261104_083033_diagram_gaps_intake"
relates: [idea_diagram_edge_label_native]
tags: [backlog, diagram_generator, groups, cluster, subgraph, layout, lavoisier, fleet_consumer]
---

# "A is composed of B and C" has no box to draw

## Problem / Opportunity

The spec model has no group/cluster field: `DiagramInput` (`model.py:93-106`) and `from_dict` (`model.py:188-200`)
read `title, id, version, diagram_type, direction, refs, authority, production, prose, nodes, edges` and nothing else.
An unknown top-level key is silently ignored: a scratch spec with `groups: {core: [a, b]}` built and validated
`adna_native [OK]` with no trace of the block (2026-11-04). The only `group` node is `diagram_root`
(`consume.py:67`), the single canonical surface. Consumers draw containment as a hub node with `composes` edges.

## Proposed Solution

- Spec: optional `groups:` mapping a label to member node ids (validated: members declared, a node in at most one
  group at first; nesting later).
- Canvas: one baseline `group` node per entry, inside `diagram_root`; `_reserved.component_types[<gid>]` =
  `{class: "group", semantic_type: "cluster", degrades_to: "group"}`. **Not** a `panel_link` surface, so A-5's
  exactly-one-canonical rule (`reserved.py:387-395`) is untouched and no LIP is needed. Mermaid twin: `subgraph`.
- The real work is layout: `layout.py:104-119` places nodes by longest-path rank, declaration order within a rank, so
  a group's members can sit in different ranks with non-members between them. The box must enclose its members and
  no one else. That needs a design card (Canvas practice: card, a fresh read-only seat, then build).
- An unknown top-level key should at least warn; consider that in the same release.

## Discussion

- 2026-11-04 (agent_mondrian): The migration asks for this with G1. G1 is a session; this is a layout design, so it
  ships after G1 (0.3.0), not with it. Wanted from the migration: one spec where a hub node stands in for a box (their
  base-node case, Home + NodeStack on a machine) as the design fixture.

## Decision
