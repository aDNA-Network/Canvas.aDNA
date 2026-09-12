---
type: lip
lip_number: "LIP-0010"
title: "Diagrammatic context — the `authority` / `production` axis split (assessment → Standard proposal, v2.4.0)"
author: "Stanley Bishop (Mondrian-drafted; Canvas.aDNA standard-bearer)"
status: accepted
created: 2026-08-24
updated: 2026-09-11
requires: []
replaces: []
last_edited_by: agent_mondrian
resolution: "Option D ACCEPTED 2026-09-11 (§7.7 signed by the operator at the Operation Gridline plan gate) — two optional validated keys, additive, v2.4.0; supersedes Option B, whose MECHANISM survives and whose CELLS do not. The 2026-08-24 trigger was INVERTED, not fired; the rewritten trigger is a file at a path and it has already fired. Implementation runs as campaign_canvas_gridline P1-P4; `implemented` on the firewall commit, `final` on the v2.4.0 cut. ⛩ The signature does NOT cover F-GL-1 (`RESERVED_KEYS` has no consumer, and `interaction` was never in it) — that is a P1 gate question, outside Option D's table."
related: ["adr_011_legacy_canvas_interop_reconciliation", "pattern_diagrammatic_context", "p1_under_coverage_ruling"]
tags: [lip, assessment, proposal, canvas, canvas_standard, diagrammatic_context, authority, production, axis_split, blueprint, p1, plumbline, p2]
---

# LIP-0010: Diagrammatic context — the `authority` / `production` axis split

> **Opened as an assessment** in the LIP-0009 mould (Operation Blueprint P1, `mission_b1_doctrine`,
> 2026-08-24): it asked whether a doctrine needs a schema change, and its "implementation" could
> legitimately have been the status quo.
>
> ⛩ **Converted to a Standard proposal at Operation Plumbline P2, 2026-09-11**, when the doctrine it
> was waiting on was ruled. **Still `draft`, and still no change taken** — `what/code/canvas_std/` is
> at diff-0 and stays there until an operator signs (§7.7). *Doctrine settles, then the machine
> enforces it* was this LIP's own ordering argument; it applies to the conversion too.

---

## §0 · Two inversions, and neither was visible without re-deriving

**This section is first because reading the ruling produces a wrong plan twice over.**

### Inversion 1 — the trigger was inverted, not fired

The 2026-08-24 trigger below is a **conjunction**:

> *"Rosetta ratifies `pattern_diagrammatic_context` **with `authority` still normative** **and** the
> **three-row set stable**."*

