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
    python3 how/gates/gate_manifest.py --check-doors     # every pending door POSTs to the live receiver?
    python3 how/gates/gate_manifest.py --probe-freshness # gate #9's legs over planted pairs; runs no suites

Exit codes are distinct on purpose — *disagreement* and *omission* are different bugs:

    0  all gates green, no undeclared surfaces
    1  a suite failed
    2  a suite's counts disagree with the manifest
    3  an undeclared test-bearing surface exists  <-- the point of this file
    4  a runner-environment precondition failed
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
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
INBOX = VAULT / "who" / "coordination" / "inbox"
GATES_DIR = VAULT / "how" / "gates"

# F-V-1 (2026-10-12): the drop-box's own rule is "uncommitted = unread". Seven days is the grace a
# sitting cadence can honestly be held to; the three weeks it actually went unread was not.
INBOX_MAX_AGE_DAYS = 7

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
    kind: str  # "pytest" | "certify" | "gitdiff" | "freshness" | "census" | "inbox"
    path: Path
    expect: tuple[int, int] | None = None
    group: str = ""
    note: str = ""
    # ⛩ F-DT-5 (2026-09-13, Datum P2). Number of skips that may LEGITIMATELY vary with the operator's
    # environment rather than with the code. Defaults to 0, so every other gate stays exactly as
    # strict as it was: a test silently becoming a skip is a real regression (*a check that cannot run
    # is not a check that passes*) and must not be waved through.
    #
    # Where it is non-zero, the assertion changes shape rather than loosening: the TOTAL
    # (passed + skipped) must still match exactly — nothing may appear or vanish — and `skipped` must
    # land in [expect[1], expect[1] + env_skips]. What stops being pinned is only the SPLIT.
    env_skips: int = 0
    env_reason: str = ""
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
    # 146 -> 151 at Datum P2 (2026-09-13): the RESERVED_KEYS-consumer firewall touch, authorized by
    # operator ruling as the fourth deliberate canvas_std touch since Keystone. DERIVED, not inferred —
    # this morning's P0 baseline measured HEAD at 146/10 with the file absent, the working tree measures
    # 151/10, and the delta reconciles exactly against the 5 test functions in
    # `tests/test_registry_consistency.py`. Skips unchanged at 10, as expected: none of the five skip.
    # 151 -> 156 at Datum P3 (2026-09-15): firewall touch #5 — every vocabulary constant now DECLARES
    # its relationship to the JSON Schema and the declaration is checked against a derivation (F-DT-7).
    # DERIVED the same way and the arithmetic was closed before the number was written: the suite was
    # run at HEAD with the working tree stashed (151/10) and again with it restored (156/10); the diff
    # adds exactly 5 `def test_` functions. Skips unchanged at 10 — none of the five skip.
    # 156 -> 170 at Datum P4b (2026-09-15): firewall touch #6 — `tests/test_schema_conformance.py`,
    # the first thing in this package ever to validate a document against the PUBLISHED JSON Schema
    # (`certification` exercises the validator's verdicts; the schema is an independent second copy —
    # F-DT-7). DERIVED the same way, arithmetic closed before the number was written: suite run at
    # HEAD with the working tree stashed (156/10) and restored (170/10). +14 reconciles as **12
    # parametrized fixture cases + 2 standalone tests** — note the file holds only 3 `def test_`, so
    # counting functions here would have given +3 and looked plausible. Skips unchanged at 10.
    # 170/10 -> 236/22 at Vernier P2b (2026-10-16): firewall touch #7, LIP-0011 → v2.5.0 (signed 2026-10-15).
    # DERIVED per file by stash/restore, arithmetic closed before this number was written:
    #   test_schema_conformance  +3 passed            (one parametrized case per new corpus canvas)
    #   test_conformance         +3 passed            (likewise)
    #   test_fixtures            +21 passed / +12 skipped — 72 → 105 cases: the 3 new fixtures × the 6 old
    #                            checks = 18 (17 pass; the extended Terminal-shape fixture skips the native-only
    #                            check) + the new advisory check × 15 fixtures = 15 (4 pass, 11 declare no
    #                            expectation and skip). 17 + 4 = 21 · 1 + 11 = 12.
    #   test_sync_semantics      +39 passed           (17 `def test_`, parametrized to 39 — counting
    #                            functions would have given 17 and looked plausible)
    #   ⇒ 170 + 3 + 3 + 21 + 39 = 236 · 10 + 12 = 22.
    Gate("canvas_std", "pytest", CODE / "canvas_std", (236, 22)),
    # 11 -> 12: the A-8 golden `adna_axes.canvas` joined the corpus at Gridline P1.
    # 12 -> 15 at Vernier P2b (2026-10-16): LIP-0011's three implementer cases (Terminal-shape ·
    # City-twin-shape · Canvas `adr_004`), per the P2b mission's exit gate.
    Gate("certification", "certify", CODE / "canvas_std", (15, 0),
         note="certify.py --json; 'passed' is fixtures agreeing with the corpus"),
    # 1035 -> 1040 at Plumbline P1 (2026-09-11): +5 in test_conform.py for the authority/production
    # split. Investigated before editing, per this file's own rule — the delta was DERIVED by running
    # the suite at HEAD (1035) and at the working tree (1040) and reconciling against the 5 test
    # functions added, not inferred from the direction of the change. (⚠ I first assumed 6 and the
    # arithmetic refused to close; test_conform was 13 before, not 12.)
    # ⛩ F-DT-5 (2026-09-13, Datum P2) — THIS PIN WAS A CLAIM ABOUT THE OPERATOR'S DESKTOP.
    # `(1040, 3)` holds only while Obsidian is OPEN on this vault:
    # `test_visual_capture.py::test_live_window_probe_is_title_pinned` passes when `vc.find_window()`
    # resolves and `pytest.skip`s when it does not. With Obsidian closed, the SAME unchanged tree
    # measures `(1039, 4)` and this gate reported DISAGREE — a real disagreement about nothing.
    #
    # ⛔ NOT fixed by re-pinning to (1039, 4): that just re-pins to the other desktop state and the
    # gate breaks again the next time Obsidian is open. The invariant that actually holds is the
    # TOTAL — 1043 in both regimes — so that is what is asserted, with ONE skip declared as
    # environment-conditioned. Nothing may appear or vanish; only the split may move.
    #
    # ⚠ And it means the Datum P0 baseline, reported that morning as "all green, reproduced exactly",
    # was green PARTLY BY COINCIDENCE OF DESKTOP STATE. Had Obsidian been closed at 08:00 this would
    # have been a P0 finding. ⇒ a pinned passed/skipped split is a claim about the runner, not about
    # the code — the sibling of this file's declared runner-environment preconditions, except that
    # those are declared and checked and this one was neither.
    # 1043 -> 1045 total at Vernier P2b (2026-10-16): +2 `test_core.py::TestSyncHashIsTheStandards` (F-V-10,
    # CanvasBuilder now delegates to canvas_std.compute_sync_hash). Two plain functions, measured 1041/4.
    Gate("canvas_core", "pytest", PRODUCTION / "canvas_core", (1042, 3), env_skips=1,
         env_reason="test_live_window_probe_is_title_pinned skips unless Obsidian is open on this vault"),
    # 57 -> 58 at Vernier P2b (2026-10-16): +1 `test_provenance_is_sync_generator` (F-V-11).
    Gate("canvas_presentation", "pytest", PRODUCTION / "canvas_presentation", (58, 2),
         note="added 2026-09-10 — was never in a STATE gate line; found by this file's own "
              "discovery check on its first run"),
    Gate("canvas_context", "pytest", CODE / "canvas_context", (58, 0),
         note="the leg-2 proof; the suite whose two-day red spell motivated this manifest"),
    *[Gate(p, "pytest", PRODUCTION / p, None, group="producers") for p in PRODUCER_PACKAGES],
    Gate("comic_render", "pytest", PRODUCTION / "comic_render", (154, 2)),
    Gate("firewall", "gitdiff", CODE / "canvas_std", None,
         note="canvas_std must be byte-clean in the working tree; production never edits it"),
    Gate("registry_census", "census", VAULT, None,
         note="added 2026-09-13 (Datum P2, F-GL-1): the three hand-maintained copies of the "
              "`_reserved` namespace — RESERVED_KEYS, the JSON Schema's $defs.reserved.properties, "
              "and spec §7.2 — must agree, and every key a validator dispatches on must be in all "
              "of them. The spec leg is why this is a VAULT gate and not only a package test: the "
              "spec is a vault artifact the package must not depend on"),
    Gate("dual_channel_freshness", "freshness", VAULT, None,
         note="added 2026-09-11 (F-PL-6): every `*.diagram.yaml` is rebuilt and compared to the "
              "`.canvas` beside it. Both pairs in the vault had been stale for four days, across "
              "four phase closes, each publishing an all-green gate line. Two legs since 2026-10-26 "
              "(Vernier P3 obj 2, F-V-16): the source digest beside the rebuild, each counted on its "
              "own and each printing what it cannot see"),
    Gate("inbox_receipt", "inbox", INBOX, None,
         note="added 2026-10-13 (Vernier P6, F-V-1): 17 inbound memos sat untracked for up to three "
              "weeks — six of them ack_required — while ten gates printed green, because the "
              "drop-box was a registry with no consumer. An untracked inbox file older than "
              f"{INBOX_MAX_AGE_DAYS} days (from its `delivered_on`, else its mtime) is a FAIL"),
]

