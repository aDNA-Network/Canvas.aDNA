"""Input model — a structured long-form document spec (ordered pages of ordered sections) + its genre contracts.

A substrate-free producer-side domain model: a human/agent authors a document (title + ordered pages, each an ordered
list of sections; each section a heading + body + rich blocks + citations) and, optionally, a **genre** carrying the
LiteratureForge **format** (F1–F7) and **visual** (V1–V8 per-asset / X1–X14 cross-asset) contracts. The consumer
(``consume.py``) maps the document onto the aDNA Canvas Standard and emits the contracts as declarative ``_reserved``
metadata. No ``canvas_std`` import here — the contracts are pure domain data (ADR-004 two-shelf firewall; E4.2).

The block set is a lean KEEP subset — the long-form elements the Standard's component model already covers
(figure/table/code/quote/list). The genre/writing **pipeline** (trap-packs, reviewer voices, reward rubrics) stays
producer-side and remains absent; E4.2 models the format/visual **contracts** (the declarative slots), not the engines.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# Rich block kinds beyond a section's heading + body prose.
BLOCK_TYPES: frozenset[str] = frozenset({"figure", "table", "code", "quote", "list"})


# ============================================================================================================
# Format contract (LiteratureForge spec_format_contract §1, F1–F7) — the format-bound output contract.
# ============================================================================================================

@dataclass(frozen=True)
class LengthWindow:                       # F1
    """Acceptable output extent. ``unit`` ∈ words|pages|slides (matches canvas_std ``PL_EXTENT_UNITS``)."""

    min: int = 0
    max: int = 0
    unit: str = "words"

    def is_set(self) -> bool:
        return self.max > 0


@dataclass(frozen=True)
class SectionSpec:                        # F2 row
    """A named structural section; ``order_locked`` for template-locked genres."""

    name: str
    required: bool = True
    order_locked: bool = False


@dataclass(frozen=True)
class OutputSurface:                      # F3 row (+ X6 aspect-ratio target, surface-keyed)
    """A deliverable surface; exactly one carries ``role: canonical``. ``aspect_ratio`` carries the X6 entry."""

    surface: str
    role: str = "derived"                 # canonical | derived
    aspect_ratio: str = ""


@dataclass(frozen=True)
class AssetConventions:                   # F4
    """Textual-side asset conventions. ``figure_placement`` is a STRING only — never an executed layout (PT-P5)."""

    table_form: str = ""
    equation_form: str = ""
    figure_placement: str = ""            # "float" | "inline" | "n/a (form-bypass)"

    def is_set(self) -> bool:
        return bool(self.table_form or self.equation_form or self.figure_placement)


@dataclass(frozen=True)
class NamingConvention:                   # F7 / X8 (shared discipline)
    label_form: str = "descriptive"       # descriptive | legacy
    migration_rule: str = ""

    def is_set(self) -> bool:
        return self.label_form != "descriptive" or bool(self.migration_rule)


@dataclass(frozen=True)
class FormatTemplateRef:                  # F6
    """External template lock. ``owner`` ∈ ""|venue|funder|partner|sub_class|brand."""

    owner: str = ""
    template_id: str = ""
    resolver: str = ""                    # style_file | structured_form | skeleton_doc

    def is_set(self) -> bool:
        return bool(self.owner)


@dataclass(frozen=True)
class FormatContract:
    length_window: LengthWindow = field(default_factory=LengthWindow)
    sections: list[SectionSpec] = field(default_factory=list)
    output_surfaces: list[OutputSurface] = field(default_factory=list)
    asset_conventions: AssetConventions = field(default_factory=AssetConventions)
    round_trip_surface: str = ""
    format_template_ref: FormatTemplateRef = field(default_factory=FormatTemplateRef)
    naming_convention: NamingConvention = field(default_factory=NamingConvention)

    def is_set(self) -> bool:
        return bool(
            self.length_window.is_set() or self.sections or self.output_surfaces
            or self.asset_conventions.is_set() or self.round_trip_surface
            or self.format_template_ref.is_set() or self.naming_convention.is_set()
        )


# ============================================================================================================
# Visual contract (LiteratureForge spec_visual_contract §1) — per-asset (V1–V8) + cross-asset (X1–X14).
# Every field is recorded as declarative intent; nothing here renders pixels or invokes an engine (PT-P5 boundary).
# ============================================================================================================

@dataclass(frozen=True)
class AssetVisual:                        # per-asset V1–V8
    substrate: str = "canvas"             # V1 canvas | raster
    producer_tool: str = ""               # V2 provenance only (TikZ|matplotlib|ComfyForge|native…)
    engine_route: str = ""                # V3 CanvasForge|ComfyForge|native|LaTeX — recorded, NOT invoked
    origin: str = "generated"             # V4 generated | captured | post_processed
    scorecard: tuple[str, ...] = ()       # V5 criteria names; n == len() (shape only; voices = p3_08)
    caption_form: str = "descriptive"     # V6 descriptive | claim_form
    target_page_fraction: float = 0.0     # V7 (0 == unset)
    intent_class: str = ""                # V8 hero | illustration | atmospheric | social_card


@dataclass(frozen=True)
class OrphanDetector:                     # X2 (config only; the traversal engine is a p3_08/PT-P5 voice)
    mode: str = "label_ref"               # label_ref | src_cited
    threshold: float = 0.0


@dataclass(frozen=True)
class BrandStylePackRef:                  # X3 (federation ref; LoRA/palette/typography deferred to the brand vault)
    vault: str = ""
    pack_id: str = ""
    version: str = ""

    def is_set(self) -> bool:
        return bool(self.vault)


@dataclass(frozen=True)
class StyleLock:                          # X5
    kind: str = "internal"                # internal | external
    provider: str = ""


@dataclass(frozen=True)
class CrossAssetVisual:                   # cross-asset X1–X14 (X6 lives per-surface on OutputSurface.aspect_ratio)
    engine_map: dict[str, str] = field(default_factory=dict)                  # X1 element-class -> engine
    orphan_detector: OrphanDetector = field(default_factory=OrphanDetector)   # X2
    brand_style_pack_ref: BrandStylePackRef = field(default_factory=BrandStylePackRef)  # X3
    color_signal_vocabulary: dict[str, str] = field(default_factory=dict)     # X4 signal -> color NAME (not RGB)
    style_lock: StyleLock = field(default_factory=StyleLock)                  # X5
    performance_budget: dict[str, Any] = field(default_factory=dict)          # X7 {max_kb, formats[]}
    naming_convention: NamingConvention = field(default_factory=NamingConvention)  # X8
    overlay_extends_base: bool = False                                        # X9
    visual_voices: tuple[str, ...] = ()                                       # X10 ids only (internals = p3_08)
    substrate_inheritance: str = "own"                                        # X11 inherit_parent | own
    surface_subclass: str = "print_page"                                      # X12 print_page | slide
    form_fill_exemption: bool = False                                         # X13
    export_round_trip: dict[str, str] = field(default_factory=dict)           # X14 {target, fidelity_note}


@dataclass(frozen=True)
class VisualContract:
    default_asset: AssetVisual = field(default_factory=AssetVisual)
    cross: CrossAssetVisual = field(default_factory=CrossAssetVisual)

    def is_set(self) -> bool:
        return self.default_asset != AssetVisual() or self.cross != CrossAssetVisual()


@dataclass(frozen=True)
class GenreProfile:
    """A genre's format + visual contracts. The empty profile (default) emits no contract metadata (E4.1-identical)."""

    name: str = ""
    format_spec: FormatContract = field(default_factory=FormatContract)
    visual_spec: VisualContract = field(default_factory=VisualContract)

    def is_set(self) -> bool:
        return bool(self.name) or self.format_spec.is_set() or self.visual_spec.is_set()


