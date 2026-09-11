---
type: lip
lip_number: "LIP-0010"
title: "Diagrammatic context — does the doctrine need a Standard change? (assessment)"
author: "Stanley Bishop (Mondrian-drafted; Canvas.aDNA standard-bearer)"
status: draft
created: 2026-08-24
updated: 2026-08-24
requires: []
replaces: []
last_edited_by: agent_mondrian
resolution: "recommendation: Option B, DEFERRED — gated on Rosetta's adoption ruling on pattern_diagrammatic_context. No change taken now."
related: ["adr_011_legacy_canvas_interop_reconciliation", "draft_pattern_diagrammatic_context"]
tags: [lip, assessment, canvas, canvas_standard, diagrammatic_context, authority, blueprint, p1]
---

# LIP-0010: Diagrammatic context — Standard-change assessment

> An **assessment**, in the LIP-0009 mould: it asks whether a doctrine needs a schema change, and its
> "implementation" may legitimately be the status quo. Produced at Operation Blueprint P1
> (`mission_b1_doctrine`, 2026-08-24). **No change is taken here** — `what/code/canvas_std/` is at
> diff-0 and stays there unless a ratified LIP says otherwise (campaign standing order).

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

## Recommendation — Option B, deferred

Take **no change now**, and open Option B as a real LIP **only if Rosetta adopts
`pattern_diagrammatic_context`**.

The reasoning is ordering, not reluctance. `authority` is load-bearing *because the pattern says so*,
and the pattern is a staged draft in another vault's queue — unruled. Validating an enum for a
doctrine that may be amended (or declined) would harden the wrong thing first: if Rosetta renames a
row, narrows the set, or rules `authority` advisory, a shipped enum becomes a migration. Doctrine
settles, then the machine enforces it.

This keeps the charter's default intact (**no schema change at P1**) without pretending the gap is
absent — the charter's default is *preserved by evidence*, not merely by assertion.

**Trigger to open Option B as a proposal:** Rosetta ratifies `pattern_diagrammatic_context` with
`authority` still normative and the three-row set stable. At that point LIP-0010 converts from
assessment to Standard proposal, cuts v2.4.0, and the enum lands additively.

**If Rosetta declines the pattern:** no change is needed at all, and this assessment closes Final on
Option A.

## What this assessment does *not* need

Everything else the doctrine asks for is already in the Standard at **2.3.0** — confirmed by
implementation, not by inspection:

- **Dual-channel pairing** — a prose/`.canvas` pair needs no schema support; sync discipline is a
  mission-process rule (Emacs REQ-Q01), enforced at gate review.
- **`view` authority semantics** — already expressible; ADR-011's migration reaches
  `adna_native [OK]` with degradation D-1/2/3 intact, on 2.3.0 unmodified.
- **`generator` provenance** — `sync.source_name` / `source_version` / `sync_hash` already carry it.
- **Conformance floor + visual gate** — `canvas-std validate --level adna_native` plus the
  agent-confirmed render (Amendment 1) already exist and are already the campaign's standing order.
- **Context-object identity** — `_reserved.context_object` (id/version/refs) shipped at 2.0.0.

**Emacs.aDNA remains the existence proof:** 13 months of the full pattern on an unmodified Standard.

## Status

**draft** — an assessment pending the ordering trigger above. Carries no §7.7 ratification because it
proposes no change; if it converts to a Standard proposal, that proposal gates on its own signature.
