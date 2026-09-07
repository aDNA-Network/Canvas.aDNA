---
mission_id: mission_b2_authoring_rail
type: mission
campaign: campaign_canvas_blueprint
phase: P2
title: "Authoring rail + dogfood — the rail Canvas itself has used"
owner: stanley
persona: mondrian
status: completed
created: 2026-09-04
updated: 2026-09-04
completed: 2026-09-04
completion_note: "complete-with-open-item — b2.4's E2 memo is authored but DELIVERY REFUSED (aDNA.aDNA held a live lease and publishes no drop-box); both dogfood canvases are visual_gate: pending on Amendment 1."
last_edited_by: agent_mondrian
executor_tier: opus
token_budget_estimated: ~120k
session: session_stanley_20260904_blueprint_p2_open_and_the_licensing_act
tags: [mission, blueprint, p2, authoring_rail, dogfood, dual_channel, diagram_generator, skill]
---

# Mission B2 — Authoring rail + dogfood

## Gate

Opened at the operator's P2 gate, 2026-09-04. Scope ruled at that gate: **rail + dogfood**;
conversion-offer memos **#10 (Operations)** and **#11 (ScienceStanley)** deferred to a second P2
session — they are worth more once the rail has been used on real artifacts than as offers made in
advance of one.

## The gap this closes

Canvas.aDNA is the standard-bearer for diagrammatic-context doctrine and ships **zero dual-channel
context canvases of its own.** Verified by enumeration, not memory: every `.canvas` in the tree is a
producer example, a test fixture, or a lattice template. None is a context artifact paired with
prose.

That is the credibility gap. P1 authored the doctrine and staged it to Rosetta; P2 has to be able to
say the vault proposing it practises it.

## Objectives

| # | Objective | Status |
|---|---|---|
| b2.1 | `diagram_generator` — optional `authority` passthrough (producer-side, additive) | ✅ |
| b2.2 | `how/skills/skill_canvas_context_diagram.md` — the authoring rail | ✅ |
| b2.3 | Dogfood: two dual-channel canvases sited beside their prose | ✅ **schema + machine-visual; `visual_gate: pending` on Amendment 1** |
| b2.4 | Erratum **E2** → Rosetta, *if and only if* the build confirms the question is real | ✅ authored; ⛔ **delivery REFUSED** (their live lease, no drop-box) |
| b2.5 | *(unplanned)* `diagram_generator` visual-gate repair — title slot · code-node sizing · group padding · title/rank overlap | ✅ |

### b2.1 — `authority` passthrough

`diagram_generator` emits no `authority` key today. Add it as an optional field on `DiagramInput`,
written through in `consume.py`'s `_reserved` enrichment. Additive, backward-compatible, default off.

- **Firewall**: `what/production/`, not `what/code/canvas_std/`. `git diff --stat -- what/code/canvas_std/`
  MUST be **0** at the gate.
- `model.py` imports no `canvas_std` — `test_model_neutrality.py` AST-guards it. Plain dataclass
  fields only.
- ⚠ `authority` is **doctrine-enforced, not machine-enforced** (F-B1-2: `canvas_std` does not know
  the key; `authority: "veiw"` passes silently). Emitting it is correct *and* currently unvalidated.
  The validated-enum fix is **LIP-0010 Option B, deferred by design** on Rosetta's ruling. Do not
  reach for it here — locked decision R2, no schema change.

### b2.2 — the rail

Authored on the proven shape of `how/skills/skill_canvas_producer_build.md`. It is a **runbook**;
the pattern half is the P1 draft. It wraps the existing engine rather than inventing one.

### b2.3 — dogfood

| Canvas | Prose channel | Why this one |
|---|---|---|
| `what/context/context_canvas_surface_legs.canvas` | `context_canvas_surface_legs.md` | Canvas's central architectural claim — three legs, each with its runtime proof |
| `what/decisions/adr_004_production_code_layout.canvas` | `adr_004_production_code_layout.md` | The two-shelf topology + the `canvas_std` firewall seam — what a newcomer most needs drawn |

Both sit inside `context_canvas_topology_graphs.md` v1.1's **calibrated range** (≲20 nodes), where
crossing-minimisation still holds as the dominant readability lever. Placement over routing.

### b2.4 — erratum E2 (conditional)

The dogfood is expected to force a question the P1 draft does not answer: **a canvas generated from
a YAML spec — `dual_channel` or `generator`?** The draft's axis assumes the canvas faces exactly one
meaning-owner; here there are two artifacts (prose `.md` + spec `.yaml`) and one output.

Working ruling, to be tested against the actual build rather than asserted: the YAML is an
*authoring source*, not a second meaning-owner ⇒ the canvas is `dual_channel` w.r.t. the prose and
records the YAML for regeneration. **File E2 only if the build confirms the question is real.**

