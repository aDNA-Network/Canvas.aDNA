---
type: mission
mission_id: mission_lodestar_review
related_campaign: campaign_canvas_lodestar
status: completed
phase: P1
created: 2026-06-30
updated: 2026-06-30
last_edited_by: agent_mondrian
owner: stanley
gated_on: P0 ratify (operator confirms scope + Decision Points D1–D4 in the campaign master)
tags: [mission, lodestar, review, audit, positioning, documentation, standard]
---

# Mission — P1: The Lodestar review (Canvas Standard work-to-date + positioning)

> **Read-only assessment.** Carefully review Canvas's work-to-date for gaps/improvements and assess how well
> Canvas has built — and documented/communicated — the aDNA Canvas Standard as a **core primitive for prompting
> / interaction / pattern-memorialization / RLHF in context-graph systems**. The review **recommends**; the
> operator **gates** any build. The gap register is **seeded** (campaign master §Gap register) — extend it.

## Objectives — three parallel tracks

### Track A — Technical strength & standard-publishing
- Re-verify the spec suite (10 specs, ratified?), `canvas_std` (modules + ~319 tests green via `canvas-std`/pytest),
  the 7 producers, and the C/E/A/I/D conformance coverage. Confirm no regression; note any draft/TODO/half-built area.
- Assess what's missing to be an **externally credible** standard: a canonical "published Standard" doc
  (title/abstract/scope/normative-refs/license), a standard-level **CHANGELOG/version-history**, an external
  **conformance certification kit** (package `what/code/canvas_std/tests/fixtures/` + a "run-this-to-certify" guide),
  and resolving the **LIP-governance home** (D3 — blocks v2.1.0 / LIP-0008 since lattice-labs archived).
- **Verdict:** a technical-gap list with severity + the standard-publishing checklist.

### Track B — Documentation & communication
- Assess external-reader readiness (could an outside developer orient + adopt from the repo alone? Today: no root
  README; `what/docs/` is all generic-aDNA; VISION is aDNA-generic).
- Design (outline, don't build) the missing doc set: **root `README.md`**, a Canvas **standard explainer**, a
  **producer quickstart**, a **Canvas↔Lattice / context-graph integration** doc, a Canvas-specific **VISION**.
- **Verdict:** a prioritized doc-gap list, each with a one-paragraph outline + audience.

### Track C — Strategic positioning (the headline)
- For each of the four new framings, evaluate what's built/documented vs the operator's vision and assign a verdict
  (**build-now / spec-it / defer / re-open-LIP-0009**):
  - **(i) Prompting primitive** — canvas in prompt/context assembly (closest today: leg-2 context-object).
  - **(ii) RLHF / feedback-signal** — the `response` log + `reconcile` draft as a learning/preference signal vs
    `adr_006`'s deferral of the RLHF schema to ISS. Where is the seam? What would Canvas own vs ISS?
  - **(iii) Pattern memorialization** — canvases as durable, versioned, discoverable reusable patterns (vs the
    producer pattern + interaction primitives that exist but aren't a capture/versioning/discovery system).
  - **(iv) "The" context-graph primitive** — Canvas's architectural role for context-graph-driven agents; the
    `aDNA.aDNA` OIP-thesis dependency; whether the operator's framing is the **concrete consumer evidence** that
    LIP-0009 §3 requires to re-open canvas-as-primitive (D2).
- **Verdict:** a per-framing recommendation + an overall ambition recommendation (D1: strengthen-and-document vs
  re-position vs staged), evidence-based.

## Deliverables (→ `missions/artifacts/`)

1. **`lodestar_gap_register.md`** — prioritized, three sections (technical · docs · positioning); extends the seeded register.
2. **`lodestar_positioning_assessment.md`** — where Canvas is vs the vision; built vs genuinely-new; per-framing verdicts; the D1 ambition recommendation; the D2 LIP-0009 re-open recommendation.
3. **`lodestar_recommendations.md`** — prioritized recommendations + a **recommended follow-on** (almost certainly a docs/communication sprint + a positioning decision), framed as gated options for the operator.

## Acceptance criteria

- All three tracks complete; each of the four framings carries an explicit verdict.
- `canvas-std`/producer suites confirmed green (technical baseline verified, not assumed).
- The three deliverables exist; the mission carries a 5-line AAR (SO-5) before `status: completed`.
- A clear operator gate at P2: which follow-on(s) to build (docs sprint and/or re-positioning) — the mission builds nothing.

## Reuse, not rebuild

`iii/` review framework · `skill_vault_review` · `skill_context_quality_audit` · the `canvas-std` harness · the
existing specs/ADRs as source of truth · the 3-track recon structure already run (campaign master §Gap register).

## AAR

*5-line AAR (SO-5) — 2026-06-30, session `…_145035_lodestar_review`.*

- **Worked:** three parallel read-only review agents (A technical · B docs · C positioning) returned dense, file-cited evidence in one pass; the `canvas_std`/`canvas_context`/7-producer suites ran **green from per-component venvs** without touching the firewall (`git status -s -- what/code/canvas_std/` stayed clean); the seeded gap register let synthesis start from evidence, not a blank page.
- **Didn't:** the seeded register carried **five inaccuracies** — test total (386+10, not ~319), spec count (9, not 10), "no CHANGELOG" (one exists, code-scope), RLHF "adjacent/audit-trail" (a built, live package exists), "no cert kit" (raw materials exist). An Explore-only recon under-counted and under-read.
- **Finding:** the gap is **articulation, not engineering** — every framing is served by the `_reserved`-over-view model; and a working **Canvas-as-RLHF-surface** (13 live `SelectionRecord`s + an III ADR-005 bridge) is buried in a producer and undersold.
- **Change:** future "assess work-to-date" missions must **run the harness + read the code** in P1, not trust a prior Explore recon's numbers; treat seeded findings as hypotheses to verify.
- **Follow-up:** operator gates the P2 follow-on (recommended: docs sprint Tier 0+1 + governance unblock Tier 3 → v2.1.0); the D3 LIP-numbering decision; the spec-it (i)/(ii) work staged. Deliverables: `missions/artifacts/lodestar_{gap_register,positioning_assessment,recommendations}.md`.
