---
type: context
subtype: context_guide
topic: derivability
subtopic: registries
created: 2026-09-15
updated: 2026-09-15
status: active
last_edited_by: agent_mondrian
context_version: "1.0"
token_estimate: ~2400
quality_score: 4.4
signal_density: 5
actionability: 5
coverage_uniformity: 4
source_diversity: 4
cross_topic_coherence: 4
freshness_category: stable
sources: ["Operation Blueprint P3/P5", "Operation Gridline P1", "Operation Plumbline P1/P3", "Operation Datum P1-P4b", "Rosetta pin-field ruling 2026-09-11"]
tags: [context, derivability, registry, no_consumer, discovery_pass, falsifiable_claim, doctrine, f_gm_1, f_gl_1, f_dt_7]
---

# Registry derivability — how hand-maintained facts rot, and what actually stops it

> **Doctrine, not inventory.** This file holds principles and the derivations that produced them.
> ⛔ It deliberately carries **no list of this vault's registries** — such a list would be a
> hand-maintained registry with no consumer, which is the defect described below, reproduced inside
> the document describing it. Live populations are produced by `how/gates/registry_census.py`.

## The rule

> **Every hand-maintained registry is in exactly one of two states, and which one it is must be
> written on the line:**
>
> 1. it has a **consumer** — something that *fails* when it drifts; or
> 2. it is covered by a **discovery pass** that enumerates the territory rather than reading the map.
>
> ⛔ **The third state is the defect**: correct today, maintained by hand, and read by nothing.

## Principle 1 — a specification with no consumer is indistinguishable from no specification

`canvas_std.reserved.RESERVED_KEYS` named the `_reserved` namespace and was read by **nothing**. So
when Standard v2.4.0 appended two names to it under a ratified LIP, the append was **correct and
inert** — and the proof that an inert list rots was already sitting in it: `interaction`, shipped and
validated since v2.2.0, was absent from **all three** hand-maintained copies of that namespace for
three months.

**No canvas was ever wrong. The *namespace description* was.** That is the characteristic signature:
the system behaves correctly while its own account of itself decays, so nothing user-visible ever
signals the rot.

*(F-GL-1, Gridline P1 · closed at Datum P2.)*

## Principle 2 — a registry defines its own blind spot in its membership rule

`federation_index` answered *"who holds a wrapper?"*. The **10 vaults emitting canvases with no
wrapper at all** — the least-supervised surface in the fleet — were therefore invisible **by
construction**, and no amount of diligent maintenance would have surfaced them.

⇒ **Ask what a registry's membership rule excludes, then ask whether that exclusion is the population
you actually care about.** It often is: the things outside a registry are outside it *because nobody
was thinking about them*, which is the same reason they are risky.

⭐ **The remedy is not a cleverer rule — it is an *unstated* rule made stated.** What made
`federation_index` wrong for five weeks was not a narrow membership rule but an unwritten one.

*(Blueprint P3. Reproduced inside the tool written to measure this family — F-DT-1 — within an hour.)*

## Principle 3 — enumerate the territory; never re-read the map

A registry that is only ever *read* cannot report what was never *written into* it.

- `canvas_context` **left** the published gate line and sat red for two days across three closes,
  each publishing an all-green line. None was lying: no commit removed it, each close copied the
  previous close's list (**F-P5-3**).
- `canvas_presentation` — 57 passed of real library code — **never arrived**. It could not be noticed
  missing, because there was nothing to notice the absence of. Only enumerating the disk found it
  (**F-GM-1**).

> ⭐ **A skipped test prints `s`. A suite nobody invoked prints nothing at all, and the gate line
> beside it reads exactly as green.**

⚠ **And a glob is not enumeration.** `ls */CLAUDE.md` counts *names*; `find -P` counts *things*. A
shim is a second true name for one object, so a glob double-counts live vaults and resurrects archived
ones — 254 files across 62 vaults where the truth was 282 across 69 (Rosetta, contributed).

## Principle 4 — visibility is not coverage, and false visibility is worse than none

**The most important principle here, and the last one learned.**

`RESERVED_KEYS` was *visibly* read by nothing — and that visibility is exactly what got it fixed. The
JSON Schema's eleven value enums had a census, a twelve-pair correspondence table, and a published
phase result all stating they agreed exactly. **Gutting one of them left all ten gates green**, while
an external validator correctly rejected an ordinary document.

The mechanism generalises past schemas: the census paired vocabularies **by content**, so when a pair
diverged past its similarity floor it did not report drift — **the pair dissolved**, and the constant
reclassified into a normal, accepted state. The instrument failed into *reassurance*. It even printed
a confident explanation — *"unrelated vocabularies reusing a generic token"* — about the Standard's
own edge-side enum.

> ⇒ ***A registry that LOOKS watched is better hidden than one that visibly is not.***

⚠ **Corollary, measured the same day:** the same trap waits one layer out in *tests*. A fixture-corpus
conformance suite looks like it guards the eleven enums; it exercises **12 of 40** declared values,
and two enums **not at all**. Whether a given drift is caught turns on which value the corpus happens
to use — `fromSide` is accidentally guarded, `toSide` is not.

