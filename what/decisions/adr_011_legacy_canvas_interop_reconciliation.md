---
type: decision
adr_id: "011"
title: "Legacy canvas-YAML interop reconciled — the `view` authority row, one level too high"
status: proposed
created: 2026-08-24
updated: 2026-08-24
last_edited_by: agent_mondrian
signed_by:
supersedes:
superseded_by:
phase: blueprint-p1
resolves: "Blueprint P1 charter item — rule the legacy-interop reconciliation (campaign_canvas_blueprint §Phases P1)"
tags: [adr, canvas, standard, legacy, canvas_yaml_interop, authority, view, blueprint, diagrammatic_context]
---

# ADR-011 — Legacy canvas-YAML interop reconciliation

## Status

**proposed** — authored at the Blueprint P1 doctrine session (`mission_b1_doctrine`, 2026-08-24);
awaiting the §7.7 signature. Canvas rules the *substance* (this is the Canvas Standard's own
authority surface); **propagation into the template channel is Rosetta's** and is offered, not
performed (Rule 10).

## Context

The 2026-02 `canvas_yaml_interop.md` spec defines a bidirectional `.lattice.yaml` ↔ `.canvas`
mapping. It predates the aDNA Canvas Standard, and the two have never been formally reconciled.
Operation Blueprint's P0 draft characterized the corpus it ships as **bare JSON Canvas** — no
`_reserved` block, invisible to tooling — and asked Rosetta to reconcile two incompatible systems.

**Measurement (2026-08-24) contradicts that diagnosis.** The count was right; the cause was not.

### Measured ground truth

| Object | Measured |
|---|---|
| Template example canvases | **196** real files across **46** live vaults (+**74** archived in `Archive.aDNA`, SO-7 retained) |
| Carrying a `_reserved` block | **196 / 196** — none are bare |
| Block contents | `{authority: "view", source_yaml, last_sync, sync_hash}` |
| Block **location** | `metadata._reserved` |
| Standard's canonical location | `metadata.frontmatter._reserved` (`what/docs/canvas_producer_quickstart.md:46`; named in A-2's own error text) |
| `canvas-std validate` | `declared=core  level_reached=extended  **[OK]**` |
| `canvas-std validate --level adna_native` | `[FAIL]` on **A-2 alone** |
| Interop **spec** copies | 69 total (50 live); 3 md5 variants differing only in the `last_edited_by` frontmatter line (one archived copy also has a stale `source_instance`) — **bodies uniform** |
| Template canvases across vaults | byte-identical (`template_architecture.canvas` → `md5 f9459bc3cbb21391fe28dd76d3e44902` in `.adna`, `Canvas.aDNA`, `Obsidian.aDNA`) |

The legacy has been emitting the `view` authority quartet since 2026-02 — to a path `canvas_std`
does not read. The block is **present and unread**, which is why it reports a green `[OK]` at `core`
while carrying semantics nobody validates.

## Decision

**The `canvas_yaml_interop` shape *is* the aDNA Canvas Standard's `view` authority row — named and
bounded under the Standard, not deprecated and not a competing system. Its defect is placement and
field shape, not design.**

1. **The legacy is ratified as a mode, not retired.** A `.canvas` that is a derived visualization of
   an authoritative non-canvas source (`.lattice.yaml`) is a **`view`-authority** canvas. Edits to it
   are view edits until reconciled through the Round-Trip Protocol. The interop spec keeps its
   mapping tables and color conventions; it defers to the Standard for **schema** and to
   `pattern_diagrammatic_context` for **authority semantics**.
2. **Canonical placement is `metadata.frontmatter._reserved`.** A `_reserved` block anywhere else is
   nonconformant — and specifically *worse* than absence, because it hides behind a green `core`
   validation. This is added to the pattern's anti-pattern list.
3. **The migration is mechanical, lossless in topology, and verified** (§Verified migration below).
   No node, edge, group, position, or color changes. Baseline-Obsidian degradation (D-1/D-2/D-3) is
   preserved.
