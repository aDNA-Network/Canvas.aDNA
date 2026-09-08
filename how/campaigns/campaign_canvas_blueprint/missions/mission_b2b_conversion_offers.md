---
mission_id: mission_b2b_conversion_offers
type: mission
campaign: campaign_canvas_blueprint
phase: P2b
title: "The conversion offers — and the defect class that turned out to be ours"
owner: stanley
persona: mondrian
status: completed
created: 2026-09-07
updated: 2026-09-08
completed: 2026-09-07
completion_note: "complete-with-open-item — both offers delivered with a working tool and re-derived figures, but the `_reserved` tier of each offer is held pending the authority-axis ruling (b1.5, Rosetta), and F-HR-1's normalize-on-collect wiring into the collector is scoped, not built. ⛩ Addendum 2026-09-08 (Berthier's reply): every figure reproduces first-party; memo #10 §5 Q1's premise is STRUCK — the projection carries its own .git and is pushed; the defect class now has a commit/author/date (f00bf04, 2026-07-22); C-3 disposition = delete; Q2 closed (hook is pre-publish); Operations is a wrapper-less canvas emitter → P3 census scope."
last_edited_by: agent_mondrian
executor_tier: opus
token_budget_estimated: ~120k
session: session_stanley_20260907_blueprint_p2b_conversion_offers
tags: [mission, blueprint, p2b, conversion, operations, sciencestanley, conform, c4, f_hr_1, authority, addendum_20260908, premise_struck]
---

# Mission B2b — the conversion offers

## Gate

Opened at the operator's plan gate, **2026-09-07** (second session that day; the first closed P2c).
P2b is the **deferred half of P2** — `mission_b2`'s AAR sequenced it deliberately *behind* the
producer re-gate, on the reasoning that *"offering conversions while our own shelf fails the gate
repeats the credibility problem the dogfood just fixed."* P2c discharged that this morning.

Memo GO for #10/#11 was pre-authorized at the charter; per-phase delivery lands only now.

## What the mission set out to do, and what it actually found

**Intended:** convert five standard-blind Operations canvases and twenty-nine bare ScienceStanley
files, offer the conversions, done.

**Found:** the scope figures were both wrong, the two vaults share **one** defect class, and that
class is one Canvas diagnosed in its own vault a fortnight ago and has been carrying as an internal
housekeeping item ever since.

Census: [`../artifacts/p2b_conversion_census_20260907.md`](../artifacts/p2b_conversion_census_20260907.md).

## Objectives

| # | Objective | Status |
|---|---|---|
| b2b.1 | Re-derive the census before writing any memo | ✅ done — 10 (not 5) and 33 (not 29) |
| b2b.2 | Characterise the Operations two-copy divergence | ✅ done — F-P2b-1/F-P2b-2 |
| b2b.3 | Build the worked conversion as a **tool**, not a snapshot | ✅ `canvas_core/conform.py` + 13 tests |
| b2b.4 | Record the authority-axis gap as b1.5 evidence | ✅ [`../artifacts/p2b_authority_axis_evidence.md`](../artifacts/p2b_authority_axis_evidence.md) — **held, not dispatched** |
| b2b.5 | Memo #10 → Berthier (Operations) | ✅ delivered |
| b2b.6 | Memo #11 → ScienceStanley | ✅ delivered |
| b2b.7 | Gates + records + AAR | ✅ done |

## Findings

- **F-P2b-1 — "md5-differ" is a literal measurement; "diverged" is a class claim.** I wrote the
  second into the session plan while holding only the first, four hours before re-deriving it. Two
  of the five Operations pairs are byte-different and *semantically identical*. Same class as
  F-P2-8; the fix is the same one, applied this time to my own fresh number.
- **F-P2b-2 — the F-HR-1 mechanism is not ours alone, and that changes its priority.** Three
  Operations files lost **100%** of their explicit `toEnd` keys (8/8→0, 5/5→0, 5/5→0) and five
  ScienceStanley boards show the same omission: the signature of an Obsidian re-save, which Canvas
  diagnosed at HR gate 3/3 on 2026-08-23 and has carried through P2 and P2c as *"a `canvas_context`
  interaction concern."* It is not an internal concern. **40 of the 41 conformance errors across
  both vaults are this one class**, in files nobody noticed were failing — because they still render
  perfectly. The normalizer is the fix that keeps a conformant canvas conformant across a human
  editing pass anywhere in the fleet.
