"""VisualDNA auto-compose (Halftone H5) — character bundles -> an enriched comic-input mapping.

Bridges the VisualDNA standard (``VisualDNA.aDNA/what/artifacts/visual_dna_schema/spec_v1.0.md``) into the
producer: a character bundle's text subsets, reference images, and (when trained) LoRA pair are composed onto the
comic input's ``characters:`` rows, which ``panels.py`` then emits per-panel as ``qualities.characters`` — the
structured asset channel the render bridge lifts into its manifest (``comic_render/extract.py``). Cross-vault
bundle reads are READ-ONLY (campaign Rule 10); nothing here writes outside the enriched output the caller names.

Content-layer module (ADR-004 two-shelf firewall): stdlib + yaml only — no ``canvas_std``, no render engine.

Empirical tolerance over spec purity — the two live bundles diverge from the v1.0 schema and from each other:

* ``lora_refs`` arrives in four shapes: spec list-form (Bearly: ``[]``), mapping-with-``entries`` (Stanley
  v0.1.x), deprecated placeholder string, or absent.
* Reference paths are bundle-dir-relative (Stanley: ``references/…``) OR vault-root-relative (Bearly:
  ``what/corpus/…``) — resolution tries both; emission is workspace-root-relative (``<Vault>.aDNA/…``, the
  bundle lora-path precedent) so enriched inputs and emitted canvases stay machine-portable.
* Canonical election may not have happened (Bearly's sole portrait is ``canonical: false``) — selection is
  canonical-FIRST, never canonical-only.

The LoRA **pair-gate**: ``trigger_word`` + ``lora_ref`` are emitted together from ONE eligible entry
(``status: TRAINED | VALIDATED``) or not at all. ``PENDING_TRAINING`` omits BOTH — an untrained trigger token is
an inert-or-harmful stray identity token (spec §5 label hygiene), and consumers read the pair together (spec §7).
Reference-images-only compose is therefore the *required* path for both live bundles today (Halftone H5 exit
criterion; Bearly's LoRA is rights-HELD, Stanley's is untrained).
"""

from __future__ import annotations

import copy
import json
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

# Descriptor fallback chain (spec §2.2). The compressed subset (~300 chars) is DESIGNED for composition; the
# longer fallbacks work but risk framing-lock (spec §4) — hence the length warning.
_DESCRIPTOR_KEYS = ("compressed_character_subset", "portrait_subset", "full_prompt_inline")
_DESCRIPTOR_WARN_CHARS = 800

# Reference categories composed by default (the generation-suitable trio of the spec §2.3 open set). Categories
# outside the set still contribute their ``canonical: true`` items. ``restricted`` is NEVER composed; mapping-
# shaped categories (e.g. Stanley's ``real_photos``) are corpus/verification data, not generation references.
DEFAULT_REF_CATEGORIES: tuple[str, ...] = ("portraits", "expressions", "scenes")
DEFAULT_REF_CAP = 6

_LORA_ELIGIBLE = frozenset({"TRAINED", "VALIDATED"})
_NEVER_COMPOSED_CATEGORIES = frozenset({"restricted", "discarded"})


# ============================================================================================================
# Bundle parsing.
# ============================================================================================================

@dataclass(frozen=True)
class Bundle:
    """A parsed VisualDNA character bundle + the roots its reference paths resolve against."""

    path: Path
    id: str = ""
    display_name: str = ""
    entity_type: str = ""
    status: str = ""
    version: str = ""
    text_prompt: dict[str, Any] = field(default_factory=dict)
    reference_image_set: dict[str, Any] = field(default_factory=dict)
    lora_entries: tuple[dict[str, Any], ...] = ()

    @property
    def bundle_dir(self) -> Path:
        return self.path.parent

    def vault_root(self) -> Path | None:
        """Nearest ancestor directory named ``*.aDNA`` (the bundle's vault), or None outside a workspace."""
        for anc in self.path.resolve().parents:
            if anc.name.endswith(".aDNA"):
                return anc
        return None


def _lora_entries(raw: Any, *, source: str) -> list[dict[str, Any]]:
    """Normalize the four live ``lora_refs`` shapes to a flat list of entry mappings."""
    if raw is None:
        return []
    if isinstance(raw, str):
        if raw.strip():
            warnings.warn(
                f"{source}: deprecated placeholder-string lora_refs — treated as no entries",
                UserWarning,
                stacklevel=3,
            )
        return []
    if isinstance(raw, dict):
        raw = raw.get("entries") or []
    if not isinstance(raw, list):
        return []
    return [e for e in raw if isinstance(e, dict)]


