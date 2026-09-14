"""The `_reserved` namespace registry has a consumer — this file.

Operation Datum P2, under the operator ruling of 2026-09-13 (a named firewall touch, the fourth
deliberate one since Keystone).

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
from pathlib import Path

import pytest

from canvas_std import reserved as reserved_mod
from canvas_std.conformance import json_schema
from canvas_std.reserved import RESERVED_KEYS

PKG_DIR = Path(reserved_mod.__file__).resolve().parent

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
