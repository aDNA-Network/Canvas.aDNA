#!/usr/bin/env python3
"""sync_semantics_census — what would LIP-0011 break? (Operation Vernier P2b, objective 4)

LIP-0011 turns three P2 verdicts into the Standard (record: `how/gates/vernier_p1_exit_20261012.output.json`):

  V-1 (b)  `sync.sync_hash` stays the 16-hex TOPOLOGY digest (`canvas_std.roundtrip.compute_sync_hash`) and the
           Standard registers `sync.source_sha256` (64 lowercase hex, sha256 of the source document's bytes).
           A-6 additions: `source_sha256` well-formed when present; when `production: generated`, the topology is
           recomputed and compared — ADVISORY at both tiers (**D-1 (i), signed 2026-10-15** at
           `how/gates/lip_0011_signature_20261015`). The unsigned alternative, D-1 (ii) (HARD at `adna_native`), is
           still counted, on one informational line, so the price of hardening later stays measured.
  V-2      A-8 (`_validate_axes`) runs at `extended` too, whenever a `_reserved` block is present.
  V-3      `sync.generator` (non-empty string: a path or URN) registered as the provenance carrier.

The mission's exit gate asks for "0 new failures" and says the claim is MEASURED, not asserted (F-GL-6 — LIP-0010's
"25 of 25 keep passing" measured 23 of 25). This script is that measurement. It is run before the LIP is signed and
again at the firewall touch, and its output is pasted into the LIP, never retyped.

⛔ How the two sides are computed, because a census is only as good as its predicates:
  * CURRENT verdict = the REAL `canvas_std.validate.validate(doc, <declared level>)`, imported from this vault's own
    source tree (never an installed copy). Undeclared level → `core`, as the CLI does.
  * PROPOSED verdict = the current error list PLUS the candidate rules above, evaluated here, outside the firewall,
    because the firewall does not move before the §7.7 signature. The A-8 leg reuses the real `_validate_axes`; the
    topology leg reuses the real `compute_sync_hash`. Only the two format rules are new code, and they are four lines.
  * NEW FAILURE = passes CURRENT and fails PROPOSED. A canvas that already fails is not a new failure, and its
    current errors are printed so nobody counts it as one.

Population (stated on the face of every number): every `.canvas` under a non-symlink top-level directory of ~/aDNA
(`llama.cpp` excluded; `find -P`; prunes .git node_modules .venv __pycache__ .obsidian) that carries a `_reserved`
block — with or without `sync`, because V-2's leg (A-8 at `extended`) does not need one — at the canonical
`metadata.frontmatter._reserved`, plus the non-canonical `metadata._reserved`, reported separately because the
validator does not read it at all.

Inherits gate_manifest.py's traps: absolute paths only, never chdir()s.

After the firewall touch the real validator already contains the signed rules, so CURRENT == PROPOSED and "new
failures" reads 0 by construction. The post-touch claim is therefore made with `--baseline`: save `--json` BEFORE the
touch, re-run AFTER it with `--baseline <that file>`, and the script prints every canvas whose REAL-validator verdict
changed. The signed claim is that exactly one changes (PercySleep `percy_topology.canvas`, the V-2 price). Where the
installed validator exposes `advisories()`, its advisory set is cross-checked against this script's candidate set.

Usage:
    python3 how/gates/sync_semantics_census.py          # summary · per-implementer table · new-failure list
    python3 how/gates/sync_semantics_census.py --json   # machine-readable
    python3 how/gates/sync_semantics_census.py --baseline pre.json   # + verdict changes since a saved --json run
Exit: 0 = no new failures · 1 = at least one new failure (the LIP must say so) · 4 = precondition fault.
"""

from __future__ import annotations

import argparse
import collections
import datetime as _dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

VAULT = Path(__file__).resolve().parent.parent.parent
SRC = VAULT / "what" / "code" / "canvas_std" / "src"
ROOT = VAULT.parent  # ~/aDNA
EXCLUDE_TOPS = {"llama.cpp"}
PRUNE = {".git", "node_modules", ".venv", "__pycache__", ".obsidian"}
# The implementers V-1 named, by top-level directory. Everything else is "other".
IMPLEMENTERS = ("Terminal.aDNA", "City.aDNA", "LatticeProtocol.aDNA", "Home.aDNA", "Canvas.aDNA")

sys.path.insert(0, str(SRC))  # the in-tree validator, never an installed copy
try:
    import importlib  # noqa: E402

    # The MODULE, by name: `from canvas_std import validate` returns the re-exported FUNCTION, which shadows the
    # submodule — and a hasattr() probe on the function is silently always False (caught on the first post-touch run).
    _validate_mod = importlib.import_module("canvas_std.validate")  # noqa: E402
    from canvas_std.reserved import _validate_axes  # noqa: E402
    from canvas_std.roundtrip import compute_sync_hash  # noqa: E402
    from canvas_std.validate import ConformanceLevel, validate  # noqa: E402
