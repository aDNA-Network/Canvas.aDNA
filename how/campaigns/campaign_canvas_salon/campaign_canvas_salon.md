---
campaign_id: campaign_canvas_salon
type: campaign
title: "Operation Salon — canvas-as-surface (context-object + interface legs)"
owner: stanley
status: completed
completed: 2026-06-22
phase_count: 6
mission_count: 6
estimated_sessions: "6-10"
calibrated_sessions: "5-8"
estimation_class: governance-broad
priority: high
predecessor: campaign_canvas_palette
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
status_history: "planning (2026-06-22 open) → active (2026-06-22 P0 ratified) → completed (2026-06-22 P5 close)"
tags: [campaign, canvas, salon, surface, context_object, interface, genesis]
---

# Campaign: Operation Salon — canvas-as-surface

## Goal

Prove the two unproven legs of the Canvas thesis. When this campaign completes, a canvas is demonstrably more than
an output primitive: **(leg 2 — context object)** an agent can *load and traverse* a canvas as a first-class context
object — a navigable graph of components, panels, and refs — **without rendering it**; and **(leg 3 — interface
surface)** the human↔AI / human↔human interaction-surface leg has a **ratified spec** and a **fixed boundary** (ADR)
against the neighbouring surfaces (ISS, Astro, Terminal) and the future cross-surface routing layer (OIP). The thesis's
three legs are then all either **proven** (1 output ✅, 2 context-object) or **specified-and-bounded** (3 interface).
The campaign is deliberately a *planning/proving* arc (the Cartography model), not an open-ended build: it produces the
boundary ADR, the leg-2 loading protocol + a working pilot, the leg-3 spec, and a follow-on charter for any leg-3 build.

## Context

Operation Palette closed 2026-06-22 with the **output family complete** — 7 in-vault producers green on `canvas_std`
(brief · deck · document · diagram · comic · letter · post), cross-producer sweep 305 passed, `canvas_std` firewall
git-diff 0. That proves **leg 1** of the three-leg thesis stated in [[what/decisions/adr_000_canvas_identity|ADR-000]]
§Context: a canvas is *(a)* a near-universal **output primitive**, *(b)* a first-class **context object**, and *(c)* a
**human↔AI / human↔human interaction surface**. Legs (b) and (c) remain unproven — they are the remaining frontier of
the vault's reason for being.

Exploration at this campaign's open surfaced two structural facts that shape the work:

- **Leg 2 has a ratified spec but no "how".** [[what/specs/spec_context_object|spec_context_object.md]] (D7) defines the
  context-object *metadata* (`_reserved.context_object`: `id` / `version` / `refs` / `summary`) and states a canvas
  **SHOULD** be loadable/traversable as context *without rendering* — but it does **not** define the agent
  loading/traversal protocol itself. The "how" is the gap.
- **Leg 3 is greenfield.** No interface-surface spec exists. ADR-000 names "the **OIP/interface thesis**" but that
  document is **not in this vault**, and a *future* `aDNA.aDNA` **OIP-unification campaign**
  (`idea_campaign_operator_interaction_patterns_unification.md`) will own the **cross-surface routing** decision-tree
  (when to use Canvas vs ISS vs Terminal vs web). Canvas must therefore define **what it owns** as a surface
  **without pre-empting** that routing layer — hence a boundary ADR is the *first* deliverable.

The operator chose canvas-as-surface (over more-producers and v2.1.0-prep) as the next strategic direction. Approved
plan + retrospective: `~/.claude/plans/please-read-the-claude-md-sleepy-aho.md`. Predecessor close + the original
deferral of this campaign: [[how/campaigns/campaign_canvas_palette/campaign_canvas_palette|Operation Palette]]
§Completion Summary.

## Scope

### In Scope

- **Boundary ADR** (`adr_006_canvas_surface_boundary`) — what canvas-as-surface owns vs **ISS / Astro / Terminal** and
  the future **OIP** routing layer; modeled on the LP↔Canvas three-way stewardship split.
- **Leg-2 loading/traversal protocol** — a spec for *how* an agent loads a canvas as a context graph (resolve
  `context_object` metadata + `refs` + `summary`; parse panel/component/edge structure into a traversable graph;
  resolve wikilinks in-vault + `federation_ref` cross-vault) — the "how" missing from `spec_context_object.md`.
