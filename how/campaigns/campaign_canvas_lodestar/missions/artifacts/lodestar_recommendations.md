---
type: artifact
artifact_type: recommendations
mission_id: mission_lodestar_review
campaign_id: campaign_canvas_lodestar
created: 2026-06-30
updated: 2026-06-30
status: active
last_edited_by: agent_mondrian
tags: [lodestar, review, recommendations, follow_on, gated, docs_sprint, governance]
---

# Lodestar Recommendations

> **Deliverable 3 of 3** (Operation Lodestar P1 review). Prioritized recommendations + a **recommended follow-on**, framed as **gated options** for the operator at the P2 gate. The review builds nothing; this is the menu. R-IDs map to gaps in `lodestar_gap_register.md`; positioning calls are justified in `lodestar_positioning_assessment.md`.

## The shape of the recommendation

Canvas is **technically strong and strategically invisible**, and the operator's "core primitive" thesis is **correct and largely already built**. So the follow-on is a **documentation & articulation sprint on a strong base + a small governance unblock** — *not* a re-positioning gamble and *not* new engineering. D1 resolved (evidence-based) to **staged**: articulate now, re-position later on evidence. D2: **do not** re-open LIP-0009 now.

This sorts into **five tiers by leverage-per-cost**. The operator gates which tiers to build.

---

## Tier 0 — Quick wins (hours; do regardless of scope choice)
*Highest credibility-per-hour. Corrections, not new docs. An external reader's first impressions, fixed cheaply.*

| R | Action | Gap | Effort |
|---|--------|-----|--------|
| **R0.1** | Fix dead/wrong-repo links: `CONTRIBUTING.md` (`LatticeProtocol/adna` → `aDNA-Network/Canvas.aDNA`; dead `README.md` link), `VISION.md:149` dead link. | B4 | S |
| **R0.2** | Refresh `what/code/canvas_std/README.md` — v2.2.0, 105/10, current status (every headline number is wrong today). | A3 | S |
| **R0.3** | Fix `spec_adna_canvas_standard.md` title + H1 to **v2.2.0**; refresh stale producer names (CanvasForge→Canvas, etc.). | A1 (part) | S |
| **R0.4** | Reconcile JSON Schema `$id` to v2.2.0 (or add a note explaining the deliberate pin). | A6 | S |

---

## Tier 1 — The documentation sprint *(recommended primary follow-on)*
*Converts an invisible repo into a navigable one. Content debt is low — most prose exists internally and is lifted/repackaged.*

| R | Action | Gap | Effort | Material exists |
|---|--------|-----|--------|-----------------|
| **R1.1** | **Root `README.md`** — the external landing page (definition · three-leg thesis · "what's here" map · 5-line quickstart · links). Closes the cluster of dead `README.md` links too. | B1 | S | ~70% (`MANIFEST.md:17-23`, `canvas_std/README`) |
| **R1.2** | **Producer quickstart** — "build a canvas producer in 15 min" (assemble `_scaffold/README` + `deck_generator/README` + `skill_canvas_producer_build`). | B3 | S | ~90% — near-pure assembly |
| **R1.3** | **Canvas Standard explainer** — the "what/why" narrative (fork story · source-vs-view · `_reserved` + degradation contract · conformance levels · the substrate-neutrality boundary). | B2 | M | ~75% |
| **R1.4** | Refresh **MANIFEST.md** (post-merge identity; status through Armature) — lift *thesis*, fix *status*. | B-note | S | n/a |

**R1.1–R1.2 alone** (a half-session) move the needle most: a navigable front door + an adopt-path. R1.3 is the narrative that sells the thesis.

---

## Tier 2 — Standard-publishing hardening
*Makes "the aDNA Canvas Standard" externally citable and certifiable — the difference between "a repo" and "a published standard."*

| R | Action | Gap | Effort |
|---|--------|-----|--------|
| **R2.1** | Make `spec_adna_canvas_standard.md` citable — add an **Abstract**, a **license** (spec text CC-BY-4.0 + ref impl MIT), resolve internal `[[wikilink]]` normative refs to real citations, assign a stable identifier/namespace URL. (R0.3 did the version/names.) | A1 | M |
| **R2.2** | Author a **standard-scope version-history** (2.0.0→2.0.1→2.0.2→[2.1.0 reserved/why]→2.2.0); back-fill `[2.0.2]` into the code CHANGELOG; separate package- vs standard-version headers. (One artifact serves A4 + B7.) | A4/B7 | S-M |
| **R2.3** | Package the **conformance certification kit** — portable fixtures + `manifest.json` as a public contract + a "run-this-to-certify" runner + a guide + Core/Extended/aDNA-Native self-attestation. Raw materials already exist. | A5 | M |
| **R2.4** | Add an **external entry/index** disambiguating the Canvas Standard from the generic `what/docs/adna_standard.md`. | A7 | S |

