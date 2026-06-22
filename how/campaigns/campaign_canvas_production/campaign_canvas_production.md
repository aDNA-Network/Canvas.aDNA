---
campaign_id: campaign_canvas_production
type: campaign
title: "Operation Atelier — Canvas production layers (diagram, then comic) on canvas_std"
owner: stanley
status: completed
activated: 2026-06-21
completed: 2026-06-21
phase_count: 4
mission_count: 4
estimated_sessions: "6-10"
estimation_class: build-broad
priority: medium
created: 2026-06-21
updated: 2026-06-21
last_edited_by: agent_stanley
predecessor: campaign_canvas_genesis
tags: [campaign, build, canvas, production, diagram, comic, atelier]
---

# Campaign: Operation Atelier (production layers)

> **EXECUTION campaign — build the two production layers Canvas owns but never built on `canvas_std`.** Successor to
> Operation Keystone (`campaign_canvas_genesis`, completed 2026-06-20), which built the Standard + reference impl + 3
> producers (deck · brief · document). At Production Tidy **pt09** (2026-06-17) Canvas absorbed the CanvasForge
> production layers (**deck · comic · diagram**, Hermes→Mondrian); Keystone built only **deck** fresh. This campaign
> builds **diagram** (warm-up) then **comic** — each a self-contained producer on the `what/production/` shelf, on the
> already-shipped `canvas_std`, with the Standard untouched. **✅ COMPLETED 2026-06-21** — both producers built +
> verified (diagram **36/36** · comic **87/87**, aDNA-Native; no regression; firewall git-diff 0); A0–A3 closed at
> their human gates (SO-1).

## Goal

Two new in-vault producers — `what/production/diagram_generator/` and `what/production/comic_generator/` — each
conformant **aDNA-Native**, round-trippable, and degradable to a valid Obsidian canvas, mirroring the established
Keystone producer pattern (`deck_generator`/`document_generator`). When complete, every CanvasForge production layer
Canvas absorbed at pt09 (deck · comic · diagram) is built and green on `canvas_std`, with the two-shelf firewall held
(`what/code/canvas_std/` git-diff 0).

## Context

Operation Keystone shipped the aDNA Canvas Standard v2.0.1, the immutable `canvas_std` reference impl, and three
producers on it (`deck_generator` 16 · `brief_consumer` 10 · `document_generator` 37). The **comic** and **diagram**
layers were absorbed in governance at pt09 but never built on the new substrate. Their legacy CanvasForge engines sit
in `Archive.aDNA/CanvasForge.aDNA/what/code/` as a **quarry** to port from (not relocate): `canvas_core/mermaid.py`
(~306 LOC Mermaid syntax generator) and `canvas_comic/` (~3,035 LOC: 6-layer prompt assembly + color-script +
character bible + panel-grid layout). This campaign builds net-new producers that quarry those engines — exactly how
E4 built deck/brief/document fresh on `canvas_std` — with **no dependency on the LIP gate** (LIP-0008/0009, FA-owned,
review closes 2026-06-27) or on **PT P5** (Hestia-owned `canvas_core`/`canvas_comic` relocation per ADR-004). Approved
plan: `~/.claude/plans/please-read-the-claude-md-lovely-star.md`.

## Scope

### In Scope (BUILD)
- `what/production/diagram_generator/` — a net-new producer (DiagramInput → v2.0.0 aDNA-Native `.canvas`), porting the
  5 Mermaid syntax generators from the quarry; native-nodes-and-edges canonical + a derived Mermaid `code` node.
- `what/production/comic_generator/` — a net-new producer (ComicInput → multi-page/spread aDNA-Native `.canvas`),
  porting the canvas-agnostic content/prompt/layout logic; panels emit image **prompts as metadata** (ComfyUI owns
  rendering).
- Per-producer test suites (conformance · round-trip · degradation · components · coverage) + worked examples + (if
  ratified at A0) `iii_quality_contract.md`.
- Cross-producer no-regression validation + structural `iii/` review of the two new examples at close.

### Out of Scope
- Modifying `canvas_std` (the two-shelf firewall; any Standard change goes through the LIP process, `adr_003`).
- Relocating the legacy `canvas_core`/`canvas_comic` packages (that is **PT P5**, Hestia-owned) — the archive is a
  port-from quarry, not a runtime dependency.
- Image **rendering** (ComfyUI) and pixel/visual scoring (`canvas_presentation`, PT-P5-gated). Diagram **layout
  rendering** beyond producer-owned integer geometry.
- Registering `diagram`/`comic` as built-in profiles in `canvas_std.schema` (that would touch the immutable substrate
  → a LIP). Profiles stay producer-side.

## Phases & Missions

