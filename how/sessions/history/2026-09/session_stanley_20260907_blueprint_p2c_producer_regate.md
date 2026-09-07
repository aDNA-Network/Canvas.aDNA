---
type: session
session_id: session_stanley_20260907_blueprint_p2c_producer_regate
created: 2026-09-07
updated: 2026-09-07
status: completed
tier: 2
persona: mondrian
operator: stanley
campaign: campaign_canvas_blueprint
phase: P2c
executor_tier: opus
last_edited_by: agent_mondrian
tags: [session, canvas, blueprint, p2c, producer_regate, layout_fit, visual_gate, traps, deck_profile]
---

# Session — Blueprint P2c: the producer re-gate

## Intent

Discharge `mission_b2_authoring_rail`'s follow-up **(a)** — the producer-wide re-gate — which its
own AAR sequenced ahead of the deferred P2b conversion memos:

> *"offering conversions while our own shelf fails the gate repeats the credibility problem the
> dogfood just fixed."*

`skill_canvas_producer_build.md` §6 declares `canvas-visual-check … --strict` **mandatory** for
every producer. It had not been run against the shipped examples since the trap corpus grew to 14.
`diagram_generator` was repaired at P2; five producers were left measured but untouched.

## Scope declaration (Tier 2)

**Writes:** `what/production/canvas_core/` (new `layout_fit.py`, `traps/cli.py`,
`traps/cv_lead_cost_01.py`, tests) · `what/production/*/src/*/layout.py` + regenerated
`examples/*.canvas` · `what/production/_scaffold/` · `how/skills/skill_canvas_producer_build.md` ·
`how/campaigns/campaign_canvas_blueprint/` · `STATE.md`.

**Firewall:** `what/code/canvas_std/` untouched — `git diff --stat` verified 0 at open and at close.

**Conflict scan:** `how/sessions/active/` empty but for `.gitkeep` at open; `git status` clean at
`57c5a67`. No peer session **at open**.

⚠ **A peer appeared mid-session, and it was not caught by the open-time scan.** Operation Polyglot
(`session_stanley_20260907_000227_polyglot_openai_backend`, cross-vault sitting) committed
`eb8939d` + `79f41e2` into this vault while this session ran — the `openai` GENERATE backend,
`adr_008` Amendment 1, and a STATE banner. Detected only when an edit reported the file had changed
on disk. Handled per the vault's concurrent-commit discipline: git kept read-only, HEAD re-checked
at close, their STATE banner left intact above ours, **their +11 `comic_render` tests explicitly
attributed to them in our gate evidence** rather than absorbed into our numbers, and this session's
changeset committed separately. *(They also swept this session file into `79f41e2` while closing
their own lease, so it is tracked from their commit, not ours.)*

## Gate

Plan approved by the operator 2026-09-07 with three rulings — see the mission file. Folded into
`campaign_canvas_blueprint` as **P2c**, a dated scope amendment, not a sibling campaign.

## Log

*(appended as work lands)*

