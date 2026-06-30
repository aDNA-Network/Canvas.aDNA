---
campaign_id: campaign_canvas_lodestar
type: campaign
title: "Operation Lodestar — Canvas Standard review & strategic positioning"
owner: stanley
status: active
estimated_sessions: "1-3"
phase_count: 3
mission_count: 1
priority: high
predecessor: campaign_canvas_armature
created: 2026-06-30
updated: 2026-06-30
last_edited_by: agent_mondrian
status_history: "planning (2026-06-30 chartered from a Mondrian/Canvas session — awaits operator ratify of scope at the P0→P1 gate; the review itself runs in a fresh post-/clear session) → active (2026-06-30, P0 ratified: D1=let-the-review-recommend · D4=assessment-only · D2/D3=recommend-don't-decide; session session_stanley_20260630_145035_lodestar_review running P1+P2)"
tags: [campaign, canvas, lodestar, review, positioning, standard, documentation, context_graph, rlhf, primitive]
---

# Campaign: Operation Lodestar — Canvas Standard review & strategic positioning

## Goal

**Carefully review Canvas.aDNA's work-to-date** for gaps and improvements, and **assess how well Canvas has
built — and documented/communicated — the aDNA Canvas Standard** as something larger than a fork of Advanced
Canvas / JSON Canvas: a **core primitive of prompting / interaction / pattern-memorialization / RLHF for
aDNA, the Lattice Protocol, and context-graph systems generally.** Produce a prioritized **gap register**, a
**positioning assessment**, and **gated recommendations**. This is a **review-and-recommend** campaign — the
build (README, positioning docs, new spec layers, any LIP re-open) is the *gated follow-on* it recommends,
not work it performs.

## Context

Six campaigns (Cartography → Keystone → Atelier → Palette → Salon → Armature) built the **three-leg canvas
thesis** — output primitive (×7 producers), context object (the `canvas_context` loader), interface surface
(the Armature interaction runtime) — to a technically strong, runtime-enabled state. A 2026-06-30 read-only
recon (3 Explore agents) found:

- **Technical: strong (~8.5/10).** 10 ratified specs, `canvas_std` reference impl (~319 tests), JSON Schema,
  `canvas-std` CLI, full C/E/A/I/D conformance, 7 conformant producers.
- **Documentation: strong internally, near-invisible externally.** No root README; `what/docs/` is all
  generic-aDNA (zero Canvas-specific); `VISION.md` is aDNA-generic. The pitch lives only in MANIFEST §Identity
  + `adr_000`.
- **Positioning: the operator's framing is new and absent.** The building blocks exist (the interaction
  `response` log + `reconcile` review draft; the context loader; the producer pattern) but are **never framed**
  as prompt-assembly / feedback-learning / pattern-capture. `adr_006` deferred RLHF to ISS; **LIP-0009
  deferred canvas-as-primitive** (Option V "keep as view") pending concrete consumer evidence — the operator's
  ask is essentially the evidence-backed re-open.

**So the opportunity is a clean re-positioning + documentation effort on a strong base — not an execution gap.**

## Scope

- **IN:** a careful assessment across three tracks (technical strength & standard-publishing · documentation &
  communication · strategic positioning); an explicit verdict on each of the four new framings; a prioritized
  gap register; a recommended (gated) follow-on.
- **OUT (gated follow-on, not this campaign):** building the root README / explainer / Lattice-integration doc
  / Canvas VISION; authoring new spec layers (prompting-primitive, RLHF-signal, pattern-memorialization);
  re-opening LIP-0009; cutting v2.1.0. Also OUT: the Hearthlight Tier-B fleet rollout (Hestia-owned).

## Phases (human-gated; never auto-advance — SO-1)

| Phase | What | Gate |
|-------|------|------|
| **P0 — Charter & scope** | Operator ratifies the scope + the ambition level + the open Decision Points below. (This master doc is the charter.) | operator ratify → activates the campaign |
| **P1 — The review** | Run `mission_lodestar_review` — three tracks (A technical · B docs · C positioning), reusing `iii/` + `skill_vault_review` + `skill_context_quality_audit`. Read-only assessment. | SITREP + HOLD |
| **P2 — Synthesis & recommend** | Gap register + positioning assessment + prioritized recommendations + a recommended follow-on (docs sprint and/or re-positioning). | operator gate: decide what to build |

## Review mission

→ `missions/mission_lodestar_review.md` (the short-term first mission; three tracks + the three deliverables).

## Gap register — SEEDED from the 2026-06-30 recon (extend, don't re-derive)

