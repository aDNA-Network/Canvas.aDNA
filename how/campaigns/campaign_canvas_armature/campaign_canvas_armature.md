---
campaign_id: campaign_canvas_armature
type: campaign
title: "Operation Armature — leg-3 interface runtime (governed write + the first canvas_std firewall touch)"
owner: stanley
status: active
estimated_sessions: "5-9"
calibrated_sessions: "5-8"
estimation_class: build-with-governance-touch
phase_count: 4
mission_count: 4
priority: high
predecessor: campaign_canvas_salon
created: 2026-06-22
updated: 2026-06-22
last_edited_by: agent_stanley
status_history: "planning (2026-06-22 open) → active (2026-06-22 P0 ratified) → ... "
tags: [campaign, canvas, armature, leg3, interface, surface, runtime, interaction, firewall]
---

# Campaign: Operation Armature — leg-3 interface runtime

## Goal

Turn Operation Salon's **ratified** leg-3 interface-surface spec + its **demonstrated** `read → act → re-read` loop into
a **real, governed leg-3 interaction runtime** — completing the interface leg of the three-leg Canvas thesis. When this
campaign completes: (1) a response advances the surface and is **reconciled back to the authoritative `.lattice.yaml`**
through the *advisory* round-trip path (a reviewed draft, never a silent write); and (2) the `I-1/I-2/I-3` interaction
conformance family — today realized only in the `canvas_context` consumer — is **wired into the `canvas_std` harness +
CLI** and `interaction_version 1.0` is **cut into a Standard version**, the first deliberate touch of the
frozen-since-Keystone `canvas_std` firewall.

This is a **build campaign** (the Keystone model), not a planning arc: Salon already chartered, specified, and bounded
leg 3 (spec-only, charter D4). Operation Armature builds the runtime the Salon Completion Summary §Descoped explicitly
deferred. It HOLDs at every phase gate (SO-1); the firewall touch is isolated to a single, separately-gated phase.

## Context

Operation Salon closed 2026-06-22 with the three-leg thesis complete *on paper* — leg 1 (output, ×7 producers) and
leg 2 (context object, the `canvas_context` loader) **proven**, leg 3 (interface surface) **ratified + POC-demonstrated**
([[../campaign_canvas_salon/campaign_canvas_salon|Operation Salon]] §Completion Summary). But Salon deliberately stopped
leg 3 at **spec-only** (charter D4). Three gaps remain, named in the follow-on stub
([[../../backlog/idea_campaign_leg3_interface_runtime|idea_campaign_leg3_interface_runtime]], `proposed`) and the Salon
§Descoped:

- **The governed round-trip write is out of scope.** The POC's `apply_response`
  ([[../../../what/code/canvas_context/src/canvas_context/interaction|interaction.py]] v0.2.0) is a pure **view-only
  append-fold** — it advances the *view* and never writes the authoritative `.lattice.yaml`
  ([[../../../what/specs/spec_interface_surface|spec_interface_surface]] §7.2). An honest runtime closes that loop to
  source — via the **advisory** reverse path ([[../../../what/specs/spec_roundtrip_protocol_v2|spec_roundtrip_protocol_v2]]
  §1.2/§5), a reviewed draft, never a silent authoritative mutation.
- **`I-*` lives in the consumer, not the harness.** The `I-1/I-2/I-3/I-D` family is realized in `canvas_context`
  (`validate_interaction_block`), forward-pointed into the `canvas_std` harness "with a leg-3 reference reader" at Salon
  P3 ([[../../../what/specs/spec_conformance_suite|spec_conformance_suite]] §4.1; spec_interface_surface §9.1/§10). Wiring
  it into `canvas_std/validate.py` is the **first leg-3 touch of the firewall** — a ratifiable decision (ADR-007), the
  leg-3 analogue of Salon's D6 (which chose to *preserve* the firewall for leg 2).
- **`interaction_version 1.0` was never cut as a Standard version.** The spec rides `_reserved.interaction` additively at
  `standard_version 2.0.2` + `interaction_version 1.0`; the spec's ratification Q7 deferred the Standard-version cut to
  "a deliberate release." This campaign is that release.

**Operator decisions at this campaign's open** (AskUserQuestion, planning session
`session_stanley_20260622_193153_armature_scaffold_p0`): **codename = Operation Armature**; **firewall posture = include
the `canvas_std` touch as a gated P2** (governed by ADR-007 — the operator chose to *lift* the firewall for this bounded
purpose, reversing the standing preserve default precisely because the leg-3 thesis needs `I-*` to be a real Standard
check, not just consumer code). Approved plan: `~/.claude/plans/please-read-the-claude-md-glimmering-teapot.md`.

