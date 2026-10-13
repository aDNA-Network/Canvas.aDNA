---
campaign_id: campaign_canvas_vernier
type: campaign
title: "Operation Vernier — the Standard met its first external consumer, and the consumer read a field we never defined; by the time we read the mail, four vaults had"
owner: stanley
status: active
estimated_sessions: "5-8"   # amended 2026-10-12 (was 2-4)
phase_count: 8   # amended 2026-10-12 (was 6)
mission_count: "created at phase-open"
priority: medium
executor_tier_default: opus
predecessor: campaign_canvas_datum
created: 2026-09-17
updated: 2026-10-13
last_edited_by: agent_mondrian
status_history: "active (2026-09-17 — chartered at the plan gate on the Armor.aDNA dogfood; three operator rulings taken: charter a campaign · adopt both freshness mechanisms · memo #21 carries findings plus both flags) · active, SCOPE AMENDED (2026-10-12 — plan gate: subject repointed Armor→Terminal.aDNA; V-1 widened to four vaults; V-4…V-8 added from the 17-memo inbox; phases 6→8; fold-not-sibling per operator precedent) · active, PHASE ORDER AMENDED (2026-10-13 — plan gate: P6 verdict-independent objectives run ahead of P2; P6 phase gate unchanged)"
tags: [campaign, canvas, vernier, armor, terminal, bastide, scope_amendment, lip_0011, b14, b18, dogfood, sync_hash, a8, provenance, freshness, dual_channel, standard_evolution]
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

---

## ⛩ Scope amendment — 2026-10-12 (plan gate; dated, not retro-fitted)

> The campaign waited 25 days at its P1 exit gate. In that window **17 inbound memos** arrived
> ([triage](artifacts/review_20261012_vault_state_and_inbox_triage.md) §2) and **four of them asked
> V-1's question independently** — Vauban/Terminal, Ledoux/City, Berthier/Automator (Boulogne B14),
> Noether/LatticeProtocol (whose `gen-canvas` is **carded on our answer**, and whose ADR-018 + the
> LinkML Profile v0.1 already define `sync_hash` as the master's byte hash). The memo cluster *is* this
> campaign's subject, widened — so it is folded in as phases, not chartered beside it (operator
> precedent: fold over sibling).

### Subject repointed

**`Armor.aDNA` was archived 2026-09-24** (Hestia; it was Terminal's pre-b06 staging snapshot, 74/75
files byte-identical to `346f9cb`). The live subject is **`Terminal.aDNA/what/canvas/`** — **8**
canvases (`bastide_design_system` added at b03), regenerated as late as the morning of this amendment
(`319b770`). **P1 re-derived against the live eight 2026-10-12: 8/8 canonical `_reserved` · 8/8 A-8
pair · 8/8 source-hash match · 0/8 topology match · 8/8 `[OK]` at declared tier · 8/8 `[OK]` with only
`conformance_level` flipped · 8/8 carry `generator`.** The P1 artifact's seven-row table stands as the
frozen measurement of the archived snapshot. P1's two *"not ours"* flags dissolve: the git history was
Terminal's all along; the staging directory's absence from the router is moot.

### Items — V-1 widened, V-4…V-8 added

