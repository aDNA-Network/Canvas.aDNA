---
campaign_id: campaign_canvas_vernier
type: campaign
title: "Operation Vernier — the Standard met its first external consumer, and the consumer read a field we never defined"
owner: stanley
status: active
estimated_sessions: "2-4"
phase_count: 6
mission_count: "created at phase-open"
priority: medium
executor_tier_default: opus
predecessor: campaign_canvas_datum
created: 2026-09-17
updated: 2026-09-17
last_edited_by: agent_mondrian
status_history: "active (2026-09-17 — chartered at the plan gate on the Armor.aDNA dogfood; three operator rulings taken: charter a campaign · adopt both freshness mechanisms · memo #21 carries findings plus both flags)"
tags: [campaign, canvas, vernier, armor, bastide, dogfood, sync_hash, a8, provenance, freshness, dual_channel, standard_evolution]
---

# Campaign: Operation Vernier

> A **vernier** scale reads *between* the marks of the main scale — it exists because the main scale's
> divisions are not fine enough to say what you actually need to say. The Standard's `sync_hash` field
> has marks: it is validated to be sixteen hex characters. **Two vaults read two different values
> between those marks, and both pass.** That is this campaign.

## Why this campaign exists

**`Armor.aDNA` is the aDNA Canvas Standard's first major external consumer** — a staged campaign
(`campaign_terminal_bastide`) whose architecture is **dual-memorialised**: 19 prose context documents
alongside **7 generated canvases**, each canvas naming its text twin. Canvas.aDNA is the
standard-bearer, so dogfooding this is ours — and the Standard has never before been exercised at this
scale by a vault that did not help write it.

⭐ **The result is not a defect list. It is mostly a pass, and the failures are ours.**

## ⭐ What Armor got right — stated first, because it is the larger part of the result

| | |
|---|---|
| **Canonical placement** | All 7 carry `_reserved` at `metadata.frontmatter._reserved` — the thing **194 fleet canvases still get wrong** (ADR-011), got right first time by a vault reading the spec cold. |
| **The A-8 axis pair** | `authority: "view"` **and** `production: "generated"` together, satisfying the asymmetric co-requirement. The first external vault to get v2.4.0's axes right. |
| **The authority semantics** | Their README states it plainly: *"The markdown is authoritative; the canvas is the view."* That is the `view` row, understood rather than copied. |
| **The regenerate discipline** | *"After editing a text twin, regenerate… never edit the digest."* — what `production: generated` is **for**. |
| **A reasoned under-declaration** | `conformance_level: extended` is **deliberate**, with a named unblock (*"until the panel/link kinds are validated… Phase D"*). ⚠ **Not an error** — it is the *state the reason on the line* discipline, practised by someone who was never told to. |

## The three findings — all of them Canvas's own

### ⛩ V-1 · `sync.sync_hash` has two incompatible meanings, and both validate

`canvas_std.roundtrip.compute_sync_hash()` returns a **topology** hash (sorted node ids + `from→to`
pairs, truncated to 16). Armor stores a **source-document** hash. Measured: `220298a17b9d680e` is
**exactly** `sha256(what/context/03_ARCHITECTURE.md)[:16]`, carried identically on three canvases whose
own topology hashes are `c8eb617d…`, `bb308ee8…` and `d94093186…` — all different.

**Neither vault is wrong**, because **the Standard never says what the field hashes.** The spec lists
`sync: { sync_hash, source_name, source_version }` and stops; A-6 checks *"is not 16 hex chars"* —
**shape, not semantic** — and its own code comment defers the rest: *"hash↔source match is checked by
the round-trip layer."*

⇒ ***A field with a validated shape and an undefined semantic will acquire two meanings, and both will
pass.*** This is Canvas's own derivability family — a specification that constrains **form** but not
**meaning** — and it took an outside reader to surface it, because inside this vault only one
implementation existed.

⚠ **And Armor's reading is arguably the more useful one for a `view` canvas**: the question a derived
view needs answered is *"has my source moved?"*, which a source hash answers and a topology hash does
not.

### V-2 · A-8 is gated behind aDNA-Native, so a correct axis pair can be inert

All 7 declare `extended`. At that tier `validate()` never reaches A-8, so the axis pair they took care
to set right is **not validated** — an invented value would pass unnoticed. They did the work; their
declared tier means nothing checks it.