> ⇒ ***A test that looks like coverage is worse than no test, unless somebody measures what it covers.***

⚠ **And the blind spot compounds.** A coverage *ratchet* on the covered count is blind to the deletion
of exactly the vocabularies it was already failing to exercise — a zero-coverage enum contributes
nothing to the count, so removing it changes nothing the ratchet measures. Pin the **declared** total
separately.

*(F-DT-7 · D13a/b/c, Datum P3–P4b.)*

## Principle 5 — the remedy is a per-object falsifiable claim, never a second list

⛔ **Checking a list against another hand-written list is the defect wearing a test's clothes.** What
works:

| | |
|---|---|
| **Discovery** | walk the AST, the disk, the schema. Never read a roster. |
| **Content-matching, not name-matching** | a name map (`VALID_SIDES → /$defs/edge/…`) is itself an unconsumed registry. |
| **A declared state on each object, checked against the derivation** | so a wrong claim **fails**. |

The third is what gives content-pairing the *memory* it structurally cannot have. In `canvas_std` the
carrier is a PEP 258 attribute docstring whose first word is the claimed state — but the mechanism
matters far less than the property: **the claim must be refutable by something that runs.**

⚠ The distinction from the forbidden pattern is worth stating explicitly, because they look alike:
**one falsifiable claim per object, checked against a derivation** — with the population still
discovered by walking. There is no second list.

## Principle 6 — publish the blind spot's size beside the number

Every instrument has a limit. A static walk cannot resolve dynamically-keyed dispatch; content-pairing
cannot see total divergence; a fixture corpus covers what its fixtures happen to use.

⛔ **The remedy is not a cleverer instrument.** It is reporting the limit **on the face of the
result**, so the number is never read as complete:

- the dispatch key list prints a `dynamic` site count beside it — *a floor, not a census*;
- the coverage report prints `12/40` and **names the zero-coverage enums**;
- discovery reports every symlink it skipped.

## Principle 7 — the report is part of the check

A gate that observes correctly and then reports a literal has only moved the unverified claim to the
layer that gets published.

- `markdown_gate_line()` **hardcoded green** for three gates: `"firewall diff **0**"` was a *constant
  string*, printed while the firewall was FAILING — in the one string a close **pastes** (**F-GL-7**).
- The census gate named **one** fault class unconditionally, so a drifted schema twin was announced
  as a namespace disagreement and sent the reader to the wrong three files (**F-DT-6**).

⭐ **And the corollary found by fixing it twice:** a *second derivation* of a cause is a second thing
that can disagree with the first. Derive the fault classes **once**, in the instrument; let the
reporter consume them.

⚠ **Sibling trap:** *a predicate only ever run against a clean tree has only ever been tested for its
false case.* The firewall check ran `git diff` — unstaged only — and was blind to staged and untracked
breaches, two of three classes, including the one a firewall touch necessarily performs. It had never
fired because no campaign had yet staged such a change (**F-GL-2**).

## Principle 8 — governance documents are registries too

The class is wider than code:

| Artifact | How it rotted |
|---|---|
| `STATE.md` phase rows | said *"P0 closed, P1 next"* while P1 and P2 had been committed two days |
| the session file | `status: active`, `phase: "Act 0 → P0"`, work log unappended, across four commits and two rulings (**F-DT-8**) |
| `who/coordination/AGENTS.md` | inherited template describing a naming convention **0 of 80** files used — and instructing *deletion*, contrary to SO-6 (**F-DT-11**) |
| a comment beside its own remedy | *"the durable fix is deliberately NOT built here"*, still standing two days after it was built (**F-DT-9**) |

⭐ **One of those comments had named its own expiry condition exactly, the condition was met, and it
still had to be corrected by hand** — because *nothing re-reads a comment*.

⚠ **But do not over-correct.** A document written **by exception** is not a broken registry: `how/gates/AGENTS.md`
documents *gates with a story*, and 4 registered gates have never appeared in it **correctly**. Adding
a completeness check over a knowingly partial document manufactures Principle 4's shape.
⇒ ***A missing twin is a fact to state with its reason, not a defect to remedy.***

## How to apply this

1. **When you write down a fact that lives in two places, name its consumer in the same commit.** If
   there is none, say so **on the line** — with the reason.
2. **When you build a checking instrument, perturb it.** Every finding above was produced by breaking
   something and watching, never by re-reading. *Re-reading never catches these; re-deriving does.*
3. **State the population on the face of the number** — tip or history · class or literal · tracked or
   working-tree.
4. **A disagreement is a finding to investigate, not a number to edit** into the expectation.
5. **Not every registry deserves a checker.** A check needing carve-outs exactly where its population
   is irregular will be *false* coverage — memo numbers were declined for precisely this, and the
   obligation was discharged by **writing the state down** instead.

## Related

[[context_canvas_standard_doctrine]] · [[context_canvas_surface_legs]] ·
`how/gates/AGENTS.md` (the executable gate set) ·
`how/backlog/idea_upstream_registry_derivability.md` (the upstream proposal) ·
`how/campaigns/campaign_canvas_datum/` (the campaign that produced Principles 4–6).
