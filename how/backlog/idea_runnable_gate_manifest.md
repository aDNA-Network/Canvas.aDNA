---
type: backlog
idea_id: idea_runnable_gate_manifest
title: "Make the gate set runnable — a prose gate list in STATE.md cannot notice a suite that quietly left it"
created: 2026-09-09
updated: 2026-09-10
status: completed
completed: 2026-09-10
shipped_as: how/gates/gate_manifest.py
priority: medium
origin: "Blueprint P5 close — F-P5-3, found by running canvas_context for the first time in three phases"
executor_tier: sonnet
token_budget_estimated: "small — one script + one doc line; the finding is already measured"
tags: [backlog, gates, ci, testing, regression, f_p5_3, upstream_candidate]
---

# The gate list is prose, so a suite can leave it without anyone being told

## What happened (F-P5-3, measured 2026-09-09)

Blueprint P5 ran `canvas_context` as part of the close sweep. **One test had been failing since
2026-09-07** — `test_pilot_loads_producer_canvas_as_context_without_rendering`, the leg-2 proof.

The cause was entirely benign. P2c legitimately regenerated `document_generator`'s whitepaper
example: section-atomic pagination split it **5 pages → 6** (commit `7e97cfd`; the CANVAS-L-002
residual, and the reason was recorded in the YAML at the time). The example went **32 nodes / 23
edges / 8 panels → 35 / 25 / 9**, and the pilot test had those numbers pinned as literals since
Salon. Four assertions went stale in one commit.

**It stayed red for two days across three phase closes** — P2b, P3 and P4 — each of which published
a gate line reading all-green. Not one of them was lying. `canvas_context` simply **was not in the
gate set**:

| Phase | Gate line published in `STATE.md` |
|---|---|
| Armature (2026-06-23) | `canvas_std` 105/10 · **`canvas_context` 58** · 7 producers 223 |
| P2c (2026-09-07) | `canvas_std` · certification · `canvas_core` · producers · `comic_render` · firewall |
| P3 (2026-09-08) | *(same six)* |
| P4 (2026-09-08) | *(same six)* |

`canvas_context` was in the gate set at Armature and **silently dropped out afterwards.** No commit
removed it; each subsequent close copied the previous close's list. Nothing announces an omission,
because the list is a sentence in a Markdown file that a human retypes each time.

## Why this is worth fixing rather than just noting

This is the F-P2-11 family — *"a check that cannot run is not a check that passes"* — with a nastier
variant: **a check that is not run is not a check that passes, and unlike a skipped check it leaves
no trace in any output.** A skipped test prints `s`. A suite nobody invoked prints nothing at all,
and the gate line beside it reads exactly as green as one that ran everything.

It is also the campaign's own recurring finding wearing new clothes. F-P3-8 established that the
federation index drifted because the pin field has six spellings, so *"no refresh can be mechanised,
and a human who skips one leaves no trace."* This is the same shape one layer down: the gate set is
hand-maintained prose, so a human who drops one leaves no trace.

## What to build

A single runnable manifest — `how/gates/gate_manifest.py` or equivalent — that:

1. **Enumerates every suite by name**, with its expected counts, in one place: `canvas_std` ·
   `canvas_std/certify.py` · `canvas_core` · `canvas_context` · the 7 producers (per-package) ·
   `comic_render` · the firewall diff check.
2. **Runs them all and prints one table**, so a close copies a generated artifact rather than
   retyping last time's sentence.
3. **Fails if a package with tests exists on disk and is not in the manifest.** This is the whole
   point — it makes *omission* an error rather than a silence. Without it, the manifest is just a
   nicer-looking prose list with the same failure mode.
4. Records the runner-env preconditions the close already checks by hand: anaconda pytest, the
   `adna-canvas-std` editable install (which has silently drifted out of the runner env once
   before, at Halftone), and `PYTHONPATH`.

Two traps found while measuring this, worth encoding:

- **The producers count is 267 across *seven* packages, one of which is named `brief_consumer`,
  not `brief_generator`.** A loop over `*_generator` directories silently returns 257 and looks
  right. (Hit live this session.)
- **`cd`-ing into a package for a per-package run persists across shell invocations**, so a
  subsequent `git diff --stat -- what/code/canvas_std/` run from the wrong directory returns empty
  — which is indistinguishable from *"firewall diff 0."* (Also hit live this session, and caught
  only because a `find` on the same path failed loudly a moment later.) The manifest should use
  absolute paths throughout.

## Upstream candidate

The generic form — *a phase-gate list should be executable, and should fail on omission rather than
on disagreement alone* — is not Canvas-specific. Every vault that publishes a gate line in `STATE.md`
has this exposure. Worth an `idea_upstream_` sibling if the local version proves out.

---

## ✅ SHIPPED 2026-09-10 — `how/gates/gate_manifest.py`

Built in `session_stanley_20260910_runnable_gate_manifest`. Contract + rationale:
[`how/gates/AGENTS.md`](../gates/AGENTS.md).

**All four requirements above are met**, and requirement 3 (fail on omission) was verified by
*derivation* rather than by reading the message: a throwaway `what/production/_probe/tests/` package
produced **exit 3 naming the surface**, a perturbed expectation produced **2**, a broken interpreter
path produced **4**, green produced **0**. The firewall's cwd-independence was regression-tested by
breaching `canvas_std` and running from a deep subdirectory — correctly `FAIL`, correctly clean after
restore. Both named traps are encoded in the script: producers are enumerated by name (`brief_consumer`),
and the script never `chdir()`s.

### ⛩ F-GM-1 — what it found on its first run, and the correction it forces on this file's premise

**`what/production/canvas_presentation/` — 57 passed / 2 skipped, real library code, and it had never
appeared in a published `STATE.md` gate line.**

This file's framing said the problem was suites *leaving* the list. That is `canvas_context`'s story.
`canvas_presentation` is a different and harder case: **it never arrived.** Its one appearance anywhere
was a single *commit message* at `53a0213` (2026-08-22) reporting `core+pres 916/5` — and the skip
arithmetic reconciles exactly (core 3 + pres 2 = 5), so that run genuinely included both, while
`STATE.md`'s line tracked `canvas_core` alone throughout (863/3 → 937/3 → 1035/3).

It was **green the whole time**, so nothing was broken. The exposure was never a red suite; it was an
**unwatched** one. And no reviewer re-reading the gate line could have caught it, because there was no
absence to notice — only enumeration against the disk finds this class.

⇒ ***A registry that is only ever read cannot report what was never written into it.***

This is the P3 `federation_index` finding one layer down — *a registry defines its own blind spot in
its membership rule* — and it argues the discovery pass, not the manifest, is the load-bearing half.

### One design requirement this file did not anticipate

"Fail if a test package on disk is not in the manifest" would have gone red on day one:
`what/production/_scaffold/` (inert clone template, its own README excludes it) and
`what/production/tests/` (skip-guarded at adr_009, F-H6RE-2) are **legitimate** non-gates. A check that
is red for good reasons gets disabled. So `EXCLUSIONS` requires a **non-empty stated reason** per entry
plus a path-existence check, and the exclusion registry is validated as strictly as the gate registry.
