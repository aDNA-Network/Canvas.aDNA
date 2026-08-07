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
    DEFAULT_REFINE_NEGATIVE,
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
# Refine / img2img — Halftone H4 (the Vulcan seam)
# ---------------------------------------------------------------------------

class TestImg2ImgWorkflowConstruction:
    def test_latent_comes_from_the_seed_image_not_an_empty_latent(self):
        """The defining difference from txt2img: LoadImage → VAEEncode supplies the latent."""
        adapter = ComfyForgeTier1Adapter()
        wf = adapter._build_img2img_workflow(
            prompt="a cat", negative=None, seed_filename="seed.png", denoise=0.4, seed=7,
        )
        assert wf["10"]["class_type"] == "LoadImage"
        assert wf["10"]["inputs"]["image"] == "seed.png"
        assert wf["11"]["class_type"] == "VAEEncode"
        assert wf["11"]["inputs"]["pixels"] == ["10", 0]
        assert wf["3"]["inputs"]["latent_image"] == ["11", 0]
        assert not any(n.get("class_type") == "EmptyLatentImage" for n in wf.values())

    def test_denoise_and_seed_are_honored(self):
        adapter = ComfyForgeTier1Adapter()
        wf = adapter._build_img2img_workflow(
            prompt="p", negative=None, seed_filename="s.png", denoise=0.62, seed=12345,
        )
        assert wf["3"]["inputs"]["denoise"] == 0.62
        assert wf["3"]["inputs"]["seed"] == 12345

    def test_negative_travels_in_its_own_node_never_concatenated(self):
        """Roadmap R6: H1 split the negative channel precisely so chain backends honor it."""
        adapter = ComfyForgeTier1Adapter()
        wf = adapter._build_img2img_workflow(
            prompt="a hero", negative="extra limbs, blurry",
            seed_filename="s.png", denoise=0.4, seed=1,
        )
        assert wf["7"]["inputs"]["text"] == "extra limbs, blurry"
        assert "extra limbs" not in wf["6"]["inputs"]["text"]
        assert wf["3"]["inputs"]["negative"] == ["7", 0]

    def test_default_negative_when_none_supplied(self):
        adapter = ComfyForgeTier1Adapter()
        wf = adapter._build_img2img_workflow(
            prompt="p", negative=None, seed_filename="s.png", denoise=0.4, seed=1,
        )
        assert wf["7"]["inputs"]["text"] == DEFAULT_REFINE_NEGATIVE

    def test_lora_node_present_only_when_a_lora_is_passed(self):
        adapter = ComfyForgeTier1Adapter()
        without = adapter._build_img2img_workflow(
            prompt="p", negative=None, seed_filename="s.png", denoise=0.4, seed=1,
        )
        assert not any(n.get("class_type") == "LoraLoader" for n in without.values())
        assert without["3"]["inputs"]["model"] == ["4", 0]

        with_lora = adapter._build_img2img_workflow(
            prompt="p", negative=None, seed_filename="s.png", denoise=0.4, seed=1,
            lora={"name": "stanley_v1.safetensors", "strength_model": 0.8},
        )
        assert with_lora["14"]["class_type"] == "LoraLoader"
        assert with_lora["14"]["inputs"]["lora_name"] == "stanley_v1.safetensors"
        assert with_lora["14"]["inputs"]["strength_model"] == 0.8
        # model AND both clip encodes rewire through the LoRA
        assert with_lora["3"]["inputs"]["model"] == ["14", 0]
        assert with_lora["6"]["inputs"]["clip"] == ["14", 1]
        assert with_lora["7"]["inputs"]["clip"] == ["14", 1]

    def test_upscale_stage_is_optional_and_feeds_save(self):
        adapter = ComfyForgeTier1Adapter()
        plain = adapter._build_img2img_workflow(
            prompt="p", negative=None, seed_filename="s.png", denoise=0.4, seed=1,
        )
        assert plain["9"]["inputs"]["images"] == ["8", 0]

        upscaled = adapter._build_img2img_workflow(
            prompt="p", negative=None, seed_filename="s.png", denoise=0.4, seed=1, upscale=True,
        )
        assert upscaled["13"]["class_type"] == "ImageUpscaleWithModel"
        assert upscaled["13"]["inputs"]["image"] == ["8", 0]
        assert upscaled["9"]["inputs"]["images"] == ["13", 0]

    def test_refine_seed_is_deterministic_per_prompt_and_seed_image(self):
        """Refine is part of a reproducible bridge run — no wall-clock seeds."""
        a = ComfyForgeTier1Adapter._refine_seed("prompt", Path("/x/panel_v1.png"))
        b = ComfyForgeTier1Adapter._refine_seed("prompt", Path("/other/dir/panel_v1.png"))
        c = ComfyForgeTier1Adapter._refine_seed("prompt", Path("/x/panel_v2.png"))
        assert a == b  # location-independent
        assert a != c  # variant-sensitive


