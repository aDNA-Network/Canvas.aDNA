---
type: mission
mission_id: mission_beacon_tier0_quickwins
campaign_id: campaign_canvas_beacon
phase: B1
status: completed
owner: stanley
persona: Mondrian
created: 2026-06-30
updated: 2026-06-30
last_edited_by: agent_mondrian
tags: [mission, beacon, tier0, quickwins, links, versions, canvas_std, spec, schema]
---

# Mission: Operation Beacon — Phase B1 / Tier 0 quick wins

## Intent

Highest credibility-per-hour corrections (Lodestar Tier 0 / gaps A1-part·A3·A6·B4). **Corrections, not new
docs** — fix an external reader's first impressions cheaply. All targets line-verified in the planning recon.
`canvas_std` README + schema are touched (docs/metadata only); re-run the harness to confirm `105/10` green.

## Objectives

| # | R | Objective | Targets (line-verified) | Status |
|---|---|-----------|-------------------------|--------|
| **O1** | R0.1 | Fix wrong-repo + dead links | `CONTRIBUTING.md` L21,22,29,49,78,157 (`LatticeProtocol/adna` → `aDNA-Network/Canvas.aDNA`) + dead `README.md` link L159; `who/governance/VISION.md` L149 dead `README.md` link | ✅ done |
| **O2** | R0.2 | Refresh `canvas_std/README.md` | L3 `v2.0.0`→`v2.2.0`; L8 `46 passed / 8 skipped`→`105 passed / 10 skipped`; status line current | ✅ done |
| **O3** | R0.3 | Fix spec title/H1 + stale producer names | `what/specs/spec_adna_canvas_standard.md` L4 (fm `title:`) + L15 (H1) `v2.0.0`→`v2.2.0`; CanvasForge/ComfyForge/SiteForge → Canvas/ComfyUI/Astro | ✅ done |
| **O4** | R0.4 | Document the schema `$id` pin | `src/canvas_std/data/adna_canvas_v2.schema.json` — `$id` deliberately pinned v2.0.0 (structural schema unchanged, CHANGELOG L29); add an inline note rather than bump | ✅ done |
| **O5** | — | Verify + HOLD | `pytest -q` in `what/code/canvas_std/` → expect `105 passed / 10 skipped`; grep links/versions clean; SITREP + HOLD at the B1→B2 gate | ✅ done |

## Firewall note
O2 + O4 touch `what/code/canvas_std/` (README + schema metadata) — **docs/metadata only, no `src/canvas_std/*.py`
logic**. Re-run `pytest -q` after (O5); `git diff --stat -- src/canvas_std/*.py` must be empty.

## Note on the dead README links
O1's `README.md` link targets (CONTRIBUTING L159, VISION L149) currently point at a non-existent root README.
They **resolve** once Phase B2 / R1.1 creates the root README. In B1 we fix the *wrong-repo* links and leave the
README links pointing at the soon-to-exist root README (do not delete them).

## AAR

- **Worked:** the planning recon's line-verified targets made R0.1–R0.4 near-pure find-replace; harness stayed **105/10**; firewall held (only `canvas_std/README.md` + the schema *data* file + spec/community-health docs touched — **no `src/canvas_std/*.py`**).
- **Didn't:** nothing blocked — paths/line numbers were exact; the schema `$comment` is a no-op annotation (suite unchanged).
- **Finding:** `CONTRIBUTING.md` (esp. its Development-Setup block) + `VISION.md` are **generic-aDNA-template boilerplate** — the link fix is a band-aid; both want a Canvas-specific rewrite (B2/docs). Also `CONTRIBUTING.md:90` references `LatticeProtocol/Agentic-DNA` (a *framework-upstream* ref, likely now `aDNA-Network/aDNA`) — **out of R0.1 scope, flagged**.
- **Change:** documented the **deliberate** schema `$id` v2.0.0 pin via a JSON-Schema `$comment` (did NOT bump `$id`) — keeps the canonical URL stable while `x-standard-version` tracks 2.2.0.
- **Follow-up:** B2 gives `CONTRIBUTING`+`VISION` a Canvas-specific pass (ties to the **B6 VISION** decision); the README links (`CONTRIBUTING:159`, `VISION:149`→`../../README.md`) **resolve when B2/R1.1 lands the root README**.
