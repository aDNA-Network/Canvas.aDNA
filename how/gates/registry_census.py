#!/usr/bin/env python3
"""registry_census — enumerate every hand-maintained vocabulary registry in `canvas_std`.

Operation Datum P1. The question this answers is NOT "do the registries agree?" (that is P3) but the
prior one: **what registries are there, and which of them is read by anything?**

⛔ THE ONE RULE THIS FILE MUST NOT BREAK. It may not contain a hand-written list of registries, nor a
hand-written map from a Python constant to its schema twin. Either would make this script the fourth
instance of the exact defect it was written to measure — a registry maintained by hand, checked
against another registry maintained by hand. Everything here is DERIVED:

  * the Python constants      -> by walking the AST of every module in the package
  * the schema enums          -> by traversing the schema JSON for every `enum` node
  * the spec's reserved keys  -> by parsing the fenced block under spec §7.2
  * the validator's dispatch  -> by walking the AST for `reserved`-subscript/`.get()` sites
  * PAIRING python <-> schema -> by SET CONTENT, never by name

That last one is the load-bearing choice. Pairing by name would need a mapping table (`VALID_SIDES` ->
`/$defs/edge/properties/fromSide`) and that table is precisely a hand-maintained registry with no
consumer. Pairing by content needs nothing maintained: two vocabularies are twins if they say the same
thing. It also gives the drift signal for free — a pair that overlaps but is not equal is exactly the
shape a drifted copy has, and it is reported as PARTIAL rather than silently left unpaired.

Sibling of `gate_manifest.py`, and it inherits both of that file's hard-won traps:
  * every path is absolute and this script NEVER chdir()s (a persisted `cd` makes a relative probe
    return empty, which is indistinguishable from a clean result);
  * discovery walks the disk, because a registry that is only ever read cannot report what was never
    written into it (F-GM-1).

Usage:
    python3 how/gates/registry_census.py            # human table
    python3 how/gates/registry_census.py --json     # machine-readable, for P2/P3 to consume
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# --- absolute paths only; this script never chdir()s (gate_manifest.py's trap) ----------------
VAULT = Path(__file__).resolve().parent.parent.parent
PKG = VAULT / "what" / "code" / "canvas_std" / "src" / "canvas_std"
SCHEMA = PKG / "data" / "adna_canvas_v2.schema.json"
SPEC = VAULT / "what" / "specs" / "spec_adna_canvas_standard.md"

EXIT_OK, EXIT_DRIFT, EXIT_PRECONDITION = 0, 1, 4

# A vocabulary constant is module-level, UPPER_SNAKE, and holds a literal collection of scalars.
# This is a SHAPE test, not a name list — a new constant of the same shape is picked up automatically.
_UPPER_SNAKE = re.compile(r"^[A-Z][A-Z0-9_]*$")


@dataclass
class PyRegistry:
    """A module-level vocabulary constant found by walking the AST."""

    name: str
    module: str
    lineno: int
    members: frozenset[Any]
    kind: str  # 'frozenset' | 'tuple' | 'set'
    ordered: tuple[Any, ...]  # tuples carry order; kept because order is meaning for some


@dataclass
class SchemaEnum:
    """An `enum` node in the JSON Schema, identified by its JSON pointer."""

    pointer: str
    members: frozenset[Any]


# ⛩ F-DT-2. Content-pairing needs a similarity floor, or it reports coincidence as drift.
#
# The first run of this script flagged three PARTIALs and ALL THREE WERE FALSE:
#   COMPONENT_CLASSES(14) vs node.type(4)  -> share {text, group, link}   jaccard 0.20
#   PL_FLOW(4)            vs toEnd(2)      -> share {none}                jaccard 0.20
#   PL_PAGINATION(3)      vs toEnd(2)      -> share {none}                jaccard 0.25
# Unrelated vocabularies collide on generic tokens — `none`, `text` — because natural vocabularies
# reuse words. That is not drift; it is English.
#
# DRIFT has a different shape: a copy of a vocabulary with a member or two changed, i.e. the two sets
# share most of their UNION. So the predicate is Jaccard |A∩B|/|A∪B| >= 0.5 — "a majority of everything
# either set says is said by both".
#
# Measured separation on the real corpus, both sides derived rather than asserted: coincidence tops out
# at **0.25** (PL_PAGINATION vs toEnd), and dropping one member from the 4-member VALID_SIDES scores
# **0.75** (3 shared / 4 union) and is correctly reported as DRIFT?. The floor is stated here rather
# than tuned until the output looked right — tuning it against the answer is `gate_manifest.py`'s
# "editing a disagreement into agreement" one level up.
#
# ⚠ The gap 0.25..0.75 is wide but it is an OBSERVATION about this corpus, not a guarantee. A future
# 2-member vocabulary sharing one token with a real twin would score 0.33 and be filed as coincidence.
# If that ever matters the answer is a named exception with a reason, not a nudged constant.
DRIFT_JACCARD_FLOOR = 0.5


@dataclass
class Pairing:
    """A python registry matched to zero or more schema enums BY CONTENT."""

    py: PyRegistry
    exact: list[SchemaEnum] = field(default_factory=list)
    partial: list[tuple[SchemaEnum, frozenset, frozenset]] = field(default_factory=list)
    coincident: list[tuple[SchemaEnum, frozenset]] = field(default_factory=list)

    @property
    def state(self) -> str:
        if self.exact:
            return "SCHEMA-TWIN"
        if self.partial:
            return "DRIFT?"
        return "VALIDATOR-ONLY"


# ---------------------------------------------------------------------------
# 1. The Python side — walk the AST of every module in the package.
# ---------------------------------------------------------------------------
def _literal(node: ast.AST) -> Any:
    """Return the literal value of a node, or raise ValueError if it is not a literal."""
    return ast.literal_eval(node)


def _collection_members(value: ast.AST) -> tuple[str, tuple[Any, ...]] | None:
    """If `value` is a literal collection of scalars (or frozenset(...) of one), return (kind, items).

    Handles the three shapes the package actually uses, recognised STRUCTURALLY:
        frozenset({...})  ·  frozenset([...])  ·  ("a", "b")  ·  {"a", "b"}
    """
    # frozenset(<literal collection>)
    if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == "frozenset":
        if len(value.args) != 1:
            return None
        try:
            return "frozenset", tuple(_literal(value.args[0]))
        except (ValueError, TypeError):
            return None
    if isinstance(value, (ast.Tuple, ast.Set, ast.List)):
        try:
            items = tuple(_literal(value))
        except (ValueError, TypeError):
            return None
        # Only scalar vocabularies. A tuple of dicts/tuples is data, not a vocabulary.
        if any(isinstance(i, (dict, list, tuple, set)) for i in items):
            return None
        kind = {ast.Tuple: "tuple", ast.Set: "set", ast.List: "list"}[type(value)]
        return kind, items
    return None


def collect_py_registries() -> list[PyRegistry]:
    """Every module-level UPPER_SNAKE literal-collection constant in the package. Derived, not listed."""
    found: list[PyRegistry] = []
    for path in sorted(PKG.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in tree.body:  # module level ONLY — a constant inside a function is not a registry
            targets: list[str] = []
            value: ast.AST | None = None
            if isinstance(node, ast.Assign):
                targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
                value = node.value
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                targets = [node.target.id]
                value = node.value
            if not targets or value is None:
                continue
            for name in targets:
                if not _UPPER_SNAKE.match(name):
                    continue
                got = _collection_members(value)
                if got is None:
                    continue
                kind, items = got
                found.append(
                    PyRegistry(
                        name=name,
                        module=str(path.relative_to(PKG)),
                        lineno=node.lineno,
                        members=frozenset(items),
                        kind=kind,
                        ordered=items,
                    )
                )
    return found


# ---------------------------------------------------------------------------
# 2. The schema side — traverse for every `enum`, plus $defs.reserved.properties.
# ---------------------------------------------------------------------------
def collect_schema_enums(schema: dict) -> list[SchemaEnum]:
    out: list[SchemaEnum] = []

    def walk(obj: Any, pointer: str) -> None:
        if isinstance(obj, dict):
            if "enum" in obj and isinstance(obj["enum"], list):
                out.append(SchemaEnum(pointer=pointer or "/", members=frozenset(obj["enum"])))
            for k, v in obj.items():
                walk(v, f"{pointer}/{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{pointer}/{i}")

    walk(schema, "")
    return out


def schema_reserved_properties(schema: dict) -> frozenset[str]:
    return frozenset(schema.get("$defs", {}).get("reserved", {}).get("properties", {}).keys())


def schema_reserved_is_open(schema: dict) -> bool:
    """§7.3 requires unknown keys be preserved, which requires this object stay OPEN. Asserted, not assumed."""
    return "additionalProperties" not in schema.get("$defs", {}).get("reserved", {})


# ---------------------------------------------------------------------------
# 3. The spec side — parse the fenced block under §7.2.
# ---------------------------------------------------------------------------
def spec_reserved_keys() -> frozenset[str]:
    """Keys listed in the fenced `_reserved:` block under spec §7.2. Parsed, not transcribed."""
    text = SPEC.read_text(encoding="utf-8")
    m = re.search(r"^7\.2\..*?^```\n(.*?)^```", text, re.MULTILINE | re.DOTALL)
    if not m:
        raise SystemExit("precondition: could not locate the fenced §7.2 block in spec_adna_canvas_standard.md")
    body = m.group(1)
    # Inside the block the shape is `  <key>: <anything>` at exactly one indent level under `_reserved:`.
    return frozenset(re.findall(r"^  ([a-z_][a-z0-9_]*):", body, re.MULTILINE))


# ---------------------------------------------------------------------------
# 4. The validator's dispatch sites — what keys does the code actually branch on?
# ---------------------------------------------------------------------------
def collect_dispatch_keys() -> tuple[dict[str, list[str]], list[str]]:
    """Every literal key the validators read off a `reserved` mapping, plus the sites it CANNOT read.

    Recognises, structurally:
        `"k" in reserved`  ·  `"k" not in reserved`  ·  `reserved.get("k")`  ·  `reserved["k"]`

    ⛩ F-DT-1 — BOTH of this function's blind spots were found by running it, not by reading it, and
    both are recorded here because the second one cannot be closed:

    1. **`not in` was missing.** The first version matched only ``ast.In``, so it did not see
       ``if "authority" in reserved and "production" not in reserved`` (reserved.py:183) and reported
       **9** dispatched keys where at least 10 exist. Fixed — ``ast.NotIn`` is now matched.

    2. **Dynamically-keyed dispatch is invisible, permanently.** ``_validate_axes`` iterates a literal
       tuple — ``for key, allowed in (("authority", AUTHORITY_VALUES), ("production", ...))`` — and then
       does ``reserved[key]`` with a VARIABLE. No AST walk can name that key without executing the code.
       Such sites are counted and returned as ``dynamic``: the number is reported on the face of the
       result so the key list is never mistaken for complete.

    ⇒ ***A detector's population is defined by its own membership rule*** — the P3-`federation_index`
    finding, reproduced inside the tool written to measure that family. The remedy is not a cleverer
    walker; it is reporting the blind spot's SIZE next to the count, which is what `dynamic` is for.
    """
    hits: dict[str, list[str]] = {}
    dynamic: list[str] = []
    targets = {"reserved"}
    for path in sorted(PKG.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for fn in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            where = f"{path.relative_to(PKG)}::{fn.name}"
            for node in ast.walk(fn):
                key: str | None = None
                obj: ast.AST | None = None
                static = True
                if isinstance(node, ast.Compare) and len(node.ops) == 1 and isinstance(node.ops[0], (ast.In, ast.NotIn)):
                    obj = node.comparators[0]
                    if isinstance(node.left, ast.Constant) and isinstance(node.left.value, str):
                        key = node.left.value
                    else:
                        static = False
                elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "get":
                    obj = node.func.value
                    if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                        key = node.args[0].value
                    else:
                        static = False
                elif isinstance(node, ast.Subscript):
                    obj = node.value
                    if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
                        key = node.slice.value
                    else:
                        static = False
                if not isinstance(obj, ast.Name) or obj.id not in targets:
                    continue
                if not static or key is None:
                    site = f"{where}:{node.lineno}"
                    if site not in dynamic:
                        dynamic.append(site)
                    continue
                hits.setdefault(key, [])
                if where not in hits[key]:
                    hits[key].append(where)
    return hits, dynamic


# ---------------------------------------------------------------------------
# 5. Pairing — BY CONTENT. No name map, because a name map is the defect.
# ---------------------------------------------------------------------------
def pair(py_regs: list[PyRegistry], enums: list[SchemaEnum]) -> list[Pairing]:
    pairings: list[Pairing] = []
    for reg in py_regs:
        p = Pairing(py=reg)
        for en in enums:
            if en.members == reg.members:
                p.exact.append(en)
                continue
            shared = en.members & reg.members
            if not shared:
                continue
            jaccard = len(shared) / len(en.members | reg.members)
            if jaccard >= DRIFT_JACCARD_FLOOR:
                p.partial.append((en, reg.members - en.members, en.members - reg.members))
            else:
                p.coincident.append((en, shared))
        pairings.append(p)
    return pairings


def duplicate_registries(py_regs: list[PyRegistry]) -> list[tuple[frozenset, list[PyRegistry]]]:
    """Distinct constants holding IDENTICAL content — two hand-maintained copies of one vocabulary.

    Both copies can be perfectly correct and this is still the campaign's target: nothing links them,
    so nothing fails when one moves. Reported, never auto-merged — whether two identical vocabularies
    are *one* vocabulary is a semantic question a set comparison cannot answer.
    """
    by_content: dict[frozenset, list[PyRegistry]] = {}
    for r in py_regs:
        by_content.setdefault(r.members, []).append(r)
    return [(k, v) for k, v in by_content.items() if len(v) > 1]


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    for p in (PKG, SCHEMA, SPEC):
        if not p.exists():
            print(f"precondition FAULT: {p} does not exist", file=sys.stderr)
            return EXIT_PRECONDITION

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    py_regs = collect_py_registries()
    enums = collect_schema_enums(schema)
    pairings = pair(py_regs, enums)
    dispatch, dynamic_sites = collect_dispatch_keys()
    dupes = duplicate_registries(py_regs)

    reserved_py = next((r for r in py_regs if r.name == "RESERVED_KEYS"), None)
    reserved_schema = schema_reserved_properties(schema)
    reserved_spec = spec_reserved_keys()
    reserved_tuple = frozenset(reserved_py.members) if reserved_py else frozenset()

    # The three-way `_reserved` namespace comparison — the F-GL-1 surface.
    three_way = {
        "python_RESERVED_KEYS": sorted(reserved_tuple),
        "schema_properties": sorted(reserved_schema),
        "spec_7_2": sorted(reserved_spec),
        "all_agree": reserved_tuple == reserved_schema == reserved_spec,
        "in_python_not_schema": sorted(reserved_tuple - reserved_schema),
        "in_schema_not_python": sorted(reserved_schema - reserved_tuple),
        "in_spec_not_python": sorted(reserved_spec - reserved_tuple),
        "in_python_not_spec": sorted(reserved_tuple - reserved_spec),
        "reserved_object_is_open": schema_reserved_is_open(schema),
    }
    # Dispatch keys that are NOT in the namespace registries — the F-GL-1 mechanism, generalised.
    dispatched = frozenset(dispatch)
    undeclared = sorted(dispatched - reserved_tuple)

    if args.json:
        print(json.dumps({
            "python_registries": [
                {"name": r.name, "module": r.module, "line": r.lineno, "kind": r.kind,
                 "members": sorted(map(str, r.members))} for r in py_regs
            ],
            "schema_enums": [{"pointer": e.pointer, "members": sorted(map(str, e.members))} for e in enums],
            "pairings": [
                {"name": p.py.name, "state": p.state,
                 "exact": [e.pointer for e in p.exact],
                 "partial": [{"pointer": e.pointer, "only_in_python": sorted(map(str, a)),
                              "only_in_schema": sorted(map(str, b))} for e, a, b in p.partial]}
                for p in pairings
            ],
            "reserved_namespace": three_way,
            "dispatch_sites": dispatch,
            "dispatch_dynamic_sites": dynamic_sites,
            "dispatched_but_undeclared": undeclared,
            "duplicate_registries": [
                {"members": sorted(map(str, k)), "constants": [f"{r.module}::{r.name}" for r in v]}
                for k, v in dupes
            ],
        }, indent=2))
        return EXIT_OK if three_way["all_agree"] and not undeclared else EXIT_DRIFT

    print(f"registry census — package {PKG.relative_to(VAULT)}\n")
    print(f"population: {len(py_regs)} python vocabulary constants across "
          f"{len({r.module for r in py_regs})} modules · {len(enums)} schema enums\n")

    w = max(len(r.name) for r in py_regs)
    print(f"{'constant':<{w}}  {'kind':<10} {'state':<15} schema twin (matched BY CONTENT)")
    print("-" * (w + 75))
    for p in sorted(pairings, key=lambda q: (q.state, q.py.name)):
        twin = ", ".join(e.pointer.replace("/$defs/", "").replace("/properties/", ".") for e in p.exact)
        if p.state == "DRIFT?":
            twin = "; ".join(
                f"{e.pointer} (py-only {sorted(map(str, a))} · schema-only {sorted(map(str, b))})"
                for e, a, b in p.partial
            )
        elif not twin and p.coincident:
            # Only worth printing when there is no real twin — otherwise it buries the answer under
            # the noise. (It did exactly that on the first run of this reporter.)
            shared_tokens = sorted({str(t) for _, s in p.coincident for t in s})
            twin = (f"— (no twin; {len(p.coincident)} enum(s) share {shared_tokens} but fall below the "
                    f"{DRIFT_JACCARD_FLOOR} drift floor — unrelated vocabularies reusing a generic token)")
        print(f"{p.py.name:<{w}}  {p.py.kind:<10} {p.state:<15} {twin or '—'}")

    if dupes:
        print(f"\n--- identical vocabularies held under {len(dupes)} distinct constant(s) ---")
        for members, regs in dupes:
            print(f"  {sorted(map(str, members))}")
            for r in regs:
                print(f"      {r.module}:{r.lineno}  {r.name}")
            print("      ⚠ both copies may be correct; nothing links them, so nothing fails when one moves")

    print(f"\n--- the `_reserved` namespace, three hand-maintained copies (F-GL-1's surface) ---")
    print(f"  python RESERVED_KEYS   {len(reserved_tuple):>2} keys")
    print(f"  schema properties      {len(reserved_schema):>2} keys")
    print(f"  spec §7.2              {len(reserved_spec):>2} keys")
    print(f"  ALL THREE AGREE:       {three_way['all_agree']}")
    for label, keyname in (("python-not-schema", "in_python_not_schema"),
                           ("schema-not-python", "in_schema_not_python"),
                           ("spec-not-python", "in_spec_not_python"),
                           ("python-not-spec", "in_python_not_spec")):
        if three_way[keyname]:
            print(f"    ⛔ {label}: {three_way[keyname]}")
    print(f"  $defs.reserved is OPEN (§7.3 forward-compat): {three_way['reserved_object_is_open']}")

    print(f"\n--- what the validators actually dispatch on "
          f"({len(dispatch)} statically-derivable keys + {len(dynamic_sites)} dynamic site(s)) ---")
    for k in sorted(dispatch):
        mark = " ⛔ NOT IN RESERVED_KEYS" if k not in reserved_tuple else ""
        print(f"  {k:<22} {', '.join(dispatch[k])}{mark}")
    if dynamic_sites:
        print(f"  ⚠ {len(dynamic_sites)} dispatch site(s) key off a VARIABLE and cannot be named by any AST walk:")
        for s in dynamic_sites:
            print(f"      {s}")
        print("      ⇒ the key list above is a FLOOR, not a census. Reported so it is never read as complete.")
    declared_not_dispatched = sorted(reserved_tuple - dispatched)
    if declared_not_dispatched:
        print(f"  ⓘ declared but not statically dispatched: {declared_not_dispatched}")

    drift = (not three_way["all_agree"]) or bool(undeclared) or any(p.state == "DRIFT?" for p in pairings)
    print(f"\n{'⛔ DRIFT FOUND' if drift else 'no drift between the derived populations'}")
    return EXIT_DRIFT if drift else EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