# Producer expectations are per-package, so a single package drifting cannot hide inside the total.
PRODUCER_EXPECT: dict[str, tuple[int, int]] = {
    "brief_consumer": (10, 0),
    "comic_generator": (123, 0),
    "deck_generator": (16, 0),
    "diagram_generator": (56, 0),  # 53 -> 56 at Vernier P3 obj 2 (2026-10-26): +3 in the new
                                   # `test_cli_source_digest.py` (the CLI stamps sync.source_sha256,
                                   # F-V-16) — DERIVED: HEAD 52a543f measured 53/0 before the edit
                                   # (and be15ce4 the same, 10-26 01:2x), the tree measures 56/0 after
                                   # it (pytest -q, 2026-10-26 08:2x), and the new file holds exactly 3
                                   # un-parametrized `def test_`, so +3 closes the arithmetic.
                                   # 52 -> 53 at Vernier P6 (2026-10-13): +1 F-S078-04 `TB` alias
                                   # test — DERIVED: 52 passed + 1 failed against HEAD's model.py,
                                   # 53 passed with the alias. Before that: 44 -> 49 at Plumbline P1: +5 for the production axis + the
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


# ---------------------------------------------------------------------------
# Gate #9's two legs (Vernier P3 objective 2, 2026-10-26).
#
# ⛩ F-V-16. The leg as first drafted read: "for every canvas that carries `sync.source_sha256`,
# recompute the hash". Neither of this vault's dual-channel canvases carried one, and the producer
# could not write one, so that leg would have run over a population of zero and printed green.
# ⇒ *a cross-check that cannot fail looks exactly like a cross-check that passed*, a third time.
# The producer now stamps the digest (diagram_generator's CLI, through canvas_std's one definition),
# and a pair without one FAILS its source leg rather than skipping it.
#
# Both legs run on every pair, every time. The mission title calls the source leg a "pre-filter";
# a literal pre-filter (skip the rebuild when the source is fresh) would reopen F-PL-6 itself,
# which was generator drift under unchanged sources. Neither leg subsumes the other:
#
#   yaml source · sha256 of the .diagram.yaml bytes vs `sync.source_sha256` — cannot see generator drift
#   rebuild     · the generator re-run vs the view, digest masked           — cannot see a view-neutral edit
#
# ⚠ What BOTH legs read, stated first (the 2026-10-26 reviewer seat's blocking finding): only the
# `.diagram.yaml` and the `.canvas`. NEITHER reads the prose `.md` of a dual-channel triple: the
# producer uses the prose path only for its stem, as a wikilink (`consume.py`, the refs line). In this
# vault "source hash" first meant a hash of the PROSE (Armor's and Terminal's sources are markdown), so
# every line this gate prints says "prose channel: neither leg reads it", and the pasted line says
# "prose unread". Prose-to-structure drift stays a gate-review obligation (REQ-O05), not a gate.
#
# The VERDICT follows the rebuild, the authority (D-O2-7, RULED 2026-10-26 by the operator; P1's
# plan-gate ruling: "source hash as a cheap pre-filter, rebuild-compare as the authority"). A stale
# digest beside a fresh rebuild is the pre-filter's own false positive: printed on every run, never a
# FAIL. A leg that cannot run (no digest, a failed recompute, a failed rebuild) FAILS its pair.
#
# The rebuild leg masks `sync.source_sha256` on BOTH documents. Without the mask, a stamped pair
# fails the rebuild leg on every source byte change, so "source stale · rebuild fresh" could never
# be observed and the two legs could not disagree by construction.
#
# The helpers take a pair list, never the vault implicitly, so `--probe-freshness` runs this exact
# code over planted pairs in a temp dir.
# ---------------------------------------------------------------------------
FRESHNESS_BLIND_SPOTS = {
    "source": "the prose channel; generator drift with the same input (F-PL-6); and whether a changed "
              "byte matters (a YAML comment reads as stale)",
    "rebuild": "the prose channel; a source edit that leaves the generated view unchanged (a comment, "
               "or a typo outside every rendered field)",
}
PROSE_UNREAD = "prose channel: neither leg reads it"

# The digest is computed in the RUNNER env, by canvas_std's own function (LIP-0011 §2, touch #7).
# This process runs under the operator's `python3`, which cannot import canvas_std (measured
# 2026-10-26: homebrew 3.14 vs the anaconda 3.12 runner), and a hashlib line here would be a second
# copy of the definition (F-V-13: a second copy can be wrong in bytes nobody can see).
_SOURCE_DIGEST = "import sys; from canvas_std import compute_source_sha256 as f; print(f(sys.argv[1]))"


def _rel(p: Path) -> str:
    try:
        return str(p.relative_to(VAULT))
    except ValueError:
        return p.name


def _generator_env() -> dict[str, str]:
    # ⚠ `src` must be PREPENDED, not appended. `what/production/diagram_generator` is the
    # *project* directory (src/, tests/, pyproject.toml) and shadows the real package at
    # `src/diagram_generator`, so a bare `-m diagram_generator` resolves to the wrong object and
    # dies with "is a package and cannot be directly executed". Found by this gate failing loudly
    # on its first run — which is the behaviour that was wanted.
    env = _env()
    env["PYTHONPATH"] = os.pathsep.join([str(PRODUCTION / "diagram_generator" / "src"), env["PYTHONPATH"]])
    return env


def _dual_channel_pairs(root: Path) -> tuple[list[tuple[Path, Path]], list[str]]:
    """Every ``*.diagram.yaml`` under ``root`` with its sibling ``.canvas`` — (pairs, problems)."""
    pairs: list[tuple[Path, Path]] = []
    problems: list[str] = []
    for src in sorted(root.rglob("*.diagram.yaml")):
        if ".git" in src.parts or "_archive" in src.parts or src.is_symlink():
            continue
        current = src.with_name(src.name.replace(".diagram.yaml", ".canvas"))
        if not current.exists():
            problems.append(f"{_rel(src)} has no .canvas beside it")
            continue
        pairs.append((src, current))
    return pairs, problems


def _sync_block(doc: object) -> dict:
    """``metadata.frontmatter._reserved.sync`` — the canonical placement (spec §7; canvas_std reads it
    the same way in ``validate._reserved_block``, which this process cannot import). ``{}`` if absent."""
    try:
        sync = doc["metadata"]["frontmatter"]["_reserved"]["sync"]  # type: ignore[index]
    except (KeyError, TypeError):
        return {}
    return sync if isinstance(sync, dict) else {}


def _digest_masked(doc: object) -> object:
    masked = copy.deepcopy(doc)
    _sync_block(masked).pop("source_sha256", None)
    return masked


def _source_digest(src: Path) -> str | None:
    proc = subprocess.run([str(PYTHON), "-c", _SOURCE_DIGEST, str(src)],
                          capture_output=True, text=True, cwd=str(VAULT), env=_env())
    return proc.stdout.strip() if proc.returncode == 0 and proc.stdout.strip() else None


def _freshness_legs(pairs: list[tuple[Path, Path]], tmp: Path) -> list[dict]:
    """Both legs over every pair. Rebuilds go into ``tmp``; nothing is written beside a pair."""
    gen_env = _generator_env()
    verdicts: list[dict] = []
    for i, (src, current) in enumerate(pairs, 1):
        v = {"pair": _rel(current), "source": "", "rebuild": ""}
        try:
            view = json.loads(current.read_text())
        except (OSError, ValueError) as exc:
            v["source"] = v["rebuild"] = f"unreadable view ({exc.__class__.__name__})"
            verdicts.append(v)
            continue
        stored = _sync_block(view).get("source_sha256")
        got = _source_digest(src) if stored else None
        if not stored:
            v["source"] = "no digest"
        else:
            v["source"] = "unreadable" if got is None else ("fresh" if got == stored else "stale")
        rebuilt = tmp / f"{i}.canvas"
        proc = subprocess.run(
            [str(PYTHON), "-m", "diagram_generator", "build", str(src), str(rebuilt)],
            capture_output=True, text=True,
            cwd=str(PRODUCTION / "diagram_generator"), env=gen_env,
        )
        if proc.returncode != 0:
            v["rebuild"] = f"failed (exit {proc.returncode})"
        else:
            fresh_doc = json.loads(rebuilt.read_text())
            # Compare parsed documents, not bytes: key order and whitespace are not the claim.
            same = _digest_masked(fresh_doc) == _digest_masked(view)
            v["rebuild"] = "fresh" if same else "stale"
            # D-O2-8 (2026-10-26, the second reviewer seat's offer #2): under D-O2-7 a broken recompute
            # that always reads "stale" could never turn this gate red. The rebuild has just stamped
            # the digest of the SAME bytes by the SAME function, so the leg's recompute must equal it;
            # if not, the leg is a tool fault and cannot run. A rebuild that no longer stamps at all
            # (the mask would hide it) is the same fault seen from the generator's side.
            stamp = _sync_block(fresh_doc).get("source_sha256")
            if not stamp:
                v["source"] = "tool fault (the rebuild carries no sync.source_sha256)"
            elif v["source"] in _LEG_RAN and got != stamp:
                v["source"] = "tool fault (the recompute differs from the rebuild's own stamp)"
        verdicts.append(v)
    return verdicts


_LEG_RAN = ("fresh", "stale")  # any other verdict means the leg could not run on that pair
BROKEN_RECOMPUTE = "a broken recompute (D-O2-8)"  # the probe case that swaps the recompute out


def _describe_pair(v: dict) -> str:
    """One pair, both leg verdicts, and in words what they mean together. Never a merged verdict."""
    text = f"{v['pair']}: yaml source {v['source']} · rebuild {v['rebuild']}"
    blocked = [leg for leg in ("source", "rebuild") if v[leg] not in _LEG_RAN]
    if blocked:
        # A leg that could not run is not a leg that disagreed, and never a leg that passed.
        why = {"no digest": "no sync.source_sha256 recorded (rebuild the canvas to stamp it)"}
        return text + "".join(f" — the {leg} leg cannot run: {why.get(v[leg], v[leg])}" for leg in blocked)
    if v["source"] == v["rebuild"]:
        return text
    if v["rebuild"] == "fresh":
        meaning = "the source moved and the view did not (a view-neutral edit, or a stale digest)"
    else:
        meaning = "the view moved and the source did not (generator drift, or a hand edit)"
    return f"{text} — the legs disagree: {meaning}"


def _pair_passes(v: dict) -> bool:
    """The REBUILD is the authority (P1, ruled at the plan gate: *"source hash as a cheap pre-filter,
    rebuild-compare as the authority"*), so a pair passes when its rebuild reads fresh **and** its
    source leg was able to run. A stale source digest beside a fresh rebuild is the pre-filter's own
    false positive (P1: *"stale when the canvas is fine"*): reported on every run, never a FAIL. A
    source leg that cannot run (no digest recorded, a failed recompute) is a FAIL, because then the
    gate does not carry both mechanisms for that pair (the campaign's definition of done, item 4) —
    F-V-16. This is D-O2-7, RULED 2026-10-26 by the operator (the strict alternative, a stale digest
    also failing, was not taken)."""
    return v["rebuild"] == "fresh" and v["source"] in _LEG_RAN


def _score_freshness(gate: Gate, verdicts: list[dict], problems: list[str]) -> None:
    """Fill ``gate`` from the per-pair verdicts. Each leg is counted on its own; nothing is averaged."""
    n = len(verdicts)
    passing = [v for v in verdicts if _pair_passes(v)]
    gate.actual = (n, 0)
    # Two legs disagree only when both RAN and differ; a leg that could not run is counted apart.
    disagreements = [_describe_pair(v) for v in verdicts
                     if v["source"] in _LEG_RAN and v["rebuild"] in _LEG_RAN and v["source"] != v["rebuild"]]
    # F-GL-7: the reporter needs every count and must not infer one. `actual` is (checked, 0), so a
    # line reading `got[0]/got[0]` would render X/X and be green-shaped even when stale.
    gate.meta.update(
        checked=n,
        fresh=len(passing),
        stale=n - len(passing),
        source_fresh=sum(v["source"] == "fresh" for v in verdicts),
        rebuild_fresh=sum(v["rebuild"] == "fresh" for v in verdicts),
        disagree=len(disagreements),
        disagreements=disagreements,
        cannot_run=sum(v["source"] not in _LEG_RAN or v["rebuild"] not in _LEG_RAN for v in verdicts),
        verdicts=verdicts,
    )
    faults = list(problems) + [_describe_pair(v) for v in verdicts if not _pair_passes(v)]
    if n == 0:
        gate.status = "FAIL"
        gate.detail = "; ".join(["no dual-channel pair found — a gate that checks nothing is not green"]
                                + faults)
        return
    if faults:
        gate.status = "FAIL"
        gate.detail = (f"{n - len(passing)} of {n} pair(s) stale by the rebuild (the authority) or "
                       "without a runnable source leg — " + "; ".join(faults))
        return
    gate.detail = f"{n} pair(s) fresh by the rebuild, the source leg ran on every one"


def freshness_leg_lines(gate: Gate) -> list[str]:
    """One line per leg, printed on every run, green or red: its count and what it cannot see."""
    if gate.kind != "freshness" or "checked" not in gate.meta:
        return []
    n = gate.meta["checked"]
    lines = [
        f"yaml source {gate.meta['source_fresh']}/{n} fresh (the pre-filter) — "
        f"compute_source_sha256(<.diagram.yaml>) vs sync.source_sha256; "
        f"blind to {FRESHNESS_BLIND_SPOTS['source']} — {PROSE_UNREAD}",
        f"rebuild     {gate.meta['rebuild_fresh']}/{n} fresh (the authority) — the generator re-run vs the "
        f"view, sync.source_sha256 masked; blind to {FRESHNESS_BLIND_SPOTS['rebuild']} — {PROSE_UNREAD}",
    ]
    if gate.meta.get("cannot_run"):
        lines.append(f"cannot run on {gate.meta['cannot_run']}/{n} pair(s) — each FAILS (D-O2-3)")
    # A disagreement is printed here on EVERY run, because a green gate prints no detail: the
    # pre-filter's false positive is not a FAIL, and it must not therefore be silent.
    lines += [f"⚠ {d}" for d in gate.meta.get("disagreements", [])]
    return lines


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

    elif gate.kind == "census":
        # F-GL-1. `RESERVED_KEYS` had no consumer, so LIP-0010's ratified append to it was correct and
        # INERT — and the proof that an inert list rots was already inside it: `interaction`, shipped
        # and validated since v2.2.0, was missing from all three hand-maintained copies of the
        # namespace for three months, because nothing read any of them.
        #
        #   => a specification with no consumer is indistinguishable from no specification.
        #
        # `test_registry_consistency.py` (Datum P2) covers the two copies INSIDE the package, so a fork
        # or a `pip install adna-canvas-std` inherits that much. This gate covers the third — spec §7.2
        # — which is a vault artifact the package correctly must not depend on. Two scopes, one
        # invariant; the duplication is named at both sites rather than left silent (F-DT-3).
        #
        # Exit codes are the census's own: 0 clean · 1 drift · 4 precondition.
        proc = subprocess.run(
            [str(PYTHON), str(Path(__file__).resolve().parent / "registry_census.py")],
            capture_output=True, text=True, cwd=str(VAULT), env=_env(),
        )
        # Derive the population from the tool's own output; do NOT restate it here. A literal in this
        # branch is exactly F-GL-7 — a gate observing correctly and reporting a constant.
        report = json.loads(subprocess.run(
            [str(PYTHON), str(Path(__file__).resolve().parent / "registry_census.py"), "--json"],
            capture_output=True, text=True, cwd=str(VAULT), env=_env(),
        ).stdout or "{}")
        ns = report.get("reserved_namespace", {})
        agree = bool(ns.get("all_agree"))
        n_keys = len(ns.get("python_RESERVED_KEYS", []))
        gate.actual = (n_keys if agree else 0, 0)
        gate.meta["keys"] = n_keys
        gate.meta["registries"] = len(report.get("python_registries", []))
        gate.meta["dynamic_sites"] = len(report.get("dispatch_dynamic_sites", []))
        if proc.returncode == EXIT_PRECONDITION:
            gate.status = "FAIL"
            gate.detail = f"census precondition fault: {proc.stderr.strip()[:120]}"
            return
        if proc.returncode != 0 or not agree:
            gate.status = "FAIL"
            # ⚠ Name the ACTUAL fault class — F-DT-6. The first version of this branch reported "the
            # _reserved namespace copies disagree" UNCONDITIONALLY, so a drifted schema TWIN
            # (`VALID_SIDES` vs `edge.fromSide`, namespace untouched and agreeing 11/11) was announced
            # as a namespace disagreement and sent the reader to the wrong three files. ⇒ *the report
            # is part of the check.*
            #
            # The fix at the time was to derive the causes HERE. Datum P3 moved that derivation into
            # the census itself and this branch now CONSUMES it — because a second derivation of the
            # cause is a second thing that can disagree with the first, which is the defect one level
            # up. The census owns its fault classes; this gate reports them.
            causes = report.get("causes") or []
            gate.detail = "; ".join(causes) or "census exit != 0 — see its output"
            return
        gate.detail = (f"{n_keys} keys agree across RESERVED_KEYS + schema + spec §7.2; "
                       f"{gate.meta['registries']} vocabulary registries enumerated, "
                       f"each declaring a state that matches the derivation")

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
        #
        # ⛩ Vernier P3 objective 2 (2026-10-26): a second leg, the source digest, beside the
        # rebuild. Each leg is counted on its own, the pair is fresh only when both legs are, and a
        # disagreement is named per pair rather than averaged. The legs, their blind spots and why the
        # rebuild masks the digest: the helpers above `run_gate` (F-V-16).
        pairs, problems = _dual_channel_pairs(VAULT)
        with tempfile.TemporaryDirectory() as tmp:
            verdicts = _freshness_legs(pairs, Path(tmp))
        _score_freshness(gate, verdicts, problems)
        if gate.status == "FAIL":
            return

    elif gate.kind == "inbox":
        # ⛩ F-V-1 (2026-10-12, Vernier P1b). `who/coordination/inbox/README.md` promises that the
        # recipient's COMMIT is the read-receipt — so an untracked file there is, by the drop-box's own
        # rule, an unread memo. Seventeen sat untracked for up to three weeks (six `ack_required`)
        # while every gate printed green: nothing read the drop-box, so nothing could notice it fill.
        #
        #   => an inbox nobody commits from is a registry with no consumer.
        #
        # Age is measured from DELIVERY, not from the file's mtime alone: a copy made with `cp -p`
        # keeps the sender's mtime, which would read a memo delivered this morning as weeks overdue.
        # `delivered_on` in the memo's frontmatter is the sender's stamp of the act; where it is
        # absent or unparseable the mtime stands in, and the basis is reported per file.
        # ⚠ What this gate CANNOT see (F-V-7, 2026-10-13): a memo addressed to us that was never copied
        # here. It measures the drop-box, not the fleet's outboxes.
        proc = subprocess.run(
            ["git", "-C", str(VAULT), "ls-files", "--others", "--exclude-standard", "--", str(gate.path)],
            capture_output=True, text=True, cwd=str(VAULT),
        )
        if proc.returncode != 0:
            gate.status = "FAIL"
            gate.detail = f"git ls-files exit {proc.returncode}: {proc.stderr.strip()[:120]}"
            gate.actual = (0, 0)
            return
        untracked = [VAULT / ln for ln in proc.stdout.splitlines() if ln.strip()]
        now = time.time()
        overdue: list[str] = []
        oldest = 0.0
        for f in untracked:
            delivered, basis = None, "mtime"
            try:
                m = re.search(r'^delivered_on:\s*"?([0-9T:+\-.Z ]+?)"?\s*(#.*)?$',
                              f.read_text(errors="replace")[:4000], re.M)
                if m:
                    delivered = dt.datetime.fromisoformat(m.group(1).strip().replace("Z", "+00:00"))
                    if delivered.tzinfo is None:
                        delivered = delivered.astimezone()
                    delivered, basis = delivered.timestamp(), "delivered_on"
            except (OSError, ValueError):
                delivered = None
            ts = delivered if delivered is not None else f.stat().st_mtime
            age = (now - ts) / 86400
            oldest = max(oldest, age)
            if age > INBOX_MAX_AGE_DAYS:
                overdue.append(f"{f.name} ({age:.0f} d by {basis})")
        gate.actual = (len(untracked), 0)
        gate.meta["untracked"] = len(untracked)
        gate.meta["overdue"] = len(overdue)
        gate.meta["oldest_days"] = oldest
        if overdue:
            gate.status = "FAIL"
            gate.detail = (f"{len(overdue)} of {len(untracked)} untracked inbox memo(s) older than "
                           f"{INBOX_MAX_AGE_DAYS} d — unread by the drop-box's own rule: " + "; ".join(overdue))
            return
        gate.detail = (f"{len(untracked)} untracked, none older than {INBOX_MAX_AGE_DAYS} d"
                       + (f" (oldest {oldest:.1f} d)" if untracked else ""))

    if gate.expect is not None and gate.actual != gate.expect:
        if gate.env_skips:
            # F-DT-5: the split may move with the environment; the TOTAL may not, and the skip count
            # may not exceed the declared allowance. Anything else is still a disagreement.
            exp_total = gate.expect[0] + gate.expect[1]
            got_total = gate.actual[0] + gate.actual[1]
            lo, hi = gate.expect[1], gate.expect[1] + gate.env_skips
            if got_total == exp_total and lo <= gate.actual[1] <= hi:
                # ⚠ status must be set explicitly here: the tail of this function is what normally
                # assigns "OK", and this branch returns before reaching it. The first version omitted
                # it and the reporter raised `KeyError: ''` — loudly, which is the point. A reporter
                # that defaulted an unknown status to green would have been F-GL-7 for the fourth time.
                gate.status = "OK"
                gate.detail = (f"{gate.actual[0]}/{gate.actual[1]} — total {got_total} holds; "
                               f"{gate.actual[1] - lo} of {gate.env_skips} env-conditioned skip(s) "
                               f"active ({gate.env_reason})")
                return
            gate.status = "DISAGREE"
            gate.detail = (f"expected total {exp_total} with skips in [{lo},{hi}], "
                           f"got {gate.actual[0]}/{gate.actual[1]} (total {got_total})")
            return
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
        elif gate.gate_id == "registry_census":
            # Derived from meta, never a literal (F-GL-7). `n/n` here is the number of _reserved keys
            # agreeing across all three copies over the number declared — on a disagreement `actual`
            # is (0, 0), so this renders `0/11` and the ⛔ suffix below fires. It cannot read green.
            keys = gate.meta.get("keys", 0)
            body = f"registry census **{got[0]}/{keys}** keys"
        elif gate.gate_id == "dual_channel_freshness":
            # `actual` is (checked, 0); every count below is from meta (F-GL-7). The headline `f/n`
            # counts PASSING pairs (the rebuild fresh and the yaml-source leg ran, D-O2-7); each leg
            # is then shown on its own (Vernier P3 obj 2), so a disagreement is visible in the pasted
            # line itself and never averaged into the headline. The population is named on the face
            # of the number (the 2026-10-26 seat's blocking finding): "source" here is the
            # .diagram.yaml, and neither leg reads the prose channel.
            n = gate.meta.get("checked", got[0])
            body = (f"dual-channel freshness **{gate.meta.get('fresh', 0)}/{n}** "
                    f"(yaml source {gate.meta.get('source_fresh', 0)}/{n} · "
                    f"rebuild {gate.meta.get('rebuild_fresh', 0)}/{n}; prose unread)")
        elif gate.gate_id == "inbox_receipt":
            # Derived from meta (F-GL-7). The verdict number is OVERDUE, so it leads; beside it, the
            # mail still INSIDE the grace window = untracked − overdue.
            # ⚠ The first version printed the raw untracked count as "< 7 d", so one overdue memo
            # rendered "1 overdue (1 untracked < 7 d)" — the same file counted on both sides of the
            # threshold, in the line written to end that family. Caught by the planted-probe run.
            overdue = gate.meta.get("overdue", 0)
            within = gate.meta.get("untracked", 0) - overdue
            body = f"inbox receipt **{overdue} overdue** ({within} untracked within {INBOX_MAX_AGE_DAYS} d)"
        else:
            shown = f"{got[0]}/{got[1]}" if got[1] else f"{got[0]}"
            body = f"`{gate.gate_id}` **{shown}**"
        # A red gate is named red in the line itself. Nothing here may render as green on a FAIL.
        parts.append(body if gate.status == "OK" else f"{body} ⛔ {gate.status}")
    return " · ".join(parts)


def check_doors() -> int:
    """⛩ F-V-5 (2026-10-12): a door is rendered against a port, and a port is a lease.

    The receiver had moved 8768 -> 8767 while it was down; four pending doors still carried
    ``data-receiver-url=…:8768`` and would have POSTed a verdict into nothing — or, worse, into
    whatever else came to hold that port (`:8765` is JupyterHub, F-P5 era). Nothing compared a
    rendered door to the live receiver, so the defect was invisible until someone clicked.

    Checks, for every ``how/gates/*.html`` that still has a ``.pending`` sentinel (an unruled door):
    its ``<body data-receiver-url>`` port equals the sidecar ``.gate_receiver.port``, and the
    receiver on that port answers ``/health`` naming THIS gates root — a probe that only confirms
    *something* is listening has not confirmed *what* is listening.

    Deliberately a flag, not a gate: whether the receiver is running is desktop state (the F-DT-5
    lesson), and a gate that fails when the operator has stopped a daemon is a claim about the
    runner, not the vault. Exits: 0 every door matches a live receiver · 1 a door points elsewhere ·
    4 no sidecar / receiver down or not ours (re-start it, then RE-RENDER the doors).
    """
    sidecar = GATES_DIR / ".gate_receiver.port"
    doors = sorted(h for h in GATES_DIR.glob("*.html")
                   if h.with_suffix(".pending").exists())
    print(f"door check — {len(doors)} pending door(s) in {GATES_DIR.relative_to(VAULT)}")
    if not sidecar.exists():
        print("  ⛔ no .gate_receiver.port sidecar — the receiver is not running for this gates root")
        return EXIT_PRECONDITION
    port = sidecar.read_text().strip()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=3) as r:
            health = json.loads(r.read().decode())
    except (OSError, ValueError) as exc:
        print(f"  ⛔ sidecar names :{port} but /health did not answer ({exc.__class__.__name__}) "
              "— stale sidecar or a dead receiver")
        return EXIT_PRECONDITION
    root = Path(str(health.get("gates_root", ""))).resolve()
    if root != GATES_DIR.resolve():
        print(f"  ⛔ :{port} answers, but serves {root} — not ours")
        return EXIT_PRECONDITION
    print(f"  receiver :{port} live, gates_root is ours (pid {health.get('pid')})")
    bad = 0
    for door in doors:
        m = re.search(r'<body[^>]*\bdata-receiver-url="([^"]*)"', door.read_text(errors="replace"))
        url = m.group(1) if m else ""
        door_port = (re.search(r":(\d+)", url) or [None, ""])[1] if url else ""
        ok = door_port == port
        bad += not ok
        print(f"  {'ok ' if ok else '⛔ '} {door.name}: "
              f"{url or '(no data-receiver-url — falls back to copy-paste / a default port)'}")
    if bad:
        print(f"\n{bad} door(s) would POST somewhere other than the live receiver — re-render them "
              "(how/federation/iss/CLAUDE.md §Render discipline).")
        return EXIT_FAILURE
    return EXIT_OK


