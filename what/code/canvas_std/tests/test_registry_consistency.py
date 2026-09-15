"""The `canvas_std` vocabulary registries have a consumer — this file.

Operation Datum **P2**, under the operator ruling of 2026-09-13 (a named firewall touch, the fourth
deliberate one since Keystone), **extended at P3** on 2026-09-15 (touch #5, the same both-legs
ruling): P2 gave the `_reserved` *namespace* a consumer; P3 gave **every vocabulary constant in the
package** one, by making each declare its relationship to the JSON Schema as a falsifiable claim.
The P3 family begins at `_declared_registries` below; F-DT-7 is why it is not optional.

## Why this file exists (F-GL-1, Gridline P1, 2026-09-11)

``canvas_std.reserved.RESERVED_KEYS`` names the ``_reserved`` namespace (spec §7.2). Until today it
was referenced **nowhere** — not in ``src/``, not in ``tests/``, not by any producer. When Standard
v2.4.0 appended ``authority`` and ``production`` to it per the ratified LIP-0010 Option D, the append
was **correct and inert.**

And the proof that an inert list rots was already inside it. ``interaction`` — shipped and validated by
``validate_interaction`` since Standard **v2.2.0** (Armature, 2026-06-23) — was missing from *all three*
hand-maintained copies of this namespace: this tuple, the JSON Schema's ``$defs.reserved.properties``,
and spec §7.2. For **three months**. Not one canvas was ever wrong; the *namespace description* was,
and nothing could notice, because §7.3 requires unknown ``_reserved`` keys be preserved — so an
unlisted key is not a validity fault **by design**.

    ⇒ a specification with no consumer is indistinguishable from no specification.

## What this file asserts, and what it must never become

It asserts the **reverse** direction, which is the cheap half and the one that catches the real defect:
**every key the validators actually dispatch on is declared in both machine-readable copies.** That is
what would have caught ``interaction`` in June.

⛔ It does **not** assert the forward direction — that every key on a document appears in
``RESERVED_KEYS``. Rejecting unknown ``_reserved`` keys would be a **major** version bump and would
break the single promise the ``_reserved`` carrier exists to make (§7.3 forward-compat). The
``$defs.reserved`` object is **open** by design, and :func:`test_reserved_object_stays_open` pins that
open-ness so a future tightening cannot happen by accident.

⛔ It does not check against a second hand-written list. The dispatched keys are **derived by walking
this package's own AST**. A list checked against a list is the defect above, wearing a test's clothes.

## Two honest limits, stated rather than papered over

1. **A static walk cannot see dynamically-keyed dispatch.** ``_validate_axes`` iterates a literal tuple
   and then subscripts ``reserved[key]`` with a *variable*. Those sites are counted and asserted to be
   a known quantity, so that the derived key list is never mistaken for a complete census
   (F-DT-1, Datum P1).
2. **This file deliberately duplicates part of ``how/gates/registry_census.py``'s AST walk**, and the
   duplication is named here rather than left silent. The package **must not** depend on the vault
   tree that contains it — a fork or a ``pip install adna-canvas-std`` has this file and no
   ``how/gates/``. The census additionally checks spec §7.2, which is a *vault* artifact and therefore
   correctly outside the package. ⇒ two scopes, two checks, one invariant; per F-DT-3 the rule is that
   a duplication is acceptable **when named with its reason** and not otherwise.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any

import pytest

from canvas_std import reserved as reserved_mod
from canvas_std import schema as schema_mod
from canvas_std.conformance import json_schema
from canvas_std.reserved import BASELINE_TYPES, RESERVED_KEYS
from canvas_std.schema import VALID_NODE_TYPES

PKG_DIR = Path(reserved_mod.__file__).resolve().parent

# A vocabulary constant is module-level, UPPER_SNAKE, and holds a literal collection of scalars.
# A SHAPE test, not a name list — a new constant of the same shape is picked up automatically, which
# is the whole point (F-GM-1: a registry that is only ever read cannot report what was never written
# into it).
_UPPER_SNAKE = re.compile(r"^[A-Z][A-Z0-9_]*$")

# The two states a vocabulary may declare. There is no third — "correct today, hand-maintained, read
# by nothing" is what Operation Datum exists to remove.
_STATES = ("SCHEMA-TWIN", "VALIDATOR-ONLY")

# The `_validate_axes` loop keys off a variable (`reserved[key]` where key is the loop target), so a
# static walk cannot name what it reads. This is the count of such sites at the time of writing. It is
# asserted rather than ignored: if it CHANGES, a new dynamic dispatch site has appeared and the derived
# key list below has silently become less complete than it was. That is a review trigger, not a failure
# of correctness — the message says so.
KNOWN_DYNAMIC_DISPATCH_SITES = 2


def _dispatch_keys() -> tuple[dict[str, set[str]], list[str]]:
    """Walk this package's AST for every literal key read off a mapping named ``reserved``.

    Recognised structurally — ``"k" in reserved`` · ``"k" not in reserved`` · ``reserved.get("k")`` ·
    ``reserved["k"]``. Returns (key -> {function names}, [dynamic site descriptions]).

    ⚠ ``ast.NotIn`` matters and was missed by the first version of the sibling walker: the axis check
    reads ``if "authority" in reserved and "production" not in reserved``, so matching only ``ast.In``
    sees the first key and is blind to the second (F-DT-1).
    """
    keys: dict[str, set[str]] = {}
    dynamic: list[str] = []
    for path in sorted(PKG_DIR.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for fn in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            for node in ast.walk(fn):
                key: str | None = None
                obj: ast.AST | None = None
                static = True
                if isinstance(node, ast.Compare) and len(node.ops) == 1 and isinstance(
                    node.ops[0], (ast.In, ast.NotIn)
                ):
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
                if not isinstance(obj, ast.Name) or obj.id != "reserved":
                    continue
                if not static or key is None:
                    dynamic.append(f"{path.name}::{fn.name}:{node.lineno}")
                    continue
                keys.setdefault(key, set()).add(f"{path.name}::{fn.name}")
    return keys, sorted(set(dynamic))


@pytest.fixture(scope="module")
def dispatched() -> dict[str, set[str]]:
    keys, _ = _dispatch_keys()
    # A walk that finds nothing would make every assertion below vacuously true — the F-P2-11 family
    # (*a check that cannot run is not a check that passes*). Fail loudly instead.
    assert keys, "the AST walk found no dispatch sites at all — the walker is broken, not the package"
    return keys


def test_every_dispatched_key_is_declared_in_reserved_keys(dispatched: dict[str, set[str]]) -> None:
    """The exact assertion that would have caught ``interaction`` in June."""
    undeclared = {k: sorted(v) for k, v in dispatched.items() if k not in RESERVED_KEYS}
    assert not undeclared, (
        "these _reserved keys are read by a validator but are NOT in RESERVED_KEYS: "
        f"{undeclared}. Append them to canvas_std.reserved.RESERVED_KEYS, to the JSON Schema's "
        "$defs.reserved.properties, and to spec_adna_canvas_standard §7.2 — all three are "
        "hand-maintained copies of one namespace (F-GL-1)."
    )


def test_every_dispatched_key_is_declared_in_the_json_schema(dispatched: dict[str, set[str]]) -> None:
    """The second machine-readable copy. It drifted from the first for three months."""
    properties = set(json_schema()["$defs"]["reserved"]["properties"])
    missing = {k: sorted(v) for k, v in dispatched.items() if k not in properties}
    assert not missing, (
        "these _reserved keys are read by a validator but are absent from the JSON Schema's "
        f"$defs.reserved.properties: {missing}. Note this is NOT a validity failure for any document "
        "— $defs.reserved is open by design (§7.3) — which is precisely why the drift was invisible."
    )


def test_reserved_keys_and_schema_properties_are_the_same_set() -> None:
    """The two machine-readable copies must agree with each other, not merely each cover dispatch.

    A key can be legitimately declared and never dispatched — ``brand_style_pack_ref`` is
    producer-resolved (VisualDNA) and no validator reads it. That is fine. What is not fine is the two
    copies disagreeing about which keys those are.
    """
    properties = set(json_schema()["$defs"]["reserved"]["properties"])
    tuple_keys = set(RESERVED_KEYS)
    assert tuple_keys == properties, (
        f"the two machine-readable copies of the _reserved namespace disagree — "
        f"only in RESERVED_KEYS: {sorted(tuple_keys - properties)}; "
        f"only in the schema: {sorted(properties - tuple_keys)}"
    )


def test_reserved_object_stays_open() -> None:
    """§7.3: unknown ``_reserved`` keys MUST be preserved. That requires this object stay open.

    Pinned as a test because closing it is a **major** bump that would break forward-compat, and it is
    the kind of change that looks like tightening and reads as an improvement in review.
    """
    reserved_schema = json_schema()["$defs"]["reserved"]
    assert "additionalProperties" not in reserved_schema, (
        "$defs.reserved has acquired an `additionalProperties` constraint. Unknown _reserved keys "
        "MUST be preserved (spec §7.3) — closing this object is a MAJOR version bump and breaks the "
        "one promise the _reserved carrier exists to make."
    )


def test_dynamic_dispatch_site_count_is_unchanged() -> None:
    """Guard the derived key list's completeness, rather than assuming it.

    Not a correctness assertion — dynamic dispatch is legitimate. It is a **review trigger**: if a new
    variable-keyed site appears, the statically-derived list above covers less of the validator than it
    did, and nobody would otherwise be told.
    """
    _, dynamic = _dispatch_keys()
    assert len(dynamic) == KNOWN_DYNAMIC_DISPATCH_SITES, (
        f"the number of variable-keyed `reserved[...]` dispatch sites changed "
        f"({KNOWN_DYNAMIC_DISPATCH_SITES} -> {len(dynamic)}): {dynamic}. No static walk can name the "
        "keys these read, so the derived list in this module is now a smaller floor than it was. "
        "Review, then update KNOWN_DYNAMIC_DISPATCH_SITES with the reason."
    )


# ---------------------------------------------------------------------------
# Datum P3 — every vocabulary DECLARES its relationship to the schema, and the declaration is
# checked against a derivation.
#
# ⛩ F-DT-7 is why these exist. `how/gates/registry_census.py` pairs a Python constant to a schema
# enum BY CONTENT and reported "12 SCHEMA-TWIN, all agreeing exactly" — which reads as twelve guarded
# vocabularies. It is not. Drift below the census's similarity floor does not report drift; the pair
# **dissolves**, and the constant reclassifies to VALIDATOR-ONLY, an accepted state. Measured at P3.1:
# gutting the schema's `fromSide`/`toSide` enums from four values to one left the census at exit 0 and
# ALL TEN vault gates green, while `jsonschema` correctly rejected an ordinary canvas.
#
#   ⇒ content-pairing is coverage that evaporates exactly when it is needed.
#
# A declared state is the memory content-pairing cannot have: `VALID_SIDES` SAYS it has a twin, so
# when the twin vanishes the claim FAILS. And it needs no name map — the map would itself be a
# hand-maintained registry with no consumer, which is the defect, not the fix.
#
# ⛔ NOT a list checked against a second hand-written list. It is one falsifiable claim per object,
# checked against a derivation, with the population discovered by walking the package. Same shape as
# KNOWN_DYNAMIC_DISPATCH_SITES above.
#
# ⚠ The duplication with `registry_census.py` is deliberate and named, per F-DT-3's own rule. The
# package MUST NOT depend on the vault tree that contains it: a fork, or `pip install
# adna-canvas-std`, has this file and no `how/gates/`. That matters more here than anywhere else in
# this module, because F-DT-7's blast radius is entirely downstream — the JSON Schema's value enums
# are read by NOTHING inside this vault (every in-package reader of `json_schema()` reads
# `$defs.reserved` only). The vault gate additionally checks spec §7.2, a vault artifact.
# ---------------------------------------------------------------------------
def _collection_members(value: ast.AST) -> tuple[Any, ...] | None:
    """If ``value`` is a literal collection of scalars (or ``frozenset(...)`` of one), return items."""
    if isinstance(value, ast.Call) and isinstance(value.func, ast.Name) and value.func.id == "frozenset":
        if len(value.args) != 1:
            return None
        try:
            return tuple(ast.literal_eval(value.args[0]))
        except (ValueError, TypeError):
            return None
    if isinstance(value, (ast.Tuple, ast.Set, ast.List)):
        try:
            items = tuple(ast.literal_eval(value))
        except (ValueError, TypeError):
            return None
        # Only scalar vocabularies. A tuple of dicts/tuples is data, not a vocabulary.
        if any(isinstance(i, (dict, list, tuple, set)) for i in items):
            return None
        return items
    return None


def _declared_registries() -> dict[str, dict[str, Any]]:
    """Walk the package for vocabulary constants and the PEP 258 attribute docstring beneath each.

    An attribute docstring is real AST structure — an ``ast.Expr`` holding a string constant, in
    module body position immediately after the assignment — so this needs no comment parsing and no
    ``tokenize`` pass. Returns ``{name: {members, module, declared_state, doc}}``; ``declared_state``
    is ``None`` when there is no docstring at all.
    """
    out: dict[str, dict[str, Any]] = {}
    for path in sorted(PKG_DIR.rglob("*.py")):
        body = ast.parse(path.read_text(encoding="utf-8"), filename=str(path)).body
        for i, node in enumerate(body):
            names: list[str] = []
            value: ast.AST | None = None
            if isinstance(node, ast.Assign):
                names = [t.id for t in node.targets if isinstance(t, ast.Name)]
                value = node.value
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                names = [node.target.id]
                value = node.value
            if not names or value is None or not _UPPER_SNAKE.match(names[0]):
                continue
            members = _collection_members(value)
            if members is None:
                continue
            doc: str | None = None
            nxt = body[i + 1] if i + 1 < len(body) else None
            if (
                isinstance(nxt, ast.Expr)
                and isinstance(nxt.value, ast.Constant)
                and isinstance(nxt.value.value, str)
            ):
                doc = nxt.value.value
            state: str | None = None
            if doc:
                first = doc.strip().split()[0].rstrip(".,—-") if doc.strip() else ""
                state = first if first in _STATES else None
            out[names[0]] = {
                "members": frozenset(members),
                "module": path.name,
                "line": node.lineno,
                "declared_state": state,
                "doc": doc,
            }
    return out


def _schema_enums() -> list[tuple[str, frozenset]]:
    """Every ``enum`` node in the JSON Schema, by JSON pointer. Traversed, not listed."""
    out: list[tuple[str, frozenset]] = []

    def walk(obj: Any, pointer: str) -> None:
        if isinstance(obj, dict):
            if isinstance(obj.get("enum"), list):
                out.append((pointer or "/", frozenset(obj["enum"])))
            for k, v in obj.items():
                walk(v, f"{pointer}/{k}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                walk(v, f"{pointer}/{i}")

    walk(json_schema(), "")
    return out


@pytest.fixture(scope="module")
def registries() -> dict[str, dict[str, Any]]:
    found = _declared_registries()
    # A walk that finds nothing makes every assertion below vacuously true — F-P2-11's family.
    assert len(found) > 20, (
        f"the vocabulary walk found only {len(found)} constants — the walker is broken, not the "
        "package. Every assertion downstream would pass vacuously."
    )
    return found


def test_every_vocabulary_declares_its_state(registries: dict[str, dict[str, Any]]) -> None:
    """The reason goes ON THE LINE — and something fails when it is missing.

    Operation Datum's definition of done: every hand-maintained vocabulary registry either has a
    consumer or is covered by a discovery pass, **and which one it is is written on the line.** A
    constant with no attribute docstring is the forbidden third state: correct today, maintained by
    hand, and read by nothing.
    """
    undeclared = sorted(
        f"{v['module']}:{v['line']} {k}" for k, v in registries.items() if v["declared_state"] is None
    )
    assert not undeclared, (
        "these vocabulary constants declare no state: "
        f"{undeclared}. Add a PEP 258 attribute docstring directly beneath the assignment whose "
        f"FIRST WORD is one of {_STATES}, and — for VALIDATOR-ONLY — say why there is no schema "
        "twin. A missing twin is a fact to state with its reason, not a defect to remedy by "
        "inventing one."
    )


def test_declared_state_matches_the_derived_state(registries: dict[str, dict[str, Any]]) -> None:
    """The claim is falsifiable, which is the whole point (F-DT-7).

    Derives each constant's ACTUAL state by looking for a schema enum with identical content, then
    compares it to what the constant SAYS. A `SCHEMA-TWIN` whose twin has been gutted fails here —
    the case that left all ten vault gates green at P3.1.
    """
    enums = _schema_enums()
    mismatches: list[str] = []
    for name, v in sorted(registries.items()):
        if v["declared_state"] is None:
            continue  # reported by the test above; do not double-report
        twins = [ptr for ptr, members in enums if members == v["members"]]
        derived = "SCHEMA-TWIN" if twins else "VALIDATOR-ONLY"
        if derived != v["declared_state"]:
            detail = f"twin(s) at {twins}" if twins else "NO schema enum holds this exact set"
            mismatches.append(
                f"{v['module']}:{v['line']} {name} declares {v['declared_state']} but derives "
                f"{derived} ({detail})"
            )
    assert not mismatches, (
        "declared state disagrees with the derived state:\n  " + "\n  ".join(mismatches) + "\n"
        "A SCHEMA-TWIN that now derives VALIDATOR-ONLY means its schema enum CHANGED OR VANISHED — "
        "the JSON Schema is validated by consumers outside this repository, so this is a real "
        "regression, not a bookkeeping mismatch. A VALIDATOR-ONLY that now derives SCHEMA-TWIN means "
        "a twin appeared: confirm it is intended, then update the docstring. ⛔ Never edit the "
        "docstring merely to make this pass."
    )


def test_validator_only_vocabularies_state_a_reason(registries: dict[str, dict[str, Any]]) -> None:
    """A bare label is not a reason, and the label alone is what rots.

    `EXCLUSIONS` in `how/gates/gate_manifest.py` learned this first: every escape hatch carries a
    non-empty reason, in the same place as the rule.
    """
    bare = sorted(
        f"{v['module']}:{v['line']} {k}"
        for k, v in registries.items()
        if v["declared_state"] == "VALIDATOR-ONLY"
        and len((v["doc"] or "").strip()) <= len("VALIDATOR-ONLY") + 8
    )
    assert not bare, (
        f"these declare VALIDATOR-ONLY with no stated reason: {bare}. Say WHY there is no schema "
        "twin — several are validator-only BY DESIGN (the `_reserved` sub-vocabularies are governed "
        "by their own specs; `VALID_COLORS` has no enum because `validate()` also accepts #-hex, so "
        "an enum would be wrong). The reason is what stops someone 'fixing' it by inventing a twin."
    )


def test_baseline_types_and_node_types_agree() -> None:
    """⛩ F-DT-3, ruled by the operator 2026-09-15: **two vocabularies that coincide — link, not merge.**

    `reserved.BASELINE_TYPES` (what a component may degrade TO, spec §11 A-3) and
    `schema.VALID_NODE_TYPES` (what node types the baseline document has) hold the same four words in
    two modules with nothing between them — so one could move and the other could not notice. That is
    not a drift; it is the *precondition* for one, and it is this campaign's target in its purest form.

    They are deliberately NOT merged. Whether these are one vocabulary or two that currently coincide
    is a semantic question a set comparison cannot answer, and §11's no-baseline-overload rule
    arguably makes the agreement a consequence rather than an identity. So: both definitions stand,
    and the day they stop agreeing, this says so.
    """
    assert BASELINE_TYPES == VALID_NODE_TYPES, (
        f"the A-3 degradation target set and the baseline node types have diverged — "
        f"only in BASELINE_TYPES: {sorted(BASELINE_TYPES - VALID_NODE_TYPES)}; "
        f"only in VALID_NODE_TYPES: {sorted(VALID_NODE_TYPES - BASELINE_TYPES)}. "
        "This is NOT automatically a bug: they answer different questions and were ruled separate "
        "vocabularies (F-DT-3). But spec §11 says a component degrades to a BASELINE type, so a "
        "degradation target outside the baseline node types would be unrepresentable in a valid "
        "Obsidian canvas. Review both specs, then decide deliberately."
    )
    # Guard the guard: two empty sets are equal, and would make the assertion above vacuous.
    assert BASELINE_TYPES, "BASELINE_TYPES is empty — the assertion above would pass vacuously"


def test_schema_module_is_covered_by_the_walk(registries: dict[str, dict[str, Any]]) -> None:
    """The walk must actually reach `schema.py`, not just `reserved.py`.

    F-DT-7's eleven exposed enums all twin constants in `schema.py`. A walk that silently covered one
    module would leave exactly the surface this phase was opened to close, while reporting success.
    """
    modules = {v["module"] for v in registries.values()}
    assert {"reserved.py", "schema.py"} <= modules, (
        f"the vocabulary walk covered {sorted(modules)} — it must reach both `reserved.py` and "
        "`schema.py`. `schema.py` holds every constant with a JSON Schema twin."
    )
    assert Path(schema_mod.__file__).name == "schema.py"
