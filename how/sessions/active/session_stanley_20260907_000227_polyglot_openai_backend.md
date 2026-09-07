---
type: session
session_id: session_stanley_20260907_000227_polyglot_openai_backend
created: 2026-09-07
updated: 2026-09-07
status: active
campaign: none — Operation Polyglot (cross-vault; charter at aDNA.aDNA/how/campaigns/campaign_agent_harness_cohort/)
objective: "Add OpenAI as second cloud GENERATE backend behind the ImageClient protocol: ADR-008 amendment draft (proposed), credential-routing snippet into CLAUDE.md, backends/openai.py + registry row + tests."
executor_tier: fable
last_edited_by: agent_fable_polyglot
tags: [session, polyglot, openai, image_generation]
---

# Lease (F-LEASE-02 — declared before first read-for-write)

Files this session may write in Canvas.aDNA — nothing else:

- `CLAUDE.md` — append the doctrine-§7 credential-routing snippet only (currently absent, doctrine-mandated)
- `what/decisions/adr_008_comic_render_doctrine.md` — append an Amendment block (`status: proposed`) OR a sibling amendment file
- `what/production/comic_render/src/comic_render/backends/openai.py` — NEW
- `what/production/comic_render/src/comic_render/backends/__init__.py` — one registry row
- `what/production/comic_render/tests/**` — new backend tests only
- `STATE.md` — one append-only intake entry
- this session file

Probed `how/sessions/active/` empty + git clean at 2026-09-07 00:02 PDT. Commits path-scoped, never `git add -A`.
