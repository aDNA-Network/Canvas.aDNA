---
session_id: session_stanley_20260622_193153_armature_scaffold_p0
type: session
tier: 2
agent: agent_stanley
persona: Mondrian
created: 2026-06-22
updated: 2026-06-22
status: active
campaign_id: campaign_canvas_armature
campaign_phase: P0
intent: "Open Operation Armature (the leg-3 interface runtime build — Salon's committed follow-on) and execute Phase P0: scaffold the campaign (master doc + CLAUDE.md + P0 mission), author the 8-decision P0 record, and draft ADR-007 (the ratifiable canvas_std firewall touch). No code. HOLD at the P0→P1 gate for operator ratification."
tags: [session, canvas, armature, leg3, interface, runtime, p0, scaffold, firewall]
---

# Session — Operation Armature P0: Scaffold + decision record + ADR-007 draft

## Intent

Graduate the Salon follow-on (`how/backlog/idea_campaign_leg3_interface_runtime.md`, `proposed`) into a campaign and
open it on a fixed footing — **before any build**. Phase P0 (Keystone/Salon precedent): (1) scaffold the campaign dir,
(2) record the eight governance/scope decisions that gate the runtime as a single ratifiable record, and (3) draft
**ADR-007** — the ratifiable decision to make the *first-ever* `canvas_std` firewall touch (wire `I-*` into the harness
+ cut `interaction_version 1.0` into a Standard version), isolated to a gated P2. No spec is changed and **no code is
written** this session.

Approved plan: `~/.claude/plans/please-read-the-claude-md-glimmering-teapot.md`. Operator decisions this planning
session (AskUserQuestion): **firewall touch = INCLUDED** as a gated P2 phase (ADR-007-governed); **codename = Operation
Armature**.

## Binding scope

- **Docs/governance only.** P0 writes markdown; it touches **no code**. The `canvas_std` firewall (the standing D6
  posture, now governed for this campaign by the proposed ADR-007) holds trivially — verify
  `git status -s -- what/code/canvas_std/` clean at close.
- **Firewall lifts only in P2, only on ratification.** This campaign is the first to *propose* editing `canvas_std`;
  the lift is bounded by ADR-007 + the P1→P2 human gate. P0/P1/P3 stay git-diff 0.
- **In-doc 5-line AARs** (Salon/Palette precedent), not a separate `how/missions/artifacts/` AAR file.

## Baselines (this session, confirmed pre-open — read-only)

- Repo `master` in sync with `origin/master` (Salon batch already pushed; working tree clean at open).
- `canvas_context` 50 passed (28 leg-2 + 22 leg-3) · `canvas_std` 82/10 · CLI `canvas-std 2.0.2` — last verified at the
  Salon P5 close (no code touched since). **Firewall git-diff 0.**
- `adr_007` confirmed the next free ADR number (`adr_000`..`adr_006` taken); `campaign_canvas_armature` does not collide
  with an existing slug.

## Scope declaration

- **Create (campaign scaffold):** `how/campaigns/campaign_canvas_armature/campaign_canvas_armature.md`;
  `how/campaigns/campaign_canvas_armature/CLAUDE.md`; `how/campaigns/campaign_canvas_armature/missions/mission_p0_charter.md`;
  `how/campaigns/campaign_canvas_armature/missions/artifacts/p0_decision_record.md`.
- **Create (decision):** `what/decisions/adr_007_leg3_firewall_touch.md` (status: proposed).
- **Modify (indices):** `what/decisions/AGENTS.md` (index adr_007).
- **Modify (doc currency):** `STATE.md` (Operation Armature OPENED lead box + `last_session`).
- **Modify (backlog):** `how/backlog/idea_campaign_leg3_interface_runtime.md` (note graduation-in-progress on ratification — deferred to the gate, not this session).
- **Firewall (DO NOT TOUCH):** `what/code/canvas_std/`.

## Conflict scan

