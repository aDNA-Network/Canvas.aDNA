---
type: session
session_id: session_stanley_20260917_vernier_p0_p1
created: 2026-09-17
updated: 2026-09-17
status: completed
tier: 2
persona: mondrian
operator: stanley
campaign: campaign_canvas_vernier
phase: "P0 (wind-down + charter) → P1 (the Armor dogfood)"
executor_tier: opus
last_edited_by: agent_mondrian
tags: [session, canvas, vernier, armor, bastide, dogfood, sync_hash, a8, provenance, dual_channel, freshness]
---

# Session — the Standard met its first external consumer, and the consumer read a field we never defined

## Intent

Wind down the review-package stretch, and charter **Operation Vernier** on the `Armor.aDNA` dogfood.
Three rulings at the plan gate: **charter a campaign** · **adopt both freshness mechanisms and say
which catches what** · **memo #21 carries findings plus both flags.**

## Cold-start ritual

| Check | Result |
|---|---|
| `git status --porcelain -uall` | **clean** — 0 entries |
| `how/sessions/active/` | empty — **no peer lease** |
| Unpushed | **1** (`4931819`, the doors commit) |
| Firewall | `canvas_std` **0 entries** |
| ⛔ Pending verdicts | **4** — and they must still be 4 at close. This session does not touch them. |
| ISS receiver | live, `:8768`, `gates_root=Canvas.aDNA` |
| Inbound | nothing new in flat `who/coordination/` or `inbox/` |
| HEAD at open | `4931819` |

## Work log

### P0 — wind-down + charter

- **Stretch AAR** written (`how/campaigns/aar_stretch_…md`), ⚠ **labelled a stretch record, not a
  campaign AAR** — no campaign was chartered for that work, and `campaign: none` is the honest
  frontmatter value rather than a missing one. Its finding: ***a claim left standing beside its own
  remedy is the most expensive kind of stale***, five instances.
- **Operation Vernier chartered.** Name: a vernier reads *between* the marks of the main scale.
- **STATE** — §Resume Here, §Current Phase. ⚠ The Datum row's *"No active campaign"* was **struck, not
  deleted**: true when written, false the moment Vernier was chartered, and left visible as a one-line
  instance of the stretch AAR's own subject.

### P1 — the dogfood, every figure re-derived at execution

⛔ Read-only into Armor throughout; their tree untouched.

⭐ **Mostly a pass, and the failures are ours.** Canonical `_reserved` path **7/7** · both A-8 axes
**7/7** · validates at its declared tier **7/7** · source-hash freshness **7/7**, verified **from
outside their vault** with no access to their generator.

⭐ **Hypothesis tested rather than asserted: they are ONE FIELD from aDNA-Native.** Changing only
`conformance_level` → `adna_native` in memory — leaving `adna_version: 2.0.0` untouched to isolate the
variable — makes **all 7 validate `[OK]`**. Their `extended` is a deliberate hold with a stated Phase-D
unblock, so they sit **below a tier they already meet**.

⛩ **V-1** — `sync_hash`: **7/7 source-hash match · 0/7 topology match.** The spec never defines what
the field hashes; A-6 checks shape only. ⇒ *a field with a validated shape and an undefined semantic
will acquire two meanings, and both will pass.* ⛔ Already shipped in both — narrowing breaks a live
consumer.
**V-2** — A-8 gated behind aDNA-Native ⇒ their correct axis pair is inert at `extended`.
**V-3** — `generator` + `title` undeclared (legal, §7.3). `generator` is the word LIP-0010 *removed*
from the authority axis, reinvented as the distinction LIP-0010 was drawing.

**Doctrine**: `context_registry_derivability.md` gains **Principle 4b** — *a validated shape with an
undefined semantic will acquire two meanings*. ⭐ Its diagnostic: **for every field a spec validates,
ask what a second implementer would have to guess.**

## SITREP

**Completed** — Vernier **P0 + P1**. Stretch AAR · charter · P1 artifact · STATE · doctrine.

**In progress** — none.

**Next up** — ⛩ **the V-1 / V-2 / V-3 rulings at the P1 exit gate**, where the firewall ruling is also
taken. Deliberately not pre-decided: V-1 is a choice between breaking our own `compute_sync_hash` and
breaking a live consumer, and that signature should be informed by the measured table.

**Blockers** — none. ⛔ **Four operator verdicts still pending at the doors** — untouched by this
session and not a dependency of P0/P1. Memo **#20** stays staged; **#21** is drafted at P4.

**Files touched** — `how/campaigns/aar_stretch_20260915_20260916_operator_review_package.md` ·
`how/campaigns/campaign_canvas_vernier/{campaign_canvas_vernier.md, artifacts/p1_armor_dogfood.md}` ·
`what/context/context_registry_derivability.md` · `STATE.md` · this file.

## Next Session Prompt

`Canvas.aDNA` (**Mondrian**). **Operation Vernier is ACTIVE; P0 + P1 are closed and the next act is a
human gate** — rule **V-1 / V-2 / V-3** at the P1 exit, where the firewall ruling is taken too. Read
`how/campaigns/campaign_canvas_vernier/artifacts/p1_armor_dogfood.md` first, and **re-derive its
figures rather than trusting them** (the one-line reproduction is in §Reproduce). **V-1 is the load-
bearing one**: `sync.sync_hash` means a *topology* hash in `canvas_std` and a *source* hash in
`Armor.aDNA`, both validate, and the field has **already shipped in both meanings** — so any ruling
must price the migration, and it may be a LIP. V-2 is a tier question (A-8 inert at `extended`); V-3 is
whether to adopt a provenance key. Then P3 (gate #9 gains a source-hash pre-filter, blind spots
published) and P4 (doctrine + **memo #21** to Berthier, findings **with credit first**, plus two flags
that are theirs not ours: Armor has **no git repo**, and it is **absent from the workspace router**).
⛔ **Four operator verdicts are still pending at the doors** and are not Vernier's business. ⚠ The ISS
receiver runs on `:8768`; if it has been stopped, **re-render any gate expecting a verdict** — a stale
sidecar makes gates POST to JupyterHub on 8765.
