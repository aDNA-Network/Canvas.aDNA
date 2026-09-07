---
type: pattern_draft
title: "Pattern: Diagrammatic Context (dual-channel prose + canvas)"
proposed_home: aDNA.aDNA/what/patterns/pattern_diagrammatic_context.md
proposed_by: mondrian (Canvas.aDNA), Operation Blueprint P0
adoption_authority: rosetta (aDNA.aDNA) — this is a DRAFT staged for their ruling; Canvas does not write into aDNA.aDNA
created: 2026-08-22
updated: 2026-08-24
last_edited_by: agent_mondrian
status: staged_for_rosetta
errata: "E1 (2026-08-24, Blueprint P1) — legacy-corpus diagnosis corrected by measurement; see §Erratum E1. Count (196) unchanged. · E2 (2026-09-04, Blueprint P2) — the authority axis mixes two questions, and the conformance floor was unachievable as written; both found by BUILDING the pattern. See §Erratum E2."
empirical_anchor: Emacs.aDNA (REQ-Q01/REQ-O05/REQ-H05, ratified, running since 2025-07 at Standard 2.3.0)
tags: [pattern, draft, canvas, diagrammatic_context, dual_channel, authority_model, upstream]
---

# Pattern: Diagrammatic Context

## Problem

Agents and operators reason about *structures* — architectures, seams, flows, topologies — but the
fleet's context is overwhelmingly prose. Where diagrams exist they are ad-hoc: 145 real `.canvas`
files live across 18 vaults today, and their conformance is bimodal. Emacs authors fully
aDNA-Native canvases; Operations, ScienceStanley, Regenesis, and aDNALabs author genuinely
excellent diagrams as **bare JSON Canvas** — no `_reserved` block, no conformance level, no sync
discipline, invisible to `canvas-std validate` and to every canvas-aware tool. Worse, **four
incompatible authority models** coexist with no doctrine choosing between them, and the 2026-02
`canvas_yaml_interop.md` legacy (69 copies, 50 of them in live vaults; **196** template `.canvas`
examples across 46 vaults) predates the aDNA Canvas Standard entirely.

> **⚠ Erratum E1 applies to this paragraph.** The *hand-authored* diagrams above are bare JSON
> Canvas as described. The **196 template-shipped** files are **not** — they carry a `_reserved`
> block written to a non-canonical path. See §Erratum E1 before ruling on the legacy.

The demand is proven — vaults keep inventing this independently. The doctrine is missing.

## Pattern

**Every key artifact MAY — and load-bearing architectural artifacts SHOULD — carry two channels:**

1. **Prose channel** (`.md`) — authoritative for *meaning*: rationale, constraints, provenance.
2. **Canvas channel** (`.canvas`, aDNA-Native conformant) — authoritative for *structure*: the
   components, seams, and flows, positioned and typed.

**The dual-channel law (graduated from Emacs REQ-Q01):** the two channels update **in the same
mission**. A change that touches one and not the other is a *defect*, caught at gate review
(REQ-O05: canvas-sync review at every gate). Canvas files are **vault citizens** (REQ-H05):
openable, linkable (`[[wikilink]]`-able), searchable beside markdown — never a build directory's
private output.

### The authority axis (reconciling the four models)

Every diagrammatic-context canvas declares its authority in `_reserved`:

