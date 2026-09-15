---
type: backlog
idea_id: idea_memo_number_registry
title: "Memo numbers are a convention with no registry and no consumer — the third instance of that shape in three weeks"
created: 2026-09-11
updated: 2026-09-15
status: declined
declined: 2026-09-15
declined_by: "Operation Datum P4 — operator ruling at the plan gate: decline, and write the line"
priority: low
owner: mondrian
executor_tier: sonnet
origin: "Operation Plumbline P3 — allocating #17/#18 required grepping prose because nothing records the allocation"
relates: [pin_field_spellings, federation_index, gate_manifest]
tags: [backlog, coordination, memo, registry, derivability, upstream_candidate]
---

# Memo numbers have no registry, and the number line is reconstructible only by grepping prose

> ⛩ **DECLINED 2026-09-15 at the Operation Datum P4 gate — operator ruling, with the reason written
> onto the line instead.** The body below is preserved **unedited**, per the precedent this campaign
> set for [`idea_reserved_keys_has_no_consumer`](idea_reserved_keys_has_no_consumer.md): the expensive
> defects are claims left standing beside their own remedy, so a disposition is recorded by annotation
> and never by rewriting the argument it disposes of.
>
> **Why declined, and it is this file's own case.** §Cost/value says *"**File, do not schedule**"* and
> rates the value *"low and real"*. §Proposed shape names two constraints that break a naive build —
> **#12 is a class, not a file**, and **errata are unnumbered by design**. A check needing two
> carve-outs exactly where its population is irregular is the shape **F-DT-7** measured at P3:
> ⇒ ***a registry that looks watched is better hidden than one that visibly is not.***
>
> ⭐ **And the convention turned out to be self-correcting** — the measurement that settled it, taken
> 2026-09-15 across the same two independent populations this file used:
>
> | Population | 2026-09-11 (when filed) | 2026-09-15 (at the ruling) |
> |---|---|---|
> | `memo_number:` frontmatter | **4** — 10, 11, 15, 16 | **7** — 10, 11, **15 · 16 · 17 · 18 · 19** |
> | prose references | max 16 | max **19** |
> | agree? | ✅ at 16 | ✅ at **19** → next is **#20** |
>
> **The gap is entirely historical (#9–#14). From #15 onward the frontmatter population is complete
> and contiguous** — the practice adopted the key on its own, and a registry would now be enforcing
> something already true.
>
> ⛔ **The decline did not discharge the obligation.** This campaign's definition of done is *consumer
> **or** discovery pass — **and which one it is is written on the line***, and memo numbers had
> **neither, and no line**: `who/coordination/AGENTS.md` mentioned numbering nowhere. The state is now
> written there, with both constraints, the two-population allocation procedure, and an explicit
> ⛔ *do not grep one population and take the max* (the operation that would miss #9 and #13).
>
> ⚠ **Writing that line turned up something larger — F-DT-11.** `who/coordination/AGENTS.md` was still
> **inherited template text** (`agent_init`, 2026-02-19) describing ephemeral `note_YYYYMMDD_*.md`
> files: **0 of 80** files use that naming, and its §Lifecycle instructed *"**Delete** when expired"*
> and *"**No archive**"* — directly contrary to **SO-6**, in the directory holding the delivery record
> the re-probe discipline depends on. Nothing was ever deleted; the practice was right and the
> document was wrong. ⇒ ***a protocol document nobody executes is a registry with no consumer.***
>
> **§Upstream candidate below remains unfiled-upstream** but has now been **mentioned and approved for
> local filing** → [`idea_upstream_registry_derivability.md`](idea_upstream_registry_derivability.md).

## The defect

Canvas numbers its outbound memos (#9 … #18). **Nothing records the allocation.**

Measured 2026-09-11 before allocating this session's two:

- Exactly **4** of ~40 outbound memos carry a `memo_number:` frontmatter key (#10, #11, #15, #16).
- **#9** records its number only in a `status:` comment; **#13** only in its `title:` and `H1`;
  **#12** is not a file at all — it is a *class* (the P3 re-pin wave, 9 copies to 8 recipients);
  **#14** predates the campaign; the two **errata** are unnumbered and attach by `thread:`.
- The ceiling of the authorising manifest was **#14**. #15 and #16 were allocated past it ad hoc,
  with no file recording that it happened.

So "the next memo number" is **derived by grepping prose and taking a max** — which is exactly the
operation that fails silently when a number is recorded somewhere the grep does not reach. This
session cross-checked two independent populations (`memo_number:` fields, and prose references across
`who/`, `how/`, `STATE.md`) precisely because one population could not be trusted. They agreed at 16.

## Why it is worth a line rather than a shrug

This is the **third instance of one shape in three weeks**, and the shape is the campaign's:

| Instance | The registry | Its blind spot |
|---|---|---|
| `federation_index` (Blueprint P3) | "who holds a wrapper?" | the 10 vaults emitting canvases with **no wrapper at all** — invisible by construction |
| the pin field (memo #13 → ruled 2026-09-11) | `version:` in `federation_ref` | **already canonical**, with *no consumer* — so six spellings drifted and nothing noticed |
| **memo numbers** (here) | *none* | the allocation itself |

Rosetta's ruling on the pin field named the generalisation precisely: **the six spellings were not
the absence of a canonical form, they were drift away from one that already exists and that nothing
enforces.** ⇒ ***a specification with no consumer is indistinguishable from no specification.***

## Proposed shape (NOT built — filed deliberately)

`who/coordination/memo_registry.md`, **derived from frontmatter, never hand-maintained**, plus a
`--check` mode that fails on:

- a gap in the number line,
- a duplicate number,
- an outbound memo carrying no `memo_number:` at all.

That is `gate_manifest.py`'s shape — three registries, discovery against the disk, distinct exit
codes — pointed one domain over. ⭐ **And it must enumerate the corpus rather than read a list**, or
it reproduces F-GM-1: *a registry that is only ever read cannot report what was never written into
it.*

⚠ **Two design constraints the measurement already surfaced**, and either would break a naive build:

1. **#12 is a class, not a file.** Any check that demands one file per number goes red on a real,
   correct historical act. Classes need to be first-class in the model.
2. **Errata are unnumbered by design** — they attach to their parent by `thread:`. A check that
   demands a number on every outbound memo would force numbers onto artifacts whose whole identity is
   "this is a correction to #9."

## Cost / value

Small (an afternoon). Value is **low and real**: nothing is currently broken, no memo has been
misnumbered, and the failure mode is a collision or a silent gap that would be cheap to fix and
annoying to notice. **File, do not schedule.**

## Upstream candidate

Probably — any vault numbering outbound correspondence has this exposure, and several do. ⛔ But
`skill_upstream_contribution` says *mention at a natural pause, file only if the operator approves*,
and **this has not been mentioned yet**. Do not file upstream from here.