4. **`authority` is doctrine-enforced, not machine-enforced — for now.** `canvas_std` does **not**
   know the key; it passes as an additive `_reserved` extension, so an invented or misspelled value
   is accepted silently. Closing that gap would be a schema change and therefore a LIP. It is
   assessed, **not** taken, in `lip_0010_assessment_diagrammatic_context.md`. **This ADR changes no
   code** — `what/code/canvas_std/` stays at diff-0.
5. **Propagation is offered, not performed.** One `.adna` edit plus a `skill_template_release`
   reaches all 46 vaults, because the files are byte-identical. Canvas supplies the verified recipe;
   Rosetta owns the template channel and the release.

## Verified migration

Executed on scratch copies of all four template canvases, then validated:

| Legacy `metadata._reserved` | Standard `metadata.frontmatter._reserved` |
|---|---|
| — | `adna_version: "2.3.0"` *(A-2)* |
| — | `conformance_level: "adna_native"` *(A-2)* |
| `sync_hash: "sha256:none"` | `sync.sync_hash: "<16 hex>"` — **nested and recomputed** via `compute_sync_hash()` (SHA-256 over sorted node ids + `from->to` pairs, truncated to 16). A-6 rejects the `sha256:`-prefixed form; it is not transliterable. |
| `source_yaml: ""` | `sync.source_name` — renamed; empty in 3 of 4, so a real value must be supplied |
| `last_sync` | no validated home — keep additive or drop |
| `authority: "view"` | no validated home (Decision 4) — keep additive |

```
$ canvas-std validate <migrated>/template_architecture.canvas --level adna_native
canvas-std 2.3.0: …/template_architecture.canvas
  declared=adna_native  level_reached=adna_native  [OK]
  degradation: {'D-1': True, 'D-2': True, 'D-3': True}
```

4 / 4 migrated files reach `adna_native [OK]` with degradation intact.

**Sync fields were never populated:** `sync_hash` is `"sha256:none"` ×3 / `"sha256:pending"` ×1 and
`source_yaml` is empty in three. The `view` contract has been *declared* for 6 months without ever
being *enforced* — the migration is the first time these files carry a real topology hash.

## Consequences

**Accepted:**
- Until the template release lands, 196 files remain `core`-valid and `adna_native`-invalid. This is
  a *known* state now rather than an unmeasured one, and nothing depends on them validating higher.
- `authority` remains unvalidated free text (Decision 4). A vault can write `authority: "veiw"` and
  no tool objects. Doctrine catches it at gate review; machines do not. Recorded, not hidden.
- Canvas cannot land the fix — it depends on Rosetta's template release. This ADR converts a
  6-month-old unowned drift into a named, recipe-complete offer.

**Reversibility:** high. The migration is additive plus a relocation; the legacy shape can be
restored from any file's own contents, and the topology hash is recomputable at will.

## Alternatives considered

- **Deprecate the interop spec and regenerate all 196 from source.** Rejected — throws away a
  working mapping and 196 hand-checked files to fix a path bug, and there is no `.lattice.yaml`
  source for three of the four templates (`source_yaml` is empty).
- **Teach `canvas_std` to read `metadata._reserved` as a fallback.** Rejected — a firewall change
  (LIP territory) that would legitimize two canonical paths forever and weaken A-2 for every future
  document to rescue four template files.
- **Leave it; the files validate green at `core`.** Rejected — they carry unread authority
  semantics, so every reader must guess whether editing them means anything. That is precisely the
  "undeclared authority" anti-pattern the doctrine names.

## Ratification (§7.7)

| Field | Value |
|-------|-------|
| Decision | `canvas_yaml_interop` = the Standard's `view` authority row · canonical placement is `metadata.frontmatter._reserved` · migration verified, offered to Rosetta, not performed · `authority` stays doctrine-enforced pending LIP-0010 · no `canvas_std` change |
| Ratified by | _(pending)_ |
| Date | _(pending)_ |
| Status | **proposed** |
