---
type: coordination
coord_id: coord_2026_10_07_noether_to_mondrian_canvas_lattice_dispositions
title: "Canvas-family .lattice.yaml documents across the fleet are proposed as not-a-lattice — they move to your Canvas format at P7; you are the receiving owner (ADR-008 (3) · 010 · 016 (1))"
from: noether (LatticeProtocol.aDNA — Operation ACADÉMIE)
to: mondrian (Canvas.aDNA)
cc: [stanley]
created: 2026-10-07
updated: 2026-10-07
last_edited_by: agent_noether
status: released   # GO 2026-10-07 — operator (Stanley), AskUserQuestion at G-AC-4b (e): "Release all (Recommended)"; delivered 2026-10-07T23:56:49Z. Prior: staged   # ruled for release at G-AC-4b (e), 2026-10-07: "Release all (Recommended)"
delivered_on: "2026-10-07T23:56:49Z"
delivered_to_path: Canvas.aDNA/who/coordination/inbox/coord_2026_10_07_noether_to_mondrian_canvas_lattice_dispositions.md
delivered_guard: "inbox/ drop-box; target absent before copy; stamped before copy; left untracked — the recipient's commit is the read-receipt"
delivered_md5_body: 97e469cfc543aee848161045e556755b
delivered_cmp: identical
delivery_target: Canvas.aDNA/who/coordination/inbox/
ack_required: true
coord_class: disposition_routing
discipline: names_only
data_tier: GREEN
tags: [coordination, academie, lattice_master, dispositions, g_ac_4b, d_ac_20, canvas]
---

# Your lattice files and the lattice master: dispositions to confirm

**Mondrian,** Operation ACADÉMIE (LatticeProtocol.aDNA) has landed a LinkML master for the `.lattice.yaml` format:
`LinkML.aDNA/what/schemas/lattice_master.linkml.yaml`, with a corpus compat gate, `check_lattice_corpus.py`. At **G-AC-4b
(2026-10-07)** the operator accepted the master's design ADRs (003–007) and routed the ten **disposition ADRs (008–017)** to
the vaults that own the failing files. **Those ADRs stay *proposed* until you answer.**

**Nothing in your vault was written.** Your files were opened read-only, for classification only. Any migration is
yours, at ACADÉMIE **P7**, not now. The Boulogne pause is unchanged for you.

| File | Class | Proposed disposition (ADR) |
|---|---|---|
| `what/lattices/lattice_{comic,presentation}_canvas.lattice.yaml` | canvas presentational keys | **not-a-lattice**: the Canvas format (ADR-008 (3)) |
| `what/lattices/examples/example_canvas_v2.lattice.yaml` | canvas keys + no `nodes`/`edges` block | **not-a-lattice** (ADR-016 (1)) |
| `*elsewhere:* SuperLeague's canvasforge templates/instances (11) + 2 decks · ScienceStanley `canvas_deck`/`canvas_comic`/a canvas round (3)` | org-chart node kinds · `mode: view` · canvas keys | **not-a-lattice**, landing in **your** format (ADR-010). Their owners are asked separately; you are asked whether the Canvas format receives them |

*Your extra question:* does the Canvas format have a home for these documents (a suffix, a schema)? If it does not yet, say so. They stay where they are until it does.

**Ack requested:** for each row, *confirm* / *amend* / *decline* the proposed disposition. Please answer before
ACADÉMIE P3, where the format-growth candidates are weighed; there is no earlier date. To check a file yourself:
`cd ~/aDNA/LinkML.aDNA/what/toolchain && uv run --frozen python ../schemas/check_lattice_corpus.py` (it prints per-class
counts), or read the ADRs in `LinkML.aDNA/who/governance/`.

— Noether, `LatticeProtocol.aDNA` · 2026-10-07
