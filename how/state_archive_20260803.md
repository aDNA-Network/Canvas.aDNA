---
type: archive
subtype: state_history
vault: Canvas.aDNA
title: "STATE.md banner-stack archive — closed campaign banners + Keystone E-phase build history"
created: 2026-08-03
archived_from: STATE.md
archived_by: "Context.aDNA / Prometheus — Operation Handfire Phase B sitting 1 (attended-apply, operator GO + WARM caveat 2026-08-03)"
source_memo: "Context.aDNA/who/coordination/coord_2026_07_12_prometheus_to_fleet_state_refresh_tail_tier.md (P1/P2/P3)"
tags: [archive, state_history, canvas, handfire]
---

# Canvas.aDNA — STATE.md banner-stack archive

**Relocated verbatim, nothing deleted (SO-3/SO-7).** These are the closed campaign banners and closed build
history that previously sat in the always-loaded `STATE.md` (~85% of the file was a reverse-chron closed-banner
stack sitting above a *stale* Resume-Here).

**Two live-correctness fixes were made in `STATE.md` BEFORE anything moved:**

1. **HOIST** — the closed 2026-07-02 Beacon banner (archived below as P3) carried the **only copy** in the
   whole file of the live Canvas Standard pins (**v2.3.0** · `canvas_std` **115/10** · certification
   **11/11**) and of the open **D3 Rosetta-registrar ack** tail. Verified by grep: those strings appeared on
   that line and nowhere else. They were lifted into a live pins block beside the Halftone banner first.
2. **REPOINT** — `## ▶ Resume Here` announced **Operation Armature**, closed 2026-06-23, while the live
   campaign has been **Operation Halftone** since 2026-07-09. Repointed.

Applied under the **WARM caveat** (vault HEAD 3 h old at apply time; `STATE.md` itself 4 weeks stable and
byte-identical to its scan baseline, so line anchors held). The in-flight
`how/sessions/active/session_stanley_20260709_135234_halftone_charter_h1.md` was left untracked — the owner's
to commit.

## P3 — top closed banners (former L17–36, verbatim)

