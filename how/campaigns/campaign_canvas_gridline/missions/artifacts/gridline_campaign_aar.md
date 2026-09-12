---
type: aar
aar_id: gridline_campaign_aar
title: "AAR — Operation Gridline: the Standard learned both axes, and every check we added found something the check before it had missed"
campaign: campaign_canvas_gridline
created: 2026-09-11
updated: 2026-09-11
status: complete
last_edited_by: agent_mondrian
tags: [aar, gridline, lip_0010, a8, standard_v240, firewall, gate_manifest, reserved_keys, derivation]
---

# AAR — Operation Gridline

**Ran:** 2026-09-11, one sitting, P0–P5, one session. Chartered on the §7.7 signature that Plumbline
had left as its single live item — signed at this campaign's plan gate, making it the shortest gap
between "the operator item is named" and "the operator item is discharged" in this vault's record.

**Shipped:** aDNA Canvas Standard **v2.4.0** — A-8 validates `authority` {`dual_channel`, `view`} and
`production` {`hand_authored`, `generated`}, both optional, `authority` requiring `production`. Third
deliberate `canvas_std` touch since Keystone; **first structural change to the JSON Schema**.
`canvas_std` 115/10 → **146/10** · certification 11 → **12/12** · 9 gates green · LIP-0010 **Final**.

## Worked

- **Running the baseline instead of quoting it.** P0's gate run was scheduled as ceremony and produced
  **F-GL-4** in its first minute — the manifest printing a stale hardcoded `267` beside a derived `272`
  and reporting ALL GATES GREEN. A copied gate line would have carried it forward again.
- **Refusing to rule the two P1 questions.** Both were surfaced to the operator, and **both rulings
  changed the artifact** — the asymmetric A-8 rule, and the `interaction` back-fill. An agent that had
  picked either one silently would have shipped a Standard our own producers could not satisfy.
- **Letting our own code contradict the specification.** The symmetric rule was not caught by
  re-reading the ruling; it was caught because `variant_board.py` **could not emit a conformant canvas
  under it**. ⇒ ***the strongest review of a rule is an existing implementation that has to obey it.***
- **Regenerating rather than hand-editing** the two stale carriers — the discipline `production:
  generated` exists to name — and verifying structure unchanged across the rebuild (22 nodes · 10 edges
  · identical `sync_hash` · 21 affordances) so "regenerated" was a measurement, not a hope.
- **Classifying before sweeping.** 32 files carried a `2.3.0` literal and they split into live pins and
  dated historical claims. A blind pass would have rewritten LIP-0008's history and, worse, **falsified
  two peer vaults' measured declarations** in the federation index.

## Didn't

- ⚠ **I wrote "147 passed / 10 skipped" and "CERTIFIED 12/12" into a README before running anything.**
  The real figure was **142**. Caught within the minute — but it went into a file, and it is the exact
  defect family this campaign's charter names. **Deriving after asserting is not deriving.**
- ⚠ **My first backward-compatibility sweep reported "0 failures" and was asking the wrong question.**
  `validate_suite(doc)`'s `declared` parameter defaults to `CORE`, so it measured every aDNA-Native
  canvas against the weakest level and returned a true answer to a question nobody asked. It was caught
  only because the same script also printed the carriers it had just declared healthy — **two of which
  were visibly `generator`.** ⇒ ***a green from the wrong predicate is indistinguishable from a green
  from a check that never ran*** — and the shipped CLI had it right all along.
- ⚠ **I left the superseded "two keys or neither" phrasing inside the schema `$comment`** after the rule
  was corrected — the old wording surviving inside the artifact that implements the new one. Caught on
  the residual-sweep, not by remembering.
- ⚠ **I mis-derived the freshness gate's tuple** (`actual` is `(checked, 0)`, not `(fresh, stale)`) and
  would have shipped a reporter that printed `1/1` for one-of-two-stale. Caught by reading the producing
  code instead of trusting the shape I expected.
- **A `$?` after a pipe reported the wrong exit code** in one verification. Harmless here, corrected in
  place, noted because it is the same class: a status read from the wrong object.

## Finding

⭐ **Every check this campaign added or touched found a defect in the check that preceded it — three
of them inside the one file written to end that family.**

| # | Where | What was unverified |
|---|---|---|
| F-GL-2 | `firewall` gate | `git diff` is **unstaged-only** — it missed **staged** and **untracked** breaches entirely, i.e. two of three classes, including the one a firewall touch necessarily performs. Never fired because no campaign before this one had staged a `canvas_std` change. |
| F-GL-4 | producers total | a hardcoded `'267/7 pkg'` printed beside a derived `272`, verdict green |
| F-GL-7 | the **gate line generator** | **hardcoded green** for all three non-pytest gates — `"firewall diff **0**"` was a *constant string*, printed while the firewall was FAILING, in the one string a close **pastes** into `STATE.md` |
| F-GL-1 | `RESERVED_KEYS` | no consumer at all; `interaction` missing from **all three** copies of the namespace since v2.2.0 |
| F-GL-6 | LIP-0010's backward-compat claim | `25 of 25` was `23 of 25`, and **the disproof was in Plumbline's own pasted census, four lines away** |

⇒ ***The report is part of the check.*** A gate that observes correctly and then reports a literal has
only moved the unverified claim one layer out — and the outermost layer is the one that gets published.
F-GL-2 adds the sharper half: ***a predicate only ever run against a clean tree has only ever been
tested for its false case.***

## Change

1. **A non-OK gate can no longer render as green.** `markdown_gate_line()` derives every cell from
   `gate.actual`/`gate.meta` and appends `⛔ <status>` to any failing gate. The line is now unpasteable
   as a false green.
2. **The firewall predicate is `git status --porcelain`** — staged, unstaged and untracked, with the
   breach classes named in the detail.
3. **One definition, two enforcement points.** `conform.py` and `diagram_generator/model.py` import the
   axis sets from `canvas_std.reserved` instead of restating them, and both enforce A-8's asymmetry at
   build time so a producer cannot emit a canvas the validator will refuse.
4. **Six now-false "canvas_std does not validate this key" claims corrected where they were written** —
   including a test docstring that had predicted its own expiry and reached it.
5. **§7.7 amendments are a dated erratum table**, not an in-place edit: what changed, who ruled it, why
   the original was wrong.

## Follow-up

- `idea_reserved_keys_has_no_consumer` — **open**, medium. The durable fix was declined deliberately;
  the cheap half (assert every key the validator dispatches on appears in both lists, derived by
  walking the dispatch sites) is what would have caught `interaction` in June.
- **`adna_version` has three values across five emitters** (`2.0.0` ×3 · a constant · `2.3.0`). Left
  alone with the reason on the line — bumping one of five makes it four values, not one. Needs a ruling
  on what the field *means* before any of them move.
- **Memo #19 → Rosetta, staged**: `ack_required: true` (their finding, our corrected default). It takes
  up their explicit `draft` invitation and reports that one sentence of the pattern supports two
  readings, with the reachable one being wrong. **Their call, not a defect claim.**
- Upstream candidates, unfiled per `skill_upstream_contribution`: the gate-manifest generic form (from
  2026-09-10) and now *a hand-maintained inventory needs a consumer or a discovery pass*.