- **Leg-2 reference impl + pilot** — a canvas-as-context loader, and a pilot that loads an **existing producer
  `.canvas`** (e.g. a `document_generator` whitepaper) as a context graph **without rendering**.
- **Leg-3 interface-surface spec** (`spec_interface_surface`) — greenfield: the interaction model (human↔AI /
  human↔human), interaction primitives, what "surface" denotes, and a conformance contract.
- **Cross-vault coordination** — heads-up memos to `aDNA.aDNA` (OIP) and Argus/ISS so the leg-3 spec stays coherent
  with the routing layer and the gate surface.

### Out of Scope

- **Cross-surface routing** (when to use Canvas vs ISS vs Terminal vs web) — owned by the future `aDNA.aDNA`
  OIP-unification campaign. This campaign defines *what a canvas-surface is*, not *when to choose it*.
- **HTML decision-gate authoring/rendering** (ISS) · **web publication** (Astro) · **CLI/TUI orchestration**
  (Terminal) · **image rendering** (ComfyUI). Substrate-neutrality test (C8).
- **Canvas-as-primitive elevation** (Δ2 / LIP-0009) — stays on its own LIP track; this campaign rides `_reserved`,
  no core-primitive change.
- **A production leg-3 runtime build** — deferred to a follow-on charter; the P4 POC (if taken) is a minimal proof, not
  a runtime.
- **Any edit to `canvas_std` schema/validators** unless a *ratified* spec requires it — the two-shelf firewall holds
  (see D6).

### Subsumes

| Plan/Mission | Status at Subsumption | Tasks Absorbed By |
|-------------|----------------------|-------------------|
| (none) | — | — |

## Phases & Missions

> Missions are authored thin and only at phase entry (SO-3 context budget). Only P0 is authored at open.

### Phase P0: Charter, boundary ADR & decision record  *(this session)*

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| 1 | P0.1 — Charter + boundary ADR + decision record | 1 | — | completed |

**Phase exit gate (P0→P1, HUMAN)**: the operator ratifies the **P0 decision record** (8 decisions — codename ·
planning-vs-build · leg sequencing · leg-3 depth · leg-2 spec home · leg-2 impl/firewall posture · boundary ADR ·
coordination posture) **and** `adr_006`. That ratification **activates** the campaign (`status: active`) and opens P1.

### Phase P1: Leg-2 loading/traversal protocol (spec)

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| 2 | P1 — Context-loading protocol spec | 1-2 | P0 | completed |

**Phase exit gate**: a spec for the agent loading/traversal protocol is authored and operator-ratified (home per D5:
new `spec_canvas_context_loading.md` keeping `spec_context_object.md` stable, or amend in place).

### Phase P2: Leg-2 reference impl + pilot

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| 3 | P2 — Canvas-as-context loader + pilot | 2-3 | P1 | completed |

**Phase exit gate**: the loader loads an existing producer `.canvas` as a context graph **without rendering**; tests
green; **`canvas_std` firewall git-diff 0** (loader placement per D6). Leg 2 is **proven**.

### Phase P3: Leg-3 interface-surface spec

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| 4 | P3 — Interface-surface spec (greenfield) | 1-2 | P0 (boundary), P2 | completed |

**Phase exit gate**: `spec_interface_surface.md` ratified **or** explicitly deferred (if the external OIP/interface
thesis doc cannot be acquired); coordination with `aDNA.aDNA` (OIP) + ISS recorded. **✅ MET** — ratified 2026-06-22; D8
memos filed.

> **P3 COMPLETE 2026-06-22** (`mission_p3_interface_surface_spec`, completed). The external OIP/interface-thesis
> dependency **resolved by proceeding first-principles** (operator, plan-mode): the doc does not exist (a future
> `aDNA.aDNA` OIP-unification deliverable), so the spec was authored **Canvas-scoped v1** — grounded on `adr_006` + the
> proven leg-2 model + ISS as exemplar — re-anchoring on a future `v1.x` OIP pass; **not** deferred.
> [[../../../what/specs/spec_interface_surface|spec_interface_surface.md]] **ratified** (operator, "Approved", at all 9
> default open-question resolutions); the `I-*` conformance family folded into `spec_conformance_suite.md` §4.1
> (additive/optional; `interaction_version 1.0`; Standard-version cut deferred). D8 memos filed. **➤ The Canvas
> three-leg thesis is now COMPLETE** — leg 1 (output) + leg 2 (context object) **proven**, leg 3 (interface surface)
> **ratified**. **⛔ HELD at the P3→P4 gate** (P4 = stretch POC; not opened).