**Technical / standard-publishing**
- No canonical "published Standard" framing doc (title/abstract/scope/license/normative-refs) for external citation.
- No version-history / `CHANGELOG` at the standard level (versions: 2.0.0 → 2.0.1 → 2.0.2 → 2.2.0; 2.1.0 pending).
- No external **conformance certification kit** (package `what/code/canvas_std/tests/fixtures/` + a "run this to certify" README).
- **LIP-governance home unresolved → v2.1.0 (LIP-0008 A-5 relaxation) blocked** since lattice-labs archived 2026-06-27 (LIP-0008/0009 frozen in `Archive.aDNA/lattice-labs/how/governance/lips/`).
- Forward-compatibility note needed for the canvas-as-primitive question (LIP-0009).

**Documentation / communication**
- **No root `README.md`** (external landing page).
- `what/docs/` (24 files) is entirely generic-aDNA — no Canvas explainer / producer quickstart / Canvas↔Lattice integration doc.
- `who/governance/VISION.md` is aDNA-generic, not a Canvas-specific vision.
- The three-leg pitch + the "core primitive" thesis are internal-only (MANIFEST/`adr_000`/STATE), not external-facing.

**Positioning — the four new framings (currently absent)**
- **(i) Prompting primitive** — unformalized; closest is canvas-as-context-object (leg 2). No spec for canvas-in-prompt/context-assembly.
- **(ii) RLHF / feedback-signal** — adjacent via the `response` log + `reconcile` draft, but framed as an audit trail; `adr_006` defers the RLHF schema to ISS.
- **(iii) Pattern memorialization** — producer pattern proven 7× + interaction primitives defined, but not a capture / versioning / discovery *system*.
- **(iv) "The" context-graph primitive** — implied (the `ContextGraph` model) but not architecturally claimed; waits on the unwritten `aDNA.aDNA` OIP thesis. **LIP-0009 = deferred (Option V); re-open needs concrete consumer evidence.**

## Decision Points (for the review + operator to resolve — defaults adjustable)

- **D1 — Ambition level.** Strengthen-and-document-what-exists · **vs** re-position as the context-graph primitive (multi-spec) · **vs** staged (document now, re-position on evidence). *Default: let the review recommend, evidence-based (matches the LIP-0009 bar).*
- **D2 — LIP-0009 re-open?** Does the operator's prompting/RLHF/pattern-memorialization framing constitute the "concrete consumer evidence" LIP-0009 requires to re-open canvas-as-primitive (Option P)? *Default: assess in Track C; recommend, don't decide.*
- **D3 — LIP-governance home.** Where do Canvas's LIP Final-decisions route now that lattice-labs is archived? (Blocks v2.1.0.) *Default: recommend a successor venue in Track A.*
- **D4 — Fold the README draft into the review mission** as a quick win, or keep the mission assessment-only? *Default: assessment-only (kept short-term); README is the top recommended follow-on.*

## Reuse, not rebuild

- The 3-track recon structure (this charter's recon) → the mission's three review tracks.
- `iii/` review framework + `skill_vault_review` + `skill_context_quality_audit` — no new audit tooling.
- The `canvas-std` conformance harness to re-verify technical green.
- Existing specs/ADRs as the review's source of truth.

## Next-session prompt (for the fresh post-`/clear` agent)

> Open `how/campaigns/campaign_canvas_lodestar/` (read its `CLAUDE.md` + this master doc). Operation Lodestar
> is a `status: planning` review-and-position campaign. At the P0 gate, confirm scope + the four Decision
> Points with the operator, then run `missions/mission_lodestar_review.md`: three read-only tracks (A technical
> & standard-publishing · B documentation & communication · C strategic positioning — the four new framings +
> the LIP-0009 re-open question), reusing `iii/` + `skill_vault_review` + `skill_context_quality_audit`. The
> **gap register is already seeded** (this doc §Gap register) — extend it, don't re-derive. Produce the three
> deliverables (gap register · positioning assessment · prioritized recommendations + a recommended follow-on),
> each with an AAR. HOLD at every phase gate. The review **recommends**; the operator **gates** the build.

## Provenance

Chartered 2026-06-30 from a Mondrian/Canvas session whose arc was: continued Operation Hearthlight → Tier-B
orientation + B-forge build → **stood down** when the Home/Hestia session took the cross-vault rollout (operator
decision) → SITREP → Canvas-local cleanup (STATE reconcile `8914613`, pushed) → this charter (off a 3-Explore-agent
recon). Session AAR: `how/sessions/history/2026-06/`.
