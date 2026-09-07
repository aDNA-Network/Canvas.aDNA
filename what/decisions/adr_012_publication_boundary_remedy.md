---
type: decision
adr_id: "012"
title: "Publication-boundary remedy — fix-forward, records untouched, authored content redacted at the next write"
status: proposed
created: 2026-09-04
updated: 2026-09-04
last_edited_by: agent_mondrian
signed_by:
supersedes:
superseded_by:
phase: blueprint-p2
resolves: "ADR-016 D6.1 (Git.aDNA) — each carrying graph owns its own remedy; Canvas's ruling"
relates: [adr_016_publication_boundary, f_f78, adr_013_host_role_inversion]
tags: [adr, canvas, publication_boundary, adr_016, d6_1, exposure, fix_forward, public_lane, records]
---

# ADR-012 — Publication-boundary remedy

## Status

**proposed** — authored 2026-09-04 (Blueprint P2 session); awaiting the §7.7 signature.
~~`Git.aDNA`'s ADR-016 is itself still `proposed`, so **nothing upstream binds this vault today**.~~
⛩ **Stale as of 2026-09-07, corrected before signature** (Hopper, 2026-09-06): **ADR-016 is
`accepted`** — rev 3, 2026-08-27 — and its **Amendment A1 was ratified 2026-09-06**. The conclusion
still holds but **for a different reason**: their **D5 keeps ADR-016's clauses to their own vault**,
so nothing of theirs binds Canvas either way. The citation is no longer to an unratified document,
which strengthens this ADR rather than weakening it — but the stated ground was wrong and is
replaced rather than quietly kept.
This rules Canvas's own conduct, which is Canvas's to rule (ADR-016 **D6.1**: each carrying graph
owns its own remedy).

## Context

Two peers measured this vault from outside and reported independently:

- **Ilmarinen (`Forgejo.aDNA`), 2026-08-26** — `aDNA-Network/Canvas.aDNA` is PUBLIC and two files
  carry the R&D forge node's overlay address, verified by unauthenticated fetch from
  `raw.githubusercontent.com` at `master`. Declared vantage: **"a floor, not a total."**
- **Hopper (`Git.aDNA`), 2026-08-27** — same finding, independently derived by anonymous clone;
  2 occurrences over the same 2 files. ⛩ Canvas was **absent from their census entirely** — not
  measured wrongly, never in the set, because the population censused was a roster of
  correspondents rather than an enumeration of public repos.

Both were explicit that **no rule was broken at either end**: Forgejo's vault is entitled to hold
its own infrastructure facts, and this repo is entitled to be public under its declared ADR-013
host class. Neither charged a defect. Both calibrated honestly — the address is RFC1918 on a
private overlay, not internet-routable, and knowing it grants no access. It is **reconnaissance
material in a class its owner rules unpublishable**, not a credential leak.

## The measurement taken here (own instrument, inside the tree)

> ⛩ **CORRECTED 2026-09-07, twice over, before ratification. The original table below is preserved;
> both of its rows are right and the set is incomplete.** Hopper replied
> (`coord_2026_09_06_…_you_were_right_about_the_reading_and_wrong_about_the_instrument`) and the
> reconciliation they left to us found that **our own census was itself a floor.**
>
> **(a) Their instrument was not blind — their *reading* was.** `census_public_carriers.sh` clones
> each public repo and greps **three** predicates: `a_host` (one literal), `a_addr` (literal+port),
> and **`b_class`** — the whole RFC1918 class, lifted from the deny pattern. `b_class` **is** the
> inside-enumeration this ADR claimed only we could perform. They built it, ran it, and quoted the
> confirming column. In their words: *"a missing capability is a gap; a capability you have and do
> not read is a habit."*
>
> **(b) ⛔ And we did the same thing, one level down.** This ADR's table reports **two literals**
> because we grepped for the two strings we had already found in one file. That is a
> **literal-census run from inside**, not a class-census — the exact error we charged them with. A
> true RFC1918 class enumeration at the pre-remediation baseline (`4acee98`) reads:
>
> | | occurrences | files | literals |
> |---|---|---|---|
> | what this ADR reported | 10 | 9 | **2** |
> | actual class at that commit | **13** | **8** | **4** |
>
> The two we missed are a Nebula lighthouse host and a `/24` subnet notation, **4 occurrences in
> `how/skills/skill_l1_upgrade.md`** — *live authored content*, the category §Decision 3 claims to
> have remediated in full. ⚠ **That claim was therefore overstated**: three files were remediated,
> a fourth was never seen.
>
> ⚖ **Mitigating, and not an excuse:** `skill_l1_upgrade.md` is **template-inherited** (created
> 2026-03-21, arrived at Canvas genesis 2026-06-06), so the same literals sit in every vault forked
> from the template — a fleet-wide file, not Canvas-authored. Redacting our copy fixes one vault of
> many; the durable fix is upstream, the same shape as the 196-file legacy in `adr_011`. **The
> disposition is an open operator item, not settled by this ADR.**
>
> ⇒ **The rule in the original paragraph survives and is strengthened, but it no longer flatters
> us:** *an outside measurement validates a hypothesis; only an inside measurement enumerates* — and
> **an inside measurement that greps for known strings is not an enumeration either.** Hopper has
> ratified the same clause from the other direction (their ADR-011 A8 §5: *a coverage claim states
> its population, or it is not a coverage claim*). **State the population on the face of the number:
> tip or history · class or literal · tracked or working-tree.** Neither of us did.

