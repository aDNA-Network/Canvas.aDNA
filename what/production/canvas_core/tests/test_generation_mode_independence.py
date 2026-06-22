"""Generation-mode independence — verify Claims 1 + 2 from
campaign_canvasforge_review.md:128.

Each application package (canvas_comic, canvas_presentation) must be importable
+ usable without pulling in the other application package as a side-effect.

Two test approaches:
1. **Source-grep** — mirror the canvas_comic/tests/test_comic_builder.py:141-146
   pattern, but for canvas_presentation/. Closes the M-R1-01 § 6 gap that no
   equivalent ratchet test existed for canvas_presentation.
2. **Subprocess import-graph** — spawn a fresh Python process, import only one
   application package, build a minimal builder, and verify the OTHER application
   package was not imported as a side-effect. This is a runtime exercise that
   complements the source-grep.
"""

from __future__ import annotations

import os
import subprocess
import sys
import textwrap
from pathlib import Path

import pytest

CODE_ROOT = Path(__file__).resolve().parent.parent.parent  # what/code/
PRESENTATION_DIR = CODE_ROOT / "canvas_presentation"
COMIC_DIR = CODE_ROOT / "canvas_comic"


# ---------------------------------------------------------------------------
# Source-grep ratchet (mirrors canvas_comic/tests/test_comic_builder.py:141-146)
# ---------------------------------------------------------------------------


class TestSourceGrepRatchet:
    """Mirror the comic-side substrate-neutrality grep, applied to canvas_presentation/.

    canvas_comic/tests/test_comic_builder.py:141-146 already covers
    canvas_comic.comic; this test extends the ratchet to every
    canvas_presentation/ module.
    """

    def test_no_canvas_presentation_imports_canvas_comic(self):
        """canvas_presentation/ must not import canvas_comic anywhere."""
        violations: list[str] = []
        for path in PRESENTATION_DIR.rglob("*.py"):
            if "tests" in path.parts:
                continue
            source = path.read_text()
            for line_no, line in enumerate(source.splitlines(), start=1):
                stripped = line.lstrip()
                if stripped.startswith("from canvas_comic") or stripped.startswith("import canvas_comic"):
                    violations.append(f"{path.relative_to(CODE_ROOT)}:{line_no} — {stripped}")
        assert violations == [], "canvas_presentation -> canvas_comic violations:\n" + "\n".join(violations)

    def test_no_canvas_comic_imports_canvas_presentation(self):
        """canvas_comic/ must not import canvas_presentation anywhere.

        Extends the existing canvas_comic/tests/test_comic_builder.py:141-146
        check (which only scans comic.py) to every canvas_comic/ module.
        """
        violations: list[str] = []
        for path in COMIC_DIR.rglob("*.py"):
            if "tests" in path.parts:
                continue
            source = path.read_text()
            for line_no, line in enumerate(source.splitlines(), start=1):
                stripped = line.lstrip()
                if stripped.startswith("from canvas_presentation") or stripped.startswith("import canvas_presentation"):
                    violations.append(f"{path.relative_to(CODE_ROOT)}:{line_no} — {stripped}")
        assert violations == [], "canvas_comic -> canvas_presentation violations:\n" + "\n".join(violations)


# ---------------------------------------------------------------------------
# Subprocess import-graph (runtime exercise)
# ---------------------------------------------------------------------------


def _run_subprocess_import_check(import_target: str, must_not_load_prefix: str) -> tuple[int, str, str]:
    """Run a subprocess that imports `import_target` and reports any sys.modules
    keys starting with `must_not_load_prefix`.

    Returns (returncode, stdout, stderr).
    """
    code = textwrap.dedent(
        f"""
        import sys
        import {import_target}
        leaked = sorted(k for k in sys.modules if k.startswith({must_not_load_prefix!r}))
        print("LEAKED:" + ",".join(leaked))
        """
    )
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        timeout=15,
        cwd=str(CODE_ROOT),
        env={**os.environ, "PYTHONPATH": str(CODE_ROOT)},
    )
    return result.returncode, result.stdout, result.stderr