---

## Tier 3 — Governance unblock (mostly a decision; unblocks v2.1.0)
*This is the one item that is genuinely **blocked** today, and it gates both v2.1.0 and any future LIP-0009 re-open.*

- **R3.1 — Stand up a Canvas-local LIP home.** Adopt `who/governance/lips/` as the **ratification venue** for Canvas-Standard LIPs (the CC0 `lip_0001` process doc is freely forkable). Rationale: Canvas is the standard-bearer that *owns* the Standard's governance; this removes the dead dependency on the archived `lattice-labs`. Re-point `adr_003_standard_governance.md §2` at the new home. **[A2/D3]**
- **R3.2 — Resolve the LIP numbering (the one piece that needs the operator/FA).** Two options:
  - **Global sequence + registrar** — keep one network-wide LIP history; `aDNA.aDNA` acts as the **number registrar** (it already governs the framework standard), Canvas holds content + ratification. *Pro:* single coherent LIP history. *Con:* a cross-vault allocation step.
  - **Per-standard namespace** — Canvas mints Canvas-scoped LIPs under its own prefix (e.g. `CLIP-`/`CANVAS-LIP-`), fully self-contained. *Pro:* clean isolation, no registrar. *Con:* fragments the network's single LIP sequence.
  - *Recommendation:* **global + `aDNA.aDNA` registrar** — it preserves one history and matches the existing "standard-evolution routes to aDNA.aDNA" hook; but this is genuinely the operator's/FA's call.
- **R3.3 — Once R3.1/R3.2 land, advance LIP-0008 → Final and cut Standard v2.1.0** (the A-5 relaxation). LIP-0009 records the Option-V deferral (per D2).

---

## Tier 4 — Positioning spec-it *(staged; additive; firewall-safe — no `canvas_std` core change)*
*The articulation that turns "buried capability" into "named Standard capability." Rides the existing loader + RLHF bridge. Best done after Tier 1 gives them an external home.*

- **R4.1 — Spec the prompting primitive (C-i).** A thin *canvas → prompt/context-assembly* contract on the proven leg-2 `canvas_context` loader (serialize a traversal into an ordered, budgeted context block). Cleanest of the framings.
- **R4.2 — Spec the RLHF seam (C-ii).** Name the **Canvas-owns-capture-substrate / III-owns-signal-schema** boundary; generalize the *already-proven* `selection_to_iii_signal` bridge to the generic leg-3 `response` log; **resolve the ISS-vs-III ownership contradiction** (docs say ISS, code routes III). This surfaces Canvas's most differentiated story — the working Canvas-as-RLHF-surface.
- *(C-ii feeds the eventual evidence base; both are served by the view model and do **not** themselves trigger a LIP-0009 re-open.)*

---

## Deferred / hold-open (do **not** build now)

- **C-iii Pattern memorialization — defer.** Least-built, registry-dependent (`latlab`, not Canvas-owned), zero consumer pressure. Building now is gold-plating. *(If a concrete consumer needs to publish/pull/federate canvases as first-class registry entities, that is also the LIP-0009 re-open evidence — revisit then.)*
- **C-iv Canvas-as-primitive / LIP-0009 re-open — hold-open.** Bar unmet (D2); depends on the unwritten `aDNA.aDNA` OIP thesis. Keep the trigger legible; revisit on concrete consumer evidence. *(The deferred OIP `v1.x` re-anchor stub `idea_oip_v1x_interface_reanchor` is the existing tracking seam.)*

---

## Decisions the operator still owns (the P2 gate)

1. **Scope** — which tiers to build? *Recommended: Tier 0 + Tier 1 now (the docs sprint); Tier 2 + Tier 3 as a close second; Tier 4 staged after; C-iii/C-iv deferred.*
2. **D3 numbering** — global+`aDNA.aDNA` registrar (recommended) vs per-standard prefix? (Gates R3.x → v2.1.0.)
3. **D2** — accept "no LIP-0009 re-open" (recommended) or override.
4. **B6 / Canvas VISION** — replace the generic `VISION.md` vs add a `VISION_canvas.md` alongside it? (Deferred into the sprint; flag the preference.)
5. **Follow-on vehicle** — charter the sprint as a new campaign (e.g. "Operation Lighthouse-Canvas"/"Operation Beacon"), or run it as standalone missions under Canvas? *(Recommend a small campaign: it spans ~3–6 missions across Tiers 0–2.)*

## Recommended follow-on (one line)

> **Charter a focused documentation-&-publishing sprint** = Tier 0 (quick wins) + Tier 1 (README · producer quickstart · explainer) + Tier 3 (governance unblock → v2.1.0), with Tier 2 hardening and Tier 4 spec-it as a planned second wave. It is the highest-leverage work, it is mostly *repackaging* a strong base, and it *builds the evidence* that a future canvas-as-primitive claim would need.
