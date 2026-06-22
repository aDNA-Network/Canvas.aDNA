"""Playwright headless-Chrome screenshot capture for canvas critique.

Guarded import — Playwright is only required when the critique pipeline
is actually invoked, not at module-load time.  If Playwright is not
installed, ``capture_screenshots`` raises ``RuntimeError`` with install
instructions.

New in M-1-08.  Pure substrate.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

_log = logging.getLogger(__name__)

_PLAYWRIGHT_AVAILABLE = False
try:
    from playwright.sync_api import sync_playwright  # type: ignore[import-untyped]
    _PLAYWRIGHT_AVAILABLE = True
except ImportError:
    pass


def capture_screenshots(
    html_path: Path,
    group_viewports: dict[str, tuple[int, int]],
    output_dir: Path,
) -> dict[str, Path]:
    """Capture per-group PNG screenshots from rendered HTML.

    Args:
        html_path: Path to the rendered HTML file.
        group_viewports: ``{group_id: (width, height)}`` for each group.
        output_dir: Directory to write PNG files to.

    Returns:
        ``{group_id: png_path}`` mapping.

    Raises:
        RuntimeError: If Playwright is not installed.
    """
    if not _PLAYWRIGHT_AVAILABLE:
        raise RuntimeError(
            "Playwright is required for screenshot capture. "
            "Install with: pip install playwright && playwright install chromium"
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    screenshots: dict[str, Path] = {}

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)

        for group_id, (width, height) in group_viewports.items():
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(f"file://{html_path.resolve()}")

            # Scroll to the group's rendered section if anchor exists.
            try:
                page.wait_for_selector(f"#{group_id}", timeout=3000)
                page.evaluate(
                    f"document.getElementById('{group_id}')?.scrollIntoView()"
                )
            except Exception:
                _log.debug("No anchor #%s found; capturing full viewport", group_id)

            png_path = output_dir / f"{group_id}.png"
            page.screenshot(path=str(png_path), full_page=False)
            screenshots[group_id] = png_path
            page.close()

        browser.close()

    return screenshots
