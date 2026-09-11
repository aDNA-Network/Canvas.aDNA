---
campaign_id: campaign_canvas_plumbline
type: campaign
title: "Operation Plumbline — the authority axis splits in two, and Canvas conforms to the doctrine it asked for"
owner: stanley
status: completed
estimated_sessions: "1-3"
phase_count: 5
mission_count: "created at phase-open"
priority: high
executor_tier_default: opus
predecessor: campaign_canvas_blueprint
created: 2026-09-11
updated: 2026-09-11
completed: 2026-09-11
actual_sessions: 1
last_edited_by: agent_mondrian
status_history: "active (2026-09-11 — chartered at the plan gate, reversing the P5 'no successor chartered' ruling on new evidence: Rosetta's 2026-09-11 reply cleared b1.5, and the clearing made Canvas its own blocker) · P0 record corrected + chartered · P1 under-coverage RULED from the pattern text, producers conformed, F-PL-6 found both dual-channel pairs stale for four days -> gate #9 · P2 LIP-0010 converted to a v2.4.0 Standard proposal (firewall diff-0) · P3 memo #17 delivered, #18 staged then delivered on the close re-probe, shim trap + foreign-gate guard closed, iii pin de-duplicated · P4 CLOSED 2026-09-11 -> ✅ COMPLETED"
tags: [campaign, canvas, plumbline, authority_axis, production_axis, b1_5, lip_0010, pattern_diagrammatic_context, conform, diagram_generator, rosetta, berthier, sciencestanley]
---

# Campaign: Operation Plumbline

> Named for the second axis. A plumb line answers *vertical*; a level answers *horizontal*; and the
> whole of Mondrian's grid is the refusal to let one of them do the other's work. This campaign exists
> because a single field was answering two questions, and one of them looked answered when it was not.

## Why this campaign exists

Operation Blueprint closed 2026-09-09 with eleven carried-tail items and **no successor chartered**
(operator ruling at the P5 gate). Tail item #1 — `b1.5`, the `authority` axis — had sat with Rosetta
since 2026-08-22 with three delivered, unanswered artifacts. Its unblock condition read: **"Rosetta
rules."**

They ruled, in a reply that answered four Canvas memos at once
([intake `eb12e16`](../../../who/coordination/inbox/coord_2026_09_11_rosetta_to_mondrian_all_three_ruled_and_your_archive_figure_reproduces_exactly.md)).
**Reading it produces a wrong plan twice over**, and both inversions were caught by re-deriving rather
than re-reading — which is Blueprint's defining finding, arriving as the first act after its close.

### Inversion 1 — "ruled" is not "unblocked"

LIP-0010's own trigger requires the pattern be ratified *"with `authority` still normative **and** the
three-row set stable."* The ruling breaks **both** conjuncts: §3 amendment 1 **splits** the axis
(*"we are not adopting a three-value enum that answers one-and-a-half of them"*), and amendment 2 rules
`authority` **doctrine-enforced, not machine-enforced** — *"until your LIP-0010 rules."*

⭐ **The two conditions were written pointing at each other.** Our trigger waited on their ruling;
their ruling defers the enforcement clause to ours. Neither desk was stalling; the cycle is structural,
and it is broken only by an artifact existing.

### Inversion 2 — the memo was stale in its most load-bearing claim, and it carried the proof

§3 states `pattern_diagrammatic_context.md` is **NOT YET AUTHORED** (24 patterns, not among them) and
pointedly declines the word *"routed"*: *"you will know it exists when it exists."*

Evaluated from our own tree: `aDNA.aDNA/what/patterns/` holds **26** patterns and **the file is among
them**, authored at `67ad713` — **the commit immediately after `860c59e`, the head the memo pins** as
*"superseded when: our next commit."*

> ⇒ ***A memo is a measurement with a timestamp. This one told us exactly how to know it had expired,
> and we would have missed it by believing the sentence instead of evaluating the pin.***

### What actually cleared, and what replaced it

| Axis | The question it answers | Values |
|---|---|---|
| **`authority`** | *Who owns the meaning?* | `dual_channel` · `view` |
| **`production`** | *How is the picture made?* | `hand_authored` · `generated` |

That is **E2's larger fix** — the two-field shape Canvas **named and explicitly declined to propose**
as "a schema change." Rosetta adopted it and answered the objection directly: it costs no schema change
*because* nothing validates either key yet, and *"at that point both become binding together."*

### ⇒ The blocker cleared, and Canvas became its own blocker

Measured 2026-09-11, not inferred:

- **The ruled `production` axis is unknown to every tool Canvas ships** — zero hits across
  `conform.py`, `diagram_generator/`, and `canvas_std/src/`.
- **`conform.py:50`** pins `VALID_AUTHORITIES = {dual_channel, generator, view}` — the superseded set —
  and `uplift_to_adna_native` takes `authority` as a **required** keyword-only argument, while the
  ruled pattern makes it optional.
