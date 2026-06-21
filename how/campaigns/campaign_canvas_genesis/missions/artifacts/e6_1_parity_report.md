---
type: artifact
artifact_class: parity_report
created: 2026-06-20
updated: 2026-06-20
last_edited_by: agent_stanley
mission: mission_e6_1_parity_validation
campaign: campaign_canvas_genesis
verdict: GREEN
tags: [artifact, parity, regression, validation, keystone, e6, cross-system]
---

# E6.1 — Cross-system parity validation report

**Operation Keystone, Phase E6 (Validation & cutover), mission E6.1.** Campaign-level confirmation that the
shipped deliverable — `canvas_std` (the aDNA Canvas Standard v2.0.0 reference impl) — does not regress any
consumer, original or net-new. Run 2026-06-20 (operator-authorized E5→E6 crossing).

**Verdict: GREEN.** All four suites green at recorded counts; all examples conformance-clean; the two-shelf
firewall intact; `canvas_std` provably frozen since E0.2; the CanvasForge cross-system parity leg structurally
reproduces the locked reference (one benign, fully root-caused delta — see §3).

## 1. Suite + lint matrix

| Package | Path | Result | Lint |
|---|---|---|---|
| `canvas_std` (reference impl) | `what/code/canvas_std/` | **46 passed / 8 skipped** | ruff clean |
| `brief_consumer` (E4.3) | `what/production/brief_consumer/` | **10 passed** | ruff clean |
| `deck_generator` (E4.4) | `what/production/deck_generator/` | **16 passed** | ruff clean |
| `document_generator` (E4.1/E4.2) | `what/production/document_generator/` | **37 passed** | ruff clean |

All counts match the campaign-recorded baselines (46/8 · 10 · 16 · 37). No regression.

## 2. CLI conformance (build → `canvas-std validate`)

Each consumer example was rebuilt through its CLI to a scratch path and validated (committed goldens untouched):

| Example | declared | level_reached | OK | degradation D-1/D-2/D-3 |
|---|---|---|---|---|
| `brief_consumer/canvas_standard_brief` | adna_native | adna_native | ✅ | True / True / True |
| `deck_generator/canvas_standard_deck` | adna_native | adna_native | ✅ | True / True / True |
| `document_generator/canvas_standard_whitepaper` | adna_native | adna_native | ✅ | True / True / True |
| `document_generator/grant_proposal` | adna_native | adna_native | ✅ | True / True / True |

CLI banner: `canvas-std 2.0.0`. All four reach `adna_native` and degrade cleanly to Extended/Core (D-1..D-3).

## 3. Cross-system parity — the CanvasForge KEEP-reference leg

Re-ran the E3.3 deterministic parity proof (`e3_3_parity_check.py`, reused verbatim) via the CanvasForge `.venv`
(now resolved through the `Archive.aDNA/CanvasForge.aDNA` back-compat symlink). Raw capture:
`e6_1_parity_recheck_capture.json`.

| Metric | E3.3 (2026-06-13) | E6.1 (2026-06-20) | Assessment |
|---|---|---|---|
| deck nodes / edges | 56 / 20 | **56 / 20** | identical |
| deck floor rejects | 0 | **0** | identical |
| deck fingerprint (types/colors/shapes) | — | `{file,group,text}` / `{2,3,4,5}` / `{pill}` | matches committed ref |
| comic nodes / rejects | 11 / 0 | **11 / 0** | identical (static committed canvas) |
| `deck_norm_sha256` | `aa675665…` | `0d741640…` | **drift — investigated, §3.1** |
| locked baseline `baseline_vr_scores.json` SHA | `3ce4d341…` | `3ce4d341…` (untouched) | unchanged (Critical Rule 2 held) |

### 3.1 The SHA drift is a relocation artifact, not a regression

The `deck_norm_sha256` differs from the E3.3 capture. This was run down rather than waved:

