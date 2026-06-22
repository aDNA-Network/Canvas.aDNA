---
type: governance
subtype: campaign_claude
created: 2026-06-21
updated: 2026-06-21
last_edited_by: agent_stanley
tags: [governance, campaign, canvas, production, atelier]
---

# CLAUDE.md — Campaign: Operation Atelier (`campaign_canvas_production`)

## Campaign Identity

| Field | Value |
|-------|-------|
| Campaign | `campaign_canvas_production` |
| Owner | stanley |
| Status | planning (activates on A0→A1 ratification) |
| Current Phase | Phase A0: Spec/contract triage |
| Persona | Mondrian (Canvas.aDNA) |

## Quick Start

1. Read this file (auto-loaded when working in the campaign dir)
2. Read `campaign_canvas_production.md` — master campaign doc (phases A0–A3, scope, Decision Points)
3. Check the phase tables for the current mission + status
4. Claim the next unclaimed objective; create a session file in `how/sessions/active/`
5. Begin work — and HOLD at the phase gate (never auto-advance, SO-1)

## Key Files

| File | Purpose |
|------|---------|
| `campaign_canvas_production.md` | Master campaign document — phases, missions, scope, Decision Points, risks |
| `missions/mission_a0_1_contract_profile_triage.md` | A0.1 — the contract/profile decision mission |
| `missions/artifacts/a0_1_contract_profile_decision.md` | A0.1 deliverable — the decision record (ratify at the A0→A1 gate) |
| `missions/` | A1/A2/A3 mission files (authored at phase entry, SO-3) |
| `~/.claude/plans/please-read-the-claude-md-lovely-star.md` | The approved plan — full technical designs for both producers |

## Standing Orders

- **`canvas_std` is immutable.** Never edit `what/code/canvas_std/`. Verify `git -C what/code/canvas_std diff --stat`
  is empty at every phase gate (the two-shelf firewall).
- **Quarry, don't depend.** Port logic *from* `Archive.aDNA/CanvasForge.aDNA/...`; do not import `canvas_core` or
  depend on PT P5 relocation. Both producers are self-contained on the installed `adna-canvas-std`.
- **Profiles stay producer-side.** Declare `{"profile": "diagram"|"comic"}`; do not register profiles in
  `canvas_std.schema` (that would touch the immutable substrate → a LIP).
- **Comic never renders.** Emit image prompts as `_reserved.component_types[panel].qualities` metadata; rendering is
  ComfyUI's. No image I/O in the producer.
- **Phase gates are human gates.** Report a SITREP and HOLD; every mission gets a 5-line AAR before `completed`
  (SO-5). Archive, never delete (SO-6).
- **Pattern fidelity.** Clone `deck_generator` (diagram) / `document_generator` (comic) structure: substrate-free
  `model.py` → `consume.py` assembles a source → `to_canvas` → enrich `_reserved` to aDNA-Native.

## Context Loading

| Subtopic | When |
|----------|------|
| `what/specs/{spec_component_model,spec_panel_link_semantics,spec_federation_contract,spec_context_object,spec_roundtrip_protocol_v2}.md` | Always — the contracts both producers conform to |
| `what/code/canvas_std/src/canvas_std/{reserved.py,schema.py}` | A1/A2 build — the `_reserved` vocabulary + enums (the shape-enum trap) |
| `what/production/deck_generator/` (+ `iii_quality_contract.md`) | A1 — the diagram pattern template |
| `what/production/document_generator/` | A2 — the multi-page/multi-region comic template |
| `Archive.aDNA/CanvasForge.aDNA/what/code/{canvas_core/mermaid.py,canvas_comic/}` | A1/A2 — the port-from quarry |

## Delegation Notes

Opened 2026-06-21 post-Keystone. The operator chose (in plan mode) to build BOTH unbuilt production layers in one
phased campaign: **diagram first (warm-up), comic second.** The campaign sits in `status: planning` until the operator
ratifies the A0.1 decision record at the A0→A1 gate — that ratification doubles as activation. Six decisions are
pending there (see the master doc Decision Points); all have doctrine-aligned plan defaults. No code is written until
A1 opens. The full technical designs (canvas mapping, port-vs-rebuild maps, `_reserved` enrichment, test plans) live
in the approved plan file — carry them into the A1/A2 mission files at phase entry.