# Day-1 genre instances (spec_format_contract §3/§5 + spec_visual_contract §3/§6). Whitepaper + grant are fully
# worked; research/blog/exec are minimal stubs (per-genre integers co-tuned later — spec p3_06).
GENRE_PROFILES: dict[str, GenreProfile] = {
    "whitepaper": GenreProfile(
        name="whitepaper",
        format_spec=FormatContract(
            length_window=LengthWindow(5000, 15000, "words"),
            sections=[],  # submodule-owned convention; order_locked false (no external lock)
            output_surfaces=[OutputSurface("pdf_latex", "canonical", "print_page"),
                             OutputSurface("html", "derived", "")],
            asset_conventions=AssetConventions("booktabs", "amsmath", "float"),
            round_trip_surface="latex_source",
            naming_convention=NamingConvention("descriptive", "fig:N-name -> fig:slug")),
        visual_spec=VisualContract(
            default_asset=AssetVisual(
                substrate="canvas", producer_tool="TikZ", engine_route="CanvasForge", origin="generated",
                scorecard=("nodes", "argument", "readability", "standalone", "overcrowding"),
                caption_form="descriptive"),
            cross=CrossAssetVisual(
                engine_map={"image": "CanvasForge", "table": "CanvasForge"},
                orphan_detector=OrphanDetector("label_ref", 0.20),
                style_lock=StyleLock("internal", "lattice-styles.tex"),
                visual_voices=("visual_hierarchy", "figure_text_coherence", "composition", "accessibility"),
                surface_subclass="print_page")),
    ),
    "grant": GenreProfile(
        name="grant",
        format_spec=FormatContract(
            length_window=LengthWindow(0, 12, "pages"),
            sections=[SectionSpec("Specific Aims", True, True),
                      SectionSpec("Research Strategy", True, True),
                      SectionSpec("Budget Justification", True, True)],
            output_surfaces=[OutputSurface("pdf", "canonical", "print_page"),
                             OutputSurface("funder_portal", "derived", "")],
            asset_conventions=AssetConventions("plain", "mathml", "n/a (form-bypass)"),
            round_trip_surface="funder_portal_export",
            format_template_ref=FormatTemplateRef("funder", "NIH-R01", "structured_form"),
            naming_convention=NamingConvention("descriptive", "")),
        visual_spec=VisualContract(
            default_asset=AssetVisual(
                substrate="canvas", producer_tool="matplotlib", engine_route="CanvasForge", origin="generated",
                scorecard=("clarity", "page_budget", "standalone"), caption_form="descriptive",
                target_page_fraction=0.33),
            cross=CrossAssetVisual(
                engine_map={"image": "CanvasForge", "table": "CanvasForge"},
                orphan_detector=OrphanDetector("label_ref", 0.10),
                style_lock=StyleLock("external", "NIH"),
                visual_voices=("visual_hierarchy", "decision_density"),
                form_fill_exemption=True, surface_subclass="print_page")),
    ),
    # --- minimal stubs (length_window + template_ref from spec_format_contract §3; visual defaults minimal) ---
    "research": GenreProfile(
        name="research",
        format_spec=FormatContract(
            length_window=LengthWindow(4500, 8000, "words"),
            sections=[SectionSpec("Introduction", True, True), SectionSpec("Methods", True, True),
                      SectionSpec("Results", True, True), SectionSpec("Discussion", True, True)],
            output_surfaces=[OutputSurface("pdf_venue_latex", "canonical", "print_page"),
                             OutputSurface("html", "derived", "")],
            round_trip_surface="latex_source",
            format_template_ref=FormatTemplateRef("venue", "NeurIPS-2026", "style_file")),
        visual_spec=VisualContract(
            default_asset=AssetVisual(substrate="canvas", engine_route="CanvasForge"),
            cross=CrossAssetVisual(style_lock=StyleLock("external", "venue"))),
    ),
    "blog": GenreProfile(
        name="blog",
        format_spec=FormatContract(
            length_window=LengthWindow(800, 2000, "words"),
            output_surfaces=[OutputSurface("mdx", "canonical", "web")],
            round_trip_surface="mdx",
            format_template_ref=FormatTemplateRef("brand", "", "skeleton_doc")),
        visual_spec=VisualContract(
            default_asset=AssetVisual(substrate="raster", engine_route="ComfyForge", intent_class="illustration")),
    ),
    "exec": GenreProfile(
        name="exec",
        format_spec=FormatContract(
            length_window=LengthWindow(250, 1500, "words"),
            output_surfaces=[OutputSurface("md", "canonical", "")],
            round_trip_surface="md"),
        visual_spec=VisualContract(
            default_asset=AssetVisual(caption_form="claim_form"),
            cross=CrossAssetVisual(surface_subclass="slide",
                                   export_round_trip={"target": "pptx", "fidelity_note": "slide sub-class"})),
    ),
}


