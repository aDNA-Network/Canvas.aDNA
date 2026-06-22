---
plan_id: mission_p0_charter_triage
type: plan
title: "P0.1 — Charter + factory/producer decision record"
owner: stanley
status: in_progress
campaign_id: campaign_canvas_palette
campaign_phase: 0
campaign_mission_number: 1
mission_class: reconnaissance
created: 2026-06-21
updated: 2026-06-21
last_edited_by: agent_stanley
tags: [plan, campaign, canvas, production, palette, decision]
---

# Mission: P0.1 — Charter + factory/producer decision record

**Campaign**: [[how/campaigns/campaign_canvas_palette/campaign_canvas_palette|campaign_canvas_palette]]
**Phase**: 0 — Charter & decision record
**Mission**: 1 of 5

## Goal

Resolve the six governance/scope questions that gate the factory and producer builds — **before any code** — and record
them as a single ratifiable decision record. This removes governance ambiguity ahead of P1/P2/P3 (the Keystone/Atelier
lesson: governance touches discovered mid-build cost the most). No code, no spec edits.

## Exit Gate

A decision record exists capturing the 6 Decision Points (codename · factory artifact homes · letter conformance level ·
post domain model · producer names · optional stretch), each with a doctrine-aligned default and rationale; the absence
of any dedicated `letter`/`post` producer or spec is confirmed. **The operator ratifies the record at the P0→P1 gate —
that ratification activates the campaign and authorizes the P1 factory build.**

## Objectives

### 1. Confirm landscape
- **Status**: completed
- **Session**: session_stanley_20260621_234100_palette_scaffold_p0
- **Description**: Verify no `letter_generator`/`post_generator` producer exists and no dedicated `spec_letter_*`/`spec_post_*` exists; note where letter/post are referenced (federation §6.3 letter sketch; incidental in component/panel-link).
- **Files**: `what/production/`, `what/specs/` (read-only)
- **Depends on**: none

### 2. Author the decision record
- **Status**: completed
- **Session**: session_stanley_20260621_234100_palette_scaffold_p0
- **Description**: Write the 6-decision record with defaults + rationale.
- **Files**: `missions/artifacts/p0_decision_record.md`
- **Depends on**: 1

### 3. Operator ratification (P0→P1 gate)
- **Status**: pending — **HELD at the P0→P1 human gate**
- **Session**: (next)
- **Description**: Present the record; operator ratifies/edits each decision. On ratification → campaign `status: active`, open P1 (factory).
- **Files**: this mission (→ completed + AAR), campaign doc (Decision Points → ratified), the decision record (→ ratified), STATE.md
- **Depends on**: 2

## Campaign Context

### Previous Mission Outputs
- None — first mission of the campaign (predecessor: Operation Atelier, completed 2026-06-21).

### Next Mission Inputs
- P1 (factory) needs: ratified factory artifact homes + the skill/scaffold shape.
- P2 (letter) needs: ratified letter conformance level + producer name.
- P3 (post) needs: ratified post domain model + producer name + platform-profile posture.

## Notes

All six decisions have plan defaults in the approved plan file (`~/.claude/plans/please-read-the-claude-md-sleepy-minsky.md`).
This mission only *records and ratifies* them; it writes no factory or producer code.

> **⛔ HELD at the P0→P1 gate (human gate, SO-1).** The decision record is authored (`status: draft`); awaiting operator
> ratification before the campaign activates and P1 opens. Completion Summary + AAR are written at ratification.
