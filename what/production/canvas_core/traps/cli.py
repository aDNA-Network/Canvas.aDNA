"""canvas-visual-check — the visual-fidelity sibling of `canvas-std validate`.

`canvas-std validate` proves schema conformance and **nothing about whether a
canvas reads** — by design (the Standard is substrate-neutral; layout belongs
to producers). This CLI fills the gap it leaves: it runs the canvas-visual
trap pack (every `implemented`/`graduated` trap in ``TRAP_PACK_REGISTRY``,
including the Obsidian-CSS-calibrated geometry traps) against any `.canvas`
file and reports findings **with fix hints** (required heights, char budgets).

Born of the Oration M-R5 incident (2026-08-03): a 53-node canvas passed
`canvas-std … [OK]` and rendered with ~20/23 text nodes clipped. Nothing in
the documented authoring path would have warned the author. Now this does.

USAGE
-----
From `what/production/` (or with it on PYTHONPATH)::

    python -m canvas_core.traps.cli <file.canvas> [...] [--vault-root DIR] [--json] [--strict]

From any other vault, the batteries-included path is the canvas_core venv
(self-bootstrapping direct-path invocation)::

    <Canvas.aDNA>/what/production/canvas_core/.venv/bin/python \
        <Canvas.aDNA>/what/production/canvas_core/traps/cli.py <file.canvas>

(A bare interpreter also works if it has `pillow` + `pyyaml` — the bootstrap
adds both `what/production/` and `what/code/canvas_std/src/` to sys.path.)

Exit codes: **0** clean (or low/medium only) · **1** any high/critical finding
(`--strict`: medium also fails) · **2** unreadable input.

The vault root (for file-node resolution + `.obsidian/app.json`) is taken
from `--vault-root`, else auto-detected by walking up from the canvas file to
the nearest directory containing `.obsidian`; without one, the file-resolution
trap (CV-FILE-PROPS-01) skips and a note is printed.

**Profiles** (``--profile``, default ``knowledge-canvas``):

- ``knowledge-canvas`` — every implemented trap except deck-workflow ones
  (registry scope ``deck-specific``, plus CV-DIMENSION-VISIBILITY-01, whose
  aspect-ratio-metadata expectation presumes a presentation pipeline and would
  flag every hand-authored vault canvas) and the comic-domain traps.
- ``comic`` — additionally drops the three **knowledge-canvas aesthetic**
  traps (group padding · hierarchy/title-slot · node density) that a composed
  comic page fails *by design*, and admits ``comic-specific`` traps.
  Added at Halftone H6 from H4 finding #4.
- ``all`` — the full pack. ``--all-traps`` is the deprecated alias.

Every profile keeps the **correctness** traps — text bounds, image aspect
ratio, file resolution, edge labels, lead cost, coherence, pending. A profile
drops domain-inapplicable *aesthetics*, never a check that can catch a real
defect. The deck/producer build path runs the full pack via ``run_all_traps``
directly.

Neither this check nor `canvas-std validate` substitutes for **looking at the
rendered canvas** — the agent-confirmed-render doctrine
(`what/context/context_canvas_visual_in_the_loop.md`) still applies.

New in Halftone HV (2026-08-03). Substrate-neutral; stdlib-only at the CLI
layer (individual traps may soft-use Pillow via `text_metrics`).
"""

from __future__ import annotations

import argparse
import json
import os
import sys

if __package__ in (None, ""):
    # Direct-path invocation: put `what/production/` on sys.path so the
    # canonical package imports below resolve, and `what/code/canvas_std/src/`
    # so the canvas_core package's canvas_std federation import works without
    # a pip install (the src-layout package is importable from its src dir).
    _PRODUCTION_ROOT = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    sys.path.insert(0, _PRODUCTION_ROOT)
    _CANVAS_STD_SRC = os.path.join(
        os.path.dirname(_PRODUCTION_ROOT), "code", "canvas_std", "src"
    )
    if os.path.isdir(_CANVAS_STD_SRC):
        sys.path.insert(1, _CANVAS_STD_SRC)

from canvas_core.traps import TRAP_PACK_REGISTRY, TrapFinding  # noqa: E402
from canvas_core.traps.runner import run_all_traps  # noqa: E402

