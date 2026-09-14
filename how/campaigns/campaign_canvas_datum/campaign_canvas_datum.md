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

*(numbered F-DT-n, appended as they are found)*