The ruling of 2026-09-11 breaks **both** conjuncts. §3 amendment 1 **splits** the axis (*"we are not
adopting a three-value enum that answers one-and-a-half of them"*); §3 amendment 2 rules `authority`
**doctrine-enforced, not machine-enforced** — *"until your LIP-0010 rules."*

⭐ **The two conditions were written pointing at each other.** Our trigger waited on their ruling;
their ruling defers the enforcement clause to ours. Neither desk was stalling — the cycle is
structural, and it is broken only by **an artifact existing**. That is why the rewritten trigger names
a file rather than a decision.

### Inversion 2 — the memo was stale in that exact claim, and carried the proof

The ruling states `pattern_diagrammatic_context.md` is **NOT YET AUTHORED** (24 patterns in
`aDNA.aDNA/what/patterns/`, not among them) and pointedly declines the word *"routed"*: *"you will
know it exists when it exists."*

Evaluated from our own tree at intake: **26** patterns, and **the file is among them** — authored at
`67ad713`, **the commit immediately after `860c59e`, the head the memo itself pins** as *"superseded
when: our next commit."*

> ⇒ ***A memo is a measurement with a timestamp.*** True at 00:55Z, false when read. Believing the
> sentence instead of evaluating the pin would have left this LIP deferred against a blocker that had
> already dissolved — and the pin that disproved it was in the same document.

### What the ruling actually settled

| Axis | The question it answers | Values |
|---|---|---|
| **`authority`** | *Who owns the meaning?* | `dual_channel` · `view` |
| **`production`** | *How is the picture made?* | `hand_authored` · `generated` |

⭐ This is **E2's larger fix** — the two-field shape Canvas *named and explicitly declined to propose*
on the reasoning that it was a schema change. The ruling answers that objection directly, and the
answer is the load-bearing sentence for everything below:

> *"The split therefore costs no schema change, which is what makes it adoptable today: adding a
> sibling key to a key nothing validates changes nothing a validator sees. Canvas declined to propose
> the two-field shape on the reasonable reading that it was a schema change; **it is one only once
> LIP-0010 makes either key binding, and at that point both become binding together.**"*

**So this LIP is exactly where the schema change lives, and it is now a two-key change or none.**

## The question

Operation Blueprint's charter locks a **default of no `canvas_std` change**: Emacs.aDNA has run the
dual-channel pattern for 13 months on Standard 2.3.0 unmodified, which is strong evidence the
substrate suffices. P1 must nevertheless *reason* to that conclusion rather than assert it.

Measuring the corpus (ADR-011) surfaced one place where the proposed doctrine and the shipped
Standard genuinely disagree.

## Finding: `authority` is load-bearing in doctrine, invisible to the machine

`pattern_diagrammatic_context` makes the field normative:

> Every diagrammatic-context canvas declares its authority in `_reserved` … `none` is retired: a
> canvas with no declared authority is nonconformant diagrammatic context.

`canvas_std` does not know the key:

| Check | Result |
|---|---|
| `authority` referenced in `canvas_std/src/` | **no** — only in `roundtrip.py` docstring prose, never as a key |
| A-2 validated keys | `adna_version`, `conformance_level` only |
| Behaviour of `authority: "veiw"` | **accepted silently** — passes as an additive `_reserved` extension |
| ~~`adna_native` canvases in-vault carrying `authority`~~ ~~**0 of 21**~~ | ⛩ **STALE — re-derived 2026-09-11: `4 of 25`.** Physical census, 56 `.canvas` files (30 tracked / **26 untracked** under gitignored `what/artifacts/`). ⚠ **The complement is still exactly 21** — 21 of 25 do *not* carry the key — so this row re-derives as a true number and reads as reproduced. **It did not reproduce.** |
| ⛩ **NEW — where the enum is actually enforced** | **two places, both ours, both on the superseded axis**: `canvas_core/conform.py:50` `VALID_AUTHORITIES` (raises; `authority` is a *required* arg) and `diagram_generator/model.py:40` `AUTHORITY_MODELS` (raises at `:91`, cross-checks `prose ⇒ dual_channel` at `:95`, 6 tests). `canvas_std` does not know the key; **producers do.** |

So the pattern would declare a field mandatory that no tool requires, whose values no tool checks,
and which none of the Standard's own 21 conformant canvases currently carry. That is a real gap —
recorded here rather than papered over.

> ⛩ **Amended 2026-09-11.** Two clauses above are now false and are struck rather than rewritten,
> because *what was believed on 2026-08-24* is the reason the recommendation was what it was.
> **(i)** *"whose values no tool checks"* — two of our own producers check them (table row above);
> the measurement was `canvas_std`-scoped and the sentence generalised past it.
> **(ii)** *"none of the … 21 … currently carry"* — **4 of 25** carry it today.
> ⭐ **And Rosetta did not adopt the mandate.** The ruled pattern states it *"does not declare a
> canvas without a stated authority nonconformant"*, on this LIP's own reasoning — so the gap this
> section names was closed **by the doctrine moving**, not by the machine. The `authority` half of
> Option B's motivation is therefore weaker than when written; the *`production`* half is new.

## Options

**Option A — No change (the charter default).**
`authority` remains doctrine-enforced: caught at gate review (REQ-O05 canvas-sync review), not by
`canvas-std validate`. Zero firewall risk, zero migration.
*Cost:* the pattern's central normative claim has no machine backing; typos and invented values pass.

**Option B — Optional validated enum (additive, minor bump → v2.4.0).** ✅ *recommended, deferred*
Add `authority` to the A-2 block as **optional**, validated *only if present*, against the closed set
`{dual_channel, generator, view}`. Backward-compatible: ~~all 21 existing `adna_native` canvases keep
passing untouched~~ (⛩ **re-derived 2026-09-11: all 25 keep passing *under this three-value set*** —
but see below, because that is no longer the ruled set); the legacy `view` value validates as-is after
the ADR-011 migration. Precedent: `AFFORDANCE_KINDS` in `reserved.py` is exactly this shape — a closed
enum on an optional block.
*Cost:* a firewall touch, therefore a real LIP through its own §7.7 gate.

> ⛩ **SUPERSEDED IN ITS CELLS 2026-09-11 — retained in its mechanism.** Rosetta split the axis, so
> `generator` is no longer an `authority` value at all; it is an answer to *how is it produced*.
> Validating `{dual_channel, generator, view}` today would **harden into the Standard the exact
> conflation the doctrine has just ruled out** — the migration this deferral existed to prevent,
> arriving one ruling late. ⚠ And the backward-compatibility claim dies with the set: **2 of the 4
> carriers** (`what/artifacts/b4_*_fixture/`, both `generator`, both untracked) would be carrying a
> *production* value in an *authority* field. **The shape survives; the cells do not.** See **Option D**.

**Option C — Require `authority` on every `adna_native` canvas.** ❌ rejected
~~**Breaking: 21 of 21**~~ ⛩ **re-derived 2026-09-11: `21 of 25`** in-vault conformant canvases would
fail immediately, plus Emacs's c01–c06 and every producer's output. A major bump to make a field
mandatory that the ecosystem has never emitted. Not proportionate.

> ⚠ **Read this correction and the Finding-table one together, or you will "fix" one by reference to
> the other.** They are **mirror images**: the Finding row's *numerator* moved (`0 → 4`) while its
> denominator's complement stayed 21; this row's *numerator* stayed 21 while its **denominator** moved
> (`21 → 25`). Both rows read "21" before and after. ⇒ ***two stale figures can disagree with reality
> in opposite directions and still agree with each other.*** Option C stays ❌ **rejected** — the
> ruling makes it moot anyway: the pattern explicitly declines to mandate the field.

**Option D — two optional validated keys (additive, minor bump → v2.4.0).** ⛩ ✅ **RECOMMENDED
2026-09-11**, superseding Option B.

The shape Option B established, applied to the axes the doctrine actually ruled:

| Key | Placement | Validated against | Required? |
|---|---|---|---|
| `authority` | `metadata.frontmatter._reserved` | `{dual_channel, view}` | **no** — only if present |
| `production` | `metadata.frontmatter._reserved` | `{hand_authored, generated}` | **no** — only if present |

**Backward-compatible, measured rather than asserted** `[D] 2026-09-11`: **25** in-vault `adna_native`
canvases, of which **4** carry `authority`. After the Plumbline P1 migration all 4 carry values inside
the proposed sets, so **25 of 25 keep passing untouched**. ⚠ Before that migration **2 of the 4**
carried `generator` — a *production* value in an *authority* field — which is precisely the state this
LIP exists to make unrepresentable, and precisely what a validated Option B would have blessed.

**Precedent for the shape:** `AFFORDANCE_KINDS` in `reserved.py` — a closed enum on an optional block.

**The firewall touch, named concretely so the §7.7 signature is informed rather than blanket:**

| # | File | Change |
|---|---|---|
| 1 | `canvas_std/src/canvas_std/reserved.py` | two frozensets beside `AFFORDANCE_KINDS`; two `if "<key>" in reserved:` membership checks in the conditional block; both names appended to `RESERVED_KEYS` |
| 2 | `canvas_std/src/canvas_std/data/adna_canvas_v2.schema.json` | two `{"enum": [...]}` properties under `$defs.reserved`; `x-standard-version` → `2.4.0` |
| 3 | conformance suite | new A-8 cases: absent (pass) · valid (pass) · misspelled (fail) · `generator`-as-authority (fail, the migration case) |
| 4 | `CHANGELOG` + `spec_conformance_suite` | the A-8 row |

⛔ **Two keys or neither.** The ruling is explicit that they *"become binding together"*. Validating
`authority` alone would re-create the original defect in the Standard itself: a canvas could then be
*validly* `dual_channel` while silently omitting the only field that says *do not hand-edit me*.

⭐ **What ratifying this buys, stated as the thing that is currently untrue.** Today the enum is
enforced in **exactly two places, both ours** — `canvas_core/conform.py` and
`diagram_generator/model.py`. Every other producer in the fleet, and every hand-authored canvas in
**15+ vaults**, can write `authority: "veiw"` and receive a green `[OK]`. This LIP is the difference
between a doctrine two of our own modules happen to police and one the Standard knows.

*Cost:* a firewall touch, therefore a real LIP through its own §7.7 gate. **Not taken here.**

---

## Recommendation — Option D, and the reason this is a conversion rather than a fresh LIP

~~Take **no change now**, and open Option B as a real LIP **only if Rosetta adopts
`pattern_diagrammatic_context`**.~~ ⛩ **That condition has been met, in a shape that superseded the
option it was protecting** — which is the deferral working exactly as designed rather than failing.

The original reasoning, preserved because it is the argument that was vindicated:

> The reasoning is ordering, not reluctance. `authority` is load-bearing *because the pattern says so*,
> and the pattern is a staged draft in another vault's queue — unruled. Validating an enum for a
> doctrine that may be amended (or declined) would harden the wrong thing first: **if Rosetta renames a
> row, narrows the set, or rules `authority` advisory, a shipped enum becomes a migration.** Doctrine
> settles, then the machine enforces it.

⭐ **All three of those hypotheticals happened.** The set was narrowed (`generator` removed), a row was
effectively renamed onto a new axis, and `authority` *was* ruled advisory-until-this-LIP. Had Option B
shipped in August, the Standard would now carry a validated enum that **blesses the exact conflation
the doctrine has since ruled out**, and unwinding it would be a major bump.

> ⇒ ***The deferral's value is only visible in the counterfactual, which is why deferrals are hard to
> defend at the time and easy to justify afterwards. It was right for the reason it gave.***

### ⛩ Trigger — REWRITTEN 2026-09-11, and deliberately a file rather than a ruling

> **Open Option D as a Standard proposal when:**
> `aDNA.aDNA/what/patterns/pattern_diagrammatic_context.md` **exists on disk** and names its split
> field set. Verified by listing that directory from this tree — **never** by reading a memo that says
> it was authored.

**Why the change of kind.** The 2026-08-24 trigger was a claim about *someone else's decision*,
evaluable only by them. It mis-predicted the decision's shape and fired in a form that inverted it —
and the document announcing the ruling was **already wrong** about whether the artifact existed.

> ⇒ ***A trigger you cannot evaluate from your own tree is a trigger someone else has to remember for
> you.***

**First evaluation, run rather than described** `[D] 2026-09-11`:

```
$ ls ~/aDNA/aDNA.aDNA/what/patterns/ | wc -l
26
$ ls ~/aDNA/aDNA.aDNA/what/patterns/ | grep diagrammatic
pattern_diagrammatic_context.md
```

**✅ The trigger has fired.** This LIP is a Standard proposal as of 2026-09-11.

*(Rosetta's own §3 models the standard adopted here: "this sentence is deliberately not the word
'routed'" — six routing claims verified in the prose that routed them. This trigger is written so it
cannot become a seventh.)*

~~**If Rosetta declines the pattern:** no change is needed at all, and this assessment closes Final on
Option A.~~ — **They did not decline.** They adopted-with-a-split, so the Option-A close is off the
table and this LIP stays open pending §7.7.

## What this assessment does *not* need

Everything else the doctrine asks for is already in the Standard at **2.3.0** — confirmed by
implementation, not by inspection:

- **Dual-channel pairing** — a prose/`.canvas` pair needs no schema support; sync discipline is a
  mission-process rule (Emacs REQ-Q01), ~~enforced at gate review~~.
  > ⛩ **The struck clause was false, and we were the counterexample** (F-PL-6, 2026-09-11). It was
  > *not* enforced at gate review: both of this vault's dual-channel canvases went stale on
  > 2026-09-07 when the P2c re-gate changed the layout engine, and stayed stale through **P2c, P3,
  > P4, P5 and the campaign close — five all-green gate lines.** The visual gate checks a canvas *as
  > it stands*; nothing compared a generated artifact to a regeneration of it. ⇒ ***a generated
  > artifact that nobody regenerates is a claim nobody re-derived.***
  > **This does not change the conclusion** — the remedy is a *gate*, not a schema key, and it
  > shipped the same day as `dual_channel_freshness` (gate #9, which rebuilds every `.diagram.yaml`
  > and compares). But "no schema support needed" was being carried by a clause that was untrue, and
  > a right answer resting on a wrong premise is worth one line to fix.
- **`view` authority semantics** — already expressible; ADR-011's migration reaches
  `adna_native [OK]` with degradation D-1/2/3 intact, on 2.3.0 unmodified.
- **`generator` provenance** — `sync.source_name` / `source_version` / `sync_hash` already carry it.
- **Conformance floor + visual gate** — `canvas-std validate --level adna_native` plus the
  agent-confirmed render (Amendment 1) already exist and are already the campaign's standing order.
- **Context-object identity** — `_reserved.context_object` (id/version/refs) shipped at 2.0.0.

**Emacs.aDNA remains the existence proof:** 13 months of the full pattern on an unmodified Standard.

## Status

**draft — and as of 2026-09-11 the reason it is draft has changed, which is itself the finding.**

It was draft *pending a ruling*. The ruling arrived and **replaced the condition rather than
satisfying it** — inverting this LIP's own trigger (§0). It is now draft *pending an operator
signature*, having converted from an assessment that proposed nothing into a **Standard proposal for
v2.4.0** that proposes a four-file firewall touch.

**No change taken.** `what/code/canvas_std/` is at **git-diff 0**, verified by the `firewall` gate of
the runnable manifest in this session's run and **not asserted** — run from the vault root, because a
persisted `cd` makes that check return empty, i.e. indistinguishable from clean.

### Ratification (§7.7) — required before any firewall touch

| Field | Value |
|-------|-------|
| Decision | **Option D** — `authority` ∈ {`dual_channel`, `view`} and `production` ∈ {`hand_authored`, `generated`}, both **optional**, both validated **only if present**, on `metadata.frontmatter._reserved`; additive; minor bump **v2.4.0**; **two keys or neither** |
| Ratified by | **Stanley Bishop (operator)** — at the Operation Gridline plan gate |
| Date | **2026-09-11** |
| Status | **accepted** |

⛩ **Signed 2026-09-11.** The signature authorizes the four-file touch in Option D's table **and nothing
wider** — the `adr_007` discipline: the firewall lifts for the phase that was authorized (Gridline P1)
and returns to diff-0 on commit. Execution campaign: `how/campaigns/campaign_canvas_gridline/`.

⛩ **One thing the signature cannot bless, because it was discovered after the table was written**
(F-GL-1, 2026-09-11). Item 1 of Option D says *"both names appended to `RESERVED_KEYS`."* That tuple —
`reserved.py:21` — **has no consumer**: it is referenced nowhere in `src/`, `tests/`, or
`what/production/`. The append is therefore correct *and* inert, and the evidence that this is a real
defect rather than a stylistic one is a second absence nobody noticed: **`interaction`**, shipped and
validated at **v2.2.0**, is in neither `RESERVED_KEYS` nor the schema's `$defs.reserved.properties`.

> ⇒ ***a specification with no consumer is indistinguishable from no specification*** — the pin-field
> ruling's own generalisation, found this time inside the firewall.

The append is performed as ratified. Whether `RESERVED_KEYS` should **gain** a consumer, and whether
`interaction` should be back-filled, are changes **outside this table** and are put to the operator at
the Gridline P1 exit gate rather than taken under this signature.

⚠ **What signing does and does not do.** It authorises the four-file touch in Option D's table and a
v2.4.0 cut. It does **not** mandate either key on any canvas: the ruled pattern declines that, and so
does this LIP. A canvas carrying neither key stays conformant — which is the correct answer for a
hand-authored **primary** artifact, whose meaning nothing else owns
([P1 ruling](../../../how/campaigns/campaign_canvas_plumbline/artifacts/p1_under_coverage_ruling.md)).
