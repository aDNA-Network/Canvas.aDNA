"""Shared canvas_core test fixtures (introduced at Halftone HR for the review-surface pair).

Only review-surface fixtures live here so far — the historic suites are self-contained and untouched.
"""

from __future__ import annotations

import json
import os
import struct
import sys
import zlib
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))


def _mk_png(path: Path, width: int, height: int) -> None:
    """A real (grey) PNG at exact dimensions — IHDR is what the review builder reads."""
    path.parent.mkdir(parents=True, exist_ok=True)

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(
            ">I", zlib.crc32(tag + data) & 0xFFFFFFFF
        )

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0)
    raw = b"".join(b"\x00" + b"\x80" * width for _ in range(height))
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


@pytest.fixture
def vault(tmp_path: Path) -> tuple[Path, Path]:
    """A tmp review-surface vault: manifest (one clean row · one row missing output_path · one row whose file
    is absent), the images, and a hidden-properties app.json. Returns (vault_root, manifest_path)."""
    root = tmp_path / "TestVault.aDNA"
    reg = root / "what/artifacts/style_registry/ss_character/canonical"
    (root / ".obsidian").mkdir(parents=True)
    (root / ".obsidian/app.json").write_text('{"propertiesInDocument": "hidden"}\n', encoding="utf-8")
    _mk_png(reg / "variations/anchor_var_1_portrait.png", 100, 100)      # 1:1
    _mk_png(reg / "variations/anchor_var_2_wide.png", 110, 60)           # 11:6
    manifest = {
        "anchor": "anchor.png",
        "variants": [
            {"id": 1, "axis": "framing", "label": "portrait", "aspect": "1:1",
             "output_path": "what/artifacts/style_registry/ss_character/canonical/variations/anchor_var_1_portrait.png",
             "prompt_or_instruction": "portrait prompt",
             "result_summary": {"success": True, "model": "imagen-4.0-ultra-generate-001"}},
            {"id": 2, "axis": "framing", "label": "wide", "aspect": "16:9",
             "prompt_or_instruction": "wide prompt",
             "error": "TypeError: run failed but the file landed later"},   # no output_path → pattern-derived
            {"id": 9, "axis": "scene", "label": "never_generated", "aspect": "1:1",
             "prompt_or_instruction": "missing"},                            # file absent → excluded
        ],
    }
    mpath = reg / "variations.manifest.json"
    mpath.write_text(json.dumps(manifest), encoding="utf-8")
    return root, mpath


def build_review(vault_fixture, **kw):
    """Build the review surface into the tmp vault; returns (vault_root, ReviewSurfacePaths)."""
    from canvas_core.rlhf import review_canvas

    root, mpath = vault_fixture
    return root, review_canvas.build_review_surface(
        mpath, root / "what/artifacts/review_surface_pilot", vault_root=root, **kw
    )