| `authority` | Meaning | When |
|---|---|---|
| `dual_channel` | Prose owns meaning; canvas owns structure; same-mission sync (drift = defect). | **Default for context/architecture canvases** — the Emacs model. |
| `generator` | The canvas is a build product of a source (YAML + script); never hand-edit; regenerate. Carries `source_*` + hash fields. | Fleet-scale projections (Home's `topology.canvas`). |
| `view` | A derived visualization of an authoritative non-canvas source (`.lattice.yaml`); edits are view edits until reconciled (Round-Trip Protocol / Obsidian ADR-010 §3). | Lattice visualizations — the legacy interop's home. |

`none` is retired: a canvas with no declared authority is nonconformant diagrammatic context.

### Conformance floor

- Validates at `adna_native` (`canvas-std validate`), Standard ≥ 2.3.0 pin in the vault's
  `canvas/` federation wrapper.
- Passes the visual gate (agent-confirmed render — a canvas that validates but renders unreadable
  is not context; Amendment 1).
- Topology canvases follow `Canvas.aDNA/what/context/context_canvas_topology_graphs.md` v1.1
  (placement over routing; angle-aware crossing budget; size/density bounds).

### Legacy reconciliation (the ruling this draft asks Rosetta for)

The 2026-02 `canvas_yaml_interop.md` spec and its `_reserved: {authority: "view", source_yaml,
sync_hash}` shape become **the `view` row of the authority axis** — i.e., the legacy is not wrong,
it is *one mode*, now named and bounded, under the Standard. **Measurement (E1) strengthens this:
the legacy already emits exactly that quartet in all 196 template files — it is not a shape to be
mapped onto the `view` row, it *is* the `view` row, written to a path the validator does not read.**
Concretely: (a) the interop spec gains a header deferring to the aDNA Canvas Standard for schema and
to this pattern for authority semantics; (b) the 196 `what/lattices/examples/*.canvas` template files
**relocate** their existing `_reserved` block from `metadata._reserved` to the canonical
`metadata.frontmatter._reserved`, gain `adna_version` + `conformance_level`, and have their stub sync
values populated — no node or edge changes — at the next `skill_template_release`; (c)
`template_node_adna_exemplar`'s canvas stubs carry this pattern's frontmatter so every newly forked
vault inherits the doctrine, not just the files.
Also proposed: re-point `how/backlog/idea_diagram_missions_herb.md` (already co-assigned
Rosetta + Mondrian) from rendered-figures-for-the-website to canvas-companions-as-context — the
Dual Method's "mermaid as structural ground truth" slots directly into the canvas channel
(`diagram_generator` already derives Mermaid).

## Evidence

- **Emacs.aDNA** — 13 months of the exact pattern, ratified (c01–c06 canvases, `adna_native`,
  `component_types` + `sync` blocks; per-mission "Canvas duty" steps). The pattern is a
  *graduation*, not an invention.
- **Unserved demand** — Operations' five C08 liaison canvases (with an invented legend convention),
  Regenesis's 11 design canvases, ScienceStanley's 29 production canvases: all standard-blind, all
  convertible with zero content change. *(These are the genuinely bare ones; the template-shipped
  196 are a different case — E1.)*
- **Substrate readiness** — the Standard needs **no change** (Emacs ships on 2.3.0 unmodified);
  `canvas_std` validate/roundtrip/conformance + 14 visual traps + `diagram_generator` already exist.

## Adoption mechanics

Per-vault cost is one wrapper pin + frontmatter on existing canvases. Rollout rides Operation
Blueprint P3's re-pin wave (lockstep-flip: wrapper pin + conformance state advance together, the
VisualDNA ADR-002 ceremony). Conversion offers to the standard-blind vaults come with the work
done for them (Blueprint P2).

## Anti-patterns

- **Canvas-as-screenshot** — an image of a diagram is not diagrammatic context; the structure must
  be typed nodes/edges, queryable and diffable.
- **Silent drift** — updating prose without the canvas (or vice versa) in a dual-channel pair.
- **Undeclared authority** — a `.canvas` with no `authority` field forces every reader to guess
  whether editing it means anything.
- **Bare JSON Canvas for context** — degrades fine *visually* but is invisible to validation,
  sync, and every canvas-aware tool.
- **`_reserved` off the canonical path** — a block at `metadata._reserved` (or anywhere but
  `metadata.frontmatter._reserved`) is *present and unread*: it looks conformant to a human reader
  and is invisible to `canvas_std`. This is the failure mode E1 found in 196 files, and it is worse
  than a missing block because it hides behind a green `[OK]` at `core`.

---

## Erratum E1 — legacy-corpus diagnosis corrected (2026-08-24, Blueprint P1)

