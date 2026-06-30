---
type: artifact
artifact_type: gap_register
mission_id: mission_lodestar_review
campaign_id: campaign_canvas_lodestar
created: 2026-06-30
updated: 2026-06-30
status: active
last_edited_by: agent_mondrian
tags: [lodestar, review, gap_register, technical, documentation, positioning, standard]
---

# Lodestar Gap Register

> **Deliverable 1 of 3** (Operation Lodestar P1 review). Extends the **seeded** register (`campaign_canvas_lodestar.md` §Gap register) with Track A/B/C evidence from the 2026-06-30 read-only review. **Severity:** High / Med / Low. **Effort:** S (hours) / M (a session) / L (multi-session). Items are IDs (A1, B1, C-i…) for cross-reference from the recommendations deliverable.
>
> **Read with:** `lodestar_positioning_assessment.md` (full Track-C analysis) · `lodestar_recommendations.md` (what to do, gated). This register is the *evidence*; the recommendations are the *plan*.

---

## ⚠ Corrections to the seeded register (the review's first job: get the baseline right)

The 2026-06-30 recon seeded this register from a 3-Explore pass. Re-verification (incl. *running* the harness) corrected five claims — captured here so downstream work starts from truth:

| # | Seeded claim | Corrected finding | Source |
|---|--------------|-------------------|--------|
| 1 | "~319 tests" | **386 passed + 10 skipped** across all named suites (canvas_std 105/10 · canvas_context 58 · 7 producers 223). The 319 figure is stale. | Track A, ran the suites |
| 2 | "10 ratified specs" | **9** `spec_*.md` files (all `status: ratified`, `standard_version: 2.2.0`). Charter is off-by-one. | Track A, `ls what/specs/` |
| 3 | "No version-history / CHANGELOG at the standard level" | A CHANGELOG **exists** (`what/code/canvas_std/CHANGELOG.md`) — but it is *code-scope*, mixes package vs standard versions, and **omits `[2.0.2]`**. The true gap is "no **standard-scope** version-history," not "no CHANGELOG." | Track A |
| 4 | "(ii) RLHF — adjacent via the response log… framed as an audit trail" | A **built, operational** Canvas-as-RLHF package exists (`what/production/canvas_core/rlhf/` — `SelectionRecord` + back-prop + III ADR-005 bridge) with **13 live selection records**. For the image domain the loop already closes. The register *undersold* this framing. | Track C |
| 5 | "No external conformance certification kit" | The **raw materials exist** (`what/code/canvas_std/tests/fixtures/` — 11 golden `.canvas` + `manifest.json`; the `canvas-std` CLI; ratified `spec_conformance_suite.md`). The gap is **packaging + a guide**, not absence. | Track A |

---

## Track A — Technical strength & standard-publishing

**Baseline verdict: genuinely green and complete — not a gap.** Every named suite matches the Armature baseline to the test (386 passed / 10 skipped); no live stubs (TODO/FIXME hits all benign); `STANDARD_VERSION = "2.2.0"` confirmed (`what/code/canvas_std/src/canvas_std/__init__.py:29`). One *legacy* suite outside the 7-producer baseline (`what/production/tests/test_federation_validation.py`) cannot collect (needs `pytest-timeout` + Pillow; imports the deprecated `what/production/canvas_core`, grace window → 2027-06-13) — an environment/legacy gap, not a logic failure (logged as A8).

The gaps are all about **external credibility**, not engineering:

