---
type: artifact
artifact_id: p1_under_coverage_ruling
title: "P1 ruling — does the split axis still under-cover hand-authored primary artifacts? No, and the reason is that they were never in scope"
campaign: campaign_canvas_plumbline
phase: P1
created: 2026-09-11
updated: 2026-09-11
status: ruled
last_edited_by: agent_mondrian
rules: [p2b_authority_axis_evidence, b1_5]
sources: ["aDNA.aDNA/what/patterns/pattern_diagrammatic_context.md @ 67ad713"]
tags: [ruling, authority_axis, production_axis, under_coverage, p2b, conform, plumbline]
---

# P1 ruling — the under-coverage question

## The question the charter refused to assume

Two independent pieces of evidence were sent to Rosetta on this axis, and the ruling cites only one:

| Evidence | Defect | Cited in the ruling? |
|---|---|---|
| **E2** (2026-09-04) | **Double coverage** — two canvases are `dual_channel` *and* machine-generated at once | ✅ by name, twice |
| **P2b** (2026-09-07, held, never dispatched) | **Under coverage** — 8 real canvases where *"all three values are wrong"* | ❌ not mentioned |

The ruled `authority` axis has **two** values, and *both presuppose something else owns the meaning*:
`dual_channel` (the prose owns it) and `view` (an authoritative `.lattice.yaml` owns it). A
hand-authored primary artifact — a teaching diagram, a review board — owns its own. So on the face of
it, **the split fixed the defect that was cited and may have left the one that was not.**

That mattered concretely: it decides what Berthier and ScienceStanley are offered at P3.

## The ruling: the population was never in scope, so there is nothing to under-cover

**Ruled from the pattern's text, not from inference.** Three quotations, each load-bearing:

**1. The scope is a *pair*, stated in the one-liner** (`pattern_diagrammatic_context.md:19-23`):

> *"a key object — an architecture, a spec, a decision — **carries two channels side by side**: the
> prose you read, and a conformant `.canvas` you see."*

**2. Both named failure modes presuppose the pair** (`:37-44`). The drifted picture is *"the prose is
edited, the diagram is not."* The undeclared picture is *"a `.canvas` sits **beside a document**."*

**3. And the anti-pattern is scoped the same way** (`:177`) — this is the sentence the charter flagged
as possibly binding:

> *"**The undeclared canvas.** A `.canvas` **beside a document** with no authority and no production
> value, so the next contributor decides by guessing."*

⇒ **`pattern_diagrammatic_context` governs a canvas that is a *second channel for something else*.**
A standalone hand-authored canvas that *is* the primary artifact is not diagrammatic context at all.
The `authority` question — *who owns the meaning?* — **does not arise**, because there is no other
channel for it to be about. An axis cannot under-cover a population it does not cover.

**Corroborated by the pattern declining the mandate outright** (`:88-90`):

> *"This pattern **does not** declare a canvas without a stated authority *nonconformant*. Mandating a
> field no validator checks would be **a conformance claim with nothing behind it**."*

So omission is not a gap to be filled later. **It is the correct answer**, and the pattern says so.

## ⛩ F-PL-7 — the nearer cause was in our own function signature

The P2b tier-2 offer was held because *"no `authority` value fits a hand-authored canvas."* True. But
the reason that **blocked** anything was ours:

```python
def uplift_to_adna_native(doc, *, source_name: str, authority: str, ...)   # authority REQUIRED
```

`conform.py` made `authority` a **required argument**. Nothing in the Standard required that;
`canvas_std` does not know the key at all. It was a faithful implementation of **Canvas's own draft
pattern**, which said *"`none` is retired: a canvas with no declared authority is nonconformant
diagrammatic context"* — the clause the ruling **declined to adopt**.

> ⇒ ***We escalated to another vault a blocker whose proximate cause was a keyword argument in our
> own module.*** The doctrine question was real and the axis genuinely needed splitting — E2's finding
> was independent and correct. But *"tier 2 is blocked until Rosetta rules"* had a second, nearer
> cause that was never named, because nobody re-read the signature while re-reading the doctrine.

⚠ **Stated fairly, because the opposite reading is also available and is wrong**: this is *not* an
argument that the escalation was unnecessary. Had we simply defaulted `authority=None` in September,
we would have shipped `production`-less blocks and still had no way to say *"never hand-edit this"* —
E2's defect, unfixed, in 46 vaults. **The doctrine work was necessary; the blockage was not.**

## What follows, mechanically

| Population | `authority` | `production` | Reaches `adna_native`? |
|---|---|---|---|
| Hand-authored primary artifact (Berthier's C08 teaching canvases; SS's review boards) | **omitted** | `hand_authored` | ✅ — pinned by `test_a_hand_authored_primary_artifact_needs_no_authority_at_all` |
| Canvas's two dogfood pairs | `dual_channel` | `generated` | ✅ — the E2 case, now sayable |
| `variant_board` / `tuning_surface` output | **omitted** | `generated` | ✅ — built from a run manifest, no prose twin |
| The `what/lattices/examples/` quartet | `view` | *(unset)* | after the ADR-011 relocation |

**⇒ The P3 offers are unblocked, and they are offered with a key deliberately absent rather than a
value chosen to make a number go green.** That is the same discipline Berthier endorsed by name when
they wrote that tier 2 *"was right to be withheld."*
