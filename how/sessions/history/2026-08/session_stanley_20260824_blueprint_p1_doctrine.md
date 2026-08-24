---
type: session
session_id: session_stanley_20260824_blueprint_p1_doctrine
created: 2026-08-24
updated: 2026-08-24
status: completed
tier: 1
executor_tier: fable
operator: stanley
persona: mondrian
last_edited_by: agent_mondrian
campaign: campaign_canvas_blueprint
mission: mission_b1_doctrine (P1 open)
plan_ref: ~/.claude/plans/please-read-the-claude-md-curious-wilkinson.md
tags: [blueprint, p1, doctrine, diagrammatic_context, legacy_interop, lip_assessment, census]
---

# Session: Blueprint P1 — doctrine (Canvas-owned half)

**Trigger**: operator opened the session at the P1 gate ("continue the campaign"). Gate decision
taken at plan approval: **open P1, ship the three Canvas-owned items, leave the Rosetta-dependent
item honestly open.** Push GO granted for the batch at close.

## SITREP

**Completed**

1. **P1 opened; `mission_b1_doctrine` created and closed complete-with-open-item.** Before touching
   the doctrine, the corpus it rests on was re-measured — and the P0 draft, already delivered to
   Rosetta for a ruling, turned out to be **right about the count and wrong about the cause**.
   196 real files / 46 live vaults (+74 archived) ✅; but **196/196 carry** a `_reserved` block with
   `{authority: "view", source_yaml, last_sync, sync_hash}`, written to **`metadata._reserved`**
   rather than the canonical `metadata.frontmatter._reserved`. Green `[OK]` at `core`; `[FAIL]` at
   `adna_native` on **A-2 alone**. The legacy has *been* the `view` authority row since 2026-02 —
   one level too high, present and unread (**F-B1-1**).
2. **Erratum → Rosetta, twice.** v1 corrected the diagnosis but described the fix as "a relocation
   plus two identity fields." Running it disproved that within the hour: **A-6 requires a nested
   `sync` object with a 16-hex hash from `compute_sync_hash()`**, so `sha256:none` is not
   transliterable and `source_yaml` → `sync.source_name` is a rename. **v2** carries the *executed*
   recipe — scratch copies of all four templates migrated **4/4 → `adna_native [OK]`** with
   degradation `{D-1, D-2, D-3}` intact and zero node/edge change. Delivered uncommitted in their
   tree (their inbox holds their own in-flight untracked memo — hygiene confirmed live).
3. **`adr_011`** (`proposed`, §7.7 pending) — the legacy **is** the Standard's `view` row: named,
   bounded, not deprecated; canonical placement normative; migration **offered, not performed**
   (one `.adna` edit + a release reaches all 46, the files being byte-identical). Three alternatives
   recorded and rejected, including teaching `canvas_std` a fallback path.
4. **LIP-0010 assessment** — the charter's "no schema change" default **held, but by evidence
   rather than assertion**: `authority` is normative in the proposed doctrine and **`canvas_std`
   does not know the key** (0 of 21 in-vault `adna_native` canvases carry it; `authority: "veiw"`
   passes silently — **F-B1-2**). Option B (optional validated enum, additive, v2.4.0) recommended
   and **deferred** — doctrine settles before the machine enforces it, since the pattern is still
   unruled. Requiring it (Option C) would break 21/21. Registry row added.
5. **b1.4** — the campaign's own standing order cited `--level adna-native`, which the CLI rejects.
   Fixed in both campaign files.

**Gate evidence**: `canvas_std` **115 passed / 10 skipped** · certification **11/11** ·
`git diff --stat -- what/code/canvas_std/` **empty** · `what/lattices/examples/` **untouched**
(migration ran on scratch copies only).

**Open** — `b1.5`: finalize the pattern with Rosetta. Memo #9 + erratum v2 both delivered,
unanswered, verified at source. **P2 does not depend on it**, but the pattern is not doctrine until
they rule, and LIP-0010's conversion trigger is their ratification.

**Next up** — **P2 gate (HOLD)**: `skill_canvas_context_diagram` · Canvas's own dual-channel
architecture canvases (it ships zero today) · conversion offers #10 Operations / #11 ScienceStanley ·
normalize-on-collect carried from F-HR-1.

**Blockers** — none. `#needs-human`: `adr_010` §7.7 · **`adr_011` §7.7** · D3 registrar ack.

**Files touched** — new: `mission_b1_doctrine.md` · `adr_011_…md` ·
`lip_0010_assessment_diagrammatic_context.md` · `coord_2026_08_24_…census_erratum.md` (+ delivery
copy in `aDNA.aDNA`, uncommitted). Modified: `draft_pattern_diagrammatic_context.md` ·
`campaign_canvas_blueprint.md` · campaign `CLAUDE.md` · `lip_registry.md` · `STATE.md`.

## Next Session Prompt

Canvas.aDNA (Mondrian), Operation Blueprint. P0 and P1 are closed; **P2 (authoring rail + dogfood)
is the next gate and is HOLDing for the operator**. P2 builds
`how/skills/skill_canvas_context_diagram.md` — the rail for authoring a conformant context canvas
(conformance = `canvas-std validate --level adna_native`, note the **underscore**, plus the
Amendment-1 agent-confirmed render; topology doctrine `context_canvas_topology_graphs.md` v1.1
applies) — then dogfoods it by authoring Canvas's **own** architecture canvases dual-channel, since
Canvas currently ships none. It also sends conversion-offer memos #10 (Operations, 5 standard-blind
C08 canvases) and #11 (ScienceStanley, 29 bare files), each with the work done for them. Carry
**normalize-on-collect** from F-HR-1: an Obsidian re-save silently dropped explicit `toEnd` keys and
un-conformed a canvas, so the rail should re-normalize rather than assume. Read
`how/campaigns/campaign_canvas_blueprint/{CLAUDE.md,campaign_canvas_blueprint.md}` and
`missions/mission_b1_doctrine.md` (its AAR carries F-B1-1/F-B1-2) first. **Still open across the
gate:** Rosetta has not ruled on `pattern_diagrammatic_context` (memo #9 + erratum v2, both
delivered and verified at source) — `b1.5` stays open, and LIP-0010 converts from assessment to
Standard proposal only if they ratify with `authority` still normative. Firewall standing order
holds: `git diff --stat -- what/code/canvas_std/` must stay empty. Operator signatures pending on
`adr_010` and `adr_011` §7.7.
