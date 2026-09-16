---
type: decision
adr_id: "011"
title: "Legacy canvas-YAML interop reconciled — the `view` authority row, one level too high"
status: proposed
created: 2026-08-24
updated: 2026-09-16
last_edited_by: agent_mondrian
signed_by:
supersedes:
superseded_by:
phase: blueprint-p1
amended: 2026-09-16   # Amendment 1 — Decision 4 struck (false since A-8); migration table gains the `production` row
resolves: "Blueprint P1 charter item — rule the legacy-interop reconciliation (campaign_canvas_blueprint §Phases P1)"
tags: [adr, canvas, standard, legacy, canvas_yaml_interop, authority, production, view, blueprint, diagrammatic_context, amendment_1, a8, v8_11]
---

# ADR-011 — Legacy canvas-YAML interop reconciliation

## Status

**proposed** — authored at the Blueprint P1 doctrine session (`mission_b1_doctrine`, 2026-08-24);
awaiting the §7.7 signature. Canvas rules the *substance* (this is the Canvas Standard's own
authority surface); **propagation into the template channel is Rosetta's** and is offered, not
performed (Rule 10).

### ⛩ Upstream disposition (2026-09-11) — accepted there, still unsigned here

Rosetta (aDNA.aDNA) **ACCEPTED** this reconciliation upstream, operator-ruled 2026-09-11. The
migration is a payload row on the next `skill_template_release` (**v8.11**); ledger at
~~`…/template_release/release_staging_ledger.md`~~ ⛩ **corrected 2026-09-16 →
`…/template_release/release_staging_ledger_v8_11.md`**. The path as written points at a *different,
already-fired* ledger (the hook fold 4.0.1 → 4.3.0) that **contains no canvas row at all** — a reader
following it finds nothing and could reasonably conclude the migration was never staged. ⚠ Caught by
walking it: the wrong file was opened first, found empty of canvas content, and only a second search
turned up the real `_v8_11` ledger. ⇒ ***a pointer that resolves to a real file is not the same as a
pointer that resolves to the right one.***

They verified at the object before accepting rather than taking our memo's word, and returned two
facts we did not have:

1. **`metadata.frontmatter` is already present and empty (`{}`)** in all four files — so the
   migration writes into a carrier that exists rather than creating one. It is marginally cheaper
   than Decision 2's mapping table implies, and it explains the failure mode exactly: `canvas_std`
   resolves `metadata.frontmatter._reserved`, finds an **empty object rather than a missing path**,
   and reports `core` with nothing to complain about.
2. **Our md5 reproduced byte-exactly, seventeen days on** — `template_architecture.canvas` →
   `f9459bc3cbb21391fe28dd76d3e44902` in **both** `.adna/` and `Canvas.aDNA/`, all four files
   byte-identical across the two trees. The *"one edit, not forty-six"* claim holds.

⛔ **It is not hand-edited into `.adna/`, and they say it will not be** — Standing Rule 1, plus a
fresher reason worth recording because it is a general one: **v8.10 folded one way only.** Its
payload rows read *"authored here → `.adna/…`"*, so the fix landed in the artifact and **never in the
dev graph — the source of record every future fold reads.** A release that folds one way is a
re-introduction channel. `skill_template_release` now carries a hard back-write step (b.2).

⚠ **Upstream acceptance is NOT this ADR's §7.7 ratification.** Decision 5 said propagation is
*offered, not performed*; **that half is now discharged by them**. The Canvas-side signature below is
still pending and is the operator's alone.

### ⛩ AMENDMENT 1, 2026-09-16 — ⛔ this ADR was **not signable as it stood**, and the reason shipped upstream

Re-derived at the object while preparing this ADR for ratification. **Two defects**, and the second
has already been acted on by a peer in good faith.

**(1) Decision 4 was false, and had been for five days when the release fired.** It asserts
*"`canvas_std` does **not** know the key… an invented or misspelled value is accepted silently…
[LIP-0010] is assessed, **not** taken."* **Operation Gridline shipped A-8 on 2026-09-11**: `canvas_std`
**validates** `authority` and `production`, and **LIP-0010 is `Final`**, not assessed. Struck below,
with the matching §Consequences bullet.

⚠ **The block immediately above this one already knew.** It was added 2026-09-11 and cites the axis
split, the `view` row surviving it, and *"LIP-0010 as the durable fix"* — while Decision 4, four
screens down, still said the LIP was untaken. ⇒ ***corrected in one place and not the other*** — the
`F-DT-9` family (*a claim left standing beside its own remedy*), inside the ADR whose own §Decision 4
is the claim.

