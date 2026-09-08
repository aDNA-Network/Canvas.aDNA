---
mission_id: mission_b3_repin_wave
type: mission
campaign: campaign_canvas_blueprint
phase: P3
title: "The federation re-pin wave — measuring a surface that had been asserted"
owner: stanley
persona: mondrian
status: completed
created: 2026-09-08
updated: 2026-09-08
completed: 2026-09-08
completion_note: "complete-with-open-item — the census, the index correction, the F-HR-1 wiring and 8 of 9 memos all landed; memo #13 to Rosetta is STAGED (their lease was live and they publish no drop-box), Seshat's rename ruling is outstanding (ack_required), and the Amendment-1 render is carried a fourth time."
last_edited_by: agent_mondrian
executor_tier: opus
token_budget_estimated: ~140k
session: session_stanley_20260908_blueprint_p3_repin_wave
tags: [mission, blueprint, p3, federation, repin, wrappers, census, conform, f_hr_1, canvasforge_rename, lockstep]
---

# Mission B3 — the federation re-pin wave

## Gate

Opened at the operator's plan gate, **2026-09-08**. P3 is the last pre-P4 gate of Operation Blueprint.
Memo GO for #12/#13 was pre-authorized at the charter; delivery lands only now that the phase is open.

## Three operator rulings taken at the gate

| Question | Ruling | Consequence |
|---|---|---|
| **P3 shape** | **Re-derive, then offer** | Full measured census first; the index is corrected *to the measurement*; memos are sized to what was found — not the chartered 6-vault wave. |
| **Lockstep dependency** | **Dropped as a dead referent** | Use Canvas's own `spec_federation_contract.md` §3 five-stage re-validation. Pygmalion is *told*, not waited on. |
| **F-HR-1** | **Measure fleet-wide AND wire the hook** | Closes carried STATE item 4. |

## Why the shape changed before a line was written

The charter's P3 row says *"5 stale + 3 misnamed"* and names a 6-vault memo wave. Re-deriving that
census rather than reading it produced four findings, each of which would have mis-sized the phase.

- **F-P3-1 — the wrapper-carrying population is 15 vaults, not the 14 the index records.**
  `WGS.aDNA/how/federation/canvas/` was created **2026-08-10** by `agent_berthier` (pin **2.2.0**,
  `adna_native`, zero grafts, mission RS-D) and **never entered `federation_index.md`**, which was
  updated 2026-08-22 — twelve days later. Canvas had a consumer it did not know it had.
- **F-P3-2 — Oration is recorded as a refusal and is in fact an adoption.** Index §1 carries
  wrapper **NONE**, *"🔴 the G7 enabling condition — adopt-a-wrapper memo staged"*. Kennedy adopted
  **the same day the memo was sent** (2026-08-04, **v2.3.0**, `conformance_target: extended`).
  The index has been reporting our one outstanding federation gap as open for **five weeks after it
  closed**.
