---
plan_id: mission_vernier_p2b_lip_0011_sync_semantics
type: plan
title: "LIP-0011 — sync semantics: define what sync_hash hashes, register a full-digest key, and cut Standard v2.5.0 additively"
owner: stanley
status: completed
campaign_id: campaign_canvas_vernier
campaign_phase: "P2b"
campaign_mission_number: 1
mission_class: implementation
executor_tier: opus
token_budget_estimated: "~250k"
created: 2026-10-12
updated: 2026-10-16
last_edited_by: agent_mondrian
tags: [plan, campaign, vernier, lip_0011]
---

# Mission: LIP-0011 — sync semantics: define what sync_hash hashes, register a full-digest key, and cut Standard v2.5.0 additively

**Campaign**: [[how/campaigns/campaign_canvas_vernier/campaign_canvas_vernier|campaign_canvas_vernier]]
**Phase**: P2b · **Mission**: 1 of 6 (chartered at the 2026-10-12 scope amendment)
**Depends on**: the signed verdicts at `how/gates/vernier_p1_exit_20261012` (P2) unless stated otherwise per objective.
**⛩ Unblocked 2026-10-15:** P2 ruled 9/9 as recommended (V-1 (b) · V-2 at `extended` · V-3 `sync.generator`); record `how/gates/vernier_p1_exit_20261012.output.json`. The V-2 census is committed as `how/gates/axis_tier_census.py` (obj 4's re-home, done early).

## Goal

Turn the V-1/V-2/V-3 verdicts into the Standard. Three implementations currently pass A-6 with three semantics (topology · source-document bytes · master-file bytes). The LIP defines the field, adds the standard full-digest key (per the V-1 verdict, expected `sync.source_sha256`, 64 hex) and the provenance carrier (per V-3, expected `sync.generator`), rules the A-8 tier (V-2), and ships as v2.5.0 with every existing passer still passing — a claim that is MEASURED on the fleet corpus (F-GL-6), not asserted.

## Exit Gate

LIP-0011 Final in `who/governance/lips/`; `canvas_std` green at new pins; certification corpus gains one Terminal canvas, one City twin, one Canvas native as cases; fleet census (`~/aDNA/*/what/lattices/examples/*.canvas` + the five known external carriers) shows 0 new failures; firewall touch #7 back to diff 0 on commit; §7.7 signature on the LIP; registry + §7.2 + schema `$defs.reserved.sync` + `RESERVED_KEYS` all updated in the same touch (F-GL-1: one definition, consumed).

## Objectives

### 1. Draft LIP-0011 from the door's `.output.json`
- **Status**: ✅ drafted 2026-10-15 · **signed 2026-10-15T23:40Z** at `how/gates/lip_0011_signature_20261015` (4/4 approve, **D-1 (i)**; `73b0ea5`) · **Final 2026-10-16** (`55ce2a1`) · **Files**: `who/governance/lips/lip_0011_sync_semantics.md`, `lip_registry.md`
- Options as ruled; migration table per implementer (Terminal 8 · City 1 · LP gen-canvas · Home 1 · Canvas 26); backward-compat claim written as a *command that is run*, not a sentence.

### 2. Firewall touch #7 (named before signature)
- **Status**: ✅ 2026-10-16 — `2b3b70a` (code + tests) · `d72e77f` (specs). Exactly the eight signed rows; diff 0 after commit. What it did beyond the LIP's text is listed in the LIP's §As implemented (the `advisories` export · the declared-level trigger · escapes for the separators · the `conformance.py` residue).
- **Files**: `canvas_std/reserved.py` (A-6 semantic check: `source_sha256` 64-hex when present; `sync_hash` == topology recomputation when `production: generated` and the verdict says so; `sync.generator` string), `roundtrip.py` (helper `compute_source_sha256(path)`), `schema/adna_canvas_v2.schema.json` (`$defs.reserved.sync`), `spec_adna_canvas_standard.md` §7.2/§8.1, `__init__.py` version 2.5.0.
- Depends on: 1 + the signature.

### 3. Fixtures + certification
- **Status**: ✅ 2026-10-16 — corpus **12 → 15**, certification 15/15; schema enum coverage re-read: **12/40 unchanged**. ⚠ **Deviation:** the Terminal and City cases are **shape-derived with synthetic content**, not copied. `aDNA-Network/Terminal.aDNA` is PRIVATE, City has no remote, and Canvas is GitHub-public, so a copy would have published peer content at the next push (and the first candidate, `bastide_node_topology`, carries the mesh's RFC1918 subnet and machine names). The Canvas case is a byte-copy of `what/decisions/adr_004_production_code_layout.canvas`.
- One Terminal canvas (copied, attribution kept), one City twin, one Canvas native; `test_schema_conformance.py` coverage report re-read (12/40 residue unchanged unless widened here).

### 4. Fleet backward-compat census — run, paste, do not predict
- **Status**: ✅ **re-run at the touch 2026-10-16** under the signed rule set with `--baseline`: exit 0, **exactly 1 real-validator verdict change (PercySleep, as signed)**, 17 advisories agreeing path for path with `canvas_std.advisories()`; pasted into the LIP. First run 2026-10-15: `how/gates/sync_semantics_census.py`, pasted into the LIP. ⛔ **The exit gate's "0 new failures" is not met**: under the strictest rule set, 4 new failures (3 Canvas-own: F-V-10 builder encoding ×2 + 1 hand-set test fixture; 1 PercySleep, the V-2 price ruled on the door). Under D-1 (i), PercySleep only. Findings F-V-10 (two topology encodings in our tree), F-V-11 (top-level `generator` is ours, 61 fleet carriers), F-V-12 (the hard topology leg is a proxy promoted to a MUST). Re-run at the firewall touch.
- Script in `how/gates/` or `what/code/canvas_std/tools/`; output pasted into the LIP with glob + date + HEADs.

### 5. Version sweep classified, not globbed
- **Status**: ✅ 2026-10-16 (`44e93bd`). Classification in §Notes.
- `2.4.0` literals split into live pins vs dated historical claims (Gridline (E) precedent); peer rows in `federation_index` §2 **not touched**.

## Campaign Context

- Review + triage this mission answers to: `artifacts/review_20261012_vault_state_and_inbox_triage.md`.
- Standing rules: phase gates are human gates · firewall touches named file-by-file before the signature · every figure re-derived before it is written · state the population on the face of the number.

## Notes

**Obj 5 — the `2.4.0` surface, classified (2026-10-16).** Population: `grep -rIn 2.4.0` over the vault, excluding
`_archive/`, `.git`, session records, `state_archive_*`, `*.canvas`, and the gitignored `what/artifacts/`. 71 files
before the sweep.

| Class | Where | Disposition |
|---|---|---|
| **Live pin: edited** | Standard title + "This version" row · `standard_version` frontmatter on 8 companion specs + `canvas_authoring_guidance` · `spec_federation_contract` §2.1 template `version` · specs `README` (×2) · `federation_index` frontmatter · plus, in the touch, `STANDARD_VERSION`, the schema, and 3 spec frontmatters | → 2.5.0 |
| **Live, but inside the firewall and outside the signed rows: residue** | `canvas_std/README.md` (×4, "current to v2.4.0") · `conformance.py` (×3: `json_schema` docstring, CLI description, `schema` help) | **not edited**; carried to the next touch |
| **Dated historical claims** | "since v2.4.0" / "cut into v2.4.0" / "at the v2.4.0 cut" in the specs' A-8 notes, `reserved.py`, `conform.py`, `diagram_generator`, tests and docs · LIP-0010 · both CHANGELOGs · ADR-011 · closed campaign docs + AARs · all memos (outbound + inbox) · `federation_index` §2 peer pin history (lines 119–121, **peer rows untouched**) · rendered doors | left as written: each is true of the day it names |
| **Current-state prose** | `STATE.md` · `CLAUDE.md` | updated at the P2b close |

## Completion Summary

LIP-0011 is **Final**, and **Standard v2.5.0 is cut** (2026-10-16). The operator signed it at a rendered door
(4/4 approve, D-1 (i)). Firewall touch #7 landed exactly the eight signed rows. Outside the firewall, CanvasBuilder now
uses the Standard's one topology encoding (F-V-10) and PresentationBuilder writes `sync.generator` (F-V-11). The
three builder-encoded artifacts were recomputed in place. The fleet census, re-run against a pre-touch baseline,
shows exactly the one verdict change that was priced and signed. Gate line, generated:

`canvas_std` **236/22** · certification **15/15** · `canvas_core` **1041/4** · `canvas_presentation` **58/2** · `canvas_context` **58** · producers **276 across 7 packages** · `comic_render` **154/2** · firewall diff **0** · registry census **11/11** keys · dual-channel freshness **2/2** · inbox receipt **0 overdue** (0 untracked within 7 d)

Commits: `73b0ea5` (signature record) · `2b3b70a` · `d72e77f` (firewall) · `fe33f10` (outside) · `55ce2a1` (LIP
Final) · `44e93bd` (sweep) · the close commit. **Exit gate:** met, except two items accepted or recorded as
deviations: "0 new failures" (1, PercySleep, accepted at signature) and "one Terminal canvas copied" (shape-derived,
for publication reasons; above).

## AAR

- **Worked:** naming every firewall file before the signature. Nothing landed unseen, and the one design detail the
  text left open (what triggers A-8 at extended) was settled against §5.1's own wording and the census predicate.
  The census written before the touch became the post-touch proof once it had a `--baseline`.
- **Didn't:** the mission's own fixture instruction ("copied, attribution kept") was written without checking peer
  visibility. The first candidate canvas carried an RFC1918 subnet. My census cross-check also printed nothing on its
  first run, because a package-level re-export shadowed the submodule, and `hasattr` was silently always False.
- **Finding:** ⇒ ***a cross-check that cannot fail looks exactly like a cross-check that passed.*** The missing
  line was only noticed because the expected output had been decided in advance.
- **Change:** before copying a peer artifact into a public tree, check the peer repo's visibility first. Shape-derive
  when the peer is private. When probing a module for an API, import it by name.
- **Follow-up:** the P2b→P3 gate (operator). Then P4 memos carrying the signed LIP (Terminal regeneration · LP ·
  City · Automator · Socials · **PercySleep one-line migration** · QuantumProteins FYI). Firewall residue for the next
  touch: `conformance.py` advisories in CLI/report, plus the two v2.4.0 docstring/README pins.