- `how/sessions/active/` — only this session at open (`.gitkeep` + this file).
- Repo in sync with origin; no concurrent agent commits expected. Keep git read-only mid-session; re-check HEAD before
  any commit (intra-vault concurrent-commit discipline). Commit/push is operator-gated (Git-Ops §3).

## Work log

- Oriented via the approved plan + the Salon P0 precedents (master doc / P0 decision record / P0 mission / campaign
  CLAUDE.md). Confirmed conventions + the next ADR number (`adr_007`); read the POC (`interaction.py`), the round-trip
  reference (`canvas_std/roundtrip.py`), the conformance harness (`conformance.py`/`validate.py`), and the binding specs
  (`spec_interface_surface` / `spec_roundtrip_protocol_v2` / `spec_conformance_suite` / `adr_006`).
- Scaffolded the campaign dir: `campaign_canvas_armature.md` (master doc — Keystone-model build, P0–P3, scope, Decision
  Points D1–D8, risks) + `CLAUDE.md` + `missions/mission_p0_charter.md`.
- Authored the **8-decision record** (`missions/artifacts/p0_decision_record.md`, `status: pending`) — D1 codename +
  D3 firewall-lift carry the operator's planning-session choice; D2/D4–D8 carry doctrine-aligned defaults.
- Drafted **`adr_007_leg3_firewall_touch.md`** (`status: proposed`) — the ratifiable first `canvas_std` touch (the
  inverse of Salon's firewall-preserving D6); lift bounded to P2 + two purposes; P2 gate = full regression.
- Doc currency: `STATE.md` Resume-Here lead box → Operation Armature OPENED/HELD + `last_session`.
- **Firewall verified git-diff 0** (`git status -s -- what/code/canvas_std/` empty) — P0 is docs/governance only.
- **P0→P1 RATIFIED (operator, on request for recs).** Gave a per-decision recommendation (accept all 8 at defaults/
  choices; flagged D5 + D6 as the two to weigh); operator ratified **all 8 + `adr_007` at the agent's recs**. Flipped
  `p0_decision_record` + `adr_007` → ratified; campaign `status: active`; `mission_p0_charter` completed (+AAR); campaign
  Decision Points + CLAUDE.md updated; graduated the backlog idea (`idea_campaign_leg3_interface_runtime` → `planned`,
  `plan_id`) + indexed.
- **P1 BUILT (this session, continued).** Studied the design surface (interaction fixtures, `model.py`/`loader.py`,
  `roundtrip.py`, real `.lattice.yaml` sources); authored `mission_p1_write_runtime`; built
  `what/code/canvas_context/src/canvas_context/reconcile.py` (`reconcile`/`governed_apply`/`write_source_draft` +
  `Reconciliation` + the §6 lossy-field restore) over `canvas_std.roundtrip` read-only; bumped `canvas_context` 0.2.0 →
  **0.3.0**; built the source fixture (`review_request.source.json` + `_build_review_source.py`, topology-matched),
  `test_reconcile.py` (8 tests), and `pilot_governed_write.py`; gitignored the generated draft output; CHANGELOG.
- **Verified:** `canvas_context` **58 passed** (50 + 8), `ruff` clean; `canvas_std` **82/10 unchanged**; **firewall
  git-diff 0**; pilot closes the loop with the on-disk authoritative source **byte-unchanged** (`conflicts=0`).

## SITREP

**Completed**
- **Operation Armature OPENED → P0 ratified → P1 built**, all this session. The leg-3 interface *runtime* is real: a
  response advances the view and reconciles to a **reviewed source draft** via the advisory reverse path, **never a
  silent write** (the headline test asserts the authoritative source is byte-unchanged).
- **P0** (`mission_p0_charter`, completed +AAR): 8-decision record + `adr_007` (the leg-3 firewall-touch ADR) ratified
  at the agent's recommended values (D5 extend `canvas_context`; D6 cut `interaction_version 1.0` → v2.2.0, maintainer
  discretion). Campaign `active`.
