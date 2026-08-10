"""Vision-model client adapters for canvas critique.

Substrate-neutral Protocol + concrete adapters for Gemini 2.5 Flash
(default) and Claude with vision (optional).  Vision-model selection is
per-call and independent of ADR 003's ImageClient doctrine — critique
and image-gen are separate concerns.

New in M-1-08.  Pure substrate.
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

_log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class VisionRequest:
    """Request to a vision model for critique analysis."""

    images: list[Path]              # PNG screenshot paths
    prompt: str                     # filled prompt template
    structured_schema: dict | None = None  # JSON schema for output
    group_id: str = ""              # which canvas group this covers
    budget_cap_usd: float = 0.08


@dataclass
class VisionResponse:
    """Response from a vision model."""

    raw_text: str = ""
    parsed_findings: list[dict] = None  # type: ignore[assignment]
    cost_usd: float = 0.0
    duration_s: float = 0.0
    model_id: str = ""
    success: bool = True
    error: str = ""

    def __post_init__(self) -> None:
        if self.parsed_findings is None:
            self.parsed_findings = []


# ---------------------------------------------------------------------------
# Protocol
# ---------------------------------------------------------------------------


@runtime_checkable
class VisionClient(Protocol):
    """Protocol for vision-model adapters."""

    model_id: str

    def analyze(self, request: VisionRequest) -> VisionResponse:
        """Send images + prompt to the vision model and return findings."""
        ...


# ---------------------------------------------------------------------------
# Gemini adapter
# ---------------------------------------------------------------------------


class GeminiVisionAdapter:
    """Gemini vision adapter (default), bound to the shared Google model layer.

    **Migrated 2026-08-10.** This was the fleet's last consumer of ``google.generativeai`` — the
    retired standalone SDK — and it pinned ``gemini-2.5-flash`` as a literal, three generations
    behind what the service now offers. Both problems were the same problem: a call site holding its
    own model knowledge. Model resolution, credential lanes and pricing now come from
    ``Home.aDNA/what/code/googleai/``.

    There is no separate "vision model": Gemini models are natively multimodal, so a vision call is
    a text call with image parts. ``model`` is a capability alias (``text.flash``), not an ID.
    """

    model_id: str = "text.flash"

    def __init__(self, model: str = "text.flash", api_key: str | None = None):
        self.model_id = model
        self._api_key = api_key  # accepted for back-compat; lane resolution is the shared layer's

    def analyze(self, request: VisionRequest) -> VisionResponse:
        """Call the vision model with screenshot images."""
        t0 = time.monotonic()
        try:
            googleai = _require_googleai()
        except ImportError as exc:
            return VisionResponse(success=False, error=str(exc), model_id=self.model_id)

        try:
            client = googleai.get_client()
            result = client.generate_text(
                request.prompt, model=self.model_id, images=list(request.images)
            )
            if not result.get("success"):
                return VisionResponse(
                    success=False, error=result.get("error", "unknown"),
                    duration_s=time.monotonic() - t0, model_id=self.model_id,
                )
            raw = result["text"]
            return VisionResponse(
                raw_text=raw,
                parsed_findings=_parse_findings_json(raw),
                cost_usd=_estimate_gemini_cost(request, raw),
                duration_s=time.monotonic() - t0,
                model_id=result.get("model", self.model_id),
                success=True,
            )
        except Exception as exc:
            _log.warning("Gemini vision call failed: %s", exc)
            return VisionResponse(
                success=False,
                error=str(exc),
                duration_s=time.monotonic() - t0,
                model_id=self.model_id,
            )


# ---------------------------------------------------------------------------
# Claude adapter
# ---------------------------------------------------------------------------


class ClaudeVisionAdapter:
    """Claude vision adapter (optional).

    Requires the ``anthropic`` SDK.  Guarded.
    """

    model_id: str = "claude-sonnet-4-20250514"

    def __init__(self, model: str = "claude-sonnet-4-20250514", api_key: str | None = None):
        self.model_id = model
        self._api_key = api_key

    def analyze(self, request: VisionRequest) -> VisionResponse:
        """Call Claude vision API with screenshot images."""
        t0 = time.monotonic()
        try:
            import anthropic  # type: ignore[import-untyped]
        except ImportError:
            return VisionResponse(
                success=False,
                error="anthropic SDK not installed",
                model_id=self.model_id,
            )

        try:
            import base64

            client = anthropic.Anthropic(api_key=self._api_key) if self._api_key else anthropic.Anthropic()

            content: list[dict[str, Any]] = []
            for img_path in request.images:
                with open(img_path, "rb") as f:
                    b64 = base64.standard_b64encode(f.read()).decode()
                content.append({
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": b64},
                })
            content.append({"type": "text", "text": request.prompt})

            response = client.messages.create(
                model=self.model_id,
                max_tokens=2048,
                messages=[{"role": "user", "content": content}],
            )
            raw = response.content[0].text

            findings = _parse_findings_json(raw)
            duration = time.monotonic() - t0

            return VisionResponse(
                raw_text=raw,
                parsed_findings=findings,
                cost_usd=_estimate_claude_cost(response),
                duration_s=duration,
                model_id=self.model_id,
                success=True,
            )

        except Exception as exc:
            _log.warning("Claude vision call failed: %s", exc)
            return VisionResponse(
                success=False,
                error=str(exc),
                duration_s=time.monotonic() - t0,
                model_id=self.model_id,
            )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Known adapter map. Google entries are CAPABILITY ALIASES resolved by the shared registry, not
# model IDs — which is why a Google model can be superseded without touching this file. The legacy
# `gemini-2.5-flash` literal is retained as a key so existing callers keep working; it resolves
# through the same registry.
VISION_ADAPTERS: dict[str, type] = {
    "text.flash": GeminiVisionAdapter,
    "text.pro": GeminiVisionAdapter,
    "text.lite": GeminiVisionAdapter,
    "gemini-2.5-flash": GeminiVisionAdapter,   # legacy pin, still resolvable
    "claude-sonnet-vision": ClaudeVisionAdapter,
    "claude-opus-vision": ClaudeVisionAdapter,
}

DEFAULT_VISION_MODEL = "text.flash"


def get_vision_client(model: str = DEFAULT_VISION_MODEL, **kwargs: Any) -> VisionClient:
    """Construct a vision client by capability alias (or a legacy model name)."""
    adapter_cls = VISION_ADAPTERS.get(model)
    if adapter_cls is None:
        raise ValueError(f"Unknown vision model: {model!r}. Known: {list(VISION_ADAPTERS)}")
    return adapter_cls(model=model, **kwargs)  # type: ignore[call-arg]


def _require_googleai() -> Any:
    """Reach the shared Google model layer (Home.aDNA, local-by-default, unpackaged).

    Mirrors ``canvas_core/rlhf/review_collect.py::_ensure_canvas_context`` — the vault's established
    way to reach an unpackaged sibling shelf — and fails with a message naming the dependency rather
    than a bare ModuleNotFoundError.
    """
    import os
    import sys
    from importlib.util import find_spec
    from pathlib import Path

    if find_spec("googleai") is None:
        override = os.environ.get("GOOGLEAI_PATH")
        root = Path(override) if override else None
        if root is None:
            for parent in Path(__file__).resolve().parents:
                candidate = parent / "Home.aDNA" / "what" / "code"
                if (candidate / "googleai" / "__init__.py").exists():
                    root = candidate
                    break
        if root is None or not (root / "googleai" / "__init__.py").exists():
            raise ImportError(
                "the shared Google model layer (Home.aDNA/what/code/googleai) was not found. "
                "It is local-by-default, so a node without Home.aDNA does not have it. Set "
                "GOOGLEAI_PATH, or use a non-Google vision adapter."
            )
        sys.path.append(str(root))  # append, never insert(0) — Home's shelf must not shadow
    import googleai

    return googleai


def _parse_findings_json(raw_text: str) -> list[dict]:
    """Extract JSON findings array from vision model response.

    Handles cases where the model wraps JSON in markdown code fences.
    """
    text = raw_text.strip()

    # Strip markdown code fences.
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last lines (fences).
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines).strip()

    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict) and "findings" in parsed:
            return parsed["findings"]
        return [parsed]
    except json.JSONDecodeError:
        _log.debug("Could not parse vision response as JSON")
        return []


def _estimate_gemini_cost(request: VisionRequest, response_text: str) -> float:
    """Rough cost estimate for Gemini 2.5 Flash (2026-04 pricing)."""
    # ~$0.00015/image + ~$0.000001/token output. Very rough.
    image_cost = len(request.images) * 0.00015
    token_cost = len(response_text) / 4 * 0.000001  # ~4 chars/token
    return image_cost + token_cost


def _estimate_claude_cost(response: Any) -> float:
    """Rough cost estimate from Claude response usage metadata."""
    try:
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        # Sonnet pricing ~$3/M input, $15/M output (2026-04)
        return (input_tokens * 3 + output_tokens * 15) / 1_000_000
    except Exception:
        return 0.0