class TestNamedWorkflowTemplates:
    def _template(self) -> dict:
        return {
            "3": {"class_type": "KSampler", "inputs": {"denoise": 1.0, "seed": 0}},
            "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "PLACEHOLDER"}},
            "7": {"class_type": "CLIPTextEncode", "inputs": {"text": "PLACEHOLDER"}},
            "10": {"class_type": "LoadImage", "inputs": {"image": "PLACEHOLDER"}},
            "20": {"class_type": "LoraLoader", "inputs": {"lora_name": "authors_choice.safetensors"}},
        }

    def test_unresolvable_workflow_degrades_to_builtin(self, tmp_path):
        """comic_panel_refine may not exist upstream yet — that is a degradation, not a failure."""
        adapter = ComfyForgeTier1Adapter(config=ComfyForgeConfig(workflow_dir=str(tmp_path)))
        graph, source = adapter._resolve_refine_workflow("comic_panel_refine")
        assert graph is None and source == "builtin"

        no_dir = ComfyForgeTier1Adapter()
        assert no_dir._resolve_refine_workflow("comic_panel_refine") == (None, "builtin")
        assert no_dir._resolve_refine_workflow(None) == (None, "builtin")

    def test_resolved_template_is_patched_by_node_class(self, tmp_path):
        (tmp_path / "comic_panel_refine.json").write_text(json.dumps(self._template()))
        adapter = ComfyForgeTier1Adapter(config=ComfyForgeConfig(workflow_dir=str(tmp_path)))
        template, source = adapter._resolve_refine_workflow("comic_panel_refine")
        assert source == "template:comic_panel_refine"

        patched = adapter._patch_workflow_template(
            template, prompt="positive text", negative="negative text",
            seed_filename="seed.png", denoise=0.35, seed=99,
        )
        assert patched["6"]["inputs"]["text"] == "positive text"   # first CLIPTextEncode
        assert patched["7"]["inputs"]["text"] == "negative text"   # second
        assert patched["10"]["inputs"]["image"] == "seed.png"
        assert patched["3"]["inputs"]["denoise"] == 0.35
        assert patched["3"]["inputs"]["seed"] == 99
        # the workflow author's own nodes are left alone
        assert patched["20"]["inputs"]["lora_name"] == "authors_choice.safetensors"

    def test_patching_never_mutates_the_caller_template(self, tmp_path):
        template = self._template()
        adapter = ComfyForgeTier1Adapter()
        adapter._patch_workflow_template(
            template, prompt="p", negative="n", seed_filename="s.png", denoise=0.1, seed=1,
        )
        assert template["6"]["inputs"]["text"] == "PLACEHOLDER"
        assert template["3"]["inputs"]["denoise"] == 1.0

    def test_text_nodes_ordered_numerically_not_lexically(self, tmp_path):
        """Node ids are numeric strings: "10" must not sort before "6"."""
        template = {
            "10": {"class_type": "CLIPTextEncode", "inputs": {"text": "x"}},
            "6": {"class_type": "CLIPTextEncode", "inputs": {"text": "x"}},
        }
        adapter = ComfyForgeTier1Adapter()
        patched = adapter._patch_workflow_template(
            template, prompt="POS", negative="NEG", seed_filename="s.png", denoise=0.4, seed=1,
        )
        assert patched["6"]["inputs"]["text"] == "POS"
        assert patched["10"]["inputs"]["text"] == "NEG"