### Phase P4 *(stretch)*: Leg-3 proof-of-concept

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| 5 | P4 — Minimal canvas-native interaction loop | 1-2 | P3 | completed |

**Phase exit gate**: a minimal interaction loop demonstrated (operator annotates a canvas → agent reads it as context →
responds), **or** the operator decides to charter a leg-3 build follow-on instead. Taken only if budget remains (D4).
**✅ MET** — the loop is demonstrated (the `read → act → re-read` proof + the runnable on-disk demo); `canvas_std`
firewall git-diff 0.

> **P4 COMPLETE 2026-06-22** (operator chose "build P4" at the P3→P4 gate; mission `mission_p4_interaction_poc`,
> `completed`). The stretch POC is built as a **read-only extension of `canvas_context`** (spec §10.2): the new additive
> sibling `interaction.py` *composes* the leg-2 `ContextGraph` (an `InteractionSurface` *has-a* `ContextGraph`) + a pure
> append-only `apply_response` fold (IX5/IX6) + the `I-1/I-2/I-3/I-D` realizations (first code realization of the `I-*`
> family, housed in the consumer) + an interaction-bearing golden (all 4 affordance kinds) + the runnable `read → act →
> re-read` demo. **The `read → act → re-read` loop closes live** — read an annotated canvas as context (leg-2 load, no
> rendering) → agent responds → re-read shows the turn complete. **Verified:** `canvas_context` **50 passed** (28 leg-2 +
> 22 leg-3); `canvas_std` **82/10 unchanged**; `ruff` clean; CLI `adna_native [OK]`; **firewall git-diff 0**. **➤ All
> three thesis legs now exercised** (1+2 proven, 3 ratified *and* demonstrated). **⛔ HELD at the P4→P5 gate** — P5
> (close) is the operator's separate call. Approved plan: `~/.claude/plans/please-read-the-claude-md-goofy-whistle.md`.

### Phase P5: Close

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| 6 | P5 — Validation, AAR, follow-on charter | 1 | P2, P3 (P4 if taken) | completed |

**Phase exit gate**: campaign Completion Summary + AAR filed; doc currency done; follow-on charter (any leg-3 build)
written; `status: completed`. **✅ MET 2026-06-22.**

> **P5 COMPLETE 2026-06-22 — CAMPAIGN CLOSED** (`mission_p5_close`, `completed`; session
> `session_stanley_20260622_175728_salon_p5_close`). Validation re-confirmed (`canvas_context` 50 · `canvas_std` 82/10 ·
> ruff clean · CLI `adna_native [OK]` · firewall git-diff 0); Completion Summary + Campaign AAR filed; the follow-on
> authored as a **backlog idea stub** (`how/backlog/idea_campaign_leg3_interface_runtime.md` — operator-chosen depth);
> patterns graduated → `what/context/context_canvas_surface_legs.md`; doc currency done (STATE + root CLAUDE.md). No
> producer example shipped → `iii/` review **N/A**. Campaign `status: completed`. **Operator-gated (outward):** commit +
> push HELD (Git-Ops §3).

## Decision Points

| # | When | Decision | Status |
|---|------|----------|--------|
| D1 | P0→P1 gate | Codename / slug (Operation Salon / `campaign_canvas_salon`) | ratified 2026-06-22 |
| D2 | P0→P1 gate | Campaign type (planning, Cartography-model) | ratified 2026-06-22 |
| D3 | P0→P1 gate | Leg sequencing (leg-2 first, then leg-3 spec) | ratified 2026-06-22 |
| D4 | P0→P1 gate | Leg-3 depth this campaign (spec-only; P4 POC stretch; build → follow-on) | ratified 2026-06-22 |
| D5 | P0→P1 gate | Leg-2 spec home (new `spec_canvas_context_loading.md` vs amend `spec_context_object.md`) | ratified 2026-06-22 — new spec |
| D6 | P0→P1 gate | Leg-2 impl placement + firewall posture (sibling `canvas_context` vs extend `canvas_std`) | ratified 2026-06-22 — sibling (firewall preserved) |
| D7 | P0→P1 gate | Boundary ADR `adr_006` (accept/edit the ISS·Astro·Terminal·OIP boundary) | ratified 2026-06-22 |
| D8 | P0→P1 gate | Cross-vault coordination posture (heads-up memos now vs at P3) | ratified 2026-06-22 |