- **F-P2b-3 — 9 of the "bare ScienceStanley files" are Canvas's own output**, from the
  `canvas_comic` producer Canvas archived at Halftone (`adr_009`). Today's `comic_generator` emits
  canonical `_reserved`. The offer for that class is regeneration, and the framing is disclosure.
- **F-P2b-4 — the offer splits at the doctrine line, and only half of it is blocked.**
  `normalize_edges` takes 7 of 8 files from FAIL to `extended [OK]` with **zero judgement calls**;
  the `_reserved` uplift needs an `authority` value that does not exist for a hand-authored canvas.
  Offering tier 1 now and naming tier 2's blocker beats picking a value on a consumer's behalf.
- ⛩ **F-P2b-5 — I nearly shipped `authority: "view"` into two vaults.** It was a placeholder in the
  trial run and it is **wrong** for every one of these files. `canvas_std` accepted it silently on
  all eight (F-B1-2 exactly as predicted: an invented value and a wrong-but-real value are
  indistinguishable to every tool we ship). Caught by reading the diagrams, not by any gate.
  ⇒ *A validating tool that does not know a key cannot tell you that you used it wrongly — and a
  green result on a key nobody validates is not evidence, it is silence.*

## Deliverable — `canvas_core/conform.py`

Three functions, separated by **how much judgement each needs**:

| Function | Judgement | Result on the 8 measured files |
|---|---|---|
| `normalize_edges` | none — mechanical | 40 of 41 errors cleared; 7 of 8 → `extended [OK]` |
| `unresolved_edges` | reports only, **never repairs** | surfaced the 1 real defect and left it standing |
| `uplift_to_adna_native` | an `authority` + a source name | reaches `adna_native`; held on b1.5 |

`unresolved_edges` deliberately does not repair. Whether a dangling edge should be deleted,
re-pointed, or kept as evidence that a node went missing requires knowing what the diagram is *for*
— and a normalizer that silently deleted edges would be the most dangerous tool in the vault.

Reproduced the defect signature in fixtures rather than copying anyone's files: the Operations
projection copy is **gitignored by its owner** and Canvas.aDNA is public (`adr_012`).

## Gates

`canvas_core` **951/3** (was 937/3: +13 `conform` +1 S-4 pin, 1 inverted) · `canvas_std` **115/10** ·
certification **11/11** · producers **267** · `comic_render` **154/2** · **firewall diff 0** ·
both consumer vaults **read-only throughout** (Rule 10) · both quiescent at delivery (0 active
leases, re-probed at act time).

## AAR

**Worked.** Re-deriving the census before writing a word of any memo. Every substantive finding in
this mission came from that step, and the memos are unrecognisably better for it — they carry a
measured defect class and a working tool instead of a conversion proposal.

**Didn't.** I wrote *"divergence, not duplication"* into the session plan on an md5 comparison alone,
and used `authority: "view"` in a trial run without checking it meant anything. Both were caught
here, but both were mine, and both are the same error: treating a result that *validates* as a
result that is *true*.

**Finding.** The dominant defect class in two other vaults was one we had already diagnosed in our
own and filed as internal housekeeping. Carried items are not neutral — an open item described as
*"a `canvas_context` interaction concern"* for a fortnight was, the whole time, the fleet's most
common conformance failure.

**Change.** `conform.py` exists and is offered rather than described. The authority-axis gap is
recorded as b1.5 evidence and **held**, not dispatched as a fourth unanswered memo to Rosetta.

**Follow-up.** *(a)* Wire `normalize_edges` into the collector — the actual F-HR-1
*normalize-on-collect*, still scoped rather than built; carried STATE item 4 now has a normalizer to
wire. *(b)* The `_reserved` tier of both offers unblocks when Rosetta rules the authority axis
(`b1.5`). *(c)* SS class (b) regeneration — the 9 comic canvases — needs the M-PL3
resurrect-vs-repoint decision, which is Canvas-side and still open. *(d)* Amendment-1 render still
has no safe path on this node (carried from P2).