This draft and its delivery memo (#9, 2026-08-22) were authored from a fleet survey. Re-measuring
before ruling corrected the diagnosis. **The count was right; the cause was not.**

| As drafted | Measured 2026-08-24 | |
|---|---|---|
| **196** template `.canvas` files | **196** real files / **46** live vaults (+74 archived, SO-7) | ✅ correct |
| "bare JSON Canvas — no `_reserved` block" | **196/196 carry** `{authority: "view", source_yaml, last_sync, sync_hash}` | ❌ wrong |
| "invisible to `canvas-std validate`" | true — but by **placement**, not absence | ⚠️ right effect, wrong cause |

**Root cause:** the legacy writes to `metadata._reserved`; the Standard's canonical path is
`metadata.frontmatter._reserved` (`what/docs/canvas_producer_quickstart.md:46`; named in A-2's own
error text). `canvas_std` reads the canonical path, finds nothing, reports `declared=core`.

```
$ canvas-std validate what/lattices/examples/template_architecture.canvas
  declared=core  level_reached=extended  [OK]
$ canvas-std validate … --level adna_native
  declared=adna_native  level_reached=extended  [FAIL]
  - A-2: aDNA-Native canvas requires a populated metadata.frontmatter._reserved block
```

Green at `extended`; fails `adna_native` on **A-2 alone**. Sync fields are unpopulated in all four
(`sync_hash` `"sha256:none"` ×3 / `"sha256:pending"` ×1; `source_yaml` empty in three) — the `view`
contract was declared but never enforced.

**Effect on the ask:** it shrinks. Not "reconcile two systems" but "relocate a block and add two
identity fields," lossless and mechanical — and the files are byte-identical fleet-wide
(`template_architecture.canvas` → `md5 f9459bc3cbb21391fe28dd76d3e44902`), so it is one `.adna` edit
plus a release, not a 46-vault sweep. Delivered to Rosetta as
`coord_2026_08_24_mondrian_to_rosetta_census_erratum.md`. Canvas's own ruling on the substance:
`what/decisions/adr_011_legacy_canvas_interop_reconciliation.md`.

---

## Erratum E2 — two defects found by *building* the pattern (2026-09-04, Blueprint P2)

E1 corrected a diagnosis by re-measuring. **E2 corrects the pattern itself by using it.** Canvas
authored the first two dual-channel canvases in its own tree (`context_canvas_surface_legs`,
`adr_004_production_code_layout`) and both defects surfaced within the first build.

### E2.1 — the authority axis mixes two independent questions

The axis as drafted presents `dual_channel` / `generator` / `view` as three peer values. Building
one shows they are not peers. Two different questions are being answered by one field:

| Question | Answers |
|---|---|
| **Who owns the meaning?** | prose (`dual_channel`) · an authoritative `.lattice.yaml` (`view`) |
| **How is the artifact produced?** | hand-authored · machine-generated (`generator`) |

Canvas's two dogfood canvases are **`dual_channel` and machine-generated simultaneously**: prose owns
the meaning, and the `.canvas` is built by `diagram_generator` from a `.diagram.yaml` beside it. The
drafted `generator` row's discipline — *"never hand-edit; regenerate"* — applies to them **exactly**,
yet their authority is `dual_channel`, so a reader following the axis literally gets no instruction
not to hand-edit them.

⇒ **Proposed (Canvas does not rule this — it is the pattern's, and the pattern is Rosetta's):** keep
the three values for compatibility, and state that *the no-hand-edit discipline attaches to
**generation**, not to the `generator` value.* A `dual_channel` canvas with a machine source carries
it too. If a cleaner separation is wanted later, the honest shape is two fields
(`authority` + `production`) — **but that is a schema change and this draft's whole posture is that
2.3.0 suffices**, so it is named and not proposed.

### E2.2 — the conformance floor was unachievable for a whole class of canvas

> ⛩ **Corrected 2026-09-06, before this erratum was delivered.** The heading and two sentences below
> originally read *"unachievable, by anyone, for 13 months"* and *"could not be passed by any canvas
> containing a titled group."* **Both were overstatements, in an erratum whose thesis is that
> plausible claims survive review.**
> - **Duration:** the two traps cannot conflict before the later of them exists —
>   `cv_hierarchy_01.py` **2026-06-22**, `cv_lead_cost_01.py` **2026-08-03**. The conflict was live
>   **~1 month**, not 13. The "13 months" came from this document's own Evidence line about
>   Emacs (§Evidence, still correct there) and was carried into an unrelated claim.
> - **Scope:** *"by anyone"* is wrong. The trap corpus has a **profile mechanism**
>   (`knowledge-canvas` · `comic` · `all`), and comic-profile canvases cleared the gate throughout.
>   The true claim is **"any `knowledge-canvas`-profile canvas with a titled group."**
>
> ⭐ **And the profile mechanism changes the recommendation.** `_KNOWLEDGE_CANVAS_AESTHETICS` already
> expresses *"this aesthetic check does not apply in this domain"* — which is what the conflict
> actually needs. **`####` is a workaround, not the fix.** The durable resolution is a trap-level or
> profile-level reconciliation owned by the trap corpus, and this erratum should not be read as
> proposing `####` as doctrine for the fleet.

The draft's §Conformance floor requires a canvas to pass "the visual gate (agent-confirmed render —
Amendment 1)" alongside `canvas-std validate`. Measured at P2: **the machine visual gate
(`canvas-visual-check --strict`) could not be passed by any **`knowledge-canvas`-profile** canvas
containing a titled group.** *(Scope corrected 2026-09-06 — see the note above; comic-profile
canvases were never affected.)*

