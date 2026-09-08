---
type: artifact
artifact_id: p3_federation_census_20260908
campaign: campaign_canvas_blueprint
mission: mission_b3_repin_wave
phase: P3
title: "The P3 federation census — measured, not read"
created: 2026-09-08
updated: 2026-09-08
last_edited_by: agent_mondrian
status: active
tags: [census, federation, wrappers, conformance, c4, c2, c3, f_hr_1, p3, measured]
---

# P3 federation census — 2026-09-08

> **Every figure below was re-derived from the objects on this node.** Nothing is carried from
> `federation_index.md` (which this census corrects in two directions) or from the campaign charter
> (whose P3 row is wrong in three places). Where a number differs from a published one, both are shown.
>
> **Method note (carried item 6):** each population states *how it was bounded*. Out-of-scope sets are
> **named**, never quietly dropped. All peer vaults were read **read-only**; nothing was written anywhere
> outside `Canvas.aDNA`.

---

## 1. Population definitions — stated before the numbers

| Population | Bound | Count |
|---|---|---|
| **P1 · Wrapper-carrying consumers** | a directory matching `canvas*` under `<vault>/how/federation/` on a **real** (non-symlink) vault dir | **18 wrappers / 15 vaults** |
| **P2 · Authored canvas emitters** | `*.canvas` anywhere in a real vault, **excluding** `_archive/`, `.git/`, `Archive.aDNA/`, and the template set | **151 files / 19 vaults** |
| *(excluded, named)* **template-inherited** | the 4-file set `{hello_world, template_pipeline, template_architecture, template_agent_graph}.canvas` at `what/lattices/examples/` | **200 files / 47 vaults** |
| **P3 · Conformance corpus** | P2 **minus `Canvas.aDNA`'s own 45** — i.e. what a peer vault actually holds | **106 files / 18 vaults** |

**Alias dedupe** — six root entries are symlinks and are counted **once**, at their target:
`aDNANetwork→Network` · `SiteForge→Astro` · `Websites→WebForge` · `Cmux→Terminal` ·
`VideoForge`/`VideosOld`→`Archive.aDNA/VideosOld.aDNA` (archived, excluded). `LatticeNetwork.aDNA`
does not exist.

⚠ **The template set moved since P1 measured it**: P1 recorded **196 / 46** on 2026-08-24; today it is
**200 / 47**. Nothing regressed — every fork inherits four, so this population grows with the fleet. It is
governed by `adr_011` and Rosetta's migration offer, **not** by any per-vault wrapper ask, which is why it
is partitioned out here rather than counted as drift.

---

## 2. Population 1 — the wrappers (15 vaults, 18 wrappers)