class TestLiveRunRegressions:
    """The two defects the 2026-08-07 live run against a real ComfyUI exposed.

    Both were invisible to mocks by construction: mocked polls return instantly, and a mock has
    no result cache. Recorded here so they cannot silently return.
    """

    def test_generation_budget_is_not_the_http_timeout(self):
        """A 30s HTTP timeout as the sampling deadline abandons every real generation."""
        cfg = ComfyForgeConfig()
        assert cfg.timeout_s == 30                      # per-request HTTP
        assert cfg.generation_timeout_s >= 300          # wall-clock sampling budget
        assert cfg.generation_timeout_s != cfg.timeout_s

    def test_poll_history_deadline_uses_the_generation_budget(self):
        adapter = ComfyForgeTier1Adapter(
            ComfyForgeConfig(generation_timeout_s=0, poll_interval_s=0.01)
        )
        with patch("urllib.request.urlopen", side_effect=OSError("nope")):
            with pytest.raises(TimeoutError, match="timed out after 0s"):
                adapter._poll_history("pid")

    def test_save_prefix_varies_per_output_so_comfyui_does_not_serve_a_cached_empty_run(self):
        """Identical graphs hit ComfyUI's cache and return success with NO outputs."""
        adapter = ComfyForgeTier1Adapter()
        a = adapter._build_img2img_workflow(
            prompt="p", negative=None, seed_filename="s.png", denoise=0.4, seed=1,
            filename_prefix="canvas_refine_panel_v1",
        )
        b = adapter._build_img2img_workflow(
            prompt="p", negative=None, seed_filename="s.png", denoise=0.4, seed=1,
            filename_prefix="canvas_refine_panel_v2",
        )
        assert a["9"]["inputs"]["filename_prefix"] != b["9"]["inputs"]["filename_prefix"]
        assert a != b, "same-seed refines to different destinations must not be identical graphs"

    def test_refine_derives_the_prefix_from_the_output_filename(self, tmp_path):
        seed = tmp_path / "p_v1.png"
        seed.write_bytes(b"png")
        adapter = ComfyForgeTier1Adapter()
        captured = {}

        def _submit(graph):
            captured["graph"] = graph
            return "pid"

        with patch.object(adapter, "health_check", return_value=True), \
             patch.object(adapter, "_upload_image", return_value="p_v1.png"), \
             patch.object(adapter, "_submit_workflow", side_effect=_submit), \
             patch.object(adapter, "_poll_history", return_value={"outputs": {}}):
            adapter.refine_image(str(seed), "p", str(tmp_path / "refined" / "p_v1.png"))

        assert captured["graph"]["9"]["inputs"]["filename_prefix"] == "canvas_refine_p_v1"

    def test_empty_outputs_error_names_the_cache_as_the_likely_cause(self, tmp_path):
        seed = tmp_path / "s.png"
        seed.write_bytes(b"png")
        adapter = ComfyForgeTier1Adapter()
        with patch.object(adapter, "health_check", return_value=True), \
             patch.object(adapter, "_upload_image", return_value="s.png"), \
             patch.object(adapter, "_submit_workflow", return_value="pid"), \
             patch.object(adapter, "_poll_history", return_value={"outputs": {}}):
            result = adapter.refine_image(str(seed), "p", str(tmp_path / "o.png"))
        assert "execution_cached" in result["error"]


