---
type: artifact
artifact_id: p1_armor_dogfood
campaign: campaign_canvas_vernier
phase: P1
title: "The Armor dogfood — mostly a pass, and the failures are ours"
created: 2026-09-17
updated: 2026-09-17
status: complete
last_edited_by: agent_mondrian
subject_vault: Armor.aDNA
access: read-only
tags: [artifact, vernier, armor, bastide, dogfood, sync_hash, a8, provenance, freshness, v1, v2, v3]
---

# P1 — the Armor dogfood

Every figure below was **re-derived at execution on 2026-09-17**, not carried from the charter or the
plan. ⛔ **Read-only into `Armor.aDNA` throughout** — no writes, no commits, nothing staged in their
tree. *(This campaign exists because a number nobody re-derived meant two things at once; carrying the
plan's figures into its own artifact would have been the same mistake in the same file.)*

**Population:** 7 canvases at `Armor.aDNA/what/canvas/`, `campaign_terminal_bastide`, 19 prose context
documents, 9 of which carry a `## Canvas twin` footer.

---

## ⭐ What Armor got right — first, because it is the larger part of the result

| Measured | Result |
|---|---|
| `_reserved` at the **canonical** `metadata.frontmatter._reserved` | **7 / 7** ✅ — the thing **194 fleet canvases still get wrong** (ADR-011), got right first time by a vault reading the spec cold |
| Carries **both** A-8 axes (`authority` + `production`) | **7 / 7** ✅ — first external vault to satisfy v2.4.0's asymmetric co-requirement |
| Values | `authority: "view"` · `production: "generated"` — correct for a derived view |
| Validates at its **declared** level (`extended`) | **7 / 7 `[OK]`** ✅ |
| Source-hash freshness, by **their own** mechanism | **7 / 7 FRESH** ✅ — and verified **from outside their vault**, with no access to their generator |

⭐ **And they are ONE FIELD from full aDNA-Native.** Hypothesis tested rather than assumed: change
**only** `conformance_level: "extended"` → `"adna_native"` in memory, leave everything else untouched
(including `adna_version: 2.0.0`), and **all 7 validate `adna_native [OK]`**. Their sole native failure
is A-2, the declaration itself.

⚠ **Their `extended` is deliberate, not a shortfall.** Their README states the unblock: *"until the
panel/link kinds are validated against `spec_panel_link_semantics.md` (Phase D)."* That is the *state
the reason on the line* discipline, practised by a vault nobody told to practise it. ⇒ They are holding
themselves **below a tier they already meet**, on a conservative reading of their own readiness.

---

## ⛩ V-1 · `sync.sync_hash` has two incompatible meanings, and both validate

| Canvas | declared `sync_hash` | `sha256(source)[:16]` | match | `compute_sync_hash()` (topology) | match |
|---|---|---|---|---|---|
| `bastide_campaign_map` | `4c08b62584e24738` | `4c08b62584e24738` | ✅ | `4eb3bd7a935c5906` | ❌ |
| `bastide_data_flows` | `220298a17b9d680e` | `220298a17b9d680e` | ✅ | `c8eb617d913d7f98` | ❌ |
| `bastide_ecosystem_seams` | `73e9612ee8cfd89c` | `73e9612ee8cfd89c` | ✅ | `5c7a5fdf7a242361` | ❌ |
| `bastide_node_topology` | `ae2a85f63ec6a9b3` | `ae2a85f63ec6a9b3` | ✅ | `7898d258503b7bb1` | ❌ |
| `bastide_port_map` | `220298a17b9d680e` | `220298a17b9d680e` | ✅ | `bb308ee8101d6f8f` | ❌ |
| `bastide_session_lifecycle` | `15cbf48881b45039` | `15cbf48881b45039` | ✅ | `97b0c73ecdcce76c` | ❌ |
| `bastide_system_composition` | `220298a17b9d680e` | `220298a17b9d680e` | ✅ | `d94093186bb92591` | ❌ |

**7 / 7 source match · 0 / 7 topology match.** Three canvases share `220298a17b9d680e` because they
share a source (`03_ARCHITECTURE.md`) — impossible under topology-hashing, since their node counts are
32, 25 and 34.

### Neither vault is wrong, and that is the finding

- **The spec** lists `sync: { sync_hash, source_name, source_version }` and **never says what is hashed**.
- **A-6** checks `"sync.sync_hash {!r} is not 16 hex chars"` — **shape, not semantic** — and its own
  code comment defers the rest: *"hash↔source match is checked by the round-trip layer."*
- **`compute_sync_hash()`** implements topology-hashing. It is the *only* implementation in this vault,
  so the ambiguity was invisible from inside.

> ⇒ ***A field with a validated shape and an undefined semantic will acquire two meanings, and both
> will pass.***

⚠ **Armor's reading is arguably the more useful one for a `view` canvas.** The question a derived view
needs answered is *"has my source moved?"* — a source hash answers it; a topology hash answers *"has
this canvas been edited?"*, which for a `generated` artifact should never happen anyway.

⛔ **The field has already shipped in both meanings.** Narrowing it to either one breaks a live
consumer. Any ruling must price that migration rather than assume it away.

## V-2 · A-8 is gated behind aDNA-Native, so a correct axis pair can be inert

At `extended`, `validate()` never reaches A-8. Armor's carefully-correct pair is therefore **not
validated** — `authority: "veiw"` would pass unnoticed at their declared tier.

⚠ The axis question — *who owns the meaning · how is it made* — is a property of **any derived
canvas**, not of the aDNA-Native feature set. The keys sit in that tier for reasons that predate the
axes (LIP-0010 added them to an existing `_reserved` block; the tier was not revisited).

## V-3 · They invented `generator` — the word LIP-0010 removed

All 7 carry, inside `_reserved`:

```
generator: "what/canvas/build_canvases.py"
title:     "<per-canvas>"
```

Both are **undeclared** in `RESERVED_KEYS` (11 keys at v2.4.0). ✅ **Legal and correctly handled** —
§7.3 requires unknown `_reserved` keys be preserved; they are advisory, never a rejection.

⭐ **`generator` is exactly the value LIP-0010 struck from the `authority` axis**, for conflating *who
owns the meaning* with *how it is made*. Armor did **not** reinstate it as an authority value — they
reinvented it as a **provenance key**, which is the very distinction LIP-0010 was drawing. ⇒ **An
independent consumer, reasoning from the spec alone, arrived at the Standard's own conclusion and then
needed a carrier the Standard does not offer.**

## ⭐ The finding that runs upstream — two freshness mechanisms, neither subsuming the other

| | catches | misses | cost |
|---|---|---|---|
| **source hash** (Armor) | the input moved | ⛔ **generator drift** — *exactly F-PL-6's cause*, where Canvas's own dual-channel pair went stale because the **layout engine** changed and the sources did not | ~nothing; **third-party verifiable** |
| **rebuild-compare** (gate #9) | the output would differ | nothing | a full rebuild; needs the generator present and reproducible |

⚠ **The asymmetry matters.** A prose typo makes the source hash report **stale when the canvas is
fine** (false positive — annoying). Generator drift makes it report **fresh when the canvas is stale**
(false negative — the F-PL-6 failure, which cost this vault five all-green gate lines).

**Ruled at the plan gate: adopt both** — source hash as a cheap pre-filter, rebuild-compare as the
authority, with each mechanism's blind spot published on the face of the output.

## Two things that are not ours, reported with owners named

| | |
|---|---|
| ⚠ **`Armor.aDNA` has no git repository** | 7 canvases + 19 context documents + a staged charter, with **no history, no rollback, no provenance**. `test -d Armor.aDNA/.git` → absent. ⛔ Not ours to create. Owner: the vault, and the node (Hestia). |
| ⚠ **Absent from the workspace router** | `Armor` does not appear in `~/aDNA/CLAUDE.md` §Project Discovery, so a cold-start agent will not find it. ⛔ Not ours to edit (Standing Rule 7 — router rows carry routing identity, and the router is not Canvas's file). |

## Reproduce

```bash
# from Canvas.aDNA, read-only into Armor
python3 - <<'EOF'
import json, glob, hashlib
from pathlib import Path
import canvas_std
from canvas_std.conformance import ConformanceLevel
from canvas_std.roundtrip import compute_sync_hash
ARM = Path.home()/"aDNA/Armor.aDNA"
for f in sorted(glob.glob(str(ARM/"what/canvas/*.canvas"))):
    d = json.loads(Path(f).read_text()); s = d["metadata"]["frontmatter"]["_reserved"]["sync"]
    live = hashlib.sha256((ARM/s["source_name"]).read_bytes()).hexdigest()[:16]
    print(Path(f).name, s["sync_hash"] == live, compute_sync_hash(d) == s["sync_hash"])
EOF
```

⇒ **Expected: `True False` on all seven.** That one line is the whole of V-1.
