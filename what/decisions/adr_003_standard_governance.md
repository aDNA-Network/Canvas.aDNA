---
type: decision
adr_id: "003"
title: "Standard governance — v2.0.0 line, LIP change process, conformance levels, version policy"
status: proposed
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
signed_by:
supersedes:
superseded_by:
resolves: D6
phase: P2
tags: [adr, canvas, standard, governance, versioning, lip, conformance, genesis, d6]
---

# ADR-003: Standard Governance (D6)

## Status

**Proposed** — drafted at P2. **Operator ratifies at the P2 exit gate.** Sets the version line, change process,
and conformance levels that `spec_adna_canvas_standard.md` and the conformance suite (P3) bind to.

## Context

The aDNA Canvas Standard forks Advanced Canvas v5.6.6 + JSON Canvas 1.0 (PIN-A, [[p1_fork_baseline]] §1) and
supersedes the embedded v1.0.0. It needs a governed evolution mechanism. A real LIP process exists
(`lattice-labs/how/governance/lips/lip_0001_lip_process.md`, latest LIP-0007) usable as the change mechanism.

## Decision

### 1. Version line — **v2.0.0** (semver)
A clean **major** successor to the embedded v1.0.0. The major bump is justified by the net-new component model
(D4), panel/link semantics (D5), and context-object model (D7). Thereafter: **MAJOR** = a baseline-incompatible
change (must be rare; the C4 Obsidian-degradation contract makes most changes additive); **MINOR** = additive
`_reserved` extensions or new conformance-optional features; **PATCH** = clarifications/errata.

### 2. Change process — **LIP-style**
Normative changes to the Standard go through a **Lattice Improvement Proposal** (`lip_0001_lip_process.md`):
proposal → review → ratify, recorded in the LIP registry. The canvas-as-primitive question (D7/Δ2) is explicitly
a LIP (it touches the aDNA core), not a unilateral edit. Editorial/errata changes may skip the full LIP at the
maintainer's discretion (aDNA Labs).

### 3. Conformance levels — **Core / Extended / aDNA-Native**
| Level | Requires | Degradation |
|-------|----------|-------------|
| **Core** | Valid JSON Canvas 1.0 + the KEEP schema floor (node/edge required fields; explicit `toEnd:"arrow"`). | Is already a valid Obsidian canvas. |
| **Extended** | Core + Advanced Canvas v5.6.6 `styleAttributes` (shape/border/textAlign, path/arrow/pathfinding) within the `VALID_*` enums. | Degrades to Core by dropping `styleAttributes`. |
| **aDNA-Native** | Extended + a populated `_reserved` block (component_types / semantic_bindings / panel_link / context_object per the specs). | **Degrades to Extended/Core by stripping `_reserved`** (C4 strip rule). |

A canvas declares its level in `_reserved.conformance_level`. The P3 conformance suite tests each level + the
degradation transitions.

### 4. Consumer `version_policy` default — **minor**
Consumer wrappers (`federation_ref`) default to `version_policy: minor` (review required on a minor bump, auto-ok
on patch) — matching the SiteForge forge pattern. Producers may pin tighter.

## Consequences

### Positive
- A governed, auditable evolution path; the degradation contract keeps the MAJOR line stable and most change additive.
- Conformance levels give producers + the P3 suite a precise target vocabulary.

### Negative
- LIP overhead for normative changes (intended — the Standard is load-bearing).

### Neutral
- Whether a distinct `Standard.aDNA` sub-category is warranted is a P4/LIP question ([[adr_000_canvas_identity]] §1); does not block here.

## Related
- [[adr_000_canvas_identity]] §5 (v2.0.0 proposal) · [[adr_001_canvasforge_relationship]] · [[adr_002_literatureforge_seam]] ·
  `spec_adna_canvas_standard.md` (binds these levels) · `lattice-labs/how/governance/lips/lip_0001_lip_process.md`.