Two shipped traps in the same profile impose mutually unsatisfiable requirements:

- `CV-HIERARCHY-01/title_slot_missing` requires a **markdown heading marker** on a text node in the
  group's upper 40%.
- `CV-LEAD-COST-01/heading_lead` flags `h1`/`h2`/`h3` leads, its docstring stating the rule as
  *"never use `#`/`##`/`###` to title a canvas text node."*

Every lead form was measured against both. `h1`/`h2`/`h3` satisfy hierarchy and trip lead-cost;
`**bold**` does the reverse; `#####`/`######` pass both **only by classifying as `plain`** — i.e. by
not being headings at all, which is a green check for the wrong reason. **`####` (h4) alone**
satisfies both as a real heading, at 42.6px against bold's 40.0px optimum.

Corroboration that this was latent rather than theoretical: `diagram_generator`'s **own shipped
example** had been failing three traps since Atelier (2026-06-21) with its Mermaid source node at
**~14% shown**, and `deck_generator`'s example carries 19 findings including 4 `heading_lead`. The
gate is declared mandatory in `skill_canvas_producer_build.md` §6 and was evidently not being run —
the trap corpus grew (14 traps now) and the shipped examples were never re-gated against it.

⇒ **Effect on the pattern:** the conformance floor is *correct* and is now **achievable** — Canvas
fixed `diagram_generator` (title slot · content-sized code node · content-scaled group padding ·
title/rank overlap) and all three canvases now pass `--strict` clean. But a floor that no artifact
could clear went unnoticed **because nobody built against it.** A pattern proposing a
conformance floor should ship with at least one artifact that demonstrably clears it; this draft did
not, until now.

⚠ **And the human half of that floor is NOT met here.** The agent-confirmed render (Amendment 1) was
attempted and abandoned: Obsidian is a desktop app, so `screencapture` takes the whole screen, and
the second attempt recorded a third party's private messages. Both dogfood canvases are
`visual_gate: pending`. The machine check is **not** a substitute and is not reported as one. A
window-scoped capture (Home.aDNA's `canvas_visual_loop.py`) is the missing tooling.

**Canvas-side records:** `mission_b2_authoring_rail` findings F-P2-3 · the rail
`how/skills/skill_canvas_context_diagram.md` · the two worked examples named above.
