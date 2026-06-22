---
campaign_id: campaign_canvas_production
type: campaign
title: "Operation Atelier — Canvas production layers (diagram, then comic) on canvas_std"
owner: stanley
status: active
activated: 2026-06-21
phase_count: 4
mission_count: 8
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
> already-shipped `canvas_std`, with the Standard untouched. **🔄 ACTIVATED 2026-06-21** — the operator ratified the A0
> decision record at the A0→A1 gate (all 6 defaults accepted); **Phase A1 (diagram) in progress.** Phase gates are
> human gates (SO-1).

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
| A2.1 (C-1) | Scaffold + ported content layer (`style`/`prompt`/`panel_layout`/`rlhf_hints`) + substrate-free `model.py`; ported pure-function tests green | 1 | planned |
| A2.2 (C-2) | Canvas construction rewrite (`layout`/`panels`/`consume` → source → `to_canvas` → `_reserved`); conformance passes aDNA-Native | 1 | planned |
| A2.3 (C-3) | Conformance hardening (round-trip/degradation/components/panel-coverage) + CLI + example mini-issue + no-regression run | 1 | planned |
| A2.4 (C-4) | `iii_quality_contract.md` + README/AGENTS + federation-wrapper notes | 0.5-1 | planned |

**Phase exit gate (A2→A3, HUMAN):** full comic suite green (~45–55 tests), example builds + conforms, no regression in the other four suites, firewall git-diff 0, AARs GO. **HELD.**

### Phase A3 — Validation & close
| # | Mission | Sessions | Status |
|---|---------|----------|--------|
| A3.1 | Cross-producer validation (all 5 production suites + `canvas_std` 80/10) + structural `iii/` review of both new examples + log any spec-gap errata to the LIP queue (`adr_003`) | 1 | planned |
| A3.2 | Completion Summary + Campaign AAR + `skill_context_graduation` + STATE.md + `status: completed` | 0.5-1 | planned |

**Campaign close gate (HUMAN / operator disposition):** all suites green; `iii/` artifacts filed; graduation run; STATE updated.

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
- **Two-shelf doctrine:** `what/code/` = the Standard (immutable); `what/production/` = producers (depend on the
  installed `adna-canvas-std`, may mutate state). Both new producers live on the production shelf.
- **Quarry, not dependency:** port logic *from* `Archive.aDNA/CanvasForge.aDNA/...`; the producers must not import
  `canvas_core` or depend on PT P5 relocation. Mirrors the LiteratureForge-as-quarry precedent.
- **Profiles producer-side:** `{"profile": "diagram"}` / `{"profile": "comic"}` declared by the producer, no
  out-of-enum inline bindings (A-4 safe). The `comic` profile is already named in `spec_federation_contract §6.1`.
- Technical designs (canvas mapping, port-vs-rebuild maps, `_reserved` enrichment, test plans) are in the approved
  plan file and will be carried into the A1/A2 mission files at phase entry.

## Completion Summary

*Fill out when setting `status: completed`.*

### Deliverables
### Descoped
### Key Findings
### Scope Changes
### Follow-Up Campaigns

## Campaign AAR

*Mandatory before setting `status: completed`. See `how/templates/template_aar_lightweight.md`.*

- **Worked**:
- **Didn't**:
- **Finding**:
- **Change**:
- **Follow-up**:
