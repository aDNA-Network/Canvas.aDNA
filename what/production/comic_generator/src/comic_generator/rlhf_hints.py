"""RLHF-derived prompt hints loaded from a bridged learning store — PORTED from the CanvasForge quarry, DORMANT.

The quarry (``canvas_comic._rlhf_hints``) read a vault-relative learning-store path at MODULE IMPORT and exposed two
module constants. Here the loader is an explicit function whose store path is an **optional argument defaulting to
absent** → the loader no-ops and returns ``({}, {})``. So in the default configuration (no store path) the producer
applies zero hints — the tuning channel is dormant until a consumer wires a store path in. The 6-layer prompt assembly
(``prompt.py``) stays pure: it accepts the per-register hint dicts as default-``None`` kwargs and is inert without them.

Substrate-neutral: no ``canvas_std`` import. Per-line JSON parse with skip-on-error (matches the quarry's defensive
parsing). Two surfaces, both ``dict[register, str]``:
  - character hints — Layer-2 character-block context, keyed by register-equivalence-class id;
  - camera nuances — Layer-4 camera-block context (same source data; the split is for builder-consumption clarity).

Source (KEEP-reference, NOT a dependency): ``Archive.aDNA/CanvasForge.aDNA/what/code/canvas_comic/_rlhf_hints.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

# The trap id the store entries are filtered by (mirrors the quarry's ``_TRAP`` constant).
_TRAP = "image_generation_variant_pick"


def _normalize_register(register: str) -> str:
    """Mirror the quarry's register normalization: lowercase, then ``+``/``-``/`` `` → ``_``."""
    return register.lower().replace("+", "_").replace("-", "_").replace(" ", "_")


def load_hints(store_path: str | Path | None = None) -> tuple[dict[str, str], dict[str, str]]:
    """Read a bridged learning store and derive per-register hint dicts. DORMANT by default.

    Returns ``(character_hints, camera_nuances)``, both keyed by register-equivalence-class id. When ``store_path`` is
    ``None`` (the default) or the file is missing, returns ``({}, {})`` — the no-op path. Malformed JSON lines are
    skipped (defensive parsing). Entries are filtered to ``trap == _TRAP``; each must carry a ``register`` +
    ``pick_reason`` under ``rlhf_consumer_namespace.canvasforge.image_generation``.
    """
    if store_path is None:
        return {}, {}
    p = Path(store_path)
    if not p.exists():
        return {}, {}

    character_acc: dict[str, list[str]] = {}
    camera_acc: dict[str, list[str]] = {}

    with p.open("r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("trap") != _TRAP:
                continue
            ns = (
                entry.get("rlhf_consumer_namespace", {})
                .get("canvasforge", {})
                .get("image_generation", {})
            )
            register = ns.get("register")
            pick_reason = ns.get("pick_reason")
            if not register or not pick_reason:
                continue
            key = _normalize_register(register)
            character_acc.setdefault(key, []).append(pick_reason)
            camera_acc.setdefault(key, []).append(pick_reason)

    # Collapse to one summary string per register (unique, sorted, ` | `-joined) — deterministic output.
    character_hints = {k: " | ".join(sorted(set(v))) for k, v in character_acc.items()}
    camera_nuances = {k: " | ".join(sorted(set(v))) for k, v in camera_acc.items()}
    return character_hints, camera_nuances


__all__ = ["load_hints"]