- **Not date volatility** — no date-like strings in any node body.
- **Not within-process nondeterminism** — two rebuilds in one process are byte-identical.
- **Not hash-seed nondeterminism** — `deck_norm_sha256` is stable across `PYTHONHASHSEED` ∈ {0,1,2,42}.
- **Not a deliverable change** — `canvas_std` (`schema.py` + all src) is git-frozen since **E0.2** (`e2b1a5d`; only the
  E0.1/E0.2 commits ever touched `canvas_std/src`); `canvas_core` frozen since **E3.2** (`1a51801`);
  `canvas_presentation` and `build_wilhelm_parity.py` git-frozen; working trees clean.

**Root cause (isolated by diffing today's rebuild against the committed, 8.80-scored reference deck
`wilhelm_parity.canvas`):** exactly **one** of 56 node bodies differs, and only in an embedded **absolute image
path** (the old CanvasForge deck builder emits `Path(...).resolve()` absolute asset paths):

| Source | embedded image path |
|---|---|
| committed reference (built on herb's machine, Apr 29) | `/Users/herb/lattice/CanvasForge.aDNA/.../429faba73377f906_v1.png` |
| E3.3 rebuild (stanley, pre-archive) | `/Users/stanley/aDNA/CanvasForge.aDNA/.../429faba73377f906_v1.png` |
| E6.1 rebuild (stanley, post-pt09 archive) | `/Users/stanley/aDNA/**Archive.aDNA**/CanvasForge.aDNA/.../429faba73377f906_v1.png` |

The pt09 Production-Tidy move (2026-06-17) physically relocated the vault into `Archive.aDNA/`; `.resolve()`
follows the `CanvasForge.aDNA` symlink to the new real path, changing that one node's `file` string. **55/56 node
bodies are byte-identical, the fingerprint is identical, counts are identical, and floor rejects are 0** → the deck
is structurally reproduced; only a machine/location-specific absolute path moved. This is orthogonal to
`canvas_std` and does not touch the rendered visual (same image file, relocated path) so the locked **Wilhelm 8.80
/ Issue 01 8.43** VR baselines carry over unchanged (as at E3.3).

### 3.2 Shim output-neutrality still holds (by construction)

E3.2 repointed only the floor *constants*, which are `is`-identical frozen objects re-exported from the frozen
`canvas_std.schema`. With both `canvas_core` and `canvas_std` frozen since E3.2/E0.2, the E3.3 "shim-ON ≡ shim-OFF"
result is unchanged. The 0 floor-rejects on both deck (56) and comic (11) re-confirm the federated floor accepts
every reference value.

## 4. Firewall invariant

- `canvas_std` tracked git-diff vs HEAD: **empty** (no schema/API/code change).
- No untracked files under `canvas_std/` (excluding `.venv`/caches).
- `schema.py` last commit: **E0.2** — the floor has not moved since it was ported.

## 5. Findings → handoff

- **PT-P5 re-baseline note:** when `canvas_core` + `canvas_presentation` relocate to `Canvas.aDNA/what/production/`
  at PT P5, the parity capture's `deck_norm_sha256` should be **re-baselined** at the new resident path, and the
  deck builder's absolute-image-path embedding noted as a **portability nit** (machine/location-specific; ideally
  relative or content-hash-keyed). Not a `canvas_std` defect; tracked as a KEEP-reference observation.
- No new `canvas_std` errata. The 4 spec-gap erratum candidates from E4.1/E4.2 remain in the LIP queue (`adr_003`),
  untouched by this validation.

## Conclusion

`canvas_std` v2.0.0 is validated across the full consumer set with **no regression**: four suites green, four
examples conformance-clean, firewall intact, the floor provably frozen, and the CanvasForge cross-system leg
structurally reproducing the locked reference. The single SHA delta is a fully-explained relocation artifact in the
archived KEEP reference. **E6.1 verdict: GREEN** — clears the cutover-criteria parity input for E6.2.