def _asset_from_dict(d: dict[str, Any]) -> AssetVisual:
    return AssetVisual(
        substrate=str(d.get("substrate", "canvas")),
        producer_tool=str(d.get("producer_tool", "")),
        engine_route=str(d.get("engine_route", "")),
        origin=str(d.get("origin", "generated")),
        scorecard=tuple(str(x) for x in d.get("scorecard", [])),
        caption_form=str(d.get("caption_form", "descriptive")),
        target_page_fraction=float(d.get("target_page_fraction", 0.0)),
        intent_class=str(d.get("intent_class", "")),
    )


# ============================================================================================================
# Document model.
# ============================================================================================================

@dataclass(frozen=True)
class Source:
    """A citation: a human label + a URL (-> a ``link`` node, ``citation`` component)."""

    label: str = ""
    url: str = ""


@dataclass(frozen=True)
class Block:
    """A rich block within a section. ``type`` selects which fields are meaningful."""

    type: str
    image: str = ""          # figure: a vault path (-> file node) or http url (-> link node)
    caption: str = ""        # figure caption
    table: Any = None        # table: a markdown string OR {headers:[...], rows:[[...]]}
    code: str = ""           # code block source
    lang: str = ""           # code block language hint (e.g. "python")
    text: str = ""           # quote text
    attribution: str = ""    # quote attribution
    items: list[str] = field(default_factory=list)  # list items
    asset: AssetVisual | None = None  # E4.2: per-figure visual-contract override (else the genre default applies)

    def __post_init__(self) -> None:
        if self.type not in BLOCK_TYPES:
            raise ValueError(f"unknown block type {self.type!r}; expected one of {sorted(BLOCK_TYPES)}")