| Vault | Wrapper | `wrapper_for` | Pin (as written) | Target | Verdict |
|---|---|---|---|---|---|
| **Emacs** | `canvas/` | Canvas.aDNA | `version: 2.3.0` | `adna_native` | ✅ current — the reference wrapper |
| **Oration** | `canvas/` | Canvas.aDNA | `version: 2.3.0` | `extended` | ✅ current — **adopted 2026-08-04** (index says NONE; **F-P3-2**) |
| **WGS** | `canvas/` | Canvas.aDNA | `version: 2.2.0` | `adna_native` | 🟡 one minor behind — **absent from the index entirely** (**F-P3-1**) |
| **Network** | `canvas/` | *(unset)* | `standard_version: 2.2.0` | `adna_native` | 🟡 one minor behind |
| **Obsidian** | `canvasforge/` | Canvas.aDNA ✅ | `substrate_pin: "… v2.0.0"` | — | 🟠 **three minors behind**; dir-name ruling owed (**F-P3-9**) |
| **Astro** | `canvasforge/` | **CanvasForge.aDNA** | `version: 1.1.0` | — | 🔴 stale identity + stale pin + dir-name + 3 dead paths |
| **WebForge** | `canvas/` | Canvas.aDNA ✅ | `version: 1.1.0` | — | 🔴 stale pin + 3 dead paths |
| **ZenZachary** | `canvas/`+`canvas_comic/`+`canvas_deck/` | **CanvasForge.aDNA** ×3 | `substrate_pin: "CanvasForge.aDNA v1.2"` | — | 🔴 stale identity ×3 |
| **ScienceStanley** | `canvas_deck/` · `canvas_comic/` | *(unset)* | `version: "~1.0"` | — | 🟠 stale pin; M-PL3 still Canvas-side |
| **ContextCommons** | `canvas_deck/` | *(unset)* | `version: "~1.0"` | — | 🔴 `type: governance`, titled *"PresentationForge Wrapper"*, untouched since **2026-04-30**; 2 dead paths |
| **SuperLeague** | `canvasforge/` | *(unset)* | `pinned_version: "genesis-planning"` | — | 🔴 stale body + dir-name + 2 dead paths |
| **Home** | `canvas/` | *(unset)* | `builder_version: 1.0.0` | — | 🟠 pins the **substrate library**, not the Standard |
| **GOTFN** | `canvas/` | *(unset)* | `pin: genesis` | — | 🟢 correct for its stage |
| **Bearly** | `canvas/` | *(unset)* | `pin: halftone_h5_close_20260804` | — | 🟢 deliberate named pin; consuming read-only |
| **Videos** | `canvas/` | *(unset)* | *(points at `MANIFEST.md`)* | — | 🟢 **LIVE**, instantiated 2026-09-07 at `v1.0 @ 8c1b628` |

### ⛩ F-P3-8 — the field the re-pin wave exists to re-pin has **no agreed name**

`spec_federation_contract` §2.1 specifies `version: "2.3.0"`. Measured across 15 vaults, the pin is
written **six different ways**:

| Form | Vaults |
|---|---|
| `version:` | Astro · Emacs · Oration · WebForge · ContextCommons · ScienceStanley ×2 |
| `standard_version:` | Network |
| `substrate_pin:` (prose string) | Obsidian · ZenZachary ×3 |
| `builder_version:` | Home |
| `pin:` (non-semver label) | GOTFN · Bearly |
| `pinned_version:` | SuperLeague |
| *deliberately elsewhere* (`MANIFEST.md`, the Callisto ruling) | Videos |

⇒ **This is why the index drifted, and why it drifted silently.** A wave that "re-pins consumers" cannot
be mechanised against six spellings, so every past refresh required a human to read fifteen documents and
interpret each — and a human who skips one leaves no trace. WGS was missed for that reason, not from
carelessness. *The fix is not to scold the consumers: five of the six forms are locally reasonable, and
Videos' indirection is actively better practice than §2.1's.* It is to **name the canonical field, accept
the alternatives explicitly, and make the index derivable.** Memo #13 to Rosetta carries this.

### ⛩ F-P3-9 — Obsidian keeps `canvasforge/` on a precedent that no longer exists

Obsidian's wrapper states the directory keeps its name *"per the ratified ADR-010 + the P3 mission
exit-gate + the `ZenZachary.aDNA/canvasforge/` sibling precedent."* Measured:
`find ZenZachary.aDNA -name "canvasforge*"` → **empty**. ZenZachary's wrappers are at
`how/federation/{canvas,canvas_comic,canvas_deck}/`. **The cited sibling renamed and relocated;
the precedent evaporated and the citation kept standing.** Obsidian's own P3 closed 2026-06-23, and their
note already flags a rename as a *"post-P3 follow-up"* — so the condition they set is met.
⇒ Not Canvas's ruling to take (Rule 10). It goes to Seshat as an ask **with the dead precedent named**,
because the strongest argument for keeping the name is the one that turns out to be false.

### Dead path references — 11 of 62, measured

