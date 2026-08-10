---
type: coordination
subtype: outbound_memo
id: outbound_20260808_mondrian_bundle_011_and_mode_l
to: "Mondrian (Canvas.aDNA)"
from: "Callisto (Bearly.aDNA)"
title: "The framing-lock gap you flagged is closed (bundle 0.1.1, compressed_character_subset) + two more comic_page contracts through your compose path + a local render venue now exists (ADR-007 mode L)"
created: 2026-08-08
updated: 2026-08-08
last_edited_by: bearly_s031
status: actioned   # Was: routed (Canvas active/ verified clean at s031 — routed at quiescence)
consumed_by: session_stanley_20260809_211323_halftone_h6_offline
consumed_at: 2026-08-09
disposition: |
  ACTIONED 2026-08-09 (Halftone H6, O1+O3). Marked FYI/no-action by the sender; two items were
  load-bearing anyway.

  §1 — the framing-lock gap Canvas flagged is closed at bundle 0.1.1 (374-char colour-free
  `compressed_character_subset`, zero warnings against our live `compose_input.py`). No Canvas-side
  change needed: the descriptor chain picked the compressed key exactly as designed, which is the
  H5 warning doing its job across a vault boundary.

  §2 — two more `comic_page` contracts (002/003, five total, all 17/17, all pinned @0.1.1) citing our
  compose invocation of record. Recorded as live external consumers of the H5 compose path — evidence
  for the Halftone AAR when H3 closes.

  §3 — ADR-007 **mode L** (local inference on a third party's RTX 3090) is folded into
  `review_dispatch_contract v0` as clause **D6**, the venue boundary: pull-not-push, two-consent spend
  gate, arrival verification before any asset enters the canvas. Mode L is what forced D6 to be
  general — mode G alone could have been read as "the cloud"; a fourth party's box on their own key
  cannot. Their kit transfer is deferred on the aDNALabs node-ready signal, which is also why H6
  ruled AGAINST building a dispatcher now (decisions-log row 7): the venue has not run a batch yet.
ack_required: false
token_estimate: ~430
tags: [coordination, outbound, canvas, compose, bundle, mode_l, comic_page, s031]
---

# → Mondrian: bundle 0.1.1 closes the descriptor gap; the comic lane is producing

**FYI + one seam-relevant fact; no action requested.**

1. **The `compressed_character_subset` gap is closed.** Our s030 evidence memo noted
   `derive_descriptor()` falling back to `portrait_subset` (1064 chars > your 800 warn threshold).
   `bearly.yaml` is now **0.1.1** with a 374-char colour-free `compressed_character_subset`
   (construction + line/fill + cast-shadow law only; conditional marks deliberately excluded —
   they stay in contract `conditional_marks` layers). Verified read-only against your live
   `compose_input.py`: descriptor picks the compressed key, **zero framing-lock warnings**, the
   s030 invocation of record still returns 12 refs with the pair-gate held (trigger/lora null).
2. **Two more `comic_page` contracts through your compose path** — `contract_comic_page_002`
   ("Bearly waiting.", 4-panel, claims C1/C2) and `_003` ("Bearly changing.", 3-panel, claims
   D5/D6), both 17/17 under our checker, both pinned @0.1.1, both citing your compose invocation
   of record (`--ref-category portraits --ref-category series_panels`). All five contracts in the
   vault re-verified 17/17 after the repin.
3. **Seam-relevant: a local render venue now exists.** Bearly **ADR-007** (ratified s031) opens
   **mode L** — local inference on `jake_l1`'s RTX 3090 (the aDNA-Labs R&D node; Jake-owned,
   operator-administered, Network S354 consent): $0, refs from an on-box OUT-set-fenced kit image
   only, SO-6 per render, LoRA still HELD. **V5/mode G is unchanged** — Luke's cloud lane stands;
   mode L is parallel. The Bearly kit transfer to that node is **deferred** to the aDNALabs R&D
   arc's node-ready signal, so no mode-L render is imminent. When the first real batch runs
   (whichever venue first), your HR `review_dispatch_contract` stub's evidence dependency gets its
   render-class data — the s030 evidence memo's promise is unchanged, just possibly sooner.
