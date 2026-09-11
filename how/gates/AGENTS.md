---
type: directory_index
created: 2026-09-10
updated: 2026-09-10
last_edited_by: agent_mondrian
tags: [directory_index, gates, ci, regression, f_p5_3, upstream_candidate]
---

# how/gates/ — The gate set, executable

## Purpose

`gate_manifest.py` **is** the gate set. Not a description of it — the thing itself.

Run it before any phase close, campaign close, or push batch:

```sh
python3 how/gates/gate_manifest.py --markdown     # run everything, emit the STATE.md line
python3 how/gates/gate_manifest.py --discover-only # omission check only; runs no tests (~1s)
```

## The standing rule

**A close pastes this script's generated output. It never retypes the previous close's sentence.**

That rule is the whole point, and it is worth knowing why it exists.

## Why this directory exists (F-P5-3)

The gate set used to be a sentence in `STATE.md` that a human retyped each close. `canvas_context`
was in that sentence at Armature, **silently fell out afterwards**, and then sat **red for two days
across three consecutive phase closes** — P2b, P3 and P4 — each of which published an all-green gate
line. None of them was lying. No commit removed the suite; each close simply copied the previous
close's list.

> **A skipped test prints `s`. A suite nobody invoked prints nothing at all, and the gate line
> beside it reads exactly as green.**

This is the F-P2-11 family (*a check that cannot run is not a check that passes*) with a nastier
variant: **a check that is not run leaves no trace in any output at all.**

## The three registries

| Registry | Job |
|---|---|
| `GATES` | Every suite by name, with the counts it must produce. Producers are enumerated **by name**, never globbed. |
| `EXCLUSIONS` | Test-bearing directories that are deliberately not gates. **Every entry must carry a non-empty reason**, and the path must exist. |
| discovery | Walks the vault for test-bearing directories and **fails if any is in neither registry**. |

Discovery is the load-bearing one. Without it this file would be a prose list written in Python,
carrying the exact failure mode it replaces. `EXCLUSIONS` exists because a check that goes red for
*good* reasons gets disabled — the escape hatch has to exist, and it has to justify itself in the
same file as the rule.

## Exit codes are distinct on purpose

`0` green · `1` a suite failed · `2` counts disagree · `3` **an undeclared surface exists** ·
`4` a runner-environment precondition failed.

*Disagreement* and *omission* are different bugs and must never share an exit code. A precondition
fault (the `adna-canvas-std` editable install drifting out of the runner env, which happened once at
Halftone) presents as a mass test failure unless it is checked first and reported separately.

## ⚠ The rule that matters most

**A disagreement is a finding to investigate, not a number to edit into the manifest.**

Editing the expectation to match the observation converts this file back into the thing it replaced,
and it is precisely the defect family Operation Blueprint found **nine times** — *a stated fact
nobody re-derived*. If a count moves, find out why it moved before you touch this file.

## Traps encoded here, each hit live at the Blueprint P5 close

- **Absolute paths throughout; the script never `chdir()`s.** A `cd` into a package persists across
  shell invocations, so a later `git diff --stat -- what/code/canvas_std/` from the wrong directory
  returns empty — **indistinguishable from `firewall diff 0`**. Regression-tested from a deep
  subdirectory.
- **The seventh producer package is `brief_consumer`, not `brief_generator`.** A `*_generator` glob
  silently returns 257 and looks right.
- **Preconditions are checked before anything runs**, because a wrong environment makes every
  number below it meaningless.

### Added 2026-09-11 (Plumbline P3) — the shim trap, contributed from outside