- **P1** (`mission_p1_write_runtime`, completed +AAR): `reconcile.py` (canvas_context 0.3.0) over `canvas_std.roundtrip`
  + source fixture + 8 tests + pilot. **58 passed · ruff clean · `canvas_std` 82/10 · firewall git-diff 0.**

**In progress**
- None — P1 complete + verified. The P1→P2 gate is the HOLD point.

**Next up (operator — P1→P2 gate)**
- **Approve crossing into P2 — the `adr_007` firewall touch** (the *first* `canvas_std` edit since Keystone): wire
  `I-1/I-2/I-3` into `canvas_std/validate.py`'s aDNA-Native path (reusing `validate_anchors`) + surface via the CLI; cut
  `interaction_version 1.0` → Standard **v2.2.0**; add an interaction-bearing golden. The P2 exit gate is **full
  regression** (`canvas_std` + `canvas_context` + 7 producers + D-1..D-3), not git-diff 0. Operator approval required.

**Blockers**
- None. (The OIP `v1.x` re-anchor is a deferred stub — D8.)

**Files touched**
- Created (governance): `how/campaigns/campaign_canvas_armature/{campaign_canvas_armature.md, CLAUDE.md,
  missions/mission_p0_charter.md, missions/mission_p1_write_runtime.md, missions/artifacts/p0_decision_record.md}`;
  `what/decisions/adr_007_leg3_firewall_touch.md`; this session.
- Created (code, P1): `what/code/canvas_context/src/canvas_context/reconcile.py`; `tests/test_reconcile.py`;
  `tests/pilot_governed_write.py`; `tests/fixtures/{_build_review_source.py, review_request.source.json}`.
- Modified: `canvas_context/src/canvas_context/__init__.py` (exports + 0.3.0); `canvas_context/CHANGELOG.md`;
  `canvas_context/.gitignore`; `STATE.md`; `how/backlog/{idea_campaign_leg3_interface_runtime.md, AGENTS.md}`.
- Firewall: `what/code/canvas_std/` **untouched** (git-diff 0). Generated `review_request.source.draft.json` is gitignored.

## Next Session Prompt

Operation Armature (the leg-3 interface **runtime** build) is **at the P1→P2 gate, HELD**. P0 is ratified (8 decisions +
`adr_007`) and **P1 is built + green** — the governed **advisory-reverse** write runtime
(`what/code/canvas_context/src/canvas_context/reconcile.py`, `canvas_context` 0.3.0): `reconcile`/`governed_apply`/
`write_source_draft` over `canvas_std.roundtrip`; a response advances the view → reconciles to a **reviewed source
draft**, never a silent write (the on-disk source is byte-unchanged; `canvas_context` 58 passed, `canvas_std` 82/10,
firewall git-diff 0). **The operator must approve crossing into P2** — the **`adr_007` firewall touch** (the first
`canvas_std` edit since Keystone): wire `I-1/I-2/I-3` into `canvas_std/src/canvas_std/validate.py`'s aDNA-Native path
(reuse `reserved.validate_anchors`) + surface through `conformance.validate_suite` + the CLI; add an interaction-bearing
golden to `canvas_std/tests`; make `canvas_context.validate_interaction_block` a thin delegate; cut `interaction_version
1.0` → Standard **v2.2.0** (bump `STANDARD_VERSION` + schema + CLI + spec frontmatters; flip the `spec_conformance_suite
§4.1` + `spec_interface_surface §10` forward-pointers to "implemented"). The P2 exit gate is **full regression**
(`canvas_std` 82/10 + I-* rows · `canvas_context` 58 · 7 producers 305 · D-1..D-3 on the interaction golden), reviewed
diff — **not** git-diff 0. Do **not** touch `canvas_std` until the operator approves the P1→P2 crossing. Push is
operator-gated (Git-Ops §3) — nothing pushed this session.