---

## Addendum — 2026-09-08, on Berthier's reply (intaken `6ef9e2d`, byte-unchanged)

Operations answered memo #10 overnight into the drop-box. **Every figure in the memo reproduces
first-party** — 5/5 `[OK]` tracked, 3 `[FAIL]`/20 errors on the projection, the `toEnd` collapses
5/5→0/5, 5/5→0/5, 8/8→0/9, and the C-3 target in neither copy. Four things change or extend the record.

⛔ **A false premise of ours, struck.** Memo #10 §5 Q1 asserted that `what/c08-liaison-package/` is
gitignored *"so that layout exists in exactly one place and is not in version control."* **Wrong.**
It is gitignored **by the vault** *and* carries **its own `.git`** — origin
`aDNA-Network/C08-LIAISON-package`, a live shared repo with a PR workflow and merged PRs from a
second operator. Nested-repo by design; the vault's `.gitignore:33` keeps the two histories separate,
it does not leave the layout unbacked. The layout is committed **and pushed**.

⇒ The generalisable error is not "I misread a `.gitignore`". It is that **`gitignore` is a statement
about one repository's index, and I read it as a statement about the file's existence in version
control anywhere.** A nested repo makes those two readings come apart, and nothing in the measurement
I ran could have distinguished them — I never looked for a second `.git`. *Same family as F-P2b-5:
a true local observation carried into a global claim it does not support.*
**The sent memo is not edited** — correspondence is a record (`adr_012`). The claim is struck here,
where it would otherwise be carried forward.

⭐ **The defect class now has a commit, an author and a date.** `f00bf04` · `jjoyner` ·
2026-07-22 23:20 -0700 · *"canvas: layout adjustments (Jake, in Obsidian)"* — **one commit performs
both halves**: it rewrites the entire `edges` block without the explicit key (×8, every edge) *and*
introduces the dangling edge, on the day C08 closed. F-HR-1 stops being an inferred signature and
becomes an **observed mechanism with provenance**. That is materially stronger evidence for the P3
wave than anything Canvas could produce from its own tree.

⭐ **The C-3 edge: disposition DELETE, and the tool was right to refuse it.** `git log --all -S` finds
the id in exactly one commit and **never as a node in any committed revision**; the other ten ids are
hand-authored slugs, this one is Obsidian-generated hex. The target never existed — created and
deleted inside a single editing session. Berthier's note on `unresolved_edges`: *"your tool was right
to refuse it … because it took a history walk to establish that the target never existed. A tool
could not have known that."* The reports-never-repairs split is vindicated by a case that **only**
history could settle. ⛔ The act is not Operations' to take either — it is a peer operator's commit on
a shared `origin/main`; it routes to him by PR, at his tempo.

✅ **Q2 closed by them:** there is no regenerator (hand-assembled once at S98, one re-projection at
M-C08-2), so `normalize_edges` belongs **before publish**, not at projection time. This directly
constrains S3's wiring: for a hand-maintained consumer the hook is *pre-publish*, not *on-collect*.

⭐ **And a finding they filed against themselves, which becomes a P3 item.** Their **tracked** five
pass today **and have no guard**: no canvas check anywhere in their tree and **no
`how/federation/canvas/` wrapper**. Both copies live inside an Obsidian vault, so the re-save that
produced `f00bf04` can reach the tracked five at any time, silently, because the file still renders
perfectly. Their words: ***"The clean tree is clean by low traffic, not by construction."***
⇒ Operations is a **canvas-emitting vault with no wrapper** — the same shape as Oration's G7 gap,
which the federation index had recorded as the last of its kind. P3's census must therefore measure
**emitters without wrappers**, not only wrapper-carrying consumers. Carded their side as
`20260907220000`, citing F-HR-1 as prior art.

*(Also reported against themselves, unprompted: their standing session-open fetch of the shared
projection had lapsed 14 days — so Canvas measured their shared repo more recently than they did.
And a caveat they raised against our result and then disproved by measurement — our five pairs are
byte-identical to `origin/main` — reported anyway, "because a doubt raised about a peer's number and
then privately resolved is not the same as one that was never raised.")*
