---
type: artifact
artifact_id: p1_registry_correspondence
campaign: campaign_canvas_datum
phase: P1
title: "The registry population, enumerated — 26 vocabularies, 12 with a schema twin, 14 read only by a validator"
created: 2026-09-13
updated: 2026-09-13
status: complete
last_edited_by: agent_mondrian
tool: how/gates/registry_census.py
tags: [artifact, datum, registry, census, discovery, canvas_std, f_dt_1, f_dt_2, f_dt_3]
---

# P1 — the registry population, by discovery

Produced by `python3 how/gates/registry_census.py` (exit **0**), 2026-09-13. ⛔ **Every figure below is
derived by the tool, not transcribed** — the tool contains no list of registries and no map from a
Python constant to its schema twin, because either would make it the fourth instance of the defect it
measures.

## Population

| | measured | plan said |
|---|---|---|
| Python vocabulary constants | **26** across 2 modules | *25* |
| Schema `enum` nodes | **14** | 14 ✅ |
| `$defs.reserved.properties` | **11** | 11 ✅ |

⚠ **The plan's 25 was wrong and the re-derivation caught it.** It came from eyeballing a `grep -nE`
listing during planning; the AST walk finds **26**. This is the campaign's own subject appearing in the
campaign's own charter — a figure written down once and not re-derived. Recorded rather than quietly
corrected, per the standing rule.

## Correspondence — matched **by content**, never by name

Pairing by name would need a `VALID_SIDES → /$defs/edge/properties/fromSide` table, and that table is
itself a hand-maintained registry with no consumer. Two vocabularies are twins here **if they say the
same thing**.

### SCHEMA-TWIN — 12 constants with an exact schema counterpart

| Constant | Schema pointer |
|---|---|
| `AUTHORITY_VALUES` | `reserved.authority` |
| `PRODUCTION_VALUES` | `reserved.production` |
| `VALID_NODE_TYPES` · `BASELINE_TYPES` | `node.type` *(both — see F-DT-3)* |
| `VALID_SHAPES` | `node.styleAttributes.shape` |
| `VALID_BORDERS` | `node.styleAttributes.border` |
| `VALID_TEXT_ALIGN` | `node.styleAttributes.textAlign` |
| `VALID_SIDES` | `edge.fromSide`, `edge.toSide` |
| `VALID_ENDS` | `edge.toEnd`, `edge.fromEnd` |
| `VALID_PATH_STYLES` | `edge.styleAttributes.path` |
| `VALID_ARROWS` | `edge.styleAttributes.arrow` |
| `VALID_PATHFINDING` | `edge.styleAttributes.pathfindingMethod` |

**All twelve agree exactly.** No drift.

### VALIDATOR-ONLY — 14 constants with no schema counterpart

`RESERVED_KEYS` · `COMPONENT_CLASSES` · `PL_EDGE_KINDS` · `PL_FLOW` · `PL_PAGINATION` ·
`PL_EXTENT_UNITS` · `NC_LABEL_FORMS` · `OD_MODES` · `ANCHOR_REF_KEYS` · `LONGFORM_SEMANTIC_TYPES` ·
`AFFORDANCE_KINDS` · `VALID_COLORS` · `NODE_REQUIRED_FIELDS` · `EDGE_REQUIRED_FIELDS`

⛔ **A missing twin is a fact, not a defect.** These are validator-only *by design* — the JSON Schema
covers the baseline Obsidian document shape, while the `_reserved` sub-vocabularies are governed by
their own specs (`spec_component_model`, `spec_panel_link_semantics`, `spec_interface_surface`) and
enforced in code. `VALID_COLORS` has no enum because `validate()` also accepts `#`-hex, so an enum
would be wrong. **Nothing here should acquire an invented schema twin.**

⇒ **These 14 are the campaign's actual surface.** They are the registries whose only consumer is the
validator that uses them — which is a genuine consumer for *value* checks, but **nothing at all** for
the question "is this list still the right list?"

## The `_reserved` namespace — the F-GL-1 surface, re-measured

| Copy | Keys |
|---|---|
| `canvas_std.reserved.RESERVED_KEYS` | **11** |
| schema `$defs.reserved.properties` | **11** |
| spec §7.2 fenced block | **11** |
| **all three agree** | ✅ **True** |

`$defs.reserved` is confirmed **open** (`additionalProperties` unset) — §7.3's forward-compat promise is
structurally intact, and it is asserted by the tool rather than assumed.

⭐ **The Gridline back-fill held.** This is the first time that claim has been *checked* rather than
believed; before today nothing could have told us either way.

## What the validators actually dispatch on

**10 statically-derivable keys**, all present in `RESERVED_KEYS`:
`adna_version` · `conformance_level` · `sync` · `component_types` · `semantic_bindings` · `panel_link` ·
`context_object` · `interaction` · `authority` · `production`

- ⓘ **`brand_style_pack_ref` is declared but never dispatched** — correct: it is producer-resolved
  (VisualDNA), and the Standard carries the key without validating it.
- ⚠ **2 dispatch sites key off a variable** (`reserved.py::_validate_axes:193,195`) and are invisible to
  any AST walk. The count above is therefore a **floor, not a census**, and the tool says so on the
  face of the result.

---

# Findings