**(2) ⛔ The §Verified migration table is now INCOMPLETE, and following it to completion produces a
NONCONFORMANT canvas.** Its `authority: "view"` row reads *"no validated home (Decision 4) — keep
additive"* and **never mentions `production`**. Under A-8 the rule is **asymmetric**: `authority`
**requires** `production`; `production` alone is legal. Measured:

```
{authority: "view"}                         -> A-8: 'authority' is present without 'production'
{authority: "view", production: <value>}    -> OK
{production: <value>}                       -> OK
```

The table was verified against **v2.3.0** and carried into **v2.4.0** unchanged. ⇒ ***a recipe is a
measurement with an expiry date, and this one was handed to another vault.*** See §What v8.11 actually
shipped.

⛔ **No `canvas_std` change.** This amendment corrects a **description**, not the validator. A-8's
behaviour is untouched and the firewall stays at diff 0.

⭐ **And the axis split does not invalidate this ADR — checked, not assumed.** The 2026-09-11 ruling
removed `generator` from the `authority` axis, which could have unseated Decision 1's `view` row and
with it a 200-file migration. It does not: `view` answers *who owns the meaning*, which is precisely
the question `authority` keeps. The value survives the split unchanged, and ~~**Decision 4**
(*"doctrine-enforced, not machine-enforced — for now"*) now has a named upstream concurrence, with
`production` as its sibling and LIP-0010 as the durable fix.~~ ⛩ **This closing clause is superseded by
Amendment 1 and is struck 2026-09-16** — it describes Decision 4 as *standing with concurrence*, which
was true for the ~14 hours between this block being written and A-8 shipping the same day. The
"durable fix" **landed**: `production` is not a *sibling awaiting* a LIP, it is a validated key and
LIP-0010 is `Final`. ⚠ **The paragraph's first two sentences are unaffected and still correct** — the
`view` row survived the axis split, which is what this block was written to check.

## Context

The 2026-02 `canvas_yaml_interop.md` spec defines a bidirectional `.lattice.yaml` ↔ `.canvas`
mapping. It predates the aDNA Canvas Standard, and the two have never been formally reconciled.
Operation Blueprint's P0 draft characterized the corpus it ships as **bare JSON Canvas** — no
`_reserved` block, invisible to tooling — and asked Rosetta to reconcile two incompatible systems.

**Measurement (2026-08-24) contradicts that diagnosis.** The count was right; the cause was not.

### Measured ground truth

| Object | Measured |
|---|---|
| Template example canvases | **196** real files across **46** live vaults (+**74** archived in `Archive.aDNA`, SO-7 retained) |
| Carrying a `_reserved` block | **196 / 196** — none are bare |
| Block contents | `{authority: "view", source_yaml, last_sync, sync_hash}` |
| Block **location** | `metadata._reserved` |
| Standard's canonical location | `metadata.frontmatter._reserved` (`what/docs/canvas_producer_quickstart.md:46`; named in A-2's own error text) |
| `canvas-std validate` | `declared=core  level_reached=extended  **[OK]**` |
| `canvas-std validate --level adna_native` | `[FAIL]` on **A-2 alone** |
| Interop **spec** copies | 69 total (50 live); 3 md5 variants differing only in the `last_edited_by` frontmatter line (one archived copy also has a stale `source_instance`) — **bodies uniform** |
| Template canvases across vaults | byte-identical (`template_architecture.canvas` → `md5 f9459bc3cbb21391fe28dd76d3e44902` in `.adna`, `Canvas.aDNA`, `Obsidian.aDNA`) |

The legacy has been emitting the `view` authority quartet since 2026-02 — to a path `canvas_std`
does not read. The block is **present and unread**, which is why it reports a green `[OK]` at `core`
while carrying semantics nobody validates.

## Decision

**The `canvas_yaml_interop` shape *is* the aDNA Canvas Standard's `view` authority row — named and
bounded under the Standard, not deprecated and not a competing system. Its defect is placement and
field shape, not design.**

1. **The legacy is ratified as a mode, not retired.** A `.canvas` that is a derived visualization of
   an authoritative non-canvas source (`.lattice.yaml`) is a **`view`-authority** canvas. Edits to it
   are view edits until reconciled through the Round-Trip Protocol. The interop spec keeps its
   mapping tables and color conventions; it defers to the Standard for **schema** and to
   `pattern_diagrammatic_context` for **authority semantics**.
2. **Canonical placement is `metadata.frontmatter._reserved`.** A `_reserved` block anywhere else is
   nonconformant — and specifically *worse* than absence, because it hides behind a green `core`
   validation. This is added to the pattern's anti-pattern list.
