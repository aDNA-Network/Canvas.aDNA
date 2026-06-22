"""Image generation wiring — connect PendingImage / PendingPanel lifecycles to
image clients via a substrate-neutral Protocol.

This module is **Protocol-only** orchestration: it never imports an image SDK
itself. Callers supply a client conforming to :class:`ImageClient` and let
:meth:`ImagenWiring.generate_variants` drive the calls, or they generate
images via any other mechanism (MCP tool, manual upload, fixture) and hand the
resulting paths back via the selection-canvas builders.

Selection workflow uses **delete-the-losers** in Obsidian: the user opens the
selection canvas, deletes the variant files they don't want, and then
the resolve methods enforce "exactly one survives" and wire the survivor into
the source builder.

Migrated from lattice-protocol/extensions/canvas/canvas_image_generation.py
(M-1-05). Application-type imports (ComicPageBuilder, PresentationBuilder)
replaced with Any — the types are TYPE_CHECKING-only in upstream and the
application packages aren't populated yet (Wave 2).

M-1-05 additions per ADR 003:
- ImageRequest dataclass (substrate-neutral request type)
- ImageClient Protocol extended with federation_ref + backend_preference docs
- Gemini/Imagen is substrate-wide v1.0 default (adapter wiring is runtime)
- Tier 1 ComfyForge adapter is style-transfer-experimental (deferred to M-3-05)
"""

from __future__ import annotations

import json
import warnings
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol


# ---------------------------------------------------------------------------
# Image request (M-1-05 / ADR 003 — substrate-neutral)
# ---------------------------------------------------------------------------


@dataclass
class ImageRequest:
    """Substrate-neutral image generation request.

    Application-agnostic: the same dataclass is used for comic panels,
    deck hero slides, inline beautification assets, and future diagram
    illustrations. Adapter implementations (Gemini, ComfyForge, etc.)
    translate these fields to their own SDK-specific parameters.

    Per ADR 003: Gemini/Imagen Ultra is the substrate-wide v1.0 default.
    ComfyForge is a style-transfer engine (Tier 1 experimental), not an
    alternative production backend.
    """

    prompt: str
    output_path: str | None = None
    application: str = "generic"  # "comic", "deck", "inline", "diagram", "generic"
    aspect_ratio: str = "1:1"  # "1:1", "16:9", "9:16", "4:3", "3:4"
    register: str = ""  # e.g., "ghibli", "pixel", "transition" (Dual Worlds)
    budget_class: str = "standard"  # "economy", "standard", "premium"
    style_hints: str = ""  # free-form style instruction for adapter
    model_tier: str = "ultra"  # "ultra", "standard" — adapter-internal mapping
    backend_preference: list[str] = field(
        default_factory=lambda: ["gemini"]
    )  # ["gemini", "comfyforge_anduril", "mac_mps"]
    federation_ref: str = ""  # e.g., "canvasforge" — which forge to route to


# ---------------------------------------------------------------------------
# Dual-prompt payload (M-R2-02 / spec § 7.1 — review-campaign Phase R2)
# ---------------------------------------------------------------------------


@dataclass
class ImagePrompt:
    """Substrate-neutral dual-prompt request payload.

    Replaces the str-only prompt path with a structured ``text + optional
    mermaid_layout`` shape. ``ImageClient`` adapters accept ``ImagePrompt``
    (preferred) or ``str`` (backcompat); when given ``str``, adapters wrap it
    as ``ImagePrompt(text=<str>)`` internally and emit a ``DeprecationWarning``
    starting v1.1, with sunset at v1.2.

    The optional ``mermaid_layout`` field carries an application-specific
    spatial-layout description (e.g. comic ``comic_panel_layout`` schema in
    ``canvas_comic/mermaid_layout.py``). When present, ``assemble_dual_prompt``
    in the consuming application module concatenates wrapper + text + mermaid
    into a single Imagen-4 input. Deck hero / cover slides typically leave
    ``mermaid_layout=None`` and use the single-prompt path per ADR 003
    (Imagen substrate-default for ALL canvas applications).

    The optional ``compositional_intent`` field (S5 — M-V1-2-F-01 2026-05-26;
    per ADR-005 § D5 amendment landed at this session) carries a free-text
    compositional anchor that surfaces in the Imagen-4 instruction as a third
    dual-prompt segment ``[PART 3: COMPOSITIONAL INTENT]`` alongside PART 1
    (text) and PART 2 (spatial layout). Substrate is opaque to the intent
    string — applications supply it from their own RLHF corpus / Visual-DNA
    bundles / authoring choices (substrate-neutrality discipline; see ADR-008
    § D4 for the full back-flow path). Default ``None`` preserves all
    existing call-site behavior verbatim (re-baseline gate guarantee per
    Q5 + CR1 + CR2). Re-merge rationale:
    ``lattice-labs/who/coordination/coord_2026_04_16_forge_split.md``.
    """

    text: str
    mermaid_layout: str | None = None
    compositional_intent: str | None = None
    aspect_ratio: str = "1:1"


