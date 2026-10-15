#!/usr/bin/env python3
"""axis_tier_census — what would A-8 break if it ran at `extended`? (Operation Vernier, V-2)

The question V-2 puts to the operator: A-8 (the `authority` / `production` axes, LIP-0010 Option D) runs
only at `adna_native`, so a correct pair on an `extended` canvas goes unchecked — and so does an invented
value. Moving A-8 down a tier is validate-if-present, so it cannot break a canvas that omits both keys;
it CAN break an `extended` canvas that carries a bad value. This script counts those, fleet-wide, before
the LIP is signed — the door's V-2 had read "unknown count today" until it ran.

⛔ It classifies with the REAL rule, `canvas_std.reserved._validate_axes`, imported from this vault's
own source tree (not whatever happens to be installed), and it ALSO evaluates the hand predicate the
first, throwaway version of this census used (2026-10-14, job tmp dir). The two must agree on every
carrier; a disagreement is printed as DISAGREE and makes the exit code 2. A census that re-implements a
rule by hand is a second copy of the rule, and a second copy is a second thing that can be wrong
(registry_census.py's one rule, one level up).

Scope, stated because a count is only as good as its population:
  * walks every top-level directory of ~/aDNA that is NOT a symlink (shims point at trees counted
    elsewhere, or at Archive) — skipped symlinks are counted and printed, `llama.cpp` excluded (external);
  * never follows symlinks below the top (os.walk followlinks=False, i.e. `find -P`);
  * prunes .git, node_modules, .venv, __pycache__, .obsidian;
  * finds `_reserved` at the canonical `metadata.frontmatter._reserved`, and ALSO at the non-canonical
    `metadata._reserved` — reported separately, since the validator does not read the latter at all.

Inherits gate_manifest.py's traps: absolute paths only, never chdir()s.

Usage:
    python3 how/gates/axis_tier_census.py           # table + the would-newly-fail list
    python3 how/gates/axis_tier_census.py --json    # machine-readable
"""

from __future__ import annotations

import argparse
import collections
import datetime as _dt
import json
import os
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent.parent
SRC = VAULT / "what" / "code" / "canvas_std" / "src"
ROOT = VAULT.parent  # ~/aDNA
EXCLUDE_TOPS = {"llama.cpp"}
PRUNE = {".git", "node_modules", ".venv", "__pycache__", ".obsidian"}

sys.path.insert(0, str(SRC))  # the in-tree validator, never an installed copy
from canvas_std.reserved import (  # noqa: E402
    AUTHORITY_VALUES,
    PRODUCTION_VALUES,
    _validate_axes,
)


def _hand_ok(r: dict) -> bool:
    """The 2026-10-14 throwaway predicate, kept verbatim so the cross-check means something."""
    a, pr = r.get("authority"), r.get("production")
    return ((a is None or a in AUTHORITY_VALUES) and (pr is None or pr in PRODUCTION_VALUES)
            and not (a is not None and pr is None))


def census() -> dict:
    c: collections.Counter = collections.Counter()
    symlinks: list[str] = []
    carriers: list[dict] = []
    for top in sorted(os.listdir(ROOT)):
        p = ROOT / top
        if top in EXCLUDE_TOPS or not p.is_dir():
            continue
        if p.is_symlink():
            symlinks.append(top)
            continue
        for dp, dn, fn in os.walk(p, followlinks=False):
            dn[:] = [d for d in dn if d not in PRUNE]
            for f in fn:
                if not f.endswith(".canvas"):
                    continue
                fp = Path(dp) / f
                c["files"] += 1
                try:
                    d = json.loads(fp.read_text(encoding="utf-8"))
                except Exception:
                    c["unparseable"] += 1
                    continue
                if not isinstance(d, dict):
                    continue
                md = d.get("metadata") if isinstance(d.get("metadata"), dict) else {}
                fm = md.get("frontmatter") if isinstance(md.get("frontmatter"), dict) else {}
                r, where = fm.get("_reserved"), "canonical"
                if not isinstance(r, dict):
                    r, where = md.get("_reserved"), "metadata._reserved"
                if not isinstance(r, dict):
                    continue
                lvl = r.get("conformance_level")
                c[f"reserved level={lvl} path={where}"] += 1
                if "authority" not in r and "production" not in r:
                    continue
                errs = _validate_axes(r)
                hand = _hand_ok(r)
                carriers.append({
                    "path": str(fp.relative_to(ROOT)), "level": lvl, "where": where,
                    "authority": r.get("authority"), "production": r.get("production"),
                    "ok": not errs, "errors": errs, "agree": hand == (not errs),
                })
    return {"counts": dict(c), "symlinks_skipped": symlinks, "carriers": carriers}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    res = census()
    res["measured_at"] = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    res["population"] = f"{ROOT}/*/**/*.canvas (non-symlink tops, -P, excl. {sorted(EXCLUDE_TOPS)})"
    dis = [x for x in res["carriers"] if not x["agree"]]
    if a.json:
        print(json.dumps(res, indent=2))
        return 2 if dis else 0

    print(f"axis_tier_census  {res['measured_at']}  {res['population']}")
    print(f"  symlinked tops skipped: {len(res['symlinks_skipped'])}")
    for k, v in sorted(res["counts"].items()):
        print(f"  {v:6d}  {k}")
    grp = collections.Counter((x["level"], x["where"], x["ok"]) for x in res["carriers"])
    print("axis carriers (level · path · valid under _validate_axes):")
    for (lvl, where, ok), n in sorted(grp.items(), key=str):
        print(f"  {n:6d}  level={lvl}  path={where}  ok={ok}")
    ext = [x for x in res["carriers"] if x["level"] == "extended" and x["where"] == "canonical"]
    bad = [x for x in ext if not x["ok"]]
    print(f"V-2 ⇒ extended (canonical) carriers: {len(ext)} · valid {len(ext) - len(bad)} · "
          f"would newly fail {len(bad)}")
    for x in bad:
        print(f"  ✗ {x['path']}  authority={x['authority']!r} production={x['production']!r}")
        for e in x["errors"]:
            print(f"      {e[:140]}")
    print(f"cross-check vs hand predicate: {len(res['carriers']) - len(dis)}/{len(res['carriers'])} agree")
    for x in dis:
        print(f"  DISAGREE {x['path']}")
    return 2 if dis else 0


if __name__ == "__main__":
    sys.exit(main())
