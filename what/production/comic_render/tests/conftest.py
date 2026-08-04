"""Shared fixtures — the mini-issue canvas in an isolated tmp dir.

The fixture ``tests/fixtures/mini_issue.canvas`` is a committed copy of
``comic_generator/examples/science_stanley_mini_issue.canvas`` (16 nodes / 13 edges: 1 comic root,
2 spreads, 4 pages, 9 prompt_only panels incl. a full-page splash) — the bridge NEVER imports the
producer, so the handoff artifact is committed, not regenerated.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from comic_render.extract import plan
from comic_render.manifest import RenderManifest

FIXTURE = Path(__file__).parent / "fixtures" / "mini_issue.canvas"

PANEL_COUNT = 9
PAGE_COUNT = 4
SPLASH_ID = "spread0_page0_p0"


@pytest.fixture()
def canvas_path(tmp_path: Path) -> Path:
    """The mini-issue canvas copied into an isolated working dir."""
    target = tmp_path / "mini_issue.canvas"
    shutil.copy(FIXTURE, target)
    return target


@pytest.fixture()
def planned(canvas_path: Path) -> tuple[RenderManifest, Path, Path]:
    """(manifest, manifest_path, canvas_path) with the default fake generate chain."""
    manifest, mpath = plan(canvas_path)
    return manifest, mpath, canvas_path


@pytest.fixture()
def chain_planned(canvas_path: Path) -> tuple[RenderManifest, Path, Path]:
    """Planned with the hybrid generate→refine chain (both fake)."""
    manifest, mpath = plan(canvas_path, chain="generate:fake,refine:fake@0.4")
    return manifest, mpath, canvas_path
