---
type: aar
aar_id: datum_campaign_aar
title: "AAR — Operation Datum: the registry we could see was fixed in a day; the one that looked fixed took the whole campaign"
campaign: campaign_canvas_datum
created: 2026-09-15
updated: 2026-09-15
status: complete
last_edited_by: agent_mondrian
tags: [aar, datum, registry, derivability, no_consumer, reserved_keys, schema_twin, coverage, f_dt_7, firewall, gate_manifest]
---

# AAR — Operation Datum

**Ran:** 2026-09-13 → 2026-09-15, **two sessions**, P0–P5 (P4 a reasoned decline, P4b a dated scope
amendment taken at the P4 gate). Chartered on the single open item Gridline's AAR left —
`idea_reserved_keys_has_no_consumer`, the durable fix Gridline had deliberately declined to build.

**Shipped:** two firewall touches (#5, #6 — the fifth and sixth deliberate `canvas_std` touches since
Keystone) · gate **#10** `registry_census` · **26 vocabularies** each declaring a falsifiable state
checked against a derivation · the package's **first document-level JSON Schema test**, shipping with
its own coverage published · the derivability doctrine graduated to `what/context/` · one backlog idea
**closed**, one **declined with its reason written onto the line**, one **filed upstream**.
`canvas_std` **146 → 170/10**. Gates **9 → 10**, all green.

**Eleven findings, F-DT-1 … F-DT-11.** Every phase produced at least one, and — the pattern worth
naming — **every instrument this campaign built produced a finding about itself before it produced
one about its subject.**

---

## Worked

- **Running the baseline instead of quoting it, even when it is quiet.** P0's gate run reproduced
  STATE's published line exactly. Recorded as a *result*, because Gridline's identical run had
  produced F-GL-4 in its first minute. ⇒ *you cannot know which kind of baseline you have until you
  run it* — and a quiet one is evidence, not a formality.
- **Perturbation over reading, without exception.** All sixteen derivations (D1–D16) produced their
  failure rather than inspecting the code that should produce it. **Three of them refuted something I
  had just written**, including the plan's central prediction about D13. Re-reading would have caught
  none of the eleven findings.
- **Refusing to rule the questions that were the operator's.** Three went up — the P2 firewall shape,
  F-DT-3's link-or-merge, P4's build-or-decline — and **all three rulings shaped the artifact**. The
  both-legs rulings in particular are what put the protection where the exposure was: downstream.
- **Building the vault leg and the package leg, twice.** The gate protects Canvas; the package test
  travels with a fork or a `pip install`. F-DT-7 vindicated this precisely — its entire blast radius
  is downstream, because nothing *inside* this vault reads the JSON Schema's value enums.
- **Declining well.** P4 was declined on the backlog idea's own argument, and the obligation was still
  discharged: the definition of done is *which state it is in, **written on the line***, so the state
  went into `who/coordination/AGENTS.md` at ~20 lines instead of a tool. ⇒ *not every registry
  deserves a checker; every registry deserves a stated disposition.*
- **Naming duplications instead of merging them.** The AST walk exists twice (package cannot import
  from `how/gates/`), and both copies carry the reason. The campaign found that rule in the morning
  (F-DT-3) and had to apply it to itself by the afternoon.

## Didn't work

- **The charter aimed at the wrong half of its own population, and got there on a true statement.**
  P3 was scoped to the **14 unpaired** constants. The exposure was in the **12 paired** ones, which P1
  had reported as *"all twelve agree exactly. No drift."* — true, and the entire protection. ⇒ the
  charter was not wrong about the facts; it was wrong about **which fact was load-bearing**.
- **I predicted, in a written plan, the opposite of what measurement showed — twice in one day.** The
  P3 close called the schema test *"larger than P3's scope"* (it is ~15 lines, and `jsonschema` was
  already installed). The P4b plan predicted the new suite *would not* have caught the F-DT-7
  perturbation; D13a shows it **does**, by an accident of which side the fixtures vary. Both corrected
  **where they were written**, not silently.
- **Two governance artifacts rotted *during* the campaign about rot.** The session file sat
  `status: active`, `phase: "Act 0 → P0"`, work log unappended, across four commits and two operator
  rulings (**F-DT-8**); `STATE.md` said *"P0 closed, P1 next"* in two places for two days.