- **F-P3-3 — their reply has sat uncollected for 34 days.** `coord_2026_08_04_kennedy_to_mondrian_wrapper_adopted.md`
  is `status: staged_unsent` in **their** outbox under their DP5 (*"delivery is an outward stroke and
  requires operator GO"*). Not a delivery defect — an **uncollected reply**. It carries a correction
  in Canvas's favour and *"two findings that are yours."*
- **F-P3-4 — the charter's own P3 dependency names an artifact that was never built.** *"Adopt
  VisualDNA lockstep-flip mechanics"*: `skill_lockstep_flip` **does not exist**. VisualDNA P4 planned
  8 skills, authored 3 (`agentic_compose`, `create_visualdna_wrapper`, `modular_extend`), and remains
  `STUB_NEXT_SESSION`. The mechanism P3 actually needs has been shipped in *this* vault since
  Keystone — `spec_federation_contract.md` §3.

F-P3-1 and F-P3-2 are the **third and fourth instances this campaign** of the class P2b and P2c each
hit (Operations 5→10 · SS 29→33 · published files 6→7). F-P3-4 is the same class one level up: **a
name that outlived its referent**, cited in a charter for a fortnight without anyone opening the
directory it names.

⇒ *Re-reading a census re-asserts it. Only re-deriving it can contradict it.* Four for four.

## A fifth, arriving from outside

Berthier's reply to memo #10 landed in the drop-box overnight (intaken `6ef9e2d`, byte-unchanged) and
**changes P3's scope**. Operations' tracked canvases pass today **and have no guard**: no canvas check
anywhere in their tree and **no `how/federation/canvas/` wrapper** — while both copies live inside an
Obsidian vault, so the exact re-save that produced `f00bf04` can reach them at any time, silently.
Their phrase: ***"The clean tree is clean by low traffic, not by construction."***

⇒ **Operations is a canvas-emitting vault with no wrapper** — the same shape as Oration's G7 gap,
which the index had recorded as the last of its kind (and which F-P3-2 shows was already closed).
The census must therefore measure **two populations**, not one:

1. **Wrapper-carrying consumers** — are they pinned current, correctly named, correctly identified?
2. **Wrapper-less canvas emitters** — who is producing `.canvas` files with no federation seam at all?

The second population has never been enumerated. It is where the *unguarded* surface lives.

## Objectives

| # | Objective | Status |
|---|---|---|
| b3.1 | Intake the overnight memo; strike memo #10's false premise in our own records | ✅ done — `6ef9e2d` + `mission_b2b` addendum |
| b3.2 | Collect Oration's reply at source; act on the correction and the two findings | ✅ done — collected byte-unchanged; §2.1a written; F-P3-5/6/7 below |
| b3.3 | The measured census — both populations, every figure traceable to a command | ✅ done — `artifacts/p3_federation_census_20260908.md` |
| b3.4 | F-HR-1 fleet measurement + build the collector/pre-publish wiring | ✅ done — +7 tests, `canvas_core` 951→**958/3** |
| b3.5 | Correct `federation_index.md` to the measurement (WGS row · Oration flip · pins) | ✅ done — + new **§1b** and ledger items 6–8 |
| b3.6 | Memos #12 per drifted consumer + #13 → Rosetta; Seshat rename ask | ✅ **8 of 9 delivered**; #13 (Rosetta) **staged** — live lease, no drop-box |
| b3.7 | Gates · records · AAR | ✅ done |

## S1 — what the 34-day-old reply contained

Collected byte-unchanged (`md5 1a5241fa…`, verified at source and destination); their file untouched, its
`staged_unsent` status left alone — theirs to flip. Their tree carries one untracked file of their own and
nothing of ours.

The reply reports the wrapper adopted, the gate honestly at **2 of 3** (render deferred rather than
counted — *"I would rather your gate be accurate than convenient, since ours being convenient is what
started all this"*), and raises two findings. **Both were verified here before being answered. Both turn
out to be already-satisfied — and neither vault could have known.**

- ⛩ **F-P3-5 — Finding 2 was implemented the day before it was written.** Kennedy proposed that
  `CV-FILE-PROPS-01` estimate a file card's rendered height *"from the target's H1 length at 2.3em plus the
  embed header"*, calling it the largest remaining hole in the trap suite. That is exactly what the trap
  does, and has done since **`9224a3f`, 2026-08-03** — the `title_clips` / `content_hidden` conditions and
  the `OBSIDIAN_H1_FACTOR` model, verified present at the creation commit, not merely today. Their memo is
  dated **2026-08-04**. It was built partly *from their own* `canvas_fit_check.py`, absorbed with credit in
  that same commit. ⇒ They have spent five weeks believing the fleet's largest trap gap is open, while
  holding the tool that closes it. **Nobody was wrong; the channel was.**
- ⭐ **F-P3-6 — we paid to rediscover a finding that was sitting in a file we could read.** The reply's
  closing note records that Oration's 13 `CV-HIERARCHY-01/title_slot_missing` mediums fire *because* they
  followed our lead-cost guidance and replaced `##` heads with `**bold**` leads, *"and the trap does not
  recognise a bold lead as a title … a guidance-versus-trap disagreement rather than a canvas defect, and it
  is yours to resolve."* **That is F-P2-9** — which Canvas independently rediscovered and fixed at P2c on
  **2026-09-07**, thirty-four days later. ⇒ *An uncollected reply is not a neutral backlog item. It is a
  finding you will pay full price to rediscover, and the second discovery is indistinguishable from the
  first except that it cost more.* The real price of F-P3-3, made concrete.
- ⛩ **F-P3-7 — Finding 1's premise is wrong, its complaint is right, and the fix was owed to 15 vaults.**
  Kennedy reported that a producer emitting Extended-valid non-native canvases *"has no way to make the
  document self-declare the level it commits to"*, because `_reserved` exists only at aDNA-Native. **Tested
  here rather than accepted:** a `_reserved` block containing **nothing but** `conformance_level:
  "extended"` yields `declared=extended level_reached=extended [OK]`. The key is read at every level; the
  A-checks run only when the declared level *is* `adna_native`. **Their map could have declared Extended on
  2026-08-04.** But their operational complaint is entirely sound — *nothing in the spec said so*, the
  absent-key default is `core`, and they reversed a **correct** ruling on that reading. ⇒ Written up as
  **§2.1a** of `spec_federation_contract` (documentation only; **firewall untouched**), and the §2.1 enum
  corrected `extended | adna_native` → `core | extended | adna_native`.
  ⚠ **Sequencing consequence — this is why S1 precedes the wave.** P3 is about to ask 15 consumers to fill
  in `conformance_target`. Had the memos gone first, we would have shipped a field with a known
  reversed-a-ruling trap in it to every one of them. *(Kennedy's originally intended finding was "the §2.1
  enum is too short"; they withdrew it when their premise dissolved and reported the withdrawal instead of
  silently substituting a better finding. The withdrawn finding was correct anyway, for a reason neither
  desk had.)*

## S3 — F-HR-1: the half that was never built

P2b shipped `normalize_edges` and scoped the wiring. This builds it, in the one place the defect is
actually made durable.

**The mechanism, stated exactly.** A review surface is emitted conformant → a human opens it in
Obsidian → Obsidian's re-save rewrites the `edges` block **without** the explicit `toEnd` keys → the
canvas still renders perfectly and now fails C-4 → **the collector reads that document, folds the
verdicts in, and writes it back.** Without the fix, *the collector is the step that makes the damage
permanent.* Normalizing between the read and the fold means the write-back **repairs** in the same act
that records the verdict.

**Wired** into `canvas_core/rlhf/review_collect.py::collect` (`normalize=True` default, `--no-normalize`
audit opt-out). Counts gained `edges_normalized` + `edges_unresolved`; the CLI prints both.

⚠ **Two design constraints, both from a peer's ruling, both tested.**

1. **Idempotency is preserved, deliberately.** The normalized doc is persisted **only when the
   collector was already going to write**. A pass with nothing to collect stays a true no-op on disk —
   that property is load-bearing and pinned by `test_rerun_is_a_no_op`. An un-conformed surface with no
   pending verdicts is therefore **reported and not silently rewritten**. This follows Berthier's
   answer to our own Q2 (2026-09-07): their projection is hand-maintained with **no regenerator**, so
   the normalize pass wants to run **before publish**, not as a side effect of somebody else's read.
   ⇒ *We asked where the hook belongs; the consumer's answer changed where we put it.*
2. ⛔ **`unresolved_edges` reports and never repairs** — pinned by a test asserting the dangling edge
   **survives** the pass. Vindicated at fleet scale this session: exactly **one** genuinely unresolved
   edge exists across 106 peer canvases, and ruling on it took a **history walk in another vault**
   (`git log --all -S` proving the target never existed as a node in any committed revision). No
   normalizer could have known that. Berthier: *"your tool was right to refuse it."*

**The defect reproduced in fixtures, never in copies** (`_obsidian_resave()` mutates the test fixture):
Canvas.aDNA is public, and the vault where this was first measured gitignores its copy (`adr_012`).
A test asserts the **premise** first — that a pure re-save really does produce C-4 and nothing else —
so the fix is not tested against an assumption.

**Verified live**, not only in fixtures: a dry run against the real HR pilot surface
(`what/artifacts/review_surface_pilot/ss_variant_review.canvas`) reports `0 normalized` (it was repaired
at HR gate 3/3 and has stayed conformant), `skipped: 6`, and **md5 unchanged** — reproducing STATE's
recorded pilot result exactly.

`canvas_core` **958/3** (was 951/3; +7). Two pre-existing tests asserted the counts dict by exact
equality and were **updated to name the two new fields rather than loosened** — on a healthy surface
both are 0, so the assertion now also catches our own builder emitting non-conformant edges.

## Standing constraints

- **Offer, never write** (Rule 10). Every consumer vault read-only; quiescence re-probed at act time;
  memos left untracked for the recipient's read-receipt.
- **Firewall**: `git diff --stat -- what/code/canvas_std/` empty at the gate. No LIP is in scope.
- **`_reserved` / `authority` tier stays HELD on `b1.5`** — F-P2b-5 stands: no value fits a
  hand-authored canvas, and `canvas_std` accepts a wrong one **silently**. Berthier explicitly
  endorsed the withholding; that is a reason to keep holding, not to relax.
- **Defect signatures reproduce in fixtures, never in copies** — Canvas is public (`adr_012`).
- **State the population on the face of the number** — tip or history · class or literal · tracked or
  working-tree. Out-of-scope sets are *named*, not quietly excluded.

---

## Gates (2026-09-08)

| Gate | Result |
|---|---|
| `canvas_std` firewall | **diff 0** — no schema change; no LIP in scope |
| `canvas_std` | **115 / 10 skipped** |
| certification | **11 / 11 fixtures agree** |
| `canvas_core` | **958 / 3** (was 951/3 — **+7**, the F-HR-1 wiring) |
| producers (7) | **267** — 10 · 16 · 37 · 44 · 123 · 17 · 20 |
| `comic_render` | **154 / 2** |
| peer-vault writes | **zero** — no `.canvas` outside this vault modified today; memos left untracked |
| census re-derived at close | **11 of 11 published figures reproduce exactly** |

**No canvas was authored this session** — a census, a spec section, a collector hook and nine memos.
So no per-canvas visual gate applies, and the Amendment-1 render remains **carried, not met** (P2 → P2b →
P2c → P3): still no safe window-scoped capture path on this node.

## AAR

**Worked.** Re-deriving before writing, again — and this time it was the *charter itself* that failed the
check. Four of the phase's findings existed before a line of work was done, simply because opening the
directories a plan cites is cheaper than trusting them. The single highest-value act of the session cost
about ninety seconds: `find VisualDNA.aDNA -iname "*lockstep*"` → empty.

**Didn't.** I wrote *"memo #12 delivered 2026-09-08"* into two index rows **before sending anything**, and
caught it only on re-reading my own diff. That is the identical failure this phase exists to correct — a
record running ahead of the thing it records — committed by the agent writing the correction. It was also
nearly a third: I almost published *"21 dangling edges fleet-wide, a 21× increase on P2b"*, a figure
literally derived from our own validator's output and false as a class claim, because `C-3` is a **bucket**
of four edge defects and 20 of the 21 were invalid `"center"` side values in one file. Both were caught by
asking *what does this number actually count* — neither by any gate.

**Finding.** The federation surface was being **measured on the wrong axis**. Membership of the index meant
*"holds a wrapper"*, so the ten vaults emitting canvases with no seam at all — the least supervised in the
fleet — were invisible to it **by construction**, and a peer had to tell us (*"the clean tree is clean by
low traffic, not by construction"*). A registry defines its own blind spot in its membership rule, and no
amount of diligently maintaining it will surface what it was built not to see.

**Change.** F-HR-1 closed where the damage was actually made durable — the collector was the step
persisting the Obsidian re-save, and it now repairs in the same act that records the verdict, with
idempotency preserved and the hook placed **before publish** for hand-maintained consumers on Berthier's
ruling rather than our own preference. `federation_index` corrected in both directions with §1b added.
`spec_federation_contract` §2.1a written on a consumer's finding that had cost them a reversed ruling.
Eight memos delivered, one honestly staged.

**Follow-up.** *(a)* **#13 to Rosetta is staged** — re-probe their lease next session; the same condition
refused E2 for two days at P2 and cleared on the third. *(b)* **`ack_required: true` from Seshat** — the
`canvasforge/` rename ruling is the only outstanding ask of this wave. *(c)* The **bold-lead-as-title**
question is ours and unruled: Kennedy framed it as guidance-vs-trap rather than a canvas defect, and
`CV-HIERARCHY-01` still does not accept a bold lead as a title. *(d)* **LAVentureGraph's two duplicate node
ids** — reported, theirs to rule on; worth a follow-up read because a duplicate entity id in an entity graph
outlives the canvas it was found in. *(e)* Amendment-1 render, carried a fourth time. *(f)* `b1.5` remains
open on Rosetta; **four** artifacts now sit with them, of which one is deliberately withheld.

⭐ **The finding that outlives this mission.** An uncollected reply is not a neutral backlog item — Kennedy's
sat 34 days and contained, in its closing paragraph, the exact defect we independently rediscovered and
fixed as F-P2-9 a month later at full cost. Two of their three findings were *already true when written*,
one of them shipped the day before, built partly from their own contributed tool. **Nobody in this exchange
was wrong about anything. The channel was.** That is the argument for the drop-box, made in arrears and paid
for in a session.
