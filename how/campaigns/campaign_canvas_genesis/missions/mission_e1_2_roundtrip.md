---
plan_id: mission_e1_2_roundtrip
type: plan
title: "E1.2 — Round-trip converters (to_canvas / from_canvas / compute_sync_hash)"
owner: stanley
status: completed
campaign_id: campaign_canvas_genesis
campaign_phase: 1
campaign_mission_number: 5
mission_class: implementation
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
tags: [plan, campaign, keystone, execution, e1, canvas_std, roundtrip]
---

# Mission: E1.2 — Round-trip converters

**Campaign**: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|campaign_canvas_genesis]] (Operation Keystone) · **Phase**: E1 · **Mission**: E1.2 (depends on E0.2, E1.1)

> Implement `roundtrip.py` per `spec_roundtrip_protocol_v2`: `compute_sync_hash` (topology SHA-256, 16-hex),
> `to_canvas` (=`build`, forward source→view, deterministic, applies the `lattice` profile, injects
> `_reserved.sync`; **layout stays producer-side** — default geometry), `from_canvas` (=`read_back`, advisory
> view→source draft, drops view-only styling/positions, best-effort semantic-type recovery).

## Objectives
### 1. `compute_sync_hash` — **completed**
SHA-256 over sorted node ids + sorted `fromNode→toNode` pairs, truncated 16-hex (spec §3).
### 2. `to_canvas` (build) — **completed**
Source→conformant canvas: lattice-profile color/shape/node_type, explicit `toEnd`, `_reserved.sync`, default geometry.
### 3. `from_canvas` (read_back) — **completed**
Canvas→advisory source draft (`_draft: true`); topology + recoverable semantic types; positions dropped (view-authority).

## Notes
- Round-trip invariant tested: `compute_sync_hash(source) == compute_sync_hash(to_canvas(source))`; topology survives `from_canvas(to_canvas(source))`.
- Layout/positions are **producer-deferred** (inventory §B): `to_canvas` uses default geometry; real layout is CanvasForge's `layout_*`.

## AAR
- **Worked**: the lattice profile (E0.2) made `to_canvas` a direct table application; sync-hash is trivially deterministic.
- **Didn't**: full forward layout is out of scope (producer-side) — `to_canvas` emits default geometry, documented.
- **Finding**: round-trip fidelity = topology + semantic types; positions + visual styling are view-authoritative (the lossy boundary).
- **Follow-up**: E1.3 — `diff`/`merge`/`preserve_positions`.