def _coerce_prompt(prompt: ImagePrompt | str) -> ImagePrompt:
    """Wrap str-shaped prompts as ImagePrompt(text=...).

    Backcompat shim for the pre-M-R2-02 str-only prompt API. Emits a
    DeprecationWarning starting at CanvasForge v1.1; the str path is
    sunset at v1.2 (per Q4 default — one-version migration window).
    Used by all ImageClient adapters and ImagenWiring at the entry point
    so downstream code can rely on ImagePrompt shape.
    """
    if isinstance(prompt, str):
        warnings.warn(
            "Passing str to generate_image is deprecated; use ImagePrompt. "
            "Sunset at CanvasForge v1.2.",
            DeprecationWarning,
            stacklevel=2,
        )
        return ImagePrompt(text=prompt)
    return prompt


# ---------------------------------------------------------------------------
# Image client protocol
# ---------------------------------------------------------------------------


class ImageClient(Protocol):
    """Minimal interface for an image-generation client.

    Conformed to by ``latlab.mcp.image.server.GeminiImageClient`` and any
    drop-in mock used in tests.

    M-R2-02 upgrade (per spec § 7.4): ``prompt`` accepts ``ImagePrompt``
    (preferred) or ``str`` (backcompat). Adapters wrap str inputs as
    ``ImagePrompt(text=<str>)`` via :func:`_coerce_prompt`; ``DeprecationWarning``
    emitted starting v1.1, str path sunset at v1.2 (per Q4 default).

    Federation extension (M-1-05 / ADR 003):
        Concrete adapters may accept ``federation_ref`` and
        ``backend_preference`` in their constructors to support multi-backend
        routing. The Protocol itself is kept minimal — a single
        ``generate_image()`` method — so that simple mocks remain one-liners.
        Use ``ImageRequest`` for richer request semantics.
    """

    def generate_image(
        self,
        prompt: ImagePrompt | str,
        output_path: str | None = None,
        style: str = "photo",
        aspect_ratio: str = "1:1",
        image_size: str = "2K",
        model: str = "ultra",
    ) -> dict[str, Any]: ...


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class VariantSet:
    """Describes a set of generated variants for one pending item."""

    item_id: str  # panel_id or pending_image_id
    kind: str  # "panel" or "pending_image"
    prompt: str
    aspect_ratio: str
    target_dir: str
    variant_paths: list[str] = field(default_factory=list)
    selection_board_path: str | None = None


# ---------------------------------------------------------------------------
# Wiring
# ---------------------------------------------------------------------------