- **Open.** Census re-derived rather than re-read (ratified practice, `STATE.md` §Carried #6): the
  F-P2-6 table reproduces exactly — 99 findings / 13 HIGH / 0 CRITICAL. Two corrections found in
  the act of re-deriving it: **F-P2-8** (the published file count is 7, not 6) and **F-P2-9**
  (`CV-LEAD-COST-01`'s fix hint recommends a lead that trips `CV-HIERARCHY-01`).
- **b2c.1** `canvas_core/layout_fit.py` + 64 tests — the tests assert *agreement* (size through the
  helper, run the trap, require zero findings), not arithmetic in isolation.
- **b2c.2** `deck` profile ruled → **F-P2-10** (it is a re-aim, not a relaxation: 19 → 13, and it
  surfaced a HIGH the default profile had been hiding). `CV-LEAD-COST-01` fix hint corrected;
  `what/docs/canvas_authoring_guidance.md` rule 1 corrected with it.
- **b2c.3** `diagram_generator` retrofitted; the four interim mirrored constants deleted. Example
  geometry changed (nodes got *smaller* — the mirror over-estimated); still 0 findings, 44 tests.
- **b2c.4** `document_generator` 52 → 0. Golden rebaselined deliberately (renamed off "e41", with a
  note on how and why to regenerate). **F-P2-11**: honest heights exposed a CRITICAL page overflow
  that had always been real; both example documents split at the offending section.
- **b2c.5** deck / brief / letter / post repaired. Deck kept its 16:9 box and gained aspect-ratio
  metadata. `test_post.py` now selects copy nodes by semantic role instead of an id prefix that
  silently counted the new title card as a post.
- **b2c.2b** Operator ruling on `CV-AUDIENCE-01` → **F-P2-12** (it scored the enclosing frame as a
  slide) and **F-P2-13** (the first draft of the advisory rule would have made 13 of 14 traps
  non-gating; caught by auditing it against the registry before trusting it).
- **b2c.6** Three assets generated from a committed deterministic builder. Restoring them turned
  `file_missing` into `aspect_drift` — a second defect the first had been masking; closed with
  `fit_image_box`, which fits both axes rather than clamping height and letting width drift.
- **b2c.7** `_scaffold` and `skill_canvas_producer_build.md` updated so the class cannot recur.
- **b2c.8** Full verification (below). Records filed; mission closed complete-with-open-item.

## SITREP

**Completed.** Blueprint **P2c** — the producer re-gate. One shared `canvas_core/layout_fit.py`
(producers and traps now measure with the same function); all 6 producers retrofitted; a `deck` trap
profile; an advisory-trap gating rule; 3 generated example assets; the recurrence path closed in the
scaffold and the skill. **13 authored surfaces gate clean, each stated with its profile.** Six
findings recorded (F-P2-8 … F-P2-13), one of them a correction struck in place at its source.

**In progress.** Nothing. P2c closed.

**Next up.** Operator's choice at the gate: **P2b** (conversion memos #10/#11 — now unblocked, since
the shelf passes the gate the offers ask others to adopt) or **P3** (federation re-pin wave).

**Blockers.** None. Carried and explicitly not done: the Amendment-1 agent-confirmed render (no safe
window-scoped capture on this node — whole-screen `screencapture` remains ruled out); the
`CV-AUDIENCE-01` calibration cycle, which now runs against real decks and says a normal
title-plus-content deck is uneven.

**Gate evidence.** `canvas_std` 115/10 · certification 11/11 · `canvas_core` 937/3 · producers 267
(diagram 44 · document 37 · deck 16 · brief 10 · letter 17 · post 20 · comic 123) · `comic_render`
154/2 *(the +11 over 143/2 is Operation Polyglot's, not ours)* · firewall `git diff --stat --
what/code/canvas_std/` **empty** · every example byte-identical on rebuild · all 10 examples
`adna_native [OK]` · `what/lattices/examples/` untouched.

**Files touched.** `what/production/canvas_core/{layout_fit.py (new), traps/cli.py,
traps/cv_audience_01.py, traps/cv_lead_cost_01.py, tests/*}` · each producer's
`src/*/{layout,consume,blocks,slides,__init__}.py` + `pyproject.toml` + regenerated
`examples/*.canvas` · `document_generator/tests/golden/document_small.canvas` (rebaselined) ·
two example `.yaml` (sections split; image refs repointed) · `what/specs/diagrams/` (new: builder +
2 PNGs) · `what/production/_scaffold/*` · `how/skills/skill_canvas_producer_build.md` ·
`what/docs/canvas_authoring_guidance.md` · `how/campaigns/campaign_canvas_blueprint/*` · `STATE.md`.

## Next Session Prompt

Blueprint P2c is closed: the producer shelf now passes its own visual gate, with producers and traps
sharing one measurement (`canvas_core/layout_fit.py`), a `deck` trap profile, and an advisory-trap
rule so an ungraduated trap reports without gating. The next gate is the **operator's choice between
P2b and P3**, and P2b is the sequenced one — `mission_b2`'s AAR deferred conversion memos **#10**
(Operations, 5 standard-blind C08 canvases) and **#11** (ScienceStanley, 29 bare files) until our own
shelf passed the gate, which it now does, so the offers can carry worked conversions rather than a
proposal. Before writing either memo, re-verify the target counts **at source** rather than citing
the 2026-08-22 census (Estafette's delivery-defect precedent, and F-P2-8's lesson that a stated
population still needs re-deriving). Alternatively P3 is the federation re-pin wave (`mission_b3`:
VisualDNA lockstep-flip mechanics, `canvasforge/`→`canvas/` with Seshat, 5 stale + 3 misnamed
wrappers). Standing carried items either way: the **Amendment-1 agent-confirmed render** for the two
dogfood canvases still has no safe path on this node (port Home.aDNA's `canvas_visual_loop.py` for a
window-scoped capture; whole-screen `screencapture` is ruled out); **`CV-AUDIENCE-01` needs its
calibration cycle** now that a `deck` profile makes it run; the III registry's
`cycles_fired`/`cycles_accepted` counters are **unmaintained** and were nearly load-bearing in a
gating rule (F-P2-13) — maintain them or stop shipping them; and `canvas_core/__init__` eagerly
imports `print`, taxing six producers with a Pillow install to reach pure arithmetic. Operator
signatures still owed: `adr_010`, `adr_011`, `adr_012` §7.7 (adr_012 was **corrected twice** on
2026-09-07 — read before signing), plus `adr_008` Amendment 1 from the concurrent Polyglot session.
**b1.5 remains open** — Rosetta has three artifacts (memo #9, erratum v2, E2) and the pattern is not
ratified until they rule; the phase does not advance on their silence.
