---
campaign_id: campaign_canvas_gridline
type: campaign
title: "Operation Gridline — the Standard learns both axes, and the producers stop being the only thing that knows"
owner: stanley
status: active
estimated_sessions: "1-3"
phase_count: 6
mission_count: "created at phase-open"
priority: high
executor_tier_default: opus
predecessor: campaign_canvas_plumbline
created: 2026-09-11
updated: 2026-09-11
last_edited_by: agent_mondrian
status_history: "active (2026-09-11 — chartered at the plan gate, on the §7.7 signature that Plumbline left as its single live item) · P0 push discharged (8 commits, 22a101b..036e156), §7.7 signed, two gate-manifest defects found by RUNNING the baseline"
tags: [campaign, canvas, gridline, lip_0010, standard_v240, firewall, authority_axis, production_axis, reserved_keys, gate_manifest, a8]
---

# Campaign: Operation Gridline

> Named for what a grid is made of. Mondrian's grid is not the fields — it is the **lines**, and a line
> is only load-bearing where something is actually held to it. Plumbline established that there are two
> axes; this campaign is the difference between two axes *written down* and two axes **enforced**.

## Why this campaign exists

Operation Plumbline closed 2026-09-11 with a single live item: the **LIP-0010 §7.7 signature**. It was
given at this campaign's plan gate, and with it a scope ruling and a push GO.

The state it authorizes work on, measured rather than asserted:

- The axis enum is enforced in **exactly two places, both ours** — `canvas_core/conform.py:60-65` and
  `diagram_generator/src/diagram_generator/model.py:39`.
- Every other producer in the fleet, and every hand-authored canvas across **15+ wrapper vaults**, can
  write `authority: "veiw"` and receive a green `[OK]`.
- **Both of our own modules say so in their own error text**: *"canvas_std does not validate this key
  (F-B1-2), so it is checked here or nowhere."*

⭐ **The campaign's own definition of done is that those two sentences in our source become false** —
and that we go and change them where they are written, rather than leaving true-sounding comments
behind a changed reality. That is the P3 job, and it is the half a version bump usually forgets.

## What the signature does and does not authorize

| | |
|---|---|
| ✅ Authorizes | the **four-file touch** in LIP-0010 Option D's table, and a **v2.4.0** cut |
| ⛔ Does not authorize | mandating either key on any canvas (the ruled pattern declines it, and so does the LIP) |
| ⛔ Does not authorize | anything outside that table — see F-GL-1, which found something the table could not have known |

`adr_007` discipline applies: the firewall lifts for **P1 only** and returns to clean on commit. Every
other phase runs at firewall-clean.

## Findings — three from orientation, two more from *running* the baseline

⛩ **F-GL-1 · `RESERVED_KEYS` has no consumer.** `reserved.py:21` is referenced **nowhere** in `src/`,
`tests/`, or `what/production/`. Option D item 1 appends two names to it, so the ratified change is
correct *and inert*. The evidence that this is a defect and not a style preference is a second absence
nobody noticed: **`interaction`** — shipped and validated at **v2.2.0** — is in neither `RESERVED_KEYS`
nor the schema's `$defs.reserved.properties`. ⇒ ***a specification with no consumer is
indistinguishable from no specification*** (the pin-field ruling's generalisation, found this time
inside the firewall). **Put to the operator at the P1 exit gate; not taken under the signature.**

⛩ **F-GL-2 · the firewall gate could not see the one operation a firewall touch necessarily performs.**
`gate_manifest.py` ran `git diff --stat` — **unstaged only**. Proved by derivation across all three
breach classes, old predicate vs new:

| Breach class | old `git diff --stat` | new `git status --porcelain` |
|---|---|---|
| unstaged edit | `2` — but those are *diffstat rows*, never a path count | `1` path ` M` ✅ |
| **staged edit** | **`0` — MISSED** | `1` path `M ` ✅ |
| **untracked new file under `canvas_std/`** | **`0` — MISSED, permanently** | `1` path `??` ✅ |

⭐ **It had never fired because no campaign before this one ever staged a `canvas_std` change.** The
check was written at Plumbline by an author who documented the persisted-`cd` trap — *a firewall
`git diff` returning empty is indistinguishable from clean* — two lines above the call that had the
same defect in a second form. ⇒ ***a predicate that has only ever been run against a clean tree has
only ever been tested for its false case.*** And the untracked class means P1 itself, which adds
`tests/test_axes.py`, would have breached the firewall invisibly.

⛩ **F-GL-4 · the manifest printed a disagreement with itself and reported ALL GATES GREEN.** The
producers aggregate row's expected cell was the **string literal `'267/7 pkg'`**, printed beside a
derived actual of **272** — stale since Plumbline P1 bumped `diagram_generator` 44→49 and updated
`PRODUCER_EXPECT` but not the summary line. The verdict was *correct* (the per-package gates carry it,
and all seven agreed), which is exactly why nobody looked. ⇒ ***a hand-typed total beside derived parts
is a claim nobody re-derives*** — the F-GM-1/F-PL-6 family, now found in the very file written to end
it. Now summed from `PRODUCER_EXPECT`.

✅ **F-GL-3 · backward compatibility is structural, not merely measured.** `$defs.reserved` is
`{"type": "object"}` with **no `additionalProperties: false`** (checked at the object). Two added enum
properties therefore *cannot* invalidate an existing canvas. LIP-0010's "25 of 25 keep passing" was
true by measurement; it is now known to be true by construction.

## Phases

| Phase | Objective | Exit gate |
|---|---|---|
| **P0** | Discharge the push · sign §7.7 · charter · **baseline the gate line by running it** | ✅ complete |
| **P1** | The bounded firewall touch (Option D's four files) + the two manifest fixes | full-regression-green (**not** diff-0, per `adr_007`) + the **F-GL-1 gate question answered** |
| **P2** | The `2.3.0 → 2.4.0` pin sweep across a **classified** 32-file surface | live pins moved, historical claims untouched, partition recorded |
| **P3** | De-duplicate: the two producer frozensets become `canvas_std` delegates; the false error text rewritten | producers green; no module claims to be the only enforcement |
| **P4** | Governance + consumers: LIP → Final · `lip_registry` · federation pin · consumer memos · manifest expectations **derived** | gate line green from `--markdown` |
| **P5** | Close: AAR, STATE, push | campaign `completed` |

**Phase gates are human gates.** Report a SITREP and HOLD.

## Out of scope

- Mandating either key on any canvas.
- Graduating `pattern_diagrammatic_context` — it needs a **third** vault adoption and neither Canvas
  nor aDNA.aDNA can manufacture one (Rosetta, 2026-09-11).
- H4 live-chain spend (blocked on ComfyUI's M-RD1 venue manifest, by both vaults' agreement).
- `ImagenWiring` deprecation · the memo registry · the gate-manifest upstream filing — open backlog,
  owners named.

## Log

### P0 — complete 2026-09-11

1. **Push discharged first**, so the Plumbline batch stays separable from this campaign's:
   `8` commits (re-derived with `git rev-list --count`, no `head -N`), authorship uniform,
   `gitleaks` clean on the range **and** again in the pre-push hook →
   `origin` **`22a101b..036e156`**. `@{u}..HEAD` now `0`.
2. **§7.7 signed** — `lip_0010` Ratified by / Date / Status = accepted; the block also records F-GL-1
   as the thing the signature explicitly cannot bless.
3. **Baseline gate line captured by running the manifest**, not copied: nine gates, all green, exit 0.
   That run is what produced F-GL-4 — the baseline was not ceremony.
