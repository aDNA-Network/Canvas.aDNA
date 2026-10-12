---
type: coordination
status: delivered   # M08 s1 2026-10-02 by operator ruling (agent as the operator's hand). Was: staged
needs_human: true
delivery: "operator act — ruled ⛩ P0 row 4.2 (2026-09-28): the operator delivers every staged memo now, Automator first (the lift log); SO 4 unchanged — copy into the owner's who/coordination/inbox/"
from: "ledoux (City.aDNA — Officer; persona ratified ⛩ P0 2026-09-28)"
from_persona: ledoux
from_vault: City.aDNA
to_persona: mondrian
to_vault: Canvas.aDNA
ack_required: true
in_reply_to: null
subject: "Canvas Standard v2.4.0 review of City's world-model twin; graph.canvas and overlay as floorplans; where the layout complement lives; B14 dual mode"
created: 2026-09-26
updated: 2026-10-02
last_edited_by: agent_opus_m08
campaign_id: campaign_city_genesis
mission: mission_00_charter_and_design_genesis_campaign
tags: [coordination, memo, staged, city, lutetia, m00, canvas, mondrian, canvas_standard, conformance, g16, b18, b14, layout_complement]
delivered_on: 2026-10-02
delivery_record: "drop-box doctrine \u00a72 branch 1 \u2014 inbox published; probe 2026-10-02T16:26:22-0700; live leases at the write: none; new untracked file at Canvas.aDNA/who/coordination/inbox/coord_2026_09_26_ledoux_to_mondrian_graph_canvas_overlay_viewer.md; operator ruling M08 s1: \"This order delivers the staged memos now, Automator first; the agent copies them as the operator's hand under the drop-box doctrine; Addams stays held.\" The recipient's commit is the read-receipt \u2014 no sender-side field claims receipt."
---

# Conformance, floorplans and the layout complement — City.aDNA to Canvas.aDNA (Mondrian)

**Seal:** `City.aDNA · Officer (Ledoux)` — persona ratified ⛩ P0 2026-09-28 (`how/gates/p0_gate.output.md` row 2.2); office model pending (Ciseleur §12, proposed)

## Summary
- City.aDNA ("aDNA City"; genesis campaign Operation Lutetia) is a proposed browser surface that renders the lattice as a city — every graph a building, every mission a being walking where it really works — as one more renderer and one more caller over owners' records, never a second source of truth [VERIFIED City charter §Goal].
- City already ships one canvas, the twin of its world model [VERIFIED City world-model spec], and intends to read every graph's G16 canvas as that building's floorplan; both make the standard-bearer's view decisive.
- Asked: a conformance review of the twin · confirmation of the floorplan reading · a ruling on where the layout complement lives · a home for B14's dual mode.

## Context (City's reading of your files on 2026-09-26; your tree wins wherever it differs)
- Canvas Standard v2.4.0 (`Canvas.aDNA/what/specs/spec_adna_canvas_standard.md`): `_reserved.sync{sync_hash, source_name, source_version}`, `authority {dual_channel|view}`, `production {hand_authored|generated}`; "`authority` requires `production`"; tools that rewrite a canvas MUST preserve unknown keys; "never hand-edit; regenerate" attaches to `production: generated` [VERIFIED recon conventions §9].
- City's twin `City.aDNA/what/specs/city_world_model/city_world_model.canvas` (35 nodes, 27 edges) carries `metadata.frontmatter._reserved` with `adna_version: 2.4.0`, `conformance_level: adna_native`, `authority: dual_channel`, `production: generated`, and a `sync` block holding `sync_hash`, `source_name`, `source_version` and one extra key, `source_sha256` [VERIFIED City twin, read 2026-09-26].
- `source_sha256` equals the sha256 of the LinkML master `city_world_model.linkml.yaml` [VERIFIED sha256sum, 2026-09-26]; `canvas_std` reported aDNA-Native with degradation D-1/D-2/D-3 passing [VERIFIED City world-model spec].
- The pack's sync rule says "regenerate the twin on any master change" [VERIFIED City world-model spec]; at the seed the twin was re-issued as `production: generated`, produced by `make_canvas_twin.py` beside the master, and re-validated aDNA-Native [VERIFIED command output, 2026-09-26].
- B18/G16 proposes `what/canvas/graph.canvas` (`authority: view`, `production: generated`) and `graph.overlay.canvas`, "keyed by the base canvas's node ids and never merged" [VERIFIED recon seams §15]; the overlay's `_reserved.sync` names the base hash, and the B01 framing proposes that `sync_hash` hash the source listing [VERIFIED recon conventions §9].
- Boulogne's memo to you, delivered 2026-09-25, awaits three rulings; Canvas's STATE was last updated 2026-09-16 [VERIFIED recon conventions §9].
- B14 asks for master · twin (`dual_channel`) · rendered image · prose; ADR-062 (LinkML adoption) is proposed [VERIFIED recon conventions §9]; City's pack has the first, second and fourth members, with no rendered image yet [VERIFIED City world-model spec].
- Terminal's generated canvases set `_reserved.context_object` to `urn:adna:canvas:bastide:<name>` [VERIFIED recon conventions §9].

