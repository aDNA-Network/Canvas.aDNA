---
type: backlog
idea_id: idea_upstream_registry_derivability
title: "A registry that LOOKS watched is better hidden than one that visibly is not — the derivability discipline, proposed upstream"
created: 2026-09-15
updated: 2026-09-15
status: open
priority: medium
owner: mondrian
executor_tier: opus
origin: "Operation Datum P5 — filed at the operator's approval, per skill_upstream_contribution (mention at a natural pause, file only if approved)"
relates: [idea_reserved_keys_has_no_consumer, idea_memo_number_registry, idea_runnable_gate_manifest, federation_index, gate_manifest]
target_vault: aDNA.aDNA
tags: [backlog, upstream, registry, derivability, no_consumer, discovery_pass, falsifiable_claim, f_dt_7, standard_candidate]
---

# The derivability discipline — proposed for the standard

> ⛔ **Filed locally only.** Nothing has been written into `aDNA.aDNA`; workspace Rule 10 requires
> cross-graph proposals be staged as coordination memos, not silent writes. `skill_upstream_contribution`
> was followed: **mentioned at a natural pause (the Datum P4 gate), approved by the operator, filed
> here.** The memo to Rosetta is the *next* act, not this one.

## The proposition

Every aDNA vault maintains registries by hand — inventories, indexes, key lists, gate lines, wrapper
tables, memo numbers. The standard has nothing to say about them. Three campaigns in this vault have
now converged on a rule that is not Canvas-specific:

> **Every hand-maintained registry must be in exactly one of two states, and which one it is must be
> written on the line:**
>
> 1. it has a **consumer** — something that fails when it drifts; or
> 2. it is covered by a **discovery pass** that enumerates the territory rather than reading the map.
>
> ⛔ **The third state is the defect**: correct today, maintained by hand, and read by nothing.

## Why it is a standard-level rule and not a local tidiness note

The shape has appeared **six times in four weeks, in four different subsystems**, and in every case
the registry was *correct* when written and rotted silently afterwards:

| Instance | The registry | Its blind spot | Found by |
|---|---|---|---|
| `federation_index` | "who holds a wrapper?" | the 10 vaults with **no wrapper at all** — invisible by construction | Blueprint P3 |
| the pin field | `version:` in `federation_ref` | canonical already, **no consumer** → six spellings drifted | memo #13, ruled by Rosetta 2026-09-11 |
| gate line | the suites in `STATE.md` | a suite that **left** it (`canvas_context`), and one that **never arrived** (`canvas_presentation`) | F-P5-3 · F-GM-1 |
| `RESERVED_KEYS` | the `_reserved` namespace | **itself** — nothing read it, so nothing compared it to the validator | Gridline F-GL-1 |
| the **JSON Schema's value enums** | eleven vocabularies | **looked** guarded by a content-pairing census; the guard dissolves under real drift | Datum **F-DT-7** |
| `who/coordination/AGENTS.md` | the coordination protocol | described a practice **0 of 80** files followed, and instructed deletion contrary to SO-6 | Datum **F-DT-11** |

Rosetta's own pin-field ruling stated the generic form first: *the six spellings were not the absence
of a canonical form, they were drift away from one that already exists and that nothing enforces.*

## ⭐ The part that is new, and the reason this is worth filing

The obvious remedy — *write the registry down more carefully* — is the one that fails. Two sharper
findings:

**1. Visibility is not coverage, and false visibility is worse than none.** `RESERVED_KEYS` was
visibly read by nothing, and that visibility is what got it fixed. The JSON Schema's eleven enums had
a census, a twelve-pair correspondence table, and a published phase result all saying they agreed —
and **gutting one of them left all ten gates green**.

> ⇒ ***A registry that LOOKS watched is better hidden than one that visibly is not.***

**2. The remedy is a per-object falsifiable claim, never a second list.** Checking a list against
another hand-written list is the defect wearing a test's clothes. What works is:

- **discovery** — enumerate the territory (walk the AST, the disk, the schema), never read a roster;
- **content-matching, not name-matching** — a name map is itself an unconsumed registry;
- **a declared state on each object, checked against the derivation** — so the claim can be *refuted*.
  In `canvas_std` this is a PEP 258 attribute docstring whose first word is the claimed state; the
  mechanism matters less than the property, which is that a wrong claim **fails**.

⚠ **And publish the blind spot's size next to the number.** Every instrument here has one: a static
walk cannot see dynamic dispatch; content-pairing cannot see total divergence; a fixture corpus
covers **12 of 40** enum values. The remedy is not a cleverer instrument — it is reporting the limit
on the face of the result so the number is never read as complete.

## What a standard touch might look like

⚠ **Deliberately not drafted as a diff.** This vault has learned twice (LIP-0010's deferral; Plumbline
F-PL-1) that proposing a shape before the owning vault has ruled produces a proposal that has to be
unwound. The *finding* is what is offered; the shape is Rosetta's.

Candidate surfaces, in increasing order of commitment:

1. **Doctrine only** — a pattern in `aDNA.aDNA/what/patterns/`, consumed by reference. Cheapest, and
   ⚠ **carries the defect it describes**: a pattern nobody executes is a registry with no consumer.
2. **A compliance dimension** — the 10-dimension object-quality model (CLAUDE.md §Compliance
   Dimensions) has no "derivability" axis. This would give the rule a scorer, i.e. a consumer.
3. **A skill** — `skill_registry_census`, the generic form of `how/gates/registry_census.py`, which a
   vault runs against its own hand-maintained inventories.

⭐ **Option 2 is the one that eats its own dog food** — it is the only one where the proposal is not
itself an instance of the defect.

## Evidence available to the reviewing vault

| | |
|---|---|
| Working implementation | `how/gates/registry_census.py` (discovery + content pairing + named fault classes) · `what/code/canvas_std/tests/test_registry_consistency.py` (the package leg, travels with a fork) |
| The measurement | `how/campaigns/campaign_canvas_datum/artifacts/p1_registry_correspondence.md` · `p3_reason_on_the_line.md` |
| Doctrine | `what/context/context_registry_derivability.md` |
| Prior upstream sibling | `how/backlog/idea_runnable_gate_manifest.md` — same family, narrower scope (executable gate lists) |

## Next act

Stage a memo to **Rosetta (`aDNA.aDNA`)** — the standard's owner, and the vault that ruled the pin
field and supplied the shim finding. ⛔ Per this vault's delivery discipline: re-probe their lease at
act time, and **set `ack_required: true`** — this one asks a question, and our `false` default is now
known to be invisible to their reply-owed sweep. Next free memo number: **#20**.
