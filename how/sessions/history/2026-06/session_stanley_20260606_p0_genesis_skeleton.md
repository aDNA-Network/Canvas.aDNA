---
type: session
session_id: session_stanley_20260606_p0_genesis_skeleton
created: 2026-06-06
updated: 2026-06-06
status: completed
campaign: campaign_canvas_genesis_planning
phase: P0
last_edited_by: agent_stanley
tags: [session, genesis, canvas, p0]
---

# Session — Canvas.aDNA P0 Genesis Skeleton

## Intent

Fork `Canvas.aDNA` and seed it to a P0 skeleton: governance, Operation Cartography charter (P0–P5),
`adr_000_canvas_identity`, and the D1–D7 decision register — then HOLD at the P0 gate.

## Files Touched (created/modified)

- `CLAUDE.md` (Mondrian provisional identity + thesis + scope), `MANIFEST.md`, `STATE.md` — modified
- `how/campaigns/campaign_canvas_genesis_planning/campaign_canvas_genesis_planning.md` — created
- `what/decisions/adr_000_canvas_identity.md`, `what/decisions/decision_register_genesis.md` — created
- `who/coordination/coord_2026_06_06_naming_persona_exceptions.md` — created
- `~/lattice/CLAUDE.md` (workspace router) — one routing row + layout line + Framework Active note
- (fork) full `.adna` triad copied → `Canvas.aDNA/`; fresh `git init`

## SITREP

- **Completed:** vault forked (C1); governance tuned to the standard-bearer thesis; Operation Cartography
  chartered P0–P5 (human-gated); `adr_000` (status: proposed) + D1–D7 register drafted; repo deltas Δ1
  (category/runtime) + Δ2 (primitive/view) foregrounded at the P0 gate; router registered.
- **In progress:** P0 mission — deliverables authored, **HELD at the P0 gate** pending operator lock.
- **Next up:** operator locks persona / category (Δ1) / scope boundary → open P1 (source inventory + fork
  baseline; pin upstream Advanced Canvas version).
- **Blockers:** `#needs-human` — P0 gate (persona / category / scope). No code, no migration, no breaking
  changes performed (C3 honored).

## Next Session Prompt

Canvas.aDNA is at Operation Cartography **P0**, HELD at the gate. Read `STATE.md` → `▶ Resume Here`, then
`what/decisions/adr_000_canvas_identity.md` (§1 category + Δ1, §2 persona, §3 scope) and
`decision_register_genesis.md`. Present the three P0 decisions to the operator for lock; once locked, set
`adr_000` to `ratified`, file the P0 AAR, and open **P1** (charter the source-inventory + fork-baseline
mission; pin the upstream Advanced Canvas baseline version). Do not cross the P0 gate without operator
approval. Do not migrate code or modify CanvasForge/LiteratureForge (C3).