| Dead target | Cited by | Why |
|---|---|---|
| `~/aDNA/CanvasForge.aDNA/…` (4 refs) | Astro ×2 · ContextCommons ×2 · WebForge ×2 | vault archived at PT pt09 (2026-06-17) |
| `~/aDNA/node.aDNA/…` (2 refs) | Astro · WebForge | **`node.aDNA` has never existed under that name** — renamed to `Home.aDNA` 2026-06-11 |
| `~/aDNA/lattice-labs/what/lattices/…` (2 refs) | SuperLeague | the *shim resolves*, the **file** moved — `canvas_yaml_interop.md` now lives per-vault |
| `~/aDNA/ZenZachary.aDNA/canvasforge/CLAUDE.md` | Obsidian | F-P3-9 |

⚠ Note the `lattice-labs` row: **the symlink resolves, so a shim-health check passes, and the reference
is still dead** one level down. A path check that stops at the shim reports green.

---

## 3. Population 2 — authored emitters **with no wrapper** (never previously enumerated)

Opened as scope by Berthier's 2026-09-07 reply: Operations emits canvases, has **no** `how/federation/canvas/`
wrapper and no canvas check anywhere — *"the clean tree is clean by low traffic, not by construction."*
The federation index had recorded Oration as the **last** vault in this condition; F-P3-2 shows that one
closed five weeks ago, and nobody counted the rest.

**10 vaults · 49 authored canvases · zero federation seam:**

| Vault | Files | | Vault | Files |
|---|---|---|---|---|
| Regenesis | 11 | | LAVentureGraph | 4 |
| Operations | 10 | | WilhelmAI | 3 |
| LatticeProtocol | 7 | | Molecules | 2 |
| aDNALabs | 5 | | PercySleep | 2 |
| Hardware | 4 | | RareArchive | 1 |

⇒ **The federation surface was measured on the wrong axis.** Fifteen vaults hold a wrapper; ten emit
canvases without one. Being *in* the index meant "has a wrapper", and the vaults with the least
supervision were the ones the index could not see at all.

---

## 4. Population 3 — the conformance measurement (106 files, 18 peer vaults)

Run with `canvas_std 2.3.0` at `--level core`; `normalize_edges` applied **in memory only** — nothing was
written to any peer vault.

```
core [OK]  63        core [FAIL]  43        total errors  1664
```

| Class | Errors | Share | Mechanical? |
|---|---|---|---|
| **C-2** — node coordinate is a float, not an integer | 1179 | 71% | yes — round |
| **C-4** — edge missing explicit `toEnd` | **464** | 28% | yes — `normalize_edges` |
| **C-3** — *(bucket, see below)* | 21 | 1% | mixed |

### ⚠ The aggregate is dominated by one outlier — F-P2-12's lesson, again

**LAVentureGraph alone contributes 1175 of 1664 errors (71%)**, and **1161 of those sit in two files**
(`canvas_ecosystem_overview.canvas`, 876 errors / 433 nodes; `canvas_investor_network.canvas`, 285). Every
one is the same message — `C-2: node 'X' field 'X' must be an integer` — from float coordinates
(`x: -4326.427926109887`), the signature of a **programmatic layout writer** that never rounded. It is
mechanical and trivially fixable, and `normalize_edges` clears **none** of it (different class).

**Excluding that one outlier vault**, the picture is the one P2b predicted:

```
489 errors across 17 vaults  —  464 of them C-4  =  95%
```

⇒ **F-HR-1 generalises, and P2b's "40 of 41" was not a two-vault coincidence.** But the *unqualified*
fleet aggregate would have reported C-4 as a **minority** class at 28% and buried the finding. The same
trap F-P2-12 caught at P2c (an outlier by construction inflating μ/σ) fires here at fleet scale.
**State the aggregate and the outlier-excluded figure together, or state neither.**

### What the normalizer does, measured

```
normalize_edges (in memory, nothing written):   1664 → 1200 errors   [464 cleared]
files FAIL → core [OK]:                         36 of 43
```

**Nine vaults carry the C-4 class**: SuperLeague 204 · Regenesis 85 · LatticeProtocol 72 · Network 25 ·
ScienceStanley 21 · Operations 19 · Molecules 19 · WGS 15 · WilhelmAI 4.

