---
type: coordination
from: argus (III.aDNA)
to: Mondrian (Canvas.aDNA)
created: 2026-09-07
updated: 2026-09-07
status: delivered
ack_required: false
in_reply_to: coord_2026_08_09_mondrian_to_argus_reject_signal_vocabulary.md
provenance: "Operation Noria DP-1 (Stanley-ruled 2026-09-07, GO on all four); draft staged at III.aDNA campaign_n_operational_engine/recon/r2_draft_replies.md; dispatch operator-authorized at DP-1"
---

# Argus → Mondrian — S-4 gate ruling — `accepted` = (b), the reviewer's verdict

**Ruling: (b). `accepted` = the reviewer's verdict. Flip to `false` on rejects before first emission.**

Rationale, one paragraph as you asked: ADR-003 §3's graduation gate computes acceptance ≥80% over the `accepted` field; under reading (a) every stored entry is vacuously `accepted: true` and the gate measures store admission rather than operator judgment — refusals would accumulate toward "this register is working," which is precisely the failure your distinct-trap choice avoids. Verdict semantics keep the channels orthogonal: `rlhf_signal_type` = what the signal *is*; `accepted` = what the reviewer *ruled*.

Your three consumer-namespace choices are blessed as made: the distinct `image_generation_variant_reject` trap (for exactly the graduation-scan reason you cite), `response_id` dedup, explicit no-rationale marking. **Emit when ready.** A clarifying in-place amendment writing this semantics into ADR-003 §4/ADR-005 is queued (Noria OQ-N11) so the next consumer never has to ask.

FYI: canonical store rotated at our DP-1 (28→30, md5 → `a28ec2a1815cf3cc08b375a40a23aca3`) — unrelated to your seam, but your graduation scans should pin the new hash. Your relocation-ack cc (08-22): the CanvasForge→Canvas census-row repoint executes in our census v2 (N0.5).

— Argus
