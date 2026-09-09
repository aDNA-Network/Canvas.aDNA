"""Run manifest v0.1 — the ComfyUI→Canvas convenience interface (`spec_comfyui_canvas_emission` §3).

One JSON file per generation run, written beside the variants. ComfyUI's whole cost for the seam
is emitting this; Canvas's whole cost is reading it. Neither side imports the other — the seam is
files, never shared code.

    {"run_id": …, "created": …, "driver": "comfyui|comic_render|other",
     "slots": [{"slot_id": …,
                "variants": [{"variant_id": …, "path": "relative/to/manifest.png",
                              "workflow": …, "model": …, "seed": …, "denoise": …,
                              "lora_refs": [], "source_backend": …}]}]}

Four behaviours, each pinned by a fixture, and each chosen for a reason the spec states:

**The provenance floor is enforced, and absence is never fabricated.** §1.1 requires
``workflow · model · seed · denoise · lora_refs[] · source_backend`` per variant and says
*"defaults describe absence, never a model name"*. A missing ``model`` therefore becomes
:data:`ABSENT`, never ``"unknown"`` dressed as an id and never the last model seen. A review board
that silently attributes a variant to the wrong model poisons the RLHF record it feeds — the
``SelectionRecord`` keeps the attribution long after the board is gone.

**Unknown keys are ignored.** 0.x evolves additively (§3), so a manifest from a newer emitter must
load on an older consumer rather than fail closed. Unknown keys are *collected* rather than
dropped, so a caller can report what it did not understand instead of pretending it saw nothing.

**Paths resolve relative to the manifest**, not to a vault root or the cwd. The manifest travels
with its pixels.

**A variant is included iff its image exists on disk.** Inherited deliberately from
``review_canvas.load_variants``, which met a partially-failed run in the wild: rows with no
``output_path``, and one row recording ``success: false`` for a file that was actually there. The
run record is a *claim*; the filesystem is the fact. A generation batch that half-failed still
produces a reviewable board of what landed.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

#: Sentinel for a provenance field the manifest did not carry. Distinct from ``None`` (which a
#: manifest may legitimately supply) and from any real value — see the module docstring on why a
#: plausible-looking default is worse than an explicit gap.
ABSENT = "<absent>"

#: Provenance floor per `spec_comfyui_canvas_emission` §1.1.
PROVENANCE_FIELDS: tuple[str, ...] = (
    "workflow", "model", "seed", "denoise", "lora_refs", "source_backend",
)

#: Keys this loader understands, by level — anything else is surfaced via ``unknown_keys``.
_KNOWN_RUN_KEYS = {"run_id", "created", "driver", "slots"}
_KNOWN_SLOT_KEYS = {"slot_id", "variants", "prompt", "label"}
_KNOWN_VARIANT_KEYS = {"variant_id", "path", *PROVENANCE_FIELDS, "prompt", "label"}


class ManifestError(ValueError):
    """The manifest is unreadable or structurally invalid (not merely incomplete)."""


@dataclass(frozen=True)
class Variant:
    """One generated image offered for review, paired with the provenance behind it."""

    variant_id: str
    path: Path                       # absolute, verified to exist
    rel_path: str                    # as written in the manifest
    workflow: str
    model: str
    seed: Any
    denoise: Any
    lora_refs: tuple[str, ...]
    source_backend: str
    prompt: str = ""
    label: str = ""
    width: int = 0
    height: int = 0

    @property
    def missing_provenance(self) -> tuple[str, ...]:
        """Provenance-floor fields this variant did not carry (``lora_refs: []`` counts as present)."""
        gaps = [
            name for name in PROVENANCE_FIELDS
            if getattr(self, name) is ABSENT
        ]
        return tuple(gaps)


@dataclass(frozen=True)
class Slot:
    """One selection slot — a panel, a frame, a shot — holding the variants competing for it."""

    slot_id: str
    variants: tuple[Variant, ...]
    prompt: str = ""
    label: str = ""


@dataclass(frozen=True)
class RunManifest:
    """A parsed run manifest, plus what the loader could not account for."""

    run_id: str
    created: str
    driver: str
    slots: tuple[Slot, ...]
    manifest_path: Path
    unknown_keys: tuple[str, ...] = ()
    skipped: tuple[str, ...] = field(default=())

    @property
    def variant_count(self) -> int:
        return sum(len(slot.variants) for slot in self.slots)

    @property
    def provenance_gaps(self) -> dict[str, tuple[str, ...]]:
        """``variant_id -> missing floor fields`` for every variant with a gap."""
        return {
            variant.variant_id: variant.missing_provenance
            for slot in self.slots for variant in slot.variants
            if variant.missing_provenance
        }


def _coerce_lora_refs(raw: Any) -> tuple[str, ...] | str:
    if raw is ABSENT:
        return ABSENT
    if raw is None:
        return ()
    if isinstance(raw, (list, tuple)):
        return tuple(str(item) for item in raw)
    raise ManifestError(f"lora_refs must be a list, got {type(raw).__name__}")


def _load_variant(
    raw: dict[str, Any],
    *,
    base_dir: Path,
    slot_id: str,
    index: int,
    unknown: set[str],
    skipped: list[str],
) -> Variant | None:
    if not isinstance(raw, dict):
        raise ManifestError(f"slot {slot_id!r} variant {index}: expected an object")
    unknown.update(f"slots[].variants[].{key}" for key in raw if key not in _KNOWN_VARIANT_KEYS)

    variant_id = str(raw.get("variant_id") or f"{slot_id}_v{index}")
    rel = raw.get("path")
    if not rel:
        skipped.append(f"{variant_id}: no path")
        return None

    image = (base_dir / str(rel)).resolve()
    if not image.is_file():
        # The run record is a claim; the filesystem is the fact (see module docstring).
        skipped.append(f"{variant_id}: {rel} not on disk")
        return None

    width = height = 0
    if image.suffix.lower() == ".png":
        from canvas_core.rlhf.image_probe import png_dimensions
        try:
            width, height = png_dimensions(image)
        except (ValueError, OSError):
            skipped.append(f"{variant_id}: {rel} is not a readable PNG")
            return None

    return Variant(
        variant_id=variant_id,
        path=image,
        rel_path=str(rel),
        workflow=str(raw["workflow"]) if "workflow" in raw else ABSENT,
        model=str(raw["model"]) if "model" in raw else ABSENT,
        seed=raw.get("seed", ABSENT),
        denoise=raw.get("denoise", ABSENT),
        lora_refs=_coerce_lora_refs(raw["lora_refs"] if "lora_refs" in raw else ABSENT),
        source_backend=str(raw["source_backend"]) if "source_backend" in raw else ABSENT,
        prompt=str(raw.get("prompt", "") or ""),
        label=str(raw.get("label", "") or ""),
        width=width,
        height=height,
    )


def load_run_manifest(manifest_path: str | Path) -> RunManifest:
    """Parse a v0.1 run manifest. Raises :class:`ManifestError` on a structurally invalid file.

    Structural invalidity (not a JSON object, no ``slots``, a slot that is not an object) raises.
    *Incompleteness* — a missing provenance field, a variant whose image never landed — does not:
    it is recorded on the result, because a half-failed run is still reviewable and the caller is
    better placed than the loader to decide whether the gaps matter.
    """
    path = Path(manifest_path)
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManifestError(f"{path}: no such manifest") from exc
    except json.JSONDecodeError as exc:
        raise ManifestError(f"{path}: not valid JSON — {exc}") from exc
    if not isinstance(raw, dict):
        raise ManifestError(f"{path}: manifest must be a JSON object, got {type(raw).__name__}")

    raw_slots = raw.get("slots")
    if not isinstance(raw_slots, list) or not raw_slots:
        raise ManifestError(f"{path}: manifest has no slots[]")

    base_dir = path.parent
    unknown: set[str] = {key for key in raw if key not in _KNOWN_RUN_KEYS}
    skipped: list[str] = []
    slots: list[Slot] = []

    for slot_index, raw_slot in enumerate(raw_slots):
        if not isinstance(raw_slot, dict):
            raise ManifestError(f"{path}: slots[{slot_index}] must be an object")
        unknown.update(f"slots[].{key}" for key in raw_slot if key not in _KNOWN_SLOT_KEYS)
        slot_id = str(raw_slot.get("slot_id") or f"slot_{slot_index + 1}")
        raw_variants = raw_slot.get("variants") or []
        if not isinstance(raw_variants, list):
            raise ManifestError(f"{path}: slot {slot_id!r} variants must be a list")

        variants = [
            variant for index, raw_variant in enumerate(raw_variants)
            if (variant := _load_variant(
                raw_variant, base_dir=base_dir, slot_id=slot_id, index=index,
                unknown=unknown, skipped=skipped)) is not None
        ]
        if not variants:
            skipped.append(f"{slot_id}: no variants on disk")
            continue
        slots.append(Slot(
            slot_id=slot_id,
            variants=tuple(variants),
            prompt=str(raw_slot.get("prompt", "") or ""),
            label=str(raw_slot.get("label", "") or ""),
        ))

    if not slots:
        raise ManifestError(
            f"{path}: no slot has a variant image on disk "
            f"({len(skipped)} skipped: {'; '.join(skipped[:5])})"
        )

    return RunManifest(
        run_id=str(raw.get("run_id") or path.stem),
        created=str(raw.get("created") or ""),
        driver=str(raw.get("driver") or "other"),
        slots=tuple(slots),
        manifest_path=path,
        unknown_keys=tuple(sorted(unknown)),
        skipped=tuple(skipped),
    )