class TestSubprocessImportGraph:
    """Spawn a fresh interpreter; verify importing one application package does
    NOT pull in the other as a side-effect.

    These tests use subprocess to bypass pytest's existing sys.modules state
    (other test files in the same session may have already imported both
    packages, polluting our snapshot).
    """

    def test_canvas_comic_does_not_load_canvas_presentation(self):
        rc, stdout, stderr = _run_subprocess_import_check(
            "canvas_comic.comic", "canvas_presentation"
        )
        assert rc == 0, f"subprocess failed: stderr={stderr}"
        leaked_line = next((line for line in stdout.splitlines() if line.startswith("LEAKED:")), "")
        leaked = leaked_line.removeprefix("LEAKED:").strip()
        assert leaked == "", (
            f"canvas_comic.comic import leaked canvas_presentation modules: {leaked}\n"
            "ADR-001 substrate-neutrality + Modularity Claim 1 (charter:128) violated."
        )

    def test_canvas_presentation_does_not_load_canvas_comic(self):
        rc, stdout, stderr = _run_subprocess_import_check(
            "canvas_presentation.presentation", "canvas_comic"
        )
        assert rc == 0, f"subprocess failed: stderr={stderr}"
        leaked_line = next((line for line in stdout.splitlines() if line.startswith("LEAKED:")), "")
        leaked = leaked_line.removeprefix("LEAKED:").strip()
        assert leaked == "", (
            f"canvas_presentation.presentation import leaked canvas_comic modules: {leaked}\n"
            "ADR-001 substrate-neutrality + Modularity Claim 2 (charter:128) violated."
        )


# ---------------------------------------------------------------------------
# Builder construction independence
# ---------------------------------------------------------------------------


class TestBuilderConstructionIndependence:
    """Verify ComicPageBuilder and PresentationBuilder can be instantiated
    independently without each other being available."""

    def test_comic_builder_construction(self):
        """ComicPageBuilder constructs without canvas_presentation."""
        code = textwrap.dedent(
            """
            import sys
            import canvas_comic.comic as cc
            cpb = cc.ComicPageBuilder(name="independence_test")
            page = cpb.add_page(1)
            assert page is not None
            leaked = sorted(k for k in sys.modules if k.startswith("canvas_presentation"))
            print("LEAKED:" + ",".join(leaked))
            """
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(CODE_ROOT),
            env={**os.environ, "PYTHONPATH": str(CODE_ROOT)},
        )
        assert result.returncode == 0, f"subprocess failed: stderr={result.stderr}"
        leaked_line = next((line for line in result.stdout.splitlines() if line.startswith("LEAKED:")), "")
        leaked = leaked_line.removeprefix("LEAKED:").strip()
        assert leaked == "", f"comic builder construction leaked: {leaked}"

    def test_presentation_builder_construction(self):
        """PresentationBuilder constructs without canvas_comic."""
        code = textwrap.dedent(
            """
            import sys
            import canvas_presentation.presentation as cp
            pb = cp.PresentationBuilder(name="independence_test")
            assert pb is not None
            leaked = sorted(k for k in sys.modules if k.startswith("canvas_comic"))
            print("LEAKED:" + ",".join(leaked))
            """
        )
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=15,
            cwd=str(CODE_ROOT),
            env={**os.environ, "PYTHONPATH": str(CODE_ROOT)},
        )
        assert result.returncode == 0, f"subprocess failed: stderr={result.stderr}"
        leaked_line = next((line for line in result.stdout.splitlines() if line.startswith("LEAKED:")), "")
        leaked = leaked_line.removeprefix("LEAKED:").strip()
        assert leaked == "", f"presentation builder construction leaked: {leaked}"