⛔ **`b1.5` does not close here.** Memo #9 + erratum v2 are delivered and unanswered, verified at
source — not a delivery defect. The phase does not advance on Rosetta's silence; E2 is an addition
to the same open ask, never a substitute for their ruling.

## Carried, not folded in

- **F-HR-1 `normalize-on-collect`** (an Obsidian re-save can un-conform a canvas — the explicit
  `toEnd` keys are dropped). Carried into P2 by the HR gate close, but it is a `canvas_context`
  *interaction* concern, not an authoring-rail concern. **Still carried**; not addressed by b2.1–b2.4.

## Gates

`canvas-std validate --level adna_native` → `[OK]` (the CLI rejects `adna-native`; fixed at P1) ·
`canvas-visual-check --strict` → `[OK]` · **agent-confirmed render** (Amendment 1) ·
`diagram_generator` suite green · `canvas_std` **115/10** · certification **11/11** · firewall diff **0**.

⚠ **Known gate risk — the agent-confirmed render.** `canvas-std [OK]` is schema, not sight; a
validated canvas has shipped unreadable before (Oration M-R5). No Obsidian vault was found at the
usual paths on this node. The live render is attempted; **if it cannot be driven, the dogfood
canvases are marked `visual_gate: pending` and do NOT claim Amendment-1 clearance.** The machine trap
check is not a substitute and will not be reported as one.

## Findings

- **F-P2-1 (2026-09-04) — Canvas was licensed in fact, in the place that mattered least.**
  `what/code/canvas_std/LICENSE` and `what/code/canvas_context/LICENSE` have been tracked and public
  since **2026-06-13**, byte-identical MIT (`b189a96420df57c630764b57ba7ff2f4`) — **nine days before
  the public flip.** The forge's `license=NULL` was *correct*: it detects on the root, and the root
  was bare. So the **reference implementation** was licensed from the instant it went public, while
  `what/specs/` + `what/docs/` — **the specification documents, the only artifact a third party
  implements *from*** — were not. The peer diagnosis ("nobody is permitted to implement from it")
  was half true, on the worse half. ⇒ Generalisable: `license=NULL` at a forge means *the root is
  bare*, not *the repo is unlicensed*, and those diverge exactly where a repo ships packages.
  Reported to Hopper for their remediation lane.

> ⛩ **CORRECTED 2026-09-07 — F-P2-2's rule survives; its two supporting claims do not. See F-P2-7.**
> The peers' instrument *had* an enumerating column (`b_class`) and they quoted the confirming one —
> so "neither *could* see it" is wrong; "neither *reported* it" is right. And **our own census was a
> literal-census, not a class-census**: a true RFC1918 enumeration at the same baseline reads
> **13 occurrences / 8 files / 4 literals**, against the 10/9/2 reported below.

- **F-P2-2 (2026-09-04) — an external instrument confirms a hypothesis; only an internal one
  enumerates.** Two peers independently measured 2 occurrences of the R&D forge overlay address over
  2 files. An inside census **confirmed their number exactly** *and* found a **second RFC1918 literal
  of the same class at 8 occurrences over 7 files** that neither could see — because a
  `raw.githubusercontent` fetch and an anonymous clone can only confirm a string already held. Had
  the peers' file list been treated as the work order, remediation would have been **4× short while
  reporting completion**, and their instruments would have confirmed us clean. Ruled at
  [[adr_012_publication_boundary_remedy]].

> ⛩ **CORRECTED 2026-09-06 — see F-P2-6. Two claims in F-P2-3 below were wrong and are struck in
> place rather than rewritten.** *"for 13 months"* → the conflict was live **~1 month**
> (`cv_lead_cost_01.py` added **2026-08-03**; `cv_hierarchy_01.py` **2026-06-22**; the two cannot
> conflict before the later of them). The generator's example had been failing **~2.5 months**, not
> 13. *"by anyone"* → **too strong**: comic-profile canvases clear the gate, and always could.
> The `####` measurement and the repair are unaffected.

- **F-P2-3 (2026-09-04) — the visual gate was unsatisfiable, by anyone, for 13 months.** Two shipped
  traps in the same profile contradict: `CV-HIERARCHY-01/title_slot_missing` **requires** a markdown
  heading marker in a group's top 40%; `CV-LEAD-COST-01/heading_lead` **forbids** `h1/h2/h3` leads
  (*"never use `#`/`##`/`###` to title a canvas text node"*). Measured across every lead form:
  `h1/h2/h3` pass hierarchy and trip lead-cost · `**bold**` the reverse · `#####`/`######` pass both
  **only by classifying as `plain`** (a green check for the wrong reason) · **`####` (h4) alone**
  passes both as a real heading, 42.6px vs bold's 40.0px optimum. ⇒ `diagram_generator` now emits
  `#### `. Corroboration it was latent: the generator's **own shipped example** had failed three
  traps since Atelier (2026-06-21) with its Mermaid node at **~14% shown**, and `deck_generator`'s
  example carries 19 findings. The gate is declared mandatory in `skill_canvas_producer_build.md` §6
  and was not being run — the trap corpus grew to 14 while shipped examples were never re-gated.
  ⚠ **Open, not fixed here:** `deck_generator`'s 19 findings (2 HIGH) and any other producer's
  examples. Only `diagram_generator` was repaired. A producer-wide re-gate is a follow-up.
  *(Scope corrected 2026-09-06 → F-P2-6: **5** producers / **6** files, not six producers.)*

