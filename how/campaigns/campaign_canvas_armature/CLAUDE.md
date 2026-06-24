---
type: governance
subtype: campaign_claude
created: 2026-06-22
updated: 2026-06-23
last_edited_by: agent_stanley
tags: [governance, campaign, canvas, armature, leg3, interface, runtime, firewall]
---

# CLAUDE.md — Campaign: Operation Armature (`campaign_canvas_armature`)

## Campaign Identity

| Field | Value |
|-------|-------|
| Campaign | `campaign_canvas_armature` |
| Owner | stanley |
| Status | ✅ **COMPLETE 2026-06-23** (`status: completed`; P0–P3) — leg-3 interface runtime built; the first `canvas_std` firewall touch landed under `adr_007`; `interaction_version 1.0` cut → Standard **v2.2.0**; three-leg thesis fully runtime-enabled. P0–P3 pushed to GitHub-public. |
| Current Phase | ✅ **Campaign CLOSED.** All 4 missions completed — P0 charter + `adr_007` · P1 governed advisory-reverse write runtime · P2 `I-*`→`canvas_std` harness + the v2.2.0 cut · P3 close. Full regression green (`canvas_std` 105/10 · `canvas_context` 58 · 7 producers 223); `iii/` review SHIP (0 High / 0 Med); patterns graduated → `context_canvas_surface_legs.md`; `idea_campaign_leg3_interface_runtime` `implemented`; OIP re-anchor stub filed; `canvas_std` git-diff 0 restored. Close record: `campaign_canvas_armature.md` §Completion Summary + §Campaign AAR. |
| Persona | Mondrian (Canvas.aDNA) |
| Predecessor | `campaign_canvas_salon` (Operation Salon, completed 2026-06-22 — this campaign builds its deferred leg-3 *runtime*) |

## Quick Start

1. Read this file (auto-loaded when working in the campaign dir)
2. Read `campaign_canvas_armature.md` — master campaign doc (phases P0–P3, scope, Decision Points, risks)
3. Check the phase tables for the current mission + status
4. Claim the next unclaimed objective; create a session file in `how/sessions/active/`
5. Begin work — and HOLD at the phase gate (never auto-advance, SO-1)

## Key Files

| File | Purpose |
|------|---------|
| `campaign_canvas_armature.md` | Master campaign document — phases P0–P3, scope, Decision Points, risks |
| `missions/mission_p0_charter.md` | P0 — the charter / decision-record / ADR-draft mission |
| `missions/artifacts/p0_decision_record.md` | P0 deliverable — the 8-decision record (ratify at the P0→P1 gate) |
| `../../../what/decisions/adr_007_leg3_firewall_touch.md` | The firewall-touch ADR (ratify at the P0→P1 gate, with the decision record) |
| `../../backlog/idea_campaign_leg3_interface_runtime.md` | The Salon follow-on stub this campaign graduates (→ `implemented` at P3 close) |
| `missions/` | P1–P3 mission files (authored at phase entry, SO-3) |
| `~/.claude/plans/please-read-the-claude-md-glimmering-teapot.md` | The approved plan — full charter + phase design |

## Standing Orders

- **`canvas_std` is immutable until P2 — and then only under `adr_007`.** Never edit `what/code/canvas_std/` in
  P0/P1/P3; verify `git status -s -- what/code/canvas_std/` is clean at those gates (the two-shelf firewall). **NB:**
  `canvas_std` is part of Canvas.aDNA's git, **not** a nested repo — the pathspec form is the accurate check (a bare
  `git -C what/code/canvas_std diff` reports the *whole* parent repo). The firewall **lifts only in P2**, only after the
  operator ratifies `adr_007`, and only for the bounded purpose it names (wire `I-*` into the harness + cut the Standard
  version). At the P2 gate the check **changes** from git-diff 0 to **full regression green** (`canvas_std` +
  `canvas_context` + 7 producers + D-1..D-3 on an interaction golden).