All eight are recorded with doctrine-aligned defaults in `missions/artifacts/p0_decision_record.md`.

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| Leg-3 is greenfield **and** depends on an external "OIP/interface thesis" doc not in the vault | High → **RESOLVED 2026-06-22** | Doc confirmed non-existent (future `aDNA.aDNA` OIP deliverable). Operator chose **proceed first-principles** over defer: spec authored **Canvas-scoped v1** (grounded on `adr_006` + proven leg-2 + ISS exemplar), re-anchors on a future `v1.x` OIP pass; D8 memos filed at P3 open. Mitigation taken: spec-only (D4) + coordinate early (D8). |
| Boundary creep vs ISS / Astro / Terminal / OIP | Medium | `adr_006` fixes the boundary **first** (P0), modeled on the LP↔Canvas seam; heads-up coordination memos |
| Touching the immutable `canvas_std` (regression across 82 tests + 7 producers) | High | Default keeps the firewall: leg-2 loader is a **new sibling package** importing `canvas_std` read-only (D6); git-diff 0 verified at every gate |
| Δ2 / LIP-0009 (canvas-as-primitive) entanglement | Low | Legs 2 & 3 ride `_reserved`; the primitive question stays on its own LIP track (out of scope) |
| Scope too large to gate cleanly | Medium | Cartography-model planning campaign; thin missions authored at phase entry; HOLD at every gate (SO-1) |
| Leg-2 "load without rendering" proves harder than the metadata implies | Medium | Pilot against an **existing** producer `.canvas` (known-good fixture), not a synthetic one; P1 spec precedes P2 impl |

## Verification Strategy

### Per-Mission

| Check | Method | Gate? |
|-------|--------|-------|
| SITREP filed | Session closure protocol | Yes |
| AAR produced | 5-step AAR protocol | Yes |
| Deliverables validated | AAR scorecard (validated/total) | Yes |
| Files committed | Git status clean | Yes |

### Per-Phase

| Check | Method | Gate? |
|-------|--------|-------|
| All mission AARs are GO | Review AAR readiness | Yes |
| Phase exit criteria met | Campaign doc phase exit gate | Yes — user approval |
| **`canvas_std` firewall** | `git status -s -- what/code/canvas_std/` clean (unless D6 lifts it) — pathspec form; canvas_std is part of Canvas.aDNA's git, not a nested repo | Yes — at every gate |
| Risk register updated | Campaign doc risk register | No — recommended |
| Scope changes documented | Campaign doc scope section | Yes |

### Campaign Validation

| Check | Method |
|-------|--------|
| Cross-file coherence | All new specs/ADRs referenced from their AGENTS.md indices |
| New spec indexed | `what/specs/AGENTS.md` updated for any new spec |
| New ADR indexed | `what/decisions/` ADR sequence coherent (`adr_006`) |
| Context graduation run | `skill_context_graduation` on campaign deliverables |
| STATE.md updated | Campaign status reflected in operational state |

## Timeline

| Phase | Missions | Sessions |
|-------|----------|----------|
| P0 Charter + boundary + decisions | 1 | 1 |
| P1 Leg-2 loading spec | 1 | 1-2 |
| P2 Leg-2 impl + pilot | 1 | 2-3 |
| P3 Leg-3 interface spec | 1 | 1-2 |
| P4 Leg-3 POC *(stretch)* | 1 | 1-2 |
| P5 Close | 1 | 1 |
| **Total** | **6 missions** | **6-10 sessions** |

## Notes

- **Boundary model.** `adr_006` reuses the structure of the **LP↔Canvas seam** countersign
  (`who/coordination/coord_2026_06_13_mondrian_countersign_lp_canvas_seam.md`): a stewardship split (Canvas owns the
  *standard/contracts*, not engines/runtimes/routing) + a heads-up coordination courtesy on seam-touching changes.
- **Leg-2 spec stability.** Default (D5) is a **new** spec so the ratified `spec_context_object.md` stays stable; the
  new spec *references* it and supplies the loading/traversal protocol it left unspecified.
