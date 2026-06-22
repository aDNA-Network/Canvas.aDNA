"""Round-trip: the sync hash is stable across rebuilds for both a single post and a thread (deterministic geometry)."""

from __future__ import annotations

from canvas_std import compute_sync_hash

from post_generator.consume import build_post


def test_sync_hash_stable_single(single_post):
    assert compute_sync_hash(build_post(single_post)) == compute_sync_hash(build_post(single_post))


def test_sync_hash_stable_thread(thread):
    assert compute_sync_hash(build_post(thread)) == compute_sync_hash(build_post(thread))
