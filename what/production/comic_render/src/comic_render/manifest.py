"""Render manifest v0.1 — the bridge's resumable sidecar state (roadmap §1).

``issue.canvas`` → (plan) → ``issue.render_manifest.json``. The manifest is the single source of
run state: every stage reads it, does idempotent work, and records results back into it. The
**hybrid interop is a first-class chain, not a backend switch** — each panel carries an ordered
``render_chain`` of stages (``generate`` → optional ``refine``).

Spec fields are the operator-approved v0.1 contract; per-panel ``results`` (variants · refined ·
selection) and header ``spend`` are the stages' bookkeeping, additive to the contract.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from comic_render import MANIFEST_SCHEMA_VERSION

# qualities.status vocabulary (producer emits the first two; "skip" is a manifest-level policy value)
STATUS_PROMPT_ONLY = "prompt_only"
STATUS_RENDERED = "rendered"
STATUS_SKIP = "skip"

VALID_STAGES = ("generate", "refine")


def default_seed(comic_id: str, panel_id: str) -> int:
    """Deterministic per-panel seed: ``sha256(comic_id + ":" + panel_id)`` → 63-bit int."""
    digest = hashlib.sha256(f"{comic_id}:{panel_id}".encode()).digest()
    return int.from_bytes(digest[:8], "big") >> 1  # keep it positive in any signed context


def prompt_hash(text: str) -> str:
    """16-hex fingerprint of a prompt text (provenance field)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


@dataclass
class RenderStage:
    """One ordered stage of a panel's render chain."""

    stage: str  # "generate" | "refine"
    backend: str  # "fake" | "gemini" | "comfy"
    workflow: str | None = None  # comfy workflow name (refine)
    seed_image: str | None = None  # refine input override; default = prior stage output
    denoise: float | None = None  # refine strength

    def __post_init__(self) -> None:
        if self.stage not in VALID_STAGES:
            raise ValueError(f"render_chain stage must be one of {VALID_STAGES}, got {self.stage!r}")


@dataclass
class PanelSpec:
    """Per-panel render manifest entry (v0.1 contract fields + stage ``results``)."""

    panel_id: str
    page_number: int
    reading_index: int
    status: str  # prompt_only | rendered | skip
    prompt_text: str
    aspect_ratio: str
    target_px: dict[str, int]  # {"w": int, "h": int} — panel geometry → print px
    seed: int
    variant_count: int
    output_dir: str  # relative to the manifest's directory
    prompt_layers: dict[str, str] | None = None  # incl. the separate "negative" channel (H1)
    dual_prompt: str | None = None
    spatial_layout: str | None = None
    compositional_intent: str | None = None
    characters: list[dict[str, Any]] = field(default_factory=list)  # H5 VisualDNA compose
    existing_image_path: str | None = None
    render_chain: list[RenderStage] = field(default_factory=list)
    results: dict[str, Any] = field(default_factory=dict)  # stages write: variants/refined/selection

    @property
    def negative(self) -> str | None:
        """The separate negative channel (never inlined into ``prompt_text`` for chain backends)."""
        return (self.prompt_layers or {}).get("negative")

    def final_outputs(self) -> list[str]:
        """The variant list selection operates on: last completed chain stage's outputs."""
        refined = self.results.get("refined") or []
        if refined:
            return list(refined)
        return list(self.results.get("variants") or [])


@dataclass
class RenderManifest:
    """Header + panels. Serialized as ``<canvas stem>.render_manifest.json`` beside the canvas."""

    comic_id: str
    source_canvas: str  # relative to the manifest's directory
    source_sync_hash: str
    backend_policy: dict[str, Any]  # {"default_chain": [stage dicts], "allow_fallback": bool}
    budget_cap: float | None = None  # USD; None = uncapped
    schema_version: str = MANIFEST_SCHEMA_VERSION
    register: str = "comic_default"  # RLHF SelectionRecord register for this run
    panels: list[PanelSpec] = field(default_factory=list)
    spend: dict[str, Any] = field(default_factory=dict)  # dispatch writes {"usd": float, "calls": int}

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        for p in d["panels"]:
            p["render_chain"] = [
                {k: v for k, v in s.items() if v is not None} for s in p["render_chain"]
            ]
            for opt in ("prompt_layers", "dual_prompt", "spatial_layout",
                        "compositional_intent", "existing_image_path"):
                if p[opt] is None:
                    del p[opt]
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RenderManifest:
        panels = []
        for p in data.get("panels", []):
            chain = [RenderStage(**s) for s in p.get("render_chain", [])]
            panels.append(PanelSpec(**{**p, "render_chain": chain}))
        return cls(**{**data, "panels": panels})

    def save(self, path: str | Path) -> Path:
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(self.to_dict(), indent=2) + "\n")
        return out

    @classmethod
    def load(cls, path: str | Path) -> RenderManifest:
        data = json.loads(Path(path).read_text())
        got = data.get("schema_version")
        if got != MANIFEST_SCHEMA_VERSION:
            raise ValueError(
                f"manifest schema_version {got!r} != supported {MANIFEST_SCHEMA_VERSION!r}"
            )
        return cls.from_dict(data)

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def panel(self, panel_id: str) -> PanelSpec:
        for p in self.panels:
            if p.panel_id == panel_id:
                return p
        raise KeyError(f"no panel {panel_id!r} in manifest {self.comic_id!r}")

    def dispatchable(self) -> list[PanelSpec]:
        """Panels the dispatch stage acts on (not already rendered, not skipped)."""
        return [p for p in self.panels if p.status == STATUS_PROMPT_ONLY]


def manifest_path_for(canvas_path: str | Path) -> Path:
    """``issue.canvas`` → ``issue.render_manifest.json`` (sidecar beside the canvas)."""
    c = Path(canvas_path)
    return c.with_name(c.stem + ".render_manifest.json")


def rendered_canvas_path_for(canvas_path: str | Path) -> Path:
    """``issue.canvas`` → ``issue.rendered.canvas`` (the NEW write-back target; input immutable)."""
    c = Path(canvas_path)
    return c.with_name(c.stem + ".rendered.canvas")
