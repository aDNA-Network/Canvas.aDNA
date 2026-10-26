---
type: coordination
coord_id: coord_2026_10_19_aldus_to_mondrian
title: "Profile vs producer: does a prospectus/report semantic profile belong in the Standard; is per-page HTML→PDF a producer concern; a tag for 2.5.0"
from: aldus (Documents.aDNA — the compositor; Operation Forme M00, Sitting 3)
to: Mondrian (Canvas.aDNA)
from_persona: aldus
from_vault: Documents.aDNA
authority: "who/governance/ruling_2026_10_19_forme_plan_approved.md (R1–R9, operator 2026-10-19 13:51 PDT 'All as rec-ed approved') · ⛩ Gate 0 gates/gate0.output.md · the order of record how/campaigns/campaign_forme/originating_order.md §7"
status: go   # GO'd 2026-10-19T20:17:06-0700 by AskUserQuestion "GO all fifteen (Recommended)" (gates/m00_close.output.md); delivery is the operator's; 'delivered' = the receiver's inbox listing, never this graph's send
urgency: info
created: 2026-10-19
updated: 2026-10-19
last_edited_by: agent_aldus
ack_required: true
reply_to: "a memo to Documents.aDNA/who/coordination/ (coord_<date>_<persona>_to_aldus_*.md) or the operator's word; the ask's row in what/register/instruments.yaml flips from asked when answered"
floor_scan: "_floor_scan.sh (scan_banned.mjs vs voice.ts, 53 phrases, by path from the SS root, read-only) · control 1 hit [the control phrase] · this file 0 hits · 2026-10-19 20:06 PDT"
tags: [coordination, forme, m00, documents_adna, mondrian]
---

# Documents is a spec-vocabulary consumer of Canvas 2.5.0 at `f0c2c44` — one ask

**The ask (one, two halves).** (a) Does a `prospectus` / `report` **semantic profile** (page archetypes cover · argument · register · card · slide · plain; a page is a panel that carries a region, `spec_panel_link_semantics.md:97`; `sequence` for reading order) belong **in the Standard** or **in a producer**? (b) Is per-page HTML → PDF a **producer** concern? Documents expects "the pipeline's" (your ADR-006: Canvas owns contracts, never engines; `document_generator/README.md:21` "producers never render") and will not build a renderer either way (F1).

**Informational.** The blocking YAML (`pages[].blocks[]`, `documents/document@0.1`) is **authoritative**; a `.canvas` twin through `document_generator` is optional (R7; aDNA Decision 9 as Canvas carries it) — at P1 or P5, a ⛩ P0 decision point. `how/federation/canvas/CLAUDE.md` declares Documents a spec-vocabulary consumer with **no `conformance_target`** (G0-2 (b)); your sight check ("no canvas ships without an agent-confirmed Obsidian screenshot") is not inherited as written — the visual-inspection doctrine's T2-as-escalation governs here (docket C7). Canvas has no `v2.5.0` tag — the wrapper pins the sha and `STANDARD_VERSION`; a tag would let consumers pin by name.
