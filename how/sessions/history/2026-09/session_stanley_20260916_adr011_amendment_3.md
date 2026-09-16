---
type: session
session_id: session_stanley_20260916_adr011_amendment_3
created: 2026-09-16
updated: 2026-09-16
status: completed
tier: 2
persona: mondrian
operator: stanley
campaign: none
phase: "ADR-011 Amendment 3 — close the four inconsistencies, make it signable"
executor_tier: opus
last_edited_by: agent_mondrian
tags: [session, canvas, adr_011, amendment_3, partition, signability, consolidating_statement, re_verification, push]
---

# Session — the amendments left a trap, and the "verified" claim was backed by the wrong transcript

## Intent

The operator asked for **commits and advice on the ADR**. There was **nothing to commit** — the tree
was clean and both prior sittings were already committed. The advice is where the work was: examining
ADR-011 for advice found that **two amendments left four live inconsistencies**, one of which
Amendment 2 *created and did not close*.

Rulings at the plan gate: **Amendment 3 + a consolidating statement** (supersession rejected —
Rosetta's fired v8.11 ledger cites *"ADR-011"* by name) · **push all three commits once it lands**.

## Cold-start ritual

| Check | Result |
|---|---|
| `git status --porcelain -uall` | **clean** — 0 entries, nothing to commit |
| `how/sessions/active/` | empty — **no peer lease** |
| Unpushed | **2** (`92866fe` gate package · `5a64e5b` Amendment 2) |
| Firewall | `canvas_std` **0 entries** |
| HEAD at open | `5a64e5b` |

## The four inconsistencies

| # | What | Why it matters |
|---|---|---|
| **a** | the `source_yaml` row still says *"a real value must be supplied"* | ⛔ **An active trap Amendment 2 created.** Those 3 are primary artifacts with no source; an invented `source_name` **resolves nothing but changes the partition test's answer** — self-concealing, and the exact *"passing a value to make a number go green"* move declined one row above. |
| **b** | *"4 / 4 migrated files reach `adna_native [OK]`"* | Verified the **superseded** recipe. Decision 3 claims *"verified"*; the claim was backed by the wrong transcript. |
| **c** | *"declared for 6 months without ever being enforced"* | **The exact misread Amendment 2 names**, still standing two paragraphs below its own correction. |
| **d** | the title | asserts the whole corpus **is** the `view` row; only **63 of 258** are. |

⭐ **And the real problem is signability.** The operative decision was spread across an August body
plus two September amendment blocks — ratifying it meant holding *what's struck* in your head.

## Work log

### Re-derived fresh, not carried

```
258 canvases across 63 vaults   (~/aDNA/*/what/lattices/examples/*.canvas, Archive excluded)
  194  primary
   63  derived (source resolves)
    1  no _reserved
```

Third independent run; reproduces exactly.

### ⭐ The partitioned recipe VERIFIED, restoring Decision 3 rather than weakening it

Run on **scratch copies** (`.adna/` untouched — Standing Rule 1; Canvas's tracked examples untouched;
all three trees confirmed at 0 entries afterwards). `sync_hash` **recomputed** via
`roundtrip.compute_sync_hash`, never transliterated — A-6 rejects the `sha256:`-prefixed form.

| Population | Migrated `_reserved` | Axis keys | Result |
|---|---|---|---|
| **DERIVED** `hello_world.canvas` | `adna_version 2.4.0 · conformance_level adna_native · authority view · production generated · sync{sync_hash 28cf14bbd135f628, source_name hello_world.lattice.yaml}` | both | **`adna_native [OK]`**, degradation `D-1/2/3` all `True` |
| **PRIMARY** `template_architecture.canvas` | `adna_version 2.4.0 · conformance_level adna_native · sync{sync_hash 85b1fe9224948842}` | **neither** | **`adna_native [OK]`**, degradation `D-1/2/3` all `True` |

⇒ **The primary form carries no `source_name`, no `authority`, no `production` — and passes.** That is
the claim Amendment 2 asserted and this run proves.

### The four fixes

- **(a) The trap closed.** `source_yaml` row split by population, with the reason named: `source_name`
  is an **input to the partition test**, so an invented value *reclassifies* the canvas instead of
  documenting it. The migration table gained a `sync.source_name` column so all three fields are
  partitioned together.
- **(b) Evidence re-run, not withdrawn** — see the table above. Decision 3's *"verified"* is true again.
- **(c)** The *"declared for 6 months without ever being enforced"* sentence struck: ⇒ ***an
  unpopulated field is data, not debt.***
- **(d)** Title corrected, preserving the original phrase so existing citations still read
  continuously. ⚠ Rosetta's ledger cites by **id**, not title — checked before changing it.

Plus two leftovers found while scanning: the *"executed on scratch copies of **all four**"* lead-in
(one recipe, four files — the error itself) and Amendment 1's note about the `4/4` claim, which was
superseded by A3 and said so. ⭐ **A1 wrote *"state the population on the face of the number"* about a
number whose population it had not itself stated** — the rule was right, applied one level short.

### The consolidating statement

`## What this ADR says today`, placed **after §Status and before the amendment blocks** so a ratifier
meets the decision before the archaeology. ⛔ **Explicitly a summary, not a replacement** — *if it and
a Decision disagree, the Decision wins and the summary is the defect.* It also states the four things
the ADR does **not** claim, including one verified this session: **nothing enforces the partition in
code** — a `view` canvas citing a non-existent source validates `OK`.

### ⭐ The visual check I owed, done — and it caught another defect

Last round the Chrome extension was down and I said so rather than implying otherwise. This round it
reconnected, and opening the gate found the **`adr_title` still showing the pre-Amendment-3 title** —
the ADR frontmatter had been corrected, the gate's copy had not. No content check would have caught
it: both strings are valid, present, and render cleanly.

**Fixed at the root, not patched**: `adr_title` is now **derived from the ADR's frontmatter** by the
build step rather than restated in the gate data. ⇒ ***a gate that restates a fact from the document
it gates is a second copy that can drift*** — the vault's own wrapper doctrine (*wrappers point, they
never restate*), found in a gate.