- **The governed write is ADVISORY, never silent.** A response advances the *view*; reconciling it to the authoritative
  `.lattice.yaml` produces a **reviewed draft** through the spec_roundtrip_protocol_v2 §5 path
  (diff → three-way merge → human-review gate → regenerate). A tool MUST NOT silently propagate edits to source (§1.2).
  A P1 test asserts the on-disk source is byte-unchanged after `reconcile`.
- **Reuse `roundtrip.py`, don't rebuild.** P1 builds on `canvas_std.roundtrip` (`diff`/`merge`/`preserve_positions`/
  `compute_sync_hash`/`from_canvas`/`to_canvas`) + the POC's `apply_response`; P2's I-2 reuses
  `reserved.validate_anchors`. Import `canvas_std` read-only **via pythonpath, never an editable install** (an `-e`
  install would write `*.egg-info` into the immutable tree).
- **Stay in the grammar lane (ADR-006).** Build the reconcile path of the affordance/anchor/response/turn *grammar* — not
  a gate engine (ISS), a renderer, a transport, or a cross-surface router (OIP). No routing logic enters this campaign.
- **Ride `_reserved.interaction`.** The interaction layer is additive; do **not** touch core schema or re-open
  canvas-as-primitive (Δ2 / LIP-0009 — out of scope). Round-trip-to-baseline (strip → valid Core canvas) MUST hold.
- **Phase gates are human gates.** Report a SITREP and HOLD; every mission gets a 5-line AAR before `completed` (SO-5).
  Archive, never delete (SO-6). Commit/push is operator-gated (Git-Ops §3).

## Context Loading

| Subtopic | When |
|----------|------|
| `what/decisions/adr_000_canvas_identity.md` (§Context — the three-leg thesis) | Always |
| `what/decisions/adr_006_canvas_surface_boundary.md` | Always — the boundary the runtime works within |
| `what/decisions/adr_007_leg3_firewall_touch.md` | Always — the firewall-touch decision governing P2 |
| `what/specs/spec_interface_surface.md` | P1/P2 — the ratified leg-3 contract (IX1–IX6; the `I-*` family) |
| `what/specs/spec_roundtrip_protocol_v2.md` | P1 — the advisory authority model + the §5 reverse path the write uses |
| `what/code/canvas_context/src/canvas_context/interaction.py` | P1 — the POC reader + `apply_response` fold to promote |
| `what/code/canvas_std/src/canvas_std/roundtrip.py` | P1 — `diff`/`merge`/`preserve_positions`/`from_canvas`/`to_canvas` to reuse |
| `what/code/canvas_std/src/canvas_std/{validate,conformance}.py` | P2 — the harness to wire `I-*` into (firewall touch) |
| `what/specs/spec_conformance_suite.md` (§4.1, §5) | P2 — the `I-*` rows to implement + the D-1..D-3 contract |
| `what/context/context_canvas_surface_legs.md` | P1 — the graduated compose-not-extend / view-fold patterns |
| `aDNA.aDNA` OIP backlog (`idea_campaign_operator_interaction_patterns_unification.md`) | P3 — the OIP re-anchor stub target (deferred) |

## Delegation Notes

Opened 2026-06-22 post-Salon, graduating the Salon follow-on stub (`idea_campaign_leg3_interface_runtime`). The operator
chose **build the leg-3 runtime** (over push/cross-post housekeeping) and, at the planning gate, chose to **include the
first-ever `canvas_std` firewall touch** as a gated P2 and the **codename Operation Armature** (AskUserQuestion). The
campaign sits in `status: planning` until the operator ratifies the P0 decision record + `adr_007` at the P0→P1 gate —
that ratification doubles as activation. **Eight decisions** are recorded there (master doc Decision Points +
`missions/artifacts/p0_decision_record.md`); D1 (codename) + D3 (firewall lift) carry the operator's planning-session
choice, the rest carry doctrine-aligned defaults. **No build code is written until P1**, and `canvas_std` is **not
touched until P2** under the ratified `adr_007`. The full charter + per-phase design lives in the master doc and the
approved plan; carry technical designs into the P1/P2/P3 mission files at phase entry.
