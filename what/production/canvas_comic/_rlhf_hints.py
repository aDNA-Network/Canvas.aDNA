"""RLHF-derived hints loaded from the bridged learning store.

Per ADR-008 §D2 candidate B1: class-level constants loaded once at module
import from ``iii/what/context/canvasforge_iii_learning_store.jsonl`` (the
ADR-007 bridge target). Substrate-additive — no I/O at call time; the
6-layer prompt assembly stays a pure function. Builder consumers
(``_build_character_block`` + ``_build_camera_block`` in ``comic.py``)
accept hints via an explicit kwarg with default ``None`` semantics, so
existing call sites preserve S2-baseline behavior verbatim and no
re-baseline gate fires (per ADR-008 § Compliance).

Two surfaces:

- ``RLHF_CHARACTER_HINTS: dict[register, str]`` — per-register accumulated
  ``pick_reason`` text relevant to Layer-2 character-block context. Keyed
  by register-equivalence-class identifier (normalized exactly as
  ``canvas_core.rlhf.iii_bridge._derive_pattern`` does — lowercase, then
  ``+`` / ``-`` / `` `` → ``_``). Per ADR-007 §3 footnote.
- ``RLHF_CAMERA_NUANCES: dict[register, str]`` — same shape, Layer-4
  camera-block context. Same source data at S3; the semantic split is
  for builder-consumption clarity. Future refinement (per-builder
  tagging or NLP extraction over ``pick_reason`` text) deferred to
  S(N+1).

Module-load read is one-shot per Python process. Safe to no-op when
the store file is missing or contains zero matching entries (the
constants are returned as empty dicts and builders never apply hints).

Per-line JSON parse with try/except; malformed lines are skipped to
match ``iii_bridge.py`` defensive-parsing discipline.

Re-merge rationale (CR7+SO7):
``lattice-labs/who/coordination/coord_2026_04_16_forge_split.md``.

Created at M-V1-2-F-01 S3.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Final

# Vault root: this file is at .../what/code/canvas_comic/_rlhf_hints.py
# so 4 parents up reaches the vault root.
_VAULT_ROOT = Path(__file__).resolve().parents[3]
_LEARNING_STORE = (
    _VAULT_ROOT / "iii" / "what" / "context" / "canvasforge_iii_learning_store.jsonl"
)

# Mirror ``canvas_core.rlhf.iii_bridge.TRAP_IMAGE_GENERATION_VARIANT_PICK``
# without taking a hard dependency (the bridge module reads, this module
# also reads — they are siblings on the bridge contract, not a chain).
_TRAP = "image_generation_variant_pick"


def _normalize_register(register: str) -> str:
    """Mirror ``iii_bridge._derive_pattern`` register normalization."""
    return register.lower().replace("+", "_").replace("-", "_").replace(" ", "_")


def _load_hints() -> tuple[dict[str, str], dict[str, str]]:
    """Read the bridged learning store and derive per-register hint dicts.

    Returns ``(character_hints, camera_nuances)``. Both keyed by
    register-equivalence-class identifier. Returns empty dicts when the
    store file is missing or no matching entries exist.
    """
    if not _LEARNING_STORE.exists():
        return {}, {}

    character_acc: dict[str, list[str]] = {}
    camera_acc: dict[str, list[str]] = {}

    with _LEARNING_STORE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
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

    # Collapse to one summary string per register (unique entries, sorted
    # for deterministic output, joined with `` | `` separator).
    character_hints = {k: " | ".join(sorted(set(v))) for k, v in character_acc.items()}
    camera_nuances = {k: " | ".join(sorted(set(v))) for k, v in camera_acc.items()}
    return character_hints, camera_nuances


RLHF_CHARACTER_HINTS: Final[dict[str, str]]
RLHF_CAMERA_NUANCES: Final[dict[str, str]]
RLHF_CHARACTER_HINTS, RLHF_CAMERA_NUANCES = _load_hints()