def load_bundle(path: str | Path) -> Bundle:
    """Parse a VisualDNA bundle YAML (the ``visual_dna:`` root mapping) into a :class:`Bundle`.

    Non-mapping files raise; a ``draft`` bundle warns but parses (Bearly's *required* LoRA-less path IS a draft
    bundle); scalar oddities (unquoted dates, etc.) are coerced to strings defensively.
    """
    p = Path(path)
    data = yaml.safe_load(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("visual_dna"), dict):
        raise ValueError(f"{p}: not a VisualDNA bundle (no `visual_dna:` root mapping)")
    vd = data["visual_dna"]
    status = str(vd.get("status", "") or "")
    if status.strip().lower() == "draft":
        warnings.warn(
            f"{p.name}: bundle status is 'draft' (no canon election yet) — composing anyway",
            UserWarning,
            stacklevel=2,
        )
    tp = vd.get("text_prompt")
    ris = vd.get("reference_image_set")
    return Bundle(
        path=p,
        id=str(vd.get("id", "") or ""),
        display_name=str(vd.get("display_name", "") or ""),
        entity_type=str(vd.get("entity_type", "") or ""),
        status=status,
        version=str(vd.get("version", "") or ""),
        text_prompt=tp if isinstance(tp, dict) else {},
        reference_image_set=ris if isinstance(ris, dict) else {},
        lora_entries=tuple(_lora_entries(vd.get("lora_refs"), source=p.name)),
    )


# ============================================================================================================
# Asset selection.
# ============================================================================================================

def select_lora(entries: tuple[dict[str, Any], ...] | list[dict[str, Any]], art_style: str = "") -> tuple[str | None, str | None]:
    """The pair-gate: ``(trigger_word, lora_ref)`` from ONE eligible entry, or ``(None, None)``.

    Eligible = ``status`` in ``TRAINED | VALIDATED`` with both ``trigger_word`` and ``path`` present (the
    campaign charter's "LoRA into refine **when trained**"). Among eligible entries, prefer the one whose
    ``register`` matches the comic's ``art_style``; else the first (deterministic).
    """
    eligible = [
        e for e in entries
        if str(e.get("status", "") or "").strip().upper() in _LORA_ELIGIBLE
        and str(e.get("trigger_word", "") or "").strip()
        and str(e.get("path", "") or "").strip()
    ]
    if not eligible:
        return None, None
    style = (art_style or "").strip().lower()
    pick = next(
        (e for e in eligible if style and str(e.get("register", "") or "").strip().lower() == style),
        eligible[0],
    )
    return str(pick["trigger_word"]).strip(), str(pick["path"]).strip()


def _discarded_strings(reference_image_set: dict[str, Any]) -> list[str]:
    """The ``discarded`` block's item strings (mapping ``{reason, items[]}`` or bare list; str or dict items)."""
    raw = reference_image_set.get("discarded")
    if isinstance(raw, dict):
        items = raw.get("items") or []
    elif isinstance(raw, list):
        items = raw
    else:
        items = []
    out: list[str] = []
    for it in items:
        s = str(it.get("path", "") or it.get("label", "") or "") if isinstance(it, dict) else str(it)
        if s.strip():
            out.append(s)
    return out


def _resolve_reference(bundle: Bundle, raw_path: str, *, strict: bool) -> str | None:
    """Resolve a bundle reference path (bundle-dir first, then vault-root) -> workspace-root-relative string.

    Unresolvable -> warn + ``None`` (``strict`` -> ``FileNotFoundError``). A path resolving outside any
    ``*.aDNA`` vault is emitted absolute with a warning (portability lost, but the reference survives).
    """
    rel = Path(raw_path)
    resolved: Path | None = None
    if rel.is_absolute():
        resolved = rel if rel.exists() else None
    else:
        for root in (bundle.bundle_dir, bundle.vault_root()):
            if root is not None and (root / rel).exists():
                resolved = root / rel
                break
    if resolved is None:
        msg = f"{bundle.path.name}: reference image {raw_path!r} does not resolve (bundle-dir nor vault-root)"
        if strict:
            raise FileNotFoundError(msg)
        warnings.warn(f"{msg} — skipped", UserWarning, stacklevel=3)
        return None
    resolved = resolved.resolve()
    vault = bundle.vault_root()
    if vault is not None:
        try:
            return str(resolved.relative_to(vault.parent))
        except ValueError:
            pass
    warnings.warn(
        f"{bundle.path.name}: {raw_path!r} resolves outside any *.aDNA vault — emitting an absolute path",
        UserWarning,
        stacklevel=3,
    )
    return str(resolved)