## Scope

### In Scope

- **The governed round-trip write runtime** — promote `apply_response` from a view-only fold to a runtime that
  reconciles a response back to the authoritative `.lattice.yaml` **via the advisory reverse path** (staleness check →
  draft → diff → three-way merge → human-review gate → regenerate), built on the existing
  `canvas_std.roundtrip` (`diff`/`merge`/`preserve_positions`/`compute_sync_hash`/`from_canvas`/`to_canvas`), imported
  read-only. Firewall-clean (P1).
- **The `canvas_std` firewall touch (gated, P2 only, per ratified ADR-007)** — wire `validate_interaction` (I-1/I-2/I-3)
  into `canvas_std/validate.py`'s aDNA-Native path (reusing `reserved.validate_anchors`); surface it through
  `conformance.validate_suite` + the `canvas-std` CLI; add an interaction-bearing golden to `canvas_std/tests`. The
  consumer's `validate_interaction_block` becomes a thin delegate/re-export.
- **The `interaction_version 1.0` Standard-version cut (P2, per ADR-007 + decision-record D6)** — bump
  `STANDARD_VERSION` + schema + CLI + spec frontmatters; flip the `spec_conformance_suite §4.1` + `spec_interface_surface
  §10` forward-pointers from "forward-pointed" → "implemented." Coordinated with the in-review **LIP-0008** v2.1.0 line.
- **A runnable pilot** — operator annotates a canvas → an agent re-reads it as context → responds → a **reviewed**
  `.lattice.yaml` draft is emitted (the on-disk source unchanged).
- **The OIP `v1.x` re-anchor — as a deferred stub** (filed, not built; cross-vault dep).

### Out of Scope

- **Cross-surface routing** (when to use Canvas vs ISS vs Terminal vs web) — the future `aDNA.aDNA` OIP-unification
  campaign owns it ([[../../../what/decisions/adr_006_canvas_surface_boundary|adr_006]] §3, the load-bearing line).
- **The ISS gate engine** — HTML rendering, capture runtime, RLHF schema, the 4-tier round-trip (ADR-006 §2). Canvas
  owns the affordance/anchor/response/turn *grammar*; ISS owns the gate *engine*.
- **A silent authoritative write to source** — the governed write is **advisory** (a reviewed draft); a tool MUST NOT
  silently propagate canvas/response edits to the `.lattice.yaml` (spec_roundtrip_protocol_v2 §1.2).
- **Rendering / capture / transport / web publication / image rendering** — fenced by ADR-006.
- **Canvas-as-primitive** (Δ2 / LIP-0009) — stays on its own LIP track; the interaction layer rides `_reserved`, no
  core-primitive change.
- **The OIP `v1.x` re-anchor build** — deferred (cross-vault dep on the unopened `aDNA.aDNA` OIP campaign).

### Subsumes

| Plan/Mission | Status at Subsumption | Tasks Absorbed By |
|-------------|----------------------|-------------------|
| `how/backlog/idea_campaign_leg3_interface_runtime.md` | `proposed` → graduates to this campaign on P0 ratification | the campaign as a whole (mark `implemented` at P3 close) |

## Phases & Missions

> Missions are authored thin and only at phase entry (SO-3 context budget). Only P0 is authored at open.

### Phase P0: Charter + decision record + ADR-007 draft  *(this session)*

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| 1 | P0 — Charter + 8-decision record + ADR-007 draft | 1 | — | completed |

**Phase exit gate (P0→P1, HUMAN)**: the operator ratifies the **P0 decision record** (8 decisions — codename · campaign
type/arc · firewall posture · governed-write semantics · runtime home · Standard-version coordination · capture/turn
scope · OIP re-anchor posture) **and** `adr_007`. Ratification **activates** the campaign (`status: active`) and opens
P1. **✅ MET 2026-06-22** — all 8 ratified at the agent's recommended values; `adr_007` accepted; campaign `active`.

### Phase P1: Governed round-trip write runtime (firewall-clean)

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| 2 | P1 — Governed write runtime + pilot | 2-3 | P0 | completed |

**Phase exit gate**: a response reconciles to a **reviewed** `.lattice.yaml` source draft via the advisory reverse path
(no silent write); the pilot runs end-to-end; `canvas_context` tests green; **`canvas_std` firewall git-diff 0**
(runtime is a read-only consumer of `canvas_std`). **✅ MET 2026-06-22** — `reconcile.py` (canvas_context 0.3.0) +
source fixture + 8 tests + pilot; `canvas_context` **58 passed**, `ruff` clean, `canvas_std` **82/10** unchanged,
**firewall git-diff 0**; the on-disk authoritative source is byte-unchanged after the loop. **⛔ HELD at the P1→P2 gate.**

