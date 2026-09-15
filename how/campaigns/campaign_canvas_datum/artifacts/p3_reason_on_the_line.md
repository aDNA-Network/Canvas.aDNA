---
type: artifact
artifact_id: p3_reason_on_the_line
campaign: campaign_canvas_datum
phase: P3
title: "The reason goes on the line — and the line is a claim the derivation can refute"
created: 2026-09-15
updated: 2026-09-15
status: complete
last_edited_by: agent_mondrian
tools: [how/gates/registry_census.py, what/code/canvas_std/tests/test_registry_consistency.py]
tags: [artifact, datum, p3, registry, reason_on_the_line, schema_twin, attribute_docstring, f_dt_7, f_dt_9, firewall_touch_5]
---

# P3 — the reason on the line, and what looking for it turned up

## The surface P3 was opened for is not the one it found

The charter scoped P3 as *"vocabulary-agreement sweep across every paired constant/enum;
reason-on-the-line for every unpaired one."* The **14 unpaired** constants were the expected work; the
**12 paired** ones were the part already believed safe — P1 had reported them *"all twelve agree
exactly. No drift."*

That sentence was true. It was also the whole protection, and it turned out to be worth less than it
reads.

## ⛩ F-DT-7 — content-pairing is coverage that evaporates exactly when it is needed

Pairing **by content** is this campaign's own load-bearing choice and it remains correct: pairing by
*name* would need a `VALID_SIDES → /$defs/edge/properties/fromSide` table, and that table is itself a
hand-maintained registry with no consumer — the defect, not the fix. But content-pairing has a failure
mode that only appears under real drift. `Pairing.state` returns `SCHEMA-TWIN` on an exact match,
`DRIFT?` on a partial one above the Jaccard floor, and `VALIDATOR-ONLY` otherwise. So a twin that
drifts **past** the floor does not report drift — **the pair dissolves**, and the constant lands in
`VALIDATOR-ONLY`: a normal, accepted, unremarkable state.

Measured both directions, by perturbation rather than by reading:

| Perturbation | Census | Gate #10 | The other nine gates |
|---|---|---|---|
| `VALID_SIDES` 4 → 1 member (**Python** side) | `VALIDATOR-ONLY`, **exit 0** | `ok` | 47 `canvas_std` failures — caught, but **not by the drift detector** |
| `edge.fromSide` + `edge.toSide` enums 4 → 1 (**schema** side) | `VALIDATOR-ONLY`, **exit 0** | `ok` | ⛔ **ALL GREEN** |

The second row is the finding. Full gate set with the Standard's edge-side vocabulary destroyed:
`canvas_std` 151/10 · certification 12/12 · `canvas_core` 1039/4 · `canvas_presentation` 57/2 ·
`canvas_context` 58 · producers 275/7 pkg · `comic_render` 154/2 · registry census `ok` ·
dual-channel freshness 2/2. The **only** red was the **firewall**, which fires on any byte changing
under `canvas_std` — it observed that a file had been edited, not what the edit did, and it is lifted
by operator ruling for every legitimate touch anyway.

### It is not dead data, and that was verified rather than assumed

```
jsonschema against the gutted schema, ordinary canvas:  "'bottom' is not one of ['top']"
canvas_std.validate() on the same document:             accepts it
```

The Python validator reads `VALID_SIDES` and **never consults the schema**. Two independent copies of
one vocabulary, one consumer each — and the schema's consumer is **outside this vault**: a fork, a
`pip install adna-canvas-std`, any external validator of a public Standard. Inside the package, every
reader of `json_schema()` reads `$defs.reserved` *only*; the lone exception (`test_smoke.py:74`)
asserts `x-standard-version` and `"node" in $defs` — structure, not values.

### And it does not fail quietly, which is worse

The census does not go silent when a twin dissolves. It prints an explanation:

```
VALID_SIDES  frozenset  VALIDATOR-ONLY  — (no twin; 3 enum(s) share ['right', 'top'] but fall below
                                           the 0.5 drift floor — unrelated vocabularies reusing a
                                           generic token)
```

*"Unrelated vocabularies reusing a generic token"* — said of the Standard's own `fromSide` enum. The
sentence is generated from a correct derivation and is completely false about this case.

⇒ ***A registry that LOOKS watched is better hidden than one that visibly is not.*** `RESERVED_KEYS`
was a registry *visibly* read by nothing, and that visibility is what got it fixed at P2. These eleven
enums had a table, a phase result, and a green number saying they were covered.

## The fix — a declared state is the memory content-pairing cannot have

Every vocabulary constant now carries a **PEP 258 attribute docstring** whose first word is its state:

```python
VALID_SIDES: frozenset[str] = frozenset({"top", "bottom", "left", "right"})
"""SCHEMA-TWIN — `$defs.edge.properties.fromSide.enum` AND `.toSide.enum` …"""

VALID_COLORS: frozenset[str] = frozenset({"0", "1", "2", "3", "4", "5", "6"})
"""VALIDATOR-ONLY — no schema enum, and a twin would be WRONG: `validate()` also accepts `#`-hex …"""
```

An attribute docstring is real AST structure (`ast.Expr` holding a `str` constant, in module-body
position after the assignment), so both walkers reach it with no comment parsing and no `tokenize`
pass. The claim is then **checked against the derivation**: a constant declaring `SCHEMA-TWIN` whose
twin has vanished now fails.

> ⚠ **This sits close to a line the charter draws, so the distinction is stated rather than assumed.**
> Forbidden: *checking a list against a second hand-written list.* This is **one falsifiable claim per
> object, checked against a derivation** — the shape `KNOWN_DYNAMIC_DISPATCH_SITES` already used. There
> is no second list, no name map, and the population is still discovered by walking the package.

**Both legs**, per the operator ruling — the same reasoning P2 used, and it matters more here because
F-DT-7's blast radius is entirely downstream:

| Leg | File | What it adds |
|---|---|---|
| **package** (travels with a fork / `pip install`) | `tests/test_registry_consistency.py` | +5 tests: state declared · declared matches derived · `VALIDATOR-ONLY` states a reason · F-DT-3's link · the walk reaches `schema.py` |
| **vault** (additionally checks spec §7.2) | `how/gates/registry_census.py` | 3 new named fault classes, surfaced through gate #10 |

## ⛩ F-DT-3 — ruled, and linked rather than merged

Operator ruling at this gate: **two vocabularies that coincide — link, do not merge.**
`reserved.BASELINE_TYPES` (what a component may degrade *to*, §11 A-3) and `schema.VALID_NODE_TYPES`
(what node types the baseline document has) answer different questions; §11's no-baseline-overload
rule arguably makes their agreement a *consequence* rather than an identity. Both definitions stand,
and `test_baseline_types_and_node_types_agree` fails the day they diverge — with a message that says
the divergence is **not automatically a bug** and names both specs to review.

⚠ The assertion carries a guard on itself: two empty sets are equal, and would pass vacuously.

## ⛩ F-DT-9 — three claims outlived the commit that falsified them

P2 built `RESERVED_KEYS` its consumer on 2026-09-13. Two days later, three places still said it had
none:

| Where | What it said | Status |
|---|---|---|
| `reserved.py` (the F-GL-1 block) | *"The durable fix … is filed as `idea_reserved_keys_has_no_consumer.md` and **deliberately NOT built here**"* and *"`test_axes.py` … is the **only reader** in the package"* | struck at source, original preserved |
| `test_axes.py:73` | *"RESERVED_KEYS has no consumer … this assertion is currently the **ONLY** thing in the package that reads it"* | struck at source, original preserved |
| `how/backlog/idea_reserved_keys_has_no_consumer.md` | `status: open` | **closed**, body preserved unedited, annotated |
| `CHANGELOG.md` §v2.4.0 | present-tense inside a **dated release record** | **not rewritten** — a dated forward-pointer added instead |

⭐ **The `test_axes.py` comment had named its own expiry condition** — *"If the P1 gate question gives
the tuple a real consumer, this test stops being its only reader and becomes a redundant-but-cheap
belt."* The condition was met, the prediction was exactly right, and the comment still had to be
corrected by hand, because **nothing re-reads a comment.**

⇒ ***a claim left standing beside its own remedy*** — the vault's own defining family (*a stated fact
nobody re-derived*), found this time in the comment that named the family. The test is **kept**, for
the reason it predicted: it pins the two v2.4.0 names *by name*, which the derived check does not.

## Derivation record — every failure class produced, not read

| # | Perturbation | Expected | Got |
|---|---|---|---|
| D8 | `OD_MODES` docstring suppressed | *declares no state*, exit 1, both legs | ✅ `['reserved.py:108 OD_MODES']` |
| D9 | `fromSide`/`toSide` enums 4 → 1 — **the F-DT-7 case** | *declared disagrees with derived*, exit 1 | ✅ `VALID_SIDES declares SCHEMA-TWIN but derives VALIDATOR-ONLY` |
| D10 | a `node.color` enum added, twinning `VALID_COLORS` | *declared disagrees with derived*, exit 1 | ✅ `VALID_COLORS declares VALIDATOR-ONLY but derives SCHEMA-TWIN` |
| D11 | `BASELINE_TYPES` loses `"link"` | F-DT-3's link fails **by name** | ✅ `test_baseline_types_and_node_types_agree` + the state check (both true of that edit) |
| D12 | `OD_MODES` docstring reduced to the bare label | *VALIDATOR-ONLY with no stated reason*, exit 1 | ✅ `['reserved.py:108 OD_MODES']` |
| — | all restored | census exit 0, firewall 0 entries, `canvas_std` 156/10 | ✅ |

⭐ **D9 is P3's justification, executed.** It re-creates the state that left all ten gates green four
hours earlier, and both legs now name it in under a second.

## Numbers, derived

| | |
|---|---|
| Vocabulary constants | **26**, all declaring a state that matches the derivation |
| `SCHEMA-TWIN` | **12** — each citing its JSON pointer |
| `VALIDATOR-ONLY` | **14** — each stating *why* there is no twin |
| `canvas_std` suite | **151 → 156/10**. Derived, not predicted: suite run at HEAD with the tree stashed (**151/10**) and restored (**156/10**); the diff adds exactly **5** `def test_` functions; skips unchanged |
| Firewall touch | **#5** — the fifth deliberate `canvas_std` touch since Keystone; back to diff **0** on commit |
| Gate #10 | now **consumes** the census's named causes instead of re-deriving them |

⚠ **Why gate #10 stopped re-deriving its own causes.** F-DT-6's fix was to derive the fault class in
the gate. P3 moved that derivation into the census and had the gate consume it, because **a second
derivation of the cause is a second thing that can disagree with the first** — F-DT-6 one level up.
One definition, two output modes, nothing to disagree with.

## What P3 deliberately did NOT do

| | |
|---|---|
| ⛔ No invented schema twins | The 14 validator-only vocabularies each say *why* they have none — `VALID_COLORS` because `validate()` accepts `#`-hex (an enum would reject legal colors); `ANCHOR_REF_KEYS` and the two `*_REQUIRED_FIELDS` because they are **key names**, not value domains, and the schema expresses them as `required`. The stated reason is what stops a later reader "fixing" the asymmetry. |
| ⛔ `$defs.reserved` untouched | Still open; `test_reserved_object_stays_open` still pins §7.3. Unknown `_reserved` keys remain advisory, never a rejection. |
| ⛔ No merge of `BASELINE_TYPES` / `VALID_NODE_TYPES` | Ruled: linked, not merged. |
| ⛔ No session-freshness gate for **F-DT-8** | Real, and not this campaign's surface. Filed, not built — the scope discipline P2's ruling was careful about. |
| ⛔ No values changed | `schema.py`'s header promise (*"No values are invented here"*) holds: every edit is a docstring. |
