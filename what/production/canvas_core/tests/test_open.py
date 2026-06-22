"""Tests for canvas_core.open (M-R4-01b).

Covers the URL-construction contract for the ``newLeaf`` flag and the
``open_in`` keyword. Mock-based — no live Obsidian needed. Closes F-33
HIGH (Phase 7 HOLD-driver) and F3 from
``lattice-labs/who/coordination/note_20260410_canvas_pattern_findings.md``.
"""

from __future__ import annotations

import os
import sys
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.open import _REST_BASE, CanvasOpener, ControlMethod


class _FakeResponse:
    """Minimal stand-in for ``urllib.request.urlopen``'s context manager."""

    def __init__(self, status: int = 200) -> None:
        self.status = status

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *_args: object) -> bool:
        return False


def _make_opener_with_rest(tmp_path) -> CanvasOpener:
    """Construct a CanvasOpener with REST forced as the only available method."""
    opener = CanvasOpener(
        vault_root=tmp_path,
        vault_name="TEST-VAULT",
        rest_api_key="test-key",
        auto_discover_rest=False,
    )
    opener._detected = {
        ControlMethod.REST: {"base_url": _REST_BASE, "api_key": "test-key"},
    }
    opener.preferred_method = ControlMethod.REST
    return opener


def test_open_batch_uses_new_leaf_by_default(tmp_path):
    """``open_batch`` must send ``newLeaf=true`` on every URL by default.

    Closes F-33: prevents silent active-leaf clobber on sequential opens.
    """
    opener = _make_opener_with_rest(tmp_path)
    captured_urls: list[str] = []

    def fake_urlopen(req, *_args, **_kwargs):
        captured_urls.append(req.full_url)
        return _FakeResponse(200)

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = opener.open_batch(["a.canvas", "b.canvas"], delay=0)

    assert result["opened"] == ["a.canvas", "b.canvas"], result
    assert result["failed"] == [], result
    assert len(captured_urls) == 2
    assert all("newLeaf=true" in url for url in captured_urls), captured_urls
    assert all("newLeaf=false" not in url for url in captured_urls), captured_urls


def test_open_with_active_uses_new_leaf_false(tmp_path):
    """``open(path, open_in="active")`` must send ``newLeaf=false``.

    Lets callers explicitly opt into the legacy active-leaf-clobber behavior
    (e.g., for the first canvas in a sequence intended to replace a junk tab).
    """
    opener = _make_opener_with_rest(tmp_path)
    captured_urls: list[str] = []

    def fake_urlopen(req, *_args, **_kwargs):
        captured_urls.append(req.full_url)
        return _FakeResponse(200)

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        ok = opener.open("test.canvas", open_in="active")

    assert ok is True
    assert len(captured_urls) == 1
    assert "newLeaf=false" in captured_urls[0], captured_urls[0]
    assert "newLeaf=true" not in captured_urls[0], captured_urls[0]