3. **The migration is mechanical, lossless in topology, and verified** (§Verified migration below).
   No node, edge, group, position, or color changes. Baseline-Obsidian degradation (D-1/D-2/D-3) is
   preserved.
4. ~~**`authority` is doctrine-enforced, not machine-enforced — for now.** `canvas_std` does **not**
   know the key; it passes as an additive `_reserved` extension, so an invented or misspelled value
   is accepted silently. Closing that gap would be a schema change and therefore a LIP. It is
   assessed, **not** taken, in `lip_0010_assessment_diagrammatic_context.md`.~~
   ⛩ **STRUCK 2026-09-16 (Amendment 1) — true when written 2026-08-24, false since 2026-09-11.**
   Preserved because its history is the argument: the gap it describes was real, it took a peer
   ruling plus a §7.7 signature to close, and **this sentence outlived the fix by five days inside
   the document that named it.** Replacement:

   **4. `authority` and `production` are MACHINE-enforced as A-8, since Standard v2.4.0.**
   `canvas_std` validates both — closed value sets (`{dual_channel, view}` · `{hand_authored,
   generated}`), both **optional**, validated only if present, with one **asymmetric** cross-key rule:
   `authority` **requires** `production`; `production` alone is legal. A misspelled value is now
   **rejected**, not accepted silently. `LIP-0010` is **Final**, not assessed. ⭐ `view` **survived the
   axis split unchanged** — it answers *who owns the meaning*, which is exactly the question
   `authority` kept. **This ADR still changes no code**: `what/code/canvas_std/` stays at diff-0, and
   A-8 was shipped by Gridline, not by this ratification.
5. **Propagation is offered, not performed.** One `.adna` edit plus a `skill_template_release`
   reaches all 46 vaults, because the files are byte-identical. Canvas supplies the verified recipe;
   Rosetta owns the template channel and the release.

## Verified migration

Executed on scratch copies of all four template canvases, then validated:

> ⛩ **AMENDED 2026-09-16.** The table was verified against **v2.3.0**. Two rows are now wrong and one
> row is **missing**; the v2.3.0 forms are struck rather than deleted, because this exact table was
> handed to another vault and partially executed (§What v8.11 actually shipped).

| Legacy `metadata._reserved` | Standard `metadata.frontmatter._reserved` |
|---|---|
| — | ~~`adna_version: "2.3.0"`~~ → **`adna_version: "2.4.0"`** for any migration performed now *(A-2)*. 2.3.0 remains a real released version and is not *invalid* — but a migration run today should declare the Standard it was verified against. |
| — | `conformance_level: "adna_native"` *(A-2)* |
| `sync_hash: "sha256:none"` | `sync.sync_hash: "<16 hex>"` — **nested and recomputed** via `compute_sync_hash()` (SHA-256 over sorted node ids + `from->to` pairs, truncated to 16). A-6 rejects the `sha256:`-prefixed form; it is not transliterable. |
| `source_yaml: ""` | `sync.source_name` — renamed; empty in 3 of 4, so a real value must be supplied |
| `last_sync` | no validated home — keep additive or drop |
| `authority: "view"` | ~~no validated home (Decision 4) — keep additive~~ → **`authority: "view"` is now VALIDATED (A-8)** and its value is unchanged and correct. ⛔ **But it may not travel alone.** |
| — | ⛔ **`production: "generated"` — NEW, REQUIRED ROW.** A-8 is asymmetric: `authority` **requires** `production`. A migrated canvas carrying `authority` and no `production` **fails A-8**. `generated` is the right value here by the pattern's own definition — a `.canvas` derived from an authoritative `.lattice.yaml` is machine-made, and `generated` is what carries *"never hand-edit; regenerate"*. ⚠ **This row did not exist when the recipe was verified, and its absence is the defect Amendment 1 exists to fix.** |

```
$ canvas-std validate <migrated>/template_architecture.canvas --level adna_native
canvas-std 2.3.0: …/template_architecture.canvas
  declared=adna_native  level_reached=adna_native  [OK]
  degradation: {'D-1': True, 'D-2': True, 'D-3': True}
```

4 / 4 migrated files reach `adna_native [OK]` with degradation intact.

**Sync fields were never populated:** `sync_hash` is `"sha256:none"` ×3 / `"sha256:pending"` ×1 and
`source_yaml` is empty in three. The `view` contract has been *declared* for 6 months without ever
being *enforced* — the migration is the first time these files carry a real topology hash.

## ⛩ What v8.11 actually shipped (measured 2026-09-16, at the object)