def probe_freshness() -> int:
    """Gate #9's legs over PLANTED pairs in a temp dir — negative controls (Vernier P3 objective 2).

    A gate that has only ever read green has not shown it can read red. This seeds one pair from the
    vault — the first ``*.diagram.yaml``, copied byte for byte, and the generator's own stamped build
    of it — plants one change per case, and runs the SAME helpers ``run_gate`` uses. The vault is
    never written. The probe's comparator is itself checked on every run: one case carries a
    deliberately wrong expectation and must be reported as a mismatch. A probe that cannot fail is
    the defect this flag exists to remove (P2b: *a cross-check that cannot fail looks exactly like a
    cross-check that passed*).

    Exits: 0 every planted verdict as expected and the control failed as it must · 1 otherwise ·
    4 no seed pair, or the seed would not build.
    """
    problems = check_preconditions()
    if problems:
        print("freshness probe — ⛔ PRECONDITION FAILURE, so no planted verdict would mean anything:")
        for p in problems:
            print(f"  · {p}")
        return EXIT_PRECONDITION
    pairs, _ = _dual_channel_pairs(VAULT)
    if not pairs:
        print("freshness probe — ⛔ no *.diagram.yaml in the vault to seed from")
        return EXIT_PRECONDITION
    seed = pairs[0][0]
    seed_bytes = seed.read_bytes()
    print(f"freshness probe — seed {_rel(seed)}; planted pairs in a temp dir (the vault is never written)")

    def comment(src: Path, view: Path) -> None:
        src.write_bytes(src.read_bytes() + b"\n# probe: a comment, outside every rendered field\n")

    def nudge(src: Path, view: Path) -> None:
        doc = json.loads(view.read_text())
        doc["nodes"][-1]["x"] = int(doc["nodes"][-1].get("x", 0)) + 1
        view.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")

    def undigest(src: Path, view: Path) -> None:
        doc = json.loads(view.read_text())
        _sync_block(doc).pop("source_sha256", None)
        view.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n")

    def relabel(src: Path, view: Path) -> None:
        text = src.read_text(encoding="utf-8")
        if 'label: "' not in text:
            raise RuntimeError("seed has no quoted label to change")
        src.write_text(text.replace('label: "', 'label: "PROBE ', 1), encoding="utf-8")

    def nothing(src: Path, view: Path) -> None:
        pass

    def unbuildable(src: Path, view: Path) -> None:
        # Bytes still readable (so the digest recomputes, and differs), but no longer a diagram spec.
        src.write_text("this: [is not, a diagram spec\n", encoding="utf-8")

    def unreadable(src: Path, view: Path) -> None:
        src.chmod(0)  # the digest recompute and the rebuild both fail to read it

    # (name, plant, expected source, expected rebuild, the comparator must agree?, the gate's expected
    # status for this pair alone, and the words its report must carry — the report is part of the
    # check, F-GL-7: in the detail when it is red, on the always-printed leg lines when it is green)
    cases = [
        ("clean copy", nothing, "fresh", "fresh", True, "OK", PROSE_UNREAD),
        ("a comment appended to the source", comment, "stale", "fresh", True, "OK", "the legs disagree"),
        ("one node's x moved in the view", nudge, "fresh", "stale", True, "FAIL", "the legs disagree"),
        ("the digest removed from the view", undigest, "no digest", "fresh", True, "FAIL",
         "the source leg cannot run"),
        ("a label changed in the source", relabel, "stale", "stale", True, "FAIL", "stale by the rebuild"),
        ("a yaml that will not build", unbuildable, "stale", "failed", True, "FAIL",
         "the rebuild leg cannot run"),
        ("an unreadable source", unreadable, "unreadable", "failed", True, "FAIL",
         "the source leg cannot run"),
        # D-O2-8: the recompute is swapped for one that always returns a wrong digest, so it reads
        # "stale" on a clean pair. Without the cross-check this pair would PASS (rebuild fresh).
        (BROKEN_RECOMPUTE, nothing, "tool fault", "fresh", True, "FAIL", "the source leg cannot run"),
        ("control: a wrong expectation", nothing, "stale", "stale", False, None, None),
    ]

    def _norm(verdict: str) -> str:
        # "failed (exit N)" carries the generator's exit code, and a tool fault its reason; neither
        # detail is the claim.
        for head in ("failed", "tool fault"):
            if verdict.startswith(head):
                return head
        return verdict
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        gen_env = _generator_env()
        for i, (name, plant, exp_s, exp_r, must_agree, exp_status, words) in enumerate(cases):
            case = root / f"case{i}"
            case.mkdir()
            src, view = case / "p.diagram.yaml", case / "p.canvas"
            src.write_bytes(seed_bytes)
            built = subprocess.run(
                [str(PYTHON), "-m", "diagram_generator", "build", str(src), str(view)],
                capture_output=True, text=True, cwd=str(PRODUCTION / "diagram_generator"), env=gen_env,
            )
            if built.returncode != 0:
                print(f"  ⛔ the seed would not build (exit {built.returncode}) — {built.stderr.strip()[:160]}")
                return EXIT_PRECONDITION
            try:
                plant(src, view)
            except (RuntimeError, OSError, ValueError, KeyError, IndexError) as exc:
                bad += 1
                print(f"  ⛔  {name:<36} could not be planted on this seed ({exc})")
                continue
            (case / "rebuilds").mkdir()
            if name == BROKEN_RECOMPUTE:
                real = globals()["_source_digest"]
                globals()["_source_digest"] = lambda _src: "0" * 64
                try:
                    v = _freshness_legs([(src, view)], case / "rebuilds")[0]
                finally:
                    globals()["_source_digest"] = real
            else:
                v = _freshness_legs([(src, view)], case / "rebuilds")[0]
            agrees = (_norm(v["source"]), _norm(v["rebuild"])) == (exp_s, exp_r)
            ok = agrees == must_agree
            bad += not ok
            got = f"yaml source {v['source']} · rebuild {v['rebuild']}"
            if must_agree:
                print(f"  {'ok ' if ok else '⛔ '} {name:<36} {got}   (expected yaml source {exp_s} · rebuild {exp_r})")
            else:
                print(f"  {'ok ' if ok else '⛔ '} {name:<36} "
                      + ("the comparator reported the mismatch, as it must" if ok
                         else "the comparator AGREED with a wrong expectation — the probe cannot fail"))
            if exp_status is None:
                continue
            # The report is part of the check (F-GL-7): the pair alone must score as expected, and its
            # report must say why — in the detail when red, on the leg lines (printed every run) when green.
            g = Gate("probe", "freshness", case)
            _score_freshness(g, [v], [])
            status = g.status or "OK"  # run_gate's tail assigns "OK" to a gate the scorer left unset
            report = g.detail if status == "FAIL" else "\n".join(freshness_leg_lines(g))
            scored = status == exp_status and (words is None or words in report)
            note = (f"{status}" + (f", and the report says {words!r}" if words else "")) if scored \
                else f"status {status!r} (expected {exp_status}), report {report!r}"
            bad += not scored
            print(f"  {'ok ' if scored else '⛔ '} {'  ↳ the gate scores it':<36} {note}")
        # An orphan: a .diagram.yaml with no .canvas beside it is listed and FAILS, uncounted in n.
        orphan_dir = root / "orphan"
        orphan_dir.mkdir()
        (orphan_dir / "p.diagram.yaml").write_bytes(seed_bytes)
        o_pairs, o_problems = _dual_channel_pairs(orphan_dir)
        g = Gate("probe", "freshness", orphan_dir)
        _score_freshness(g, [], o_problems)
        orphan_ok = (not o_pairs and g.status == "FAIL" and "has no .canvas beside it" in g.detail
                     and g.meta.get("checked") == 0)
        bad += not orphan_ok
        print(f"  {'ok ' if orphan_ok else '⛔ '} {'an orphan yaml (no canvas)':<36} "
              + ("listed, uncounted, gate FAIL, as it must" if orphan_ok
                 else f"status {g.status!r}, detail {g.detail!r}"))
    # Zero population: a gate that checks nothing must not read green.
    g = Gate("probe", "freshness", VAULT)
    _score_freshness(g, [], [])
    zero_ok = g.status == "FAIL"
    bad += not zero_ok
    print(f"  {'ok ' if zero_ok else '⛔ '} {'no pairs at all':<36} "
          + ("gate FAIL, as it must" if zero_ok else f"status {g.status!r} — zero population read green"))
    if bad:
        print(f"\nPROBE FAILED: {bad} planted verdict(s) not as expected")
        return EXIT_FAILURE
    print("\nprobe OK — every planted verdict as expected; the control failed when it had to")
    return EXIT_OK


def main() -> int:
    ap = argparse.ArgumentParser(description="Run the Canvas.aDNA gate set and fail on omission.")
    ap.add_argument("--markdown", action="store_true", help="emit the STATE.md gate line")
    ap.add_argument("--discover-only", action="store_true", help="omission check only; run no tests")
    ap.add_argument("--check-doors", action="store_true",
                    help="check every pending door's receiver URL against the live receiver; run no tests")
    ap.add_argument("--probe-freshness", action="store_true",
                    help="run gate #9's two legs over planted pairs in a temp dir; run no suites")
    args = ap.parse_args()

    if args.check_doors:
        return check_doors()
    if args.probe_freshness:
        return probe_freshness()

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

    # Gate #9's legs, one line each, on EVERY run (Vernier P3 obj 2): a blind spot printed only when
    # the gate is red is a blind spot nobody reads while it is green, which is when it matters.
    for gate in GATES:
        lines = freshness_leg_lines(gate)
        if lines:
            print(f"\n{gate.gate_id} — two legs, each naming what it cannot see:")
            for line in lines:
                print(f"  {line}")

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
