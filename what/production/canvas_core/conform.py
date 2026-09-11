"""Conformance repair for canvases that already exist — the C-4/C-3 pass, and the `_reserved` uplift.

Two operations, deliberately separated by how much judgement they need:

===============================  =====================================  ===================
Function                         What it does                           Judgement required
===============================  =====================================  ===================
:func:`normalize_edges`          adds the explicit ``toEnd`` C-4 wants   **none** — mechanical
:func:`uplift_to_adna_native`    writes ``metadata.frontmatter._reserved``  a source name; axis keys optional
:func:`unresolved_edges`         *reports* C-3 dangling refs             **all of it** — never repaired here
===============================  =====================================  ===================

**Why this exists (F-P2b-2, Blueprint P2b).** The aDNA Canvas Standard requires every edge to carry
an *explicit* top-level ``toEnd`` (``canvas_std.validate`` C-4; v1.0.0's "always include
toEnd:arrow"), where baseline JSON Canvas is happy to let it default. Obsidian does not write the
key on re-save. So **a human opening a conformant canvas and saving it silently un-conforms it** —
the file still renders perfectly, and nothing tells anyone.

Canvas diagnosed this in its own vault at HR gate 3/3 (**F-HR-1**, 2026-08-23) and carried
"normalize-on-collect" as an open item through P2 and P2c, described each time as an internal
``canvas_context`` concern. The P2b census found the same signature in **two other vaults** — three
Operations files that lost *100%* of their ``toEnd`` keys (8/8→0, 5/5→0, 5/5→0) and five
ScienceStanley boards, **40 of the 41 total errors across both**. It is not an internal concern; it
is the fix that keeps a conformant canvas conformant across a human editing pass anywhere.

**What this module will not do.** It will not repair a C-3 unresolvable edge reference. Deciding
whether a dangling edge should be deleted, or re-pointed at the node someone meant, or kept as
evidence that a node went missing, requires knowing what the diagram is *for*. :func:`unresolved_edges`
surfaces them and stops. (The census found exactly one, in a shipped teaching package, pointing away
from an ``expires_at`` node at a target that has never existed in that file.)
"""

from __future__ import annotations

from typing import Any

from canvas_std import compute_sync_hash

__all__ = [
    "normalize_edges",
    "unresolved_edges",
    "uplift_to_adna_native",
    "VALID_AUTHORITIES",
    "VALID_PRODUCTION",
]

#: The **authority** axis — *who owns the meaning?* Both values name an **other** channel that owns it,
#: because that relationship is what `pattern_diagrammatic_context` is about: ``dual_channel`` (the
#: prose owns it) and ``view`` (an authoritative ``.lattice.yaml`` owns it).
#:
#: ⛩ **Ruled 2026-09-11** (aDNA.aDNA HAUSSMANN R1, on Canvas's offer as amended by our own erratum E2).
#: ``generator`` was **removed** — it never answered this question. It answers *how is the picture
#: made*, which is now :data:`VALID_PRODUCTION`. Under the old single enum our own first two
#: dual-channel canvases were ``dual_channel`` **and** machine-generated at once, so a reader following
#: the table literally received no instruction not to hand-edit them.
#:
#: ⚠ ``canvas_std`` still does **not** validate either key (F-B1-2: an invented value passes silently),
#: so the checks here and in ``diagram_generator.model`` remain the only enforcement anywhere.
#: LIP-0010 holds the durable fix; its cells are now fixed by the ruled pattern.
VALID_AUTHORITIES = frozenset({"dual_channel", "view"})

#: The **production** axis — *how is the picture made?* ``generated`` carries the "never hand-edit;
#: regenerate" discipline. ⭐ That discipline attaches **here and not to any authority value** — which
#: is the whole reason the axes are split.
VALID_PRODUCTION = frozenset({"hand_authored", "generated"})

_DEFAULT_TO_END = "arrow"


def normalize_edges(doc: dict[str, Any], *, to_end: str = _DEFAULT_TO_END) -> tuple[dict[str, Any], int]:
    """Add the explicit top-level ``toEnd`` that C-4 requires, changing nothing else.

    Returns ``(doc, repaired_count)``. The document is mutated in place and also returned, so this
    reads naturally either way.

    **This is a no-op on meaning.** An edge with no ``toEnd`` already renders as an arrow — that is
    the JSON Canvas default, and why the omission is invisible. Writing the key states what the file
    already does. An edge that *deliberately* carries ``toEnd: "none"`` (a permitted undirected edge)
    is left alone, because it is already explicit.
    """
    repaired = 0
    for edge in doc.get("edges", []):
        if not isinstance(edge, dict):
            continue
        if "toEnd" not in edge:
            edge["toEnd"] = to_end
            repaired += 1
    return doc, repaired