### Phase P2: Firewall touch — wire I-* into canvas_std + cut the Standard version  *(per ratified ADR-007)*

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| 3 | P2 — I-* into the harness + interaction_version Standard-version cut | 1-2 | P1, ADR-007 ratified | completed |

**Phase exit gate**: `I-1/I-2/I-3` validate natively through the `canvas-std` CLI on an interaction-bearing golden;
`interaction_version 1.0` is cut into the Standard version; **D-1..D-3 still prove round-trip-to-baseline** on that
golden; **full regression green** (`canvas_std` + `canvas_context` + 7 producers). This is the *only* phase that edits
`canvas_std` — entered only on the operator's explicit approval at the P1→P2 gate, behind ADR-007. **✅ MET 2026-06-23**
— `I-*` validate via the `canvas-std 2.2.0` CLI on `adna_interaction.canvas`; `interaction_version 1.0` cut → **v2.2.0**;
D-1..D-3 green on the golden; **full regression GREEN** (`canvas_std` **105/10** · `canvas_context` **58** · 7 producers
**223**; `ruff` clean); the firewall touch is **+159/−9 across 9 files** (logic = `validate_interaction` + a 1-line
dispatch). **⛔ HELD at the P2→P3 gate.**

### Phase P3: Close

| Mission | Title | Sessions | Dependencies | Status |
|---------|-------|----------|-------------|--------|
| 4 | P3 — Validation, iii/ review, AAR, doc currency, OIP stub | 1 | P1, P2 | pending |

**Phase exit gate**: cross-suite sweep green (no regression); structural `iii/` review of the runtime + pilot;
Completion Summary + Campaign AAR filed; doc currency done; the leg-3 runtime backlog idea marked `implemented`; the OIP
`v1.x` re-anchor filed as a deferred stub; `status: completed`.

## Decision Points

