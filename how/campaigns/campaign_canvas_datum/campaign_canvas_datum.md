---
campaign_id: campaign_canvas_datum
type: campaign
title: "Operation Datum — every hand-maintained registry gets a consumer or a discovery pass, and which one it is goes on the line"
owner: stanley
status: active
estimated_sessions: "1-3"
phase_count: 6
mission_count: "created at phase-open"
priority: medium
executor_tier_default: opus
predecessor: campaign_canvas_gridline
created: 2026-09-13
updated: 2026-09-13
last_edited_by: agent_mondrian
status_history: "active (2026-09-13 — chartered at the plan gate on Gridline AAR §Follow-up's single open item, `idea_reserved_keys_has_no_consumer`; Act 0 discharged the held memo #19 delivery first)"
tags: [campaign, canvas, datum, reserved_keys, registry, no_consumer, derivability, f_gl_1, f_gm_1, canvas_std, discovery_pass]
---

# Campaign: Operation Datum

> A **datum** is a surveyor's fixed mark, and its entire value is that someone returns to it. One that
> nobody returns to is a scratch in a rock — still perfectly precise, still exactly where it was put,
> and carrying no information at all. This vault has spent four weeks discovering that its registries
> are datums of the second kind.

## Why this campaign exists

Gridline's AAR left one open follow-up, and it is the one Gridline deliberately declined to build:

> `idea_reserved_keys_has_no_consumer` — **open**, medium. The durable fix was declined deliberately;
> the cheap half (assert every key the validator dispatches on appears in both lists, derived by
> walking the dispatch sites) is what would have caught `interaction` in June.

The declination was correct at the time — Gridline was executing a ratified LIP table and F-GL-1 was
found *inside* it, so building the fix would have been scope the signature did not authorize. Nothing
about it has aged well, because the finding it rests on is now the **fourth instance in four weeks of
one shape**:

| Instance | The registry | Its blind spot | Found by |
|---|---|---|---|
| `federation_index` | "who holds a wrapper?" | the 10 vaults with **no wrapper at all** | Blueprint P3 |
| the pin field | `version:` in `federation_ref` | canonical already, **no consumer** → six spellings | memo #13, ruled 2026-09-11 |
| memo numbers | *none exists* | the allocation itself | Plumbline P3 |
| `RESERVED_KEYS` | the tuple | **itself** — nothing reads it, so nothing compares it to the validator | Gridline P1 (F-GL-1) |

⇒ ***A specification with no consumer is indistinguishable from no specification.***

And the proof it is not a tidiness note is that the drift had **already happened and nobody could
notice**: `interaction` — shipped and validated by `validate_interaction` since Standard **v2.2.0**
(Armature, 2026-06-23) — was missing from **all three** hand-maintained copies of the `_reserved`
namespace for three months. Not one canvas was ever wrong. The *namespace description* was.

## Definition of done

Every hand-maintained vocabulary registry in `canvas_std` is in exactly one of two states, and **which
one is written on the line**:

1. it has a **consumer** — something that fails when it drifts; or
2. it is covered by a **discovery pass** that enumerates the territory rather than reading the map.

⛔ **A third state is not acceptable and is the thing being removed**: a registry that is correct today,
maintained by hand, and read by nothing.

## What this campaign must not do

| | |
|---|---|
| ⛔ Must not make unknown `_reserved` keys a **rejection** | `$defs.reserved` is open *by design* and spec §7.3 **mandates** preservation of unknown keys. Rejecting them is a **major** bump and breaks the one promise the `_reserved` carrier exists to make. |
| ⛔ Must not check a list against a second hand-written list | That is the failure being fixed, wearing a test's clothes. Every check here **derives by walking** — AST for the dispatch sites, JSON traversal for the schema, enumeration for the population. |
| ⛔ Must not invent a schema twin for a validator-only vocabulary | Several constants have no schema enum **by design**. A missing twin is a fact to state with its reason, not a defect to remedy. |
| ⛔ Must not edit a disagreement into agreement | `gate_manifest.py`'s standing rule: *a disagreement is a finding to investigate, not a number to edit into the manifest.* |

## Phases

| Phase | What | Gate |
|---|---|---|
| **P0** | Baseline **by running it**; correct STATE's two stale live-items; charter | plan gate — HELD, then approved |
| **P1** | Enumerate the registry population **by discovery**, not by listing. Three-way correspondence table (Python constants ↔ schema enums ↔ spec prose) | ⛩ **the firewall ruling for P2 is taken at this exit gate**, informed by P1's measurements |
| **P2** | Give `RESERVED_KEYS` its consumer — AST-walk the dispatch sites. **A named firewall touch.** | human gate |
| **P3** | Vocabulary-agreement sweep across every paired constant/enum; reason-on-the-line for every unpaired one | human gate |
| **P4** | `idea_memo_number_registry` — a registry with a derivation check, **or a reasoned decline** | human gate |
| **P5** | Close — AAR, STATE, gate line pasted from `--markdown` | close gate |

