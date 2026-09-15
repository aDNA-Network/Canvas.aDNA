---
type: directory_index
created: 2026-02-17
updated: 2026-09-15
last_edited_by: agent_mondrian
tags: [directory_index, coordination, memo, memo_number, registry, derivability, f_dt_11, datum_p4]
---

# Coordination — Agent Protocol

> ⛩ **CORRECTED 2026-09-15 (Operation Datum P4).** Everything below the §Purpose line was
> **inherited template text last edited by `agent_init` on 2026-02-19**, and this vault's practice
> left it behind long ago. Measured before editing: **0 of 80** files use the documented
> `note_YYYYMMDD_{topic}.md` naming, and the directory is a **permanent, numbered memo archive** with
> an `inbox/`, not a scratchpad of expiring notes.
>
> ⛔ **One drifted instruction was actively dangerous and is struck first**: §Lifecycle said *"**Delete**
> when the note is expired"* and *"**No archive** — coordination notes are ephemeral, no history
> needed."* That contradicts **Standing Order 6 (archive, never delete)** and would, followed
> literally, destroy the delivery record that this vault's `delivery_basis` / re-probe discipline rests
> on. Nothing was ever deleted — the practice was right and the document was wrong — but an agent
> reading this file for instructions would have been told to do it.
>
> ⇒ ***a protocol document nobody executes is a registry with no consumer*** — this campaign's subject,
> found in the governance file for the directory where its memos live. Recorded as **F-DT-11**.
>
> The original text is **preserved below under §Superseded template**, struck rather than deleted.

## Purpose

Correspondence between this vault and its peers, and between concurrent agents in it. Two distinct
things live here and they have different lifetimes:

| | What | Lifetime |
|---|---|---|
| **Memos** (`coord_YYYY_MM_DD_<from>_to_<to>_<subject>.md`) | inter-vault correspondence — findings, rulings, asks, errata | **permanent** (SO-6) |
| **`inbox/`** | inbound memos delivered *to* us, awaiting consumption | permanent once consumed; see `inbox/README.md` |

## Memo numbers — a convention with no registry, deliberately

⛩ **Ruled at Operation Datum P4 (2026-09-15): a reasoned decline.** The registry proposed in
[`how/backlog/idea_memo_number_registry.md`](../../how/backlog/idea_memo_number_registry.md) was
**not built**, and the reason belongs here rather than only in the backlog, because *the campaign's
own definition of done is that a registry's state is written on the line.*

**The state, stated:** memo numbers have **no consumer and no discovery pass**. The number line is
reconstructed by derivation at each allocation. That is deliberate, and the reasons are:

1. **#12 is a class, not a file** — the Blueprint P3 re-pin wave: 9 copies to 8 recipients under one
   number. Any check demanding one file per number goes red on a real, correct historical act.
2. **Errata are unnumbered by design** — they attach to their parent by `thread:` (an erratum to #9 is
   not memo #20). A check demanding a number on every outbound memo would force numbers onto
   artifacts whose whole identity is *"this is a correction to #9."*

⇒ A check needing two carve-outs exactly where its population is irregular is the **F-DT-7** shape —
*a registry that looks watched is better hidden than one that visibly is not.*

⭐ **And the convention is self-correcting, which is the measurement that settled it.** Re-derived
2026-09-15 across two independent populations:

| Population | Result |
|---|---|
| `memo_number:` frontmatter | **7** files — 10, 11, **15, 16, 17, 18, 19** |
| prose references across `who/`, `how/`, `STATE.md` | max **19** |
| **agree?** | ✅ both at **19** — next allocation is **#20** |

**The gap is entirely historical.** From **#15 onward the frontmatter population is complete and
contiguous** (it was 4 files when the idea was filed on 2026-09-11; it is 7 now). A registry would be
enforcing something the practice already does.

### How to allocate the next number

⛔ **Do not grep one population and take the max.** That is the operation that fails silently when a
number is recorded somewhere the grep does not reach — which is how #9 (number only in a `status:`
comment) and #13 (only in its `title:` and `H1`) would be missed.

**Cross-check two independent populations and require them to agree:**