def select_reference_images(
    bundle: Bundle,
    *,
    categories: tuple[str, ...] = DEFAULT_REF_CATEGORIES,
    cap: int = DEFAULT_REF_CAP,
    strict: bool = False,
) -> list[str]:
    """Generation-suitable reference images: canonical-FIRST, workspace-root-relative, capped.

    Walks list-shaped categories only. Included categories contribute all items; other list categories
    contribute only their ``canonical: true`` items. ``restricted`` never composes; ``discarded`` excludes by
    substring against raw path AND basename (an image may be dual-listed in a category and discarded). Order:
    canonical first, then included-category priority, then bundle order. Missing files don't consume the cap.
    """
    discarded = _discarded_strings(bundle.reference_image_set)
    wanted = tuple(c.strip() for c in categories if c and c.strip())
    candidates: list[tuple[int, int, int, str]] = []  # (non_canonical, category_priority, bundle_order, path)
    order = 0
    for cat, items in bundle.reference_image_set.items():
        if cat in _NEVER_COMPOSED_CATEGORIES or not isinstance(items, list):
            continue
        canonical_only = cat not in wanted
        for it in items:
            if not isinstance(it, dict):
                continue
            raw_path = str(it.get("path", "") or "").strip()
            if not raw_path:
                continue
            canonical = bool(it.get("canonical", False))
            if canonical_only and not canonical:
                continue
            base = Path(raw_path).name
            if any(raw_path in d or base in d for d in discarded):
                continue
            priority = wanted.index(cat) if cat in wanted else len(wanted)
            candidates.append((0 if canonical else 1, priority, order, raw_path))
            order += 1
    candidates.sort()
    out: list[str] = []
    for _, _, _, raw_path in candidates:
        if len(out) >= cap:
            break
        norm = _resolve_reference(bundle, raw_path, strict=strict)
        if norm and norm not in out:
            out.append(norm)
    return out


def derive_descriptor(bundle: Bundle) -> str:
    """The Layer-2 descriptor text: compressed subset -> portrait subset -> full inline prompt ('' if none)."""
    for key in _DESCRIPTOR_KEYS:
        val = bundle.text_prompt.get(key)
        if isinstance(val, str) and val.strip():
            text = val.strip()
            if key != "compressed_character_subset" and len(text) > _DESCRIPTOR_WARN_CHARS:
                warnings.warn(
                    f"{bundle.path.name}: descriptor falls back to {key} ({len(text)} chars > "
                    f"{_DESCRIPTOR_WARN_CHARS}) — long prompts risk framing-lock (VisualDNA spec §4); "
                    "consider authoring compressed_character_subset",
                    UserWarning,
                    stacklevel=3,
                )
            return text
    return ""


@dataclass(frozen=True)
class BundleAssets:
    """One character's composed assets (the panel-facing shape, minus the name)."""

    descriptor: str = ""
    trigger_word: str | None = None
    lora_ref: str | None = None
    reference_images: tuple[str, ...] = ()


def compose_assets(
    bundle: Bundle,
    *,
    art_style: str = "",
    categories: tuple[str, ...] = DEFAULT_REF_CATEGORIES,
    cap: int = DEFAULT_REF_CAP,
    strict_refs: bool = False,
) -> BundleAssets:
    """Compose one bundle into assets. LoRA-less bundles yield reference-images-only (the pair-gate holds)."""
    trigger, lora = select_lora(bundle.lora_entries, art_style)
    refs = select_reference_images(bundle, categories=categories, cap=cap, strict=strict_refs)
    return BundleAssets(
        descriptor=derive_descriptor(bundle),
        trigger_word=trigger,
        lora_ref=lora,
        reference_images=tuple(refs),
    )


# ============================================================================================================
# Matching + enrichment.
# ============================================================================================================

def match_bundle_to_character(bundle: Bundle, names: list[str]) -> str:
    """Match one bundle to exactly ONE input character name (bible ∪ panel names).

    Exact (name == display_name or name == id, case-insensitive) beats substring; the substring direction is
    input-name-IN-bundle-string, so ``agent_stanley`` never matches Stanley's bundle. Zero or 2+ matches -> hard
    error naming the candidates (escape hatch: the explicit ``name=path`` form).
    """
    disp = bundle.display_name.strip().lower()
    bid = bundle.id.strip().lower()
    uniq = [n for n in dict.fromkeys(names) if str(n).strip()]
    exact = [n for n in uniq if n.lower() == disp or n.lower() == bid]
    if len(exact) == 1:
        return exact[0]
    if len(exact) > 1:
        raise ValueError(
            f"{bundle.path.name}: ambiguous character match {exact} — use the explicit name=path form"
        )
    sub = [n for n in uniq if n.lower() in disp or n.lower() in bid]
    if len(sub) == 1:
        return sub[0]
    if sub:
        raise ValueError(
            f"{bundle.path.name}: ambiguous character match {sub} — use the explicit name=path form"
        )
    raise ValueError(
        f"{bundle.path.name}: no character in the input matches bundle "
        f"(display_name={bundle.display_name!r}, id={bundle.id!r}); candidates were {uniq} — "
        "use the explicit name=path form"
    )


