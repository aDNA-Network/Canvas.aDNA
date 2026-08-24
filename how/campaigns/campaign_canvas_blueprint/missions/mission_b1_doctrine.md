---
mission_id: mission_b1_doctrine
type: mission
title: "B1 — Diagrammatic-context doctrine: the legacy reconciliation, ruled from measurement"
campaign: campaign_canvas_blueprint
phase: P1
owner: stanley
persona: mondrian
status: completed
status_history: "active (2026-08-24, P1 gate) → completed (2026-08-24, Canvas-owned half shipped; b1.5 remains open pending Rosetta — the mission closes complete-with-open-item, the phase does not advance on their silence)"
executor_tier: fable
token_budget_estimated: "~90k"
created: 2026-08-24
updated: 2026-08-24
last_edited_by: agent_mondrian
tags: [mission, blueprint, p1, doctrine, diagrammatic_context, legacy_interop, canvas_yaml_interop, lip_assessment]
---

# Mission B1 — Doctrine

Opened at the P1 gate (2026-08-24, operator). P1's charter names four items. **One is not Canvas's
to complete**: finalizing the pattern is Rosetta's ruling in their vault. Memo #9 was verified
delivered at source (`aDNA.aDNA/who/coordination/coord_2026_08_22_mondrian_to_rosetta_diagrammatic_context_pattern.md`),
two days old, unanswered — genuinely pending, **not** a delivery defect (the campaign's Estafette
standing order required checking, and the check passed). This mission ships the other three and
leaves that one open by name.

## The measurement that reshapes the phase

P0 authored the pattern draft from a fleet survey. Before ruling on it, the corpus was re-measured
with `canvas-std` 2.3.0 and direct JSON inspection. **The count was right; the diagnosis was wrong.**

| P0 draft / memo #9 | Measured (2026-08-24) | Verdict |
|---|---|---|
| "**196** template `.canvas` files" | **196** real live files across **46** vaults (+**74** archived in `Archive.aDNA`, SO-7) | ✅ **correct — no correction needed** |
| "**bare** JSON Canvas — no `_reserved` block" | **196/196** carry `_reserved` = `{authority: "view", source_yaml, last_sync, sync_hash}` | ❌ **wrong** |
| "invisible to `canvas-std validate`" | True — but *because of placement*, not absence | ⚠️ **right effect, wrong cause** |
| "the old shape, unreconciled with the Standard" | The block **is** the `view` authority row the draft proposes to create | ⚠️ **already the model** |