@dataclass(frozen=True)
class Section:
    """An order-locked section: a heading, optional body prose, ordered rich blocks, and citations."""

    heading: str
    body: str = ""
    blocks: list[Block] = field(default_factory=list)
    sources: list[Source] = field(default_factory=list)
    section_kind: str = ""   # E4.2: maps to a format-contract SectionSpec.name (advisory order-lock); "" = unconstrained


@dataclass(frozen=True)
class Page:
    """A printed page (a paginated panel) holding one or more sections."""

    sections: list[Section]


@dataclass(frozen=True)
class Document:
    title: str
    id: str
    version: str
    pages: list[Page]
    refs: list[str] = field(default_factory=list)
    genre: GenreProfile = field(default_factory=GenreProfile)  # E4.2: format + visual contracts (empty => E4.1-identical)

    def word_count(self) -> int:
        """Approximate prose word count (LF ``length_window``) — body + list + quote + caption + heading text."""
        n = 0
        for page in self.pages:
            for sec in page.sections:
                n += len(sec.heading.split()) + len(sec.body.split())
                for blk in sec.blocks:
                    n += len(blk.text.split()) + len(blk.caption.split())
                    n += sum(len(it.split()) for it in blk.items)
        return n

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Document:
        genre_name = str(d.get("genre", ""))
        if genre_name and genre_name not in GENRE_PROFILES:
            raise ValueError(f"unknown genre {genre_name!r}; expected one of {sorted(GENRE_PROFILES)} (or omit)")
        genre = GENRE_PROFILES[genre_name] if genre_name else GenreProfile()

        pages: list[Page] = []
        for pg in d.get("pages", []):
            sections = [
                Section(
                    heading=str(s["heading"]),
                    body=str(s.get("body", "")).strip(),
                    blocks=[_block_from_dict(b) for b in s.get("blocks", [])],
                    sources=[
                        Source(label=str(c.get("label", "")), url=str(c.get("url", "")))
                        for c in s.get("sources", [])
                    ],
                    section_kind=str(s.get("section_kind", "")),
                )
                for s in pg.get("sections", [])
            ]
            if not sections:
                raise ValueError("page has no sections")
            pages.append(Page(sections=sections))
        if not pages:
            raise ValueError("document has no pages")
        return cls(
            title=str(d["title"]),
            id=str(d["id"]),
            version=str(d.get("version", "0.1.0")),
            refs=[str(r) for r in d.get("refs", [])],
            genre=genre,
            pages=pages,
        )


def _block_from_dict(b: dict[str, Any]) -> Block:
    return Block(
        type=str(b["type"]),
        image=str(b.get("image", "")),
        caption=str(b.get("caption", "")),
        table=b.get("table"),
        code=str(b.get("code", "")),
        lang=str(b.get("lang", "")),
        text=str(b.get("text", "")).strip(),
        attribution=str(b.get("attribution", "")),
        items=[str(x) for x in b.get("items", [])],
        asset=_asset_from_dict(b["asset"]) if isinstance(b.get("asset"), dict) else None,
    )


def load_document(path: str | Path) -> Document:
    """Load a document from ``.yaml``/``.yml`` (PyYAML) or ``.json``."""
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in (".yaml", ".yml"):
        import yaml

        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"document input {p} did not parse to a mapping")
    return Document.from_dict(data)
