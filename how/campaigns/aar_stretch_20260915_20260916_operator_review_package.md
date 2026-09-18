---
type: aar
aar_id: aar_stretch_20260915_20260916_operator_review_package
title: "Stretch AAR — the operator-owed tail became four doors, and ADR-011 was wrong twice on the way"
scope: stretch          # ⚠ NOT a campaign AAR — no campaign was chartered for this work
campaign: none
covers: "2026-09-15 → 2026-09-16 · Datum close → operator review package → ADR-011 Amendments 1–3 → the doors"
created: 2026-09-17
updated: 2026-09-17
status: complete
last_edited_by: agent_mondrian
tags: [aar, stretch, adr_010, adr_011, adr_012, iss, ratification, amendment, memo_20, doors, self_correction]
---

# Stretch AAR — the operator review package

> ⚠ **This is a stretch record, not a campaign AAR**, and the distinction is deliberate. No campaign
> was chartered for this work — it was the operator-owed tail after Operation Datum closed. Calling it
> a campaign AAR would invent a structure that did not exist. *(`campaign: none` in the frontmatter is
> the honest value, not a missing one.)*

**Ran:** 2026-09-15 → 2026-09-16, four sittings. **Commits:** `92866fe` · `5a64e5b` · `e44a9aa` ·
`4931819`. **No campaign, no phases, no gates of its own** — the work *produced* gates.

**Shipped:** ISS adopted (`how/federation/iss/`, the fleet's 11th wrapper) · **four operator decision
doors** rendered, with a live receiver and a verified POST round-trip · **ADR-010 erratum** ·
**ADR-011 Amendments 1, 2 and 3** · ADR-012 confirmed needing no change · **memo #20 staged** ·
the memo-allocation procedure amended · doctrine and gate-contract docs updated.

⛔ **Nothing was ratified.** Four verdicts remain pending at the doors, which is the correct state.

---

## Worked

- **Building a decision surface instead of continuing to rule in prose.** Three ADRs had sat
  `proposed` with **no place to sign them**, so every ruling happened in chat and left no artifact.
  Standing Rule 8 already said what to do; it had simply never been done here.
- **Refusing to treat *"your recs are good"* as a signature.** Flipping `status: accepted` on the
  strength of a chat line would have fabricated a ratification record — the exact failure the doors
  exist to prevent, and the one Home hit as `provenance: operator_in_chat`. ⇒ ***an endorsement of
  advice is not a ratification of a decision.***
- **Red-teaming my own recommendations when asked to advise on them.** That instruction produced more
  value than any fresh analysis: it found the defect in the amendment authored the day before.
- **Opening the rendered file.** Twice this caught defects **no content check could**: a stale
  `adr_title` (both strings valid, present, rendering cleanly) and two section titles wrapping
  illegibly while *under* the authoring cap. ⇒ ***validity is not legibility.***
- **Probing by what answers rather than by the status code**, after getting it wrong once.
- **Re-running the verification instead of withdrawing it.** Striking the stale `4/4` transcript would
  have left Decision 3 asserting *"verified"* with nothing behind it.

## Didn't work

- ⛔ **ADR-011 was wrong twice, in two different ways, and both were about SCOPE rather than substance.**
  Amendment 1 fixed a false machine-enforcement claim and added a blanket `production` row; Amendment 2
  found that row was wrong for **194 of 258** canvases; Amendment 3 found the amendments had left an
  **active trap** — an instruction to supply a `source_name` value that *feeds the partition test*, so
  inventing one silently reclassifies a primary canvas as derived.
- **I reported a receiver as "live" on a 307 that was JupyterHub's OAuth redirect.** A status code
  without an identity check. ⇒ ***a probe that confirms something is listening has not confirmed what
  is listening.***
- **I claimed the visual check and then could not perform it** — the browser extension dropped. Said
  so plainly rather than substituting static checks silently, and did it the following round.
- **I piped generator output to `/dev/null` on several renders**, which would have hidden any warning
  it emitted. Caught by re-running with output visible. It had not warned; that was luck, not process.
- **I miscounted unpushed commits again** (said 8, was 9) — the same slip recorded on 2026-09-10 and
  again during Datum.

## The finding

> ⭐ ***A claim left standing beside its own remedy is the most expensive kind of stale, because the
> fix is visible and the claim still reads as current.***

Every substantive defect this stretch was an instance:

| Where | The claim | Its remedy, already present |
|---|---|---|
| `reserved.py` | *"the durable fix is deliberately NOT built here"* | built two days earlier, in the same package |
| `test_axes.py` | *"this is the ONLY thing that reads it"* | a comment that **named its own expiry condition**, reached it, and still needed correcting by hand |
| ADR-011 Decision 4 | *"`canvas_std` does not know the key"* | A-8, cited four screens **above** it in the same file |
| ADR-011 §Verified migration | *"a real value must be supplied"* | Amendment 2's partition, one table-row **below** |
| `STATE.md` | the `production` row as the fix | Amendment 2, written the same day |

⇒ **Corrections propagate to where they are *authored*, not to where the claim is *repeated*.** The
mitigation that worked was mechanical: when striking a claim, grep for its restatements **in the same
pass**, and strike them together — so neither can be "verified" by reference to the other (F-PL-3's
lesson, where two stale figures agreed with each other and with nothing else).

## Change

- **ISS adopted** — Canvas has a decision surface, with `federation_ref` only and **no `substrate_pin`**
  (the fleet exemplar carries both; Canvas removed that duplication at Plumbline P3).
- **Four doors**, a Canvas-rooted receiver, and a POST round-trip verified end to end — including that
  a verdict **clears the `.pending` sentinel**, making `ls how/gates/*.pending` the live owed-list.
- **ADR-011 has a `§What this ADR says today`** block, because the decision had become unreadable
  without reconstructing it from strikes. ⚠ Explicitly a summary, not a replacement.
- **The memo-allocation procedure** gained *a forward reference is a promise, not an allocation*.
- **`.gitignore`** — receiver runtime state, because a **committed** sidecar is worse than none.

## Follow-up

| Item | State |
|---|---|
| **The four verdicts** | ⛔ pending at the doors. Nothing proceeds on 010/012/011/queue until they land. |
| **Memo #20** | staged; delivery is queue section ②'s verdict plus an act-time lease re-probe. |
| **The Armor dogfood** | → **Operation Vernier**, chartered 2026-09-17. |
| **Push** | one commit unpushed; this batch needs its own GO. |