> Missions kept thin until phase entry (SO-3); objectives authored at entry. Phase exits are **human gates** (SO-1) —
> report a SITREP and HOLD. Diagram is the warm-up (built first); comic second (the larger build). Each producer is
> self-contained on `canvas_std` with **zero PT-P5 dependency**.

### Phase A0 — Spec/contract triage (cheap; no code)
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| A0.1 | Production-contract + profile triage → a decision record (the 6 Decision Points below); confirm no diagram/comic spec exists | ≤1 | 🔄 **in progress 2026-06-21** ([[how/campaigns/campaign_canvas_production/missions/mission_a0_1_contract_profile_triage\|mission]]) |

**Phase exit gate (A0→A1, HUMAN):** operator ratifies the A0 decision record (quality-contract posture, profiles-are-producer-side, shape-enum policy, diagram-type scope, comic data-driven scope, codename). **This ratification activates the campaign** (`status: active`) and authorizes the A1 diagram build.

### Phase A1 — Diagram producer (warm-up)
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| A1.1 | Build `diagram_generator` (all 5 types) — clone deck pattern; ported `mermaid.py`; flowchart+sequence end-to-end first, then class/state/gantt; full test suite + worked example + `iii_quality_contract.md` (A1.2 folded in) | 2-3 | ✅ **done 2026-06-21** — 36/36, all 5 types aDNA-Native ([[how/campaigns/campaign_canvas_production/missions/mission_a1_1_diagram_build\|mission]]) |

**Phase exit gate (A1→A2, HUMAN):** full diagram suite green (~16–22 tests), every diagram type validates aDNA-Native + degrades (D-1/D-2/D-3), `canvas_std` firewall git-diff 0, mission AARs GO. **HELD before comic.**

> **Phase progress (2026-06-21) — PHASE A1 COMPLETE ✅ (diagram producer built):** `what/production/diagram_generator/`
> built on `canvas_std` (native-primary + a derived Mermaid `code` node); all 5 diagram types validate **aDNA-Native** +
> degrade (D-1/D-2/D-3); suite **36/36**, `ruff` clean; `canvas_std` firewall git-diff 0; **no regression** (canvas_std
> 80/10 · deck 16 · brief 10 · document 37). Worked example committed; light `iii_quality_contract.md` shipped. **1
> spec-gap erratum candidate** (no diagram/graph unit in `PL_EXTENT_UNITS` → diagram region omits `extent`) → A3.1 LIP
> queue. **⛔ HELD at the A1→A2 phase gate (human gate)** — do not start the comic build (A2) without the operator.

### Phase A2 — Comic producer (the larger build)
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| A2 | Build `comic_generator` — C-1 ported content layer · C-2 canvas construction · C-3 conformance+CLI+example · C-4 quality contract+docs (A2.1–A2.4 folded as objectives) | 3-5 | ✅ **done 2026-06-21** — 87/87, example aDNA-Native ([[how/campaigns/campaign_canvas_production/missions/mission_a2_comic_build\|mission]]) |

**Phase exit gate (A2→A3, HUMAN):** full comic suite green (~45–55 tests), example builds + conforms, no regression in the other four suites, firewall git-diff 0, AARs GO. **HELD.**

> **Phase progress (2026-06-21) — PHASE A2 COMPLETE ✅ (comic producer built):** `what/production/comic_generator/`
> built on `canvas_std` (the 5th in-vault producer; ~1,790 src LOC, mostly ports from the `canvas_comic` quarry).
> Multi-page/spread aDNA-Native (`comic_root` canonical surface; spread/page nested-group regions; `image`-class panels
> carrying the 6-layer prompt in `qualities.image_prompt` — **no rendering**, ComfyUI keeps pixels). Suite **87/87**,
> `ruff` clean; example (4-page SS mini-issue) validates aDNA-Native + degrades; `canvas_std` firewall git-diff 0; **no
> regression** (canvas_std 80/10 · brief 10 · deck 16 · document 37 · diagram 36). **⛔ HELD at the A2→A3 phase gate
> (human gate)** — A3 is cross-producer validation + structural `iii/` review + LIP-queue errata, then campaign close.

### Phase A3 — Validation & close
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| A3 | Validation & close — A3.1 cross-producer sweep + `iii/` review + LIP-queue errata · A3.2 Completion Summary + AAR + graduation + STATE + `status: completed` (A3.1/A3.2 folded as objectives) | 1 | ✅ **done 2026-06-21** ([[how/campaigns/campaign_canvas_production/missions/mission_a3_validation_close\|mission]]) |

**Campaign close gate (HUMAN / operator disposition):** all suites green; `iii/` artifacts filed; graduation run; STATE updated.

