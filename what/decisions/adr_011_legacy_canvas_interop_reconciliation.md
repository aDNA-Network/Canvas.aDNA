---
type: decision
adr_id: "011"
title: "Legacy canvas-YAML interop reconciled — the `view` authority row, one level too high and stamped on three files for every one it fits"
status: proposed
created: 2026-08-24
updated: 2026-09-16
last_edited_by: agent_mondrian
signed_by:
supersedes:
superseded_by:
phase: blueprint-p1
amended: 2026-09-16   # A1 — Decision 4 struck (false since A-8) · A2 — corpus PARTITIONED (A1's blanket `production` row was wrong for 194 of 258) · A3 — the `source_yaml` trap closed, evidence re-verified under the partitioned recipe, title corrected
resolves: "Blueprint P1 charter item — rule the legacy-interop reconciliation (campaign_canvas_blueprint §Phases P1)"
tags: [adr, canvas, standard, legacy, canvas_yaml_interop, authority, production, view, blueprint, diagrammatic_context, amendment_1, amendment_2, amendment_3, a8, v8_11, partition, plumbline_p1, signability]
---

# ADR-011 — Legacy canvas-YAML interop reconciliation

## Status

**proposed** — authored at the Blueprint P1 doctrine session (`mission_b1_doctrine`, 2026-08-24);
awaiting the §7.7 signature. Canvas rules the *substance* (this is the Canvas Standard's own
authority surface); **propagation into the template channel is Rosetta's** and is offered, not
performed (Rule 10).

---

## What this ADR says today

> ⚠ **A summary of the Decisions below — not a replacement for them.** Added at Amendment 3 because
> the operative content had become distributed across an August body plus two September amendment
> blocks, so ratifying it meant reconstructing it from what was struck. ⛔ **The Decisions remain the
> authority.** If this block and a Decision ever disagree, the Decision wins and this block is the
> defect. *(It is deliberately not a fourth independent statement of the substance — a fourth
> independent statement is how this ADR reached three amendments.)*

**The legacy `canvas_yaml_interop` shape is not a competing system.** For the canvases it actually
describes, it **is** the Standard's `view` authority row — written to the wrong path, and stamped on
far more files than it fits.

**1 · Placement.** Canonical is `metadata.frontmatter._reserved`. A `_reserved` block anywhere else is
nonconformant and specifically *worse than absent*, because it hides behind a green `core` result.

**2 · The migration is not one recipe. Partition first:**

> A canvas is **derived** iff `_reserved.source_yaml` is non-empty **and** the referenced file resolves
> relative to the canvas. Otherwise it is **primary**.
> ⛔ A declared source that does not resolve is **not** evidence of derivation — it is evidence of a
> stamp. And **never invent one to fill the field**: `source_name` is an *input to this test*, so a
> fabricated value reclassifies the canvas instead of documenting it.

| | **Derived** *(63 of 258 measured)* | **Primary** *(194 of 258)* |
|---|---|---|
| `sync.source_name` | the real, resolving source | ⛔ omit |
| `authority` | `"view"` | ⛔ omit |
| `production` | `"generated"` | ⛔ omit |

Both populations reach **`adna_native [OK]`** with degradation intact — re-verified 2026-09-16 under
this recipe, not the superseded one (§Re-verified below).

**3 · `authority` and `production` are machine-enforced** as **A-8** since Standard **v2.4.0**, both
optional, with one asymmetric rule: `authority` **requires** `production`; `production` alone is legal.

**4 · Propagation is offered, never performed.** Canvas supplies the verified recipe; Rosetta owns the
template channel.

### ⛔ What this ADR does NOT claim

| | |
|---|---|
| **No `canvas_std` change** | A-8 was shipped by Operation Gridline, not by this ratification. The firewall stays at diff 0. |
| **No fleet migration by us** | The 194 primary canvases across 63 vaults are not ours to edit. |
| **No repair of the 8 files v8.11 already shipped** | They pass at their declared level (`core`); repairing them is Rosetta's call once they hold the erratum. |
| **No enforcement of the partition in code** | The test is derivable and stated; nothing validates that a `view` canvas really has a resolving source. |