| | Item | Waiters | Ruling surface |
|---|---|---|---|
| **V-1** (widened) | `sync.sync_hash` semantic + a standard full-digest key. Three readings now pass: topology (`canvas_std`, City) · source-document bytes (Terminal) · master-file bytes (LP ADR-018, Profile v0.1). Noether Q1/Q2 are the sharpest form. | Terminal · City · LP (`gen-canvas` M-B1) · Automator (B14) | door |
| **V-2** | A-8 inert below `adna_native` — tier question | Terminal (8 `extended`) | door |
| **V-3** (second instance) | `generator` as a provenance key — Terminal 8/8 top-level `_reserved.generator`; **Home `topology.canvas`** `authority: "generator"` at a non-canonical path (Berthier's FYI, confirmed) | Terminal · Home | door |
| **V-4** | **B14 dual-mode schema pack** (LinkML master + `.canvas` twin `dual_channel` + image + prose, one sync hash) — where the rule lives (Standard vs ADR-062); loading modes text/diagram/both in `spec_canvas_context_loading` | Automator · City · Terminal | door |
| **V-5** | **B18 per-graph `graph.canvas`** (`view`/`generated`) + live overlay — one file with a group, or a second file keyed by node id; City's floorplan reading | Automator · City | door |
| **V-6** | `_reserved` placement for generated canvases — spec as written vs grandfathering note | Automator (Home's finding) | door |
| **V-7** | Noether's **lattice dispositions** (our 2 lattice files + example = not-a-lattice → "Canvas format"?) + **4 CEL rewrites**. Measured: no runtime consumes them (1 federation test · 1 archived smoke · AILedger Folio dossier *pointer*). | LP (**overdue** — P3 opened 10-10) | door |
| **V-8** | Socials: social formats in `post_generator` today? (**measured: not yet**) · `style_ref` by reference · read-only RLHF rows · is `iii_quality_contract.md` the binding contract? | Socials (SG-4 blocks on (1)) | door + P7 |

### Phases — 6 → 8

| Phase | What | Gate | State |
|---|---|---|---|
| P0 | Wind-down AAR · charter · STATE | plan gate | ✅ 2026-09-17 |
| P1 | Dogfood artifact, figures re-derived | — | ✅ 2026-09-17 · **re-derived on the live subject 2026-10-12** |
| **P1b** | Review + inbox triage + this amendment + the ruling door rendered + interim acks | plan gate (2026-10-12) | ✅ this sitting |
| **P2** | Rule V-1 … V-8 + the firewall touch at [`how/gates/vernier_p1_exit_20261012`](../../gates/vernier_p1_exit_20261012.html) | **human gate — at the door** | ⛔ owed |
| **P2b** | **LIP-0011** sync semantics → Standard **v2.5.0** (additive); firewall touch #7; backward-compat **measured on the fleet corpus** | human gate | [mission](missions/mission_vernier_p2b_lip_0011_sync_semantics.md) |
| P3 | Freshness both ways — gate #9 + `canvas-std check-sync` for third parties | human gate | [mission](missions/mission_vernier_p3_freshness_both_ways.md) |
| P4 | Doctrine (Principle 4b, n=4) + substantive replies carrying the verdicts + B14/B18 spec text | human gate | [mission](missions/mission_vernier_p4_doctrine_and_memos.md) |
| **P5** | **Canvas memorialisation research** — context doc, pattern proposal, AILedger offer, our own `graph.canvas` | human gate | [mission](missions/mission_vernier_p5_canvas_memorialisation.md) |
| **P6** | **Vault review & hygiene** — STATE compaction, F-DT-10, pins, LIP drafts, gate #11 `inbox_receipt`, door-port check, F-S078-04, Seven Lamps, ImagenWiring, RFC1918, `data_bearing` | human gate | [mission](missions/mission_vernier_p6_vault_review_and_hygiene.md) |
| **P7** | **`post_generator` social formats + `style_ref` + RLHF read path** (Socials) | human gate | [mission](missions/mission_vernier_p7_post_generator_social_formats.md) |
| P8 | Close — AAR, STATE, gate line pasted from `--markdown`, push GO | close gate | — |

### Definition of done — extended

6. B14 and B18 each have **a ruling and a home** (Standard §, profile, or a reasoned decline with the
   owner named), and Canvas has eaten B18 first (`what/canvas/graph.canvas` validates `adna_native`).
7. Every `ack_required: true` memo in the 2026-10-12 inbox has a **substantive** reply carrying a
   signed verdict, not a recommendation.
8. The inbox cannot go unread for three weeks again without a gate line turning ⛔ (gate #11).
9. The memorialisation deferral (Lodestar C-iii) is **re-evaluated on the record**, either way.

### ⛔ Added to "what this campaign must not do"

| | |
|---|---|
| ⛔ Must not answer V-1 in a memo before the door | Four vaults will build on the answer; a recommendation in prose is read as a ruling by whoever needs one. Interim acks say *recommendation, door rendered, not a signature*. |
| ⛔ Must not accept the 16 elsewhere-owned canvasforge files into "the Canvas format" | The Standard describes canvases, not the pipelines that make them; receiving workflow descriptions would invent a format to hold them. Say so. |
| ⛔ Must not compact STATE in the same sitting that adds to it | Today adds a dated banner; P6 restructures with the archive file beside it. |

## ⛩ Phase-order amendment — 2026-10-13 (plan gate; dated, not retro-fitted)

**Ruling (operator, plan gate, `AskUserQuestion` 2026-10-13):** *"Door + P6 hygiene"*. P2 is still the operator's verdict at the
door, which is unruled at this sitting's open: `.pending` present, no `.output.json`, receiver `:8767` healthy. So the **P6
objectives that depend on no verdict run now, ahead of P2–P5**. That covers obj 1–6: STATE compaction · F-DT-10 · pins + LIP
statuses · gate #11 `inbox_receipt` + `--check-doors` · F-S078-04 · the ImagenWiring sweep, plus the opus items as context allows.
**Obj 7 (door archival per Home ADR-017) still waits for the verdicts**, and **the P6 phase gate stays a human gate**. Running
an objective early does not close its phase.

**Evidence added to the door, not a ruling.** Three replies arrived 10-12, after P1b closed, and were receipted at `db21711`
(body md5 = `delivered_md5_body` ×3). LP **withdraws (a)** and has no objection to (b). Terminal accepts (b) + V-3 in direction
and **migrates once, after P4**. Socials says no date of theirs forces P7 before LIP-0011, and discloses a bounded direct image
bridge that closes on our verdict memo. All three were folded into V-1 · V-3 · V-8 and the door re-rendered (`e2ddf15`). **No
recommendation changed.** V-8 gained a fifth sub-question: close that bridge before the verdict memo, or on it (default).

**F-V-7 — a memo addressed to us that only reached a peer.** Vulcan's
`coord_2026_10_08_outbound_vulcan_to_mondrian_vitruvius_ledoux_anduril_endpoint` names Mondrian first. Its copy sits in
**City's** inbox, and the Canvas copy is still `status: staged` in `ComfyUI.aDNA/who/coordination/`, five days later. It
carries the **venue of record for the H4 live chain**: ComfyUI 0.39.2 on Anduril's RTX 3090, `comic_panel_refine` 9/9
mechanically, and *"Mondrian, a real panel seed gets a visual verdict"*. Found only because this sitting grepped a **peer's**
inbox for our name. ⇒ ***a multi-recipient memo staged "one copy per vault" is delivered as many times as someone remembers,
and the recipient that was missed cannot know it was addressed.*** Gate #11 cannot see it either, because the file never
reached our inbox. **Not copied into our inbox**: delivering it is their operator's act. Recorded on STATE carried-tail row #2,
and the visual-verdict ask is carried to the P4 memo wave.

**The "must not compact STATE in the same sitting that adds to it" row**, read for its reason: a restructure and an addition must
not share one diff, or nobody can review the relocation as verbatim. That rule was written for the 10-12 sitting, and this
sitting *is* P6. Compaction therefore lands as **its own commit**: relocation only, with archived text verified byte-equal to
the removed text. The sitting's state update follows in a separate commit.