_SEVERITY_ORDER = ["critical", "high", "medium", "low"]
_FAIL_SEVERITIES = {"critical", "high"}

# Presentation-workflow traps excluded from the default (visual-fidelity)
# profile: they presume deck metadata a hand-authored vault canvas never has.
_PRESENTATION_ONLY = {"CV-DIMENSION-VISIBILITY-01"}

# Container-geometry traps that encode KNOWLEDGE-CANVAS AESTHETICS — breathing
# room, a title slot, a fill-ratio ceiling. They are correct for a board a
# human reads by scanning. They are wrong for a **comic page**, which is a
# composed reading surface: panels bleed flush to the page edge BY DESIGN, a
# page carries no heading, and a full-page splash fills its page by definition.
#
# Halftone H4 finding #4 measured it: the mini-issue draws 24 findings at
# source and 18 rendered, and every one of them comes from exactly these three
# traps. None is a defect. A gate that always fails is not a gate.
_KNOWLEDGE_CANVAS_AESTHETICS = {
    "CV-GROUP-PADDING-01",
    "CV-HIERARCHY-01",
    "CV-NODE-DENSITY-01",
}

DEFAULT_PROFILE = "knowledge-canvas"
PROFILES = ("knowledge-canvas", "comic", "all")


def _scoped(scope: str) -> set[str]:
    return {
        trap_id for trap_id, meta in TRAP_PACK_REGISTRY.items()
        if meta.get("scope") == scope
    }


def _profile_skips(profile: str = DEFAULT_PROFILE) -> set[str]:
    """Trap ids suppressed under ``profile``.

    ``all`` suppresses nothing. Every profile keeps the **correctness** traps
    (text bounds, image aspect ratio, file resolution, edge labels, lead cost,
    coherence, pending) — profiles only ever drop domain-inapplicable
    *aesthetic* checks, never a check that can catch a real defect.
    """
    if profile == "all":
        return set()
    skips = set(_PRESENTATION_ONLY) | _scoped("deck-specific")
    if profile == "comic":
        skips |= _KNOWLEDGE_CANVAS_AESTHETICS
        skips -= _scoped("comic-specific")  # admit the comic-domain traps
    else:
        skips |= _scoped("comic-specific")
    return skips


def _resolve_profile(profile: str | None, all_traps: bool) -> str:
    """``--all-traps`` is the pre-H6 spelling of ``--profile all``."""
    if profile is not None:
        return profile
    return "all" if all_traps else DEFAULT_PROFILE