⛩ **Why the firewall ruling moved from P0 to the P1 exit gate.** The approved plan carried a
recommended split (package-internal check inside `canvas_std/tests/`; the spec-prose half in
`how/gates/`). It is deliberately **not** taken as ratified by plan approval: P1 is pure measurement
and touches no firewalled file, so nothing is blocked by waiting, and the signature is strictly better
informed once the correspondence table exists. `adr_007` discipline then applies as at Gridline — the
firewall lifts for **P2 only** and returns to clean on commit.

## P0 baseline — run, not quoted

`python3 how/gates/gate_manifest.py --markdown` from the vault root, 2026-09-13, **exit 0**:

```
`canvas_std` **146/10** · certification **12/12** · `canvas_core` **1040/3** · `canvas_presentation`
**57/2** · `canvas_context` **58** · producers **275 across 7 packages** · `comic_render` **154/2** ·
firewall diff **0** · dual-channel freshness **2/2**
```

Discovery: **14 test-bearing surfaces (physical), all declared** — 12 gated, 2 excluded with reasons,
0 symlink shims skipped.

⚠ **It reproduced STATE's published line exactly, and that is worth recording rather than passing
over.** Gridline scheduled the same run as ceremony and it produced **F-GL-4** in its first minute. The
argument for running a baseline was never that it usually finds something — it is that *you cannot know
which kind of baseline you have until you run it.* This one was quiet. The previous one was not.

⚠ **One self-caught slip in the act of taking the baseline**, recorded not buried: I read the exit code
via `${PIPESTATUS[0]}` after a pipe and got an **empty string**, which I could have glossed as success.
`PIPESTATUS` is a bash array; this shell is zsh (`$pipestatus[1]`). Re-run without the pipe: **exit 0**.
This is precisely the Gridline slip *"a `$?` after a pipe reported the wrong exit code — a status read
from the wrong object"*, recurring five days later in a different shell idiom. ⇒ ***the habit does not
transfer by having written the finding down*** — which is the same argument, one level up, that this
whole campaign makes about registries.

## Findings

Full detail + the derivation record: [`artifacts/p1_registry_correspondence.md`](artifacts/p1_registry_correspondence.md).

⛩ **F-DT-1 · the dispatch detector had two blind spots, and only one can be closed.** The first
version reported **9** dispatched keys; the true static count is **10**. It matched `ast.In` but not
`ast.NotIn`, so it read the first half of `if "authority" in reserved and "production" not in reserved`
and was blind to the second. **Fixed.** The second blind spot is permanent: `_validate_axes` iterates a
literal tuple and then subscripts `reserved[key]` with a **variable**, which no static walk can
resolve. ⇒ ***a detector's population is defined by its own membership rule*** — Blueprint P3's
`federation_index` finding, reproduced **inside the tool written to measure that family**, within an
hour of writing it. Reported as a `dynamic` site count printed beside the key list, so the number is
never read as complete.

⛩ **F-DT-2 · content-pairing reported coincidence as drift, three times out of three.** Unrelated
vocabularies collide on generic tokens (`none`, `text`, `right`) because natural vocabularies reuse
words — `PL_FLOW` vs `toEnd` share `none` and nothing else. Drift has a different shape: a copy sharing
most of its **union**. Floor set at **Jaccard ≥ 0.5**, stated *before* testing and then verified both
ways — coincidence tops out at **0.25**, a one-member perturbation of `VALID_SIDES` scores **0.75**.
⚠ Recorded as an observation about *this corpus*, not a guarantee.

⛩ **F-DT-3 · two constants hold an identical vocabulary and nothing links them.** `BASELINE_TYPES`
(`reserved.py:54`) and `VALID_NODE_TYPES` (`schema.py:18`) are both `{text, file, group, link}`. **Both
correct**, in two modules, with no link — so if the baseline gains a node type, one can move and the
other cannot notice. The campaign's target in its purest form: not a drift, but **the precondition for
one**. ⛔ Not merged and not proposed for merging — whether these are one vocabulary or two that
coincide is a *semantic* question a set comparison cannot answer. **Carried to the P3 gate with the
measurement attached.**