```sh
grep -rh "^memo_number:" who/coordination/ | sort -t' ' -k2 -n | tail -1
grep -rhoE "memo #[0-9]+" who/ how/ STATE.md | grep -oE "[0-9]+" | sort -n | tail -1
```

If they disagree, that **is the finding** — investigate it; do not take the larger and move on.
**Set `memo_number:` in the frontmatter of anything you allocate**, so the cheap population stays the
reliable one.

## ⚠ `ack_required` states the sender's expectation — it cannot state whether a question was asked

Rosetta measured this about us on 2026-09-11 and it is a finding **about our outbound default**.
Their reply-owed sweep filtered on `ack_required: true`; every Canvas memo sets it `false` —
correctly by our lights, because we were not demanding a courtesy. So their sweep reported *nothing
owed to Canvas*, **four times**, while memo #13 sat in their tree saying *"still awaits your ruling."*

⇒ If a memo **asks a question**, say so in a way a machine sweep can see. Our default is now known to
be invisible to at least one peer's.

## Delivery discipline

- **Re-probe at act time.** A delivery GO is granted on a stated basis; if the basis has changed when
  you go to act (a peer acquired a live lease, a drop-box vanished), **hold and report** — do not
  execute the GO on facts that no longer hold. Memo #19 was held on exactly this and delivered two
  days later at a re-probe that found the lease released.
- ⭐ **A staged memo is not a refused one.** Both refusal conditions this vault has met — a live peer
  lease, no drop-box — are **transient**. Re-probe; do not escalate, and do not read
  silence-by-staging as silence-by-choice.
- **Correct `delivery_basis` before sending** if the basis changed while staged. Memo #15 shipped with
  a stale one; a memo whose header contradicts the act that delivered it is a record that misleads.
- **Peer trees are read-only.** Leave delivered memos untracked in the peer's tree; never commit into
  another vault (workspace Rule 10 — cross-graph writes are staged memos, never silent writes).

## Load/Skip Decision

**Load this directory when**:
- Session startup — scanning for inbound memos (startup checklist step 5). ⚠ Scan **both** the flat
  directory *and* `inbox/`: memos have been delivered to the flat path before.
- Allocating a memo number, or sending/receiving any inter-vault correspondence.

**Skip when**: already scanned at startup and mid-session on unrelated work.

**Token cost**: ~900 tokens (this AGENTS.md).

---

## Superseded template

> ⛔ **Preserved, not deleted — and not to be followed.** This is the `agent_init` text of 2026-02-19,
> kept because the history is the argument: it is the measured example of a governance document that
> described a practice nobody performed, in the directory whose memos record this vault's findings
> about exactly that failure. **The `Delete` / `No archive` lifecycle is the dangerous part.**

### ~~Format~~ — *superseded; **0 of 80** files use this naming*

Files should be named: `note_YYYYMMDD_{topic}.md`

```yaml
---
created: YYYY-MM-DD
author: agent_{username}
urgency: info | warning | blocking
expires: YYYY-MM-DD
---

# {Topic}

Brief description of what other agents need to know.
```

### ~~Urgency Levels~~ — *superseded; no memo has ever carried an `urgency:` key*

| Level | Meaning | Agent Action |
|-------|---------|--------------|
| `info` | Advisory only | Note and proceed normally |
| `warning` | Proceed with caution | Check the flagged area before modifying |
| `blocking` | Stop and consult user | Do not proceed with affected work |

### ⛔ ~~Lifecycle~~ — *superseded, and steps 3–4 contradict Standing Order 6*

1. **Create** when you discover something cross-cutting (e.g., "shared config is mid-edit", "sync issue detected")
2. **Read** on session start (part of the Agent Startup Checklist in CLAUDE.md)
3. ⛔ ~~**Delete** when the note is expired or no longer relevant~~ — **never do this.** Memos are permanent.
4. ⛔ ~~**No archive** — coordination notes are ephemeral, no history needed~~ — **the opposite is true.**
   The delivery record is what the re-probe and `delivery_basis` discipline rest on.

### ~~Rules~~ — *superseded*

- Keep notes short (1-2 paragraphs)
- Set `expires` date — notes without expiry clutter the directory
- `blocking` urgency means agents should pause and consult the user
- `warning` means proceed with caution
- `info` is advisory only