def _bundle_ref(bundle: Bundle) -> str:
    """The bundle's provenance pointer — workspace-root-relative when inside a vault, else absolute."""
    vault = bundle.vault_root()
    if vault is not None:
        try:
            return str(bundle.path.resolve().relative_to(vault.parent))
        except ValueError:
            pass
    return str(bundle.path.resolve())


def enrich_comic_dict(
    raw: dict[str, Any],
    bundles: list[tuple[str | None, Bundle]],
    *,
    categories: tuple[str, ...] = DEFAULT_REF_CATEGORIES,
    cap: int = DEFAULT_REF_CAP,
    strict_refs: bool = False,
) -> dict[str, Any]:
    """Enrich a raw comic-input mapping with composed bundle assets; returns a NEW dict (input untouched).

    ``bundles`` pairs an optional explicit character name with each bundle (``None`` -> heuristic match).
    Policy: an in.yaml non-empty ``descriptor`` always wins (author intent); the bundle fills empty ones; asset
    fields always attach when composed. A matched panel-only character gains an auto-created bible row (true
    auto-compose — Bearly comics need no pre-authored bible). Provenance rides under ``composed_from`` (a key
    ``ComicInput.from_dict`` ignores); recompose replaces a character's prior entry (idempotent).
    """
    out = copy.deepcopy(raw)
    chars = out.setdefault("characters", [])
    if not isinstance(chars, list):
        raise ValueError("comic input `characters:` is not a list")

    bible_names = [str(c.get("name", "")) for c in chars if isinstance(c, dict)]
    panel_names: list[str] = []
    for pg in out.get("pages", []) or []:
        for p in pg.get("panels", []) or []:
            panel_names.extend(str(n) for n in (p.get("characters", []) or []))
    candidates = list(dict.fromkeys(bible_names + panel_names))

    provenance = out.get("composed_from")
    if not isinstance(provenance, list):
        provenance = []
    art_style = str(out.get("art_style", "") or "")

    for explicit_name, bundle in bundles:
        if bundle.entity_type and bundle.entity_type != "character":
            warnings.warn(
                f"{bundle.path.name}: entity_type {bundle.entity_type!r} — skipped (only characters compose)",
                UserWarning,
                stacklevel=2,
            )
            continue
        name = explicit_name or match_bundle_to_character(bundle, candidates)
        assets = compose_assets(
            bundle, art_style=art_style, categories=categories, cap=cap, strict_refs=strict_refs
        )
        row = next(
            (c for c in chars if isinstance(c, dict) and str(c.get("name", "")).lower() == name.lower()),
            None,
        )
        if row is None:
            row = {"name": name}
            chars.append(row)
            if name not in candidates:
                candidates.append(name)
        if not str(row.get("descriptor", "") or "").strip() and assets.descriptor:
            row["descriptor"] = assets.descriptor
        if assets.trigger_word:
            row["trigger_word"] = assets.trigger_word
        if assets.lora_ref:
            row["lora_ref"] = assets.lora_ref
        if assets.reference_images:
            row["reference_images"] = list(assets.reference_images)
        provenance = [
            e for e in provenance
            if not (isinstance(e, dict) and str(e.get("character", "")).lower() == name.lower())
        ]
        provenance.append({"character": name, "bundle": _bundle_ref(bundle), "bundle_version": bundle.version})

    if provenance:
        out["composed_from"] = provenance
    else:
        out.pop("composed_from", None)
    return out


# ============================================================================================================
# Raw input IO (the CLI's file-shaped seam).
# ============================================================================================================

def load_raw_input(path: str | Path) -> dict[str, Any]:
    """Load a comic input file (.yaml/.yml/.json) as a raw mapping (unknown keys preserved for enrichment)."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    data = yaml.safe_load(text) if p.suffix.lower() in (".yaml", ".yml") else json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"comic input {p} did not parse to a mapping")
    return data


def dump_enriched(enriched: dict[str, Any], path: str | Path) -> None:
    """Write the enriched input as YAML (a derived artifact — comments/ordering of the source are not kept)."""
    Path(path).write_text(
        yaml.safe_dump(enriched, sort_keys=False, allow_unicode=True, width=110),
        encoding="utf-8",
    )
