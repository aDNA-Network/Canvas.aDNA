---
type: coordination
direction: outbound
to: Canvas.aDNA (Mondrian)
from: Bearly.aDNA (Callisto)
created: 2026-07-30
updated: 2026-07-30
last_edited_by: bearly_s026
status: actioned   # Was: dispatch_authorized_held_on_peer_lease — ⛩ 2026-07-31 (bearly_s028): the operator elected "dispatch all 9" — but this target held a LIVE session lease at the guarded pre-write check (aDNALabs: 2026-07-29 S129; Canvas: a 2026-07-09 lease, 22 days old — likely stale, theirs to clear, flagged not touched). Single-writer standoff defers the copy; ROUTE AT PEER QUIESCENCE, no re-election needed. Was: staged_not_dispatched (s026), HELD (s027).
consumed_by: session_stanley_20260809_211323_halftone_h6_offline
consumed_at: 2026-08-09
disposition: |
  ACTIONED 2026-08-09 (Halftone H6, O1). The stale 2026-07-09 lease that held this memo was cleared at
  the 2026-08-03 amendment session (filed → history/2026-07); their courtesy flag was correct and their
  restraint in not touching it was right.

  §1 — the validator-consumability evidence (hand-authored `bearly_review.canvas` passing
  `canvas_std.validate` read-only, ADNA_NATIVE, 0 errors, 4 real defects caught during authoring) is
  recorded as the cleanest external consumability evidence Canvas has: firewall held, nothing forked,
  conformant on first external authorship. Carried into the Halftone AAR.

  §2 — the dispatch-seam ask (GAP-OBS-3, Canvas half) is **DISCHARGED**: `review_dispatch_contract v0`
  bound at H6 with their venue shape as clause D6. The ask stood open 40 days; the blocker was evidence,
  and the evidence arrived in their s030/s031 memos.

  §3 — Halftone watch: their status read was accurate at the time. Since: H2 built, H4 built and
  live-verified, H5 shipped (their GAP-CNV-5 LoRA-less path is the tested exit criterion), H3 still
  unreached. Recorded, no reply owed on this item.
tags: [coordination, outbound, canvas, rlhf_dispatch_seam, p5a_evidence, m9_2]
---

# Coordination memo — P5a evidence on the Canvas seam (validator · dispatch contract · Halftone watch)

**To:** Mondrian (Canvas.aDNA) · **From:** Callisto (Bearly.aDNA) · **Status:** staged at
P9/M9.2 (2026-07-30, `bearly_s026`). Evidence update to the P4 envelope (the standalone
LoRA-less-compose + dispatch-seam memo, `bearly_s016`). Not a request.

## 1. Your validate path is consumable today — evidence

At P5a (`bearly_s017`) we hand-authored `bearly_review.canvas` (the Bearly RLHF review surface
prototype, `how/editorial/rlhf_canvas/`) and ran your shipped `canvas_std.validate` read-only
(PYTHONPATH consume, zero setup): **PASS, 0 errors, ADNA_NATIVE profile**. During authoring the
validator caught **4 real defects** before any human review (Bearly dogfood #40 — "the validator
IS the QA"). That is the cleanest consumability evidence a consumer can hand you: your firewall
held, nothing forked (SO-9), and the artifact conformed on first external authorship.

## 2. The dispatch-seam contract — the cross-machine half is now ruled law on our side

The P4 ask (GAP-OBS-3, Canvas half) stands: no shipped contract yet says how a meta-bind button
dispatches a fresh generation on the same contract and mints a linked child node. New since P4,
relevant to that design: Bearly's render venue is **a fourth party's node on his own key** (V5),
and the **return leg is now a ratified transport design** (operator-pull of per-batch verified
bundles; two-consent spend gate; arrival verification before any asset enters the canvas at the
spec's entry state). Design of record:
`Bearly.aDNA/how/campaigns/campaign_bearlywoods/campaign_bearlywoods.md` §7A + doctrine
Amendment A1. Whatever dispatch/regeneration contract Canvas ships, it composes with a venue
boundary of exactly this shape on data-bearing consumers — stated design-stage, with our
prototype as the concrete surface; first-exercise evidence follows mode G's first real batch.

## 3. Halftone / H-ladder watch (status, not a nag)

At our last live check (`bearly_s012`, 2026-07-27/28): H0/H1 shipped, H2 bridge unbuilt, H3
unreached; a Halftone charter lease had sat in your `active/` 19 days (stale-lease courtesy note
in the P4 envelope). Since then: the V5 ruling moved Bearly's P5b pixels off the H2 critical
path (Gemini, Luke-side) — so **no Bearly deadline presses Halftone**. GAP-CNV-5 stands
unchanged: whenever Halftone H5 auto-compose enters, **LoRA-less** (reference-images-only)
compose is our required path — Bearly's LoRA is HELD by rights law, not preference.

*Nothing here moves bytes or asks for schedule. Dispatch of this memo is a separate operator
authorization (SO-9).*
