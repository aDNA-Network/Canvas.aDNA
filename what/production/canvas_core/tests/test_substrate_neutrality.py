"""Substrate-neutrality ratchet — formalize the ADR-001 grep as a runtime test.

Mirrors the source-grep pattern at canvas_comic/tests/test_comic_builder.py:141-146.
Iterates over every .py file in canvas_core/ and asserts that no module imports
the application packages (deck or comic). Closes M-R5-01 F-7 (registry / re-export
side-effect coverage) and locks the substrate-neutrality ratchet against drift.

Comment-only references (in docstrings, # comments) are tolerated — the assertions
match the leading "import" / "from" statement form to avoid false positives on
historical Wave 2 transition documentation in print.py / design_tokens.py / etc.

Note: this file's docstring intentionally avoids beginning lines with the literal
"from canvas_presentation" / "from canvas_comic" pattern, so the ratchet grep stays
clean against its own ratchet test. (M-R5-01a S1 cleanup.)
"""

from __future__ import annotations

import os
import re
from pathlib import Path

CANVAS_CORE_DIR = Path(__file__).resolve().parent.parent

# Match leading import statements only — at start-of-line (after optional whitespace).
# Excludes commented-out imports and string-literal references in docstrings.
_FORBIDDEN_IMPORT = re.compile(
    r"^\s*(?:from\s+canvas_(?:presentation|comic)|import\s+canvas_(?:presentation|comic))",
    re.MULTILINE,
)


def _iter_canvas_core_files() -> list[Path]:
    """Walk canvas_core/ and return every .py file except tests/."""
    out: list[Path] = []
    for root, _dirs, files in os.walk(CANVAS_CORE_DIR):
        if os.path.basename(root) == "tests":
            continue
        for f in files:
            if f.endswith(".py"):
                out.append(Path(root) / f)
    return out


class TestSubstrateNeutrality:
    """ADR-001 substrate-neutrality ratchet — canvas_core never imports applications."""

    def test_canvas_core_has_modules(self):
        """Sanity: the iterator finds modules to scan."""
        files = _iter_canvas_core_files()
        # 21 top-level + 5 critique + 3 rlhf + 8 traps = 37 modules expected as of M-R3-01a.
        assert len(files) >= 30, f"expected >=30 canvas_core modules, found {len(files)}"

    def test_no_canvas_presentation_imports(self):
        """No canvas_core/ module imports from canvas_presentation."""
        violations: list[str] = []
        for path in _iter_canvas_core_files():
            source = path.read_text()
            for match in _FORBIDDEN_IMPORT.finditer(source):
                if "canvas_presentation" in match.group(0):
                    line_no = source[: match.start()].count("\n") + 1
                    violations.append(f"{path.relative_to(CANVAS_CORE_DIR.parent)}:{line_no} — {match.group(0).strip()}")
        assert violations == [], "substrate-neutrality violations:\n" + "\n".join(violations)

    def test_no_canvas_comic_imports(self):
        """No canvas_core/ module imports from canvas_comic."""
        violations: list[str] = []
        for path in _iter_canvas_core_files():
            source = path.read_text()
            for match in _FORBIDDEN_IMPORT.finditer(source):
                if "canvas_comic" in match.group(0):
                    line_no = source[: match.start()].count("\n") + 1
                    violations.append(f"{path.relative_to(CANVAS_CORE_DIR.parent)}:{line_no} — {match.group(0).strip()}")
        assert violations == [], "substrate-neutrality violations:\n" + "\n".join(violations)

    def test_init_files_have_no_application_side_effects(self):
        """Subpackage __init__.py files (canvas_core/, critique/, traps/, rlhf/) do not
        import application packages as a side-effect of being imported themselves.

        Closes F-7 — registry / re-export side-effect coverage.
        """
        init_files = [p for p in _iter_canvas_core_files() if p.name == "__init__.py"]
        # Expected: canvas_core/__init__.py + critique/__init__.py + rlhf/__init__.py + traps/__init__.py = 4
        assert len(init_files) >= 4, f"expected >=4 __init__.py files, found {len(init_files)}"

        violations: list[str] = []
        for path in init_files:
            source = path.read_text()
            for match in _FORBIDDEN_IMPORT.finditer(source):
                line_no = source[: match.start()].count("\n") + 1
                violations.append(f"{path.relative_to(CANVAS_CORE_DIR.parent)}:{line_no} — {match.group(0).strip()}")
        assert violations == [], "registry side-effect violations:\n" + "\n".join(violations)
