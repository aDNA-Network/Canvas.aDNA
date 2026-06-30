# CLAUDE.md — Campaign: Operation Lodestar (`campaign_canvas_lodestar`)

## Campaign Identity

| Field | Value |
|-------|-------|
| Campaign | `campaign_canvas_lodestar` |
| Owner | stanley |
| Status | ✅ **completed** (P2 gate resolved 2026-06-30: operator chose Tier 0–3 full-hardening · new campaign **Operation Beacon** · D3=global+aDNA.aDNA registrar · D2=accept no-reopen; review pushed `9f49a6e`) |
| Current Phase | **P2 closed.** Review delivered (3 artifacts in `missions/artifacts/`); operator gated the follow-on → **`campaign_canvas_beacon`** (Operation Beacon, Tier 0–3). |
| Persona | Mondrian (Canvas.aDNA) |
| Predecessor | `campaign_canvas_armature` (Operation Armature, completed 2026-06-23 — closed the three-leg runtime; Lodestar reviews + positions the whole) |

## Quick Start

1. Read this file (auto-loaded in the campaign dir).
2. Read `campaign_canvas_lodestar.md` — the master/charter (goal, context, phases, **seeded gap register**, Decision Points, next-session prompt).
3. At the **P0 gate**, confirm scope + D1–D4 with the operator (that ratification activates the campaign).
4. Run `missions/mission_lodestar_review.md` — three read-only review tracks; create a session in `how/sessions/active/`.
5. HOLD at every phase gate (never auto-advance, SO-1). The review **recommends**; the operator **gates** the build.

## Key Files

| File | Purpose |
|------|---------|
| `campaign_canvas_lodestar.md` | Master/charter — phases P0–P2, **seeded gap register**, Decision Points D1–D4, next-session prompt |
| `missions/mission_lodestar_review.md` | The short-term review mission — three tracks (A technical · B docs · C positioning) + deliverables |
| `missions/artifacts/` | Mission deliverables land here (gap register · positioning assessment · recommendations) |
| `~/.claude/plans/please-read-the-claude-md-playful-rain.md` | The approved charter plan (full design) |

## Standing Orders

- **This is a review, not a build.** P1/P2 are read-only assessment + recommendations. Do **not** write the
  README, new specs, or re-open LIP-0009 inside this campaign — those are the *gated follow-on* the review
  recommends. *(D4: the operator may opt to fold a root-README draft in as a quick win — only on explicit say-so.)*
- **`canvas_std` stays immutable.** Running the conformance harness to verify green is fine; editing
  `what/code/canvas_std/` is not (the firewall holds; `git status -s -- what/code/canvas_std/` clean).
- **Reuse the audit tooling.** `iii/` review framework + `skill_vault_review` + `skill_context_quality_audit`
  + the `canvas-std` harness. No new audit tooling.
- **Evidence-based positioning.** Track C's verdict on canvas-as-primitive (LIP-0009 re-open) must carry
  concrete consumer evidence (the LIP-0009 §3 re-open bar) — assess and recommend; don't decide for the operator.
- **Phase gates are human gates.** SITREP + HOLD; every mission gets a 5-line AAR before `completed` (SO-5);
  archive never delete (SO-6); commit/push operator-gated (Git-Ops §3).

## Context Loading

| Subtopic | When |
|----------|------|
| `campaign_canvas_lodestar.md` (§Gap register, §Decision Points) | Always — the seeded findings + the open questions |
| `what/decisions/adr_000_canvas_identity.md` (the three-leg thesis) | Always |
| `what/decisions/adr_006_canvas_surface_boundary.md` | Track C — the ISS/RLHF boundary |
| `what/context/context_canvas_surface_legs.md` | Track C — the graduated leg principles |
| `what/specs/` (the 10 ratified specs) + `what/code/canvas_std/` | Track A — technical strength |
| `MANIFEST.md` · `who/governance/VISION.md` · `what/docs/` · (absent) root `README.md` | Track B — docs & communication |
| `what/decisions/lip_queue_disposition.md` · LIP-0008/0009 (`Archive.aDNA/lattice-labs/how/governance/lips/`) | Track A/C — standard-debt + the canvas-as-primitive deferral |
| `what/code/canvas_context/` (interaction.py · reconcile.py) | Track C — the RLHF/feedback-signal adjacency |

## Delegation Notes

Chartered 2026-06-30 by a Mondrian/Canvas session after it stood down from the Hearthlight Tier-B rollout
(handed to Home/Hestia) and completed a Canvas-local cleanup. The charter rests on a 3-Explore-agent read-only
recon (technical / docs / positioning) whose findings are **seeded into the master doc's gap register** so the
fresh session starts from evidence, not a blank page. The campaign sits in `status: planning` until the operator
ratifies scope + D1–D4 at the P0 gate (that doubles as activation). Keep it **mini**: one review mission, three
tracks, three deliverables, then an operator gate on the recommended follow-on.
