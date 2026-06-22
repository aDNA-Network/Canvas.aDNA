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
    """Gemini 2.5 Flash vision adapter (default).

    Requires ``google-generativeai`` SDK.  Guarded — raises
    RuntimeError if the SDK is not installed.
    """

    model_id: str = "gemini-2.5-flash"

    def __init__(self, model: str = "gemini-2.5-flash", api_key: str | None = None):
        self.model_id = model
        self._api_key = api_key

    def analyze(self, request: VisionRequest) -> VisionResponse:
        """Call Gemini vision API with screenshot images."""
        t0 = time.monotonic()
        try:
            import google.generativeai as genai  # type: ignore[import-untyped]
        except ImportError:
            return VisionResponse(
                success=False,
                error="google-generativeai SDK not installed",
                model_id=self.model_id,
            )

        try:
            if self._api_key:
                genai.configure(api_key=self._api_key)

            model = genai.GenerativeModel(self.model_id)

            # Build multimodal content: images + prompt.
            from PIL import Image  # type: ignore[import-untyped]

            parts: list[Any] = []
            for img_path in request.images:
                parts.append(Image.open(img_path))
            parts.append(request.prompt)

            response = model.generate_content(parts)
            raw = response.text

            # Parse structured findings from JSON in response.
            findings = _parse_findings_json(raw)
            duration = time.monotonic() - t0

            return VisionResponse(
                raw_text=raw,
                parsed_findings=findings,
                cost_usd=_estimate_gemini_cost(request, raw),
                duration_s=duration,
                model_id=self.model_id,
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

# Known adapter map for convenience.
VISION_ADAPTERS: dict[str, type] = {
    "gemini-2.5-flash": GeminiVisionAdapter,
    "claude-sonnet-vision": ClaudeVisionAdapter,
    "claude-opus-vision": ClaudeVisionAdapter,
}


def get_vision_client(model: str = "gemini-2.5-flash", **kwargs: Any) -> VisionClient:
    """Construct a vision client by model name."""
    adapter_cls = VISION_ADAPTERS.get(model)
    if adapter_cls is None:
        raise ValueError(f"Unknown vision model: {model!r}. Known: {list(VISION_ADAPTERS)}")
    return adapter_cls(model=model, **kwargs)  # type: ignore[call-arg]


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