class ImagenWiring:
    """Wire pending image / panel records to an image generation client.

    The class itself holds no I/O credentials and never imports an SDK. It is
    safe to instantiate in tests with no arguments. Pass a client (real or
    fake) per call to :meth:`generate_variants` or skip that helper entirely
    and feed paths in directly.

    Conventions:
      * Variant files are named ``{item_id}_v{N}.png`` (1-indexed).
      * Selection canvas files are named ``{item_id}_selection.canvas``.
      * Sidecar records are named ``{item_id}.selection.json``.

    Application builder types (ComicPageBuilder, PresentationBuilder) are
    accepted as Any — the module accesses their methods via duck typing.
    Concrete type annotations arrive when Wave 2 populates the application
    packages.
    """

    DEFAULT_MODEL = "pro"
    DEFAULT_STYLE = "photo"
    VARIANT_FILENAME = "{item_id}_v{n}.png"
    SELECTION_FILENAME = "{item_id}_selection.canvas"
    SIDECAR_FILENAME = "{item_id}.selection.json"

    def __init__(
        self,
        default_model: str = DEFAULT_MODEL,
        default_style: str = DEFAULT_STYLE,
        default_count: int = 3,
    ) -> None:
        self.default_model = default_model
        self.default_style = default_style
        self.default_count = default_count

    # ------------------------------------------------------------------
    # Path planning (pure functions — no I/O)
    # ------------------------------------------------------------------

    def variant_path(self, target_dir: str | Path, item_id: str, n: int) -> Path:
        """Return the canonical path for variant ``n`` of ``item_id``."""
        return Path(target_dir) / self.VARIANT_FILENAME.format(item_id=item_id, n=n)

    def selection_canvas_path(self, target_dir: str | Path, item_id: str) -> Path:
        """Return the canonical path for the selection canvas of ``item_id``."""
        return Path(target_dir) / self.SELECTION_FILENAME.format(item_id=item_id)

    def sidecar_path(self, target_dir: str | Path, item_id: str) -> Path:
        """Return the canonical path for the selection sidecar of ``item_id``."""
        return Path(target_dir) / self.SIDECAR_FILENAME.format(item_id=item_id)

    def prepare_variant_paths(
        self,
        target_dir: str | Path,
        item_id: str,
        count: int | None = None,
    ) -> list[Path]:
        """List the planned variant paths for ``item_id`` (no files created)."""
        n_variants = count if count is not None else self.default_count
        return [self.variant_path(target_dir, item_id, i + 1) for i in range(n_variants)]

    # ------------------------------------------------------------------
    # Client-driven generation (optional convenience)
    # ------------------------------------------------------------------

    def generate_variants(
        self,
        client: ImageClient,
        prompt: ImagePrompt | str,
        aspect_ratio: str,
        target_dir: str | Path,
        item_id: str,
        count: int | None = None,
        model: str | None = None,
        style: str | None = None,
    ) -> list[str]:
        """Drive ``client.generate_image`` ``count`` times for one item.

        M-R2-02: ``prompt`` accepts ``ImagePrompt`` (preferred) or ``str``
        (backcompat with DeprecationWarning, sunset v1.2). The downstream
        ``client.generate_image`` is called with ``prompt_obj.text`` —
        concrete clients (e.g. ``GeminiImageClient``) may not yet absorb
        ImagePrompt; forwarding the text keeps the inner contract str-only
        until the broader concrete-client migration lands.

        Returns a list of saved file paths in variant order. Raises
        :class:`RuntimeError` with all collected errors if any call fails.
        """
        prompt_obj = _coerce_prompt(prompt)
        target = Path(target_dir)
        target.mkdir(parents=True, exist_ok=True)
        n_variants = count if count is not None else self.default_count
        used_model = model if model is not None else self.default_model
        used_style = style if style is not None else self.default_style

        saved: list[str] = []
        errors: list[str] = []
        for i in range(n_variants):
            out_path = self.variant_path(target, item_id, i + 1)
            result = client.generate_image(
                prompt=prompt_obj.text,
                output_path=str(out_path),
                style=used_style,
                aspect_ratio=aspect_ratio,
                model=used_model,
            )
            if result.get("success"):
                saved.append(result.get("image_path", str(out_path)))
            else:
                errors.append(f"variant {i + 1}: {result.get('error', 'unknown error')}")

        if errors:
            raise RuntimeError(
                f"generate_variants failed for {item_id}: " + "; ".join(errors)
            )
        return saved

    # ------------------------------------------------------------------
    # Selection canvas construction
    # ------------------------------------------------------------------

    def build_panel_selection_canvas(
        self,
        comic_builder: Any,
        panel_id: str,
        variant_paths: list[str],
        output_path: str | Path,
        labels: list[str] | None = None,
    ) -> Path:
        """Save a selection canvas for one comic panel's variants.

        Args:
            comic_builder: ComicPageBuilder instance (duck-typed; Wave 2
                adds concrete type annotation).
        """
        board = comic_builder.generate_panel_variants(
            panel_id=panel_id,
            variant_paths=variant_paths,
            variant_labels=labels,
        )
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        board.save(str(out))
        return out

    def build_image_selection_canvas(
        self,
        presentation_builder: Any,
        pending_id: str,
        variant_paths: list[str],
        output_path: str | Path,
        labels: list[str] | None = None,
    ) -> Path:
        """Save a selection canvas for one PendingImage's variants.

        Args:
            presentation_builder: PresentationBuilder instance (duck-typed;
                Wave 2 adds concrete type annotation).
        """
        cb = presentation_builder._cb  # noqa: SLF001 — internal CanvasBuilder
        variants = [
            {"id": cb.generate_id(), "file": path} for path in variant_paths
        ]
        used_labels = labels or [f"Variant {i + 1}" for i in range(len(variant_paths))]
        board = cb.selection_board(
            variants=variants,
            labels=used_labels,
            title=f"PendingImage {pending_id} — Variant Selection",
        )
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        board.save(str(out))
        return out

    # ------------------------------------------------------------------
    # Resolution after Herb deletes the losers
    # ------------------------------------------------------------------

    def find_survivors(
        self,
        target_dir: str | Path,
        item_id: str,
    ) -> list[Path]:
        """Return surviving variant files for ``item_id`` in ``target_dir``."""
        target = Path(target_dir)
        if not target.exists():
            return []
        prefix = f"{item_id}_v"
        return sorted(
            p for p in target.iterdir()
            if p.is_file() and p.name.startswith(prefix) and p.suffix == ".png"
        )

    def resolve_panel_with_choice(
        self,
        comic_builder: Any,
        panel_id: str,
        selected_path: str | Path,
        all_variant_paths: list[str] | Path | None = None,
        sidecar_dir: str | Path | None = None,
    ) -> str:
        """Wire an explicitly-chosen variant into the comic builder."""
        chosen = str(selected_path)
        comic_builder.resolve_panel(panel_id, chosen)
        if sidecar_dir is not None:
            self.write_selection_record(
                item_id=panel_id,
                kind="panel",
                all_variant_paths=[str(p) for p in (all_variant_paths or [chosen])],
                selected_path=chosen,
                sidecar_dir=sidecar_dir,
            )
        return chosen

    def resolve_image_with_choice(
        self,
        presentation_builder: Any,
        pending_id: str,
        selected_path: str | Path,
        all_variant_paths: list[str] | Path | None = None,
        sidecar_dir: str | Path | None = None,
    ) -> str:
        """Wire an explicitly-chosen variant into the presentation builder."""
        chosen = str(selected_path)
        presentation_builder.resolve_pending_image(pending_id, chosen)
        if sidecar_dir is not None:
            self.write_selection_record(
                item_id=pending_id,
                kind="pending_image",
                all_variant_paths=[str(p) for p in (all_variant_paths or [chosen])],
                selected_path=chosen,
                sidecar_dir=sidecar_dir,
            )
        return chosen

    def resolve_panel_from_surviving_files(
        self,
        comic_builder: Any,
        panel_id: str,
        variant_dir: str | Path,
        sidecar_dir: str | Path | None = None,
        all_variant_paths: list[str] | None = None,
    ) -> str:
        """Legacy delete-the-losers resolution path.

        Prefer :meth:`resolve_panel_with_choice` — preserving all variants on
        disk is more useful for RLHF datasets, future re-prompts, and audit
        trails.
        """
        survivors = self.find_survivors(variant_dir, panel_id)
        selected = self._enforce_single_survivor(panel_id, survivors)
        comic_builder.resolve_panel(panel_id, str(selected))
        if sidecar_dir is not None:
            self.write_selection_record(
                item_id=panel_id,
                kind="panel",
                all_variant_paths=all_variant_paths or [str(s) for s in survivors],
                selected_path=str(selected),
                sidecar_dir=sidecar_dir,
            )
        return str(selected)

    def resolve_image_from_surviving_files(
        self,
        presentation_builder: Any,
        pending_id: str,
        variant_dir: str | Path,
        sidecar_dir: str | Path | None = None,
        all_variant_paths: list[str] | None = None,
    ) -> str:
        """After user deletes losers, wire the survivor into the builder."""
        survivors = self.find_survivors(variant_dir, pending_id)
        selected = self._enforce_single_survivor(pending_id, survivors)
        presentation_builder.resolve_pending_image(pending_id, str(selected))
        if sidecar_dir is not None:
            self.write_selection_record(
                item_id=pending_id,
                kind="pending_image",
                all_variant_paths=all_variant_paths or [str(s) for s in survivors],
                selected_path=str(selected),
                sidecar_dir=sidecar_dir,
            )
        return str(selected)

    @staticmethod
    def _enforce_single_survivor(item_id: str, survivors: list[Path]) -> Path:
        if len(survivors) == 0:
            raise RuntimeError(
                f"resolve: no surviving variants for {item_id!r}. "
                "Did you delete all of them by mistake?"
            )
        if len(survivors) > 1:
            names = ", ".join(p.name for p in survivors)
            raise RuntimeError(
                f"resolve: {len(survivors)} variants survive for {item_id!r} "
                f"({names}). Delete all but one, then retry."
            )
        return survivors[0]

    # ------------------------------------------------------------------
    # Sidecar audit log
    # ------------------------------------------------------------------

    def write_selection_record(
        self,
        item_id: str,
        kind: str,
        all_variant_paths: list[str],
        selected_path: str,
        sidecar_dir: str | Path,
    ) -> Path:
        """Write ``{item_id}.selection.json`` recording the choice."""
        if kind not in ("panel", "pending_image"):
            raise ValueError(f"kind must be 'panel' or 'pending_image', got {kind!r}")
        sidecar = self.sidecar_path(sidecar_dir, item_id)
        sidecar.parent.mkdir(parents=True, exist_ok=True)

        try:
            selected_index = all_variant_paths.index(selected_path) + 1
        except ValueError:
            selected_name = Path(selected_path).name
            selected_index = next(
                (
                    i + 1
                    for i, p in enumerate(all_variant_paths)
                    if Path(p).name == selected_name
                ),
                None,
            )

        record = {
            "item_id": item_id,
            "kind": kind,
            "selected_at": datetime.now(timezone.utc).isoformat(),
            "all_variants": list(all_variant_paths),
            "selected": selected_path,
            "selected_index": selected_index,
        }
        sidecar.write_text(json.dumps(record, indent=2) + "\n")
        return sidecar