except Exception as exc:  # pragma: no cover - precondition
    print(f"precondition fault: cannot import in-tree canvas_std from {SRC}: {exc}", file=sys.stderr)
    sys.exit(4)

_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_LEVELS = {lv.value: lv for lv in ConformanceLevel}


def _proposed_extra(r: dict, doc: dict, level: str, d1: str = "i") -> tuple[list[str], list[str], bool | None]:
    """LIP-0011 rules → (hard errors, advisories, topology_match-or-None). ``d1`` = "i" (signed) or "ii" (counted)."""
    hard: list[str] = []
    adv: list[str] = []
    sync = r.get("sync") if isinstance(r.get("sync"), dict) else {}
    if level not in ("extended", "adna_native"):
        return hard, adv, None  # core: no _reserved check runs, before or after
    if "source_sha256" in sync and not (isinstance(sync["source_sha256"], str) and _HEX64.match(sync["source_sha256"])):
        hard.append(f"A-6: sync.source_sha256 {sync['source_sha256']!r} is not 64 lowercase hex")
    if "generator" in sync and not (isinstance(sync["generator"], str) and sync["generator"].strip()):
        hard.append(f"A-6: sync.generator {sync['generator']!r} is not a non-empty string")
    if level == "extended":
        hard += _validate_axes(r)  # V-2 — at adna_native it already runs inside the current validator
    topo = None
    if isinstance(sync.get("sync_hash"), str):
        topo = sync["sync_hash"] == compute_sync_hash(doc)
    if r.get("production") == "generated" and topo is False:
        msg = "A-6: sync.sync_hash does not match the recomputed topology (production: generated)"
        (hard if (d1 == "ii" and level == "adna_native") else adv).append(msg)
    return hard, adv, topo


def _builder_hash(doc: dict) -> str:
    """`canvas_core.CanvasBuilder.compute_sync_hash`, reproduced to CLASSIFY, never to validate (F-V-10).

    A SECOND topology encoding inside Canvas's own production code: the same sorted ids and `from->to` pairs,
    serialised as `json.dumps({"nodes": [...], "edges": [...]}, sort_keys=True)` instead of joined with U+0001/U+0002. Same
    topology, different digest. Kept here only so the census can name which encoding a mismatch carries.
    """
    import hashlib
    topo = {
        "nodes": sorted(str(n["id"]) for n in doc.get("nodes", []) if isinstance(n, dict) and "id" in n),
        "edges": sorted(f"{e.get('fromNode')}->{e.get('toNode')}" for e in doc.get("edges", []) if isinstance(e, dict)),
    }
    return hashlib.sha256(json.dumps(topo, sort_keys=True).encode()).hexdigest()[:16]


def _encoding(sync: dict, doc: dict) -> str:
    sh = sync.get("sync_hash")
    if not isinstance(sh, str):
        return "no sync_hash"
    if sh == compute_sync_hash(doc):
        return "canvas_std topology"
    if sh == _builder_hash(doc):
        return "CanvasBuilder topology (json)"
    return "neither (source bytes, stale, or hand-set)"