| ID | Gap | Sev | Effort | What exists / what's missing |
|----|-----|-----|--------|------------------------------|
| **A1** | **No citable "published Standard" framing** | **High** | M | `spec_adna_canvas_standard.md` has strong bones (RFC-2119, scope, normative refs, conformance levels) but: **title + H1 say "v2.0.0"** (standard is 2.2.0); **no license on spec text** (zero SPDX/CC across all 9 specs; code is MIT, spec text is unlicensed); **internal `[[wikilink]]` normative refs** (`[[p1_fork_baseline]]`) that don't resolve externally; **stale producer names** (CanvasForge/ComfyForge/SiteForge); no abstract block; no stable external identifier/DOI/URL. |
| **A2** | **LIP-governance home unresolved → v2.1.0 blocked (D3)** | **High** | decision + S | LIP-0008 (gates v2.1.0) + LIP-0009 frozen `status: Review` in **archived** `Archive.aDNA/lattice-labs/how/governance/lips/` (reader-only since 2026-06-27; review clock lapsed, no live steward). `adr_003_standard_governance.md §2` binds the change process to a now-dead path. Canvas has **no** `who/governance/lips/`. The whole LIP-0001–0009 number space is used. → see recommendation R-A2 (Canvas-local home + numbering decision). |
| **A3** | **Stale reference-impl README** | **Med-High** | S | `what/code/canvas_std/README.md` says "v2.0.0", `STANDARD_VERSION "2.0.0"`, "46 passed / 8 skipped" — frozen at Keystone E2. It is the **first file an external implementer reads** and every headline number is wrong. |
| **A4** | **No standard-scope version-history; code CHANGELOG mixes scopes, missing `[2.0.2]`** | **Med** | S-M | (See correction #3.) Need a spec-scope history covering 2.0.0 → 2.0.1 → 2.0.2 → [2.1.0 reserved/why] → 2.2.0; back-fill `[2.0.2]` (AT-1/AT-2 errata, documented only in `lip_queue_disposition.md`); separate package- vs standard-version headers. (Overlaps B7.) |
| **A5** | **Conformance certification kit not packaged** | **Med** | M | (See correction #5.) Fixtures + `manifest.json` (`expected_level_reached`/`expected_ok`) + CLI + `spec_conformance_suite.md` all exist but are wired to the *internal* pytest harness. Missing: a portable "run-this-to-certify-your-implementation" runner, a certification guide, and Core/Extended/aDNA-Native self-attestation flow. *Close* — packaging, not engineering. |
| **A6** | **JSON Schema `$id` pinned to v2.0.0 URL** | **Low** | S | `data/adna_canvas_v2.schema.json` has `title: "…v2.2.0"` but `$id: …/canvas/v2.0.0/…` (deliberate — schema structurally unchanged — but an external-facing version mismatch). |
| **A7** | **Empty root README / `adna_standard.md` namespace confusion** | **Low** | S | Root `README.md` is a 0-byte placeholder; `what/docs/adna_standard.md` is the *generic* "aDNA Universal Standard" (easily confused with the Canvas Standard). No single "start here" index. (Overlaps B1.) |
| **A8** | **Legacy federation suite cannot run** | **Low** | S | `what/production/tests/test_federation_validation.py` errors on collection (env: `pytest-timeout`/Pillow; imports deprecated `canvas_core`). Outside the green baseline; resolve or quarantine before the PT-P5 `canvas_core` relocation. |

**Standard-publishing checklist (the artifacts that make this externally publishable):** citable spec (fix version/license/refs/names + abstract + stable ID) · refreshed `canvas_std/README` · standard-scope version-history · packaged cert kit + guide · external entry/index doc · a *live* governance/change process (A2).

---

## Track B — Documentation & communication

**Verdict: an external developer cannot orient or adopt from the repo today.** The repo is genuinely GitHub-public (`aDNA-Network/Canvas.aDNA`, class P-released) — readers really land here — on a tree with **no rendered landing page**. The substance (~80%) is written; the **routing is ~0%**, and the two generic community-health files at root (VISION, CONTRIBUTING) describe a *different* project with dead/wrong links. **Content debt low, packaging/routing debt high.**

| ID | Gap | Sev | Effort | Material already internal |
|----|-----|-----|--------|---------------------------|
| **B1** | **No root `README.md`** (external landing page) | **High** | S | ~70% — thesis at `MANIFEST.md:17-23`, quickstart at `canvas_std/README`, repo map at `MANIFEST` Architecture. The single highest-leverage move; also fixes the cluster of dead `[README](README.md)` links already pointing at it. |
| **B2** | **No Canvas Standard explainer** (the "what/why" narrative) | **High** | M | ~75% — fork story (`spec_adna_canvas_standard §2`, `adr_000 §4`), source-vs-view (Decision 9), `_reserved` + degradation contract (the headline differentiator). Normative spec is the backbone but too dense to *be* the explainer. |
| **B3** | **No producer quickstart** | **High** | S | ~90% — `what/production/_scaffold/README.md` (copy-me recipe), `deck_generator/README.md` (CLI + Python), `how/skills/skill_canvas_producer_build.md`. Near-pure assembly; highest-ROI/lowest-cost doc. |
| **B4** | **Dead / wrong-repo links (fix-in-place)** | **High** | S | `CONTRIBUTING.md` points external contributors at `LatticeProtocol/adna` (wrong repo) + dead `README.md` link; `VISION.md:149` dead `README.md` link. Corrections, not new docs, but they actively mislead today. |
| **B5** | **No Canvas↔Lattice / context-graph integration doc** | **Med** | M | ~60% — spread across `spec_context_object`, `spec_canvas_context_loading`, `spec_interface_surface`, `spec_federation_contract`, `spec_roundtrip_protocol_v2`, `context_canvas_surface_legs`. Needs a unifying spine (the three legs). This is also where the **positioning** lands externally (Track C framing iv). |
| **B6** | **VISION.md is generic aDNA, not Canvas-specific** | **Med** | M | ~30% — titled "The Decentralized Frontier Lab"; zero canvas/three-leg content. Thesis paragraph + doc skeleton reusable; vision prose written fresh. Decision: replace vs add `VISION_canvas.md`. |
| **B7** | **No Canvas-Standard CHANGELOG** (history scattered) | **Med** | S | Root `CHANGELOG.md` tracks the generic knowledge-architecture; Standard's own version line is scattered across MANIFEST/STATE/ADRs/`lip_queue_disposition`. (Overlaps A4 — do once.) |
| **B8** | **No architecture / repo-map overview for humans** | **Low-Med** | S | The triad split + where spec/impl/producers/ADRs live. Could be a README section, not a standalone doc. |
| **B9** | **No glossary** | **Low** | S | Heavy in-house vocab (aDNA-Native, `_reserved`, two-shelf firewall, panel-link, canonical surface, degradation contract, substrate-neutrality). Appendix to B2. |
| **B-note** | **MANIFEST.md is stale** (not a doc gap, a freshness gap) | Med | S | §Identity still frames CanvasForge (Hermes) + LiteratureForge (Thoth) as separate producers (pre-merge); §Status stops at Atelier (misses Palette/Salon/Armature). **Lift the *thesis* prose, not the *status* prose**, and refresh it. |

---

## Track C — Strategic positioning (the four framings)

*Summary of verdicts; full evidence + the RLHF seam + D1/D2 reasoning in `lodestar_positioning_assessment.md`.* The through-line: **every framing is served today by the `_reserved`-over-lattice-view model — the bottleneck is articulation, not engineering.**

| ID | Framing | Built today (adjacent) | Gap | **Verdict** |
|----|---------|------------------------|-----|-------------|
| **C-i** | **Prompting primitive** (canvas in prompt/context assembly) | Leg-2 `canvas_context` loader → `ContextGraph` with `reading_order()`/`refs()`/traversal; load+traverse **without rendering**. | No spec for canvas→prompt/context-window assembly (serialize a traversal into an ordered, budgeted block). | **spec-it** — cleanest; thin additive contract on the proven loader. |
| **C-ii** | **RLHF / feedback-signal** | **Built & live:** `canvas_core/rlhf/` (`SelectionRecord`, `backprop.py`, `iii_bridge.py::selection_to_iii_signal`, comic `_rlhf_hints.py` read-back); 13 records. **Generic & thin:** leg-3 `_reserved.interaction` `response` log + `reconcile.py` advisory draft. | The two are **unconnected**; no generic `response`→RLHF-signal bridge; the owns-vs-defers seam undocumented. **Doc/code contradiction:** `adr_006`/`spec_interface_surface §11.1` name **ISS** as RLHF-schema owner, but the live impl routes through **III's ADR-005**. | **spec-it (the seam)** — generalize the already-proven bridge; resolve ISS-vs-III ownership. |
| **C-iii** | **Pattern memorialization** (durable/versioned/discoverable reusable canvases) | Producer pattern proven 7× (`_scaffold/` + skill); `context_object` gives `id`+`version`+`refs`; external `latlab` registry doctrine. | No capture/versioning/discovery **system**; registry half is external (`latlab`), not Canvas-owned; zero consumer pressure. | **defer** — least-built, registry-dependent; building now is gold-plating ahead of demand. |
| **C-iv** | **"The" context-graph primitive** (canvas as the primitive context graphs render/edit/interact through) | The `ContextGraph` model *is* a context-graph abstraction; the three legs together *are* render/edit/interact — but **implied, never claimed** (specs keep canvas "a view of the `lattice` primitive"). | The architectural **claim** is unmade; depends on the **unwritten** `aDNA.aDNA` OIP thesis; it *is* the LIP-0009 question, whose re-open bar is unmet (D2). | **hold-open** (re-open-LIP-0009 **not yet**) — staged path's re-open target, not a now-action. |

---

## Cross-track dependencies (do-once / sequencing)

- **A4 ≡ B7** — the standard version-history is one artifact (do once; serves both publishing + docs).
- **A7 ⊂ B1** — the empty root README is the same hole from two angles; B1 closes it.
- **A2 (D3) gates v2.1.0** — and any future LIP-0009 re-open (C-iv). Resolve the governance home before either lands.
- **B5 ⟷ C-iv** — the Canvas↔Lattice integration doc is where the context-graph positioning becomes externally legible; write B5 *after* the C-iv ambition call so the doc reflects the chosen framing (view vs primitive).
- **C-i / C-ii spec-it work** rides the *existing* loader + RLHF bridge — additive, `_reserved`, firewall-safe (no `canvas_std` core change).
