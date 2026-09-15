---
type: session
session_id: session_stanley_20260915_datum_p3
created: 2026-09-15
updated: 2026-09-15
status: active
tier: 2
persona: mondrian
operator: stanley
campaign: campaign_canvas_datum
phase: P3
executor_tier: opus
last_edited_by: agent_mondrian
tags: [session, canvas, datum, p3, registry, reason_on_the_line, schema_twin, attribute_docstring, f_dt_6, f_dt_7, f_dt_8]
---

# Session — the reason goes on the line, and the schema turns out to have no reader at all

## Intent

Operation Datum **P3**: *vocabulary-agreement sweep across every paired constant/enum; reason-on-the-line
for every unpaired one.* Two operator rulings were taken at this gate, both with their measurement in
hand: **firewall — both legs again** (markers live in the package; firewall touch **#5**) and
**F-DT-3 — two vocabularies that coincide; link, do not merge.**

## Cold-start ritual

| Check | Result |
|---|---|
| `git status --porcelain -uall` | **clean** — 0 entries |
| Flat `who/coordination/` scanned too? | ✅ yes — nothing new inbound |
| `how/sessions/active/` | ⚠ **a stale lease** — see below |
| Unpushed commits | **6**, counted with `git rev-list --count @{u}..HEAD` (no `head -N`) |
| Active campaign | Operation Datum, **P2 closed**, P3 next |
| Firewall | `canvas_std` **0 entries** under `git status --porcelain` (staged + unstaged + untracked, per F-GL-2) |
| HEAD at open | `af741fa` |

⚠ **`STATE.md` §Current Phase said *"P0 CLOSED 2026-09-13, P1 next."* P0, P1 and P2 are all committed.**
Git HEAD is truth (CLAUDE.md §Git Coordination). Corrected at this phase, recorded rather than
silently overwritten.

⚠ **A stale session lease, and it is the campaign's own subject** — see **F-DT-8**. The 09-13 session
file was still `status: active`, `phase: "Act 0 → P0"`, work log `*(appended as the session runs)*`,
two days and four commits later. Closed to `history/2026-09/` with a reconstruction derived from the
commits and an explicit note that it is a reconstruction.

## Work log

### P3.1 — the measurement, before any firewall touch

⛩ **F-DT-7 confirmed by perturbation, and the hole is much larger than the plan predicted.** The plan
expected a below-floor twin to reclassify silently. It does — and the reason that matters is the part
the plan did not anticipate:

1. **Python side gutted** (`VALID_SIDES` 4 members → 1, Jaccard 0.25): census reports
   `VALIDATOR-ONLY`, **exit 0**, gate #10 `ok`. Caught by *other* gates only because `VALID_SIDES` is
   exercised — 47 `canvas_std` failures.
2. **Schema side gutted** (`edge.fromSide` + `edge.toSide` enums, 4 values → 1 — the realistic drift
   direction, since the schema is data): census `VALIDATOR-ONLY`, **exit 0**, gate #10 `ok` — and
   **every one of the other nine gates green.** 151/10 · 12/12 · 1039/4 · 57/2 · 58 · 275/7 pkg ·
   154/2 · freshness 2/2. The only red was the **firewall**, which fires on *any* byte changing under
   `canvas_std` — it noticed a file was edited, not that the Standard's edge-side vocabulary had been
   destroyed, and it is lifted by ruling for every legitimate touch anyway.
3. **The schema is load-bearing, verified directly, not assumed**: `jsonschema` against the gutted
   schema returns `'bottom' is not one of ['top']` for an ordinary canvas. Meanwhile
   `canvas_std.validate()` accepts it, because the Python validator reads `VALID_SIDES` and never
   consults the schema. Two independent copies, one consumer each — and the schema's consumer is
   **outside this vault**.
4. **Who reads `json_schema()` in the package**: every call site reads `$defs.reserved` *only*
   (`test_axes.py`, `test_registry_consistency.py`). The single exception, `test_smoke.py:74`, asserts
   `x-standard-version` and `"node" in $defs` — structure, not values. ⇒ **the JSON Schema's eleven
   value enums are consumed by nothing in this vault.**

⇒ ***content-pairing is coverage that evaporates exactly when it is needed.*** The census reported
12 SCHEMA-TWIN pairs "all agreeing exactly", which reads as twelve guarded vocabularies; what it
actually guarantees is that *pairs which still look alike still look alike.* And it does not fail
quietly — it prints a confident false explanation: *"unrelated vocabularies reusing a generic token"*,
said of the Standard's own `fromSide` enum.

Both perturbations restored; `git status --porcelain what/code/canvas_std` **empty**; census **exit 0**.

⭐ **This is why the approved design is the right one and not merely a tidy one.** A docstring on
`VALID_SIDES` *declaring* `SCHEMA-TWIN` is a falsifiable claim: when the twin vanishes, the claim
fails. Declared-vs-derived gives the pairing the memory that content-pairing cannot have, and it needs
no name map — so the charter's ban is untouched.
