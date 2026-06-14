---
type: artifact
artifact_class: parity_report
created: 2026-06-13
updated: 2026-06-13
last_edited_by: agent_stanley
mission: mission_e3_3_parity_gate
campaign: campaign_canvas_genesis
tags: [artifact, parity, regression, gate, keystone, e3, canvasforge]
---

# E3.3 — Parity/regression report (Approach A: deterministic structural proof)

**Question.** Does routing CanvasForge through `canvas_std` (via the E3.2 constants-only shim) regress any
output vs the locked baselines **Wilhelm 8.80** (deck) / **Issue 01 8.43** (comic)?

**Method (operator-chosen).** Deterministic, API-free. Because E3.2 repointed only the floor *constants*
(now `is`-identical objects) and `core.py`'s only change is constant-definitions→imports, the canvas-generation
logic is unchanged — so parity reduces to **structural equivalence**, provable without the non-deterministic
Gemini VR re-score. Reproducible via `e3_3_parity_check.py` (this dir) on the E3.2 `.venv`.

## Evidence

### 1. Static proof — no logic changed
`git diff 1a51801~1 1a51801 -- what/code/canvas_core/core.py`: **1 file, +41 / −75**, entirely the constant block
collapsing to `from canvas_std import schema` re-exports + the import/`DeprecationWarning` header. Filtering the
diff for any method/control-flow line (`def`/`return`/`self.`/`if`/`for`/…, excluding constants/imports/comments)
yields a single hit — `stacklevel=2`, part of the `warnings.warn(...)` call. **No `CanvasBuilder` method touched.**

### 2. Object identity (E3.2, re-confirmed)
All 12 floor symbols (`VALID_*` ×10 + `TYPE_MAPPING` + `EDGE_TYPE_MAPPING`) on `CanvasBuilder` are
`is`-identical to `canvas_std.schema` → the federated objects ARE the ones generation reads.

### 3. Determinism (normalizer complete)
Two shim-ON rebuilds of the Wilhelm deck (`build_wilhelm().build()` → full generation path), normalized modulo the
random `secrets.token_hex` IDs, give an **identical** structural SHA-256
`aa6756658d07eff8d871ed57d22e4602e5cfce479de7be905f0efedb3c423ac7`. The build is deterministic modulo IDs.

### 4. A/B isolation — the shim is output-neutral (the load-bearing result)
Rebuild shim-ON (HEAD) vs shim-OFF (`core.py` reverted to `1a51801~1`, then restored to HEAD):

| Run | `deck_norm_sha256` |
|-----|--------------------|
| shim-ON  | `aa6756658d07eff8d871ed57d22e4602e5cfce479de7be905f0efedb3c423ac7` |
| shim-OFF | `aa6756658d07eff8d871ed57d22e4602e5cfce479de7be905f0efedb3c423ac7` |

**Identical** → the shim changes nothing in generated output. (Deck: 56 nodes / 20 edges.) `core.py` confirmed
restored to HEAD (stub present, working tree clean) after the revert.

### 5. Federated floor accepts both reference artifacts
Every node value in the rebuilt deck (56 nodes) **and** the committed Issue-01 comic canvas (11 nodes) is accepted
by the federated `CanvasBuilder.VALID_NODE_TYPES` / `VALID_COLORS` / `VALID_SHAPES` → **0 rejects** on both. The
comic path is exercised on its committed canvas (its build does Gemini image-gen, deliberately not invoked).

### 6. VR1–VR5 ≥ baseline — by construction
The regenerated output is structurally identical (modulo IDs) to the output that scored **8.80 / 8.43**. VR scores
are a function of the rendered output, so they are **unchanged by construction**; the locked baseline scores carry
over. No re-score performed (Approach A; avoids LLM noise + baseline-write risk).

### 7. Baseline integrity + regression backstop
- `baseline_vr_scores.json` SHA-256 = `3ce4d341a727e53434eab16a30b3c9a6e0316ca62c5d6914b984e3ac2939e8b6`
  **UNCHANGED** before and after (CanvasForge Critical Rule 2 held — Approach A writes nothing to it).
- CanvasForge canonical suite under the shim: **900 passed / 3 skipped / 0 failed**.

## Conclusion

Structural equivalence is proven deterministically: the E3.2 shim is **output-neutral**. No regression vs the
locked baselines is possible. **Verdict: GREEN** (see `e3_3_parity_verdict.md`).