> **Phase progress (2026-06-21) — PHASE A3 COMPLETE ✅ / CAMPAIGN CLOSED:** final sweep **266 passed** (canvas_std
> 80/10 · brief 10 · deck 16 · document 37 · diagram 36 · comic 87); `canvas_std` firewall git-diff 0. Structural
> `iii/` review filed (`iii/feedback_2026_06_21_atelier_producers.md`) — **0 High / 0 Med**, 2 Low, 2 spec-gap errata
> (AT-1/AT-2) → LIP queue. Producer pattern graduated → `what/context/context_canvas_producer_pattern.md`. Campaign
> `status: completed`.

> Diagram alone (A0+A1) is an independently shippable deliverable (~3–4 sessions) if comic slips.

## Decision Points

| # | When | Decision | Plan default | Status |
|---|------|----------|--------------|--------|
| 1 | A0→A1 gate | Per-producer `iii_quality_contract.md`? | Yes for both — light for diagram, full for comic | ✅ ratified 2026-06-21 |
| 2 | A0→A1 gate | `diagram`/`comic` `semantic_bindings` profiles producer-side (no Standard LIP)? | Producer-side, no LIP | ✅ ratified 2026-06-21 |
| 3 | A0→A1 gate | Diagram shape-enum policy | Mermaid shapes in `_reserved.qualities.shape`; no baseline `styleAttributes.shape` | ✅ ratified 2026-06-21 |
| 4 | A0→A1 gate | Diagram-type scope for v1 | All 5; flowchart+sequence as first end-to-end slice (A1.1), rest in A1.2 | ✅ ratified 2026-06-21 |
| 5 | A0→A1 gate | Comic scope: data-driven vs baked SS story | Data-driven engine; legacy 32-page SS issue → `examples/` only; drop `ContextPack` gate (→ `context_object.refs`); RLHF dormant; page/spread counts from input | ✅ ratified 2026-06-21 |
| 6 | A0→A1 gate | Codename / slug | Operation Atelier / `campaign_canvas_production` | ✅ ratified 2026-06-21 |

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| Diagram shape-enum mismatch (`rect/round/stadium` ∉ `VALID_SHAPES`) breaks E-2/degradation | Medium | Carry Mermaid shapes in `_reserved.qualities.shape`; never set baseline `styleAttributes.shape`; a D-2 test asserts no out-of-enum leak. |
| Mis-tagged `sequence` edge on a looping flowchart/state diagram fails A-5 acyclicity | Medium | Flowchart/state edges = `dependency`/`reading_order` (may cycle); reserve `sequence` for gantt/linear; a round-trip test exercises a cyclic flowchart. |
| Comic image boundary leak (rendering creeps into the producer) | Medium | Producer emits prompts as `qualities` metadata only; no ComfyUI import, no image I/O; the `PendingPanel`/variant machine is dropped. |
| Comic build is large (~1,870 src LOC) — scope/time creep | Medium | Bulk is **ports** (~1,100 LOC); 4-objective split; only ~150 LOC genuinely rewritten; data-driven scope avoids baking the SS story. |
| Accidental edit to the immutable `canvas_std` | High | Verify `git -C what/code/canvas_std diff --stat` empty at every phase gate. |
| Confusion with PT P5's planned `canvas_comic` relocation | Low | New producer is `comic_generator/` (net-new) and self-contained on `canvas_std`; PT P5 relocates the legacy `canvas_comic/` separately. Note in handoff. |

## Verification Strategy

### Per-Mission
| Check | Method | Gate? |
|-------|--------|-------|
| SITREP filed | Session closure protocol | Yes |
| AAR produced | 5-step AAR + scorecard | Yes |
| Producer suite green + `ruff` clean | `pytest` in the producer `.venv` | Yes |
| Example builds + validates aDNA-Native | `<producer> build … && canvas-std validate …` → `adna_native [OK]` | Yes |
| `canvas_std` firewall git-diff 0 | `git -C what/code/canvas_std diff --stat` | Yes |
| Files committed | Git status clean | Yes |

### Per-Phase
| Check | Method | Gate? |
|-------|--------|-------|
| All mission AARs GO | Review AAR readiness | Yes |
| Phase exit criteria met | This doc's phase exit gate | Yes — operator approval |
| Degradation report all-True | `degradation_report(doc)` D-1/D-2/D-3 | Yes |
| Scope changes documented | Scope section | Yes |

### Campaign Validation
| Check | Method |
|-------|--------|
| All 5 production suites + `canvas_std` (80/10) green | Cross-producer no-regression run (A3.1) |
| Structural `iii/` review of both new examples | `iii/` wrapper, target 0 High / 0 Med (pixel/VR PT-P5-gated) |
| Context graduation run | `skill_context_graduation` on campaign deliverables |
| STATE.md updated | Operational state reflects close |

## Timeline

