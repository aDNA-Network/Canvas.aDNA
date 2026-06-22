---
type: spec
spec_id: spec_context_object
title: "aDNA Canvas context-object model (D7) — canvas as a first-class context object"
standard_version: "2.0.2"
status: ratified
created: 2026-06-12
updated: 2026-06-12
last_edited_by: agent_stanley
phase: P2
resolves: D7
tags: [spec, canvas, context-object, primitive, lip, genesis, p2, d7]
---

# aDNA Canvas Context-Object Model (D7)

> **Status: RATIFIED 2026-06-12 (operator, P2 gate) — keep-as-view.** Specifies how an aDNA canvas is a
> first-class **context** object. The canvas-**as-primitive** question (Δ2) is ratified as **deferred to an open
> LIP** ([[lip_draft_canvas_as_primitive]]); the aDNA core primitive set is **untouched** (C3). RFC 2119 keywords.

## 1. The dual nature

An aDNA canvas is both **render-AS-output** (a 2D artifact: deck, paper, comic) and **read-AS-context** (a
structured object an agent loads to understand a domain). This spec governs the read-AS-context face: how a
canvas is stored, referenced, and versioned as a context object — orthogonal to how it renders.

## 2. Context-object metadata

2.1. A canvas declares its context identity in `_reserved.context_object`:
```
context_object:
  id:       <stable urn/slug>          # stable across regenerations
  version:  <semver>                   # the canvas's own content version
  refs:     [ <wikilink | federation_ref>, … ]   # outbound context references
  summary:  <short agent-facing description>      # optional
```
2.2. `id` **MUST** be stable across forward-regeneration (it is not the volatile per-node id). `refs` **MUST**
use existing aDNA reference forms — wikilinks for in-vault, `federation_ref` for cross-vault — so a canvas is
discoverable by the same machinery as any other context object.

2.3. A canvas referenced as context **SHOULD** be loadable by summary/refs without rendering — i.e. an agent can
traverse `refs` and read `summary` + component/panel structure as a context graph.

## 3. Δ2 — canvas-as-primitive vs canvas-as-view (deferred to a LIP)

3.1. **Today (aDNA Decision 9):** a canvas is a *view/serialization of the `lattice` primitive*, not a fourth
deployable primitive. The deployable set is {module, dataset, lattice}, extensible via `{namespace}_{type}`.

3.2. **The Δ2 question:** should a canvas be elevated to a **first-class primitive** (carrying semantics beyond
"a lattice rendered visually")? This spec **does NOT decide it** and **MUST NOT** alter the core primitive set.
The argument-for (a canvas carries panel/link + component + multi-surface semantics a bare lattice does not) and
the argument-against (those live cleanly in `_reserved` over a lattice view) are both real.

3.3. **Resolution path:** the elevation, if pursued, is a **Lattice Improvement Proposal** to the aDNA standard
(owned by `lattice-labs` / `aDNA.aDNA`), per [[adr_003_standard_governance]] §2. A draft is staged at
[[lip_draft_canvas_as_primitive]] for submission — **not ratified here**. Until a LIP ratifies otherwise, a canvas
**remains a view** and this spec's context-object metadata rides in `_reserved` (no core change).

## 4. Conformance

`context_object` is an **aDNA-Native** feature. A validator **MUST** check: `id` present + stable-typed; `version`
semver; every `ref` is a well-formed wikilink/federation_ref. Absent `_reserved.context_object` → the canvas is a
pure output artifact (not registered as context), still valid Core/Extended.

## 5. Related
- [[spec_adna_canvas_standard]] §7 (`_reserved`) · [[adr_003_standard_governance]] §2 (LIP) ·
  [[lip_draft_canvas_as_primitive]] (Δ2 draft) · [[p1_source_inventory]] (D7 stub) · [[p1_fork_baseline]] §4 ·
  `aDNA.aDNA` (core primitive set — untouched) · `lattice-labs/how/governance/lips/lip_0001_lip_process.md`.
