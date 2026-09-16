---
type: federation_wrapper
wrapper_for: Astro.aDNA (ISS subsystem)
created: 2026-09-16
updated: 2026-09-16
last_edited_by: agent_mondrian
mission_origin: "Canvas.aDNA operator review package — 3 ADRs + the open queue (2026-09-16); adopted at the plan gate, Workspace Standing Rule 8"
status: active
# ⛔ NO `substrate_pin:` FIELD. Canvas removed exactly that from its `iii/` wrapper at Plumbline P3
# (2026-09-11) with a written reason: **wrappers POINT, they never RESTATE, so a pin cannot be stale
# in two places at once.** The fleet's own model — `CakeHealth.aDNA/how/federation/iss/` — carries
# `substrate_pin:` AND `federation_ref`, i.e. two pin-shaped fields for one fact. This wrapper carries
# `federation_ref` only. Deviation from the sibling exemplar is deliberate and is named here so the
# next reader does not "fix" it back.
tags: [federation, iss, consumer_wrapper, canvas, platform_pattern, adr_gate, phase_exit, neutral_persona, genesis]
---

# Canvas.aDNA `iss/` — Astro ISS Consumer Wrapper

Federation wrapper for the **Astro.aDNA Interaction Surface Site (ISS)** subsystem — agent-authored,
standalone-HTML **operator decision gates**. Canvas consumes the substrate; it never copies it.

**Why this exists.** Workspace **Standing Rule 8** names *ADR ratification* as a gate class and says
plainly: *invoke the canonical skill; do not roll a bespoke gate.* Canvas accumulated **three ADRs at
`proposed`** plus a queue of operator-owed items and had **no decision surface** — so every ruling was
happening in chat, where it leaves no artifact. Adopted 2026-09-16 at the plan gate.

⚠ **Canvas was not among the 10 wrappers in the 2026-07-02 census** (Champollion G3 D6.1). It is now
an 11th. *(Observed in passing, not acted on: `ls -d */how/federation/iss` finds more live wrappers
than that census lists. Reporting the discrepancy is not the same as re-running their census, and
re-running it is theirs, not ours.)*

**Pattern: Platform.aDNA** (standard-bearer). Gates here are **internal operator decisions** —
ratification, phase exit, disposition of an open queue — not partner-facing capture. Read
`Astro.aDNA/what/lib/iss/adaptation_guides/forge_platform_guide.md` before authoring a new gate class.

## federation_ref

```yaml
federation_ref:
  source_vault: Astro.aDNA
  source_path: ~/aDNA/Astro.aDNA
  source_skill: how/skills/skill_create_iss.md   # canonical at aDNA.aDNA/how/skills/skill_create_iss.md
  source_library: what/lib/iss/                  # generator + primitives + templates + tokens + skins
  # ⚠ NO SEMVER EXISTS FOR THIS SUBSTRATE — stated rather than invented.
  # Astro.aDNA/MANIFEST.md carries no `version:`, and generator.py carries no VERSION constant
  # (both checked at the object, 2026-09-16). A `version: "1.0.0"` here would be a number this
  # wrapper made up, which is worse than no number. The pin is therefore a COMMIT.
  version: null
  version_policy: commit_pin
  pinned_at_commit: "1c51382"    # last commit touching what/lib/iss/ — "forge/iss consumer-wrapper
                                 # pattern → how/federation/ [ADR-045]", 2026-06-30. NOT Astro HEAD
                                 # (12d772e): HEAD moves for reasons that do not touch this substrate.
  pinned_at: 2026-09-16
  templates_used:
    - adr_gate        # one ADR per gate (adr_id / adr_title / decision_statement are singular)
    - phase_exit      # multi-section composite — the shape for a multi-item operator queue
  persona: neutral
  # ⚠ `mondrian` IS NOT AN AVAILABLE PERSONA. The generator accepts exactly
  # {franklin, hermes, neutral, partner, rosetta, tokyo}. The skill says "default = consumer-vault
  # persona"; for Canvas that persona does not exist in the substrate, so `neutral` is chosen
  # DELIBERATELY rather than a borrowed voice (franklin/hermes/rosetta all belong to other vaults,
  # and a gate signed in someone else's voice misstates who is asking).
  gate_output_dir: how/gates/            # <gate_id>.html · <gate_id>.pending · <gate_id>.output.json
  receiver: null                         # ⛔ NO RECEIVER SERVES CANVAS TODAY — see below
  receiver_discovery: .gate_receiver.port   # sidecar in gate_output_dir; generator.discover_receiver_url()
  local_extensions: []
```