---

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

### ⛩ AMENDMENT 2, 2026-09-16 — ⛔ **Amendment 1's new row is wrong for the MAJORITY of the corpus**

Found by red-teaming Amendment 1 rather than by any new external input. **The corpus is two
populations, and neither this ADR nor Amendment 1 partitioned it.**

| Population | Test | Correct declaration |
|---|---|---|
| **Derived** — `hello_world.canvas` | `source_yaml: "hello_world.lattice.yaml"` **and the file resolves** | `authority: view` + `production: generated` ✅ Amendment 1's row is right *here* |
| **Primary** — `template_agent_graph` · `template_architecture` · `template_pipeline` | `source_yaml: ""`, and ⚠ **no `template_*.lattice.yaml` exists anywhere in the workspace** — the negative was verified with `find`, not assumed | ⛔ **omit BOTH keys** |

**Measured 2026-09-16** — glob `~/aDNA/*/what/lattices/examples/*.canvas`, `Archive.aDNA` excluded,
live vaults, this node *(stated on the face of the number, since it is a different glob from
§Measured ground truth's 196/46 and the two are not interchangeable)*:

```
258 canvases across 63 vaults
  194  sourceless                 -> PRIMARY   -> omit both keys
   63  sourced + source RESOLVES  -> derived   -> view + generated
    1  no _reserved block
```

Uniform per vault: **one `hello_world.canvas` plus three `template_*`.** ⇒ **≈3 : 1 against the recipe
as written** — Amendment 1 would have stamped `production: generated` onto 194 files generated from
nothing, on top of an `authority: view` that is not true of them either.

⛔ **And `view` is WRONG on the 194, not merely incomplete.** The **Plumbline P1 ruling** already
settled this population: *"A standalone hand-authored canvas that **is** the primary artifact is not
diagrammatic context at all"* — the axis does not apply and **omission is the correct answer**.
`view` asserts *another channel owns the meaning*; for these there is no other channel.

**Provenance, stated fairly rather than as a single culprit:** the 2026-02 legacy tooling stamped
`authority: "view"` on everything it emitted, sourced or not. This ADR inherited that as ground truth
— and ⚠ **it saw the symptom and misread it**: §Verified migration reports *"sync fields were never
populated… the `view` contract has been declared for 6 months without ever being enforced."*
⇒ ***it read "unpopulated" where the truth was "these are not views."*** Rosetta verified **placement
and byte-identity**, which is exactly what we asked of them — not semantics, and not their miss.
Amendment 1 then added `production` on top.

⭐ **The `production` row was the single most confident claim in the whole package** — offered as
*"right by the pattern's own definition"* — and it is the one that was wrong. ⇒ ***confidence was
doing the work a partition should have done.***

#### The partition test, executable rather than described

> A canvas is **derived** iff `_reserved.source_yaml` is non-empty **and** the referenced file
> resolves relative to the canvas. Otherwise it is **primary**.
>
> ⛔ A declared source that does **not** resolve is **not** evidence of derivation — it is evidence of
> a stamp. Treat it as primary.

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

   ⛩ **Corollary added at Amendment 2, 2026-09-16 — the sentence above is CORRECT AS WRITTEN and is
   the test the corpus fails.** It defines a `view` canvas by **derivation from an authoritative
   source**. It never said what to do when the source is *declared but absent*, and the legacy
   tooling stamped `authority: "view"` regardless — so this ADR read the stamp as the fact.

   > **A canvas whose declared source does not resolve is not a derived visualization, and must not
   > be stamped as one.** Sourceless ⇒ **primary artifact** ⇒ the authority axis does not apply
   > (Plumbline P1) ⇒ **omit both keys**.

   ⇒ ***the presence of a field is not evidence of the fact it asserts*** — 194 of 258 measured
   canvases declare an owner that does not exist.
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

~~Executed on scratch copies of all four template canvases, then validated:~~ ⛩ **Amendment 3:** that
2026-08-24 run applied **one recipe to all four**, which is the error this ADR took three amendments
to find. The current evidence is **§Re-verified under the PARTITIONED recipe** below — one canvas from
**each** population. The v2.3.0 material is retained, struck, because the mapping rows it establishes
(placement · `sync_hash` recomputation · A-6's rejection of the `sha256:` form) are **still correct
and still the recipe**; only the population handling was wrong.

> ⛩ **AMENDED 2026-09-16.** The table was verified against **v2.3.0**. Two rows are now wrong and one
> row is **missing**; the v2.3.0 forms are struck rather than deleted, because this exact table was
> handed to another vault and partially executed (§What v8.11 actually shipped).

| Legacy `metadata._reserved` | Standard `metadata.frontmatter._reserved` |
|---|---|
| — | ~~`adna_version: "2.3.0"`~~ → **`adna_version: "2.4.0"`** for any migration performed now *(A-2)*. 2.3.0 remains a real released version and is not *invalid* — but a migration run today should declare the Standard it was verified against. |
| — | `conformance_level: "adna_native"` *(A-2)* |
| `sync_hash: "sha256:none"` | `sync.sync_hash: "<16 hex>"` — **nested and recomputed** via `compute_sync_hash()` (SHA-256 over sorted node ids + `from->to` pairs, truncated to 16). A-6 rejects the `sha256:`-prefixed form; it is not transliterable. |
| `source_yaml: ""` | ⛩ **SPLIT BY POPULATION at Amendment 3 — see below.** ~~`sync.source_name` — renamed; empty in 3 of 4, so **a real value must be supplied**~~ ⛔ **STRUCK: this instruction was an active trap.** The three it refers to are **primary artifacts with no source**. Supplying a value would not merely be cosmetic — `source_name` **is an input to the partition test**, so an invented one *resolves nothing but changes the test's answer*, silently reclassifying a primary canvas as derived. ⚠ **Self-concealing, and therefore worse than an empty field**: the empty field is the evidence. This is the *"passing a value to make a number go green"* habit `conform.py` names — declined one table-row below by Amendment 2, and left standing here until now. |
| `last_sync` | no validated home — keep additive or drop |
| `authority: "view"` | ⛩ **SPLIT BY POPULATION at Amendment 2 — see the two rows below.** ~~no validated home (Decision 4) — keep additive~~ (v2.3.0 form) and ~~*"now VALIDATED (A-8), its value unchanged and correct"*~~ (Amendment 1's form) are **both struck**: the first because A-8 ships, the second because it is true of **63** files and false of **194**. |

**⇒ The migration is not one recipe. Apply the partition test first, then the matching row:**

| Population | `sync.source_name` | `authority` | `production` |
|---|---|---|---|
| **Derived** — `source_yaml` non-empty **and** it resolves *(63 of 258 measured)* | the **real, resolving** source, carried over | `"view"` — unchanged and **correct**; it survived the axis split, and another channel really does own the meaning | **`"generated"`** — required by A-8's asymmetry, and right by the pattern's definition: a `.canvas` built from an authoritative `.lattice.yaml` is machine-made, and `generated` is what carries *"never hand-edit; regenerate"* |
| **Primary** — sourceless, or a declared source that does not resolve *(194 of 258 measured)* | ⛔ **OMIT.** There is no source. ⚠ **Never invent one** — `source_name` feeds the partition test, so a fabricated value reclassifies the canvas rather than documenting it | ⛔ **OMIT.** Not "leave additive" — **remove it.** These are standalone hand-authored artifacts; `view` asserts an owner that does not exist. Plumbline P1: *a hand-authored primary artifact "is not diagrammatic context at all"* ⇒ the axis does not apply and **omission is the correct answer** | ⛔ **OMIT.** `production: "hand_authored"` would be *legal* (A-8 permits `production` alone) but it is **not what was ruled** — and inventing a declaration to make a field non-empty is the habit `conform.py` names as *"passing a value to make a number go green."* |

⚠ **Both keys omitted is fully conformant.** A-8 makes each optional; a canvas carrying neither passes
at `adna_native`. Verified, not assumed.

> ⛩ **SUPERSEDED EVIDENCE, 2026-09-16 (Amendment 3).** The v2.3.0 transcript below and its
> *"4 / 4 migrated files reach `adna_native [OK]`"* verified **the unpartitioned recipe** — every file
> given `authority: "view"` and a supplied `source_name`. That is **not the recipe this ADR now
> recommends**, so Decision 3's *"verified"* claim was resting on the wrong transcript. ⛔ **Struck,
> not deleted — and re-run rather than merely withdrawn**, because withdrawing it would have left
> Decision 3 asserting "verified" with nothing behind it.

```
~~$ canvas-std validate <migrated>/template_architecture.canvas --level adna_native~~
~~canvas-std 2.3.0: …/template_architecture.canvas~~
~~  declared=adna_native  level_reached=adna_native  [OK]~~
~~  degradation: {'D-1': True, 'D-2': True, 'D-3': True}~~
~~4 / 4 migrated files reach adna_native [OK] with degradation intact.~~
```

### ✅ Re-verified under the PARTITIONED recipe — 2026-09-16

Executed on **scratch copies** of one canvas from each population (`.adna/` untouched per Standing
Rule 1; Canvas's tracked examples untouched; all three trees confirmed at **0 entries** afterwards).
`sync_hash` **recomputed** via `roundtrip.compute_sync_hash()`, never transliterated — A-6 rejects the
`sha256:`-prefixed form.

| Population | Migrated `metadata.frontmatter._reserved` | Axis keys | Result |
|---|---|---|---|
| **DERIVED** — `hello_world.canvas` | `adna_version: 2.4.0` · `conformance_level: adna_native` · `authority: view` · `production: generated` · `sync{sync_hash: 28cf14bbd135f628, source_name: hello_world.lattice.yaml}` | both | **`adna_native [OK]`** · degradation `D-1/D-2/D-3` all `True` |
| **PRIMARY** — `template_architecture.canvas` | `adna_version: 2.4.0` · `conformance_level: adna_native` · `sync{sync_hash: 85b1fe9224948842}` | **neither** | **`adna_native [OK]`** · degradation `D-1/D-2/D-3` all `True` |

⇒ **The primary form carries no `source_name`, no `authority` and no `production` — and passes.** That
is the claim Amendment 2 asserted; this is the run that proves it. **Decision 3's *"verified"* is true
again, of the recipe actually recommended.**

**Sync fields were never populated:** `sync_hash` is `"sha256:none"` ×3 / `"sha256:pending"` ×1 and
`source_yaml` is empty in three. ~~The `view` contract has been *declared* for 6 months without ever
being *enforced* — the migration is the first time these files carry a real topology hash.~~

⛩ **STRUCK 2026-09-16 (Amendment 3) — this sentence is the misread itself.** The emptiness was not a
maintenance gap; **it was the evidence.** `source_yaml` is empty in three files *because those three
are not views* — there is nothing for them to be a view **of**. Reading it as "declared but not
enforced" is precisely how a stamp got mistaken for a fact, and the sentence survived two amendments
standing two paragraphs below its own correction. ⇒ ***an unpopulated field is data, not debt.***

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

> ⛩ **Amendment 3 supersedes this note and sharpens it.** The `4/4` claim is now **struck entirely**,
> because the distinction was **not two** (recipe vs `.adna/`) but **three**: the full recipe · what
> shipped · **and which population either applies to**. ⭐ Amendment 1 wrote *"state the population on
> the face of the number"* **about a number whose population it had not itself stated** — the four
> files were two populations, and that is what Amendment 2 found. The rule was right; it simply had
> not been applied one level further in. Current evidence: **§Re-verified under the PARTITIONED
> recipe**.

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
