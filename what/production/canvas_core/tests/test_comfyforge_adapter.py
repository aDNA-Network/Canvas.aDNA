"""Tests for ComfyForge Tier 1 adapter and style mapping loader.

Uses mock HTTP responses — no actual ComfyUI endpoint required.
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure canvas_core is importable
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from canvas_core.comfyforge_adapter import (
    ASPECT_RATIO_MAP,
    ComfyForgeConfig,
    ComfyForgeTier1Adapter,
)
from canvas_core.style_mapping import load_style_config, resolve_style


# ---------------------------------------------------------------------------
# ComfyForgeConfig
# ---------------------------------------------------------------------------

class TestComfyForgeConfig:
    def test_defaults(self):
        cfg = ComfyForgeConfig()
        assert cfg.endpoint == "http://10.42.0.8:8188"
        assert cfg.timeout_s == 30
        assert cfg.failover_ms == 2000
        assert cfg.poll_interval_s == 2.0
        assert cfg.style_config_path is None

    def test_custom_config(self):
        cfg = ComfyForgeConfig(
            endpoint="http://localhost:8188",
            timeout_s=10,
            failover_ms=1000,
        )
        assert cfg.endpoint == "http://localhost:8188"
        assert cfg.timeout_s == 10


# ---------------------------------------------------------------------------
# Aspect ratio mapping
# ---------------------------------------------------------------------------

class TestAspectRatioMap:
    def test_standard_ratios(self):
        assert ASPECT_RATIO_MAP["1:1"] == (1024, 1024)
        assert ASPECT_RATIO_MAP["16:9"] == (1344, 768)
        assert ASPECT_RATIO_MAP["9:16"] == (768, 1344)
        assert ASPECT_RATIO_MAP["4:3"] == (1152, 896)
        assert ASPECT_RATIO_MAP["3:4"] == (896, 1152)

    def test_all_ratios_are_multiples_of_64(self):
        """ComfyUI requires dimensions divisible by 64 for SDXL."""
        for ratio, (w, h) in ASPECT_RATIO_MAP.items():
            assert w % 64 == 0, f"{ratio} width {w} not divisible by 64"
            assert h % 64 == 0, f"{ratio} height {h} not divisible by 64"


# ---------------------------------------------------------------------------
# Adapter instantiation
# ---------------------------------------------------------------------------

class TestAdapterInstantiation:
    def test_default_config(self):
        adapter = ComfyForgeTier1Adapter()
        assert adapter.config.endpoint == "http://10.42.0.8:8188"

    def test_custom_config(self):
        cfg = ComfyForgeConfig(endpoint="http://localhost:8188")
        adapter = ComfyForgeTier1Adapter(config=cfg)
        assert adapter.config.endpoint == "http://localhost:8188"

    def test_protocol_conformance(self):
        """Adapter has generate_image method matching ImageClient Protocol."""
        adapter = ComfyForgeTier1Adapter()
        assert hasattr(adapter, "generate_image")
        assert callable(adapter.generate_image)


# ---------------------------------------------------------------------------
# Health check / circuit breaker
# ---------------------------------------------------------------------------

class TestHealthCheck:
    def test_healthy_endpoint(self):
        adapter = ComfyForgeTier1Adapter()
        mock_resp = MagicMock()
        mock_resp.status = 200
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)

        with patch("urllib.request.urlopen", return_value=mock_resp):
            assert adapter.health_check() is True

    def test_unreachable_endpoint(self):
        adapter = ComfyForgeTier1Adapter()
        with patch("urllib.request.urlopen", side_effect=OSError("Connection refused")):
            assert adapter.health_check() is False

    def test_timeout_endpoint(self):
        adapter = ComfyForgeTier1Adapter()
        with patch("urllib.request.urlopen", side_effect=TimeoutError):
            assert adapter.health_check() is False

    def test_generate_image_returns_error_when_unhealthy(self):
        adapter = ComfyForgeTier1Adapter()
        with patch.object(adapter, "health_check", return_value=False):
            result = adapter.generate_image("test prompt")
            assert result["success"] is False
            assert result["error"] == "anduril_unreachable"
            assert result["adapter"] == "comfyforge_tier1"


# ---------------------------------------------------------------------------
# Workflow construction
# ---------------------------------------------------------------------------

class TestWorkflowConstruction:
    def test_basic_workflow(self):
        adapter = ComfyForgeTier1Adapter()
        workflow = adapter._build_workflow("a cat", "1:1", "photo", "ultra")

        # Check node types
        assert workflow["4"]["class_type"] == "CheckpointLoaderSimple"
        assert workflow["3"]["class_type"] == "KSampler"
        assert workflow["5"]["class_type"] == "EmptyLatentImage"
        assert workflow["6"]["class_type"] == "CLIPTextEncode"
        assert workflow["9"]["class_type"] == "SaveImage"

    def test_aspect_ratio_applied(self):
        adapter = ComfyForgeTier1Adapter()
        workflow = adapter._build_workflow("test", "16:9", "photo", "ultra")
        latent = workflow["5"]["inputs"]
        assert latent["width"] == 1344
        assert latent["height"] == 768

    def test_square_aspect(self):
        adapter = ComfyForgeTier1Adapter()
        workflow = adapter._build_workflow("test", "1:1", "photo", "ultra")
        latent = workflow["5"]["inputs"]
        assert latent["width"] == 1024
        assert latent["height"] == 1024

    def test_unknown_aspect_uses_default(self):
        adapter = ComfyForgeTier1Adapter()
        workflow = adapter._build_workflow("test", "7:3", "photo", "ultra")
        latent = workflow["5"]["inputs"]
        assert latent["width"] == 1024
        assert latent["height"] == 1024

    def test_prompt_in_positive_encode(self):
        adapter = ComfyForgeTier1Adapter()
        workflow = adapter._build_workflow("a beautiful sunset", "1:1", "photo", "ultra")
        positive_text = workflow["6"]["inputs"]["text"]
        assert "a beautiful sunset" in positive_text

    def test_custom_checkpoint(self):
        cfg = ComfyForgeConfig(checkpoint="custom_model.safetensors")
        adapter = ComfyForgeTier1Adapter(config=cfg)
        workflow = adapter._build_workflow("test", "1:1", "photo", "ultra")
        assert workflow["4"]["inputs"]["ckpt_name"] == "custom_model.safetensors"


# ---------------------------------------------------------------------------
# Full generate_image flow (mocked HTTP)
# ---------------------------------------------------------------------------

class TestGenerateImageFlow:
    def _mock_urlopen(self, responses):
        """Create a side_effect function that returns different responses per call."""
        call_count = [0]

        def _urlopen(req, timeout=None):
            idx = min(call_count[0], len(responses) - 1)
            call_count[0] += 1
            resp_data, status = responses[idx]
            mock = MagicMock()
            mock.status = status
            mock.read.return_value = json.dumps(resp_data).encode() if isinstance(resp_data, dict) else resp_data
            mock.__enter__ = MagicMock(return_value=mock)
            mock.__exit__ = MagicMock(return_value=False)
            return mock

        return _urlopen

    def test_successful_generation(self):
        adapter = ComfyForgeTier1Adapter()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test.png")

            responses = [
                # health check
                ({}, 200),
                # submit workflow
                ({"prompt_id": "abc-123"}, 200),
                # poll history
                ({"abc-123": {"outputs": {"9": {"images": [
                    {"filename": "canvasforge_00001_.png", "subfolder": "", "type": "output"}
                ]}}}}, 200),
                # download image (binary data)
                (b"\x89PNG fake image data", 200),
            ]

            # Mock urlopen with strict call accounting + EOF semantics for binary responses.
            # M-R5-01a Phase 5 (F-10 root-cause repair): the previous version had two bugs.
            # (1) `min(call_count, len-1)` silently clamped extra calls to the last response,
            #     hiding adapter-side re-polling regressions and causing infinite loops when the
            #     last response was binary (shutil.copyfileobj called .read() forever because
            #     the mock returned the same bytes on every call instead of b"" at EOF).
            # (2) For binary responses, mock.read.return_value returned the same bytes on every
            #     call, never signalling EOF — shutil.copyfileobj's `while buf := fsrc_read()`
            #     loop never terminated.
            # Fix: drop the clamp (raise on unexpected extra calls), and use side_effect to
            # return the bytes once then b"" so file-like read semantics terminate copyfileobj.
            call_count = [0]

            def mock_urlopen(req, timeout=None):
                if call_count[0] >= len(responses):
                    raise AssertionError(
                        f"Unexpected urlopen call #{call_count[0] + 1}; only "
                        f"{len(responses)} responses queued. Adapter may be re-polling "
                        f"without terminal-state detection."
                    )
                idx = call_count[0]
                call_count[0] += 1
                resp_data, status = responses[idx]
                mock = MagicMock()
                mock.status = status
                if isinstance(resp_data, bytes):
                    # File-like EOF: first .read() returns the bytes, subsequent return b"".
                    # shutil.copyfileobj uses chunked reads and stops on empty bytes.
                    mock.read.side_effect = [resp_data, b""]
                    mock.__iter__ = MagicMock(return_value=iter([resp_data]))
                else:
                    mock.read.return_value = json.dumps(resp_data).encode()
                mock.__enter__ = MagicMock(return_value=mock)
                mock.__exit__ = MagicMock(return_value=False)
                return mock

            with patch("urllib.request.urlopen", side_effect=mock_urlopen):
                result = adapter.generate_image("a cat", output_path=output_path)

            assert result["success"] is True
            assert result["adapter"] == "comfyforge_tier1"
            assert result["prompt_id"] == "abc-123"

    def test_submission_failure(self):
        adapter = ComfyForgeTier1Adapter()
        with patch.object(adapter, "health_check", return_value=True):
            with patch.object(adapter, "_submit_workflow", side_effect=RuntimeError("server error")):
                result = adapter.generate_image("test")
                assert result["success"] is False
                assert "server error" in result["error"]


# ---------------------------------------------------------------------------
# Style mapping loader
# ---------------------------------------------------------------------------

class TestStyleMapping:
    def test_load_missing_file(self):
        config = load_style_config("/nonexistent/path.yaml")
        assert config == {}

    def test_load_valid_yaml(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("mutation_operators:\n  ghibli:\n    positive_suffix: 'studio ghibli style'\n")
            f.flush()
            config = load_style_config(f.name)
        os.unlink(f.name)

        assert "mutation_operators" in config
        assert "ghibli" in config["mutation_operators"]

    def test_load_non_dict_yaml(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("- item1\n- item2\n")
            f.flush()
            config = load_style_config(f.name)
        os.unlink(f.name)
        assert config == {}

    def test_resolve_known_register(self):
        config = {
            "mutation_operators": {
                "ghibli": {"positive_suffix": "studio ghibli anime style"},
                "pixel": {"positive_suffix": "pixel art retro style"},
            }
        }
        result = resolve_style(config, register="ghibli", style_hints="")
        assert result["positive_suffix"] == "studio ghibli anime style"

    def test_resolve_unknown_register(self):
        config = {"mutation_operators": {"ghibli": {"positive_suffix": "ghibli"}}}
        result = resolve_style(config, register="unknown", style_hints="")
        assert result == {}

    def test_resolve_empty_config(self):
        result = resolve_style({}, register="ghibli", style_hints="")
        assert result == {}

    def test_resolve_with_style_hints_fallback(self):
        config = {
            "mutation_operators": {
                "ghibli_warm": {"positive_suffix": "warm ghibli tones"},
            }
        }
        result = resolve_style(config, register="", style_hints="ghibli")
        assert result.get("positive_suffix") == "warm ghibli tones"