Rosetta **fired template release v8.11 on 2026-09-11** with *"the ADR-011 canvas migration"* as payload
row **P3** (their ledger: `release_staging_ledger_v8_11.md`, `status: accepted`, **RATIFIED AND FIRED**).
⚠ **What shipped is the relocation half only** — not the field-shape half this ADR's table specifies.
Read directly from `.adna/what/lattices/examples/template_architecture.canvas`:

```json
"_reserved": { "authority": "view", "source_yaml": "",
               "last_sync": "2026-03-02T00:00:00Z", "sync_hash": "sha256:none" }
```
```
top-level metadata._reserved removed?  yes  (the relocation worked — the block is on the canonical path)
validate(core)                         OK
validate(adna_native)                  A-2 ×2 (no adna_version · no conformance_level)
                                       A-6   (_reserved.sync missing)
                                       A-8   ('authority' present without 'production')
```

⚠ **§Verified migration's *"4/4 migrated files reach `adna_native` [OK]`"* describes the FULL recipe,
executed here on scratch copies. It does not describe what is in `.adna/` today.** Both statements are
true of different objects, and the ADR did not distinguish them — *state the population on the face of
the number*.

### What is and is not at risk — stated plainly, because the alarming reading is available and wrong

| | |
|---|---|
| ✅ **Nothing is broken today.** | The shipped files declare **no `conformance_level`**, so they validate at `core` and **pass**. A-8 only fires when a document is validated at `adna_native`. |
| ✅ **The fleet was not touched.** | Rosetta scoped P3 explicitly: *"8 files, ours and the image's. **NOT the fleet.**"* The ~200 canvases across ~47 forked vaults are untouched, exactly as Decision 5 intended. |
| ⛔ **The trap is for whoever finishes the job.** | Completing the field-shape half from this ADR's table clears A-2 ×2 and A-6 — and **then trips A-8**, because the table never said to add `production`. The remedy is Amendment 1's new table row. |
| ⚠ **This is not Rosetta's error.** | They verified at the object before accepting, returned two facts we did not have, and scoped the release narrowly. They executed a correct relocation against a recipe that was accurate when offered. **The stale recipe is ours.** |

⇒ **Owed to them: an erratum**, carried on memo **#20** with `ack_required: true`. Repairing the 8
shipped files is **theirs to decide** once they hold it — they pass at their declared level, and this
vault does not write into `.adna/` (Standing Rule 1) or their tree (Rule 10).

## Consequences

**Accepted:**
- Until the template release lands, 196 files remain `core`-valid and `adna_native`-invalid. This is
  a *known* state now rather than an unmeasured one, and nothing depends on them validating higher.
- ~~`authority` remains unvalidated free text (Decision 4). A vault can write `authority: "veiw"` and
  no tool objects. Doctrine catches it at gate review; machines do not. Recorded, not hidden.~~
  ⛩ **STRUCK 2026-09-16 (Amendment 1) — false since 2026-09-11.** `authority: "veiw"` is now **rejected**
  by A-8, at `adna_native`. The replacement consequence is the opposite in direction and smaller in size:
  **a canvas carrying `authority` without `production` is now nonconformant**, which is a new obligation
  on the migration recipe rather than a gap in it. *(This bullet and Decision 4 were one claim written
  twice; both are struck in the same pass so neither can be "verified" by reference to the other —
  F-PL-3's lesson, where two stale figures agreed with each other and with nothing else.)*
- Canvas cannot land the fix — it depends on Rosetta's template release. This ADR converts a
  6-month-old unowned drift into a named, recipe-complete offer.

**Reversibility:** high. The migration is additive plus a relocation; the legacy shape can be
restored from any file's own contents, and the topology hash is recomputable at will.

## Alternatives considered

- **Deprecate the interop spec and regenerate all 196 from source.** Rejected — throws away a
  working mapping and 196 hand-checked files to fix a path bug, and there is no `.lattice.yaml`
  source for three of the four templates (`source_yaml` is empty).
- **Teach `canvas_std` to read `metadata._reserved` as a fallback.** Rejected — a firewall change
  (LIP territory) that would legitimize two canonical paths forever and weaken A-2 for every future
  document to rescue four template files.
- **Leave it; the files validate green at `core`.** Rejected — they carry unread authority
  semantics, so every reader must guess whether editing them means anything. That is precisely the
  "undeclared authority" anti-pattern the doctrine names.

## Ratification (§7.7)

| Field | Value |
|-------|-------|
| Decision | `canvas_yaml_interop` = the Standard's `view` authority row · canonical placement is `metadata.frontmatter._reserved` · migration verified, offered to Rosetta, not performed · `authority` stays doctrine-enforced pending LIP-0010 · no `canvas_std` change |
| Ratified by | _(pending)_ |
| Date | _(pending)_ |
| Status | **proposed** |
