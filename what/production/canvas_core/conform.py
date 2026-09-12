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
from canvas_std.reserved import AUTHORITY_VALUES, PRODUCTION_VALUES

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
#: ⛩ **DE-DUPLICATED 2026-09-11 (Gridline).** These were two locally-declared frozensets, and the
#: comment here used to read *"``canvas_std`` still does not validate either key (F-B1-2), so the checks
#: here and in ``diagram_generator.model`` remain the only enforcement anywhere."* **That is now false**:
#: LIP-0010 was ratified and `canvas_std` validates both keys as **A-8** at Standard **v2.4.0**. So the
#: values are no longer restated here — they are **imported from the Standard's own implementation**, and
#: this module keeps only the *early* raise (refusing to build beats failing after the block is in
#: someone's file). ⇒ ***one definition, two enforcement points, no drift possible*** — the Armature
#: precedent, where a consumer became a thin delegate rather than a second source of truth.
#:
#: The public names are retained (they are in ``__all__``) so no consumer import breaks.
VALID_AUTHORITIES = AUTHORITY_VALUES
VALID_PRODUCTION = PRODUCTION_VALUES

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
    # ⛩ NOT bumped to 2.4.0 at the Gridline cut, deliberately. `adna_version` states which Standard
    # version a canvas was authored against, not which is newest — the Beacon precedent keeps
    # 2.0.0-authored fixtures valid for exactly this reason. ⚠ And the vault is ALREADY inconsistent
    # here: five emitters stamp three different values (`variant_board`/`tuning_surface`/
    # `review_canvas` write "2.0.0", `diagram_generator` writes its own ADNA_VERSION constant, this
    # writes "2.3.0"). Bumping one of the five would make it four values, not one. Recorded as a
    # finding for a separate ruling rather than half-fixed here.
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
    :data:`VALID_PRODUCTION` — which are now the Standard's own sets, imported rather than restated.

    ⛩ **This paragraph used to end** *"because ``canvas_std`` will not check either for you
    (F-B1-2)"*. **That expired on 2026-09-11**: LIP-0010 was ratified and both keys are validated as
    **A-8** at Standard **v2.4.0**. The checks stay because they fire **earlier** — refusing to build
    beats failing after the block is in someone's file — not because they are the only ones left.

    ⛔ One rule is **asymmetric** and is enforced here too: passing ``authority`` without
    ``production`` raises, because the Standard rejects that pair. ``production`` alone does not — it
    is the correct block for an artifact no other channel owns.
    """
    if authority is not None and authority not in VALID_AUTHORITIES:
        raise ValueError(
            f"authority {authority!r} not in {sorted(VALID_AUTHORITIES)} — refused at build time "
            "because a canvas is cheaper to not-write than to fix in someone's file; `canvas_std` "
            "also rejects it now (A-8, v2.4.0). Note `generator` was REMOVED from this axis on "
            "2026-09-11: it answers *how is the picture made*, so pass production='generated' instead."
        )
    if production is not None and production not in VALID_PRODUCTION:
        raise ValueError(
            f"production {production!r} not in {sorted(VALID_PRODUCTION)} — refused at build time; "
            "`canvas_std` also rejects it now (A-8, v2.4.0)"
        )
    if authority is not None and production is None:
        # ⛩ A-8's asymmetry (Standard v2.4.0, Gridline P1). Emitting `authority` without `production`
        # would build a canvas `canvas-std validate` refuses. The converse stays allowed and is
        # documented above as the *correct* block for an artifact no other channel owns.
        raise ValueError(
            f"authority {authority!r} passed without production — A-8 (Standard v2.4.0) requires "
            "`production` whenever `authority` is present: naming another channel as the owner of "
            "this canvas's meaning while leaving unsaid how it is made omits the field that carries "
            "'never hand-edit; regenerate'. Pass production='generated' or 'hand_authored'."
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