⚠ The axis question — *who owns the meaning · how is it made* — applies to **any** derived canvas, not
only aDNA-Native ones. The keys live in the aDNA-Native tier for reasons that predate the axes.

### V-3 · They invented `generator`, the word LIP-0010 removed

All 7 carry `generator: "what/canvas/build_canvases.py"` inside `_reserved` — **undeclared** in
`RESERVED_KEYS` (legal per §7.3: unknown keys are preserved, advisory, never a rejection), alongside
`title`.

⭐ **`generator` is precisely the value LIP-0010 struck from the `authority` axis**, for conflating
*who owns the meaning* with *how it is made*. Armor did not reinstate it as an authority value — they
reinvented it as a **provenance key**, which is the distinction LIP-0010 was drawing. ⇒ **independent
demand for a provenance carrier the Standard does not offer.**

## ⭐ The finding that runs upstream into Canvas — two freshness mechanisms, neither subsuming the other

| | catches | misses |
|---|---|---|
| **source hash** (Armor) | the input moved | ⛔ **generator drift** — *exactly F-PL-6's cause*, where Canvas's own dual-channel pair went stale because the **layout engine** changed, not the source |
| **rebuild-compare** (Canvas gate #9) | the output would differ | nothing — but costs a rebuild and requires the generator to be present and reproducible |

⚠ A prose typo makes the source hash report **stale when the canvas is fine** (false positive);
generator drift makes it report **fresh when the canvas is stale** (false negative). ⭐ Armor's is
**third-party verifiable**: all 7 confirmed fresh from outside their vault in three lines, with no
access to their generator.

**Ruled: adopt both**, with each mechanism's blind spot on the face of the output.

## Definition of done

1. `sync_hash`'s semantic is **defined**, not merely shaped — or the field is split so each meaning has
   its own name.
2. The A-8 tier question is **ruled**, either way, with the reason recorded.
3. `generator` is either **adopted** as a provenance key or **ruled** a producer-local §7.3 extension.
4. Gate #9 carries **both** freshness mechanisms, each labelled with what it cannot catch.
5. Armor holds the findings, **with credit stated first**.

## ⛔ What this campaign must not do

| | |
|---|---|
| ⛔ Must not write into `Armor.aDNA` | Read-only recon; the memo is delivered to their inbox and left untracked (Rule 10). |
| ⛔ Must not narrow `sync_hash` without pricing the migration | It has **already shipped in two meanings**. Choosing one breaks a live consumer; say which, and what it costs, before choosing. |
| ⛔ Must not treat Armor's choices as defects | Three of the five things they did are things the fleet gets wrong. The report leads with that. |
| ⛔ Must not let a cheap pre-filter read as coverage | A source hash in front of gate #9 is the **F-DT-7 shape** if its blind spot is not published beside it. |
| ⛔ Must not fix what is not ours | Armor's missing git repo and its absence from the workspace router are **reported with owners named**, never repaired here. |

## Phases

| Phase | What | Gate |
|---|---|---|
| **P0** | Wind down the review-package stretch (AAR) · charter · STATE | plan gate — approved |
| **P1** | The dogfood artifact — **every figure re-derived at execution**, credit first | ⛩ **the V-1/V-2/V-3 rulings AND the firewall ruling are taken at this exit gate** |
| **P2** | Rule V-1 · V-2 · V-3. LIP where the ruling touches the Standard | human gate |
| **P3** | Freshness — gate #9 gains the source-hash pre-filter, blind spots published | human gate |
| **P4** | Doctrine (`context_registry_derivability`) + **memo #21** to Berthier | human gate |
| **P5** | Close — AAR, STATE, gate line pasted from `--markdown` | close gate |

⛩ **Why the rulings wait for the P1 exit.** P1 is pure measurement and touches no firewalled file, so
nothing is blocked by waiting — and V-1 in particular is a choice between breaking our own
`compute_sync_hash` and breaking a live consumer. That signature should be informed by the measured
table, not by a plan's summary of it. The Datum precedent, applied deliberately.

## Live items

⛔ **Four operator verdicts remain pending at the doors** (`adr_010` · `adr_011` · `adr_012` ·
`operator_queue_20260916`) and are **untouched by this campaign**. Memo **#20** stays staged.
