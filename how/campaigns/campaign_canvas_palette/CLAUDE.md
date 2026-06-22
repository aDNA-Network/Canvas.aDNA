# CLAUDE.md — Campaign: Operation Palette (`campaign_canvas_palette`)

## Campaign Identity

| Field | Value |
|-------|-------|
| Campaign | `campaign_canvas_palette` |
| Owner | stanley |
| Status | ✅ completed 2026-06-22 (P0–P4 closed; 7 producers green; factory shipped) |
| Current Phase | — campaign complete (close record: `campaign_canvas_palette.md` §Completion Summary) |
| Persona | Mondrian (Canvas.aDNA) |

## Quick Start

1. Read this file (auto-loaded when working in the campaign dir)
2. Read `campaign_canvas_palette.md` — master campaign doc (phases P0–P4, scope, Decision Points)
3. Check the phase tables for the current mission + status
4. Claim the next unclaimed objective; create a session file in `how/sessions/active/`
5. Begin work — and HOLD at the phase gate (never auto-advance, SO-1)

## Key Files

| File | Purpose |
|------|---------|
| `campaign_canvas_palette.md` | Master campaign document — phases, missions, scope, Decision Points, risks |
| `missions/mission_p0_charter_triage.md` | P0.1 — the charter/decision mission |
| `missions/artifacts/p0_decision_record.md` | P0.1 deliverable — the decision record (ratify at the P0→P1 gate) |
| `missions/` | P1/P2/P3/P4 mission files (authored at phase entry, SO-3) |
| `~/.claude/plans/please-read-the-claude-md-sleepy-minsky.md` | The approved plan — retrospective + full charter |

## Standing Orders

- **`canvas_std` is immutable.** Never edit `what/code/canvas_std/`. Verify `git -C what/code/canvas_std diff --stat`
  is empty at every phase gate (the two-shelf firewall).
- **Factory-then-pilot.** P1 builds the skill + `_scaffold`; P2 *uses* them to build `letter_generator` — that build
  is the factory's acceptance test. Fix factory friction in P2 before P3.
- **Scaffold at producer depth.** `what/production/_scaffold/` so `../../code/canvas_std` relative paths stay valid on
  clone; `_scaffold` is inert (TODO stubs), excluded from the cross-producer sweep.
- **Profiles stay producer-side.** Declare `{"profile": "document"|"post"}`; do not register profiles in
  `canvas_std.schema` (that would touch the immutable substrate → a LIP).
- **Producers never render.** Emit image prompts as `_reserved.component_types[panel].qualities.image_prompt`
  metadata; rendering is ComfyUI's. No image I/O in the producer (C8).
- **Phase gates are human gates.** Report a SITREP and HOLD; every mission gets a 5-line AAR before `completed`
  (SO-5). Archive, never delete (SO-6).
- **Pattern fidelity.** Follow `what/context/context_canvas_producer_pattern.md`: substrate-free `model.py` →
  `consume.py` assembles a source → `to_canvas` → enrich `_reserved` to aDNA-Native.

## Context Loading

| Subtopic | When |
|----------|------|
| `what/context/context_canvas_producer_pattern.md` | Always — the pattern the factory operationalizes |
| `what/specs/{spec_component_model,spec_panel_link_semantics,spec_federation_contract,spec_context_object,spec_roundtrip_protocol_v2}.md` | Build phases — the contracts producers conform to (`§6.3` = the letter sketch) |
| `what/code/canvas_std/src/canvas_std/{reserved.py,schema.py,conformance.py}` | P1–P3 — the `_reserved` vocabulary + enums |
| `what/production/deck_generator/` (single-surface) · `what/production/document_generator/` (multi-page) | P1/P2 — clone templates for the scaffold + letter |
| `what/production/diagram_generator/` | P1 — smallest/cleanest layout reference for the scaffold |

## Delegation Notes

Opened 2026-06-21 post-Atelier. The operator chose (in plan mode, Option A of the cross-campaign retrospective) to
complete the output family + harden the producer factory. The campaign sits in `status: planning` until the operator
ratifies the P0 decision record at the P0→P1 gate — that ratification doubles as activation. Six decisions are pending
there (see the master doc Decision Points); all have doctrine-aligned plan defaults. No code is written until P1 opens.
The full charter (retrospective context, per-phase deliverables, verification) lives in the approved plan file — carry
the technical designs into the P1/P2/P3 mission files at phase entry.
