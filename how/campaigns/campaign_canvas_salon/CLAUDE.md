---
type: governance
subtype: campaign_claude
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [governance, campaign, canvas, salon, surface]
---

# CLAUDE.md — Campaign: Operation Salon (`campaign_canvas_salon`)

## Campaign Identity

| Field | Value |
|-------|-------|
| Campaign | `campaign_canvas_salon` |
| Owner | stanley |
| Status | planning (→ active on P0 ratification) |
| Current Phase | P0 — Charter, boundary ADR & decision record (HELD at P0→P1 gate) |
| Persona | Mondrian (Canvas.aDNA) |
| Predecessor | `campaign_canvas_palette` (Operation Palette, completed 2026-06-22) |

## Quick Start

1. Read this file (auto-loaded when working in the campaign dir)
2. Read `campaign_canvas_salon.md` — master campaign doc (phases P0–P5, scope, Decision Points, risks)
3. Check the phase tables for the current mission + status
4. Claim the next unclaimed objective; create a session file in `how/sessions/active/`
5. Begin work — and HOLD at the phase gate (never auto-advance, SO-1)

## Key Files

| File | Purpose |
|------|---------|
| `campaign_canvas_salon.md` | Master campaign document — phases, missions, scope, Decision Points, risks |
| `missions/mission_p0_charter_boundary.md` | P0.1 — the charter/boundary/decision mission |
| `missions/artifacts/p0_decision_record.md` | P0.1 deliverable — the 8-decision record (ratify at the P0→P1 gate) |
| `../../what/decisions/adr_006_canvas_surface_boundary.md` | The boundary ADR (ratify at the P0→P1 gate) |
| `missions/` | P1–P5 mission files (authored at phase entry, SO-3) |
| `~/.claude/plans/please-read-the-claude-md-sleepy-aho.md` | The approved plan — retrospective + full charter |

## Standing Orders

- **`canvas_std` is immutable by default.** Never edit `what/code/canvas_std/`; verify `git -C what/code/canvas_std
  diff --stat` is empty at every phase gate (the two-shelf firewall). The leg-2 loader is a **new sibling package**
  unless D6 explicitly lifts the firewall.
- **Boundary first.** `adr_006` fixes what Canvas-as-surface owns vs ISS / Astro / Terminal / OIP **before** any
  leg-2/leg-3 build. Do not specify cross-surface *routing* — that is the future `aDNA.aDNA` OIP campaign's job.
- **Spec before impl.** Leg 2 = P1 spec → P2 impl/pilot. Leg 3 = P3 spec only (build deferred to a follow-on; P4 POC
  is stretch).
- **Ride `_reserved`.** Legs 2 & 3 use the namespaced `_reserved` extension carrier; do **not** touch core schema or
  re-open the canvas-as-primitive question (Δ2 / LIP-0009 — out of scope).
- **Load without rendering.** The leg-2 proof is loading an existing producer `.canvas` as a context graph with **no**
  render-pipeline / image I/O.
- **Phase gates are human gates.** Report a SITREP and HOLD; every mission gets a 5-line AAR before `completed` (SO-5).
  Archive, never delete (SO-6).

## Context Loading

| Subtopic | When |
|----------|------|
| `what/decisions/adr_000_canvas_identity.md` (§Context — the three-leg thesis) | Always |
| `what/decisions/adr_006_canvas_surface_boundary.md` | Always — the boundary the campaign works within |
| `what/specs/spec_context_object.md` | P1/P2 — the leg-2 metadata foundation (the "how" is the gap to fill) |
| `who/coordination/coord_2026_06_13_*lp_canvas_seam*` | P0 — the stewardship-split template for `adr_006` |
| `what/specs/{spec_component_model,spec_panel_link_semantics,spec_roundtrip_protocol_v2}.md` | P1/P2 — the structure a loader traverses |
| `what/production/document_generator/` | P2 — source of a known-good `.canvas` for the loader pilot |
| `aDNA.aDNA` OIP backlog (`idea_campaign_operator_interaction_patterns_unification.md`) + ISS (`skill_create_iss.md`) | P3 — the leg-3 neighbours to coordinate with |

## Delegation Notes

Opened 2026-06-22 post-Palette. The operator chose canvas-as-surface (the deferred Option B from the Palette
retrospective) to exercise the under-proven **context-object** (leg 2) + **interface-surface** (leg 3) legs of the
thesis. The campaign sits in `status: planning` until the operator ratifies the P0 decision record + `adr_006` at the
P0→P1 gate — that ratification doubles as activation. **Eight decisions are pending** there (see the master doc
Decision Points + `missions/artifacts/p0_decision_record.md`); all have doctrine-aligned defaults. **No build code is
written until P2**, and the leg-2 loader's home + firewall posture is itself a ratifiable decision (D6) — do not touch
`canvas_std` on assumption. The full charter (foundation facts, per-phase deliverables, risks) lives in the master doc
and the approved plan; carry technical designs into the P1/P2/P3 mission files at phase entry.
