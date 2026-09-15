---
type: session
session_id: session_stanley_20260915_datum_p3
created: 2026-09-15
updated: 2026-09-15
status: completed
tier: 2
persona: mondrian
operator: stanley
campaign: campaign_canvas_datum
phase: "P3 (closed)"
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

### P3.2/P3.3 — firewall touch #5, both legs

All **26** constants now carry a PEP 258 attribute docstring declaring `SCHEMA-TWIN` (12, each citing
its JSON pointer) or `VALIDATOR-ONLY` (14, each stating *why* there is no twin). Checked against the
derivation by both legs — package (`test_registry_consistency.py`, +5) and vault
(`registry_census.py`, 3 new named fault classes → gate #10).

⛩ **F-DT-3 ruled and implemented**: two vocabularies that coincide — linked, not merged.
⛩ **F-DT-9**: three now-false *"`RESERVED_KEYS` has no consumer"* claims corrected where written.
The `test_axes.py` one **had named its own expiry condition**, the condition was met, and it still
needed correcting by hand — *nothing re-reads a comment*.

⚠ **A pre-existing `ruff` F541 in `registry_census.py`** (an `f`-string with no placeholders, line
546 — untouched by this phase) was fixed in passing and is recorded rather than folded in silently.

### P3.4 — verification

Five failure classes, each **derived rather than read**, each failing precisely its own check:
D8 no docstring · **D9 the F-DT-7 case** · D10 a twin appears · D11 F-DT-3's link by name · D12 a
bare label. All restored.

`canvas_std` **151 → 156/10** — derived by running the suite at HEAD with the working tree stashed
(151/10) and again restored (156/10); the diff adds exactly **5** `def test_` functions; skips
unchanged at 10. Arithmetic closed before the number was written into the manifest.

## SITREP

**Completed** — Operation Datum **P3**, at a human gate.
- F-DT-7 measured by perturbation (both directions) and closed; F-DT-6 retro-numbered into the
  campaign record; F-DT-8 recorded and deliberately **not** fixed here; F-DT-9 corrected at source.
- Firewall touch **#5** (`reserved.py` · `schema.py` · `test_registry_consistency.py` ·
  `test_axes.py` · `CHANGELOG.md`), back to **diff 0** on commit.
- `idea_reserved_keys_has_no_consumer` **CLOSED**, body preserved unedited and annotated.
- Artifact: `artifacts/p3_reason_on_the_line.md`. Campaign §P3 result + §Follow-up written.
- STATE.md updated, including the stale §Current Phase row — **correction recorded, not silently
  applied.**

**Gate line** (pasted from `python3 how/gates/gate_manifest.py --markdown`, exit 0, never retyped):

`canvas_std` **156/10** · certification **12/12** · `canvas_core` **1039/4** · `canvas_presentation` **57/2** · `canvas_context` **58** · producers **275 across 7 packages** · `comic_render` **154/2** · firewall diff **0** · registry census **11/11** keys · dual-channel freshness **2/2**

⚠ `canvas_core` reads **1039/4** where the pin is `(1040, 3)`: Obsidian is not open on this vault, so
one test skips. `Gate.env_skips` (F-DT-5) permits the split to move while requiring the **total** to
match exactly — the gate is `ok` because 1043 = 1043, not because the pin was loosened.

**In progress** — none. P3 is complete and gated.

**Next up** — **P4**: `idea_memo_number_registry` — a registry with a derivation check, **or a
reasoned decline**. Phase gates are human gates; P4 is not opened by this session.

**Blockers** — none.
- ⛔ **Operator items owed**, unchanged by this phase: the §7.7 signatures (`adr_010` · `adr_011` ·
  `adr_012`) · the mermaid trust grant · **a push GO** — now **9 unpushed commits** (6 inherited + 3
  from this session), counted with `git rev-list --count @{u}..HEAD`.
  ⚠ **This line read "8 unpushed (6 + 2)" when first written, and it was wrong in the addend**: this
  session made **three** commits, not two. Caught on the post-commit re-verify and corrected here
  rather than silently. ⇒ It is the 2026-09-10 slip **exactly** — *"I committed Blueprint's own defect
  in the first act after its close: reported 20 unpushed where the real figure was 22"* — recurring
  five days later in a session whose entire subject is hand-maintained numbers that nothing re-derives.
  ***The habit does not transfer by having written the finding down***, which is the argument this
  campaign makes about registries, made here about me.
- ⓘ **Raised, not absorbed** (campaign §Follow-up): nothing in the package validates a real document
  against the JSON Schema. F-DT-7's root condition is now *guarded* but not *removed*, and closing it
  touches the certification corpus — larger than P3's scope.
- ⓘ **Upstream candidate still unfiled** per `skill_upstream_contribution` — mention at a pause, file
  only on operator approval.

**Files touched** — `what/code/canvas_std/{src/canvas_std/reserved.py, src/canvas_std/schema.py,
tests/test_registry_consistency.py, tests/test_axes.py, CHANGELOG.md}` ·
`how/gates/{registry_census.py, gate_manifest.py}` · `how/backlog/idea_reserved_keys_has_no_consumer.md` ·
`how/campaigns/campaign_canvas_datum/{campaign_canvas_datum.md, artifacts/p3_reason_on_the_line.md}` ·
`STATE.md` · this file · `how/sessions/history/2026-09/session_stanley_20260913_datum_p0.md` (closed).

## Next Session Prompt

Operation Datum P3 closed 2026-09-15 (`Canvas.aDNA`, persona Mondrian); **P4 is next and is a human
gate.** P4 is `how/backlog/idea_memo_number_registry.md` — build the memo-number registry *with a
derivation check*, **or decline it with a stated reason**; the charter treats a reasoned decline as a
valid outcome, and P3's F-DT-8 (the stale session file) is a nearby candidate the campaign
deliberately declined to widen into, so read both before choosing. Start with the cold-start ritual
(`git status --porcelain -uall`, flat `who/coordination/` **and** `who/coordination/inbox/`,
`how/sessions/active/`, `git rev-list --count @{u}..HEAD`) and then run
`python3 how/gates/gate_manifest.py --markdown` **rather than trusting STATE's line** — Datum has now
produced a finding inside its own instruments at every single phase. Note two live operator items a
session cannot self-serve: **9 unpushed commits await a batch push GO** (verify with `git rev-list --count @{u}..HEAD`, never `head -N`), and the §7.7 signatures
(`adr_010` · `adr_011` · `adr_012`) plus the mermaid trust grant remain outstanding. The standing
caution from P3: `canvas_core` measures 1039/4 with Obsidian closed and 1040/3 with it open — that is
`Gate.env_skips` working, not a regression.