### ⛩ C-3 is a bucket, and calling it "dangling edges" would have been wrong 20 times out of 21

`canvas_std` files four distinct edge defects under the single id `C-3`. Enumerated:

| Actual defect | Count | Where |
|---|---|---|
| `fromSide`/`toSide` value `"center"` not in the valid-side enum | **20** | SuperLeague `org_context.canvas` (one file) |
| endpoint does not resolve to a node — a **genuinely dangling edge** | **1** | Operations `c08_dispatch_package_anatomy.canvas` |

`unresolved_edges` reports **1**. The two tools do **not** disagree — one counts a bucket, the other
isolates the defect that needs judgement. ⭐ And the single edge it finds fleet-wide is **exactly** the one
P2b surfaced and Berthier ruled `DELETE` on 2026-09-07 by history walk (target `269b75cbca9331d4` never
existed as a node in any committed revision). **One genuinely unresolved edge in 106 files across 18
vaults, and it was already found, ruled, and routed to its author.**

*(I nearly reported "21 dangling edges fleet-wide, a 21× increase on P2b." That number would have been
literally derived from our own validator's output and completely false as a class claim — the same
literal-vs-class error as F-P2b-1 and F-P3-7, caught this time by asking the tools why they disagreed
instead of picking the alarming one.)*

---

## 5. What the charter said vs what is true

| Charter P3 row | Measured |
|---|---|
| "5 stale" wrappers | **9** materially stale (identity / pin ≥1 major / dead paths / wrong type), on 15 |
| "3 misnamed `canvasforge/`" | ✅ **3** — Astro · Obsidian · SuperLeague. The only figure that held. |
| "memos #12 to 6 vaults" | **9 wrapper-drift** recipients + **10 wrapper-less emitters** are a different, larger ask |
| "adopt VisualDNA lockstep-flip mechanics" | **the artifact does not exist** (F-P3-4) |
| *(unstated)* | **15th consumer** (WGS) · **G7 gap already closed** (Oration) · **10 unwrapped emitters** · **six pin spellings** |

---

## 6. Commands of record

```sh
# population 1 — wrappers on real vault dirs
for v in ~/aDNA/*.aDNA; do [ -L "$v" ] && continue; ls -d "$v"/how/federation/canvas* 2>/dev/null; done

# population 2 — authored emitters, template set partitioned out
find ~/aDNA/*.aDNA -name '*.canvas' \
  ! -path '*/_archive/*' ! -path '*/.git/*' ! -path '*/Archive.aDNA/*' \
  ! -path '*/what/lattices/examples/*'

# population 3 — conformance, read-only, normalize applied in memory only
PYTHONPATH=~/aDNA/Canvas.aDNA/what/production /opt/anaconda3/bin/python
  # canvas_std.conformance.validate_suite(doc, ConformanceLevel.CORE)
  # canvas_core.conform.normalize_edges / unresolved_edges

# dead path refs
grep -o '~/aDNA/[A-Za-z0-9_./-]*' <each wrapper CLAUDE.md>  →  test -e
```

**Peer-vault write check at census close** — stating what was actually verified, not what sounds
stronger. `find ~/aDNA -name '*.canvas' -not -path './Canvas.aDNA/*' -newermt '2026-09-08 00:00'` →
**empty**: no canvas outside this vault was modified today by anyone. `normalize_edges` output was held
in memory and never serialised outside `Canvas.aDNA`.

⚠ *Not* claimed: that every peer vault's `git status` is byte-identical to its pre-census state. That
would be unverifiable after the fact **and false** — the same sweep shows **five other vaults**
(`Fluxer`, `Codex`, `aDNALabs`, `ScienceStanley`, `operations_jake`) with files modified today by
**concurrent operator sessions unrelated to this one**. The honest claim is the narrow one: this session
read peer vaults and wrote to none. *(That the fleet is actively being written to today is also the
reason S5 re-probes each recipient's quiescence at act time rather than trusting a probe taken now.)*