**Root cause (new):** the legacy writes its block at **`metadata._reserved`**. The Standard's
canonical path is **`metadata.frontmatter._reserved`** (`what/docs/canvas_producer_quickstart.md:46`;
A-2's own error text names it). `canvas_std` reads the canonical path, finds nothing, and reports
`declared=core`. The block has been sitting one level too high in 196 files since 2026-02.

Observed, verbatim:

```
$ canvas-std validate what/lattices/examples/template_architecture.canvas
canvas-std 2.3.0: what/lattices/examples/template_architecture.canvas
  declared=core  level_reached=extended  [OK]

$ canvas-std validate what/lattices/examples/template_architecture.canvas --level adna_native
canvas-std 2.3.0: what/lattices/examples/template_architecture.canvas
  declared=adna_native  level_reached=extended  [FAIL]
  - A-2: aDNA-Native canvas requires a populated metadata.frontmatter._reserved block
  degradation: {'D-1': True, 'D-2': True, 'D-3': True}
```

All four template examples behave identically; all 196 copies are byte-identical per file
(`template_architecture.canvas` → `md5 f9459bc3cbb21391fe28dd76d3e44902` in `.adna`, `Canvas.aDNA`,
and `Obsidian.aDNA` alike). The interop **spec** has 69 copies in 3 md5 variants — the only
difference among live copies is the `last_edited_by` frontmatter line; one archived copy also
carries a stale `source_instance`. **The bodies are uniform.**

**Why this matters to the ruling:** the reconciliation is not "merge two incompatible systems." It is
"the legacy is already structurally the `view` model, written to the wrong path." The remedy is a
*relocation plus two identity fields* — mechanical, lossless, zero node/edge change — landing as one
template edit plus a release, not a 46-vault sweep. That is a materially smaller ask than memo #9
put to Rosetta, and they should have it before they rule.

## Objectives

| # | Objective | Status |
|---|---|---|
| **b1.1** | Census/diagnosis erratum → Rosetta; amend Canvas's staged draft + campaign master to match | ✅ |
| **b1.2** | `adr_011` — rule the legacy-interop reconciliation (authored `proposed`, §7.7 pending) | ✅ |
| **b1.3** | LIP-0010 assessment — does the doctrine need a schema change? | ✅ (Option B, **deferred**) |
| **b1.4** | Defect: `--level adna-native` is an invalid CLI value in campaign docs | ✅ |
| **b1.5** | *(not Canvas's)* Finalize the pattern with Rosetta | 🔓 **OPEN — pending their ruling** |

`idea_diagram_missions_herb` (P1's re-point item) lives in `aDNA.aDNA` and is **already proposed**
inside the staged draft. Rule 10 — offer, never write. Nothing further is Canvas's to do on it.

## Discipline

- `what/code/canvas_std/` untouched — no LIP is ratified here, so nothing may touch the firewall.
- Zero writes into `aDNA.aDNA` beyond the memo delivery, left **uncommitted** in their tree.
- Every published number re-derived before publication (the first draft of this mission's own
  erratum claimed "270" — the symlink-following count — and was corrected before it left the vault).

## Deliverables

| Artifact | State |
|---|---|
| `who/coordination/coord_2026_08_24_mondrian_to_rosetta_census_erratum.md` (**v2**) | delivered to `aDNA.aDNA`, uncommitted in their tree |
| `artifacts/draft_pattern_diagrammatic_context.md` | amended — §Erratum E1 + corrected Problem/Legacy/Evidence + a new anti-pattern |
| `what/decisions/adr_011_legacy_canvas_interop_reconciliation.md` | new, **`proposed`**, §7.7 pending |
| `who/governance/lips/lip_0010_assessment_diagrammatic_context.md` + registry row | new, **draft** (assessment; no change taken) |
| `campaign_canvas_blueprint.md` + campaign `CLAUDE.md` | census note; `adna-native` → `adna_native` |

**Gate evidence:** `canvas_std` **115 passed / 10 skipped** · certification **11/11** ·
`git diff --stat -- what/code/canvas_std/` **empty** · `what/lattices/examples/` **untouched**
(the migration ran on scratch copies only).

## AAR

**Worked.** Measuring before ruling. The charter's framing ("reconcile two incompatible systems")
dissolved into a much smaller, provable statement once `canvas-std` and a JSON parse were pointed at
the actual files — and *executing* the migration on scratch copies turned a proposed remedy into a
verified recipe (4/4 → `adna_native [OK]`, degradation intact) that Rosetta can ship rather than
re-derive.

**Didn't.** My first two census attempts were both wrong, in opposite directions. "270" followed
symlinks into `Archive.aDNA`; a `comm` reconciliation then mis-flagged real vaults as missing because
shell `sort` and Python `sorted()` disagree on collation. The draft's original **196 was correct all
along** — I nearly shipped an "erratum" correcting a number that needed no correction. And v1 of the
memo went out calling the migration "a relocation plus two identity fields" before I had run it;
A-6's nested `sync` block and 16-hex hash format made that materially wrong within the hour.

**Finding (F-B1-1).** A `_reserved` block at a **non-canonical path** is a worse failure mode than a
missing one: 196 files across 46 vaults have carried `view`-authority semantics at
`metadata._reserved` since 2026-02, reporting a green `[OK]` at `core` the whole time. Present-and-
unread beats absent for invisibility. Added to the pattern's anti-patterns; ruled in `adr_011`.

**Finding (F-B1-2).** `authority` is normative in the proposed doctrine and **unvalidated** by
`canvas_std` — 0 of 21 in-vault `adna_native` canvases carry the key, and `authority: "veiw"` passes
silently. Recorded as LIP-0010 rather than silently widening the firewall.

**Change.** Publish no number without re-deriving it by a second, independent method — and prefer
`find` without symlink-follow over glob for fleet censuses. Do not describe a migration in an
outbound memo before executing it: the memo is the contract, and "roughly this" costs a same-day v2.

**Follow-up.** b1.5 stays open pending Rosetta. LIP-0010 converts from assessment to proposal only
if they ratify the pattern with `authority` still normative. The sync-field stubs
(`sha256:none` ×3, empty `source_yaml` ×3) are theirs to populate at the template release.
