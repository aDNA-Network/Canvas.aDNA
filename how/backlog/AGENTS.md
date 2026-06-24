---
type: directory_index
created: 2026-02-17
updated: 2026-06-22
last_edited_by: agent_stanley
tags: [directory_index, backlog]
---

# Backlog — Ideation & Improvement Tracking

## Purpose

A durable place for agents to record ideas, feature requests, improvement proposals, and build goals as they arise during sessions. The backlog bridges the gap between:

- **`coordination/`** — ephemeral notes that expire and get deleted
- **`missions/`** — committed, decomposed multi-session work — too formal for "what if we..."

The backlog is the **intake funnel** for the mission system. Ideas accumulate context over time and graduate into missions when they're ready.

---

## Directory Structure

```
how/backlog/
├── AGENTS.md                    # This file — protocol + category index
└── idea_<short_name>.md         # One file per idea/feature/issue
```

---

## Idea File Format

```yaml
---
idea_id: idea_<short_name>
title: "Human-readable title"
category: vault_infra | pipeline | technical | governance | tooling
status: proposed | discussed | planned | implemented | rejected
priority: low | medium | high
effort: quick | session | plan
proposed_by: agent_<username>
proposed_date: YYYY-MM-DD
updated: YYYY-MM-DD
plan_id:
---

# Title

## Problem / Opportunity
What's the issue or idea? Why does it matter?

## Proposed Solution
How could this be addressed? (Can be rough — this is ideation, not planning.)

## Discussion
Agents append notes here as they encounter related context:
- YYYY-MM-DD (agent_name): observation or additional context

## Decision
Filled in when status changes to `planned`, `implemented`, or `rejected`.
```

### Field Reference

| Field | Values | Description |
|-------|--------|-------------|
| `idea_id` | `idea_<short_name>` | Unique ID, matches filename |
| `title` | Free text | Human-readable title |
| `category` | `vault_infra` / `pipeline` / `technical` / `governance` / `tooling` | Primary domain |
| `status` | `proposed` / `discussed` / `planned` / `implemented` / `rejected` | Current lifecycle state |
| `priority` | `low` / `medium` / `high` | Relative importance |
| `effort` | `quick` / `session` / `mission` | Estimated scope |
| `proposed_by` | `agent_<username>` | Who created it |
| `proposed_date` | `YYYY-MM-DD` | When created |
| `updated` | `YYYY-MM-DD` | Last modification |
| `plan_id` | `plan_<name>` or empty | Links to mission when graduated |

### Categories

| Category | Scope | Examples |
|----------|-------|---------|
| `vault_infra` | Vault structure, templates, naming, Obsidian config | Template variants, CSS improvements, nav redesign |
| `pipeline` | Content-as-code pipelines, automation | New pipeline types, stage improvements, quality gates |
| `technical` | Domain-specific technical work | Models, hardware, protocols, tooling |
| `governance` | Agent protocol, documentation, coordination | CLAUDE.md updates, session protocol, mission templates |
| `tooling` | Agent tools, skills, machine setup | New skills, CLI integration |

---

## Lifecycle

```
proposed → discussed → planned → implemented
                    ↘ rejected
```

- **proposed**: Agent creates the idea file during a session. Problem + rough Solution is sufficient.
- **discussed**: Other agents (or the same agent in later sessions) add context in the Discussion section.
- **planned**: User or agent graduates the idea into a mission in `how/missions/`. Set `plan_id` to link them.
- **implemented**: Mission completed, idea realized. Note what was done in the Decision section.
- **rejected**: Decision made not to pursue. Record rationale in Decision section.

---

## Agent Protocol

### On Session Start

- Scan `how/backlog/` for `status: proposed` or `discussed` ideas relevant to the current session's domain
- If the current session reveals new context for an existing idea, append to its Discussion section
- Quick scan only — do not spend more than ~1 minute on this

### During Work

- If a new idea surfaces during work, create an idea file (Problem + rough Solution, <5 min effort)
- If you encounter context relevant to an existing idea, append a Discussion entry
- Do not let backlog maintenance distract from the primary task

### On Session End

- If ideas were created or updated, mention them in the SITREP

### Graduation Protocol

When an idea accumulates enough context and gets user buy-in:

1. Create a mission in `how/missions/mission_<name>.md`
2. Update the idea's `status: planned` and `plan_id: mission_<name>`
3. The idea file remains as the "why" record; the mission is the "how"

---

## Current Backlog

> Triaged 2026-06-21 (post-Keystone, `session_stanley_20260621_141753_backlog_triage`). Live backlog holds only
> Canvas-canonical objects; inherited `.adna` template scaffold was quarantined → `_inherited_scaffold/`.

| Idea | Category | Status | Priority | Effort |
|------|----------|--------|----------|--------|
| `idea_campaign_leg3_interface_runtime` | technical | implemented (Armature P3, 2026-06-23) | high | plan |
| `idea_oip_v1x_interface_reanchor` | technical | proposed (deferred — gated on the `aDNA.aDNA` OIP campaign) | high | session |
| `idea_deck_generator_canvas_pilot` | pipeline | implemented | high | plan |
| `idea_upstream_fork_inherits_stale_backlog` | governance | proposed | medium | quick |

> `idea_campaign_leg3_interface_runtime` filed 2026-06-22 at the Operation Salon P5 close — the committed follow-on
> (the deferred leg-3 interaction **runtime** build: governed `.lattice.yaml` round-trip write + `I-*` into the
> `canvas_std` harness + the `interaction_version 1.0` Standard-version cut + the `v1.x` OIP re-anchor). **GRADUATED
> 2026-06-22 → Operation Armature (`campaign_canvas_armature`)** — operator committed at the Salon-close follow-on;
> chartered + ratified (P0→P1) as a 4-phase build. **✅ IMPLEMENTED 2026-06-23 at the Armature P3 close** (P1 governed
> advisory-reverse write · P2 `I-*`→`canvas_std` harness + the `interaction_version 1.0` → Standard **v2.2.0** cut · P3
> close); full regression green throughout. The `v1.x` OIP re-anchor is filed as its own deferred stub →
> `idea_oip_v1x_interface_reanchor` (D8; gated on the unopened `aDNA.aDNA` OIP-unification campaign).

**Archived (non-canonical):** `_inherited_scaffold/` holds 6 inherited `campaign_adna_polish` template ideas (demo
GIF · plugin trim · inner-README III · custom logo · banner variants · startup optimization) — they concern the aDNA
workspace/template/brand, not the Canvas Standard, and route to `aDNA.aDNA` / `aDNALabs.aDNA`. See
[[how/backlog/_inherited_scaffold/README|_inherited_scaffold/README]].

## Load/Skip Decision

**Load this directory when**:
- Session startup scan — quickly check for `proposed` or `discussed` ideas relevant to your current task (startup checklist step 6)
- Creating a new idea file when an improvement surfaces during work
- Graduating a mature idea into a mission (set `status: planned`, link `plan_id`)

**Skip when**:
- Startup scan shows no relevant ideas and you're not creating new ones
- Deep in mission execution where backlog scanning would be a distraction
- Already reviewed backlog this session and found nothing relevant

**Token cost**: ~1,100 tokens (this AGENTS.md)