- **Discovery uses `find -P` semantics: it does not follow symlinks, and it reports every one it
  skips.** Rosetta (aDNA.aDNA) measured the cost of the other choice: a census run as
  `ls */what/lattices/examples/*.canvas` reads **254 files across 62 vaults** where the physical
  truth is **282 across 69** — 14 root-level back-compat shims, followed by the glob, so live vaults
  count twice under two names and archived vaults reappear inside the live set.

  > ***A shim is a second true name for one object, and a glob cannot tell a name from a thing.***

  ⚠ **This vault already instantiates it at its own root.** `./git` and `./iii` are symlinks into
  `how/federation/`, so `ls */CLAUDE.md` reports **two** federation wrappers where there are
  **three** — naming both of the two by their *second* name, and missing `comfyui/`, which has no
  shim at all.

  The omission **verdict** was already safe (both sides `.resolve()`). What was not safe was the
  **population line**, which counted names rather than things — *in the file whose entire thesis is
  enumerate the territory, don't re-read the map.* Verified by derivation, not by reading the
  message: with a shim planted under `what/production/`, the old code printed
  `15 test-bearing surfaces … (13 gated)` **with a correct verdict and exit 0**; the new code prints
  `14 … (physical) … 1 symlink shim(s) skipped` and names it.
- **No declared gate may resolve outside the vault** (exit **4**, precondition — not exit 3).
  `run_gate()` sets `cwd=` to the gate path, so a gate pointed through a shim into a peer vault would
  run their suite and write `.pytest_cache/` into their tree, against this vault's read-only conduct
  with peers. The realistic path to that is an agent adding a shim to `GATES` to clear an exit-3
  omission — by accident, not malice.

## ⛔ What discovery cannot see — its membership rule, stated so the blind spot is named

Discovery's rule is: **a directory named `tests`, at exactly depth 1 under `what/production` or
`what/code`, containing at least one `test_*.py`** (plus a bare `tests/` directly under either
parent).

Three things are therefore invisible **by construction**:

1. tests living anywhere outside those two parents (e.g. under `how/`);
2. a directory spelled `test/` rather than `tests/`;
3. `test_*.py` sitting at a package root rather than inside a `tests/` directory.

**Measured 2026-09-11: zero such files exist.** The exposure is real and currently costs nothing.

⇒ ***A registry defines its own blind spot in its membership rule*** — the P3 `federation_index`
finding, reappearing inside the file written to fix registries. It is **named here rather than coded
around**: widening the walk costs runtime at every close and buys nothing measurable today, and what
made `federation_index` wrong for five weeks was not a narrow rule but an **unstated** one.

## What it found on its first run (2026-09-10)

`what/production/canvas_presentation/` — 57 passed / 2 skipped, real library code, **never present in
any published `STATE.md` gate line**. Unlike `canvas_context` it had not fallen out; it had never
been enumerated. It was green, so nothing was broken — but it had been ungated for its whole life,
and no amount of careful re-reading would have surfaced it. It is now gate #8.

## What it found on its second outing (2026-09-11, Plumbline P1) — gate #9

`dual_channel_freshness`. Both of this vault's dual-channel canvases — the pair
`pattern_diagrammatic_context` cites **by name** as its motivating example — were **stale**, and had
been since 2026-09-07 when the P2c re-gate changed the layout engine. They stayed stale through
**P2c, P3, P4, P5 and the Blueprint close: five all-green gate lines.** Rebuilding from their own
unmodified sources differed by 36 and 32 lines.

The pattern's central law is *"drift between channels is a defect, not a chore."* Nothing enforced
it: the visual gate checks a canvas **as it stands**, and no check compared a generated artifact to a
regeneration of it.

> ⇒ ***A generated artifact that nobody regenerates is a claim nobody re-derived.***

Sibling of **F-P5-3** (a suite nobody invoked) and **F-GM-1** (a suite never enrolled) — a third
variant of the same family, one layer out from tests. The gate rebuilds every `*.diagram.yaml` into a
temp dir and compares **parsed documents** (key order and whitespace are not the claim). It never
writes into the vault.

## Upstream candidate

The generic form — *a phase-gate list should be executable, and should fail on omission rather than
on disagreement alone* — is not Canvas-specific. Every vault that publishes a gate line in `STATE.md`
carries this exposure. See `how/backlog/idea_runnable_gate_manifest.md` §Upstream candidate.