- **Firewall posture.** Default (D6) keeps `canvas_std` frozen-since-Keystone; the loader is a new sibling. The
  alternative (extend `canvas_std` as a sanctioned reference-impl capability) deliberately lifts the firewall and is the
  single biggest technical-governance call — hence it is an explicit operator decision, not an agent assumption.
- **OIP forward-reference.** The leg-3 spec must define *what a canvas-surface is* without encoding *when to route to
  it*; the routing decision-tree belongs to the future `aDNA.aDNA` OIP-unification campaign. Keeping these separate is
  what prevents this campaign from over-reaching into cross-vault territory.

## Completion Summary

**Closed 2026-06-22** (P5, `mission_p5_close`). Operation Salon exercised the two under-proven legs of the three-leg
Canvas thesis (ADR-000): **leg 2 (context object) PROVEN**, **leg 3 (interface surface) RATIFIED + POC-demonstrated**.
With leg 1 (output) already proven by Palette, all three legs are now either proven (1, 2) or specified-and-demonstrated
(3). The `canvas_std` firewall held **git-diff 0 at every phase gate**. Validation at close: `canvas_context` **50
passed** (28 leg-2 + 22 leg-3) · `canvas_std` **82 passed / 10 skipped** · `ruff` clean (both) · CLI `canvas-std 2.0.2`
→ interaction golden `adna_native [OK]` (D-1/D-2/D-3). No producer example shipped this campaign → structural `iii/`
review **N/A**.

### Deliverables
- **P0** — `adr_006_canvas_surface_boundary` (ratified): fixes what canvas-as-surface owns vs ISS / Astro / Terminal /
  the future OIP routing layer; + the 8-decision P0 record (`missions/artifacts/p0_decision_record.md`, D1–D8 ratified
  at doctrine-aligned defaults).
- **P1** — `what/specs/spec_canvas_context_loading.md` (ratified): the leg-2 loading/traversal protocol — abstract
  context-graph model + normative **L1–L7** load pipeline + traversal read-contract + resolver interface + conformance
  (the "how" the ratified `spec_context_object.md` left unspecified).
- **P2** — `what/code/canvas_context/` leg-2 reference loader (a **new sibling** importing `canvas_std` read-only via
  pythonpath, D6 firewall preserved) + pilot: loads a real producer `.canvas` (whitepaper, 32 nodes / 23 edges) as a
  navigable `ContextGraph` **with no render pipeline invoked** (PIL/cairosvg never imported); 28/28. **Leg 2 PROVEN.**
- **P3** — `what/specs/spec_interface_surface.md` (ratified): the greenfield leg-3 interface-surface contract bounded by
  `adr_006` (no routing / no engine / no transport; rides `_reserved.interaction`); the `read → act → re-read` loop +
  five primitives (anchor · affordance · response · surface state · turn); the `I-*` conformance family folded into
  `spec_conformance_suite.md §4.1`. **Leg 3 RATIFIED.**
- **P4** *(stretch)* — `what/code/canvas_context/interaction.py` v0.2.0: the leg-3 interaction-loop POC — a read-only
  extension *composing* the leg-2 `ContextGraph` (reader) + a pure append-only `apply_response` view-fold (reducer) +
  the first code realization of `I-1/I-2/I-3/I-D` (in the consumer, reusing `validate_anchors` + `strip`/`validate`) +
  an interaction-bearing golden (all 4 affordance kinds) + a runnable on-disk `read → act → re-read` demo; 50 passed
  (28 + 22). **Leg 3 DEMONSTRATED live.**
- **Cross-vault** — D8 coordination memos to `aDNA.aDNA` (OIP) + Argus/ISS
  (`who/coordination/coord_2026_06_22_mondrian_to_{oip,iss}_canvas_interface_seam.md` + the salon-open heads-up).
- **Close artifacts** — the follow-on backlog idea stub (`how/backlog/idea_campaign_leg3_interface_runtime.md`) + the
  graduated context guide (`what/context/context_canvas_surface_legs.md`).

### Descoped
- **The leg-3 *runtime* build** — deferred to the follow-on (the P4 POC is a minimal proof, not a runtime).
- **Cross-surface routing** (when to use Canvas vs ISS vs Terminal vs web) — owned by the future `aDNA.aDNA`
  OIP-unification campaign; this campaign defines *what* a canvas-surface is, not *when* to choose it.
