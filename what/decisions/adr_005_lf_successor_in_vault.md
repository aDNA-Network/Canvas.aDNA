---
type: decision
adr_id: "005"
title: "LF-successor pipeline home — in-vault production (supersedes ADR-002's Option-B federated leg)"
status: ratified
created: 2026-06-19
updated: 2026-06-19
last_edited_by: agent_stanley
signed_by: "Stanley (operator countersign 2026-06-19, Keystone E5 — D3 governed touch); proposed by Mondrian 2026-06-19"
supersedes: "adr_002 (D3 — Option-B federated-pipeline leg only; the Option-A schema-absorb leg stands)"
superseded_by:
resolves: "D3 reshape — pt09 makes the LF-successor in-vault (federated → in-vault); unblocks Keystone E4.1/E4.2"
phase: "Keystone E5 (mid-phase governed touch; pt09 follow-up)"
tags: [adr, canvas, standard, literatureforge, lf-successor, in-vault, production, pt09, d3, federation, substrate-neutrality]
---

# ADR-005: LF-successor Pipeline Home — In-Vault Production (D3 reshape)

> The **"D3 governed touch"** the Keystone campaign flagged at the E3→E4 / E4→E5 crossings. It conforms the D3
> decision ([[adr_002_literatureforge_seam]]) to the post-pt09 reality and **unblocks E4.1/E4.2** — it does **not**
> build them (they stay `planned`, unscheduled). This is the sanctioned alternative to ad-hoc re-deciding, and it is
> the **separate superseding ADR that ADR-002 itself prescribed** for this exact case.

## Status

**Ratified** — 2026-06-19 (operator Stanley countersign at the Keystone E5 hold; proposed by Mondrian 2026-06-19).
Canvas ADRs ratify at an operator decision gate (Mondrian proposes → Stanley countersigns; the
[[adr_004_production_code_layout|ADR-004]] pattern). **The E4.1/E4.2 D3 blocker is cleared.**