| Phase | Missions | Sessions |
|-------|----------|----------|
| A0 — Triage | A0.1 | ≤1 |
| A1 — Diagram | A1.1–A1.2 | 2-3 |
| A2 — Comic | A2.1–A2.4 | 3-5 |
| A3 — Close | A3.1–A3.2 | 1-2 |
| **Total** | **9 missions** | **6-10 sessions** |

## Notes

- **Scope change (2026-06-21, at activation):** A1.2 folded into A1.1 (one diagram-build mission, all 5 types);
  `mission_count` 9→8. Operator ratified all 6 A0 decisions (defaults) at the A0→A1 gate.
- **Scope change (2026-06-21, at A2 open):** A2.1–A2.4 folded into one A2 mission (objectives C-1..C-4);
  `mission_count` 8→5. Operator cleared the A1→A2 gate ("proceed to A2").
- **Two-shelf doctrine:** `what/code/` = the Standard (immutable); `what/production/` = producers (depend on the
  installed `adna-canvas-std`, may mutate state). Both new producers live on the production shelf.
- **Quarry, not dependency:** port logic *from* `Archive.aDNA/CanvasForge.aDNA/...`; the producers must not import
  `canvas_core` or depend on PT P5 relocation. Mirrors the LiteratureForge-as-quarry precedent.
- **Profiles producer-side:** `{"profile": "diagram"}` / `{"profile": "comic"}` declared by the producer, no
  out-of-enum inline bindings (A-4 safe). The `comic` profile is already named in `spec_federation_contract §6.1`.
- Technical designs (canvas mapping, port-vs-rebuild maps, `_reserved` enrichment, test plans) are in the approved
  plan file and will be carried into the A1/A2 mission files at phase entry.

## Completion Summary

### Deliverables
- **Two new in-vault producers on `canvas_std`:** `what/production/diagram_generator/` (36/36; all 5 diagram types —
  flowchart/sequence/class/state/gantt — aDNA-Native; native-primary + derived Mermaid `code` node) and
  `what/production/comic_generator/` (87/87; multi-page/spread; `image`-class panels carrying prompts as metadata —
  no rendering). With brief/deck/document, **all 5 producers green** — final sweep **266 passed**; `canvas_std`
  firewall git-diff 0 throughout.
- **Governance/quality:** A0.1 decision record (6 ratified decisions); structural `iii/` review
  `iii/feedback_2026_06_21_atelier_producers.md` (0 High / 0 Med); 2 spec-gap errata (AT-1 graph extent unit; AT-2
  surface vocabulary) logged → `what/decisions/lip_queue_disposition.md`; producer pattern graduated →
  `what/context/context_canvas_producer_pattern.md`.

### Descoped
- Legacy comic orchestration (`ComicProductionAdapter`) + producer self-scoring (`ComicReport.review`) — out of scope
  (CanvasForge/ComfyUI concerns; the review rubric became the comic quality *contract*, not shipped code).
- Pixel rendering + per-panel style-lock + the 24-criterion scoring → PT P5 (`canvas_presentation`) / ComfyUI.

### Key Findings
- The canvas grammar generalizes cleanly: a diagram (graph) and a comic (multi-page media) reduce to the **same
  producer pipeline** as deck/document (substrate-free model → `consume` assembles source → `to_canvas` → enrich
  `_reserved`). The Standard needed **no new feature** — only 2 minor vocabulary errata surfaced.
- Delegating each build to a subagent seeded with the *confirmed* `canvas_std` API facts (then re-verifying via the
  persisted venvs) produced faithful, fully green producers without substrate drift.

### Scope Changes
- A1.2 folded into A1.1; A2.1–A2.4 folded into one A2 mission; A3.1/A3.2 folded into one A3 mission. `mission_count`
  9→4 (builds executed as cohesive units).

### Follow-Up Campaigns
- **None required.** Open items ride existing tracks: AT-1/AT-2 errata → LIP queue (editorial PATCH at maintainer
  discretion, or fold into the next LIP batch); pixel render/scoring → PT P5; image rendering → ComfyUI. Future
  producers (poster/letter/post) reuse `context_canvas_producer_pattern.md`.

## Campaign AAR

- **Worked**: the deck/document pattern + clean ports from the `canvas_comic`/`mermaid` quarry let two producers
  (including a ~1,790-LOC comic) land green fast; per-phase human gates kept the operator in control without stalling.
- **Didn't**: nothing blocked — the only friction was 2 minor Standard vocabulary gaps, captured as non-blocking errata.
- **Finding**: a 2D output (a graph, a comic page) reduces to typed nodes + typed edges + `_reserved` metadata — the
  Mondrian "reduce to the grammar" thesis held across all 5 producers.
- **Change**: none — the Keystone producer pattern transferred 1:1; graduated it to context for the next producer.
- **Follow-up**: AT-1/AT-2 → LIP queue; `context_canvas_producer_pattern.md` graduated for reuse.
