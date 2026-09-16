---
type: session
session_id: session_stanley_20260916_adr011_amendment_2
created: 2026-09-16
updated: 2026-09-16
status: completed
tier: 2
persona: mondrian
operator: stanley
campaign: none
phase: "ADR-011 Amendment 2 — partitioning the corpus"
executor_tier: opus
last_edited_by: agent_mondrian
tags: [session, canvas, adr_011, amendment_2, partition, authority, production, a8, plumbline_p1, self_correction]
---

# Session — red-teaming my own recommendations found the defect in my own amendment

## Intent

The operator asked for **advice on the recommendations**, not a restatement of them. Adversarially
re-checking the ADR-011 amendment I authored yesterday found that **its central new row is wrong for
the majority of the corpus**, and that the underlying error predates the amendment.

Two rulings taken at the plan gate: **author Amendment 2 now and re-render the gate before any
signing** · the sourceless canvases **omit both keys**.

## Cold-start ritual

| Check | Result |
|---|---|
| `git status --porcelain -uall` | **clean** — 0 entries |
| `how/sessions/active/` | empty — **no peer lease** |
| Unpushed | **1** (yesterday's gate-package commit) |
| Firewall | `canvas_std` **0 entries** |
| HEAD at open | `92866fe` |

## The finding

⛩ **The corpus is two populations, and neither ADR-011 nor Amendment 1 partitioned it.**

**Re-derived independently at session open rather than carried from the plan** — the whole point of
the finding is that a stated number nobody re-derived is how it happened:

```
glob : ~/aDNA/*/what/lattices/examples/*.canvas   (Archive.aDNA excluded, live vaults, this node)
total: 258 canvases across 63 vaults

  194  sourceless                  -> PRIMARY artifact  -> omit both keys
   63  sourced + source RESOLVES   -> genuinely derived -> authority: view + production: generated
    1  no _reserved block
```

The shape is uniform per vault: **one `hello_world.canvas`** (cites `hello_world.lattice.yaml`, and
that file exists) **plus three `template_*` canvases** citing nothing. ⚠ **The negative was verified,
not assumed**: `find` across the entire workspace returns **no** `template_agent_graph.lattice.yaml`,
`template_architecture.lattice.yaml` or `template_pipeline.lattice.yaml`.

⇒ **Roughly 3 : 1 against the recipe as written.** Amendment 1's blanket `production: "generated"`
row would have been applied to 194 files that are not generated from anything — and on top of an
`authority: "view"` that is not true of them either.

### Why `authority: view` is wrong on the 194, not merely incomplete

The **Plumbline P1 ruling** already settled this population: *"A standalone hand-authored canvas that
**is** the primary artifact is not diagrammatic context at all"* — the axis does not apply and
**omission is the correct answer**. `view` asserts *another channel owns the meaning*; for these,
there is no other channel.

### The error's provenance, stated fairly

| Who | What they did |
|---|---|
| the legacy tooling (2026-02) | stamped `authority: "view"` on **everything** it emitted, sourced or not |
| **ADR-011** (2026-08-24) | inherited that as ground truth. ⚠ It **saw the symptom and misread it** — §Verified migration says *"sync fields were never populated… declared for 6 months without ever being enforced."* ⇒ it read **"unpopulated"** where the truth was **"these are not views."** |
| Rosetta (2026-09-11) | verified **placement and byte-identity**, which is what we asked them to verify. Not semantics. Not their miss. |
| **me** (Amendment 1, 2026-09-15) | added `production: generated` on top, *compounding* it |

⭐ **The calibration lesson, recorded because it is the useful part.** The `production` row was the
single item I rated most confident in the entire package — described in the gate as *"right by the
pattern's own definition."* It is the one that was wrong. **Confidence was doing the work a partition
should have done.**

## Work log

### What was written

- **`adr_011` Amendment 2** — the partition, the measurement with its glob, the Plumbline P1 citation,
  and an explicit statement that **Amendment 1's blanket `production` row was wrong for 194 of 258**.
- **Migration table split into two population rows** — derived → `view` + `generated`; primary →
  **omit both**. ⚠ `production: "hand_authored"` was considered and **declined**: legal under A-8's
  asymmetry, but not what was ruled, and inventing a declaration to make a field non-empty is the habit
  `conform.py` names as *"passing a value to make a number go green."*
- **Decision 1 gains the corollary it never stated** — *a canvas whose declared source does not resolve
  is not a derived visualization, and must not be stamped as one.* ⇒ ***the presence of a field is not
  evidence of the fact it asserts.***
- **An executable partition test**, so the recipe can be run rather than interpreted.
- **`STATE.md` corrected where it published the `production` row as the fix**, plus a **recommended
  order** — the gates are not independent.

### ⚠ Verification: what I could and could not check this round

| | |
|---|---|
| ✅ Claim re-verified at the object | *"both keys omitted is fully conformant"* — asserted in the ADR, then **run**: `validate(..., ADNA_NATIVE)` → `OK` |
| ✅ Partition re-derived at session open | 258 / 194 / 63 / 1 — reproduced exactly, **not carried from the plan** |
| ✅ The negative verified | `find` across the whole workspace returns **no** `template_*.lattice.yaml` |
| ✅ Gate structure | no unrendered placeholders · HTML parses with **no unclosed tags and no stray closers** · sentinel written · **zero CSS classes** present in the visually-confirmed `adr_010` gate are missing from `adr_011` ⇒ structurally equivalent to a render I *did* confirm by eye |
| ⛔ **NOT done: the visual check** | The Chrome extension **disconnected** mid-session (`Browser extension is not connected`). I could not re-open the re-rendered gate. **Said plainly rather than implied** — the rule this vault wrote is *verify by opening the file*, and this round I did not. The static evidence above is a substitute, and it proves structural equivalence, **not that the page looks right.** |

## SITREP

**Completed** — ADR-011 **Amendment 2** authored; gate re-rendered; `STATE.md` corrected where it had
published the superseded fix; recommended order added.

**In progress** — none.

**Next up** — operator rules at the doors. **`adr_010` · `adr_012` · queue ① ③ ⑤ are free.**
⛔ **`adr_011` and queue ② move together.** Re-open `adr_011_ratification.html` yourself before signing
— I could not.

**Blockers** — none. ⚠ One standing caveat: this ADR has now been **wrong twice, in two different
ways**. A third population may exist that neither pass found; the partition test is derivable, so
**re-run it before any fleet migration** rather than trusting these figures.

**Files touched** — `what/decisions/adr_011_legacy_canvas_interop_reconciliation.md` ·
`how/gates/adr_011_ratification.{data.json,html,pending}` · `STATE.md` · this file.

## Next Session Prompt

`Canvas.aDNA` (**Mondrian**), no active campaign. Four ISS gates await verdicts in `how/gates/`;
**`adr_011_ratification` was re-rendered 2026-09-16 with Amendment 2** and is the one to read first —
the corpus is **two populations** (258 canvases / 63 vaults: **194 primary → omit both axis keys**,
**63 derived → `view` + `generated`**), and Amendment 1's blanket `production` row was wrong for the
194. ⛔ **`adr_011` and queue section ② (memo #20) move together** — #20's payload is ADR-011's erratum,
now *"partition before migrating"* rather than *"add a production row"*. `adr_010`, `adr_012` and queue
① ③ ⑤ are independent and free to rule. ⚠ **Re-run the partition test before any fleet migration**
(`source_yaml` non-empty **and** resolves ⇒ derived; else primary) — this ADR has been wrong twice and
the figures should be re-derived, not trusted. ⚠ **The Chrome extension was disconnected at the end of
the last session**, so the re-rendered gate was verified structurally but **not visually** — open it
before signing.
