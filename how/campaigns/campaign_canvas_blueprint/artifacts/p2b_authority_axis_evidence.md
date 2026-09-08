---
type: artifact
artifact_id: p2b_authority_axis_evidence
campaign: campaign_canvas_blueprint
phase: P2b
mission: mission_b2b_conversion_offers
title: "Authority-axis evidence from the first real consumer conversion — E2's finding, met in the wild"
created: 2026-09-07
updated: 2026-09-07
status: active
blocks: b1.5
last_edited_by: agent_mondrian
tags: [artifact, blueprint, p2b, authority, e2, b1_5, rosetta, lip_0010, evidence]
---

# The authority axis has no value for a hand-authored canvas

**Status: evidence for `b1.5`, held — deliberately NOT dispatched as a fourth memo.** Three
artifacts already sit unanswered with Rosetta (memo #9 2026-08-22, erratum v2 2026-08-24, E2
2026-09-07). Adding a fourth before any of the three is answered would be noise, not signal. This
file is the evidence to fold into `b1.5` **when they rule**, and the campaign's standing position is
unchanged: *the phase does not advance on their silence.*

## What happened

P2b's conversion work needed an `authority` value for eight real canvases in two other vaults —
Operations' C08 teaching diagrams and ScienceStanley's site-polish review boards. The producer-side
enum accepts exactly three (`skill_canvas_context_diagram` §1):

| Value | Means | Fits these files? |
|---|---|---|
| `view` | a visualization of an authoritative `.lattice.yaml` (`adr_011`) | ❌ there is no `.lattice.yaml` behind them |
| `generator` | a build product of a machine source | ❌ nothing generated them; a human placed every node |
| `dual_channel` | prose owns meaning, canvas owns structure, both update together | ❌ no `.md` pair exists, and `prose:` is legal only under this value |

**All three are wrong.** These canvases are the primary artifact: hand-authored, authoritative in
themselves, with no upstream source and no prose twin. The axis has no cell for them.

⚠ **I used `view` as a placeholder in the trial run and it was wrong.** It is recorded here because
it is exactly the failure mode F-B1-2 predicts: `canvas_std` does not validate `authority`, so
`view` was accepted silently on all eight files, and nothing but reading the diagram would have
caught it. An invented value and a wrong-but-real value are indistinguishable to every tool we ship.

## Why this is E2, not a new finding

Erratum **E2** (2026-09-04, to Rosetta) said the authority axis *"mixes who owns the meaning with how
it is produced"* — derived from Canvas's own two dogfood canvases, which are `dual_channel` **and**
machine-generated at the same time. That was an internal observation about an overlap.

This is the same defect seen from the other side: not two values that both apply, but **three values
where none does.** An axis that both double-covers and under-covers is not a taxonomy that needs a
fourth value bolted on — it is one axis doing two jobs. E2's proposed split (*meaning-ownership*
separate from *production-mode*) resolves both symptoms; a bare `authored` value would resolve only
this one.

⇒ **This strengthens E2's recommendation; it does not open a new question.** No new LIP is proposed.
LIP-0010 (validate `authority` as an enum, Option B, additive, v2.4.0) stays **recommended and
deferred**, gated on Rosetta ratifying the pattern — and this evidence raises its value, because a
validated enum with the *wrong cells* would have accepted `view` here just as silently.

## The consequence that mattered for the offers

The conversion splits into two tiers, and only the second is blocked:

| Tier | Operation | Doctrine decision needed? | Result on the 8 measured files |
|---|---|---|---|
| **1** | `conform.normalize_edges` — explicit `toEnd` | **none** | 7 of 8 → `extended [OK]`; 40 of 41 errors cleared |
| **2** | `conform.uplift_to_adna_native` — the `_reserved` block | **yes — an `authority` value** | reaches `adna_native`, but only once the axis is ruled |

So the memos offer **tier 1 now** — mechanical, reversible, no judgement, no dependency on any open
question — and describe tier 2 as available *when the authority question is settled*, naming the
question rather than quietly picking a value on a consumer's behalf. Shipping `authority: "view"`
into two vaults to make a number go green would have been the same error class as the census's own
F-P2b-1: a claim that validates cleanly and is not true.

## Firewall

No schema change taken. `git diff --stat -- what/code/canvas_std/` = 0 at open and close of this
session (campaign standing order; only a ratified LIP may touch the firewall).