def _head(top: Path) -> str:
    try:
        out = subprocess.run(["git", "-C", str(top), "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, timeout=10)
        return out.stdout.strip() or "-"
    except Exception:
        return "-"


def census() -> dict:
    c: collections.Counter = collections.Counter()
    symlinks: list[str] = []
    rows: list[dict] = []
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
                c["_reserved carriers"] += 1
                has_sync = isinstance(r.get("sync"), dict)
                c["  of which carry sync"] += has_sync
                lvl = r.get("conformance_level") if r.get("conformance_level") in _LEVELS else "core"
                cur = validate(d, _LEVELS[lvl]) if where == "canonical" else validate(d, ConformanceLevel.CORE)
                hard, adv, topo = _proposed_extra(r, d, lvl) if where == "canonical" else ([], [], None)
                hard_ii = _proposed_extra(r, d, lvl, "ii")[0] if where == "canonical" else []
                real_adv = None  # the installed validator's own advisories, once the touch exposes them
                if where == "canonical" and hasattr(_validate_mod, "advisories"):
                    real_adv = _validate_mod.advisories(d, _LEVELS[lvl])
                sync = r["sync"] if has_sync else {}
                rows.append({
                    "has_sync": has_sync, "encoding": _encoding(sync, d),
                    "path": str(fp.relative_to(ROOT)), "top": top, "level": lvl, "where": where,
                    "production": r.get("production"), "authority": r.get("authority"),
                    "has_source_sha256": "source_sha256" in sync, "has_generator": "generator" in sync,
                    "has_top_generator": "generator" in r, "topology_match": topo,
                    "current_ok": not cur, "current_errors": cur,
                    "proposed_ok": not cur and not hard, "proposed_hard": hard, "advisories": adv,
                    "proposed_ok_d1_ii": not cur and not hard_ii, "real_advisories": real_adv,
                })
    heads = {t: _head(ROOT / t) for t in IMPLEMENTERS if (ROOT / t).is_dir()}
    return {"counts": dict(c), "symlinks_skipped": symlinks, "rows": rows, "heads": heads}


def _bucket(top: str) -> str:
    return top if top in IMPLEMENTERS else "other"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--baseline", type=Path, help="a saved --json run; print real-validator verdict changes since it")
    a = ap.parse_args()
    res = census()
    res["measured_at"] = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    res["population"] = (f"{ROOT}/*/**/*.canvas with a _reserved block (non-symlink tops, -P, "
                         f"excl. {sorted(EXCLUDE_TOPS)})")
    rows = res["rows"]
    new = [x for x in rows if x["current_ok"] and not x["proposed_ok"]]
    if a.json:
        print(json.dumps(res, indent=2))
        return 1 if new else 0

    print(f"sync_semantics_census  {res['measured_at']}  {res['population']}")
    print(f"  symlinked tops skipped: {len(res['symlinks_skipped'])}")
    for k, v in sorted(res["counts"].items()):
        print(f"  {v:6d}  {k}")
    print("  HEADs: " + " · ".join(f"{t.removesuffix('.aDNA')} {h}" for t, h in res["heads"].items()))
    print("per implementer (_reserved carriers · level · current ok · proposed ok · topology match · "
          "source_sha256 · sync.generator · top-level generator · advisories):")
    grp: dict = collections.defaultdict(collections.Counter)
    for x in rows:
        g = grp[(_bucket(x["top"]), x["level"], x["where"])]
        g["n"] += 1
        g["cur"] += x["current_ok"]
        g["prop"] += x["proposed_ok"]
        g["topo"] += bool(x["topology_match"])
        g["src"] += x["has_source_sha256"]
        g["gen"] += x["has_generator"]
        g["tgen"] += x["has_top_generator"]
        g["adv"] += bool(x["advisories"])
    for (b, lvl, where), g in sorted(grp.items(), key=str):
        print(f"  {b:22s} {lvl:12s} {where:18s} n={g['n']:4d} cur={g['cur']:4d} prop={g['prop']:4d} "
              f"topo={g['topo']:4d} src256={g['src']:3d} sync.gen={g['gen']:3d} top.gen={g['tgen']:3d} "
              f"adv={g['adv']:3d}")
    enc = collections.Counter((_bucket(x["top"]), x["encoding"]) for x in rows if x["has_sync"])
    print("sync_hash encoding (which digest the stored value actually is):")
    for (b, e), n in sorted(enc.items(), key=str):
        print(f"  {n:6d}  {b:22s} {e}")
    gen_native = [x for x in rows if x["level"] == "adna_native" and x["production"] == "generated"]
    print(f"adna_native · production: generated: {len(gen_native)} · topology match "
          f"{sum(bool(x['topology_match']) for x in gen_native)} (the HARD leg's whole population)")
    print(f"LIP-0011 ⇒ passers today: {sum(x['current_ok'] for x in rows)} · "
          f"still pass under the proposal: {sum(x['current_ok'] and x['proposed_ok'] for x in rows)} · "
          f"NEW FAILURES: {len(new)}")
    for x in new:
        print(f"  ✗ {x['path']}  level={x['level']} production={x['production']!r} authority={x['authority']!r}")
        for e in x["proposed_hard"]:
            print(f"      {e[:150]}")
    new_ii = [x for x in rows if x["current_ok"] and not x["proposed_ok_d1_ii"]]
    print(f"  (informational: under the unsigned D-1 (ii) the count would be {len(new_ii)})")
    adv = [x for x in rows if x["advisories"]]
    print(f"advisories (warn, not fail): {len(adv)}")
    for x in adv:
        print(f"  ~ {x['path']}")
    if any(x["real_advisories"] is not None for x in rows):
        real = {x["path"] for x in rows if x["real_advisories"]}
        cand = {x["path"] for x in adv}
        print(f"real-validator advisories (canvas_std.advisories): {len(real)} · "
              f"{'agree with the candidate set' if real == cand else 'DISAGREE: ' + str(sorted(real ^ cand))}")
    if a.baseline:
        base = {x["path"]: x["current_ok"] for x in json.loads(a.baseline.read_text())["rows"]}
        changed = [x for x in rows if x["path"] in base and base[x["path"]] != x["current_ok"]]
        print(f"real-validator verdict changes since {a.baseline.name} ({len(base)} rows then, {len(rows)} now; "
              f"{sum(x['path'] not in base for x in rows)} new paths, not compared): {len(changed)}")
        for x in changed:
            print(f"  {'✓→✗' if base[x['path']] else '✗→✓'} {x['path']}")
            for e in x["current_errors"]:
                print(f"      {e[:150]}")
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main())