## ⛩ F-DT-1 — the dispatch detector had two blind spots, and only one of them can be closed

**Found by running the tool, not by reading it.** The first version reported **9** dispatched keys. The
true static count is **10**.

1. **`not in` was not matched.** The walker handled `ast.In` only, so it never saw
   `if "authority" in reserved and "production" not in reserved` (`reserved.py:183`) — it read the
   first half of that line and was blind to the second. **Fixed.**
2. **Dynamically-keyed dispatch cannot be named.** `_validate_axes` iterates a literal tuple —
   `for key, allowed in (("authority", AUTHORITY_VALUES), ("production", PRODUCTION_VALUES))` — then
   does `reserved[key]` with a *variable*. No static walk can resolve that key. **Not fixable; reported
   instead**, as a count of `dynamic` sites printed beside the key list.

⇒ ***A detector's population is defined by its own membership rule.*** This is Blueprint P3's
`federation_index` finding — *a registry defines its own blind spot in its membership rule* —
reproduced **inside the tool written to measure that family**, within an hour of writing it. The remedy
is not a cleverer walker. It is publishing the blind spot's *size* next to the number, so the number is
never read as complete.

## ⛩ F-DT-2 — content-pairing reported coincidence as drift, three times out of three

The first run flagged **3 PARTIAL** pairs and **all three were false**:

| Pair | Shared | Jaccard |
|---|---|---|
| `COMPONENT_CLASSES`(14) vs `node.type`(4) | `text` `group` `link` | 0.20 |
| `PL_FLOW`(4) vs `toEnd`(2) | `none` | 0.20 |
| `PL_PAGINATION`(3) vs `toEnd`(2) | `none` | 0.25 |

Unrelated vocabularies collide on generic tokens — `none`, `text`, `right` — because natural
vocabularies reuse words. That is not drift; it is English. Drift has a different shape: a *copy* with
a member or two changed, sharing most of its **union**.

Floor set at **Jaccard ≥ 0.5**, stated before it was tested, then verified by derivation both ways:
coincidence tops out at **0.25**; dropping one member from the 4-member `VALID_SIDES` scores **0.75**
and is correctly reported. ⚠ The gap is wide but it is an *observation about this corpus*, not a
guarantee — a future 2-member vocabulary sharing one token would score 0.33 and be filed as
coincidence. If that ever matters the answer is a named exception with a reason, **not a nudged
constant**.

## ⛩ F-DT-3 — two constants hold an identical vocabulary and nothing links them

```
['file', 'group', 'link', 'text']
    reserved.py:54   BASELINE_TYPES      (the degradation target set, A-3)
    schema.py:18     VALID_NODE_TYPES    (the baseline node types)
```

**Both are correct.** They are also two hand-maintained copies of one four-word vocabulary, in two
modules, with **no link between them** — so if the baseline ever gains a node type, one can move and
the other cannot notice. This is the campaign's target in its purest form: *not* a drift, but the
precondition for one.

⛔ **Not auto-merged, and not proposed for merging here.** Whether "the baseline node types" and "what a
component may degrade to" are *one* vocabulary or two that currently coincide is a **semantic** question
a set comparison cannot answer — and the Standard's degradation contract (§11 no-baseline-overload)
arguably makes their coincidence a *consequence* rather than an identity. Carried to the P3 gate as a
question for the operator, with the measurement attached.

## ⚠ Two self-caught shell slips, recorded not buried

Both are the same class, and it is the class this vault keeps re-finding: **a status read from the
wrong object.**

1. `${PIPESTATUS[0]}` after a pipe returned an **empty string** (P0). `PIPESTATUS` is a bash array;
   this shell is zsh (`$pipestatus[1]`). An empty string glosses as success.
2. `CENSUS="python3 how/gates/registry_census.py"` then `$CENSUS` returned **exit 127**. **zsh does not
   word-split unquoted parameter expansions**, so the whole string became one command name. The
   derivation check D1 that ran through it therefore *tested nothing* — and its `||` branch printed
   "1 = drift reported, correct" beside a 127. **A verification harness that cannot run its subject
   still prints a verdict.**

⇒ Slip 2 is worth more than slip 1: it is F-P2-11's family (*a check that cannot run is not a check
that passes*) occurring **inside the derivation step whose entire purpose was to prove the tool works.**
D1 was re-run without the variable and passed properly.

# Derivation record — the tool verified by perturbation, not by reading its output

| # | Perturbation | Expected | Got |
|---|---|---|---|
| D1 | drop `"right"` from `VALID_SIDES` | `DRIFT?` naming `fromSide`/`toSide`, exit 1 | ✅ exact, Jaccard 0.75 |
| D2 | add `if "telemetry_probe" in reserved:` to `validate_reserved` | key flagged `⛔ NOT IN RESERVED_KEYS`, exit 1 | ✅ |
| D3 | delete `interaction:` from spec §7.2 — **the literal F-GL-1 state** | three-way disagreement, exit 1 | ✅ `python-not-spec: ['interaction']` |
| — | all restored | exit 0, firewall 0 entries | ✅ |

⭐ **D3 is the campaign's justification, executed.** It re-creates the exact state the vault sat in for
three months — `interaction` shipped, validated, and absent from the spec's key list — and the census
names it in under a second. Nothing that existed in June could have.