| # | When | Decision | Status |
|---|------|----------|--------|
| D1 | P0→P1 gate | Codename / slug (Operation Armature / `campaign_canvas_armature`) | ratified 2026-06-22 |
| D2 | P0→P1 gate | Campaign type & phase arc (4-phase build campaign P0–P3, Keystone model, each human-gated) | ratified 2026-06-22 |
| D3 | P0→P1 gate | Firewall posture — **lift** `canvas_std` in a gated P2 (wire I-* + cut version) via `adr_007` | ratified 2026-06-22 (w/ `adr_007`) |
| D4 | P0→P1 gate | Governed-write semantics (advisory-reverse / reviewed draft; no silent source write) | ratified 2026-06-22 |
| D5 | P0→P1 gate | Runtime home (extend `canvas_context` vs new `canvas_runtime` sibling) | ratified 2026-06-22 — extend `canvas_context` |
| D6 | P0→P1 gate | Standard-version coordination (cut `interaction_version 1.0` into v2.2.0; LIP-or-discretion; vs v2.1.0) | ratified 2026-06-22 — v2.2.0, maintainer discretion |
| D7 | P0→P1 gate | Capture / turn-lifecycle / operator-annotation scope (thin pilot path only; gate engine stays ISS's) | ratified 2026-06-22 |
| D8 | P0→P1 gate | OIP `v1.x` re-anchor posture (deferred stub; cross-vault dep) | ratified 2026-06-22 |

All eight are recorded with defaults + rationale + alternatives in `missions/artifacts/p0_decision_record.md`. **All
ratified 2026-06-22 at the agent's recommended values** (P0→P1 gate); the campaign is `active` at P1.

## Risk Register

| Risk | Severity | Mitigation |
|------|----------|------------|
| **First-ever `canvas_std` edit** — regression across 82 `canvas_std` tests + 7 producers + `canvas_context` | High | The touch is isolated to a single, separately-gated phase (P2) governed by `adr_007`; the P2 exit gate is **full regression green** + D-1..D-3 on an interaction golden, not git-diff 0; P0/P1/P3 stay git-diff 0 |
| Governed write drifts into a **silent authoritative write** to source (violates spec_roundtrip_protocol_v2 §1.2) | High | The runtime emits a `_draft`/`_merged`-marked reviewed draft + a human-review gate; a test asserts the on-disk `.lattice.yaml` is byte-unchanged after `reconcile` |
| Boundary creep into **ISS** (capture/gate engine) or **OIP** (routing) | Medium | `adr_006` is the binding fence; the runtime builds the *grammar's* reconcile path, not a gate engine or a router; no routing logic |
| **Standard-version collision** with the in-review LIP-0008 (→ v2.1.0, FA review closes 2026-06-27) | Medium | D6 default reserves v2.1.0 for LIP-0008 and cuts `interaction_version` into **v2.2.0** (or folds into v2.1.0 only if LIP-0008 lands first); coordinate at the P2 gate |
| **OIP cross-vault dependency** (the `v1.x` re-anchor) blocks the build | Low | The runtime builds on the ratified Canvas-scoped v1 spec; the re-anchor is additive (`interaction_version` semver) and deferred to a stub — not a blocker (idea stub §Discussion) |
| Scope too large to gate cleanly | Medium | Keystone-model build; thin missions at phase entry; HOLD at every gate (SO-1); the firewall touch is its own phase |

## Verification Strategy

### Per-Mission

| Check | Method | Gate? |
|-------|--------|-------|
| SITREP filed | Session closure protocol | Yes |
| AAR produced | 5-step AAR (in-doc) | Yes |
| Deliverables validated | AAR scorecard | Yes |
| Files committed | Git status clean (operator-gated push) | Yes |

### Per-Phase

| Check | Method | Gate? |
|-------|--------|-------|
| Phase exit criteria met | Campaign doc phase exit gate | Yes — user approval |
| **`canvas_std` firewall** | `git status -s -- what/code/canvas_std/` clean for **P0/P1/P3** | Yes — at those gates |
| **P2 regression** (firewall lifted) | Full suites green: `canvas_std` (82/10 + I-* rows) + `canvas_context` (50+) + 7 producers (305) + D-1..D-3 on an interaction golden | Yes — the P2 gate replaces git-diff 0 with full regression |
| Round-trip-to-baseline | `strip(interaction_golden)` validates at Core (D-1) | Yes — P2 |
| Risk register updated | Campaign doc risk register | No — recommended |

### Campaign Validation

| Check | Method |
|-------|--------|
| New ADR indexed | `what/decisions/AGENTS.md` + ADR sequence coherent (`adr_007`) |
| Runtime patterns graduated | `skill_context_graduation` → a `what/context/` guide (P3) |
| Backlog idea closed | `idea_campaign_leg3_interface_runtime` → `implemented` (P3) |
| STATE.md updated | Campaign status reflected in operational state |
| OIP re-anchor filed | Deferred stub created (P3) |

## Timeline

| Phase | Missions | Sessions |
|-------|----------|----------|
| P0 Charter + decisions + ADR-007 | 1 | 1 |
| P1 Governed write runtime + pilot | 1 | 2-3 |
| P2 Firewall touch + version cut | 1 | 1-2 |
| P3 Close | 1 | 1 |
| **Total** | **4 missions** | **5-9 sessions** |

## Notes

- **Firewall posture is the inverse of Salon's.** Salon D6 *preserved* the `canvas_std` firewall (leg-2 loader = a new
  read-only sibling). Armature D3/`adr_007` *lifts* it — deliberately, for one bounded purpose (wire the already-ratified
  `I-*` family into the harness + cut the version), isolated to P2. Every other phase holds git-diff 0. This is the
  single biggest governance call of the campaign and is an explicit operator decision (taken this planning session),
  recorded as `adr_007`.
- **Advisory, not silent.** The "governed round-trip write" is governed *because* it is advisory — `spec_roundtrip_protocol_v2`
  §1.2 forbids silent source propagation. The runtime closes the loop by emitting a reviewed draft through the §5
  diff→merge→human-review→regenerate path, reusing the existing `roundtrip.py` machinery. The honesty the POC bought with
  a view-only fold, the runtime keeps with a review gate.
- **Reuse over rebuild.** P1 builds on `canvas_std.roundtrip` (already has `diff`/`merge`/`preserve_positions`/
  `compute_sync_hash`/`from_canvas`/`to_canvas`) + the POC's `apply_response`; P2 reuses `reserved.validate_anchors` for
  I-2. The campaign writes glue + the reconcile path + the harness wiring, not new core algorithms.
- **Version coordination.** LIP-0008 (A-5 relaxation) is in FA review → v2.1.0 on Final (closes 2026-06-27). D6 default
  reserves v2.1.0 for it and cuts `interaction_version 1.0` into **v2.2.0**, to avoid a two-change collision in one
  version; revisit at the P2 gate if LIP-0008 has already landed.
