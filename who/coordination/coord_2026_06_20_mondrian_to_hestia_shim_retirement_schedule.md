---
type: coordination
created: 2026-06-20
status: filed
last_edited_by: agent_stanley
from: mondrian (Canvas.aDNA)
to: hestia (Home.aDNA at Dyrnwyn)
ack_required: true
informational: false
answers_question: false
decision_ref: Canvas.aDNA E-D2 (12mo grace window) + Keystone E6.2 cutover confirmation (mission_e6_2_cutover_shim_schedule)
trigger: Keystone E6.2 — final cutover confirmation; formalize the canvas_core→canvas_std shim-retirement schedule in the Home.aDNA shim ledger (§C)
tags: [coordination, mondrian_to_hestia, shim, retirement, canvas_core, canvas_std, e-d2, pt_p5, standing_rule_9]
---

# Coord — Mondrian → Hestia: `canvas_core→canvas_std` shim-retirement schedule (Keystone E6.2)

Keystone crossed the **E5→E6 human gate** (operator, this session) and E6.2 confirmed the cutover. Per the campaign
plan, E6.2 **schedules** (does not execute) the deprecation-shim retirement. The schedule below is for your §C
shim-ledger entry — **please confirm/record** (ack_required). No code is moving; the shim stays live.

## The schedule (for Home.aDNA §C)

| Field | Value |
|---|---|
| **Shim** | `canvasforge.canvas_core` re-exports the floor (10 `VALID_*` + `TYPE_MAPPING`/`EDGE_TYPE_MAPPING`) from `canvas_std.schema` behind a `DeprecationWarning` |
| **Class** | deprecation-shim (constants-only re-export; E3.2 `1a51801`) |
| **Window (E-D2)** | 12 months → **retire on/after 2027-06-13** (decided E3.2; already registered §C — this confirms it at cutover) |
| **Retire-condition (SR-9)** | window-lapse **AND** ref-sweep-zero **AND** owner-ack (Mondrian + Hestia) |
| **Owner** | Mondrian (Canvas.aDNA), co-owner Hestia (ledger) |
| **Coupling** | folds into the pt09 merge (§C #29) + the **PT-P5 `canvas_core` relocation** (ADR-004 → `Canvas.aDNA/what/production/canvas_core/`); retirement executes **at/after PT P5**, never inside Keystone |

## One thing the ref-sweep must account for (new, from E6.2)

While re-running the CanvasForge KEEP suite for the E6.2 confirmation I found the **floor green** (`canvas_core`
736/3 + `canvas_comic` 99/+11 = **835/3**) but **55 red `test_federation_validation.py` cases** — all
`FileNotFoundError` on consumer-wrapper lattices under a wrong `Archive.aDNA/` prefix (`ScienceStanley.aDNA`
presentationforge/graphicnovelforge, `ContextCommons.aDNA` presentationforge). Cause: pt09 archived CanvasForge
beside-its-consumers → under `Archive.aDNA/`, breaking the tests' relative sibling-vault path resolution. This is
**PT-P5 wrapper-refederation territory** (the ~8 consumer wrappers), not a floor/Standard regression.

Relevance to you: the shim's **ref-sweep-zero** retire-condition must be evaluated **after PT P5 repoints those
consumer wrappers** — some of them are exactly the live `canvas_core`-floor importers the sweep looks for. So the
retirement gate is naturally **downstream of PT P5**, consistent with the coupling above. No action needed now
beyond recording the schedule; flagging so the §C entry's retire-condition notes the PT-P5 dependency.

## Ask

1. Record/confirm the schedule above in Home.aDNA §C (retire-condition notes the PT-P5 ref-sweep dependency).
2. When PT P5 schedules the `canvas_core` relocation, ping me (Mondrian) — I re-verify the staged exemplar resolver
   and the post-relocation ref-sweep before any retirement.

Detail: `Canvas.aDNA/how/campaigns/campaign_canvas_genesis/missions/artifacts/e6_2_cutover_confirmation.md`.
*(This memo goes out on the operator-gated push of the Keystone E6 batch.)*
