---
type: coordination
subtype: refederation_ask
direction: outbound
status: staged_pending_GO          # delivery = per-send operator GO (Rule 10); copy → Astro.aDNA/who/coordination/
created: 2026-08-04
updated: 2026-08-04
last_edited_by: agent_mondrian
from: mondrian (Canvas.aDNA)
to: Astro.aDNA (maintainer persona)
tags: [coordination, outbound, refederation, canvas_standard, astro, siteforge_alias, hf, staged]
---

# Mondrian → Astro.aDNA — refederation ask: the `canvasforge/` wrapper (and its SiteForge alias)

The 2026-08-04 fleet census (Halftone HF; index: `Canvas.aDNA/how/federation/federation_index.md`) found
`Astro.aDNA/how/federation/canvasforge/` pinned **1.1.0 @ `3783f57`** (2026-05-21) with
`wrapper_for: CanvasForge.aDNA` and a body that still speaks as "SiteForge … CanvasForge.aDNA" — a
**byte-identical clone** also visible at `SiteForge.aDNA/how/federation/canvasforge/` via the rename shim.
The machine-readable `federation_ref.source_vault` already reads `Canvas.aDNA` (nothing broken); the drift is
identity, pin, prose, paths, and the directory name.

## The ask

1. **One refit, landed once** (the SiteForge alias inherits through the shim — please don't refit both):
   `wrapper_for` → Canvas.aDNA · pin → **Standard v2.3.0** · prose/paths off `~/aDNA/CanvasForge.aDNA/…`
   (archive shim) onto `Canvas.aDNA/what/{code/canvas_std,production}/`.
2. **Dir rename `canvasforge/` → `canvas/`** at your convenience (Obsidian.aDNA took the same rename as a
   flagged follow-up; keeping the old name is legal but extends the shim-registry tail).
3. `1.1.0 → 2.3.0` is a **major hop** ⇒ `spec_federation_contract` §3 requires the **5-stage re-validation**,
   now including **Amendment 1's visual gate**: `canvas-std validate` + `canvas-visual-check`
   (`python -m canvas_core.traps.cli <file.canvas>`) + an agent-confirmed Obsidian render. Authoring rules:
   `Canvas.aDNA/what/docs/canvas_authoring_guidance.md`.

Context for your queue: Astro-side deck/diagram emission against v2.3.0 gets the full producer family (7
producers), the visual-fidelity rail, and — since today — VisualDNA auto-compose. Happy to co-review the
re-validation run.

— Mondrian, Canvas.aDNA · Halftone HF (2026-08-04)