- **F-P2-4 (2026-09-04) — a fixed constant cannot satisfy a ratio.** `CV-GROUP-PADDING-01` fires
  when children fill >90% of the container. `PAD = 80` was fixed while content width grows, so the
  trap fires on any diagram past ~1440px — it fired here at 90.36%, i.e. *barely*, which is what made
  it look like a one-off rather than a scaling defect. Fixed by scaling the container to a fill
  target. Generalisable: **a threshold expressed as a ratio needs a fix expressed as a ratio.**

- **F-P2-6 (2026-09-06) — the producer-wide census, measured properly; and two of my own P2 claims
  were wrong.** Re-measuring before recommending a re-gate corrected the mission's own record.

  **(a) I ran the wrong profile.** `traps/cli.py` takes `--profile` (`knowledge-canvas` default ·
  `comic` · `all`). I ran the default against everything. Under its own profile
  `comic_generator`'s example is **0 findings [OK]**, as is the `comic_render` fixture — all 24
  findings including **all 6 CRITICAL** were profile mismatch. **Halftone had already measured and
  dispositioned exactly these**, and the CLI says so in a comment: *"None is a defect. A gate that
  always fails is not a gate."* ⇒ I reported a solved problem as an open one, and did it by
  skipping a flag the tool documents. **The lesson is narrower and more useful than "read the
  docs": a gate result is only meaningful with its profile stated.** A bare "[FAIL]" is not a
  measurement.

  **(b) "13 months" was wrong by ~12×.** Dated from git above. The figure came from the draft
  pattern's own legitimate line — *"Emacs.aDNA — 13 months of the exact pattern"* — read in the
  same document and carried into an unrelated claim. It reached `STATE.md`, the campaign master,
  this mission, the draft's §E2 and the E2 memo, and four of those were pushed. ⚠ **This is the
  precise failure the E2 memo is *about*** — a figure that reads plausibly, survives review, and is
  false. Caught only because the recommendation required re-deriving it.

  **Corrected census** (right profile per domain, `--strict`, 2026-09-06):

  | Producer | Findings | HIGH |
  |---|---|---|
  | `document_generator` (2 examples) | 26 + 26 | 5 + 5 |
  | `deck_generator` | 19 | 2 |
  | `brief_consumer` | 17 | 1 |
  | `post_generator` (2) | 2 + 4 | 0 |
  | `letter_generator` | 5 | 0 |
  | `diagram_generator` · `comic_generator` · `comic_render` | **0 [OK]** | — |

  **6 files · 5 producers · 99 findings · 13 HIGH · 0 CRITICAL** (was reported as "six producers,
  incl. CRITICAL").

  **89 of 99 (90%) are the four classes already solved once here:** `CV-TEXT-BOUNDS-01/overflow` 55 ·
  `CV-LEAD-COST-01/heading_lead` 20 · `CV-GROUP-PADDING-01/aggregate_fill` 10 ·
  `CV-HIERARCHY-01/title_slot_missing` 4. The remaining 10 are **new classes**:
  `CV-GROUP-LABEL-01/label_truncates` (7 HIGH — group labels too long for their width) and
  `CV-FILE-PROPS-01/file_missing` (3 HIGH — shipped examples referencing PNGs that do not exist and
  are **not** gitignored; now that Canvas is MIT and publicly clonable, an external user gets three
  broken examples).

  **(c) A producer MAY depend on `canvas_core`.** `layout.py`'s comment asserted otherwise; the
  vault's own `comic_render/compose.py` does `from canvas_core.print import …`, and `adr_004` sites
  `canvas_core` as the shared **engine shelf**, not a sibling producer. Corrected in place.
  ⇒ The re-gate should be **one shared `canvas_core/layout_fit.py`** over the existing
  `text_metrics` functions the traps themselves call — so producers and traps share one measurement
  and my conservative guesses (`SRC_LINE_H = 44`, mirrored `H4_LEAD_COST`) are replaced by exact
  ones — not five hand-repairs that would produce five slightly different answers.

- **F-P2-7 (2026-09-07) — we charged the peers with a blindness we then committed ourselves, one
  level down.** Hopper's reply corrected F-P2-2's diagnosis and the reconciliation they left to us
  corrected our own numbers.

  **(a) Their instrument was not blind.** `census_public_carriers.sh` greps three predicates —
  `a_host` (a literal), `a_addr` (literal+port) and **`b_class`** (the whole RFC1918 class, lifted
  from the deny pattern). `b_class` *is* the inside-enumeration F-P2-2 claimed only we could do.
  They built it, ran it, and published the confirming column: *"a missing capability is a gap; a
  capability you have and do not read is a habit."*

  **(b) ⛔ And our census was a literal-census wearing an enumeration's name.** We grepped for the
  two strings already found in one file and reported the result as a class measurement. A real
  RFC1918 enumeration at the same baseline (`4acee98`): **13 occurrences / 8 files / 4 literals**,
  against the **10 / 9 / 2** reported. The two missed are a Nebula lighthouse host and a `/24`
  subnet notation — **4 occurrences in `how/skills/skill_l1_upgrade.md`**, which is *live authored
  content*, the category `adr_012` §Decision 3 claimed to have remediated **in full**.

  ⚖ `skill_l1_upgrade.md` is **template-inherited** (2026-03-21; arrived at Canvas genesis
  2026-06-06), so those literals sit in every vault forked from the template. Fixing our copy fixes
  one vault of many — the durable fix is upstream, the same shape as the 196-file legacy in
  `adr_011`. **Left as an open operator item; not remediated unilaterally.**

  **(c) Their `--depth 1` clone means every figure their census has produced describes *tips*,
  never history** — and had never said so. Their correction, not ours, and a larger one than the
  column.

  ⇒ **The rule that survives all of this, sharper than F-P2-2's version and no longer flattering:**
  *an outside measurement validates a hypothesis; an inside measurement that greps for known strings
  is not an enumeration either.* Hopper ratified the same clause from the other direction (ADR-011
  A8 §5 — *a coverage claim states its population, or it is not a coverage claim*), after their own
  instance of it: a `grep -rl … | head` that silently truncated at 10 and reported **9** where the
  population was **22**. **Practice: state the population on the face of the number — tip or
  history · class or literal · tracked or working-tree.**

## AAR

**Worked.** Building the pattern instead of re-reading it. Every one of the four findings came from
the first two real builds — none was visible in eight weeks of authoring, review, and two prior
errata. The dogfood was the instrument.

**Didn't.** The Amendment-1 agent-confirmed render. Two attempts; the second screen-captured a third
party's private messages, because `screencapture` on a desktop app takes the whole screen. Stopped,
deleted the captures, restored the operator's window. The canvases ship `visual_gate: pending` and
the machine check is **not** reported as a substitute. Also: my plan asserted the render gate was
at risk because "no Obsidian vault was found" — that was a bad probe (I checked `~/Obsidian*`; the
vault is this repo). Obsidian was installed and working the whole time; the real blocker was
different and I would not have found it by reasoning.

**Finding.** The two that outlive this mission: *(1)* an external instrument confirms a hypothesis
about your tree, only an internal one enumerates it — two peers agreed exactly on 2 occurrences and
were both structurally blind to 8 more of the same class (F-P2-2); *(2)* a conformance floor nobody
has built against can be unsatisfiable and still read as reasonable to every reviewer, indefinitely
(F-P2-3).

**Change.** `diagram_generator` emits a title slot, sizes its code node to its content, scales group
padding to a fill ratio, and offsets rank 0 below the title. The rail records `####` as doctrine with
the reason, and records that the human visual gate has no safe automated path on a shared workstation.

**Follow-up.** *(a)* Re-gate **5 producers / 6 files** (99 findings, 13 HIGH, 0 CRITICAL — F-P2-6,
corrected 2026-09-06 from "six producers"); do it as **one shared `canvas_core/layout_fit.py`**, not
five hand-repairs, and retrofit `diagram_generator` onto it. *(b)* Port a window-scoped capture
(Home.aDNA `canvas_visual_loop.py`) so Amendment 1 has a safe path. *(c)* Deliver E2 to Rosetta when
their lease clears — **done 2026-09-06, after correcting two overstatements in it**. *(d)* F-HR-1
normalize-on-collect is still carried, untouched. *(e)* Conversion memos #10/#11 — the deferred half
of P2; **sequence them after (a)**, since offering conversions while our own shelf fails the gate
repeats the credibility problem the dogfood just fixed. *(f)* Restore or remove the 3 missing example
PNGs (HIGH, and now publicly clonable).

**AAR addendum (2026-09-06).** The mission's own AAR said *"Worked: building the pattern instead of
re-reading it."* Two days later the same discipline applied to the mission's **output** found two
false claims in it, one pushed publicly. ⇒ The generalisation is stronger than the original: *the
check that catches you is re-deriving a number, not re-reading the sentence containing it.* Both
errors survived my own review, the commit message, and the SITREP.
