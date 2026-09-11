---
type: aar
aar_id: plumbline_campaign_aar
title: "AAR — Operation Plumbline: the ruling cleared the blocker and left us as the blocker"
campaign: campaign_canvas_plumbline
created: 2026-09-11
updated: 2026-09-11
status: complete
last_edited_by: agent_mondrian
tags: [aar, plumbline, authority_axis, production_axis, lip_0010, drift, freshness]
---

# AAR — Operation Plumbline

**Ran:** 2026-09-11, one sitting, five phases (P0–P4), one session, chartered and closed same day.

## Worked

- **Re-deriving before planning, twice, and both times it changed the plan.** The ruling's own
  evidence said *nothing* had cleared (the trigger inverted); the ruling's own **pin** said the
  opposite (the pattern existed). Reading either alone produces a wrong campaign.
- **Ruling the open question from the pattern's text before writing a line of code** (P1). The
  charter refused to assume the split fixed P2b's evidence. It did not need to — three quotations
  settled it, and the answer (*out of scope, so omission is correct*) is better than the answer we
  would have guessed (*add a fourth value*).
- **Letting the tool find the drift.** `dual_channel_freshness` exists because a routine
  regeneration produced a 36-line diff nobody ordered.
- **Verifying every check by derivation, including counterfactuals.** The shim fix was proved by
  showing the *old* code printing `15 … (13 gated)` with a correct verdict — the defect made visible
  rather than described.

## Didn't

- **The first census run reported `0 tracked`** from a `git ls-files` call missing its `--`, and was
  minutes from being published **inside a correction whose entire subject is stale figures**
  (F-PL-5). True figure: 30 of 56.
- **I fabricated an ordinal** — wrote "gate #14 of the runnable manifest" into LIP-0010 when the
  manifest publishes gates by name, not number. Caught on re-read, corrected to `firewall`.
- **I assumed +6 tests where the truth was +5**, and only noticed because the arithmetic refused to
  close (`test_conform` was 13 before, not 12). The assumption was cheap; the *habit* of reconciling
  is what caught it.
- **P3 could not deliver both memos** — SS held two live leases and publishes no drop-box, so #18 was
  staged. ✅ **Resolved inside the same sitting**: the close re-probe found 0 leases and it went. The
  plan said "deliver both" and both were delivered, but only because the close re-probes rather than
  trusting the phase's own finding.

## Finding

⭐ **A ruling can clear a blocker and leave you holding it.** `b1.5` sat with another vault for
eighteen days. When it cleared, the remaining obstruction was entirely ours: the ruled `production`
axis was unknown to every tool we ship, and `conform.py` **required** a field the ruling had just
declined to mandate — because it faithfully implemented **our own draft's** over-reach (F-PL-7).

> ***We escalated to another vault a blocker whose proximate cause was a keyword argument in our own
> module.***

Stated fairly, because the opposite reading is available and wrong: the doctrine work *was* necessary
— E2's finding was independent and real, and a September default would have shipped a hole into 46
vaults. **The doctrine work was necessary; the blockage was not.** Two different claims, and we had
been making only the first.

## Change

- **Gate #9, `dual_channel_freshness`** — the durable fix for F-PL-6, and the first gate in this
  vault that checks an *artifact* rather than a *suite*.
- **Triggers must be evaluable from your own tree.** LIP-0010's old trigger was a claim about another
  vault's decision; its replacement is a file at a path, and it was *run* at the moment of writing.
- **`--markdown` output pasted, never retyped** — held for the third consecutive close.

## Follow-up

| # | Item | Owner |
|---|---|---|
| 1 | **LIP-0010 §7.7 signature** — Option D, v2.4.0, four-file firewall touch named | operator |
| 2 | ~~Memo #18 → SS~~ ✅ **delivered at close** — staged at P3 (2 leases), re-probed at P4 (0 leases) | — |
| 3 | `adr_010` · `adr_011` · `adr_012` signatures (⚠ `adr_012`'s two 2026-09-07 corrections first) | operator |
| 4 | Mermaid trust grant — one click | operator |
| 5 | `idea_memo_number_registry` — filed, not scheduled | Mondrian |
| 6 | **Mention at a pause, do not file**: the gate manifest's upstream case is now stronger (a second, externally-sourced trap) | Mondrian |

## ⚠ What this campaign did NOT do, deliberately

Author or amend `pattern_diagrammatic_context` (not our vault) · touch `what/code/canvas_std/`
(operator-ruled; firewall diff 0 at close) · sweep the fleet for pin fields (unauthorised) · edit
historical records carrying superseded figures (`adr_012` — struck in situ instead) · run tier 2 on
Berthier's population pre-emptively (theirs to commit) · request H4 spend.