class TestRefineImageFlow:
    def test_missing_seed_image_fails_before_any_http(self):
        adapter = ComfyForgeTier1Adapter()
        with patch("urllib.request.urlopen", side_effect=AssertionError("no HTTP expected")):
            result = adapter.refine_image("/nonexistent/seed.png", "p", "/tmp/out.png")
        assert result["success"] is False
        assert "seed_image not found" in result["error"]

    def test_unreachable_endpoint_short_circuits(self, tmp_path):
        seed = tmp_path / "seed.png"
        seed.write_bytes(b"\x89PNG fake")
        adapter = ComfyForgeTier1Adapter()
        with patch.object(adapter, "health_check", return_value=False):
            result = adapter.refine_image(str(seed), "p", str(tmp_path / "out.png"))
        assert result["success"] is False
        assert result["error"] == "comfyui_unreachable"
        assert result["endpoint"] == adapter.config.endpoint

    def test_upload_builds_multipart_and_returns_server_filename(self, tmp_path):
        seed = tmp_path / "seed.png"
        seed.write_bytes(b"\x89PNG fake image bytes")
        adapter = ComfyForgeTier1Adapter()
        captured = {}

        def mock_urlopen(req, timeout=None):
            captured["url"] = req.full_url
            captured["content_type"] = req.headers.get("Content-type")
            captured["body"] = req.data
            mock = MagicMock()
            mock.read.return_value = json.dumps(
                {"name": "seed.png", "subfolder": "", "type": "input"}
            ).encode()
            mock.__enter__ = MagicMock(return_value=mock)
            mock.__exit__ = MagicMock(return_value=False)
            return mock

        with patch("urllib.request.urlopen", side_effect=mock_urlopen):
            name = adapter._upload_image(seed)

        assert name == "seed.png"
        assert captured["url"].endswith("/upload/image")
        assert captured["content_type"].startswith("multipart/form-data; boundary=")
        assert b'name="image"; filename="seed.png"' in captured["body"]
        assert b"\x89PNG fake image bytes" in captured["body"]

    def test_upload_prefixes_subfolder_when_the_server_returns_one(self, tmp_path):
        seed = tmp_path / "seed.png"
        seed.write_bytes(b"png")
        adapter = ComfyForgeTier1Adapter()
        mock = MagicMock()
        mock.read.return_value = json.dumps({"name": "seed.png", "subfolder": "canvas"}).encode()
        mock.__enter__ = MagicMock(return_value=mock)
        mock.__exit__ = MagicMock(return_value=False)
        with patch("urllib.request.urlopen", return_value=mock):
            assert adapter._upload_image(seed) == "canvas/seed.png"

    def test_upload_without_a_filename_raises(self, tmp_path):
        seed = tmp_path / "seed.png"
        seed.write_bytes(b"png")
        adapter = ComfyForgeTier1Adapter()
        mock = MagicMock()
        mock.read.return_value = json.dumps({}).encode()
        mock.__enter__ = MagicMock(return_value=mock)
        mock.__exit__ = MagicMock(return_value=False)
        with patch("urllib.request.urlopen", return_value=mock), \
             pytest.raises(RuntimeError, match="No filename"):
            adapter._upload_image(seed)

    def test_successful_refine_end_to_end(self, tmp_path):
        """health → upload → submit → poll → download, with strict call accounting."""
        seed = tmp_path / "panel_v1.png"
        seed.write_bytes(b"\x89PNG seed")
        out = tmp_path / "refined" / "panel_v1.png"
        adapter = ComfyForgeTier1Adapter()

        responses = [
            ({}, 200),                                            # health check
            ({"name": "panel_v1.png", "subfolder": ""}, 200),     # upload
            ({"prompt_id": "refine-1"}, 200),                     # submit
            ({"refine-1": {"outputs": {"9": {"images": [
                {"filename": "canvas_refine_00001_.png", "subfolder": "", "type": "output"}
            ]}}}}, 200),                                          # poll
            (b"\x89PNG refined bytes", 200),                      # download
        ]
        submitted = {}
        call_count = [0]

        def mock_urlopen(req, timeout=None):
            if call_count[0] >= len(responses):
                raise AssertionError(f"unexpected urlopen call #{call_count[0] + 1}")
            idx = call_count[0]
            call_count[0] += 1
            if req.full_url.endswith("/prompt"):
                submitted["graph"] = json.loads(req.data)["prompt"]
            resp_data, status = responses[idx]
            mock = MagicMock()
            mock.status = status
            if isinstance(resp_data, bytes):
                mock.read.side_effect = [resp_data, b""]
            else:
                mock.read.return_value = json.dumps(resp_data).encode()
            mock.__enter__ = MagicMock(return_value=mock)
            mock.__exit__ = MagicMock(return_value=False)
            return mock

        with patch("urllib.request.urlopen", side_effect=mock_urlopen):
            result = adapter.refine_image(
                str(seed), "a hero mid-stride", str(out),
                negative="blurry", denoise=0.45,
            )

        assert result["success"] is True
        assert result["stage"] == "refine"
        assert result["denoise"] == 0.45
        assert result["workflow_source"] == "builtin"
        assert Path(result["image_path"]).read_bytes() == b"\x89PNG refined bytes"
        # the uploaded name reached the graph's LoadImage node
        assert submitted["graph"]["10"]["inputs"]["image"] == "panel_v1.png"
        assert submitted["graph"]["3"]["inputs"]["denoise"] == 0.45
        assert submitted["graph"]["7"]["inputs"]["text"] == "blurry"

    def test_submission_failure_is_reported_not_raised(self, tmp_path):
        seed = tmp_path / "seed.png"
        seed.write_bytes(b"png")
        adapter = ComfyForgeTier1Adapter()
        with patch.object(adapter, "health_check", return_value=True), \
             patch.object(adapter, "_upload_image", return_value="seed.png"), \
             patch.object(adapter, "_submit_workflow", side_effect=RuntimeError("server error")):
            result = adapter.refine_image(str(seed), "p", str(tmp_path / "out.png"))
        assert result["success"] is False
        assert "server error" in result["error"]
        assert result["stage"] == "refine"

    def test_empty_history_outputs_is_reported(self, tmp_path):
        seed = tmp_path / "seed.png"
        seed.write_bytes(b"png")
        adapter = ComfyForgeTier1Adapter()
        with patch.object(adapter, "health_check", return_value=True), \
             patch.object(adapter, "_upload_image", return_value="seed.png"), \
             patch.object(adapter, "_submit_workflow", return_value="pid"), \
             patch.object(adapter, "_poll_history", return_value={"outputs": {}}):
            result = adapter.refine_image(str(seed), "p", str(tmp_path / "out.png"))
        assert result["success"] is False
        assert "No images" in result["error"]


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
