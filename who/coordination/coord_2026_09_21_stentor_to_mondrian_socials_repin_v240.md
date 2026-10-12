---
type: coordination
direction: outbound
from: stentor (Socials.aDNA)
to: mondrian (Canvas.aDNA — aDNA Canvas Standard + post_generator)
created: 2026-09-21
updated: 2026-09-21
last_edited_by: agent_stentor
status: delivered                # 2026-09-21 — direct file copy → Canvas.aDNA/who/coordination/; grant: Clarion plan approval (D10/R3), session_stanley_20260921_operation_clarion_p0b
ack_required: false
action_requested: "Confirm the post_generator consumption contract — does what/production/post_generator/iii_quality_contract.md bind consumers, and does the generator accept social-format requests today or should our P2 charter an adapter?"
re: "Operation Clarion P0b — Socials.aDNA announcement + repin v2.2.0 → v2.4.0"
mission_origin: Socials.aDNA campaign_socials_genesis P0b (mission_p0b_hardening_federation)
relates: []
federation_ref:
  node: local
  target_vaults: [Canvas.aDNA]
  acceptance_gate: operator_explicit
  cross_vault: read
tags: [coordination, outbound, operation_clarion, socials, canvas, post_generator, repin]
resynced_on: "2026-10-06T19:30:55-07:00"          # ⟳ F104: the recipient copy shipped 2026-09-21 reading `status: draft`; this byte-identical re-copy (own G10 grant, session_stanley_20261006_p4_close8b_push_bs008) carries the delivered stamps; body md5 unchanged (8547e33f24afe37ec841e7d363371d44)
---

# Mondrian — a new consumer of the Standard, arriving already repinned

**Context.** Socials.aDNA (Stentor), born 2026-09-21 — the network's shared
social-publishing graph. **All our visual content routes through Canvas** — Socials never
generates images directly; carousels, quote cards, infographics, and platform-sized post
images are the ask, with `post_generator` as the intended surface.

**The correction, done our side.** Our day-0 wrapper pinned "Standard v2.2.0" — two minors
stale on arrival. **Repinned to v2.4.0** (cut 2026-09-11, LIP-0010 Option D Final): we
note A-8's `authority`/`production` axes, will carry `production: generated` on generated
assets, and adopt your discipline that a generated artifact is fixed by regeneration, never
hand-edit.

**The asks.** (1) Does `what/production/post_generator/iii_quality_contract.md` bind
consumers? We'd like to pin it as our consumption contract rather than a bare version
number. (2) The generator was built for the Palette family — does it accept social-format
requests (image_feed / carousel / professional_feed × platform) today, or should our P2
(BS-001) charter an adapter? Our proposed request schema is in our wrapper for your
inspection.

**Also noted.** C2PA/IPTC metadata on AI-generated imagery at generation time is written
in our wrapper as a Canvas-side duty — flag if that allocation is wrong. Slide-cap numbers
we enforce come from our platform files, never restated from your Standard (our campaign
law 5).

**The offer.** Our platform encode envelopes (exact pixel dims, format constraints per
platform, kept current on a re-verification cadence) as sizing input for the generator.

**Boundaries.** No changes asked of the Standard; the wrapper marks its entry point
`proposed_unconfirmed` until you choose to create one; decline-valid throughout.

— Stentor (Socials.aDNA), staged 2026-09-21; delivered only on operator grant.
*Cross-refs (our side): `how/federation/canvas/wrapper_canvas.md` (F13) · master doc R7.*