**Original table, preserved unaltered** — both rows measured correctly; the *set* was incomplete:

| Literal | Occurrences | Files | Peers' finding |
|---|---|---|---|
| R&D forge overlay address | **2** | `how/federation/comfyui/CLAUDE.md` · `coord_2026_08_22_vulcan_to_mondrian_…RECEIVED.md` | ✅ **confirmed exactly** |
| A **second** RFC1918 literal (a parked box, endpoint dropped 2026-08-22) | **8** | **7 files** — incl. live code, a test, a session record, a closed-campaign artifact | ❌ **never measured by either peer** |

⭐ **The finding that matters is the second row.** Two external instruments agreed precisely on the
address they were looking for, and neither *reported* a literal of the same class with **four times
the occurrence count** in the same repo. *An outside measurement can validate a hypothesis about your
tree; only an inside measurement can enumerate it.* This is why Ilmarinen's "floor, not a total"
disclaimer was the correct posture and why accepting the floor as the total would have
under-remediated by 4×. *(Struck 2026-09-07: "neither **could see**" → "neither **reported**" —
Hopper's `b_class` column could and did.)*

The second literal belongs to a **different graph's** infrastructure (the ComfyUI/node estate), so
it falls outside the boundary Forgejo declared. It is remediated here anyway: same class, larger
surface, and D2.4's logic — *a boundary declared by the graph that owns the fact binds every graph
that quotes it* — does not care which peer happened to notice.

## Decision

1. **Fix-forward. No history rewrite.** The content is pushed and may be cached, forked, or indexed
   independently; only an allowlist reaches history, and for a public repo not even that. Redaction
   after publication is theatre. ADR-016 **D4** is fix-forward by design and this vault adopts it.
   *(Ilmarinen's own corollary, applied to their memo before delivering it: redaction is the right
   remedy **before** a commit exists and the wrong one after — the distinction is whether a commit
   exists, not whether the edit feels sufficient.)*

2. **Correspondence is a record — sent as well as received.** Neither the received Vulcan memo of
   2026-08-22 nor this vault's own outbound ask of 2026-08-06 is edited. Hopper holds received
   correspondence to be a record; **this vault extends that to sent correspondence for the same
   reason** — editing what we sent falsifies the record of what we actually sent. Session history
   (`how/sessions/history/`) and closed-campaign artifacts are records on the same ground (SO-6).

3. **Authored content is ours to change, and is changed now** — three files, the second literal
   included:
   - `how/federation/comfyui/CLAUDE.md` — both literals → `<forge-overlay-addr>` /
     `<parked-box-addr>`, plus a standing note pointing to where the literals are held.
   - `what/production/canvas_core/comfyforge_adapter.py` — an explanatory comment; the literal
     carried no information the prose did not.
   - `what/production/comic_render/tests/test_backends_comfy.py` — an env-var passthrough
     assertion. Replaced with **RFC 5737 TEST-NET-2** (`198.51.100.7`), a reserved documentation
     address. The test only ever needed an arbitrary string; a reserved one is strictly better and
     is now self-documenting.

4. **The remedy binds the next write.** Overlay addresses, ports, and node inventory are resolved
   at their owner (`ComfyUI.aDNA`'s wrapper · the node's `Home.aDNA` inventory) and **never
   re-inlined into this repo**, which publishes. This is the enforceable half of the ruling; the
   redactions above are the one-time cleanup.

5. **No enforcement surface is claimed.** `gitleaks` passes these repos clean and is **correct** to
   — an IP and a port are not secrets. This vault does not invent a scanner for a fleet-wide gap
   Ilmarinen named as having no enforcement surface anywhere. The remedy here is authoring
   discipline, and it is honest about being exactly that.

## Consequences

- Two peers' measurements are **confirmed, not merely accepted**, and one is extended by 4×.
- Live code and one test change; behaviour does not. The test's assertion is unchanged in kind.
- Records remain records — the audit trail of what was sent and received is intact.
- ⚠ **The exposure is not undone.** Three of the ten occurrences (records) remain public by this
  ruling, and all ten remain in history. That is the accepted cost of fix-forward, stated rather
  than obscured.
- The second literal's owner is not this vault. Reported back to Hopper; **not** written into
  ComfyUI.aDNA or Forgejo.aDNA (Rule 10).

## Ratification (§7.7)

| Field | Value |
|-------|-------|
| Decision | Fix-forward, no history rewrite · correspondence + session history + closed artifacts are records, untouched · authored content redacted (3 files, incl. a second literal neither peer measured) · overlay addresses resolved at owner, never re-inlined · no enforcement surface claimed |
| Ratified by | _(pending)_ |
| Date | _(pending)_ |
| Status | **proposed** |
