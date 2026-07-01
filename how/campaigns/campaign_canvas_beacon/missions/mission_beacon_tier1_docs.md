---
type: mission
mission_id: mission_beacon_tier1_docs
campaign_id: campaign_canvas_beacon
phase: B2
status: completed
owner: stanley
persona: Mondrian
created: 2026-06-30
updated: 2026-06-30
last_edited_by: agent_mondrian
tags: [mission, beacon, tier1, documentation, readme, quickstart, explainer, manifest, vision]
---

# Mission: Operation Beacon — Phase B2 / Tier 1 documentation sprint

## Intent

Convert an invisible-but-strong repo into a navigable one (Lodestar Tier 1 / gaps B1·B2·B3·B-note·B6).
**~80% of the prose exists internally** — lift & repackage; author the connective narrative fresh.
No `canvas_std` code touch expected (docs only); the schema/spec version-currency was done in B1.

## Objectives

| # | R | Objective | Source material | Status |
|---|---|-----------|-----------------|--------|
| **O1** | R1.1 | Root **`README.md`** (external landing page) — definition · three-leg thesis · "what's here" map · 5-line quickstart · links | `MANIFEST.md:15-23` (thesis) · `canvas_std/README` (quickstart) · MANIFEST architecture (map) | ✅ done |
| **O2** | R1.4 | Refresh **`MANIFEST.md`** — §Status through Armature (add Palette/Salon/Armature); fix pre-merge producer framing (CanvasForge/Hermes, LiteratureForge/Thoth) | STATE.md (current) · campaign close records | ✅ done |
| **O3** | R1.2 | **Producer quickstart** — "build a canvas producer in 15 min" | `what/production/_scaffold/README.md` · `deck_generator/README.md` · `how/skills/skill_canvas_producer_build.md` | ✅ done |
| **O4** | R1.3 | **Canvas Standard explainer** — fork story · source-vs-view · `_reserved`+degradation · conformance levels · substrate-neutrality · the Canvas-as-RLHF capture-substrate story | `spec_adna_canvas_standard §2` · `adr_000` · `context_canvas_surface_legs` · Lodestar positioning assessment | ✅ done |
| **B6** | — | **VISION sub-gate** — replace generic `who/governance/VISION.md` (rec) vs add `VISION_canvas.md`; then author the Canvas-specific vision | operator decision + `MANIFEST` thesis | ✅ done (replaced) |
| **O5** | — | Verify (markdown links resolve; no residual `v2.0.0`/stale in touched docs) + SITREP + HOLD at B2→B3 | — | ✅ done |

## Notes
- **B6 is an operator sub-decision** — surface it before touching VISION; do not assume.
- The root README resolves the deliberately-left README links (`CONTRIBUTING:159`, `VISION:149`).
- Keep it **repackaging, not re-deriving** — cite/lift internal sources; the explainer (O4) is the one genuinely-new narrative.

## AAR

- **Worked:** ~80% of the prose existed internally — the README/MANIFEST lifted the thesis, the quickstart was near-pure assembly of `_scaffold`+skill, and the explainer was the one genuinely-new narrative. All new-doc links verified resolving.
- **Didn't:** nothing blocked. The generic `VISION`/`CONTRIBUTING` boilerplate ran deeper than B1's link-fix band-aid — B6 resolved VISION (**replaced** with a Canvas vision); `CONTRIBUTING.md` is still generic-template (candidate follow-up).
- **Finding:** the repo now has a navigable front door — Lodestar's invisible-repo gap (B1/B2/B3) is closed. The buried **capture-substrate / Canvas-as-RLHF** story is now told externally (explainer + VISION), per D1=staged.
- **Change:** VISION **replaced** (not added) — cleaner for a standard-bearer; kept it (and the README) frontmatter-free for clean GitHub rendering, matching CONTRIBUTING.
- **Follow-up:** `CONTRIBUTING.md` wants a Canvas-specific rewrite; B5 (Canvas↔Lattice integration) + B8/B9 remain lower-priority candidate adds; the README's spec-license note stays light pending **R2.1** (B3).
