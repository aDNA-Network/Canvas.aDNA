---
type: registry
created: 2026-07-02
updated: 2026-09-11
last_edited_by: agent_mondrian
tags: [lip, governance, registry, canvas, authority_axis, production_axis, plumbline]
icon: list
---

# LIP Registry — Canvas.aDNA (Canvas-scoped view)

Canonical index of the Lattice Improvement Proposals **stewarded by Canvas.aDNA**, listed under their **global** LIP
numbers.

> **Registrar.** The global LIP number line is registrar'd by **aDNA.aDNA** (D3, proposed 2026-07-02 — handshake
> pending; see `who/coordination/coord_2026_07_02_lip_registrar_handshake.md`). Canvas stewards the *content* and
> *ratification* of its own LIPs (LIP-0008, LIP-0009) under their globally-assigned numbers; the registrar arbitrates
> number assignment across vaults. Until the handshake is acked, numbering here is **Canvas-provisional-final** under
> the numbers inherited from the predecessor line.
>
> **Predecessor line.** LIP-0001…LIP-0009 were assigned in the original `lattice-labs` registry (archived reader-only
> 2026-06-27 → `Archive.aDNA/lattice-labs/how/governance/lips/lip_registry.md`). LIP-0002…LIP-0007 belong to other
> domains (RBAC · protocol spec · character-NFT · Org-Graph · Network · ISS) and remain in that archived line — they
> are **not** copied here. LIP-0001 (the CC0 process doc) is forked as a Canvas-local working copy.

## Canvas-stewarded LIPs

| LIP | Title | Type | Status | Landed | Author | Date |
|-----|-------|------|--------|--------|--------|------|
| [[lip_0001_lip_process\|LIP-0001]] | LIP Purpose and Guidelines (Canvas-local working copy) | Process | Accepted | — | Stanley Bishop | 2026-03-07 |
| [[lip_0008_derived_surface_pure_metadata\|LIP-0008]] | Derived Surfaces as Pure Metadata (Canvas `panel_link` A-5 relaxation) | Standard | Final | v2.3.0 | Stanley Bishop (Mondrian-drafted) | 2026-06-20 |
| [[lip_0009_canvas_as_primitive\|LIP-0009]] | Canvas as a First-Class aDNA Primitive (evaluation) | Standard | Final (Option V) | — (no core change) | Stanley Bishop (Mondrian-drafted) | 2026-06-20 |
| [[lip_0010_assessment_diagrammatic_context\|LIP-0010]] | Diagrammatic context — the `authority`/`production` axis split (assessment → Standard proposal → **A-8**) | Standard | **Final** — Option D, §7.7 signed + implemented + cut 2026-09-11 (Gridline P1); **2 operator errata** (A1 asymmetric rule · A2 `interaction` back-fill) | **v2.4.0 (CUT)** | Stanley Bishop (Mondrian-drafted) | 2026-09-11 |

## Status (Canvas-stewarded)

| Status | Count |
|--------|-------|
| Draft | 0 |
| Review | 0 |
| Accepted | 1 |
| Implemented | 0 |
| Final | 3 |
| Rejected | 0 |
| Withdrawn | 0 |
| **Total** | **4** |

> **LIP-0008** is **Final** — the A-5 relaxation landed in **Canvas Standard v2.3.0** (Operation Beacon B4.2; suite
> 115/10, certification 11/11). **LIP-0009** is Final on **Option V** (keep canvas as a view; elevation deferred, no
> re-open — D2). **LIP-0010** is an **assessment** opened at Blueprint P1 (2026-08-24): it found that `authority` is
> normative in the proposed diagrammatic-context doctrine but **unvalidated** by `canvas_std` (~~0 of 21 in-vault
> `adna_native` canvases carry the key~~ — ⛩ **re-derived 2026-09-11: `4 of 25`**; the 08-24 figure is stale, and
> ⚠ its **complement is still exactly 21**, so it re-derives as a true number and reads as reproduced when it is not).
> Recommendation **Option B** — an optional validated enum, additive, v2.4.0 — was **deferred** and gated on Rosetta
> ratifying `pattern_diagrammatic_context`. ⛩ **They ratified 2026-09-11 and SPLIT the axis**, so Option B is
> **superseded in its cells and retained in its mechanism**: the shape survives, the three-value set does not.
> ⛩ **Converted to a Standard proposal 2026-09-11** (Plumbline P2): **Option D** — `authority`
> {`dual_channel`, `view`} + `production` {`hand_authored`, `generated`}, both optional, validated only if
> present, **two keys or neither**, additive, **v2.4.0**. ~~No change taken; firewall at diff-0 pending §7.7.~~
> ⛩ **§7.7 SIGNED 2026-09-11** at the Operation Gridline plan gate, then **implemented and CUT the same
> phase → FINAL**: `canvas_std` v2.4.0 validates both keys as **A-8** (suite 146/10, certification 12/12).
> ⚠ The signature was bounded to Option D's four-file table, and **two operator errata were ruled at the P1
> exit gate** rather than taken by the implementing agent: **A1** — the ratified *"two keys or neither"* was a
> misreading of *"both become binding together"* (a claim about **validation scope**) and was **self-defeating**,
> since this vault's own `variant_board`/`tuning_surface` deliberately emit `production` alone; the rule ships
> **asymmetric** (`authority` requires `production`). **A2** — `interaction` was missing from all **three**
> hand-maintained copies of the `_reserved` namespace since v2.2.0, because nothing read any of them; back-filled.
> ⛩ And the LIP's **backward-compatibility claim was false** when signed (F-GL-6): *"25 of 25 keep passing"*
> measured **23 of 25** — two untracked canvases still declared `authority: generator`, and **Plumbline P1's own
> census printed both rows** four lines from where the claim was written. Fixed by regeneration; A-8 failures now **0**.
> ⇒ ***the number a decision rests on is the one most worth re-deriving before you sign it.***

---
*LIP Registry — Canvas.aDNA · established Operation Beacon B4, 2026-07-02 · predecessor: `Archive.aDNA/lattice-labs/how/governance/lips/lip_registry.md`*
