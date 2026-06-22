"""Round-trip: the sync hash is stable across rebuilds (deterministic geometry, no wall-clock/randomness)."""

from __future__ import annotations

from canvas_std import compute_sync_hash

from letter_generator.consume import build_letter


def test_sync_hash_is_stable(letter):
    assert compute_sync_hash(build_letter(letter)) == compute_sync_hash(build_letter(letter))