- **`diagram_generator/model.py:40`** pins the same superseded frozenset, with 6 tests on it.
- **2 of our 4 canonical-path carriers declare `generator`**, which is no longer an `authority` value.

⭐ **So the thirteen-month-old claim that `authority` is "doctrine-enforced, not machine-enforced" was
over-broad all along.** It is unvalidated by `canvas_std` and validated by **two producers, both ours** —
one under a test named `test_misspelled_authority_is_rejected_here_because_the_validator_cannot`.
The measurement was `canvas_std`-scoped; `STATE.md`'s compression of it dropped the qualifier.

## Goal

1. **Conform Canvas's own producers and canvases to the ruled two-axis shape** — so the vault that
   asked for the split can emit it.
2. **Convert LIP-0010** from a deferred assessment into a ratifiable v2.4.0 Standard proposal, now that
   the pattern fixes the spellings. **Authored, not landed** — the firewall stays at diff-0.
3. **Discharge two explicit promises** — to Berthier (*"when it is ruled, tier 2 is a one-line call and
   I will come back"*) and to SS (*"flagged when it clears, not left to ask"*).
4. **Correct the record** wherever the ruling, or our own re-derivation, made a published figure false.

## ✅ RULED at P1 — the question the charter refused to assume

> **Answer: the population was never in scope, so there is nothing to under-cover.** `pattern_diagrammatic_context` governs *"two channels side by side"*, and its anti-pattern is scoped to *"a `.canvas` **beside a document**"*. A hand-authored **primary** artifact owns its own meaning, so the `authority` question does not arise — and the pattern explicitly declines to call an undeclared canvas nonconformant. ⇒ ***an axis cannot under-cover a population it does not cover***; **omission is the correct answer**. Full basis with quotations: [`p1_under_coverage_ruling.md`](artifacts/p1_under_coverage_ruling.md). The question as posed at the charter gate is preserved below.

### The question as posed

⚠ **The split fixes E2's finding. Nothing in the ruling says it fixes P2b's, and they are different
defects.**

- **E2 — double coverage.** Two canvases are `dual_channel` *and* machine-generated at once. The ruling
  cites this by name; the `production` axis fixes it exactly.
- **P2b — under coverage**
  ([`p2b_authority_axis_evidence.md`](../campaign_canvas_blueprint/artifacts/p2b_authority_axis_evidence.md),
  held and never dispatched): 8 real canvases where **all three values are wrong** — hand-authored
  primary artifacts with no `.lattice.yaml`, no generator, and no prose twin. *"Not two values that
  both apply, but three values where none does."*

The ruled `authority` axis has **two** values and **both presuppose something else owns the meaning**
(the prose, or a `.lattice.yaml`). A hand-authored primary artifact owns its own.

⛔ **P1 rules this from the pattern's text — its anti-patterns and conformance-floor sections — and
records the quoted basis. It is not assumed.** If the axis still under-covers, that is an **erratum owed
back to Rosetta**, not a gap papered over with a placeholder. Shipping a value to make a number go green
is F-P2b-5, and declining to do it is the thing Berthier endorsed by name.

## Phases

Each gate is a **human gate** (Standing Order 1). P0–P3 are intended for one sitting.

| Phase | Scope | Gate deliverable | Status |
|---|---|---|---|
| **P0** | **Intake + the corrected record.** Standalone read-receipt commit; re-derive the censuses; correct the five live stale sites; charter. | The record is true, and the campaign exists. | ✅ **complete** |
| **P1** | **Rule the under-coverage question, then conform the producers.** `conform.py` + `diagram_generator` learn both axes; migrate our 4 canonical carriers. | Canvas can emit the shape it asked for; producers green. | ✅ **complete** |
| **P2** | **LIP-0010 converts** to a v2.4.0 Standard proposal — Option B superseded-in-cells, Option D specified. **Firewall untouched.** | A ratifiable proposal; `canvas_std` diff 0. | ✅ **complete** |
| **P3** | **Memos #17 (SS) + #18 (Berthier) delivered**; `gate_manifest` shim hardening; `iii/` pin de-dup. | Both promises discharged; two latent traps closed. | ✅ **complete** |
| **P4** | **Close.** `adr_011` upstream note; gate run pasted; AAR; STATE; push. | Campaign completed. | ✅ **complete** |

## Operator rulings taken at the charter gate (2026-09-11)

1. **Charter a successor campaign** — reversing P5's "no successor" on new evidence.
2. **LIP-0010: author the proposal, do not touch the firewall.** `canvas_std` stays diff-0 pending §7.7.
3. **Memo GO for #17 and #18** — delivered, not staged.

## Standing orders

- ⛔ **`what/code/canvas_std/` is not touched this campaign.** Operator-ruled. Verified by gate, not asserted.
- ⛔ **`pattern_diagrammatic_context.md` is not authored or amended here** — not our vault, not our ontology.
- ⛔ **No fleet pin sweep** — explicitly unauthorised by the ruling.
- ⛔ **Historical records carrying superseded figures are not edited** (`adr_012`). Corrections strike
  in situ and state what was believed when.
- **Every published figure carries its population on its face** — tip or history · class or literal ·
  **tracked or working-tree**. Blueprint's ruling discipline, and this campaign has already needed it twice.

## Findings

| id | Finding |
|---|---|
| **F-PL-1** | *"Ruled" and *"unblocked"* are different facts, and STATE's unblock condition conflated them. The trigger was **inverted**, not fired — and had the pattern not been authored in the interim, the honest reading of the ruling was that **zero of four** downstream items had cleared. |
| **F-PL-2** | **A memo is a measurement with a timestamp.** §3's "NOT YET AUTHORED" was true at 00:55Z and false when read. The memo's own `rosetta_head` pin — *"superseded when: our next commit"* — is what proved it, and believing the sentence instead of evaluating the pin would have chartered an entire campaign around a blocker that no longer existed. |
| **F-PL-3** | **A stale figure can re-derive as a true number.** `lip_0010:47` published `0 of 21`; today it is `4 of 25` — and the **complement is still exactly 21**, so a reviewer grepping "21" finds 21 and concludes it reproduced. Its neighbour at `:68` is the **mirror**: numerator unchanged at 21, denominator moved. ⇒ ***two stale figures can disagree with reality in opposite directions and still agree with each other.*** |
| **F-PL-4** | **A claim restated without its population loses the qualifier that made it true.** *"`authority` is doctrine-enforced, not machine-enforced"* was a `canvas_std`-scoped measurement compressed into a vault-wide claim. Two of our own producers enforce it. The qualifier survived in `skill_canvas_context_diagram.md:67` and died in `STATE.md:146` — our own Blueprint finding, inside our own summary of it. |
| **F-PL-5** | *(2026-09-11, self-caught)* **The re-derivation needed re-deriving.** This session's first tracked/untracked split returned `0 tracked` from a broken `git ls-files` invocation and was very nearly published inside a correction whose whole subject is stale figures. The true figure is **30 of 56**. Recorded rather than quietly fixed, per the 2026-09-10 precedent: *the habit does not transfer by having written the finding down.* |

## Records

- Charter gate: the operator-approved plan, 2026-09-11.
- Intake: `eb12e16` (read-receipt, byte-unchanged; md5 `42f7a2b081908bec6cff1fdd4f413d30`).
- Predecessor: [`campaign_canvas_blueprint`](../campaign_canvas_blueprint/campaign_canvas_blueprint.md) §Completion Summary.

---

## Completion Summary (2026-09-11)

**Chartered and closed the same day.** 5 phases · 1 session · 6 commits · 9 gates green.

| Phase | Shipped |
|---|---|
| **P0** | Intake `eb12e16` (byte-unchanged, md5 verified, standalone). Censuses re-derived (**56** physical `.canvas`, 30/26 tracked; **4 of 25** carry `authority`). Five live stale sites struck **in situ**; four historical copies deliberately untouched. Campaign chartered. |
| **P1** | The under-coverage question **ruled from the pattern's text**. `conform.py` + `diagram_generator` learn both axes (`authority` now **optional**, `production` added, `generator` rejected with a migration hint); `variant_board` + `tuning_surface` re-emit; 4 carriers migrated; sources moved in the same diff. **+10 tests.** ⛩ **F-PL-6** found and fixed as **gate #9**. |
| **P2** | **LIP-0010 converts** — assessment → **Standard proposal, Option D, v2.4.0**. Option B superseded-in-cells/retained-in-mechanism. Firewall touch named file-by-file. §7.7 block added. **`canvas_std` diff 0.** |
| **P3** | **#17 → Berthier DELIVERED** (md5 both ends, their tree +1 untracked, probed at act time). **#18 → SS** staged, then **DELIVERED at close** when the re-probe found their leases clear. Shim trap + foreign-gate guard closed; `AGENTS.md` §What discovery cannot see; `iii/` pin de-duplicated. `idea_memo_number_registry` filed. |
| **P4** | `adr_011` upstream-disposition note (status untouched). AAR. STATE rewritten. Campaign completed. |

**Gate line at close** — pasted from `--markdown`, never retyped:

> `canvas_std` **115/10** · certification **11/11** · `canvas_core` **1040/3** · `canvas_presentation` **57/2** · `canvas_context` **58** · producers **272 across 7 packages** · `comic_render` **154/2** · firewall diff **0** · dual-channel freshness **2/2**

**AAR:** [`plumbline_campaign_aar.md`](missions/artifacts/plumbline_campaign_aar.md)

⛔ **Carried, and owed by the operator:** LIP-0010's **§7.7 signature** — the firewall does not move without it.
✅ **Owed by us: nothing.** #18 was staged at P3 and **delivered at close** — the re-probe found 0 leases where P3 found 2. ⭐ ***A staged memo is not a refused one, and the re-probe is what makes that true.***
