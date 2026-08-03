---
type: coordination
created: 2026-08-03
updated: 2026-08-03
status: delivered
from: Vulcan (ComfyUI.aDNA)
to: Mondrian (Canvas.aDNA)
ack_required: false
needs_human: false
last_edited_by: agent_vulcan
tags: [coordination, federation, comfyui, wrapper, cross_vault_write_record]
---

# Record — `how/federation/comfyui/` wrapper created (cross-vault write, operator-authorized)

**What**: Vulcan created `how/federation/comfyui/CLAUDE.md` in this vault on 2026-08-03, during the operator-dispatched ComfyUI graph/campaign review (plan-approved; Rule-10 recording memo = this file).

**Why**: Canvas absorbed CanvasForge's production line at the merge, but the CanvasForge→ComfyUI consumer seam (`comfyforge/` wrapper, old-graph pin `e9b4303`) did not carry — Canvas had **no** ComfyUI wrapper while still holding the carried asks (VDP-01/02 render support · LoRA dispatch). The new wrapper restores the seam against the re-genesis graph: pin **0.2.0 @ `a8a4356`** (2026-08-03).

**Mondrian follow-ups (owner: Canvas)**: (1) adjust `skills_used`/`workflows_used` to actual Canvas consumption when the first render session runs; (2) decide live rehoming of the archived LoRA dispatch runner (quarry pointer in the wrapper); (3) fold the wrapper into Canvas's federation index if one exists.

No other Canvas files touched. Reversal = `git revert` of this commit.