> **▶ 2026-07-02 — ✅ OPERATION BEACON COMPLETE — CAMPAIGN CLOSED (Mondrian, `session_stanley_20260702_204459_beacon_b4_governance`).** All four human-gated phases of `campaign_canvas_beacon` (Canvas Standard publish-hardening & governance unblock) shipped on a green base. **B1** quick-wins · **B2** docs (root README · MANIFEST · producer quickstart · Standard explainer · VISION replaced) · **B3** publishing (citable spec [Abstract/CC-BY-4.0/identifier/resolved refs] · standard-scope version-history · **certification kit** · specs index) · **B4** governance unblock: stood up Canvas-local **`who/governance/lips/`** (forked CC0 `lip_0001` + template · migrated LIP-0008/0009 live from the archived `lattice-labs` registry) · re-pointed the dead `adr_003 §2`/`adr_000` refs via a dated Amendment · staged the **Rosetta (aDNA.aDNA) registrar coord memo** (D3, pending ack) · and (the B4 investigation confirmed the A-5 relaxation was **not** in v2.2.0) **implemented LIP-0008** (`reserved.py::validate_panel_link`: `role: derived` surfaces MAY be pure metadata / omit `id`) **+ cut it into Canvas Standard v2.3.0** (the reserved **2.1.0 slot superseded** — never cut; MINOR atop the Armature 2.2.0 line). **LIP-0008 → Final** (landed v2.3.0); **LIP-0009 → Final** (Option V, no re-open, D2). **End state:** Standard **v2.3.0**; `canvas_std` **115/10**, certification **11/11**; firewall clean (B4.2 = one reviewable `reserved.py` touch; `validate.py`/`schema.py` untouched). Commits: B4.1 governance `b344968` · B4.2 v2.3.0 + close (this session). **Open tail (non-blocking):** D3 **Rosetta registrar ack** (`#needs-human`); on ack, flip `adr_003` Amendment 1 + `lip_registry` "pending" → ratified. **Named second wave:** Tier 4 spec-it (prompting primitive · RLHF seam). Close records: `campaign_canvas_beacon.md` §Completion Summary + §Campaign AAR; `missions/mission_beacon_tier3_governance.md` §AAR. **No active campaign** — next work is operator-directed.
>
> **▶ 2026-06-30 — OPERATION BEACON — B1–B3 phase-log (superseded by the Beacon-COMPLETE banner above; retained for build history) (Mondrian, `session_stanley_20260630_164238_beacon_charter_tier0`).** Lodestar **closed at its P2 gate** (box below); the operator gated the **build** → chartered **`campaign_canvas_beacon`** — Canvas Standard **publish-hardening & governance unblock**. **Scope locked: Tier 0+1+2+3** (full hardening): **B1** quick-wins (links · canvas_std README · spec title/names · schema `$id`-note) · **B2** docs sprint (root README · MANIFEST · producer quickstart · Standard explainer) · **B3** publishing hardening (citable spec · standard-scope version-history + `[2.0.2]` · conformance cert kit · external index) · **B4** governance unblock (stand up Canvas-local `who/governance/lips/` → migrate LIP-0008/0009 → reconcile the 2.1.0 slot). **Decisions:** D3 = **global + `aDNA.aDNA` registrar**; D2 = **accept no LIP-0009 re-open** (record Option-V in the new home). **Pre-build done:** Lodestar review committed+pushed `9f49a6e` (operator-gated; +3 completed ADR-045 federation commits rode the same push). ⚠ **2.1.0 = a reconciliation, not a naive cut** — the Standard already ships **v2.2.0**; the LIP-0008 A-5 relaxation can't be retro-inserted (resolved in B4). **B1–B3 shipped:** Tier 0 quick-wins (links · canvas_std README v2.2.0/105-10 · spec title/H1 · schema `$id` `$comment`) · Tier 1 docs (root `README` · `MANIFEST` refresh · producer quickstart · Standard explainer · **VISION replaced**) · Tier 2 publishing (**citable spec** [Abstract/identifier/CC-BY+MIT/resolved refs] · CHANGELOG version-history + `[2.0.2]` · **certification kit** `certify.py` **CERTIFIED 10/10** · `specs/README` index). **Harness 105/10 throughout; firewall clean** (no `src/canvas_std/*.py`); pushed through `465fbc2` (+ B3 `c79ac58`). **▶ NEXT = B4 (Tier 3, CROSS-VAULT governance unblock):** stand up a Canvas-local `who/governance/lips/` (fork CC0 `lip_0001` · migrate `lip_0008`/`lip_0009` from `Archive.aDNA/lattice-labs` · re-point `adr_003 §2`) · **Rosetta registrar coord memo** (D3: global+`aDNA.aDNA` registrar) · **reconcile the reserved 2.1.0 slot** (is LIP-0008's A-5 relaxation already in v2.2.0?) + LIP-0008→Final + LIP-0009 Option-V. Phases human-gated (SO-1). Charter: `how/campaigns/campaign_canvas_beacon/`; source of truth = Lodestar's 3 deliverables + B4 detail in the mission's Next-Session Prompt.
>
> **▶ 2026-06-30 — ✅ OPERATION LODESTAR COMPLETE — CLOSED AT P2 (superseded by Operation Beacon above) (Mondrian, `session_stanley_20260630_145035_lodestar_review`).** `campaign_canvas_lodestar` (review-and-recommend). **P0 ratified** (D1=let-the-review-recommend · D4=assessment-only · D2/D3=recommend-don't-decide) → **P1** three-track read-only review run (A technical · B docs · C positioning) → **3 deliverables landed**: `how/campaigns/campaign_canvas_lodestar/missions/artifacts/lodestar_{gap_register,positioning_assessment,recommendations}.md`. **Findings:** technical baseline **GREEN** (canvas_std **105/10** · canvas_context **58** · 7 producers **223** = **386 passed / 10 skipped**; firewall git-diff 0) but the Standard is **externally invisible + under-articulated**; the operator's "core primitive" thesis is **correct and largely already built** (incl. a buried, *operational* Canvas-as-RLHF surface — 13 live records). **Positioning verdicts:** (i) prompting-primitive **spec-it** · (ii) RLHF-seam **spec-it** · (iii) pattern-memorialization **defer** · (iv) canvas-as-primitive **hold-open**; **D1 = staged**, **D2 = NO LIP-0009 re-open** (bar's "demonstrably cannot serve" prong contradicted by 6 shipped campaigns). **Recommended follow-on:** a docs-&-publishing sprint (Tier 0 quick-wins + Tier 1 README/quickstart/explainer) **+** the governance unblock (Tier 3 → stand up a Canvas-local LIP home → v2.1.0). **✅ P2 RESOLVED** — operator chose **Tier 0–3** (full hardening) · new campaign **Operation Beacon** (`campaign_canvas_beacon`) · **D3 = global+aDNA.aDNA registrar** · D2 = accept no-reopen. Build now runs in the Beacon banner above. *⚠ Corrections to prior STATE numbers: the Standard suite is **386/10** (not the "~319" cited at Armature); **9** specs (not 10); a code CHANGELOG **exists** but omits `[2.0.2]`.*
>
> **▶ 2026-06-30 — POST-ARMATURE · Hearthlight-standdown currency notes (Mondrian, cross-session; superseded as "current campaign" by Lodestar above, retained for context).** Canvas's own campaigns are all closed (Armature ✅ 2026-06-23, below). Four updates since the last STATE write:
> - **Hearthlight P4 Wave-1 shipped Canvas's home page** — `HOME.md` + `home_config.yaml` + masthead `who/assets/banners/banner_canvas.png`, generated by `build_home.py` v0.1.5 (`convergence_qa` platform/command_center **9/9**), **operator eye-gate approved 2026-06-29** (`a93c083` descriptor + banner · `520911b` HOME.md). `HOME.md` is machine-owned now — regenerate via `home_config.yaml`, don't hand-edit. *(Hearthlight is a `Home.aDNA` fleet campaign: `Home.aDNA/how/campaigns/campaign_fleet_home_pages/`.)*
> - **lattice-labs archived 2026-06-27** (Operation Drydock M05) → `Archive.aDNA/lattice-labs` (reader-only-historical; `~/aDNA/lattice-labs` back-compat shim). The LIP files this STATE references now live at `Archive.aDNA/lattice-labs/how/governance/lips/`; the historical `lattice-labs/...` paths below resolve via the shim (not rewritten).
> - **⚠ LIP-0008 → Canvas Standard v2.1.0 — OPEN; needs a LIP-governance-home decision.** LIP-0008 (A-5 "derived surface = pure metadata" relaxation) + LIP-0009 (canvas-as-primitive deferral) opened Review 2026-06-20 (earliest close 2026-06-27, **now lapsed**), but both sit frozen `status: review` in the **archived** lattice-labs registry and **no successor LIP-governance home exists** post-archival. Before v2.1.0 can be cut (land A-5 at `what/code/canvas_std/.../reserved.py::validate_panel_link` + conformance A-5 + `spec_panel_link_semantics §5.2`), the operator/FA must decide where LIP Final-decisions route. Disposition: `what/decisions/lip_queue_disposition.md`.
> - **Hearthlight Tier B (2026-06-30) is Home/Hestia-driven** — Canvas is not re-involved (its part closed in Wave-1). The rollout's open items (LatticeProtocol/zeta `.obsidian` reseed · the `build_home.py` `CLASS_ALIASES` F1 add · the Venus/Wave-3 poll) are Home/Seshat/Venus-owned, tracked in `Home.aDNA`.
>
> *Operation Lodestar (P2 gate, top banner) reviewed exactly this open-work list and recommends: LIP-0008→v2.1.0 unblocks by standing up a Canvas-local LIP home (R3.x/D3); a docs-&-publishing sprint is the recommended primary follow-on; the PT P5 tail stays Hestia-owned; the OIP `v1.x` re-anchor stays deferred. Armature/Keystone build history retained below.*

> ✅ **OPERATION KEYSTONE COMPLETE (2026-06-20).** The aDNA Canvas Standard v2.0.0 shipped as running infrastructure
> (reference impl + parity-gated floor migration + 3 in-vault consumers, no regression); E6 validated + cutover
> confirmed + campaign closed (operator disposition: complete-with-PT-P5-tail). **Authoritative close record:**
> `how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis.md` §Completion Summary + §Campaign AAR. **Open tail
> → PT P5 + LIP queue:** `how/campaigns/campaign_canvas_genesis/missions/artifacts/e6_3_handoff_register.md`. The
> dense sections below are retained as build history.

## P1 — stacked closed banners under Resume Here (former L49–290, verbatim)

> **🟢 OPERATION ARMATURE — P2 (prior phase; the campaign is now CLOSED — see the Resume-Here line above) (`session_stanley_20260623_105436_armature_p2_firewall_touch`).**
> Crossed the **P1→P2 gate** on operator approval and executed the firewall touch under ratified `adr_007` — the first
> `canvas_std` edit since Keystone (6 campaigns of git-diff 0). **Wiring:** `reserved.py::validate_interaction(reserved, doc)`
> realizes `I-1`/`I-2`/`I-3` over `_reserved.interaction` (doc-path only — no `ContextGraph` import; a 2-part-tolerant
> `_INTERACTION_SEMVER`; **does not** re-run `validate_anchors`, which `validate_reserved` already does — no double A-5);
> dispatched on the aDNA-Native `validate()` path, surfaced through `validate_suite` + the CLI; re-exported from
> `__init__`. New `tests/fixtures/adna_interaction.canvas` (4 affordance kinds) + manifest row + `tests/test_interaction.py`
> (16: valid e2e · I-2 orphan · I-3 bad value · D-1 strip→Core · the no-double-A-5 guard · CLI 0/1). The consumer
> `canvas_context.validate_interaction_block` is now a **thin delegate** to `canvas_std.validate_interaction` (dropped the
> duplicated logic + the dead `_SEMVER`/`re`; `canvas_context` **0.3.0 → 0.3.1**). **Version cut:** `2.0.2 → 2.2.0` at
> `STANDARD_VERSION` · schema `title` + `x-standard-version` (kept `$id`) · `conformance.py` ×3 · `test_smoke` ×2 +
> `test_conformance` ×1 · the 9 spec frontmatters + the `spec_federation_contract` example · both CHANGELOGs; forward-pointers
> flipped (`spec_conformance_suite §4.1`, `spec_interface_surface §9.1/§10` + status block + Q7). Fixtures' `adna_version`
> stays `2.0.0` (additive layer — producers unaffected). **Verified (the P2 exit gate, full regression):** `canvas_std`
> **105/10** · `canvas_context` **58** · 7 producers **223** (brief 10 · deck 16 · document 37 · diagram 36 · comic 87 ·
> letter 17 · post 20) · `canvas-std 2.2.0` CLI → interaction golden `adna_native [OK]` (D-1/D-2/D-3) · `ruff` clean both.
> P0+P1 were committed first (two clean commits) to isolate the firewall diff. **Deviations from the approved plan:** also
> bumped `canvas_context.STANDARD_VERSION → 2.2.0` + package `0.3.1` (plan flagged this optional; done for vault-wide
> coherence). **Pre-existing finding (P3 doc-currency):** the `canvas_std` CHANGELOG had no `[2.0.2]` entry (the AT-1/AT-2
> cut bumped strings only); the new `[2.2.0]` entry bridges from 2.0.2. ⛔ **HELD at the P2→P3 gate** — push operator-gated
> (Git-Ops §3); nothing pushed. The boxes below are prior history (P0/P1, Salon close, Palette/Atelier/Keystone).

> **🟢 OPERATION ARMATURE — P0 RATIFIED + P1 BUILT (prior phase, `session_stanley_20260622_193153_armature_scaffold_p0`; superseded by the P2 box above).**
> Graduated the Salon follow-on stub (`idea_campaign_leg3_interface_runtime`) into a **build** campaign (Keystone model;
> P0–P3, human-gated). **P0:** scaffolded + authored the **8-decision record** + **`adr_007`** (the leg-3 firewall-touch
> ADR — the inverse of Salon's firewall-preserving D6; lift bounded to P2, the P2 gate becomes **full regression**), then
> the operator (on request for recs) **ratified all 8 + `adr_007` at the agent's recommended values** (D5 extend
> `canvas_context`; D6 cut `interaction_version 1.0` → v2.2.0 by maintainer discretion). **P1 (built this session):** the
> governed **advisory-reverse** write runtime — `what/code/canvas_context/src/canvas_context/reconcile.py`
> (`reconcile` = staleness gate §3.2 + topology `diff` + three-way `merge` draft + **§6 lossy-field restore** + the
> interaction response payload; `governed_apply`; `write_source_draft`), all over `canvas_std.roundtrip` **read-only**;
> `canvas_context` **0.2.0 → 0.3.0**. A response advances the view → reconciles to a **reviewed source draft**, **never a
> silent write** — the headline test asserts the on-disk authoritative source is **byte-unchanged**. Source fixture
> (`review_request.source.json`, topology-matched to the view) + 8 tests + a runnable pilot. **Verified:**
> `canvas_context` **58 passed** (50 + 8), `ruff` clean; `canvas_std` **82/10 unchanged**; **firewall `git status -s --
> what/code/canvas_std/` git-diff 0**; pilot closes the loop, source byte-unchanged. ⛔ **HELD at the P1→P2 gate** — P2 is
> the **`adr_007` firewall touch** (wire `I-1/I-2/I-3` into `canvas_std/validate.py` reusing `validate_anchors` + cut
> `interaction_version 1.0` → Standard **v2.2.0**); the P2 gate is full regression, **operator approval required to
> cross**. Approved plan: `~/.claude/plans/please-read-the-claude-md-glimmering-teapot.md`. The boxes below are prior
> history (Salon close, Palette/Atelier/Keystone).

> **✅ OPERATION SALON COMPLETE — CAMPAIGN CLOSED (this session, `session_stanley_20260622_175728_salon_p5_close`).**
> P5 (`mission_p5_close`) ran validation + close — the operator continued the campaign past the P4→P5 gate. Filled the
> campaign **Completion Summary + Campaign AAR**; authored the committed follow-on as a **backlog idea stub**
> (`how/backlog/idea_campaign_leg3_interface_runtime.md` — the deferred leg-3 *runtime* build: governed `.lattice.yaml`
> round-trip write + `I-*` into the `canvas_std` harness + the `interaction_version 1.0` Standard-version cut + the
> `v1.x` OIP re-anchor); **graduated** the patterns → `what/context/context_canvas_surface_legs.md`
> (compose-not-extend · load-without-rendering · view-only append-fold); doc currency done (STATE + root CLAUDE.md).
> **Verified at close:** `canvas_context` **50 passed** (28 leg-2 + 22 leg-3); `canvas_std` **82/10 unchanged**; `ruff`
> clean (both); CLI `canvas-std 2.0.2` → interaction golden `adna_native [OK]` (D-1/D-2/D-3); **firewall `git status -s
> -- what/code/canvas_std/` git-diff 0** (P5 is docs-only — no code touched). No producer example shipped → structural
> `iii/` review **N/A**. Campaign `status: completed`; the three Salon specs already indexed; the follow-on + the new
> context guide indexed. **⛔ Operator-gated (outward):** commit + push (repo ahead 5; GitHub-public standard-bearer,
> Git-Ops §3) — HELD for authorization. The boxes below are prior history (P4/P3/P1–P2, Palette/Atelier/Keystone).

> **⚒ OPERATION SALON — P4 COMPLETE → LEG-3 POC BUILT + DEMONSTRATED (this session, `session_stanley_20260622_164829_salon_p4_interaction_poc`).**
> Operator chose **build P4** at the P3→P4 gate (HOLD at P4→P5 after). Built the stretch POC as a **read-only extension
> of `canvas_context`** (spec §10.2): a new additive sibling **`interaction.py`** that *composes* the leg-2
> `ContextGraph` (an `InteractionSurface` *has-a* `ContextGraph` — leg-2 code byte-unchanged) with two clearly-separated
> halves — **reader** (`load_interaction_surface` / `affordances()` / `surface_state()` / `validate_interaction`) +
> **reducer** (`apply_response` — a pure **append-only** fold that logs a response and recomputes `state`, IX5/IX6,
> advancing the *view* only, §7.2). First **code realization of the `I-*` family** (I-1/I-2/I-3 reusing
> `canvas_std::validate_anchors`; I-D `is_round_trip_safe` + `strip_interaction` reusing `canvas_std.strip`/`validate`)
> — housed in the **consumer**, NOT wired into the `canvas_std` harness (firewall). **Interaction-bearing golden**
> (`tests/fixtures/interaction_review.canvas`, self-validating generator) declares one affordance of each of the **4
> kinds** (`input`/`choice`/`annotation`/`action`), both anchor-binding forms. **22 new tests** (I-1/I-2/I-3 · the
> loop proof + no-render assertion · I-D) + a runnable on-disk demo (`pilot_interaction_loop.py`). Boundary held: **not**
> a capture runtime (ISS), renderer, or transport; the governed round-trip write (`.lattice.yaml`) stays out of scope
> (`spec_roundtrip_protocol_v2`). Mission `completed` (+AAR); campaign P4 row → completed. **⛔ HELD at the P4→P5 gate.**
> **`canvas_std` firewall git-diff 0.** Approved plan: `~/.claude/plans/please-read-the-claude-md-goofy-whistle.md`. The
> boxes below are prior history (P1/P2/P3, Palette/Atelier/Keystone).

> **⚒ OPERATION SALON — P3 COMPLETE → LEG-3 SPEC RATIFIED (prior session, `session_stanley_20260622_153722_salon_p3_interface_surface`).**
> The operator (plan-mode) chose **proceed first-principles** + **concrete shape + `I-*` checks** after I surfaced that
> the external "OIP/interface thesis" doc ADR-000 named to ground leg 3 **does not exist** (a future deliverable of the
> unopened `aDNA.aDNA` OIP-unification campaign; the P3 gate explicitly allows "ratified **or** deferred", and ratified
> **D4** already scoped leg 3 **spec-only**). **Authored** [[what/specs/spec_interface_surface|spec_interface_surface.md]]
> (`status: draft`) — a canvas as a **human↔AI / human↔human interaction surface**, **as a contract bounded by
> [[what/decisions/adr_006_canvas_surface_boundary|adr_006]]** (no routing — the §3 load-bearing line; no engine; no
> transport; rides `_reserved.interaction` additively). Core: interaction = a **`read → act → re-read` loop** over the
> proven leg-2 `ContextGraph`; **five primitives** (`anchor` · `affordance` · `response` · `surface state` · `turn`);
> concrete additive `_reserved.interaction` shape; **IX1–IX6**; the **round-trip-to-baseline** headline property;
> proposed **`I-*`** conformance family (parallels `A-5`/`A-7`; folds into the suite *at ratification*). Reuses, not
> reinvents: `anchor` = `panel_link.anchors` (orphan check `validate_anchors`); read step = leg-2 load; state = leg-2
> graph. **D8 memos filed** (`who/coordination/coord_2026_06_22_mondrian_to_{oip,iss}_canvas_interface_seam.md`;
> canonical in Canvas, cross-post into `aDNA.aDNA` operator-gated). **RATIFIED same session** (operator: "Approved", at
> all 9 default open-question resolutions) → spec `status: ratified` (+ RATIFIED banner; open-questions → resolved-
> decisions log); **`I-*` family folded into `spec_conformance_suite.md` §4.1** (additive/optional; `interaction_version
> 1.0`; degradation via §5; validator-impl forward-pointed, reuses `validate_anchors`; Standard-version cut deferred);
> mission `mission_p3_interface_surface_spec` **completed** (+AAR); campaign **P3 row → completed**. **➤ Canvas
> three-leg thesis COMPLETE** (1+2 proven, 3 ratified). **`canvas_std` firewall git-diff 0** (spec-only; no code).
> **⛔ HELD at the P3→P4 gate** — P4 (stretch POC) operator-gated; next is P4 *or* P5 close. Approved plan:
> `~/.claude/plans/please-read-the-claude-md-misty-sonnet.md`. The boxes below are prior history (P1/P2, Palette/Atelier/Keystone).

> **⚒ OPERATION SALON — P1 RATIFIED + P2 COMPLETE → LEG 2 PROVEN (prior session, `session_stanley_20260622_143651_salon_p1_ratify_p2_loader`).**
> **P1:** operator ratified the leg-2 loading/traversal spec
> [[what/specs/spec_canvas_context_loading|spec_canvas_context_loading]] **as drafted** — now the binding leg-2
> contract (abstract context-graph model + normative **L1–L7 load pipeline** + traversal read-contract + resolver
> interface + conformance), bounded by [[what/decisions/adr_006_canvas_surface_boundary|adr_006]] (contract + reference
> loader, **never** runtime/transport/router). Spec `status: ratified`; mission P1 `completed` (+AAR). **P2 (built same
> session, operator: "build P2 now"):** the leg-2 reference loader `what/code/canvas_context/` — a **new sibling**
> importing `canvas_std` **read-only via pythonpath** (D6 firewall preserved) — `model` (§3) · `loader` (L1–L7) ·
> `resolver` (§5) · `traversal` (§6). **Pilot proof:** `canvas_standard_whitepaper.canvas` (32 nodes / 23 edges,
> adna_native) loads as a `ContextGraph` — identity resolved, `reading_order() == [page0..page4]`, 4 wikilink refs,
> L3 overlay, file-by-reference — **with no render pipeline invoked** (PIL/cairosvg never imported); 2nd producer
> (`grant_proposal`) loads identically. **`canvas_context` 28/28, ruff clean; `canvas_std` firewall git-diff 0 + its
> suite 82p/10s (no regression).** Mission P2 `completed` (+AAR). **⛔ HELD at the P2→P3 gate** — next is **P3** (leg-3
> interface-surface spec, greenfield; risk-gated on the external OIP/interface thesis doc). Firewall check is `git
> status -s -- what/code/canvas_std/` (canvas_std is part of Canvas.aDNA's git, not a nested repo). Approved plan:
> `~/.claude/plans/please-read-the-claude-md-floating-pumpkin.md`. The boxes below are prior history (Palette/Atelier/Keystone).

> **✅ OPERATION PALETTE COMPLETE — CAMPAIGN CLOSED (this session, `session_stanley_20260622_005329_palette_p4_close`).**
> Post-Atelier (no active campaign), the operator asked for a cross-campaign AAR/review; a 3-sweep retrospective
> (Cartography → Keystone → Atelier) confirmed all three hit charter and the *output* leg of the thesis is proven
> (5 producers, Standard untouched), but surfaced two Mondrian-owned gaps: **output coverage is incomplete** (letter
> only spec-sketched `§6.3`; post unspec'd) and the **producer pattern is proven 5× but isn't a reusable factory**.
> Operator chose follow-up **Option A** (complete output family + harden factory) over canvas-as-surface (B, deferred)
> and adoption-readiness (C, gated). Chartered **Operation Palette** (`how/campaigns/campaign_canvas_palette/`,
> `status: completed`): **P0** ✅ 6 decisions · **P1** ✅ factory (`skill_canvas_producer_build.md` +
> `what/production/_scaffold/`) · **P2** ✅ `letter_generator` 17/17 · **P3** ✅ `post_generator` 20/20 (single + thread)
> · **P4** ✅ close — cross-producer sweep **305 passed** (7 producers 223 + `canvas_std` 82), `iii/` review
> `iii/feedback_2026_06_22_palette_producers.md` **0 High / 0 Med**, pattern doc graduated 5×→7×, doc currency done;
> **`canvas_std` firewall git-diff 0** throughout. **7 in-vault producers green** (brief · deck · document · diagram ·
> comic · letter · post) — the thesis output family is complete. **No active campaign.** Candidate next strategic
> campaign: **canvas-as-surface** (the context-object + interface legs — needs a boundary ADR vs ISS/Astro/Terminal).
> External tracks unchanged: **LIP-0008/0009** (FA, closes 2026-06-27 → v2.1.0); **PT P5** (Hestia). Close record:
> `how/campaigns/campaign_canvas_palette/campaign_canvas_palette.md` §Completion Summary. Approved plan:
> `~/.claude/plans/please-read-the-claude-md-sleepy-minsky.md`. The boxes below are prior history (Atelier/Keystone).

> **✅ ATELIER ERRATA AT-1/AT-2 RESOLVED → CANVAS STANDARD v2.0.2 (this session,
> `session_stanley_20260621_221625_atelier_errata_v202`).** Post-Atelier (no active campaign), the operator chose
> "Resolve Atelier errata." Both spec-gap errata resolved as **editorial clarifications (PATCH; `adr_003` §2 —
> maintainer-discretion, no LIP)** + shipped in **v2.0.2**: **AT-1 (option ii)** — `extent` is **OPTIONAL**; a
> non-paginated single-surface region (`pagination: none`, e.g. a diagram/graph) legitimately omits it; **no
> `graph`/`nodes` unit added** (a node-graph is sized by content, not paged — would conflate pagination with graph
> size). **AT-2 (option i)** — the `surface` subclass label (region `surface` + `surfaces[].surface`) is an **OPEN,
> producer-defined vocabulary**; **no enum added** (a closed enum would force a LIP per new producer). **No
> validator-behavior change** — both make explicit what the reference impl already does (`extent` checked only when
> present; `surface` never enum-checked). Edits: `spec_panel_link_semantics §4/§5.2/§6` + errata banner; doc-comments
> in `reserved.py`; **2 regression tests** (`test_anchors.py::test_at1_*`/`test_at2_*`). **v2.0.2 cut** mirrors the
> v2.0.1 sites (`STANDARD_VERSION` · schema `title`+`x-standard-version`, **`$id` unchanged** · `conformance.py` ·
> `test_smoke`/`test_conformance` · 7 spec `standard_version` frontmatters + the federation example); fixtures'
> `adna_version` stays `2.0.0`. **Verified:** `canvas_std` **82/10** (+2) + ruff clean; CLI `2.0.2`; **5 producer
> suites green** (brief 10 · deck 16 · document 37 · diagram 36 · comic 87) + all 6 examples `adna_native [OK]`;
> **firewall:** validator logic untouched (`reserved.py` git-diff = comments only). **Errata queue fully drained**
> (B1–B4 + AT-1/AT-2). Disposition: `what/decisions/lip_queue_disposition.md` §Closeout — AT-1/AT-2. **No new
> campaign; Atelier stays closed.** **Tail unchanged:** LIP-0008/0009 FA review closes **2026-06-27** (→ v2.1.0 on
> LIP-0008 Final); PT P5 Hestia-owned. **Pushed `64a338f` 2026-06-21** (`9eae4f6..64a338f`, operator-authorized). The
> boxes below are Atelier build history.

> **✅ OPERATION ATELIER COMPLETE — CAMPAIGN CLOSED (this session, `session_stanley_20260621_210130_a3_validation_close`).**
> Phase **A3** ran validation & close: final sweep **266 passed** (canvas_std 80/10 · brief 10 · deck 16 · document 37
> · diagram 36 · comic 87); `canvas_std` firewall git-diff 0. Structural `iii/` review filed
> (`iii/feedback_2026_06_21_atelier_producers.md`) — **0 High / 0 Med**, 2 Low; 2 spec-gap errata (AT-1 graph extent
> unit · AT-2 free-form `surface` vocabulary) → LIP queue (`what/decisions/lip_queue_disposition.md` §Atelier
> addendum). Producer pattern **graduated** → `what/context/context_canvas_producer_pattern.md` (indexed in
> `what/context/AGENTS.md`). Campaign + all 4 missions (A0.1 · A1.1 · A2 · A3) `status: completed`; Completion Summary +
> Campaign AAR filed. **Net result: both production layers Canvas absorbed at pt09 (diagram + comic) are now real +
> green on `canvas_std` — all 5 in-vault producers (brief · deck · document · diagram · comic) conformant.** **Open
> items ride existing tracks (no new campaign):** AT-1/AT-2 → LIP queue · pixel render/scoring → PT P5
> (`canvas_presentation`) · image rendering → ComfyUI. **Keystone tail unchanged:** LIP-0008/0009 review closes
> 2026-06-27; PT P5 Hestia-owned. The boxes below are A1/A2 build history.

> **⚒ ATELIER A2 COMPLETE — COMIC PRODUCER BUILT (this session, `session_stanley_20260621_202519_a2_comic_build`).**
> Operator cleared the A1→A2 gate ("proceed to A2"); Phase **A2** built **`what/production/comic_generator/`** on
> `canvas_std` (the 5th in-vault producer; ~1,790 src LOC, ~60% **ported** from the `canvas_comic` quarry — 6-layer
> prompt assembly · panel-grid layout · tables; only the canvas construction rewritten). Multi-page/spread
> **aDNA-Native**: `comic_root` group = one canonical surface; spread + page nested-group `region`s (`extent.unit:
> pages`); panels = `image`-class `file`/`text` nodes; `sequence` (pages, acyclic) / `reading_order` (page Z-path) /
> `adjacency` (gutters) edges; `isStartNode` on page 0. **Image boundary preserved** — the assembled prompt rides in
> `component_types[panel].qualities.image_prompt`; **no rendering** (no ComfyUI/torch/PIL import); ComfyUI keeps pixels.
> **Scope D5:** data-driven engine; the SS issue is the worked example only (`examples/`). **Verified independently:**
> comic **87/87** + ruff clean; CLI build+validate `adna_native [OK]` + degradation D-1/D-2/D-3; **no regression**
> (canvas_std 80/10 · brief 10 · deck 16 · document 37 · diagram 36); `canvas_std` firewall git-diff 0. **⛔ HELD at the
> A2→A3 gate** — A3 = cross-producer validation + structural `iii/` review of both new examples + LIP-queue errata (the
> diagram `PL_EXTENT_UNITS` gap + the comic `surface`-token note), then campaign close. **All 3 pt09-absorbed production
> layers (deck · diagram · comic) are now real + green on `canvas_std`.**

> **⚒ ATELIER A1 COMPLETE — DIAGRAM PRODUCER BUILT (this session, `session_stanley_20260621_194755_a1_diagram_build`).**
> Operator **ratified all 6 A0 decisions** (defaults) → campaign `status: active`; then Phase **A1** built
> **`what/production/diagram_generator/`** on `canvas_std` (the 4th in-vault producer; ~656 src LOC): a substrate-free
> `DiagramInput` → a v2.0.0 **aDNA-Native** `.canvas` via the deck pattern — **native-primary** (native nodes+edges
> canonical, one `diagram_root` canonical surface) **+ a derived Mermaid `code` node**; `mermaid.py` **ported** from the
> CanvasForge quarry (theme stripped; not a dependency). **All 5 diagram types** (flowchart · sequence · class · state ·
> gantt) validate aDNA-Native + degrade (D-1/D-2/D-3). **Suite 36/36, `ruff` clean; `canvas_std` firewall git-diff 0;
> no regression** (canvas_std 80/10 · deck 16 · brief 10 · document 37). Shape-enum trap handled (Mermaid shapes ride
> `_reserved…qualities.shape`, never baseline `styleAttributes.shape`); cyclic flowcharts validate (`dependency` edges,
> not the acyclicity-checked `sequence`). **1 spec-gap erratum candidate → A3.1 LIP queue (`adr_003`):** no
> diagram/graph unit in `PL_EXTENT_UNITS`, so a diagram `region` omits `extent`. **⛔ HELD at the A1→A2 (comic) gate** —
> A2 builds `comic_generator` (~1,870 LOC, mostly ports from `canvas_comic`); do not start without the operator. Design:
> approved plan `~/.claude/plans/please-read-the-claude-md-lovely-star.md` (§Comic producer).

> **⚒ OPERATION ATELIER OPENED (this session, `session_stanley_20260621_193649_atelier_scaffold_a0`).** Post-Keystone,
> the operator chose (plan mode) to build the two production layers Canvas owns since pt09 but never built on
> `canvas_std` — **`diagram_generator` (warm-up) then `comic_generator`** — in ONE phased campaign
> ([[how/campaigns/campaign_canvas_production/campaign_canvas_production|Operation Atelier]], `status: planning`; plan
> `~/.claude/plans/please-read-the-claude-md-lovely-star.md`). **This session scaffolded the campaign** (master doc +
> per-campaign `CLAUDE.md` + the A0.1 mission) and **executed Phase A0.1** — a contract/profile **decision record**
> (`how/campaigns/campaign_canvas_production/missions/artifacts/a0_1_contract_profile_decision.md`) resolving **6 gating
> questions** (per-producer quality contracts · profiles-producer-side/**no Standard LIP** · diagram shape-enum policy ·
> diagram-type scope · comic **data-driven** scope · codename), each with a doctrine-aligned default. Confirmed **no
> dedicated diagram/comic spec exists** (only mentions inside federation/component/panel-link specs). **No code;
> `canvas_std` untouched** (firewall git-diff 0). **⛔ HELD at the A0→A1 gate** — operator ratifies the 6 decisions
> (that ratification **activates** the campaign + opens the **A1 diagram build**). The producer designs (canvas mapping,
> port-vs-rebuild maps, `_reserved` enrichment, test plans) live in the approved plan; carried into A1/A2 missions at
> phase entry. **Keystone tail unchanged:** LIP-0008/0009 review closes 2026-06-27; PT P5 Hestia-owned. The boxes below
> are Keystone-close history.

> **▶ POST-KEYSTONE BACKLOG TRIAGED (this session, `session_stanley_20260621_141753_backlog_triage`).** Operator chose
> "triage + work backlog." Result: **6 of 7 ideas were inherited `.adna` template scaffold** (`agent_init` 2026-04-04,
> `campaign_adna_polish`; root README / `.adna/README.md` / Obsidian plugins / aDNA banner+logo / generic startup) →
> **quarantined** to `how/backlog/_inherited_scaffold/` (mirrors the campaigns precedent; `git mv`, SO-6) with
> provenance + owning-vault routing (aDNA.aDNA / aDNALabs.aDNA). The 1 canonical idea
> (`idea_deck_generator_canvas_pilot`) was **already shipped as E4.4** → marked `implemented`; its parked planning
> mission reconciled to `completed` (SO-5 AAR). Root cause filed upstream
> (`idea_upstream_fork_inherits_stale_backlog` → `aDNA-Network/aDNA`). **Live Canvas backlog is now clean** (1
> implemented + 1 upstream). No code touched (firewall git-diff 0); **PT P5 + LIP review unchanged.**

> **▶ FULL CLOSEOUT EXECUTED (prior session, `session_stanley_20260620_225259_lip_review_open`).** Operator chose the
> full closeout — all three operator-gated actions taken: **(1)** Canvas.aDNA `6fe95c1` **pushed** (`87db9d0..6fe95c1`);
> **(2)** the lattice-labs LIP batch **committed surgically + pushed** (`ba635dfb` — staged only `lip_0008` + `lip_0009`
> + `lip_registry.md`; the owner's dirty `.obsidian/` tree left untouched, no `git add -A`); **(3)** **Review OPENED** on
> **LIP-0008 + LIP-0009** (status Draft→Review; LIP-0001 formal ≥7-day period, **earliest close 2026-06-27**; recorded in
> each LIP's Decision Log + `review_opened`/`review_earliest_close` frontmatter + the registry, Draft 5→3 / Review 0→2).
> **Remaining:** on/after **2026-06-27** the FA accepts/rejects each LIP — **LIP-0008 Final → Canvas Standard v2.1.0**
> (A-5 relaxation at the pinned sites), **LIP-0009** records the canvas-stays-a-view deferral (no core change). **PT P5
> (Hestia) unchanged.** The box below is the prior session's tail-clear record.

> **▶ POST-KEYSTONE TAIL CLEARED (prior session, `session_stanley_20260620_221404_post_keystone_tail`).** The four
> Mondrian-ownable tail items are done: **(1)** B4 **filed as LIP-0008 (Draft)** + **(2)** Δ2 **filed as LIP-0009
> (Draft)** in `lattice-labs/how/governance/lips/` (+ `lip_registry.md`) — both **await the operator/FA opening
> Review** (the ≥7-day clock; **LIP-0008 → Canvas Standard v2.1.0** on Final, LIP-0009 records the canvas-stays-a-view
> deferral, no core change); **(3)** the **migration-parity context guide** written
> (`what/context/context_migration_parity_methodology.md`, graduation §D); **(4)** the **3 Low review-errata SWEPT** —
> brief label fix (F-E51-001) + **CANVAS-L-001 link-label carry** (fold `sources[].label` →
> `_reserved…qualities.label` in `document_generator` + `brief_consumer`, producer-side, guarded) + deck slide-order
> swap (F-E51-003). **Verified:** consumer suites **10/16/37** + ruff clean; 4 examples `adna_native [OK]`
> (`canvas-std 2.0.1`); **`canvas_std` firewall git-diff 0**; the `document_small` golden regenerated **surgically**
> (only `qualities.label` added). Bonus: fixed a pre-existing malformed `_meta` line in the `iii/` learning store.
> **[SUPERSEDED 2026-06-20 — both batches now pushed; see the FULL CLOSEOUT note above]** the lattice-labs LIP files +
> registry + the Canvas batch were operator-gated (lattice-labs carries a dirty owner tree); the operator authorized the
> full closeout and both are pushed (`6fe95c1` + `ba635dfb`). **PT P5 (Hestia) unchanged.**

## P2 — Keystone E-phase build detail (former L292–381, verbatim)

**Phase E5 is OPEN (2026-06-19, operator-authorized E4→E5 crossing — "Advance to E5" + "Ratify ADR-004"); E5.1 is
DONE.** (E0–E2 reference impl + E3 CanvasForge cutover + E4 consumers are complete history; the `canvas_core` shim
stays live to the E-D2 window 2027-06-13, retired at E6.2.) **E4 closed-with-deferral:** E4.3 (`brief_consumer` 10/10)
+ E4.4 (`deck_generator` 16/16) done; **E4.1/E4.2 (LF-successor) — D3 touch RESOLVED:** `adr_002`'s Option-B
*federated* leg is superseded by **[[what/decisions/adr_005_lf_successor_in_vault|adr_005]]** (**ratified 2026-06-19**
→ in-vault `what/production/`; the Option-A schema leg stands). **E4.1 + E4.2 are now BUILT — PHASE E4 COMPLETE** (operator
opened E4.1/E4.2 at the E5 hold, SO-3, 2026-06-19; built E4.1 same day, **E4.2 on 2026-06-20**): **`document_generator`**
— the in-vault long-form LF-successor — is green (**37/37**) on `canvas_std`, structural `iii/` review 0 High/0 Med
(`iii/feedback_2026_06_20_document_generator_e4_2.md`). **E4.2 done:** the LF format/visual contracts ride the `.canvas`
as declarative `_reserved` metadata + per-genre `GENRE_PROFILES`; first `region`-class use; section-level reflow closes
the bulk of `CANVAS-L-002`.

**E5.1 — `iii/` wrapper wired + first real canvas review (DONE 2026-06-19):**
- **Wrapper activated** — `iii/CLAUDE.md` scaffold → **active**; III pin **confirmed v0.5.0** (commit `0f06aa6`, oracle
  lattice 1.2.6) vs `III.aDNA/MANIFEST.md` (minor bump reviewed per III ADR-002 §3; siblings VideoForge/CanvasForge/wga
  already @ v0.5.0; stale router "v0.4.0" superseded). New `iii/what/context/` files — `canvas_reviewers.yaml` (5-lens
  panel) + `canvas_iii_learning_store.jsonl`; `reviewer_registry` extension added (existing ADR-002 §1a kind — no amendment).
- **First real review** — structural III review of both consumers' example canvases → **0 High / 0 Med** across the
  lenses; **3 Low + 1 GRAPH-GAP** tracked as errata; `CANVAS-L-001` (citation-label-dropped) accumulated **local**.
  **Pixel/VR1 explicitly PT-P5-gated** (deferred, not passed). Artifact: `iii/feedback_2026_06_19_canvas_consumers.md`.
  Mission: [[how/campaigns/campaign_canvas_genesis/missions/mission_e5_1_iii_wiring|mission_e5_1]].
- **ADR-004 ratified** (operator countersign at the gate) — binds the PT P5 relocation target; NOT authorization to
  move code (relocation = PT P5).
- No regression: `canvas_std` 46/8 · `brief_consumer` 10/10 · `deck_generator` 16/16; `ruff` clean; both examples `[OK]`.

**E4.1 — LF-successor built (DONE 2026-06-19):**
- **`document_generator`** (3rd in-vault consumer; `what/production/document_generator/`) — a structured long-form
  document spec → a v2.0.0 aDNA-Native **multi-page** `.canvas` (pages = group nodes; `profile: long_document`;
  `sequence` across pages, `reading_order` within, `adjacency` prose→citations). On `canvas_std` alone (zero PT-P5 dep,
  per `adr_005`); the genre/writing pipeline stays producer-side (E4.2+).
- **First use of the `code` component class**; figure→file/link, table, caption, blockquote, list, citations all carry +
  degrade. Worked example: a self-referential whitepaper about the Standard (2 pages / 27 nodes / 23 edges).
- **Green:** `document_generator` **18/18**, `ruff` clean; CLI `document-generator build` + `canvas-std validate` →
  `adna_native [OK]` + D-1/D-2/D-3.
- **Structural `iii/` review → 0 High / 0 Med** (pixel/VR1 PT-P5-gated): 2 Low (`CANVAS-L-001` recurrence freq→2;
  `CANVAS-L-002` layout-overflow) + 1 GRAPH-GAP + **3 spec-gap erratum candidates** (see Open side-tracks). Artifact:
  `iii/feedback_2026_06_19_document_generator.md`. Mission:
  [[how/campaigns/campaign_canvas_genesis/missions/mission_e4_1_lf_successor|mission_e4_1]] (completed).

**E4.2 — LF visual/format contracts + reflow (DONE 2026-06-20; full envelope, operator go):**
- **Contracts as declarative metadata** — `spec_format_contract` F1–F7 + `spec_visual_contract` V1–V8/X1–X14 (scavenged
  from `Archive.aDNA/LiteratureForge.aDNA/what/specs/`) now ride `document_generator`'s `.canvas` in `_reserved`
  (`semantic_bindings.{genre,format,visual}` + `brand_style_pack_ref` + derived `panel_link.surfaces`), driven by a
  5-entry **`GENRE_PROFILES`** registry (whitepaper + grant worked; research/blog/exec stubbed) + per-figure `asset`
  overrides. The genre/writing pipeline stays producer-side; `canvas_std` schema **untouched** (firewall git-diff 0).
- **First use of the `region` component class** — derived-surface backing markers + the `rgn_subclass` region (X12).
- **Reflow / auto-pagination (section-level) closes the bulk of `CANVAS-L-002`** — whitepaper 2→5 pages, grant 1→4,
  every emitted page ≤ `CONTENT_H`; a non-overflowing no-genre doc is **byte-identical to E4.1** (golden-locked). Narrow
  residual (a single section taller than a page) flagged `oversized_overflow` → PT P5.
- **Green:** `document_generator` **37/37** (18 + 19 new), `ruff` clean; CLI + `canvas-std validate` → `adna_native
  [OK]` + D-1/D-2/D-3; no regression (`canvas_std` 46/8 · `brief_consumer` 10 · `deck_generator` 16); `model.py`
  AST-guarded substrate-neutral. Structural `iii/` review **0 High / 0 Med** (`iii/feedback_2026_06_20_document_generator_e4_2.md`);
  `CANVAS-L-002` → addressed; **1 new spec-gap erratum candidate** (derived-surface backing node) + sequence-unit
  erratum sharpened → LIP queue. Mission:
  [[how/campaigns/campaign_canvas_genesis/missions/mission_e4_2_lf_contracts|mission_e4_2]] (completed). **Phase E4 complete.**

**Next: ✅ PHASE E6 COMPLETE — OPERATION KEYSTONE CLOSED (2026-06-20).** E6.1 cross-system parity **GREEN**; E6.2
cutover confirmed at the Standard/floor level (rollback intact; shim retire scheduled 2027-06-13); E6.3 handoff
register + context graduation + Campaign AAR. **Open tail → PT P5** (E5.2 federation rollout = the ~8
producer-wrapper refederations + `canvas_core` relocation + v2.0.0 registration; the 55 federation-integration test
reds are this work made concrete) **+ LIP queue** (4 spec-gap errata, `adr_003`) **+ optional** Δ2 LIP (E5.3).
Authoritative close: [[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] §Completion
Summary; tail: `how/campaigns/campaign_canvas_genesis/missions/artifacts/e6_3_handoff_register.md`.

**Open follow-ups → contracted as PT P5 items in [[what/decisions/adr_004_production_code_layout|ADR-004]] (ratified
2026-06-19):** (1) **FU1 — canvas/-routing Standing Order** (route `what/production/` standard-consumption through
`canvas/`, mirroring `iii/`) at the P5 refederation — **not** an edit to the archived "do-not-resume" CanvasForge
`CLAUDE.md`. (2) **FU2 — round-trip-function dedup** (validate/diff/merge/round-trip → `canvas_std`) at `canvas_core`
relocation (once co-located with `canvas_std`), gated by `e3_3_parity_check.py` (baseline `3ce4d341` unchanged).

**Build hygiene:** Canvas.aDNA's `canvas_std` suite: `.venv` at `what/code/canvas_std` (46/8). **E4 consumer suites
(gitignored `.venv` per package, `adna-canvas-std` editable): `what/production/brief_consumer/` → 10/10;
`what/production/deck_generator/` → 16/16; `what/production/document_generator/` → 37/37 (E4.2: 18 + 19 new); all `ruff` clean.** The CanvasForge suite (KEEP reference) runs in the
gitignored `.venv` at `CanvasForge.aDNA/what/code/` → 900/3. Tracking:
[[how/campaigns/campaign_canvas_genesis/campaign_canvas_genesis|Operation Keystone]] (active).

**Open side-tracks:** Δ2 canvas-as-primitive LIP ([[what/decisions/lip_draft_canvas_as_primitive|draft]]) → **filed as
LIP-0009 2026-06-20**; the 3 Low review errata (citation provenance; link-label carry; deck slide order) → **SWEPT
2026-06-20** (producer-side `qualities.label` carry + fixture fixes; suites green); III/Astro upstream
notes. **E4.1 spec-gap erratum candidates → LIP queue (`adr_003`):** (1) orphan-anchor + `naming_convention` validator
absent — `spec_panel_link_semantics §5.3/§6` mandates the check but `canvas_std/reserved.py::validate_panel_link` lacks
it (headline); (2) no dedicated `quote`/`blockquote` or `footnote` component class (long-form rides on `text` +
`semantic_type`); (3) `sequence`-unit ambiguity for paginated multi-section docs (§5.1 section-panels vs the page-centric
chain used by `document_generator`). Detail: `iii/feedback_2026_06_19_document_generator.md`. **E4.2 update
(2026-06-20):** (4) **NEW** — a *derived* `panel_link.surface` (html / funder_portal) has no content region, so the
producer must mint a synthetic `region`-class backing node to satisfy A-5; should the Standard allow a surface-as-pure-
metadata declaration? (surface-model erratum). Erratum (3) is **sharpened** — E4.2 now **exercises the `region` class**
(for surface/subclass markers), while pagination still rides page-`panel` nodes, so "which construct owns pagination —
`region` or page-`panel`?" is now concrete. `CANVAS-L-002` (layout overflow) **addressed by E4.2 section-level reflow**
(narrow residual → PT P5). Detail: `iii/feedback_2026_06_20_document_generator_e4_2.md`.
