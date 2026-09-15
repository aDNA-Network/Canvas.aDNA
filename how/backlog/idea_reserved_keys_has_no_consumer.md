---
type: backlog
idea_id: idea_reserved_keys_has_no_consumer
title: "`RESERVED_KEYS` has no consumer — and three hand-maintained copies of one namespace all missed the same key for three months"
created: 2026-09-11
updated: 2026-09-15
status: closed
closed: 2026-09-15
closed_by: "Operation Datum P2 (86b002b) + P3 (firewall touch #5)"
priority: medium
owner: mondrian
executor_tier: sonnet
origin: "Operation Gridline P1 (F-GL-1) — found while appending two names to the tuple per LIP-0010 Option D item 1; the append was correct and inert"
relates: [idea_memo_number_registry, federation_index, gate_manifest, lip_0010, f_gl_1]
tags: [backlog, canvas_std, reserved_keys, registry, derivability, no_consumer, upstream_candidate]
---

# A registry nothing reads cannot report its own drift

> ✅ **CLOSED 2026-09-15 by Operation Datum.** The body below is preserved unedited as the record of
> what was true on 2026-09-11 — the campaign this idea chartered found, twice, that the expensive
> defects are claims left standing beside their own remedy, so this one is closed by annotation and
> not by rewriting.
>
> **What was built**, and it is more than this file proposed:
>
> | | |
> |---|---|
> | **P2** (`86b002b`, firewall touch #4) | `tests/test_registry_consistency.py` — the "cheaper half" §Proposed shape called for, built exactly as specified: every key the validators dispatch on, **derived by walking the package's AST**, asserted present in `RESERVED_KEYS` *and* in `$defs.reserved.properties`. Plus `test_reserved_object_stays_open`, pinning the §7.3 forward-compat promise this file was careful to protect. |
> | **P1** (`d39f4e2`) | `how/gates/registry_census.py` — the discovery pass, gate **#10**. Enumerates **26** vocabulary constants by AST walk and pairs them to schema enums **by content**, never by a name map. |
> | **P3** (firewall touch #5) | the part this file did not foresee. **F-DT-7**: content-pairing is coverage that *evaporates exactly when it is needed* — a twin drifting past the similarity floor does not report drift, the pair **dissolves** and the constant reclassifies to an accepted state. Gutting the schema's `fromSide`/`toSide` enums left all ten gates green. So every constant now **declares** its relationship to the schema as a falsifiable claim, checked against the derivation. |
>
> ⛔ **The advisory unknown-key report was NOT built**, and that remains correct: `$defs.reserved` is
> open by design, §7.3 mandates preservation, and the reverse direction caught the real defect. The
> §Proposed-shape warning — *"it must not become an error"* — is now enforced by a test.
>
> ⚠ **The `RESERVED_KEYS` block in `reserved.py` still said this idea was open and "deliberately NOT
> built here" two days after P2 built it.** Corrected at P3 as **F-DT-9**, struck rather than deleted.
> ⇒ *a claim left standing beside its own remedy* — this file's own family, found in the comment that
> named it.
>
> **Upstream candidate below is still open**, and unfiled per `skill_upstream_contribution`. It is now
> stronger than when written: the generic form is not merely *"a hand-maintained inventory needs a
> consumer or a discovery pass"* but ***a registry that LOOKS watched is better hidden than one that
> visibly is not*** — and the remedy is a per-object falsifiable claim, not a second list.

## The defect

`canvas_std.reserved.RESERVED_KEYS` — the tuple naming the `_reserved` namespace
(`spec_adna_canvas_standard` §7.2) — was, at 2026-09-11, referenced **nowhere**:

```
grep -rn "RESERVED_KEYS" what/code/canvas_std/src what/code/canvas_std/tests what/production
  -> what/code/canvas_std/src/canvas_std/reserved.py:21:RESERVED_KEYS: tuple[str, ...] = (
```

One hit: its own definition. LIP-0010 Option D item 1 required two names be appended to it, so they
were — **correctly, and inertly.**

## Why it is more than a tidiness note: the drift had already happened

The same namespace is written down **three times, by hand**, and `interaction` — shipped and validated
by `canvas_std.validate_interaction` since Standard **v2.2.0** (Operation Armature, 2026-06-23) — was
in **none** of them until the Gridline P1 back-fill:

| Copy | Read by anything? | Held `interaction`? |
|---|---|---|
| `reserved.py::RESERVED_KEYS` | **no** | ❌ (3 months) |
| `adna_canvas_v2.schema.json` `$defs.reserved.properties` | yes, by `jsonschema` — but the object is **open** (`additionalProperties` unset), so an absent property is not an error | ❌ (3 months) |
| `spec_adna_canvas_standard` §7.2 | humans only | ❌ (3 months) |

**Nothing could notice.** §7.3 *requires* unknown `_reserved` keys be preserved, so an unlisted key is
not a validity fault by design — which is exactly what makes the record rot silently. No canvas was
ever wrong; the *namespace description* was.

> ⇒ ***A specification with no consumer is indistinguishable from no specification.*** Rosetta's pin-field
> ruling stated the generic form; this is that shape found inside the firewall.

## The shape, for the fourth time in four weeks

| Instance | The registry | Its blind spot |
|---|---|---|
| `federation_index` (Blueprint P3) | "who holds a wrapper?" | the 10 vaults with no wrapper at all |
| the pin field (memo #13, ruled 2026-09-11) | `version:` in `federation_ref` | canonical already, **no consumer** → six spellings |
| memo numbers (`idea_memo_number_registry`) | *none* | the allocation itself |
| **`RESERVED_KEYS`** (here) | the tuple | **itself** — nothing reads it, so nothing compares it to the validator |

## Proposed shape (NOT built — declined at the P1 gate, deliberately)

An **advisory** unknown-key report, never a rejection:

- `validate_reserved` (or a sibling `reserved_key_advisory(reserved)`) returns keys present on a
  document but absent from `RESERVED_KEYS` — surfaced through `validate_suite` as advisory, **not** in
  `failed`, **not** affecting `ok`.
- ⛔ **It must not become an error.** `$defs.reserved` is open by design and §7.3 mandates preservation
  of unknown keys; rejecting them would be a **major** bump and would break forward-compat, which is
  the one promise the `_reserved` carrier exists to make.
- The reverse direction is the cheaper half and catches the actual observed defect: a test asserting
  **every key the validator dispatches on appears in `RESERVED_KEYS` and in the schema properties** —
  derived by walking the dispatch sites, not by reading a list. That is what would have caught
  `interaction` in June.

⭐ **And it must enumerate rather than read a list**, or it reproduces the failure it replaces — the
same lesson `gate_manifest.py`'s discovery pass exists for (F-GM-1: a registry that is only ever read
cannot report what was never written into it).

## Upstream candidate

The generic form — *a hand-maintained inventory needs either a consumer or a discovery pass, and
naming which one is part of shipping it* — is a candidate for the standard, alongside the gate-manifest
proposal from 2026-09-10. `skill_upstream_contribution`: **mention at a pause, file only if the
operator approves.** Not filed upstream.