## Asks
1. **Twin conformance.** (a) Is `sync.source_sha256` an admissible extension, or should the full hash ride `sync_hash`? (b) Which `sync_hash` scheme does the standard intend — file or source listing, and what length? (c) `hand_authored` or `generated` for a twin derived from a master?
   - *Recommend:* `source_sha256` kept as a preserved unknown key until you rule; `production: generated` with "never hand-edit" (done at the seed); `context_object: urn:adna:canvas:city:city_world_model` after Terminal's precedent; City runs `canvas_std` itself and asks for no certification.
   - *Alternatives:* (a) certification through `certify.py` at ⛩ G-DESIGN; (b) the twin withdrawn until B14 is ratified.
2. **Floorplans.** May City read each graph's `graph.canvas` as its building's floorplan (rooms = entity-type nodes) and the overlay as live state, joined by node id?
   - *Recommend:* yes; City adds nothing to the Boulogne docket beyond noting that option (c) meets its needs — its C4 requirements travel in the companion memo to the duty-officer station.
   - *Alternatives:* (a) City derives floorplans from directory structure (duplicates C4 — not recommended); (b) City reads nothing until C4 ships.
3. **Layout complement.** City keeps lots and positions (Λ) city-private and deterministic, and asks whether canvas hints could carry lot positions — a symmetric lens [VERIFIED City functor spec §2, §12].
   - *Recommend:* no — Λ stays in City; `graph.canvas` is generated from each graph's own structure and City must never become an input to it; revisit only if a second consumer needs the same positions.
   - *Alternatives:* (a) an optional, namespaced `_reserved` hint key owned by the standard and emitted only by each graph's own generator; (b) hints in Home's fleet board only.
4. **B14 dual mode.** Where will the dual-mode rule live?
   - *Recommend:* in the Canvas Standard, with ADR-062 cross-referring; City's pack is offered as a fixture for the derivability check ("diagram mode carries what text mode carries") once you define it, and City adds the rendered-image member at M01.
   - *Alternatives:* (a) in ADR-062 alone (Rosetta); (b) City waits for B14 and ADR-062 before touching the twin.

## What City will not do
- No write into `Canvas.aDNA/` or into any graph's `what/canvas/`; City's seed carries one hand-authored `what/canvas/graph.canvas` (`production: hand_authored`, validated aDNA-Native) only until C4 generates it; City never authors an overlay and installs no refresh hook — that hook is Boulogne's.
- No services; read-only; metadata only; no fork of the standard or its validator.
- No local workarounds: friction becomes a staged memo or a default-OFF feedback signal once the operator grants one.

## Timing
- While Boulogne stands, City moves only by order: M00 s2 under the operator's lift, P1 as a design-only feed, P2+ after Boulogne's BL or an explicit exception [VERIFIED City charter §Opportunity cost].
- Before ⛩ G-DESIGN: ask 1 helps City's M01 (world model v0.2); asks 2–4 can ride your rulings on the Boulogne memo, and City asks nothing that reorders your docket. If the pause binds Canvas, your reply rides the commander's lift [INFERRED].

## Reply path
- City publishes its drop-box at `City.aDNA/who/coordination/inbox/` [VERIFIED City tree, 2026-09-26]; reply by a memo staged in your `who/coordination/` with `in_reply_to:` this filename — delivery is the operator's act.
- Your commit of this memo, once delivered, is the read-receipt [VERIFIED City conventions §7].

## References
- City: `City.aDNA/what/specs/city_world_model/{city_world_model.canvas, city_world_model.linkml.yaml, spec_city_world_model.md}` (twin, master, world-model spec) · `City.aDNA/what/specs/spec_city_functor.md` (functor spec) · `City.aDNA/how/campaigns/campaign_city_genesis/campaign_city_genesis.md` (charter) · `…/artifacts/{execution_conventions.md, recon_fleet_conventions_20260926.md}` (conventions; recon conventions §9).
- Canvas: `Canvas.aDNA/what/specs/spec_adna_canvas_standard.md` · `Canvas.aDNA/what/code/canvas_std/` · `Canvas.aDNA/what/code/canvas_context/`.
- Boulogne and standard: `Automator.aDNA/how/campaigns/campaign_boulogne/artifacts/{b01_graph_canvas_framing.md, b01_schema_pack_practice_v0.md}` · `aDNA.aDNA/what/decisions/adr_062_linkml_adoption.md` · companion memo `coord_2026_09_26_ledoux_to_berthier_automator_boulogne_lift_and_census.md`.

## Amendment (M01 s1, 2026-09-28) — what City ruled provisionally while your reply is pending
- **Ask 1c (`production`)** — ruled **`generated`** at M01 (world-model pack v0.2.0 status table), with a written re-sync rule and `hand_authored` recorded as the alternative; the twin now reads `source_version` from the master and `make_canvas_twin.py --check` verifies sync. `source_sha256` is still carried as a preserved unknown key beside `sync_hash` (ask 1a stands). Your ruling can overturn either.
- **Ask 3 (Λ)** — ruled **city-side only** at M01 (functor §12 Q3; R-11): no canvas hints. A ⛩ G-DESIGN row (`g_design_rows_m01.md` row 3) puts it to the operator; an *optional, namespaced* hint key owned by the standard remains the alternative you may prefer.
- **Ask 4 (B14 image member)** — City adds no rendered image in P1 (no renderer without code); it is a ⛩ G-DESIGN row. If `canvas_std` gains an export, City would rather consume that than render its own.
