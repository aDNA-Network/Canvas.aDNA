---
idea_id: idea_upstream_fork_inherits_stale_backlog
type: backlog
category: governance
title: "Fork inherits stale campaign_adna_polish backlog + example campaign as live content"
status: proposed
priority: medium
effort: quick
proposed_by: agent_stanley
proposed_date: 2026-06-21
created: 2026-06-21
updated: 2026-06-21
last_edited_by: agent_stanley
plan_id:
tags: [backlog, upstream-suggestion, fork, scaffold, hygiene]
upstream_target: aDNA-Network/aDNA
---

# Fork inherits stale `campaign_adna_polish` backlog + example campaign as live content

## Observation

The `.adna` base template ships **non-canonical example/deferred content as live tree content**, and
`skill_project_fork.md` copies it verbatim into every new `<Name>.aDNA` vault. Two concrete classes seen in this one
vault (Canvas.aDNA):

1. **Six backlog ideas** sourced from `campaign_adna_polish` (`idea_demo_gif`, `idea_plugin_trimming`,
   `idea_inner_readme_iii`, `idea_custom_logo`, `idea_text_banner_variants`, `idea_startup_optimization`) — all
   authored by `agent_init` on **2026-04-04**, i.e. baked into the template, not the project. They concern the aDNA
   *workspace / template / brand* (root README, `.adna/README.md`, bundled Obsidian plugins, the aDNA banner & logo,
   generic agent cold-start), so they are **non-canonical to every forked project's domain**.
2. **An example campaign** (`campaign_adna_workspace_upgrade/`) likewise shipped as a live campaign.

Each fork must then manually recognize and quarantine this debt. In Canvas.aDNA it has now happened **twice**: the
example campaign was hand-moved to `how/campaigns/_inherited_scaffold/` during genesis P1 (2026-06-12), and the six
backlog ideas to `how/backlog/_inherited_scaffold/` post-Keystone (2026-06-21). Presumably every other fork carries the
same uncleaned scaffold.

## Context

Surfaced during a post-Keystone **backlog triage** in Canvas.aDNA (`session_stanley_20260621_141753_backlog_triage`).
The operator asked to "work the backlog"; the triage found 6 of 7 ideas were inherited template scaffold, not Canvas
work — so the session became hygiene (quarantine + route to owning vaults) rather than a build.

## Suggested improvement

Pick one (in rough order of preference):

- **A — template carries examples as inert.** Move shipped example campaigns + `campaign_adna_polish`-style backlog
  ideas out of the live tree into a clearly-marked `_examples/` (or `.example`-suffixed) location the fork process
  **does not** copy into a new project. The template still demonstrates the format without seeding debt.
- **B — fork clears/quarantines on copy.** `skill_project_fork.md` gains a step that, at fork-time, either drops
  template-example `how/backlog/idea_*.md` + example `how/campaigns/*` or relocates them into an `_inherited_scaffold/`
  holder automatically (the convention forks already use by hand). Add a one-line note to the fork SITREP so the
  operator knows.
- **C — at minimum, document it.** If neither A nor B, add a fork-time checklist item / onboarding note telling new
  vaults to triage inherited `how/backlog/` + example campaigns, pointing at the `_inherited_scaffold/` convention.

## Affected files (aDNA template / aDNA.aDNA)

- `.adna/how/skills/skill_project_fork.md` — fork copy logic (the place to add B or C).
- `.adna/how/backlog/idea_*.md` — the shipped `campaign_adna_polish` ideas (candidates for A).
- `.adna/how/campaigns/<example campaign>/` — the shipped example campaign (candidate for A).
- Lands via `aDNA.aDNA`'s `skill_template_release` (the maintainer of this node's `.adna/`; do **not** edit `.adna/`
  directly — Standing Rule 1).

## Discussion

- 2026-06-21 (agent_stanley): filed from Canvas.aDNA's triage. The `_inherited_scaffold/` quarantine convention used
  here (folder-note README + `git mv`, SO-6) is a reasonable template for option B's automated holder.

## Decision

Pending operator review + (optionally) a `gh issue` to `aDNA-Network/aDNA`. Not auto-filed upstream.
