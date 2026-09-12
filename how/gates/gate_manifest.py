#!/usr/bin/env python3
"""Runnable gate manifest for Canvas.aDNA — the gate set, executable.

Fixes F-P5-3. The gate set used to be a sentence in ``STATE.md`` that a human retyped each close.
``canvas_context`` was in that sentence at Armature, silently fell out, and sat red for two days
across three phase closes that each published an all-green gate line — none of them lying.

    A skipped test prints ``s``. A suite nobody invoked prints nothing at all,
    and the gate line beside it reads exactly as green.

So this script's central job is not to run tests. It is to make **omission an error**. Every
test-bearing directory in the vault must be either a declared gate or an declared exclusion with a
stated reason; anything else is a hard failure (exit 3). Without that check this file would be a
prose list written in Python, with the same failure mode it replaces.

Usage
-----
    python3 how/gates/gate_manifest.py              # run everything, print the table
    python3 how/gates/gate_manifest.py --markdown   # also emit the STATE.md gate line
    python3 how/gates/gate_manifest.py --discover-only   # omission check alone; runs no tests

Exit codes are distinct on purpose — *disagreement* and *omission* are different bugs:

    0  all gates green, no undeclared surfaces
    1  a suite failed
    2  a suite's counts disagree with the manifest
    3  an undeclared test-bearing surface exists  <-- the point of this file
    4  a runner-environment precondition failed
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------------------
# Vault root is derived from THIS FILE, never from the cwd.
#
# Trap, hit live at P5: a `cd` into a package for a per-package run persists across shell
# invocations, so a later `git diff --stat -- what/code/canvas_std/` from the wrong directory
# returns empty — which is indistinguishable from "firewall diff 0". Every path below is absolute
# and every subprocess gets an explicit cwd=. This script never chdir()s.
# ---------------------------------------------------------------------------
VAULT = Path(__file__).resolve().parent.parent.parent
PRODUCTION = VAULT / "what" / "production"
CODE = VAULT / "what" / "code"

PYTEST = Path("/opt/anaconda3/bin/pytest")
PYTHON = Path("/opt/anaconda3/bin/python")

# PYTHONPATH per STATE.md §Verified Ground Truth (runner environment).
PYTHONPATH = os.pathsep.join([str(PRODUCTION), str(CODE / "canvas_context" / "src")])

EXIT_OK, EXIT_FAILURE, EXIT_DISAGREEMENT, EXIT_OMISSION, EXIT_PRECONDITION = 0, 1, 2, 3, 4


# ---------------------------------------------------------------------------
# Registry 1 — GATES. Every suite, by name, with the counts it is expected to produce.
#
# Trap, hit live at P5: the seventh producer package is named `brief_consumer`, NOT
# `brief_generator`. A glob over `*_generator` silently returns 257 and looks right. Producers are
# therefore enumerated by name here and must never be globbed.
# ---------------------------------------------------------------------------
@dataclass
class Gate:
    """One gate. ``expect`` is (passed, skipped); None means "not a counted pytest gate"."""

    gate_id: str
    kind: str  # "pytest" | "certify" | "gitdiff" | "freshness"
    path: Path
    expect: tuple[int, int] | None = None
    group: str = ""
    note: str = ""
    # Populated at run time:
    actual: tuple[int, int] | None = field(default=None, compare=False)
    status: str = field(default="", compare=False)
    detail: str = field(default="", compare=False)
    # Gate-specific facts the reporter needs and must not re-derive by hand (F-GL-7): e.g. the
    # certification corpus total, which used to be a literal `11` inside the gate-line generator.
    meta: dict = field(default_factory=dict, compare=False)


PRODUCER_PACKAGES = [
    "brief_consumer",  # <-- NOT brief_generator. Never glob this list.
    "comic_generator",
    "deck_generator",
    "diagram_generator",
    "document_generator",
    "letter_generator",
    "post_generator",
]

GATES: list[Gate] = [
    # 115 -> 146 at Gridline P1 (2026-09-11): the A-8 firewall touch. DERIVED, not inferred —
    # per-file collection at HEAD vs the working tree reconciles as +20 `test_axes.py` · +1
    # `test_conformance` (one parametrized case per fixture, 12->13) · +6 `test_fixtures` (six checks
    # per fixture, 66->72) = +27, then -1/+5 when the symmetric co-requirement was corrected to
    # asymmetric (F-GL-5). Arithmetic closed before this number was written.
    Gate("canvas_std", "pytest", CODE / "canvas_std", (146, 10)),
    # 11 -> 12: the A-8 golden `adna_axes.canvas` joined the corpus at Gridline P1.
    Gate("certification", "certify", CODE / "canvas_std", (12, 0),
         note="certify.py --json; 'passed' is fixtures agreeing with the corpus"),
    # 1035 -> 1040 at Plumbline P1 (2026-09-11): +5 in test_conform.py for the authority/production
    # split. Investigated before editing, per this file's own rule — the delta was DERIVED by running
    # the suite at HEAD (1035) and at the working tree (1040) and reconciling against the 5 test
    # functions added, not inferred from the direction of the change. (⚠ I first assumed 6 and the
    # arithmetic refused to close; test_conform was 13 before, not 12.)
    Gate("canvas_core", "pytest", PRODUCTION / "canvas_core", (1040, 3)),
    Gate("canvas_presentation", "pytest", PRODUCTION / "canvas_presentation", (57, 2),
         note="added 2026-09-10 — was never in a STATE gate line; found by this file's own "
              "discovery check on its first run"),
    Gate("canvas_context", "pytest", CODE / "canvas_context", (58, 0),
         note="the leg-2 proof; the suite whose two-day red spell motivated this manifest"),
    *[Gate(p, "pytest", PRODUCTION / p, None, group="producers") for p in PRODUCER_PACKAGES],
    Gate("comic_render", "pytest", PRODUCTION / "comic_render", (154, 2)),
    Gate("firewall", "gitdiff", CODE / "canvas_std", None,
         note="canvas_std must be byte-clean in the working tree; production never edits it"),
    Gate("dual_channel_freshness", "freshness", VAULT, None,
         note="added 2026-09-11 (F-PL-6): every `*.diagram.yaml` is rebuilt and compared to the "
              "`.canvas` beside it. Both pairs in the vault had been stale for four days, across "
              "four phase closes, each publishing an all-green gate line"),
]

# Producer expectations are per-package, so a single package drifting cannot hide inside the total.
PRODUCER_EXPECT: dict[str, tuple[int, int]] = {
    "brief_consumer": (10, 0),
    "comic_generator": (123, 0),
    "deck_generator": (16, 0),
    "diagram_generator": (52, 0),  # 44 -> 49 at Plumbline P1: +5 for the production axis + the
                                   # removed `generator` authority cell (test_authority.py).
                                   # 49 -> 52 at Gridline P1: +3 for A-8's asymmetry at the spec
                                   # surface (authority-without-production refused; production-alone
                                   # allowed) + the de-duplication pin that the axis sets ARE
                                   # canvas_std's objects rather than a local copy.
    "document_generator": (37, 0),
    "letter_generator": (17, 0),
    "post_generator": (20, 0),
}
for _g in GATES:
    if _g.group == "producers":
        _g.expect = PRODUCER_EXPECT[_g.gate_id]


# ---------------------------------------------------------------------------
# Registry 2 — EXCLUSIONS. A test-bearing directory that is deliberately not a gate.
#
# Every entry MUST carry a non-empty reason. A check that goes red for good reasons gets disabled,
# so "fail on anything unlisted" is not enough on its own — the escape hatch has to exist and has
# to be documented in the same place as the rule.
# ---------------------------------------------------------------------------
EXCLUSIONS: dict[str, str] = {
    "what/production/_scaffold": (
        "Inert copy-me clone template, not a producer. Its own README states it is excluded from "
        "the cross-producer sweep; its 11 tests exercise the skeleton, not shipped behaviour."
    ),
    "what/production/tests": (
        "Legacy federation-validation module, skip-guarded at adr_009 (F-H6RE-2): SS and CC retired "
        "the wrapper surfaces it validates. Kept under SO-7 archive-never-delete."
    ),
    "what/production/_archive": (
        "SO-7 archive. Never collected — `norecursedirs = _archive` in what/production/pytest.ini."
    ),
}


# ---------------------------------------------------------------------------
# Preconditions. The editable install has silently drifted out of the runner env once before
# (Halftone), which looks like a mass test failure rather than an environment fault. Check first,
# and fail with a distinct code so the two are never confused.
# ---------------------------------------------------------------------------
def check_preconditions() -> list[str]:
    problems: list[str] = []

    if not PYTEST.is_file():
        problems.append(f"anaconda pytest not found at {PYTEST}")
    if not PYTHON.is_file():
        problems.append(f"anaconda python not found at {PYTHON}")

    if PYTHON.is_file():
        probe = subprocess.run(
            [str(PYTHON), "-c", "import canvas_std; print(canvas_std.__file__)"],
            capture_output=True, text=True, cwd=str(VAULT),
        )
        if probe.returncode != 0:
            problems.append(
                "`adna-canvas-std` is not importable — the editable install has drifted. "
                "Fix: pip install -e what/code/canvas_std"
            )
        else:
            resolved = Path(probe.stdout.strip())
            expected_root = CODE / "canvas_std" / "src"
            if expected_root not in resolved.parents:
                problems.append(
                    f"`canvas_std` resolves to {resolved}, not the in-vault editable source under "
                    f"{expected_root}. A stale site-packages copy would certify the wrong code."
                )

    for required in (PRODUCTION, CODE, VAULT / ".git"):
        if not required.exists():
            problems.append(f"expected path missing: {required}")

    # No declared gate may resolve outside this vault. `run_gate` executes pytest with `cwd=` at the
    # gate path, so a gate pointed through a shim into a peer vault would run their suite and write
    # `.pytest_cache/` into their tree. This vault's standing conduct with peers is read-only
    # throughout (memo #10, memo #15) — and an agent adding a shim to GATES to clear an exit-3
    # omission is exactly how that would happen by accident, not by malice.
    # Deliberately EXIT_PRECONDITION, not EXIT_OMISSION: a foreign gate path is an environment
    # fault, and this file's contract is that distinct bugs never share an exit code.
    for gate in GATES:
        resolved = gate.path.resolve()
        if resolved != VAULT and VAULT not in resolved.parents:
            problems.append(
                f"gate {gate.gate_id!r} resolves to {resolved}, outside {VAULT}. run_gate() would "
                "execute pytest with cwd= inside another vault and write .pytest_cache there. "
                "Peer trees are read-only."
            )

    return problems


# ---------------------------------------------------------------------------
# Registry 3 — DISCOVERY. The whole point.
# ---------------------------------------------------------------------------
def discover_test_surfaces() -> tuple[list[Path], list[Path]]:
    """Every directory in the vault that holds tests, found on disk rather than recalled.

    Returns ``(surfaces, shims_skipped)``.

    ⚠ **``find -P``, not ``find -L`` — this walk does not follow symlinks.** Rosetta (aDNA.aDNA,
    2026-09-11) measured the cost of the other choice: a census of the template corpus run as
    ``ls */what/lattices/examples/*.canvas`` reads **254 files across 62 vaults** where the physical
    truth is **282 across 69**, because 14 root-level back-compat shims are followed by the glob —
    so live vaults are counted twice under two names and archived vaults reappear inside the live set.

        A shim is a second true name for one object, and a glob cannot tell a name from a thing.

    **This vault carries the same shape at its own root.** ``./git`` and ``./iii`` are symlinks into
    ``how/federation/``, so ``ls */CLAUDE.md`` reports **two** federation wrappers where there are
    **three** — and names both of the two by their *second* name, while missing ``comfyui/``, which
    has no shim at all.

    The omission *verdict* was already safe (:func:`run_discovery` compares ``.resolve()`` on both
    sides, so a shim canonicalises onto its target). What was not safe is the **population line**,
    which counted names rather than things, in the one file whose whole thesis is *enumerate the
    territory, don't re-read the map*. Nothing under ``what/production`` or ``what/code`` is a symlink
    today (measured 2026-09-11) — which is exactly when this is cheap to close.
    """
    found: set[Path] = set()
    shims: list[Path] = []
    for parent in (PRODUCTION, CODE):
        if not parent.is_dir():
            continue
        for child in sorted(parent.iterdir()):
            if child.is_symlink():
                # Skipped, never silently: an unreported skip is this file's own founding finding
                # one layer down — a check that is not run leaves no trace.
                shims.append(child)
                continue
            if not child.is_dir():
                continue
            if (child / "tests").is_dir() and _has_tests(child / "tests"):
                found.add(child)
    # A bare tests/ directory directly under a parent (what/production/tests/) is a surface too.
    for parent in (PRODUCTION, CODE):
        tests = parent / "tests"
        if tests.is_symlink():
            shims.append(tests)
            continue
        if tests.is_dir() and _has_tests(tests):
            found.add(tests)
    return sorted(found), shims


def _has_tests(tests_dir: Path) -> bool:
    return any(tests_dir.rglob("test_*.py"))


def declared_surfaces() -> dict[Path, str]:
    """Path -> how it is accounted for ('gate:<id>' or 'excluded')."""
    declared: dict[Path, str] = {}
    for gate in GATES:
        if gate.kind == "pytest":
            declared[gate.path.resolve()] = f"gate:{gate.gate_id}"
    for rel in EXCLUSIONS:
        declared[(VAULT / rel).resolve()] = "excluded"
    return declared


def run_discovery() -> tuple[list[Path], list[str], list[Path], int]:
    """Return (undeclared surfaces, EXCLUSIONS-registry problems, shims skipped, surfaces found)."""
    declared = declared_surfaces()
    surfaces, shims = discover_test_surfaces()
    undeclared = [p for p in surfaces if p.resolve() not in declared]

    problems: list[str] = []
    for rel, reason in EXCLUSIONS.items():
        if not reason.strip():
            problems.append(f"exclusion {rel!r} carries no reason — every exclusion must justify itself")
        if not (VAULT / rel).exists():
            problems.append(f"exclusion {rel!r} names a path that does not exist — stale registry entry")
    return undeclared, problems, shims, len(surfaces)


# ---------------------------------------------------------------------------
# Runners
# ---------------------------------------------------------------------------
_SUMMARY = re.compile(r"(\d+)\s+(passed|failed|skipped|error|errors)")


def _parse_pytest(output: str) -> tuple[int, int, int, int]:
    """(passed, skipped, failed, errors) from pytest's summary line."""
    for line in reversed([ln for ln in output.splitlines() if ln.strip()]):
        if "passed" in line or "failed" in line or "error" in line or "no tests ran" in line:
            counts = {"passed": 0, "skipped": 0, "failed": 0, "error": 0, "errors": 0}
            for n, word in _SUMMARY.findall(line):
                counts[word] = int(n)
            return (counts["passed"], counts["skipped"], counts["failed"],
                    counts["error"] + counts["errors"])
    return (0, 0, 0, 0)


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = PYTHONPATH
    return env