## ⛩ The receiver — and a probe I got wrong, recorded because the mechanism is general

**No `gate_receiver` serves Canvas's gates-root.** Measured 2026-09-16:

| Port | Actually held by | `--gates-root` |
|---|---|---|
| **8765** | **JupyterHub** (`server: uvicorn`) | — |
| 8766 | `gate_receiver.py` pid 52698 | `Terminal.aDNA/how/gates` |
| 8767 | `gate_receiver.py` pid 52085 | `Home.aDNA/how/gates` |
| 8768–8772 | **free** | — |

⚠ **I reported this receiver as "live (http 307)" before checking what answered.** It is JupyterHub's
OAuth redirect — `location: /hub/api/oauth2/authorize?client_id=service-home`. **A 307 from the wrong
service is indistinguishable from a 307 from the right one** if you only read the status code.
⇒ ***a probe that confirms *something* is listening has not confirmed *what* is listening*** — the
same shape as Datum's F-DT-7 (an instrument failing into reassurance) and of this vault's standing
rule to *state the population on the face of the number*.

⭐ **The Terminal receiver's own command line carries the proof**: it was launched `--port 8765` and is
**serving on 8766** — `gate_receiver.py` port-scans when its requested port is taken. So the declared
port in a process listing is a *request*, not an address.

**Consequence for Canvas:** a rendered gate falls back to the copy-paste tier rather than POSTing.
That is a working door, not a broken one. To get POST-back, start a receiver rooted at this vault —
it will port-scan to a free port and write the `.gate_receiver.port` sidecar that
`discover_receiver_url()` reads:

```bash
python3 ~/aDNA/Astro.aDNA/what/lib/iss/runtime/gate_receiver.py \
  --host 127.0.0.1 --gates-root ~/aDNA/Canvas.aDNA/how/gates
```

⛔ **Not started by an agent unasked** — it is a persistent local service on the operator's machine,
and the plan that authorized this wrapper rested on a receiver claim that turned out to be false.

## Render discipline

1. **Generate, never hand-author.**
   ```bash
   python3 ~/aDNA/Astro.aDNA/what/lib/iss/runtime/generator.py \
     --template adr_gate --persona neutral \
     --data <json> --output how/gates/<gate_id>.html --write-sentinel
   ```
   `--write-sentinel` performs the skill's step 6; do not `touch` the `.pending` separately.
2. **Every gate carries a `sitrep:` block** — campaign · phase · mission · `gate_purpose` ·
   `importance` · `importance_reason` · `output_destination`. A gate without one asks a question with
   no context for answering it.
3. ⛔ **Rule at the door, not in chat.** Home's 2026-09-03 ceremony rendered an ISS door and was then
   ruled in chat, leaving `provenance: operator_in_chat` and **two candidate verdict surfaces for one
   queue**. If a gate is rendered, the verdict comes back through it — otherwise render nothing and
   use `AskUserQuestion`.
4. **Verify by opening the rendered file.** ⚠ A zero exit from the generator means it wrote a file, not
   that the file renders. This vault spent an entire campaign (Datum) on instruments that report
   success without doing the thing.
5. **Gate records are records** (SO-6). `.html`, `.output.json` and the sentinel are committed and
   never deleted — a ratification's evidence is the artifact, not the memory of a conversation.

## ⚠ `how/gates/` holds two different things

`gate_manifest.py` **is** Canvas's executable *test*-gate set — ten suites, fail-on-omission. ISS
*operator decision* gates now live in the same directory. **There is no functional conflict**:
`gate_manifest.py`'s discovery walks only `what/production/` and `what/code/` for test-bearing
directories, so a `.html` here is invisible to it and cannot affect a gate line. The collision is one
of vocabulary only, and it is named in [`how/gates/AGENTS.md`](../../gates/AGENTS.md) rather than
worked around with a Canvas-only path.

## Load/Skip Decision

**Load when**: authoring an operator decision gate (ratification · phase exit · approval · structured
input), or reading a `.output.json` verdict back.
**Skip when**: the decision has ≤ 4 options and no rich context — that is `AskUserQuestion`, per the
skill's own §When to invoke.