## SITREP

**Completed** — ADR-011 **Amendment 3**: four inconsistencies closed, evidence re-verified under the
partitioned recipe, consolidating statement added, gate re-rendered and **visually confirmed**.

**In progress** — none.

**Next up** — operator rules at the doors. `adr_010` · `adr_012` · queue ① ③ ⑤ are free;
⛔ **`adr_011` and queue ② still move together** — #20's payload is this erratum.

**Blockers** — none.

**Files touched** — `what/decisions/adr_011_legacy_canvas_interop_reconciliation.md` ·
`how/gates/adr_011_ratification.{data.json,html,pending}` · `STATE.md` · this file.

## Next Session Prompt

`Canvas.aDNA` (**Mondrian**), no active campaign. Four ISS gates await verdicts in `how/gates/`.
**`adr_011_ratification` was re-rendered 2026-09-16 after Amendment 3 and visually confirmed** — read
**§What this ADR says today** in the ADR first; it is the whole decision in one place, and it is a
summary, not a replacement (the Decisions remain the authority). The corpus is **two populations**:
**194 primary → omit `source_name`, `authority` and `production`**; **63 derived → all three**. ⛔
**`adr_011` and queue section ② (memo #20) move together** — #20's payload is *"partition before
migrating"*. `adr_010`, `adr_012`, queue ① ③ ⑤ are independent. ⚠ **Nothing enforces the partition in
code** (a `view` canvas citing a non-existent source validates `OK` — verified), so **re-run the
partition test before any fleet migration**: `source_yaml` non-empty **and** it resolves ⇒ derived,
else primary. Standing caution: `canvas_core` measures 1039/4 with Obsidian closed and 1040/3 with it
open — `Gate.env_skips` working, not a regression.