def run_gate(gate: Gate) -> None:
    if gate.kind == "pytest":
        proc = subprocess.run([str(PYTEST), "-q"], capture_output=True, text=True,
                              cwd=str(gate.path), env=_env())
        passed, skipped, failed, errors = _parse_pytest(proc.stdout + proc.stderr)
        gate.actual = (passed, skipped)
        if failed or errors or proc.returncode not in (0, 5):
            gate.status = "FAIL"
            gate.detail = f"{failed} failed, {errors} errors (exit {proc.returncode})"
            return

    elif gate.kind == "certify":
        proc = subprocess.run([str(PYTHON), "certify.py", "--json"], capture_output=True,
                              text=True, cwd=str(gate.path), env=_env())
        if proc.returncode != 0:
            gate.status = "FAIL"
            gate.detail = f"certify.py exit {proc.returncode}"
            gate.actual = (0, 0)
            return
        report = json.loads(proc.stdout)
        gate.actual = (report["passed"], 0)
        gate.meta["total"] = report["total"]  # F-GL-7: the reporter must not hard-code this
        gate.detail = f"standard v{report['standard_version']}"
        if not report["certified"]:
            gate.status = "FAIL"
            gate.detail = f"not certified: {report['passed']}/{report['total']}"
            return

    elif gate.kind == "gitdiff":
        # Absolute pathspec + explicit cwd=VAULT. See the cwd trap at the top of this file.
        #
        # ⛩ F-GL-2 (2026-09-11, Gridline P1): this was `git diff --stat`, which reports the
        # **unstaged** difference only. `git add`-ing a canvas_std edit made this gate print `diff 0`
        # while the tree differed from HEAD — *indistinguishable from clean*, which is the exact
        # sentence the cwd trap at the top of this file is about. It had never fired because no
        # campaign before Gridline ever staged a canvas_std change; the firewall's own gate could not
        # see the one operation a firewall touch necessarily performs.
        #
        # `git status --porcelain` is the predicate that answers the question actually being asked —
        # "is canvas_std byte-identical to HEAD?" — because it covers all THREE breach classes:
        # unstaged (` M`), staged (`M `), and **untracked** (`??`). The old check could not see the
        # third one at all: a new file added under canvas_std was a firewall breach that reported
        # `diff 0` forever, staged or not.
        proc = subprocess.run(
            ["git", "-C", str(VAULT), "status", "--porcelain", "--", str(gate.path)],
            capture_output=True, text=True, cwd=str(VAULT),
        )
        lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
        gate.actual = (len(lines), 0)
        if lines:
            gate.status = "FAIL"
            # Name the classes present, so a breach report distinguishes "edited" from "added" —
            # a bare count sent the reader back to the shell to find out which.
            classes = sorted({ln[:2].strip() or "??" for ln in lines})
            gate.detail = (f"{len(lines)} dirty path(s) in canvas_std [{' '.join(classes)}] "
                           "— the firewall is breached")
            return
        gate.detail = "clean vs HEAD (staged + unstaged + untracked)"

    elif gate.kind == "freshness":
        # F-PL-6. `pattern_diagrammatic_context`'s central law is that **drift between the two
        # channels is a defect, not a chore**. Nothing enforced it: the visual gate checks a canvas
        # as it stands, and no check compared a generated artifact against a regeneration of it.
        # Canvas's own two dual-channel canvases — the pair the ruled pattern cites BY NAME as its
        # motivating example — went stale on 2026-09-07 when the P2c re-gate changed the layout
        # engine, and stayed stale through P2c, P3, P4, P5 and the campaign close.
        #
        #   => a generated artifact that nobody regenerates is a claim nobody re-derived.
        #
        # The check is the regeneration itself, because that is the only thing that can answer it.
        # Rebuilds run into a temp dir: this gate never writes into the vault.
        # ⚠ `src` must be PREPENDED, not appended. `what/production/diagram_generator` is the
        # *project* directory (src/, tests/, pyproject.toml) and shadows the real package at
        # `src/diagram_generator`, so a bare `-m diagram_generator` resolves to the wrong object and
        # dies with "is a package and cannot be directly executed". Found by this gate failing loudly
        # on its first run — which is the behaviour that was wanted.
        gen_env = _env()
        gen_env["PYTHONPATH"] = os.pathsep.join(
            [str(PRODUCTION / "diagram_generator" / "src"), gen_env["PYTHONPATH"]]
        )
        stale: list[str] = []
        checked = 0
        with tempfile.TemporaryDirectory() as tmp:
            for src in sorted(VAULT.rglob("*.diagram.yaml")):
                if ".git" in src.parts or "_archive" in src.parts or src.is_symlink():
                    continue
                current = src.with_name(src.name.replace(".diagram.yaml", ".canvas"))
                if not current.exists():
                    stale.append(f"{src.relative_to(VAULT)} has no .canvas beside it")
                    continue
                checked += 1
                rebuilt = Path(tmp) / f"{checked}.canvas"
                proc = subprocess.run(
                    [str(PYTHON), "-m", "diagram_generator", "build", str(src), str(rebuilt)],
                    capture_output=True, text=True,
                    cwd=str(PRODUCTION / "diagram_generator"), env=gen_env,
                )
                if proc.returncode != 0:
                    stale.append(f"{src.relative_to(VAULT)} failed to rebuild (exit {proc.returncode})")
                    continue
                # Compare parsed documents, not bytes: key order and whitespace are not the claim.
                if json.loads(rebuilt.read_text()) != json.loads(current.read_text()):
                    stale.append(f"{current.relative_to(VAULT)} differs from a rebuild of its own source")
        gate.actual = (checked, 0)
        # F-GL-7: the reporter needs fresh-vs-checked and must not infer it. `actual` is (checked, 0),
        # so a gate line reading `got[0]/got[0]` renders X/X and is green-shaped even when stale.
        gate.meta["checked"] = checked
        gate.meta["stale"] = len(stale)
        if stale:
            gate.status = "FAIL"
            gate.detail = f"{len(stale)} of {checked} stale — " + "; ".join(stale)
            return
        gate.detail = f"{checked} pair(s) fresh"

    if gate.expect is not None and gate.actual != gate.expect:
        gate.status = "DISAGREE"
        gate.detail = f"expected {gate.expect[0]}/{gate.expect[1]}, got {gate.actual[0]}/{gate.actual[1]}"
    elif not gate.status:
        gate.status = "OK"


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------
def markdown_gate_line() -> str:
    """Render the STATE.md gate line from what the run OBSERVED — never from a literal.

    ⛩ **F-GL-7 (2026-09-11, Gridline P1): this function hard-coded green for all three non-pytest
    gates**, which are precisely the gates whose failure matters most:

    - ``"firewall diff **0**"`` was a **constant string**. It printed a clean firewall *while the
      firewall gate was FAILING*, during an authorized breach — and this is the one string a phase
      close **pastes** into `STATE.md`. The file's own contract is *"a close pastes generated output"*,
      so a hard-coded green here does not merely mislead the author, it **publishes** the wrong fact
      under the authority of having been generated.
    - ``certification **{passed}/11``** hard-coded the corpus total. The corpus reached 12 at this
      phase, so the line read **``12/11``**; had the corpus *shrunk* it would have read ``10/11`` and
      looked like a failure that had not happened.
    - ``dual-channel freshness **{n}/{n}**`` printed X/X unconditionally, so *one of two* pairs going
      stale would have rendered as ``1/1`` — green, in the gate built because two pairs went stale.

    ⇒ ***the report is part of the check.*** A gate that observes correctly and reports a literal has
    only moved the unverified claim one layer out — which is the family this whole file exists to end
    (F-GM-1, F-PL-6), found three times inside it in one sitting.

    Every gate now renders from ``gate.actual``/``gate.meta``, and any non-OK gate renders as an
    explicit ``⛔ <status>`` so the line **cannot be pasted as green while red**.
    """
    producers = [g for g in GATES if g.group == "producers"]
    total = sum((g.actual or (0, 0))[0] for g in producers)
    parts: list[str] = []
    emitted_producers = False
    for gate in GATES:
        if gate.group == "producers":
            # Collapse the group into one entry, in the position the group occupies in GATES.
            if not emitted_producers:
                producer_note = "" if all(g.status == "OK" for g in producers) else " ⛔"
                parts.append(f"producers **{total} across {len(producers)} packages**{producer_note}")
                emitted_producers = True
            continue
        got = gate.actual or (0, 0)
        if gate.gate_id == "certification":
            corpus_total = gate.meta.get("total", got[0])
            body = f"certification **{got[0]}/{corpus_total}**"
        elif gate.gate_id == "firewall":
            # Derived, not asserted: the count is dirty paths, so 0 is the only clean value.
            body = ("firewall diff **0**" if gate.status == "OK"
                    else f"firewall **{got[0]} dirty path(s)**")
        elif gate.gate_id == "dual_channel_freshness":
            # `actual` is (checked, 0) — the fresh count is checked minus stale, from meta.
            checked = gate.meta.get("checked", got[0])
            body = f"dual-channel freshness **{checked - gate.meta.get('stale', 0)}/{checked}**"
        else:
            shown = f"{got[0]}/{got[1]}" if got[1] else f"{got[0]}"
            body = f"`{gate.gate_id}` **{shown}**"
        # A red gate is named red in the line itself. Nothing here may render as green on a FAIL.
        parts.append(body if gate.status == "OK" else f"{body} ⛔ {gate.status}")
    return " · ".join(parts)


