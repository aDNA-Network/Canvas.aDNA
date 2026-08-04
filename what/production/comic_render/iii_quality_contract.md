---
type: quality_contract
package: comic_render
campaign: campaign_canvas_halftone
created: 2026-08-03
updated: 2026-08-03
last_edited_by: agent_mondrian
status: active
tags: [iii, quality_contract, comic_render, bridge, halftone]
---

# III Quality Contract — comic_render

A **contract, not an engine**: III inspects the bridge's outputs against these gates; the bridge
itself never scores or reviews.

## §1 Inspect panel (lenses)

| Lens | Question |
|------|----------|
| Boundary | Zero render-engine imports (AST guard green); PIL only via `canvas_core.print`; `comic_generator` never imported |
| Immutability | Input canvas byte-untouched; `issue.rendered.canvas` is a NEW file; `_reserved.sync` byte-identical |
| Topology | `compute_sync_hash(rendered) == compute_sync_hash(source)` — write-back adds/removes nothing |
| Conformance | Rendered canvas: `validate_suite` aDNA-Native green, D-1/2/3 green |
| Provenance | Every rendered panel carries `render_provenance` (backend_chain · model · seed · prompt_hash · generated_at · selection_record) and a Schema-A record exists |

## §2 Quantitative gates

1. **Stage-6 gate** (`validate.py`): conformance + degradation + every `file` node target exists +
   sync-hash equality — hard fail.
2. **Idempotency**: any stage re-run against unchanged state performs zero new work (dispatch
   skips existing variants; write-back skips an existing rendered canvas; select skips recorded
   panels).
3. **Determinism (offline)**: the `fake` chain is reproducible byte-for-byte — same canvas → same
   variant bytes, same rendered topology, same page geometry.
4. **Budget**: with `budget_cap` set, projected spend over the cap dispatches NOTHING
   (`BudgetCapExceededError` before the first call).
5. **Placement golden**: composited page placements match the R5 geometry remap within ±1 px
   (the 663-vs-662.5 authoring slop).
6. **Effective DPI**: below-200 panels surface as warnings (never silently); R7 accepts the
   warning at H2/H3 v0 — the refine/upscale chain is the fix path.
7. **Visual rail (HV, amended H2 exit)**: `canvas-visual-check` on `issue.rendered.canvas` reports
   expected findings only + an agent-confirmed render of the composited page is recorded in the
   mission file.