def _detect_vault_root(canvas_path: str) -> str | None:
    """Walk up from the canvas file to the nearest dir containing `.obsidian`."""
    current = os.path.dirname(os.path.abspath(canvas_path))
    while True:
        if os.path.isdir(os.path.join(current, ".obsidian")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            return None
        current = parent


def _finding_dict(f: TrapFinding) -> dict:
    return {
        "trap_id": f.trap_id,
        "condition": f.condition,
        "node_ids": f.node_ids,
        "severity": f.severity,
        "message": f.message,
    }


def check_canvas(
    canvas_path: str,
    vault_root: str | None = None,
    all_traps: bool = False,
    profile: str | None = None,
) -> tuple[list[TrapFinding], str | None]:
    """Run the trap pack against one canvas file.

    Returns ``(findings, resolved_vault_root)``. Raises ``OSError`` /
    ``ValueError`` on unreadable input.

    ``profile`` selects the trap set (``knowledge-canvas`` default · ``comic``
    · ``all``); see ``_profile_skips``. ``all_traps=True`` is the pre-H6
    spelling of ``profile="all"`` and is honored when ``profile`` is omitted.
    """
    profile = _resolve_profile(profile, all_traps)
    if profile not in PROFILES:
        raise ValueError(
            f"unknown profile {profile!r} (expected one of {', '.join(PROFILES)})"
        )
    with open(canvas_path, encoding="utf-8") as fh:
        canvas_data = json.load(fh)
    root = vault_root or _detect_vault_root(canvas_path)
    kwargs: dict = {}
    if root:
        # vault_root: file-node resolution (CV-FILE-PROPS-01);
        # asset_root: image-source resolution (CV-IMAGE-ASPECT-RATIO-01).
        # The runner filters per-trap by signature, so both are safe to send.
        kwargs["vault_root"] = root
        kwargs["asset_root"] = root
    findings = run_all_traps(canvas_data, **kwargs)
    skips = _profile_skips(profile)
    if skips:
        findings = [f for f in findings if f.trap_id not in skips]
    return findings, root


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="canvas-visual-check",
        description=(
            "Visual-fidelity check for .canvas files (Obsidian-calibrated "
            "geometry traps). Sibling of `canvas-std validate`, which checks "
            "schema only."
        ),
    )
    parser.add_argument("paths", nargs="+", metavar="file.canvas")
    parser.add_argument(
        "--vault-root",
        default=None,
        help="vault root for file/image resolution (default: auto-detect via .obsidian)",
    )
    parser.add_argument(
        "--json", action="store_true", dest="as_json",
        help="machine-readable output",
    )
    parser.add_argument(
        "--strict", action="store_true",
        help="medium-severity findings also fail the run",
    )
    parser.add_argument(
        "--profile", choices=PROFILES, default=None,
        help=(
            f"trap set to run (default: {DEFAULT_PROFILE}). 'comic' drops the "
            "knowledge-canvas aesthetic traps (padding/hierarchy/density) that "
            "a composed comic page fails by design, and admits comic-domain "
            "traps; correctness traps run under every profile. 'all' runs the "
            "full pack."
        ),
    )
    parser.add_argument(
        "--all-traps", action="store_true", dest="all_traps",
        help="deprecated alias for --profile all",
    )
    args = parser.parse_args(argv)

    try:
        profile = _resolve_profile(args.profile, args.all_traps)
    except ValueError as exc:  # pragma: no cover - argparse validates choices
        print(f"canvas-visual-check: {exc}", file=sys.stderr)
        return 2

    fail_severities = _FAIL_SEVERITIES | ({"medium"} if args.strict else set())
    skips = _profile_skips(profile)
    n_traps = sum(
        1 for trap_id, meta in TRAP_PACK_REGISTRY.items()
        if meta.get("status") in ("implemented", "graduated")
        and meta.get("module")
        and trap_id not in skips
    )

    reports = []
    worst_exit = 0
    for path in args.paths:
        try:
            findings, root = check_canvas(
                path, vault_root=args.vault_root, profile=profile,
            )
        except (OSError, ValueError) as exc:
            if args.as_json:
                reports.append({"canvas": path, "error": str(exc)})
            else:
                print(f"canvas-visual-check: {path}\n  ERROR  {exc}\n", file=sys.stderr)
            worst_exit = max(worst_exit, 2)
            continue

        counts = {sev: 0 for sev in _SEVERITY_ORDER}
        for f in findings:
            counts[f.severity] = counts.get(f.severity, 0) + 1
        failed = any(f.severity in fail_severities for f in findings)
        worst_exit = max(worst_exit, 1 if failed else 0)

        reports.append({
            "canvas": path,
            "vault_root": root,
            "profile": profile,
            "traps_run": n_traps,
            "findings": [_finding_dict(f) for f in findings],
            "counts": counts,
            "ok": not failed,
        })

        if not args.as_json:
            print(f"canvas-visual-check: {path}")
            print(f"  {n_traps} traps run (profile={profile})"
                  + (f", vault_root={root}" if root
                     else "  (no vault root — file-resolution traps skipped)"))
            for sev in _SEVERITY_ORDER:
                for f in findings:
                    if f.severity != sev:
                        continue
                    ids = ",".join(f.node_ids[:4]) + ("…" if len(f.node_ids) > 4 else "")
                    print(f"  [{sev.upper():>8}] {f.trap_id}/{f.condition} {ids}: {f.message}")
            summary = " / ".join(f"{counts[s]} {s}" for s in _SEVERITY_ORDER if counts[s])
            print(f"  {len(findings)} finding(s)" + (f" ({summary})" if summary else "")
                  + f" [{'FAIL' if failed else 'OK'}]")
            if not failed:
                print("  Visual fit passes. Schema conformance is a separate check "
                      "(canvas-std validate);")
                print("  and neither substitutes for looking at the rendered canvas.")
            print()

    if args.as_json:
        print(json.dumps(reports if len(reports) > 1 else reports[0], indent=2))
    return worst_exit


if __name__ == "__main__":
    sys.exit(main())