- **Capture runtime · renderer · transport** — fenced out by `adr_006 §2`.
- **The governed `.lattice.yaml` round-trip write** — the POC's `apply_response` is a view-only append-fold;
  the authoritative write stays in `spec_roundtrip_protocol_v2`.
- **Wiring `I-*` into the `canvas_std` harness** — the family is realized in the consumer; harness-wiring + the formal
  Standard-version cut for `interaction_version 1.0` are deferred to the runtime build.
- **Canvas-as-primitive** (Δ2 / LIP-0009) — stays on its own LIP track; legs 2 & 3 rode `_reserved`, no core change.

### Key Findings
- **Compose-not-extend kept the firewall clean for free.** Making `canvas_context` (and the leg-3 `InteractionSurface`)
  a *has-a* consumer of `canvas_std` rather than an extension meant the immutable tree was never touched — git-diff 0
  held at every gate without special effort.
- **A view-only append-fold lets a POC prove the loop honestly.** An honest interaction loop wants a write; modelling
  `apply_response` as a pure append-only fold that advances the *view* (not the authoritative `.lattice.yaml`) closed
  the `read → act → re-read` loop live while keeping the governed round-trip write cleanly out of scope.
- **Leg 3 was authored first-principles.** The external "OIP/interface thesis" doc ADR-000 leaned on to ground leg 3
  **does not exist** (a future `aDNA.aDNA` deliverable). The spec was authored Canvas-scoped v1 (grounded on `adr_006` +
  the proven leg-2 model + ISS as exemplar), designed to re-anchor on a future `v1.x` OIP pass via `interaction_version`
  semver — additive, not re-litigated.
- **The leg-2 gap was the loading protocol, not the metadata.** `spec_context_object.md` defined the context-object
  metadata but not *how* an agent loads/traverses it; the new `spec_canvas_context_loading.md` + the sibling loader
  filled it, and "load without rendering" held against a real producer output.

### Scope Changes
- **Thin missions at phase entry (SO-3).** Only P0 existed at open; P1–P4 were authored at their phase gates, and
  `mission_p5_close` (mission 6) was authored at the close.
- **P4 stretch taken.** D4 scoped the P4 POC optional; the operator chose "build P4" at the P3→P4 gate.
- **Follow-on depth = backlog idea stub** (operator decision at P5), not a full charter directory.

### Follow-Up Campaigns
- **`how/backlog/idea_campaign_leg3_interface_runtime.md`** — the deferred leg-3 interaction **runtime** build (full
  runtime + `I-*` into the `canvas_std` harness + the formal Standard-version cut + the governed round-trip write + the
  `v1.x` OIP re-anchor). Graduates to a campaign on operator commit; carries a cross-vault dependency on the future
  `aDNA.aDNA` OIP-unification campaign + the ISS seam.
- **External tracks (unchanged):** LIP-0008/0009 FA review closes **2026-06-27** → v2.1.0 (LIP-0008 A-5 relaxation;
  LIP-0009 records the canvas-as-primitive deferral); **PT P5** (Hestia) — `canvas_core` relocation + the ~8
  consumer-wrapper refederations + shim retirement (2027-06-13).

## Campaign AAR

- **Worked**: the Cartography-model planning arc — boundary ADR first, spec-before-impl, compose-not-extend — exercised both under-proven legs (2 PROVEN, 3 RATIFIED + POC-demonstrated) with the `canvas_std` firewall git-diff 0 at every gate.
- **Didn't**: the external OIP/interface-thesis doc ADR-000 leaned on to ground leg 3 doesn't exist; surfaced at P3, resolved by proceeding first-principles (Canvas-scoped v1 + an `interaction_version` re-anchor seam) rather than stalling.
- **Finding**: composing (*has-a*) over extending kept the firewall clean for free, and a view-only append-fold proves the interaction loop honestly without the governed write — both graduated to `context_canvas_surface_legs.md`.
- **Change**: author the follow-on as a backlog idea stub, not a full charter directory — matches how Salon itself incubated from a Palette note and avoids presuming the next campaign is committed.
- **Follow-up**: `how/backlog/idea_campaign_leg3_interface_runtime.md` (the leg-3 runtime build); external LIP-0008/0009 (closes 2026-06-27) + PT P5 unchanged.