def main() -> int:
    ap = argparse.ArgumentParser(description="Run the Canvas.aDNA gate set and fail on omission.")
    ap.add_argument("--markdown", action="store_true", help="emit the STATE.md gate line")
    ap.add_argument("--discover-only", action="store_true", help="omission check only; run no tests")
    args = ap.parse_args()

    print(f"gate manifest — vault {VAULT}")
    print()

    problems = check_preconditions()
    if problems:
        print("PRECONDITION FAILURE — the runner environment is wrong, so no result below would mean anything:")
        for p in problems:
            print(f"  · {p}")
        return EXIT_PRECONDITION
    print("preconditions OK — anaconda pytest, adna-canvas-std editable in-vault, paths present")

    undeclared, registry_problems, shims, _found = run_discovery()
    if registry_problems:
        print("\nEXCLUSION REGISTRY PROBLEM:")
        for p in registry_problems:
            print(f"  · {p}")
        return EXIT_OMISSION
    if undeclared:
        print("\nOMISSION — test-bearing surfaces exist that this manifest does not account for.")
        print("This is the failure this file exists to produce. Add each to GATES, or to EXCLUSIONS")
        print("with a stated reason. Do not delete the check.")
        for p in undeclared:
            print(f"  · {p.relative_to(VAULT)}")
        return EXIT_OMISSION
    # Partition the surfaces actually found, rather than subtracting the size of a registry that
    # may name paths carrying no discoverable tests (what/production/_archive is one — it holds
    # tests only at grandchild depth, so discovery never sees it). Reporting `found - len(registry)`
    # would print a gated-count nobody derived, which is the exact defect class this file serves.
    surfaces, _ = discover_test_surfaces()
    declared = declared_surfaces()
    gated = [p for p in surfaces if declared.get(p.resolve(), "").startswith("gate:")]
    excluded_seen = [p for p in surfaces if declared.get(p.resolve()) == "excluded"]
    # "physical" is load-bearing, not decoration: this count is of THINGS, not of names. A symlink
    # shim under either parent would inflate it while leaving every verdict correct — Rosetta's
    # 254-vs-282 finding, which this vault already instantiates at its own root (./git, ./iii).
    print(f"discovery OK — {len(surfaces)} test-bearing surfaces (physical), all declared "
          f"({len(gated)} gated, {len(excluded_seen)} excluded with reasons; "
          f"{len(shims)} symlink shim(s) skipped)")
    for shim in shims:
        print(f"  · shim skipped: {shim.relative_to(VAULT)} -> {shim.resolve()}")

    if args.discover_only:
        return EXIT_OK

    print()
    for gate in GATES:
        run_gate(gate)

    width = max(len(g.gate_id) for g in GATES)
    print(f"{'gate'.ljust(width)}  {'expected':>10}  {'actual':>10}  status")
    print("-" * (width + 34))
    for gate in GATES:
        exp = f"{gate.expect[0]}/{gate.expect[1]}" if gate.expect else "—"
        got = f"{gate.actual[0]}/{gate.actual[1]}" if gate.actual else "—"
        mark = {"OK": "ok", "FAIL": "FAIL", "DISAGREE": "DISAGREE"}[gate.status]
        print(f"{gate.gate_id.ljust(width)}  {exp:>10}  {got:>10}  {mark}"
              + (f"  — {gate.detail}" if gate.detail and gate.status != "OK" else ""))

    producers = [g for g in GATES if g.group == "producers"]
    print("-" * (width + 34))
    # ⛩ F-GL-4 (2026-09-11, Gridline P1): the expected cell was the string literal `'267/7 pkg'`,
    # printed beside a derived actual of 272 — stale since Plumbline P1 bumped diagram_generator
    # 44 -> 49 and updated PRODUCER_EXPECT but not this line. The manifest therefore displayed a
    # disagreement with itself, in its own summary row, and reported ALL GATES GREEN — correctly,
    # because the per-package gates are what carry the verdict and every one of them agreed.
    # ⇒ a hand-typed total beside derived parts is a claim nobody re-derives. Now summed from
    # PRODUCER_EXPECT, so it cannot go stale: it is the same numbers the gates are checked against.
    exp_total = sum(PRODUCER_EXPECT[g.gate_id][0] for g in producers)
    got_total = sum((g.actual or (0, 0))[0] for g in producers)
    print(f"{'producers total'.ljust(width)}  {f'{exp_total}/{len(producers)} pkg':>10}  "
          f"{f'{got_total}/{len(producers)} pkg':>10}")

    failed = [g for g in GATES if g.status == "FAIL"]
    disagreed = [g for g in GATES if g.status == "DISAGREE"]

    if args.markdown:
        print("\n--- STATE.md gate line (generated — paste, do not retype) ---")
        print(markdown_gate_line())

    if failed:
        print(f"\nSUITE FAILURE: {', '.join(g.gate_id for g in failed)}")
        return EXIT_FAILURE
    if disagreed:
        print(f"\nCOUNT DISAGREEMENT: {', '.join(g.gate_id for g in disagreed)}")
        print("A disagreement is a finding to investigate, NOT a number to edit into this file.")
        print("Editing the expectation to match the observation is the defect this vault keeps finding.")
        return EXIT_DISAGREEMENT

    print("\nALL GATES GREEN — and every test-bearing surface on disk is accounted for.")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
