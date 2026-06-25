---
type: context_guide
topic: canvas
subtopic: visual_in_the_loop
created: 2026-06-24
updated: 2026-06-24
sources: ["Operation Prytaneion Phase 1 (Home.aDNA M1.1 capability)", "Home.aDNA what/code/{canvas_visual_loop,iii_runner,window_helpers}.py"]
context_version: "1.0"
token_estimate: ~1500
last_edited_by: agent_hestia
tags: [context, canvas, visual_in_the_loop, agentic, verification, prytaneion, contributed]
---

# Canvas: Visual-in-the-Loop (agent-confirmed render)

> **Contributed by Home.aDNA (Hestia) — Operation Prytaneion M6.3.** Companion to `context_canvas_topology_graphs.md`. Establishes the producer-side standard: **no canvas ships without an agent-confirmed render.**

## The standard

A canvas's correctness is **visual** — JSON validity proves nothing about whether it reads. The rule Home adopted and proved across ~100 Prytaneion cycles:

> **No canvas ships without an agent-confirmed Obsidian screenshot.** The agent (not a human, not a metric) reads the rendered image and judges it. Optional vision-model critique is an aid, never the gate.

## The loop

```
design  →  render (generator writes .canvas)  →  open/navigate in live Obsidian
        →  screenshot (non-disruptive, focus-free)  →  AGENT READS the image
        →  edit  →  re-render  →  (repeat until the agent-eye passes)
```

This bridges two pre-existing pieces: a **producer's HTML/offline render** (proves the layout deterministically) and a **live-Obsidian capture** (proves it renders the same way the operator will see it, with the Advanced Canvas plugin actually drawing the edges).

## Reference implementation (Home.aDNA — macOS)

Home's hardened harness (offered as the worked reference; the *code home* — `canvas_core` vs. consumer-local — is Mondrian's call per the M6.3 memo):

| Module | Role | Portability |
|---|---|---|
| `canvas_visual_loop.py` | Orchestrator; CLI `--render --capture --critique` | **Portable** — thin wrapper; paths via env (`VAULT_ROOT`/`HOME_PATH`) |
| `iii_runner.py` | Navigate-to-canvas + capture series + optional vision critique + JSONL learning-store | **Portable** (Gemini critique is optional/`--critique`-gated) |
| `window_helpers.py` | Focus-free window capture | **⚠ macOS-only** (`CGWindowList` + `screencapture` + `osascript`); needs Linux (`xdotool`/`wmctrl`) + Windows (PowerShell) stubs to generalize |

**Preconditions:** Obsidian running; a one-time `obsidian://` "Don't ask again for open" grant (else navigation stalls silently); window resolved by **title-pinning** (`title_contains`) so blind captures don't grab the wrong vault.

## Known constraints (carry-forward)

- **Stills, not timing/frame-rate** — the harness captures images, not performance; render *cost* is a separate (operator-eye) concern.
- **No headless zoom-to-fit** — captures the current viewport; frame the canvas before capture or crop after.
- **Window instability post-restart** — re-resolve the window each cycle; fall back to a fresh capture if the handle goes stale.

## Adoption path

1. Adopt the **standard** (agent-confirmed render) in `canvas_std` producer doctrine — independent of any specific harness.
2. If the harness graduates into `canvas_core`: generalize `window_helpers` behind an abstract `get_window_info()` with per-OS backends; keep the Gemini critique optional.
3. The canvas-visual *learnings* (state-luminance scoring, edge-de-spaghetti critique prompts, the no-canvas-without-screenshot check) are a separate **III.aDNA** graduation candidate (filed at M6.3).

## Sources

Home.aDNA Operation Prytaneion: `mission_p1_m1_1*` (capability build, 6 findings) + `mission_p1_m1_3*` (100-cycle cadence). Code: `Home.aDNA/what/code/{canvas_visual_loop,iii_runner,window_helpers}.py` + `how/skills/skill_canvas_visual_loop.md`.