⚠ **F-DT-4 · a verification harness that cannot run its subject still prints a verdict.** Derivation
check D1 was written as `CENSUS="python3 …"` then `$CENSUS`, which in **zsh** does not word-split — the
whole string became one command name and returned **127**. The `||` branch printed *"1 = drift
reported, correct"* beside it. The check tested **nothing** and said it passed. Re-run without the
variable, it passed properly. ⇒ F-P2-11's family (*a check that cannot run is not a check that passes*)
occurring **inside the derivation step whose whole purpose was to prove the tool works**. Sibling of
P0's `${PIPESTATUS[0]}`-in-zsh slip four hours earlier: **two bash-isms in one session, both returning
a falsy value that reads as success.**

⛩ **F-DT-5 · a gate pin that was a claim about the operator's desktop.** `canvas_core` was pinned
`(1040, 3)`. That holds **only while Obsidian is open on this vault** —
`test_live_window_probe_is_title_pinned` passes when `vc.find_window()` resolves and `pytest.skip`s
when it does not. With Obsidian closed, the **same unchanged tree** measures `(1039, 4)` and the
manifest reported DISAGREE: a real disagreement about nothing. ⛔ **Not fixed by re-pinning to
`(1039, 4)`** — that re-pins to the other desktop state and breaks again next time. The invariant that
holds is the **total, 1043 in both regimes**, so `Gate.env_skips` now declares how many skips may vary
with the environment: the total must still match **exactly** and the skip count must stay in
`[expect[1], expect[1]+env_skips]`. Defaults to **0**, so every other gate is exactly as strict as
before — *a test silently becoming a skip is still a regression.* ⚠ **And it means this morning's P0
baseline, reported as "all green, reproduced exactly", was green partly by coincidence of desktop
state**; had Obsidian been closed at 08:00 it would have been a P0 finding. ⇒ ***a pinned
passed/skipped split is a claim about the runner, not about the code*** — sibling of this file's
declared runner-environment preconditions, except those are *declared and checked* and this was
neither.

## P1 result

| | |
|---|---|
| Population | **26** Python vocabulary constants (the charter said 25 — re-derivation caught it) · 14 schema enums |
| **SCHEMA-TWIN** | **12**, all agreeing exactly |
| **VALIDATOR-ONLY** | **14** — the campaign's real surface |
| `_reserved` three-way | **11 = 11 = 11, all three agree** — the Gridline back-fill held, and this is the first time it was *checked* rather than believed |
| `$defs.reserved` open | ✅ §7.3 forward-compat structurally intact |
| Tool | `how/gates/registry_census.py`, exit 0, **no firewall touch** |

## P2 result — the ruling was BOTH legs, and both shipped

Operator ruling at the P1 exit gate (2026-09-13): **gate + package test.**

| | |
|---|---|
| Firewall touch | `what/code/canvas_std/tests/test_registry_consistency.py` (+5) — **the fourth deliberate `canvas_std` touch since Keystone** |
| Gate #10 | `registry_census`, the spec §7.2 leg (a vault artifact the package must not depend on) |
| `canvas_std` | **146 → 151/10**, derived: HEAD 146/10 this morning, working tree 151/10, delta reconciles against the 5 tests exactly; skips unchanged |
| Verified by | **perturbation** — D4 undeclared dispatch key · D5 key dropped from `RESERVED_KEYS` · D6 `$defs.reserved` closed · D7 a new variable-keyed site. Each failed precisely the tests it should; all restored |
| Gate line | **exit 0, ten gates green** |

⭐ **Why the package leg was worth a firewall touch, stated because the cheaper option was genuinely
available**: `registry_census.py` alone would have satisfied this campaign's definition of done *for
this vault*. But **F-GL-1 was a defect in the package**, and `canvas_std` is the released reference
implementation of a public Standard — a fork, or a `pip install adna-canvas-std`, would reproduce it
with nothing to notice. The gate protects Canvas; the test protects everyone downstream.

⚠ **The duplicated AST walk is named at both sites, not left silent.** The package cannot import from
`how/gates/`, so the walk exists twice. Per **F-DT-3**'s own rule — *a duplication is acceptable when
named with its reason and not otherwise* — both files carry the reason. The campaign found that rule
in the morning and had to apply it to itself by the afternoon.

⛩ **F-DT-6 · gate #10 named the wrong fault class, and the finding then lived only in a commit
message.** *(Retro-numbered 2026-09-15. The defect was found, fixed and fully derived at `af741fa`
within the hour of adding the gate — and then **written into no campaign artifact**, so this §Findings
section ended at F-DT-5 while a sixth finding sat in `git log`.)*

The census gate reported *"the `_reserved` namespace copies disagree"* **unconditionally**. So a
drifted schema **twin** — `VALID_SIDES` vs `edge.fromSide`, with the namespace untouched and agreeing
11/11 — was reported as a namespace disagreement, sending the reader to the wrong three files with a
green-looking `11/11` printed beside a `FAIL`. Now derived from the census JSON and split into three
named causes: *namespace disagreement* / *dispatched-but-undeclared* / *vocabulary drifted from its
schema twin*. **Verified by deriving both failure classes separately**, not by reading the code.

