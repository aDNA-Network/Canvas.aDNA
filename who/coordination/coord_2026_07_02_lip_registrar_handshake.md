---
type: coordination
title: "LIP numbering registrar handshake — Canvas.aDNA → aDNA.aDNA (Rosetta)"
status: pending_ack
direction: outbound
from_vault: Canvas.aDNA
from_persona: Mondrian
to_vault: aDNA.aDNA
to_persona: Rosetta
created: 2026-07-02
updated: 2026-07-02
last_edited_by: agent_mondrian
campaign: campaign_canvas_beacon
phase: B4
decision_ref: D3
tags: [coordination, cross-vault, lip, governance, registrar, numbering, d3, beacon]
---

# Coord memo — LIP numbering registrar handshake (Canvas.aDNA → aDNA.aDNA / Rosetta)

> **Staged, not delivered.** This is a Canvas-local coordination memo. It is **not** written into `aDNA.aDNA`
> (workspace Rule 10 / Git-Ops §6 — no silent cross-vault writes). Delivery to Rosetta is operator-gated. Until
> Rosetta acks, Canvas LIP numbering is **provisional-final** under the numbers inherited from the predecessor line.

## Context

At Operation Lodestar (Canvas.aDNA review, 2026-06-30) the operator resolved **D3**: the aDNA **LIP number line is a
global sequence** with **`aDNA.aDNA` as the number registrar**; a stewarding vault holds the *content* and
*ratification* of its own LIPs under their globally-assigned numbers.

The predecessor global registry lived at `lattice-labs/how/governance/lips/lip_registry.md`. `lattice-labs` was
**archived reader-only 2026-06-27** (→ `Archive.aDNA/lattice-labs/…`, Operation Drydock M05). That left Canvas's
governance ADR (`adr_003_standard_governance.md §2`) pointing at a dead path and its two in-review LIPs (LIP-0008,
LIP-0009) without a live home. **Operation Beacon Phase B4 (2026-07-02)** stood up a Canvas-local LIP home at
`Canvas.aDNA/who/governance/lips/` and migrated live copies of LIP-0008 + LIP-0009 there (archived originals left
reader-only). This memo formalizes the registrar half of D3.

## Proposal

1. **`aDNA.aDNA` (Rosetta) is the master registrar** of the global LIP number line — it arbitrates number assignment
   across vaults so the sequence stays collision-free and maintains (or points at) the cross-vault master index.
2. **Canvas.aDNA stewards its own LIPs** — content authorship, review, and ratification (Phase-0 FA authority) — under
   their **globally-assigned numbers**. Canvas keeps a Canvas-scoped `lip_registry.md` as a view; the master index is
   the registrar's.
3. **Inherited numbers stand.** LIP-0001…LIP-0009 were assigned in the predecessor `lattice-labs` line. Canvas retains
   **LIP-0008** (Derived Surfaces as Pure Metadata) and **LIP-0009** (Canvas as a First-Class aDNA Primitive) under
   those numbers; LIP-0001…0007 remain historical in the archived line (other domains). No renumbering.
4. **Next Canvas LIP number** is requested from the registrar at filing time (successor to the current global max).

## The ask (Rosetta)

- **Ack** the registrar role for `aDNA.aDNA`, or counter-propose (e.g. an `aDNALabs.aDNA` HQ home, or a dedicated
  standards registrar) — Canvas defers to the standard-owner's call on where the master line lives.
- Confirm whether the master index should be **rebuilt in `aDNA.aDNA`** (re-homing the archived `lattice-labs`
  registry as historical) or **referenced in place** from the archive.
- Confirm the **inherited-number retention** (0008/0009) and the **next-number** handshake mechanism.

## Status / dependency

- **PENDING ACK.** This is a cross-vault dependency. Canvas has proceeded with local stewardship under the inherited
  global numbers so the governance home is unblocked now; **global numbering is not treated as final until Rosetta
  acks.** Recorded as a `#needs-human` watch item at Beacon close.
- On ack: update `adr_003 §2` Amendment 1 + `who/governance/lips/lip_registry.md` + `lip_0001_lip_process.md`
  (registrar note) from "handshake pending" to the ratified arrangement.

## References

- `Canvas.aDNA/what/decisions/adr_003_standard_governance.md` §2 + Amendment 1 (2026-07-02)
- `Canvas.aDNA/who/governance/lips/` (the new home) · `lip_registry.md` · `lip_0001_lip_process.md`
- `Canvas.aDNA/how/campaigns/campaign_canvas_lodestar/` (D3 resolved) · `campaign_canvas_beacon/` (B4)
- Predecessor: `Archive.aDNA/lattice-labs/how/governance/lips/lip_registry.md` (reader-only)
