---
type: federation_index
title: "Canvas.aDNA federation index — consumers of the Standard + Canvas's own consumed wrappers"
created: 2026-08-04
updated: 2026-08-04
last_edited_by: agent_mondrian
status: active
standard_version: "2.3.0"
source_census: how/campaigns/campaign_canvas_halftone/missions/artifacts/halftone_federation_census_20260804.md
tags: [federation, index, wrappers, consumers, canvas_standard]
---

# Canvas Federation Index

> **The living registry** (G8 closure, Halftone HF): who consumes the aDNA Canvas Standard, at what pin, in
> what health — plus the wrappers Canvas itself consumes. Born from the dated
> [2026-08-04 census](../campaigns/campaign_canvas_halftone/missions/artifacts/halftone_federation_census_20260804.md);
> **update THIS file** when wrappers change (last-verified column), and re-census only when drift is suspected
> fleet-wide. Contract every consumer conforms to: [`spec_federation_contract.md`](../../what/specs/spec_federation_contract.md)
> (§2.1 required `federation_ref` fields · §3 version policy — **a 1.x→2.x hop REQUIRES 5-stage re-validation** ·
> §4 gates incl. **Amendment 1's visual gate**: `canvas-std validate` + `canvas-visual-check` + agent-confirmed render).

## 1. Consumers of the Standard (canvas wrappers, deduped by rename-alias)

| Consumer (aliases) | Wrapper(s) | Pin | Policy | Health (2026-08-04) | Last verified |
|---|---|---|---|---|---|
| **Emacs.aDNA** | `canvas/` | **2.3.0** `adna_native` | minor | ✅ clean — the reference wrapper | 2026-08-04 (census) |
| **Network.aDNA** *(← aDNANetwork, LatticeNetwork)* | `canvas/` ×3 aliases | 2.2.0 | — | 🟡 pin lag; alias copies verbatim | 2026-08-04 |
| **GOTFN.aDNA** | `canvas/` | genesis (`planned`) | minor | 🟢 current for its stage | 2026-08-04 |
| **Home.aDNA** | `canvas/` | builder 1.0.0 | minor | 🟠 **stale runtime import path** via the `CanvasForge.aDNA` shim — highest functional risk in the fleet | 2026-08-04 |
| **WebForge.aDNA** *(← Websites)* | `canvas/` ×2 aliases | 1.1.0 @ `3783f57` | minor | 🟠 stale body (CanvasForge prose) + old pin | 2026-08-04 |
| **ScienceStanley.aDNA** | `canvas_deck/` · `canvas_comic/` | ~1.0 | minor | ✅ M-PL2-reconciled 2026-07-18; ⚠ comic wrapper carries an archive-only `context_ref` (M-PL3 resurrect decision pending Canvas-side) | 2026-08-04 |
| **ContextCommons.aDNA** | `canvas_deck/` | ~1.0 | minor | 🟠 stale body (live-CanvasForge cites) | 2026-08-04 |
| **Videos.aDNA** *(← VideoForge)* | `canvas_deck/` ×2 aliases | ~1.0 | minor | 🟠 stale title/body; **this refit is the Videos shim's named retire-condition** | 2026-08-04 |
| **Obsidian.aDNA** | `canvasforge/` (dir-rename → `canvas/` flagged post-their-P3) | provisional | minor | 🟢 target reconciled; pin verification due at their M09 | 2026-08-04 |
| **ZenZachary.aDNA** | `canvas/` · `canvas_comic/` · `canvas_deck/` | ~1.2.0 | minor | 🔴 stale identity (`wrapper_for`/`substrate_pin` = CanvasForge v1.2) — refederation memo staged | 2026-08-04 |
| **Astro.aDNA** *(← SiteForge)* | `canvasforge/` ×2 aliases | 1.1.0 @ `3783f57` | minor | 🔴 stale identity + dir-name — refederation memo staged | 2026-08-04 |
| **SuperLeague.aDNA** | `canvasforge/` | genesis-planning | per-target | 🔴 stale body; engagement-scoped (archives at W4) — light memo staged | 2026-08-04 |
| **Bearly.aDNA** | `canvas/` (EMPTY) | — | — | ⚪ seam designed at their P4 (`seam_canvas.md`); population at Bearly's pace | 2026-08-04 |
| **Oration.aDNA** | **NONE** | — | — | 🔴 the G7 enabling condition — **adopt-a-wrapper memo staged** | 2026-08-04 |

**Machine-ref compliance:** `federation_ref.source_vault` reads `Canvas.aDNA` in every populated wrapper — zero
broken refs; ALL drift is identity/pin/prose/path-level (census §1).

## 2. Wrappers Canvas.aDNA consumes

| Wrapper | Source vault (persona) | Pin | Policy | Notes |
|---|---|---|---|---|
| `comfyui/` | ComfyUI.aDNA (Vulcan) | **0.2.0** @ `a8a4356` (2026-08-03) | tracking | Restores the ex-`comfyforge/` consumer seam. **Vulcan follow-up #3 (index the wrapper): SATISFIED by this row.** Pending: #1 adjust `skills_used`/`workflows_used` at the first render session (H3/H4) · #2 archived-LoRA-dispatch-runner rehoming decision (H4). Sibling exemplars: WebForge + ZenZachary `comfyui/` wrappers. |
| `git/` | Git.aDNA (Grace Hopper) | per declaration | — | Git-ops federation (GitHub-public since P6 Wave 2). |
| `iii/` | III.aDNA (Argus Panoptes) | per declaration | — | Quality loop; live learning store `iii/what/context/canvas_iii_learning_store.jsonl` (the `iii` symlink resolves here; `iii_bridge` default repointed 2026-08-04, HR). |

## 3. Standing drift ledger (non-memo items — fold into consumers' next natural touch)

1. **Home runtime path** (§1) — flagged to Hestia in the refederation wave's courtesy notes; the import should
   land on `Canvas.aDNA/what/production/canvas_core` (post-pt09 home), not the archive shim.
2. **Network trio pin 2.2.0 → 2.3.0** — minor-policy auto-adopt is legal (§3); a one-line pin bump + re-run of
   stage 3 suffices; fold into the next Network session.
3. **ScienceStanley comic `context_ref`** — archive-only target; the resurrect-vs-repoint decision is
   Canvas-side (M-PL3 flag stands).
4. **Obsidian dir-rename** (`canvasforge/` → `canvas/`) — post-their-P3, per their ADR-010 note.
5. **Rename-alias dedupe** — Astro≡SiteForge · Videos≡VideoForge · Network≡aDNANetwork≡LatticeNetwork: each
   refit should land once and let the alias copies retire with their shims (Home §C windows).