- **A defect was fixed, fully derived, committed — and written into no campaign artifact.** F-DT-6
  lived only in a commit message; §Findings ended at F-DT-5 while a sixth finding sat in `git log`.
  Retro-numbered at P3.
- **I miscounted unpushed commits again** — wrote "8" where it was 9, five days after recording the
  identical slip ("reported 20 where it was 22"). Caught on the post-commit re-verify. ⇒ ***the habit
  does not transfer by having written the finding down***, which is this campaign's own thesis
  about registries, aimed at me.

## The finding

> ⭐ ***A registry that LOOKS watched is better hidden than one that visibly is not.***

`RESERVED_KEYS` was *visibly* read by nothing — and that visibility is exactly what got it fixed, in a
day, at P2. The JSON Schema's eleven value enums had a census, a twelve-pair correspondence table, and
a published phase result all stating they agreed exactly. **Gutting one of them left all ten gates
green**, while `jsonschema` correctly rejected an ordinary canvas.

The mechanism is general and it is the campaign's real contribution: the census paired **by content**
— the right choice, since a name map would itself be an unconsumed registry — but content-pairing
**dissolves a pair** when the two sides diverge, rather than reporting drift. The constant reclassifies
into a normal, accepted state. **The instrument fails into reassurance**, and prints a confident false
explanation while doing it.

Three corollaries, each measured:

1. **The same trap waits one layer out, in tests.** A fixture-corpus conformance suite *looks* like it
   guards eleven enums; it exercises **12 of 40** values, two enums not at all, and which drifts are
   caught turns on which values the fixtures happen to use. ⇒ ***a test that looks like coverage is
   worse than no test, unless somebody measures what it covers.***
2. **The blind spot compounds.** A coverage ratchet is blind to the deletion of exactly the
   vocabularies it was already failing to exercise (D13c: both zero-coverage enums deleted, 14 passed).
3. **The remedy is a per-object falsifiable claim, never a second list** — a declared state checked
   against a derivation, which supplies the memory content-pairing structurally cannot have.

## Change

- **`canvas_std` carries its own disposition.** 26 vocabularies each declare `SCHEMA-TWIN` or
  `VALIDATOR-ONLY`, the 14 unpaired ones with the reason there is no twin — enforced in both legs.
- **Gate #10** `registry_census`; gate #9's sibling in checking *a thing* rather than *a suite*.
- **`Gate.env_skips`** (F-DT-5) — a pinned passed/skipped split is a claim about the runner, not the
  code. The total must still match exactly, so no other gate got looser.
- **Fault classes derived once and consumed** (F-DT-6, twice) — the reporter cannot disagree with the
  instrument, because there is nothing for it to disagree with.
- **The schema is tested against documents at all**, and publishes how little that covers.
- **Doctrine graduated** → `what/context/context_registry_derivability.md`, 8 principles. ⛔ Carrying
  no list of registries, deliberately.
- **`who/coordination/AGENTS.md` rewritten** — it was inherited `agent_init` template text instructing
  *deletion* of memos, contrary to SO-6, in the directory holding the delivery record.

## Follow-up

| Item | State | Unblocks when |
|---|---|---|
| **The certification corpus covers 12 of 40 enum values** | ⛔ **open — the campaign's largest residue** | widening it changes a corpus behind a 12/12 gate with downstream meaning. Named, costed, not done. |
| **F-DT-8 — session-file staleness** | filed, not built | deliberately outside a charter scoped to `canvas_std` vocabularies. A freshness check is real and belongs to whoever owns session protocol. |
| **Upstream proposal** | filed locally, **memo not yet sent** | staging a memo to Rosetta — next free number **#20**, and ⛔ `ack_required: true` this time, because our `false` default is known to be invisible to their reply-owed sweep. |
| `idea_memo_number_registry` | **declined** 2026-09-15 | — (state written onto the line instead) |
| `idea_reserved_keys_has_no_consumer` | **closed** 2026-09-15 | — |

---

## The thing I would tell the next campaign

**Ask what your instrument does when its subject is badly wrong, not when it is slightly wrong.**
Every instrument here behaved correctly under small perturbations and reassuringly under large ones —
content-pairing dissolves rather than alarms; a coverage ratchet ignores what it never covered; a
firewall notices a byte changed but not that a Standard's vocabulary was destroyed. Small drift is the
case people design for; **large drift is where instruments fail silently**, and it is the cheaper case
to test because you can simply break the thing and look.
