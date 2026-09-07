---
type: session
session_id: session_stanley_20260907_blueprint_p2c_producer_regate
created: 2026-09-07
updated: 2026-09-07
status: active
tier: 2
persona: mondrian
operator: stanley
campaign: campaign_canvas_blueprint
phase: P2c
executor_tier: opus
last_edited_by: agent_mondrian
tags: [session, canvas, blueprint, p2c, producer_regate, layout_fit, visual_gate, traps, deck_profile]
---

# Session — Blueprint P2c: the producer re-gate

## Intent

Discharge `mission_b2_authoring_rail`'s follow-up **(a)** — the producer-wide re-gate — which its
own AAR sequenced ahead of the deferred P2b conversion memos:

> *"offering conversions while our own shelf fails the gate repeats the credibility problem the
> dogfood just fixed."*

`skill_canvas_producer_build.md` §6 declares `canvas-visual-check … --strict` **mandatory** for
every producer. It had not been run against the shipped examples since the trap corpus grew to 14.
`diagram_generator` was repaired at P2; five producers were left measured but untouched.

## Scope declaration (Tier 2)

**Writes:** `what/production/canvas_core/` (new `layout_fit.py`, `traps/cli.py`,
`traps/cv_lead_cost_01.py`, tests) · `what/production/*/src/*/layout.py` + regenerated
`examples/*.canvas` · `what/production/_scaffold/` · `how/skills/skill_canvas_producer_build.md` ·
`how/campaigns/campaign_canvas_blueprint/` · `STATE.md`.

**Firewall:** `what/code/canvas_std/` untouched — `git diff --stat` verified 0 at open and at close.

**Conflict scan:** `how/sessions/active/` empty but for `.gitkeep` at open; `git status` clean at
`57c5a67`. No peer session.

## Gate

Plan approved by the operator 2026-09-07 with three rulings — see the mission file. Folded into
`campaign_canvas_blueprint` as **P2c**, a dated scope amendment, not a sibling campaign.

## Log

*(appended as work lands)*

- **Open.** Census re-derived rather than re-read (ratified practice, `STATE.md` §Carried #6): the
  F-P2-6 table reproduces exactly — 99 findings / 13 HIGH / 0 CRITICAL. Two corrections found in
  the act of re-deriving it: **F-P2-8** (the published file count is 7, not 6) and **F-P2-9**
  (`CV-LEAD-COST-01`'s fix hint recommends a lead that trips `CV-HIERARCHY-01`).
