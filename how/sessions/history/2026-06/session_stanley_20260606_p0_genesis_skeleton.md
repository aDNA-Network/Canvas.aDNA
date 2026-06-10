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
- `~/aDNA/CLAUDE.md` (workspace router) — one routing row + layout line + Framework Active note
- (fork) full `.adna` triad copied → `Canvas.aDNA/`; fresh `git init`

## SITREP

- **Completed:** vault forked (C1); governance tuned to the standard-bearer thesis; Operation Cartography
  chartered P0–P5 (human-gated); `adr_000` (status: proposed) + D1–D7 register drafted; repo deltas Δ1
  (category/runtime) + Δ2 (primitive/view) foregrounded at the P0 gate; router registered.
- **Gate cleared:** operator **ratified P0** in-session — persona **Mondrian**; category **Platform.aDNA
  (standard-bearer), Option P** (ships reference tooling, vault+code split); scope **confirmed**. `adr_000`
  → `status: ratified`; D1 resolved; P0 phase AAR filed in the charter.
- **Next up:** open **P1** (source inventory + fork baseline; pin upstream Advanced Canvas version) **on
  operator go** (one phase per gate).
- **Blockers:** none blocking. No code, no migration, no breaking changes performed (C3 honored).

## Next Session Prompt

Canvas.aDNA **P0 is ratified** (persona Mondrian; category Platform.aDNA/Option P — ships reference tooling,
vault+code split; scope confirmed). Read `STATE.md` → `▶ Resume Here`. On operator go, **open P1**: charter the
source-inventory + fork-baseline mission (catalog Canvas Standard v1.0.0 + `CanvasBuilder` constants + the
`advanced_canvas/` corpus + Round-Trip Protocol + graft_manifest + LF visual/format/genre specs; label
KEEP/EXTEND/SUPERSEDE/DEFER-TO-PRODUCER; **pin the upstream Advanced Canvas baseline version** — confirm v5.6.6).
Carry the Platform vault+code split (declare `what/code/canvas_std/`, don't build it, C3) and the D2-extraction
lean. One phase per gate — do not open P1 without operator approval; do not migrate code or modify
CanvasForge/LiteratureForge.
