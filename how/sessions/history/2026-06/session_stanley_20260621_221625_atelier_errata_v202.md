---
type: session
created: 2026-06-21
updated: 2026-06-21
last_edited_by: agent_stanley
tags: [session, canvas, standard, errata, lip-queue, atelier, v2_0_2]
session_id: session_stanley_20260621_221625_atelier_errata_v202
user: stanley
started: 2026-06-21T22:16:25-0700
status: completed
completed: 2026-06-21
tier: 2
intent: "Resolve the two post-Atelier spec-gap errata (AT-1 graph extent unit · AT-2 free-form surface vocabulary) as editorial clarifications (PATCH) and cut Canvas Standard v2.0.2. AT-1=(ii) document extent optional for non-paginated/single-surface regions; AT-2=(i) document surface as open vocabulary. No validator-behavior change; +2 regression tests; disposition marked RESOLVED. Plan: ~/.claude/plans/tidy-pondering-peach.md (operator-approved)."
scope:
  - what/specs/spec_panel_link_semantics.md
  - what/specs/*.md (standard_version frontmatter bump only)
  - what/code/canvas_std/ (version string + 2 tests + doc-comments; NO validator logic)
  - what/decisions/lip_queue_disposition.md
conflict_scan: "No other active sessions (how/sessions/active/ holds only .gitkeep). git @{u}..HEAD = 0 (clean baseline)."
files_modified:
  - what/specs/spec_panel_link_semantics.md
  - what/specs/spec_adna_canvas_standard.md
  - what/specs/spec_component_model.md
  - what/specs/spec_conformance_suite.md
  - what/specs/spec_context_object.md
  - what/specs/spec_roundtrip_protocol_v2.md
  - what/specs/spec_federation_contract.md
  - what/code/canvas_std/src/canvas_std/__init__.py
  - what/code/canvas_std/src/canvas_std/conformance.py
  - what/code/canvas_std/src/canvas_std/data/adna_canvas_v2.schema.json
  - what/code/canvas_std/src/canvas_std/reserved.py
  - what/code/canvas_std/tests/test_anchors.py
  - what/code/canvas_std/tests/test_smoke.py
  - what/code/canvas_std/tests/test_conformance.py
  - what/decisions/lip_queue_disposition.md
  - STATE.md
  - MANIFEST.md
files_created:
  - how/sessions/history/2026-06/session_stanley_20260621_221625_atelier_errata_v202.md
---

## Activity Log

- 22:16 — Session opened. Operator chose "Resolve Atelier errata" (post-Atelier, no active campaign). Plan
  approved (`~/.claude/plans/tidy-pondering-peach.md`). Baseline clean: git pull up-to-date, 0 unpushed,
  canvas_std 80/10 per STATE. Beginning with the spec clarifications.
- 22:17–22:35 — Edited `spec_panel_link_semantics §4/§5.2/§6` + errata banner (AT-1 extent-optional; AT-2
  surface-open); added `reserved.py` doc-comments (no logic); added 2 regression tests to `test_anchors.py`; cut
  **v2.0.2** across the enumerated sites; marked AT-1/AT-2 RESOLVED in `lip_queue_disposition.md` (§Closeout).
- 22:36 — Verification GREEN: `canvas_std` 82/10 (+2) + ruff clean; CLI `2.0.2`; 5 producer suites 10/16/37/36/87;
  6 examples `adna_native [OK]`; firewall: `reserved.py` git-diff = comments only (validator logic untouched).
- 22:40 — Updated STATE.md (new Resume box + header) + MANIFEST.md (currency addendum). Closing session.

## SITREP

**Completed**: Resolved both post-Atelier spec-gap errata as **editorial clarifications (PATCH; `adr_003` §2 —
no LIP)** and cut **aDNA Canvas Standard v2.0.2**.
- **AT-1 (option ii)** — `extent` documented **OPTIONAL**; a non-paginated single-surface region (`pagination:
  none`, e.g. a diagram/graph) legitimately omits it. **No `graph`/`nodes` unit** (substrate-neutrality: a graph is
  sized by content, not paged).
- **AT-2 (option i)** — the `surface` subclass label (region `surface` + `surfaces[].surface`) documented as an
  **OPEN, producer-defined vocabulary**; validators MUST NOT reject unknown tokens. **No enum.**
- **No validator-behavior change** — both make explicit what the reference impl already does. Two regression tests
  lock the contract (`test_anchors.py::test_at1_extent_optional_for_nonpaginated_region` +
  `test_at2_surface_label_is_open_vocabulary`).
- **v2.0.2 cut** mirrors v2.0.1 sites (`STANDARD_VERSION`, schema `title`+`x-standard-version` with `$id` unchanged,
  `conformance.py`, `test_smoke`/`test_conformance`, 7 spec `standard_version` frontmatters + the federation
  example); fixtures' `adna_version` stays `2.0.0`.
- **Verified:** `canvas_std` **82/10** (+2) + ruff clean; CLI `2.0.2`; 5 producer suites **10/16/37/36/87**; 6
  examples `adna_native [OK]`; **firewall:** `canvas_std` validator logic untouched (`reserved.py` diff = comments).
- **Errata queue fully drained** (B1–B4 + AT-1/AT-2). Disposition §Closeout — AT-1/AT-2 records it.

**In progress**: none.

**Next up**: nothing on this track — the errata queue is drained. Open governance tail (unchanged, not Mondrian-
gated): **LIP-0008 / LIP-0009** in FA Review, earliest close **2026-06-27** (on LIP-0008 Final → cut **v2.1.0**, the
A-5 pure-metadata relaxation at `validate_panel_link`/A-5/§5.2); **PT P5** (Hestia) — `canvas_core` relocation + ~8
wrapper refederations + registry registration.

**Blockers**: none.

**Files touched**: see frontmatter (7 specs · 7 `canvas_std` files [version + 2 tests + comments] · disposition ·
STATE · MANIFEST · this session). **Committed locally; push is operator-gated** — Canvas.aDNA will be ahead of
origin by this commit; do not push without operator authorization (verify `@{u}..HEAD` all Mondrian-authored first).

**Minor finding (not actioned — out of scope)**: `MANIFEST.md` line ~23 still frames CanvasForge (Hermes) +
LiteratureForge (Thoth) as external producers — stale post-pt09 (CanvasForge absorbed; Hermes→Mondrian; LF wound
down). A doc-currency nit for a future MANIFEST pass.

## Next Session Prompt

**Canvas Standard is at v2.0.2 (2026-06-21).** The two post-Atelier spec-gap errata are resolved as editorial
clarifications: **AT-1** — `extent` is optional (a non-paginated single-surface region like a diagram omits it; no
graph unit added); **AT-2** — the `surface` subclass label is an open, producer-defined vocabulary (no enum). Both
are documentation/comment + version-label changes only — **no `canvas_std` validator logic changed** (firewall held;
`reserved.py` diff = comments); 2 regression tests added (`test_anchors.py`). Suites green: `canvas_std` 82/10, all
5 producers 10/16/37/36/87, 6 examples `[OK]`. The errata queue (B1–B4 + AT-1/AT-2) is **fully drained**; record in
`what/decisions/lip_queue_disposition.md` §Closeout — AT-1/AT-2. **No active campaign; Operation Atelier stays
closed.** Outstanding workspace items, all on existing tracks (no new campaign): **(1) push** — Canvas.aDNA is ahead
of origin by the v2.0.2 commit (Mondrian/stanley-authored), push is operator-gated; **(2)** the **LIP-0008/0009** FA
review closes **2026-06-27** — on LIP-0008 Final, cut **Standard v2.1.0** (the A-5 pure-metadata relaxation:
`canvas_std/reserved.py::validate_panel_link` surfaces check + conformance A-5 + `spec_panel_link_semantics §5.2`),
then `document_generator/consume.py` can stop minting synthetic `surface_<name>` marker nodes; **(3) PT P5**
(Hestia) — `canvas_core` relocation (ADR-004) + ~8 consumer-wrapper refederations + v2.0.x registry registration +
parity re-baseline. If the operator wants more net-new output layers (poster/letter/post), reuse
`what/context/context_canvas_producer_pattern.md` — it's a fill-in-the-blanks build.
