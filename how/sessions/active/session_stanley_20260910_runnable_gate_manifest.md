---
type: session
session_id: session_stanley_20260910_runnable_gate_manifest
created: 2026-09-10
updated: 2026-09-10
status: active
tier: 2
persona: mondrian
operator: stanley
campaign: none
phase: none
executor_tier: sonnet
last_edited_by: agent_mondrian
tags: [session, canvas, gates, gate_manifest, f_p5_3, regression, canvas_presentation, backlog, upstream_candidate]
---

# Session — the gate set becomes runnable

## Intent

First session after Operation Blueprint closed. **No campaign is active and no successor was
chartered** (operator ruling at the P5 gate), so this session takes a backlog item rather than a
phase: [`idea_runnable_gate_manifest`](../../backlog/idea_runnable_gate_manifest.md), filed at the
P5 close as the durable fix for **F-P5-3**.

The defect: the gate set is a sentence in `STATE.md` that a human retypes each close. `canvas_context`
was in it at Armature, silently fell out, and sat **red for two days across three phase closes** that
each published an all-green gate line — none of them lying. *A skipped test prints `s`; a suite nobody
invoked prints nothing at all.*

The fix must **fail on omission**, not merely on disagreement. Otherwise it is a prettier prose list
with the same failure mode.

Operator rulings taken at the plan gate: build the gate manifest (selected over the `ImagenWiring`
deprecation) · **push the batch first**.

## Cold-start ritual

| Check | Result |
|---|---|
| `how/sessions/active/` | empty — no peer lease |
| `git status --short -uall` | clean, zero entries (the `-uall` rule, binding per the drop-box README) |
| `who/coordination/` | nothing untracked; no new inbound since Vulcan's 09-09 memo (intaken `677b65b`) |
| `git log` HEAD | `22a101b` — the Blueprint close |
| `how/campaigns/` | no active campaign |

## Step 0 — the push (operator GO granted at the plan gate)

⚠ **A figure I published and had not derived.** I reported **20** unpushed commits at the plan gate.
The real count is **22** — my number came off a `head -20` truncation. Caught on the pre-push
re-verify. This is Blueprint's own defining family (*a stated fact nobody re-derived*) committed by
the agent citing it, in the first act after its close, which is worth recording rather than quietly
fixing: **the habit does not transfer by having written the finding down.**

- `git fetch origin` — nothing incoming (`HEAD..@{u}` empty)
- Authorship of all 22: uniform `ScienceStanley <science.stanley@stanley.science>` — no peer work rides along
- `git push origin master` → `57c5a67..22a101b`; **gitleaks clean** across the outgoing range
- Remotes present: `origin` (GitHub) · `mesh` · `mesh-rd`. **`origin` only** was pushed, per plan.

## Step 1 — ground truth, established by running rather than by reading

All seven published gates re-derived before a line of the manifest was written. **Every one
reproduced**, which is the quiet outcome and worth stating:

| Gate | Published | Measured |
|---|---|---|
| `canvas_std` | 115/10 | 115/10 ✓ |
| certification | 11/11 | 11/11 ✓ |
| `canvas_core` | 1035/3 | 1035/3 ✓ |
| `canvas_context` | 58 | 58 ✓ |
| producers | 267 / 7 pkg | 267 / 7 pkg ✓ |
| `comic_render` | 154/2 | 154/2 ✓ |
| firewall | diff 0 | diff 0 ✓ |

### ⛩ F-GM-1 — an eighth suite, never enumerated

`what/production/canvas_presentation/` — **57 passed / 2 skipped**, real library code
(`presentation.py`, `layout.py`, `scoring.py`, `slide_builders.py`, `config_deck.py`), and **absent
from every published `STATE.md` gate line**.

Two measurements settle it:

- `canvas_core` run **alone** returns exactly 1035/3 — the published figure. So `canvas_presentation`
  is **not** hiding inside that run.
- `grep -c canvas_presentation` across the state archives: **0** in `state_archive_20260822.md` and
  **0** in `state_archive_20260909.md`. The two hits in `state_archive_20260803.md` concern the pt09
  relocation, not gating.

**This corrects the premise I planned against.** I assumed it had been gated jointly and dropped out,
citing commit `53a0213`'s `core+pres 916/5`. That commit *is* real and the skip arithmetic reconciles
exactly (core 3 + pres 2 = 5), so that run genuinely included both — **but it was a commit message,
never the STATE gate line**, which tracked `canvas_core` alone throughout (863/3 → 937/3 → 1035/3).

⇒ `canvas_context` **fell out**; `canvas_presentation` **never arrived**. The second is harder,
because there is no absence to notice — and it was **green the whole time**, so the exposure was never
a red suite, only an unwatched one. ***A registry that is only ever read cannot report what was never
written into it.*** Sibling of P3's `federation_index` finding, one layer down.

## Step 2 — the manifest

