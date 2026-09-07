---
mission_id: mission_b2c_producer_regate
type: mission
campaign: campaign_canvas_blueprint
phase: P2c
title: "The producer re-gate — one shared measurement, not five hand-repairs"
owner: stanley
persona: mondrian
status: completed
created: 2026-09-07
updated: 2026-09-07
completed: 2026-09-07
completion_note: "complete-with-open-item — every shipped surface passes its own domain's gate, but the Amendment-1 agent-confirmed render is still carried (no safe window-scoped capture on this node), and CV-AUDIENCE-01's calibration cycle is deferred."
last_edited_by: agent_mondrian
executor_tier: opus
token_budget_estimated: ~150k
session: session_stanley_20260907_blueprint_p2c_producer_regate
tags: [mission, blueprint, p2c, producer_regate, layout_fit, canvas_core, traps, deck_profile, visual_gate]
---

# Mission B2c — The producer re-gate

## Gate

Opened at the operator's plan gate, **2026-09-07**. P2c is a **dated scope amendment** to
`campaign_canvas_blueprint` — the campaign's own precedent is to fold adjacent work in as an added
phase rather than charter a sibling.

Three rulings taken at that gate:

| # | Ruling |
|---|---|
| 1 | **Work order** — the re-gate runs *before* the deferred P2b conversion memos (#10 Operations, #11 ScienceStanley), per `mission_b2`'s own follow-up (e). |
| 2 | **Rule the deck profile before repairing the deck** — 8 of deck's 19 findings come from the three traps `cli.py` names `_KNOWLEDGE_CANVAS_AESTHETICS`, the same set Halftone H6 ruled inapplicable to comic pages. Add a `deck` profile; repair only what survives it. |
| 3 | **Generate the three missing example assets**, rather than repointing the refs or deleting the image blocks. |

## The gap this closes

`skill_canvas_producer_build.md` §6 declares the visual gate **mandatory** for every producer. It
was not being run. The trap corpus grew from its Halftone-era size to **14** while shipped examples
were never re-gated — the defect F-P2-3 caught in `diagram_generator` (its own example failing three
traps since Atelier at ~14% of its source text shown) was never producer-specific.

P2 repaired one producer. This mission repairs the shelf, and repairs it in a way that cannot
silently drift again: producers and traps measure with **one function**, not two independently
guessed models.

## Ground truth — re-derived 2026-09-07, not re-read

`canvas_core/.venv/bin/python canvas_core/traps/cli.py <f> --strict`, from `what/production/`:

| Producer | File(s) | Findings | HIGH |
|---|---|---|---|
| `document_generator` | `grant_proposal` · `canvas_standard_whitepaper` | 26 + 26 | 5 + 5 |
| `deck_generator` | `canvas_standard_deck` | 19 | 2 |
| `brief_consumer` | `canvas_standard_brief` | 17 | 1 |
| `post_generator` | `example_post_single` · `example_post_thread` | 2 + 4 | 0 |
| `letter_generator` | `example_letter` | 5 | 0 |
| `diagram_generator` · `comic_generator` · `comic_render` (own profiles) | — | **0 [OK]** | — |

**99 findings · 13 HIGH · 0 CRITICAL** — F-P2-6's totals reproduce exactly.

**89 of 99 (90%) are the four classes already solved once in `diagram_generator`:**
`CV-TEXT-BOUNDS-01/overflow` 55 · `CV-LEAD-COST-01/heading_lead` 20 ·
`CV-GROUP-PADDING-01/aggregate_fill` 10 · `CV-HIERARCHY-01/title_slot_missing` 4.
The other 10 are new classes: `CV-GROUP-LABEL-01/label_truncates` **7 HIGH** ·
`CV-FILE-PROPS-01/file_missing` **3 HIGH**.

**Root cause of the 55.** Every producer carries its own naive
`est_text_height(text, wrap=…, line_h=…, pad=…)` — a character-count guess with per-producer
constants (`deck_generator/layout.py:52` wrap=60/line_h=30; `document_generator/layout.py:75`
wrap=88/line_h=24; siblings likewise). The traps measure with the Obsidian-CSS-calibrated model in
`canvas_core/text_metrics.py`. **Producer and trap have never shared a measurement.**
`diagram_generator/layout.py:45` already says so about its own interim constants.

## Findings

- **F-P2-8 (2026-09-07) — the published file count was 6; it is 7.** The census in F-P2-6 lists
  document ×2, deck ×1, brief ×1, post ×2, letter ×1 — which sums to **7**, and its own headline
  reads "6 files · 5 producers · 99 findings · 13 HIGH". Findings, HIGH, CRITICAL and the producer
  count are all correct; only the file count is wrong, by one.

  ⚠ Worth more than its size. F-P2-6 is *the record that established* the practice **state the
  population on the face of the number**, ratified by Hopper as their ADR-011 A8 §5 after six
  instances in one week across four desks. This is instance seven, inside the record itself, and it
  survived the correction pass that produced F-P2-7 two days later. ⇒ The practice is necessary and
  **not sufficient**: stating a population does not verify it. What caught this was re-deriving the
  table row by row before acting on it. Struck in place at the source, never rewritten.

- **F-P2-9 (2026-09-07) — `CV-LEAD-COST-01`'s fix hint walks the author into `CV-HIERARCHY-01`.**
  `cv_lead_cost_01.py:68-71` emits *"use a `**bold**` lead (40.0px) instead"*. F-P2-3 measured that
  `**bold**` carries **no heading marker** and therefore trips
  `CV-HIERARCHY-01/title_slot_missing`; `####` (42.6px) is the only lead form that clears **both**.
  Following the tool's own documented advice produces a canvas that fails a sibling trap in the same
  pack, in the same run.

  ⇒ F-P2-3 was reported as a contradiction *between two checks* and repaired in the producer. It was
  also live **in a fix hint**, where it is worse: a check that fails tells you something is wrong; a
  fix hint that fails tells you what to do, and is believed. The 2.6px it saves is not worth the
  sibling failure it causes. **Generalisation: when two checks in one pack constrain the same
  property, their fix hints are part of the contradiction surface and must be re-derived together.**

- **F-P2-10 (2026-09-07) — the wrong profile under-reports as readily as it over-reports, and
  F-P2-6 only caught the over-reporting half.** The `deck` profile was ruled on the expectation
  that it would *relax* the gate: drop the 3 knowledge-board aesthetics a 16:9 slide fails by
  design, 19 → **11**. Measured, it is **13** — because a deck profile must also **admit** the
  `deck-specific` traps and the presentation-metadata trap that `knowledge-canvas` suppresses
  *precisely because* they presume a deck. Two checks the default run could not see:

  | Admitted by `deck`, hidden by the default | |
  |---|---|
  | `CV-AUDIENCE-01/audience_variance` | **HIGH** — one slide carries 186 words against a deck mean of 53 (CV 1.06 > 0.50) |
  | `CV-DIMENSION-VISIBILITY-01/aspect_ratio_missing` | MEDIUM — the deck declares no aspect-ratio metadata, which a deck genuinely should |

  ⇒ A profile is **a re-aim, not a relaxation.** F-P2-6 framed profile mismatch as a false-positive
  problem — *"I reported a solved problem as an open one"* — and the correction it drew was to
  state the profile. That is necessary and, again, not sufficient: the same mismatch was
  **concealing a HIGH** on the same file, in the same runs, for as long as the over-report existed.
  Running everything under one profile does not bias a census in one direction; it decouples it
  from the domain in both. **The census F-P2-6 corrected was still wrong about the deck — it said
  19 where the answer is 13, and it was missing a HIGH.**

- **An 8th failing file, outside the census.**
  `document_generator/tests/golden/document_small.canvas` — 10 medium (`CV-LEAD-COST-01` ×5 among
  them). A golden, not a shipped example, so it regenerates with the repair rather than needing its
  own fix — but it is a file the census did not see, and the census did not say it was looking only
  at `examples/`.

- **F-P2-11 (2026-09-07) — the honest measurement made a real defect visible, and it was ours.**
  With text heights corrected, `grant_proposal` drew a **CRITICAL** `edge_violation`: a section
  overflowed its own page by 142px. Not a regression — `layout.paginate` is **section-atomic** and a
  section taller than one US-Letter content column (912px) gets its own page and is *allowed* to
  overflow it, the documented CANVAS-L-002 residual. The combined "Research Strategy" section
  measured 1054px. It had always been too tall; the under-estimate hid it. ⇒ Both example documents
  were split at the section that exceeded the limit, with the reason recorded in the YAML.
  **Correcting a measurement does not only remove false findings — it admits the true ones that the
  bad measurement was suppressing.**

- **F-P2-12 (2026-09-07) — `CV-AUDIENCE-01` counts the frame as a slide.** It sampled *every* group,
  so a deck's enclosing `deck_root` — whose text is the union of all the slides' — was scored as a
  slide. It is an outlier **by construction** on any deck with more than one slide, *and* it inflates
  μ and σ, which can mask a genuine outlier among the real slides. Both directions wrong, from one
  line. Fixed by excluding groups that enclose another group (bounding-box test; substrate-neutral).
  Latent because the trap is `deck-specific` scope and the only profile that runs it was created
  today.

- **F-P2-13 (2026-09-07) — the governance rule I wrote first would have silenced the entire gate.**
  The operator ruled that an ungraduated trap should report but not gate. The obvious predicate —
  *"`graduated: false` and `cycles_accepted == 0`"* — reads exactly right and captures **13 of the
  14 live traps**, including `CV-TEXT-BOUNDS-01`, which fired 55 times in this session and caught
  the Oration M-R5 incident. It was written, then audited before being trusted, and the audit is the
  only reason it did not ship.

  The cause: `cycles_fired`/`cycles_accepted` were **never maintained** — every trap but one still
  reads `fired=0`. So `fired == 0` means *"no record either way"*, not *"never useful"*. The
  narrowed predicate (`fired > 0 and accepted == 0`) changes exactly 3 traps and leaves 11 gating.

  ⚠ **The generalisation is uncomfortable and worth keeping:** *a governance rule that reads as
  principled is more dangerous than one that reads as arbitrary, because nobody audits it.* This one
  cited real registry fields, matched the operator's ruling word for word, and would have turned the
  visual gate into a no-op while every report kept saying `[OK]`. The registry's III counters are
  **not a trustworthy substrate** for gating decisions; this uses the single unambiguous signal in
  them and no more.

## Objectives

| # | Objective | Status |
|---|---|---|
| b2c.1 | `canvas_core/layout_fit.py` + 64 tests — one shared measurement | ✅ done |
| b2c.2 | Rule the `deck` profile; fix the `CV-LEAD-COST-01` hint (F-P2-9) | ✅ done |
| b2c.3 | Retrofit `diagram_generator` onto `layout_fit` (interim mirror retired) | ✅ done |
| b2c.4 | Repair `document_generator` (52 → 0; golden rebaselined) | ✅ done |
| b2c.5 | Repair `deck` · `brief` · `post` · `letter` | ✅ done |
| b2c.6 | Generate the 3 missing example assets (from a committed builder) | ✅ done |
| b2c.7 | Close the recurrence path (`_scaffold` + the skill's gate command) | ✅ done |
| b2c.8 | Verification sweep · records · AAR | ✅ done |

## Result

**Every shipped surface passes its own domain's gate**, stated with its profile:

| File | Profile | Before | After |
|---|---|---|---|
| `grant_proposal` · `canvas_standard_whitepaper` | knowledge-canvas | 26 + 26 (10 HIGH) | **0 · 0** |
| `document_small` (golden) | knowledge-canvas | 10 | **0** |
| `canvas_standard_deck` | deck *(new)* | 19 under the wrong profile | **0 gating** (4 advisory) |
| `canvas_standard_brief` | knowledge-canvas | 17 (1 HIGH) | **0** |
| `example_letter` | knowledge-canvas | 5 | **0** |
| `example_post_single` · `example_post_thread` | knowledge-canvas | 2 + 4 | **0 · 0** |
| `canvas_standard_flow` | knowledge-canvas | 0 | **0** (retrofitted, still 0) |
| `science_stanley_mini_issue` · `mini_issue` | comic | 0 | **0** |
| the two P2 dogfood canvases | knowledge-canvas | 0 | **0** |

⚠ **State the population.** That is **13 authored surfaces** — 11 producer examples/goldens plus the
2 dogfood canvases. It is *not* every `.canvas` in the vault. The remainder, deliberately out of
scope and named rather than quietly excluded:

- **13 conformance-suite fixtures** (`canvas_std/tests/fixtures`, `canvas_context/tests/fixtures`) —
  deliberately span valid/invalid/minimal; the visual gate does not apply to a file whose job is to
  be malformed. Certification is **11/11**.
- **15 files under `what/artifacts/`** — the gitignored on-node corpus (`adr_010`), not published.
- **4 files under `what/lattices/examples/`** — untouched by standing order, verified `git status`
  clean.

**Gate evidence:** `canvas_std` **115/10** · certification **11/11** · `canvas_core` **937/3** ·
producers **267** (diagram 44 · document 37 · deck 16 · brief 10 · letter 17 · post 20 · comic 123) ·
`comic_render` **154/2** · firewall `git diff --stat -- what/code/canvas_std/` **empty** · every
example **byte-identical on rebuild** · all 10 examples `canvas-std validate --level adna_native`
**[OK]**.

⚠ **Not met, carried:** the Amendment-1 agent-confirmed render. Still blocked on a window-scoped
capture (whole-screen `screencapture` remains ruled out — it recorded a third party's private
messages at P2). The machine gate is **not** reported as a substitute.

## Discipline

- `what/code/canvas_std/` **untouched**; `git diff --stat` verified 0 at open and close.
- Every example regenerated from its `.yaml` via the producer's own `build` CLI — never hand-edited.
- Every gate result **states its profile**. A bare `[FAIL]` is not a measurement (F-P2-6).
- Corrections to published figures are **struck in place**, not rewritten (vault practice).

## AAR

**Worked.** Fixing it once. 89 of 99 findings were four classes already solved in
`diagram_generator`, and `canvas_core/text_metrics` already held the answer —
`obsidian_required_node_height()` is literally the number `CV-TEXT-BOUNDS-01` prints in its own fix
hint. `layout_fit` mostly *delegates*; it implements almost nothing. Five hand-repairs would have
produced five slightly different answers and a sixth drift to find later.

**Didn't.** The Amendment-1 render, again — same blocker as P2, untouched. And the deck's four
advisory findings are visible but unresolved: `CV-AUDIENCE-01` needs the calibration cycle its own
docstring scheduled, which this mission deliberately did not attempt.

**Finding.** Three that outlive the mission. *(1)* **A profile is a re-aim, not a relaxation**
(F-P2-10) — F-P2-6 caught the wrong profile *over*-reporting; the deck profile caught it
*under*-reporting a HIGH on the same file in the same runs. Running one profile over everything does
not bias a census in one direction, it decouples it from the domain in both. *(2)* **Correcting a
measurement admits true findings, not just removes false ones** (F-P2-11) — an honest height turned
a passing example into a CRITICAL page overflow that had been real all along, and restoring three
missing PNGs turned `file_missing` into `aspect_drift`: a check that cannot run is not a check that
passes. *(3)* **A governance rule that reads as principled is more dangerous than one that reads as
arbitrary, because nobody audits it** (F-P2-13) — the first draft of the advisory-trap rule cited
real registry fields, matched the operator's ruling word for word, and would have made 13 of 14
traps non-gating while every report still said `[OK]`.

**Change.** Producers and traps now share one measurement (`canvas_core/layout_fit.py`);
`####` is encoded as the canonical lead in one place instead of rediscovered per producer; a `deck`
profile exists; `CV-LEAD-COST-01` no longer advises a fix that trips its sibling; `CV-AUDIENCE-01`
no longer scores the frame as a slide; ungraduated-and-never-accepted traps report without gating;
the `_scaffold` a new producer clones now imports `layout_fit` and carries a worked example, and the
skill's documented gate command carries `--profile`.

**Follow-up.** *(a)* `CV-AUDIENCE-01`'s calibration cycle — it now runs against real decks and says
a normal title-plus-content deck is uneven. *(b)* The III registry counters
(`cycles_fired`/`cycles_accepted`) are unmaintained and were nearly load-bearing; either maintain
them or stop shipping them as if they mean something. *(c)* `canvas_core/__init__` eagerly imports
`print` (hard PIL dependency), so a producer pays a Pillow install to reach ~300 lines of
arithmetic; making the re-exports lazy would remove the tax from six producers and `comic_render`.
*(d)* Amendment-1 window-scoped capture — still carried from P2. *(e)* P2b conversion memos
**#10/#11 are now unblocked**: the shelf passes the gate the offers ask others to adopt.