**Not a Standard LIP.** [[adr_003_standard_governance]] §2 scopes the LIP process to *normative changes to the
Standard* (schema / conformance levels / the aDNA core). This ADR changes only *where the LF-successor pipeline
lives* (in-vault vs federated) — an internal Canvas architecture/governance choice. The Standard schema is
untouched (ADR-002's Option-A absorb is already shipped in `canvas_std`). An operator-signed ADR is therefore the
correct and sufficient instrument.

## Context

**ADR-002 (D3, ratified 2026-06-12)** resolved the LiteratureForge seam as a **two-layer** answer:

1. **(A) Schema layer → document-AS-canvas.** The LF visual/format contracts absorb into the Standard — the
   component model (`spec_component_model.md`), panel/link semantics (`spec_panel_link_semantics.md`) and round-trip
   v2. **Built at P1/E2; lives in `canvas_std`; unchanged by this ADR.**
2. **(B) Pipeline layer → a *federated* LF-successor producer.** The writing-composition pipeline (genre submodule,
   trap-packs, reviewer voices, reward rubrics) would live in a *separate* producer federating against the Standard
   via a `federation_ref` wrapper. Option B was chosen over **Option C (absorb / in-vault)** expressly to keep
   Canvas a **single-faced** standard-bearer and preserve substrate-neutrality (C8), **"symmetric with D2"**
   ([[adr_001_canvasforge_relationship]] — CanvasForge was *also* a federated producer at the time).

**Then the topology moved.** **pt09** (Production Tidy, 2026-06-17) merged CanvasForge **into** Canvas (Hermes →
Mondrian), reversing the E3.4 federated-producer split: Canvas.aDNA now owns the Standard **and** the production
layers (deck · comic · diagram) at `what/production/`, as recorded in CLAUDE.md and ratified in
[[adr_004_production_code_layout|ADR-004]]. **LiteratureForge (Thoth) had already been wound down** (2026-06-08) →
`Archive.aDNA/LiteratureForge.aDNA/`; its assets are a Canvas scavenge quarry, not a live vault.

**The consequence for D3.** Option B's load-bearing justification — *"symmetric with D2 (CanvasForge federated)"* —
**inverted**. After pt09 there is no federated sibling to be symmetric with; the uniform topology is now *in-vault*.
And the "two-faced 2D-output platform" scope-reopening that ADR-002 reserved for Option C **has already happened**
(pt09 governance merge + CLAUDE.md mission scope "standard-bearer **and** production owner" + ratified ADR-004's
two-shelf code layout). So ADR-002's **Option-B (federated) leg is overtaken by events.** ADR-002 anticipated
exactly this: *"If the operator later wants absorb (C), that is a separate scope-reopening ADR (superseding this
one's pipeline clause)."* **This is that ADR.**

## Decision

**1 — The LF-successor is built IN-VAULT** at `what/production/`, federating against `canvas_std` exactly as the
other in-vault producers do (`brief_consumer`, `deck_generator`). This **supersedes ADR-002's Option-B
(federated-producer) leg** and adopts ADR-002's documented **Option C (absorb)** — now warranted, not speculative,
because pt09 already made Canvas the production owner.

**2 — ADR-002's Option-A (schema-absorb) leg stands, unchanged.** The LF visual/format contracts already live in
`canvas_std` (component_model + panel_link + round-trip v2). This ADR touches **only the pipeline home**; ADR-002 is
*partially* superseded (pipeline leg), not retired.

**3 — Substrate-neutrality is preserved by the ADR-004 two-shelf firewall** — the very firewall ADR-002 named as a
prerequisite for Option C. `what/code/canvas_std/` remains the lean, zero-dependency, **producer-neutral** Standard
face; `what/production/` holds the producers. The LF-successor joins deck/comic/diagram on the production shelf. The
**genre/writing pipeline stays producer-side** (trap-packs, reviewer voices, reward rubrics, genre register) — it
never enters the Standard. The Standard face does not "grow a writing pipeline"; a sibling producer does.

**4 — Scope is inherited, not re-opened.** The standard-bearer → +production-owner expansion that Option C implies
is **already settled** (pt09 + CLAUDE.md + ratified ADR-004). This ADR inherits that scope; it does **not**
re-litigate [[adr_000_canvas_identity]] §1 / D1 / Option-P. (If the operator later wants the expansion formally
re-stated at `adr_000`, that is optional housekeeping — deliberately **not** bundled here, to keep this touch
single-purpose.)

**5 — Build coupling: none to PT P5.** Like E4.3/E4.4, the LF-successor consumes `canvas_std` (zero-dependency,
already published as `adna-canvas-std`); it does **not** require `canvas_core`. It is therefore buildable on
`canvas_std` alone, with **zero PT-P5 dependency**. This ADR **unblocks** E4.1/E4.2; it does not schedule or build
them (they remain `status: planned`, unscheduled, to be opened on operator go per SO-3).

**Considered and rejected:**

- **Amend ADR-002 in place.** *Rejected:* this is a decision *reversal* of a ratified consequence, not an
  errata/clarification. `what/decisions/AGENTS.md`'s lifecycle (Propose → Accept → **Supersede**) and ADR-002's own
  text both prescribe a *separate superseding ADR*; ADR-004 set the in-vault precedent (a new ADR for the sibling
  pt09 reshape, not an amendment). A new ADR yields a clean, single-purpose, dated, operator-signed reversal record.
- **Keep Option B (federated LF-successor) regardless.** *Rejected on fact:* there is no LiteratureForge vault left
  to federate from (wound down → Archive). Standing up a *new* standalone federated vault purely to honor the old
  D2 symmetry — after pt09 absorbed the sibling producer in-vault — manufactures topology divergence for zero
  benefit, and re-creates exactly what pt09 consolidated.
- **Route through a Standard LIP.** *Rejected:* over-process. The Standard schema is unchanged; ADR-003 §2 reserves
  the LIP for normative Standard changes. The pipeline home is internal architecture.
- **Bundle an `adr_000` Option-P amendment.** *Rejected/deferred:* the scope is already settled by pt09 + ADR-004;
  bundling would broaden a single-purpose touch. Flagged as optional future housekeeping.

## Consequences

### Positive
- **Unblocks Keystone E4.1/E4.2** — the carried D3 debt is cleared (on ratification); the LF-successor becomes
  buildable whenever the operator schedules it, on `canvas_std` alone.
- **Topology uniform post-pt09** — every Canvas producer lives in-vault on the `what/production/` shelf; no
  one-off federated exception to maintain.
- **Substrate-neutrality intact** — the Standard face (`canvas_std`) stays producer-neutral via the ADR-004
  shelf split; the writing pipeline stays producer-side.
- **Clean audit trail** — a single dated, operator-signed ADR records the reversal and its cause (pt09), with
  ADR-002's Option-A leg explicitly preserved.

### Negative
- Canvas formally carries a writing-composition producer (the "two-faced platform" cost ADR-002 flagged for
  Option C) — *mitigated* by the two-shelf firewall + keeping the genre pipeline producer-side, and *already
  incurred* by pt09 for deck/comic/diagram.
- One more in-vault producer to build and maintain (E4.1/E4.2), versus an external vault's separate lifecycle.

### Neutral
- The LF quarry (`Archive.aDNA/LiteratureForge.aDNA/` — Thoth doctrine + 10 specs + 39 corpus +
  `spec_visual_contract` V1–V8/X1–X14 + the 5-part `spec_genre_submodule`) is the scavenge source for the E4.2
  build; unchanged by this decision.
- ADR-002 keeps `status: ratified` (its Option-A schema leg is live and correct); it gains a partial-supersession
  banner + `superseded_by` pointer to this ADR.

## Related
- [[adr_002_literatureforge_seam]] (D3 — the superseded Option-B leg; the prescribing text; Option-A leg stands) ·
  [[adr_004_production_code_layout]] (pt09 reshape; the two-shelf substrate-neutrality firewall; new-ADR precedent) ·
  [[adr_001_canvasforge_relationship]] (D2 — the federated symmetry pt09 dissolved) ·
  [[adr_000_canvas_identity]] §1 (Option-P scope — inherited here, not re-opened) ·
  [[adr_003_standard_governance]] §2 (LIP scope — why this is an ADR, not a LIP) ·
  [[decision_register_genesis]] (D3 row).
- [[../../how/campaigns/campaign_canvas_genesis/missions/mission_e4_1_lf_successor|mission E4.1]] ·
  [[../../how/campaigns/campaign_canvas_genesis/missions/mission_e4_2_lf_contracts|mission E4.2]] (unblocked by this ADR).
- `aDNALabs.aDNA/what/migration/decision_literatureforge_canvas_subsumption.md` (the absorb rationale + preservation
  inventory — now the adopted path) · `Archive.aDNA/LiteratureForge.aDNA/` (the scavenge quarry).
