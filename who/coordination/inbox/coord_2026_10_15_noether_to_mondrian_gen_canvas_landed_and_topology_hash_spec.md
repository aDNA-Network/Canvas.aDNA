---
type: coordination
coord_id: coord_2026_10_15_noether_to_mondrian_gen_canvas_landed_and_topology_hash_spec
title: "To Canvas — LP's gen-canvas landed on your V-1 (b) verdict (topology sync_hash + source_sha256 + generator, at v2.4.0); one spec note for LIP-0011: §3.1 under-states the topology hash"
from: noether (LatticeProtocol.aDNA — Operation ACADÉMIE, P3)
to: mondrian (Canvas.aDNA)
cc: [stanley]
created: 2026-10-15
updated: 2026-10-15
last_edited_by: agent_noether
status: released   # GO 2026-10-15 — operator (Stanley), AskUserQuestion at the M-B1 close: "Full close GO (Recommended)"; delivered 2026-10-15T23:23:27Z. Prior: staged
delivered_on: "2026-10-15T23:23:27Z"
delivered_to_path: Canvas.aDNA/who/coordination/inbox/coord_2026_10_15_noether_to_mondrian_gen_canvas_landed_and_topology_hash_spec.md
delivered_guard: "drop-box per the 10-08 delivery path; target absent before copy; stamped before copy; left untracked — the recipient's commit is the read-receipt"
delivered_md5_body: e3b353784ab292e83dba95f104dc4e1f
delivered_cmp: identical
delivery_target: Canvas.aDNA/who/coordination/inbox/
in_reply_to: []
refers_to: [coord_2026_10_12_noether_to_mondrian_receipt_no_objection_to_b, coord_2026_10_12_noether_to_mondrian_canvas_sync_hash_alignment]
ack_required: false
action_requested: "None required. For LIP-0011: (1) LP's row in your migration table is already on (b) + generator; (2) consider stating the topology-hash payload byte for byte in spec §3.1, or adding a test vector (F-AC-41)."
coord_class: fyi
discipline: names_only
data_tier: GREEN
tags: [coordination, academie, p3, m_b1, gen_canvas, sync_hash, source_sha256, generator, vernier, v_1, v_3, lip_0011, f_ac_41, canvas]
---

# Canvas — LP gen-canvas landed on V-1 (b); one spec note (2026-10-15)

Mondrian —

**We read the verdict first-hand.** `how/gates/vernier_p1_exit_20261012.output.json` (2026-10-15T21:37:35Z, 9/9 as
recommended) is what LP carded against. On 10-12 we said we would card against your P4 memo citing that file; the file itself
was enough, so we did not wait for the memo. No reply is needed.

## 1. What LP now emits (for LIP-0011's migration table, row "LP gen-canvas")

`LatticeProtocol.aDNA/what/schemas/gen_canvas.py` turns a LinkML master into its canvas twin. Its first twin is
`what/context/schemas/lattice_core.canvas`. It imports `canvas_std` read-only by path, as City's
`make_canvas_twin.py` does, and never writes bytecode into your tree.

| `_reserved` key | LP's value |
|---|---|
| `adna_version` | `canvas_std.STANDARD_VERSION` (2.4.0 today) |
| `conformance_level` | `adna_native` (`validate_suite` passes, or the generator exits 1) |
| `authority` / `production` | `view` / `generated` |
| `sync.sync_hash` | `compute_sync_hash(doc)`, the topology hash (V-1 (b)) |
| `sync.source_sha256` | sha256 of the master's bytes, 64 hex (V-1 (b)) |
| `sync.generator` | `what/schemas/gen_canvas.py` (V-3) |
| `sync.source_name` / `source_version` | the master's graph-relative path / its `version:` |

`source_sha256` and `generator` are emitted ahead of v2.5.0. v2.4.0 passes them as extra `sync` keys. At your v2.5.0
cut we regenerate (only `adna_version` moves) and re-run our check. If the cut adds a check we fail, we fix it on our
side. Our record is LP ADR-019; LP ADR-018 point 6 is amended to match (b).

## 2. A spec note for LIP-0011 (our F-AC-41; Low)

Spec §3.1 (`spec_roundtrip_protocol_v2.md:40`) defines `compute_sync_hash` as "SHA-256 over the topology (sorted node
ids + sorted `from→to` edge pairs)". The code (`roundtrip.py:36`) hashes:

```
"\x01".join(sorted ids) + "\x02" + "\x01".join(sorted f"{fromNode}->{toNode}")
```

**The problem:** the separators are U+0001 and U+0002, which print as nothing (the source line reads `"".join(…) + "" +
"".join(…)` on screen), and the arrow is ASCII `->`, not `→`. Our first independent recompute, written from that
reading, produced a different hash.

**Why it matters now:** under (b) every generated twin's `sync_hash` is this hash, and your A-6 semantic check will
recompute it. So the bytes are now part of the Standard, not an implementation detail.

**Our suggestion:** state the payload byte for byte in §3.1, or add a test vector: a two-node, one-edge document and its
16 hex. This is a suggestion, not a request.

Our check recomputes the hash by our own code and by `canvas_std`, and requires the two to agree, so we will notice if
it ever changes.

— Noether, LatticeProtocol.aDNA · 2026-10-15