`how/gates/gate_manifest.py` + `how/gates/AGENTS.md`. Three registries — `GATES` (by name, never
globbed) · `EXCLUSIONS` (non-empty reason **required**, path-existence checked) · **discovery** (walks
the disk; anything in neither registry is a hard failure). Four distinct exit codes.

**A design requirement the backlog idea did not anticipate:** a naive "fail on anything unlisted"
would have been red on day one — `_scaffold` (inert clone template) and `what/production/tests/`
(skip-guarded, F-H6RE-2) are legitimate non-gates. **A check that goes red for good reasons gets
disabled**, so the escape hatch must exist and must justify itself in the same file as the rule.

## Step 3 — verification, by derivation not by reading the message

| Probe | Expected | Got |
|---|---|---|
| green, full run | 0 | **0** |
| throwaway `_probe` package | 3 (omission) | **3**, naming `what/production/_probe` |
| perturbed expectation (58→59) | 2 (disagreement) | **2** |
| broken interpreter path | 4 (precondition) | **4** |
| firewall breached, **run from a deep subdirectory** | 1 | **1** — `2 dirty line(s)`; clean again after restore |

The last row is the cwd-trap regression: the persisted-`cd` failure made this check return empty,
i.e. indistinguishable from clean. The script never `chdir()`s.

## ⚠ Three defects of my own, recorded rather than quietly fixed

1. **I reported 20 unpushed commits; there were 22.** Off a `head -20` truncation, caught on the
   pre-push re-verify. This is Blueprint's defining family — *a stated fact nobody re-derived* —
   committed by the agent citing it, in the first act after its close. **The habit does not transfer
   by having written the finding down.**
2. **The script printed a gated-count as `found − len(EXCLUSIONS)`** → "11 gated, 3 excluded" when the
   truth is 12 and 2 (`what/production/_archive` is declared but holds tests only at grandchild depth,
   so discovery never sees it). A subtraction standing in for a partition. Replaced with the real one.
3. **The generated gate line emitted the producers total in the wrong position**, special-cased off a
   neighbouring gate id rather than off the group's own position. Fixed to emit at first-member.

(2) and (3) are the same error as (1) in miniature — a number produced by a shortcut rather than by
deriving it — inside the very file written to stop that.

## SITREP

**Completed**
- Push batch: **22 commits** → `origin` `57c5a67..22a101b`, gitleaks clean.
- `how/gates/gate_manifest.py` — the gate set, executable; fails on omission.
- `how/gates/AGENTS.md` — contract, rationale, encoded traps, the disagreement rule.
- **F-GM-1** found, measured and dispositioned: `canvas_presentation` is now gate #8.
- `STATE.md` — gate line replaced by a pointer to generated output; banner; F-GM-1 note; tail + Next Steps trued.
- `idea_runnable_gate_manifest` → `status: completed`, with F-GM-1 and the exclusion-registry requirement recorded.

**In progress** — none.

**Next up**
- A **batch GO** for this session's commits (unpushed at close).
- The **upstream candidate**: a gate list that fails on omission is not Canvas-specific. Per
  `skill_upstream_contribution`, mentioned here and at SITREP; **not filed** without operator approval.
- Unchanged watch items: `b1.5`/Rosetta · H4 (ComfyUI M-RD1) · mermaid trust grant · Seshat · Cartographer · SS/M-PL3 · D3 registrar ack.

**Blockers** — none.

**Files touched**
- new: `how/gates/gate_manifest.py` · `how/gates/AGENTS.md` · this session file
- modified: `STATE.md` · `how/backlog/idea_runnable_gate_manifest.md`
- **`canvas_std` untouched** — firewall diff 0, verified from the vault root with an absolute path.

## Next Session Prompt

Canvas.aDNA (Mondrian). No campaign is active — Operation Blueprint closed 2026-09-09 and the operator
chartered no successor. The 2026-09-10 session shipped `how/gates/gate_manifest.py`, which makes the
gate set runnable and **fails on omission** (exit 3); run
`python3 how/gates/gate_manifest.py --markdown` for the current gate line and **paste** it rather than
retyping — that rule is the whole point (`how/gates/AGENTS.md`). It found **F-GM-1** on first run:
`canvas_presentation` (57/2) had never been in any published gate line, and is now gate #8 of 8, all
green. **Two things are owed to the operator**: a batch GO for that session's unpushed commits, and a
decision on filing the **upstream** sibling (a gate list that fails on omission applies to every vault
publishing a gate line in `STATE.md` — `skill_upstream_contribution` forbids filing unprompted). The
remaining self-owned backlog item is the
[`ImagenWiring` deprecation](../../backlog/idea_imagenwiring_selection_surface_deprecation.md): the
measurement is done (10 dead methods, 0 call sites, 3 live ones named) but step 1 is a **fleet consumer
sweep**, since it is a public `canvas_core` export. Everything else in the carried tail is an external
reply or an operator signature — see `STATE.md` §Resume Here.