def unresolved_edges(doc: dict[str, Any]) -> list[tuple[str, str, str]]:
    """Report C-3 dangling endpoints as ``(edge_id, endpoint, unresolved_ref)`` — never repair them.

    Mirrors ``canvas_std.validate``'s C-3 endpoint check so the two cannot drift apart in what they
    consider unresolvable, but returns structured tuples rather than message strings, because a
    caller doing something about them needs the ids and not the prose.
    """
    node_ids = {n.get("id") for n in doc.get("nodes", []) if isinstance(n, dict)}
    out: list[tuple[str, str, str]] = []
    for edge in doc.get("edges", []):
        if not isinstance(edge, dict):
            continue
        eid = str(edge.get("id", "<no id>"))
        for endpoint in ("fromNode", "toNode"):
            ref = edge.get(endpoint)
            if ref is not None and ref not in node_ids:
                out.append((eid, endpoint, str(ref)))
    return out


def uplift_to_adna_native(
    doc: dict[str, Any],
    *,
    source_name: str,
    authority: str | None = None,
    production: str | None = None,
    adna_version: str = "2.3.0",
    context_object: dict[str, Any] | None = None,
    extra_reserved: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Write a canonical ``metadata.frontmatter._reserved`` block, leaving nodes and edges untouched.

    Follows the migration recipe verified 4/4 at Blueprint P1 (erratum v2 → Rosetta): ``adna_version``
    + ``conformance_level`` + a **nested** ``sync`` block whose ``sync_hash`` is *recomputed* by
    :func:`canvas_std.compute_sync_hash` (16 hex over sorted node ids and ``from->to`` pairs). A
    ``sha256:``-prefixed legacy value is not transliterable and is never carried across.

    ⚠ **The canonical path is ``metadata.frontmatter._reserved``.** A block written one level up at
    ``metadata._reserved`` carries semantics no tool reads *while still reporting a green* ``[OK]``
    *at* ``core`` — strictly worse than having no block at all (F-B1-1; 196 fleet files have been in
    that state since 2026-02). This function only ever writes the canonical path.

    ⛩ **``authority`` is OPTIONAL as of 2026-09-11, and that is a doctrine change, not a relaxation.**
    It was a *required* argument here because Canvas's own draft pattern said *"none is retired: a
    canvas with no declared authority is nonconformant diagrammatic context."* The ruled pattern
    **declines that mandate** — mandating a field no validator checks would be "a conformance claim
    with nothing behind it" — so requiring it here would now be this function inventing a rule the
    doctrine refused to make.

    ⭐ **And omission is frequently the *correct* answer, not a gap.** ``authority`` asks *who owns the
    meaning*, and both values name an **other** channel that owns it. A hand-authored **primary**
    artifact — a teaching diagram, a review board — owns its own meaning, has no prose twin and no
    ``.lattice.yaml``, and is **outside the scope of ``pattern_diagrammatic_context`` entirely**
    (which governs a `.canvas` *beside a document*). For that population the honest block is
    ``production="hand_authored"`` with ``authority`` omitted. Passing a value to make a number go
    green is the defect this signature used to force.

    Both keys are validated **only if present**, against :data:`VALID_AUTHORITIES` and
    :data:`VALID_PRODUCTION`, because ``canvas_std`` will not check either for you (F-B1-2).
    """
    if authority is not None and authority not in VALID_AUTHORITIES:
        raise ValueError(
            f"authority {authority!r} not in {sorted(VALID_AUTHORITIES)} — "
            "canvas_std does not validate this key (F-B1-2), so it is checked here or nowhere. "
            "Note `generator` was REMOVED from this axis on 2026-09-11: it answers *how is the "
            "picture made*, so pass production='generated' instead."
        )
    if production is not None and production not in VALID_PRODUCTION:
        raise ValueError(
            f"production {production!r} not in {sorted(VALID_PRODUCTION)} — "
            "canvas_std does not validate this key either, so it is checked here or nowhere"
        )
    # A-7 requires a non-empty string id. `canvas_std` does catch this one, but it catches it at
    # validation time, i.e. after the block has been written into someone's file — cheaper to refuse
    # to build it. (Unlike `authority` above, this check is a convenience, not the only enforcement.)
    if context_object is not None and not (
        isinstance(context_object.get("id"), str) and context_object["id"]
    ):
        raise ValueError("context_object requires a non-empty string 'id' (canvas_std A-7)")

    reserved: dict[str, Any] = {
        "adna_version": adna_version,
        "conformance_level": "adna_native",
        # Both axis keys are emitted only when declared. An absent key is a *statement that the
        # question does not arise*; a key written with a placeholder is a false answer that every
        # tool we ship will accept in silence.
        **({"authority": authority} if authority is not None else {}),
        **({"production": production} if production is not None else {}),
        "sync": {
            "source_name": source_name,
            "sync_hash": compute_sync_hash(doc),
        },
    }
    if context_object is not None:
        reserved["context_object"] = context_object
    if extra_reserved:
        reserved.update(extra_reserved)

    metadata = doc.setdefault("metadata", {})
    frontmatter = metadata.setdefault("frontmatter", {})
    frontmatter["_reserved"] = reserved
    return doc