⇒ ***the report is part of the check*** — F-GL-7's family for the fifth time, inside the gate this
campaign had just added. And the second half, which is why it is numbered here rather than left in the
log: ⇒ ***a finding whose only home is a commit message is a finding nobody will re-derive*** — the
mechanism of F-GM-1, whose one prior appearance anywhere was also a single commit message
(`53a0213`). Sibling of **F-DT-8** below.

⛩ **F-DT-7 · the JSON Schema's eleven value enums are read by nothing in this vault, and the one
instrument built to watch them goes blind exactly when they drift.** Found by perturbation at P3.1,
where the plan predicted a narrower hole.

Content-pairing (P1) classifies a Python constant `SCHEMA-TWIN` when some schema enum holds the same
set. Drift below the **Jaccard 0.5** floor therefore does not report `DRIFT?` — the pair **dissolves**
and the constant reclassifies to `VALIDATOR-ONLY`, an accepted, unremarkable state. Both directions
measured:

| Perturbation | Census | Gate #10 | Other nine gates |
|---|---|---|---|
| `VALID_SIDES` 4 → 1 member (Python side) | `VALIDATOR-ONLY`, **exit 0** | `ok` | 47 `canvas_std` failures — caught, but *not by the drift detector* |
| `edge.fromSide` + `edge.toSide` enums 4 → 1 (**schema side**) | `VALIDATOR-ONLY`, **exit 0** | `ok` | ⛔ **ALL GREEN** — 151/10 · 12/12 · 1039/4 · 57/2 · 58 · 275/7 pkg · 154/2 · freshness 2/2 |

The schema-side result is the finding. The only red was the **firewall**, which fires on any byte
changing under `canvas_std` — it observed that a file was edited, not that a core vocabulary of a
public Standard had been destroyed, and it is lifted by ruling for every legitimate touch anyway.

⛔ **And the schema is genuinely load-bearing — verified directly rather than assumed.** `jsonschema`
against the gutted schema rejects an ordinary canvas with `'bottom' is not one of ['top']`, while
`canvas_std.validate()` accepts it, because the Python validator reads `VALID_SIDES` and never
consults the schema. Two independent copies of one vocabulary, one consumer each — and **the schema's
consumer is outside this vault**: a fork, a `pip install adna-canvas-std`, an external validator. Every
in-package reader of `json_schema()` reads `$defs.reserved` *only*; the lone exception
(`test_smoke.py:74`) asserts `x-standard-version` and `"node" in $defs` — structure, not values.

⇒ ***content-pairing is coverage that evaporates exactly when it is needed.*** P1 reported *12
SCHEMA-TWIN, all agreeing exactly*, which reads as twelve guarded vocabularies. What it actually
guarantees is that **pairs which still look alike still look alike.** Worse than silence: the census
prints a confident false explanation — *"unrelated vocabularies reusing a generic token"* — said of the
Standard's own `fromSide` enum.

⭐ **This is the campaign's thesis in its strongest form yet, and it was hiding behind a green number.**
`RESERVED_KEYS` was a registry *visibly* read by nothing. These eleven enums were a registry that
**looked** read — by the census, by the twelve-pair table, by a phase result written into this file —
and the appearance was the whole protection.

⛩ **F-DT-8 · the session file is a registry too.** Cold start found
`session_stanley_20260913_datum_p0.md` still `status: active`, still `phase: "Act 0 → P0"`, work log
still reading *"(appended as the session runs)"* — **two days and four commits later**, spanning P0,
P1, P2 and two operator rulings. Nothing was lost, because the commits carry their own derivation
records. But the file that *is* this vault's lease and audit trail recorded none of it, and a peer
checking `how/sessions/active/` for a live lease would have found one claiming to be mid-P0.

It is hand-maintained, it is read by the cold-start ritual and by any peer looking for a lease, and
**nothing fails when it goes stale** — the campaign's forbidden third state, in the campaign's own
session file, found on the day the campaign reached the phase about it. Closed to
`history/2026-09/` with a reconstruction **derived from the commits and labelled as a
reconstruction**, not backfilled as though written live.

⚠ **Deliberately not fixed with a gate here.** A session-freshness check is a real idea and it is
*not* this campaign's surface — Datum's definition of done is scoped to `canvas_std` vocabulary
registries, and widening it at P3 on a fresh finding is the scope creep the charter's own P2 ruling
was careful to avoid. Filed instead; see §Follow-up.
