"""The ``comfy`` refine seam (Halftone H4) — binding behavior + the fake→comfy chain proof.

Everything here runs offline: the ComfyUI HTTP surface is mocked from the recorded-shape fixtures
in ``fixtures/comfy/`` (which are the contract with Vulcan). One live smoke is marked ``network``
and skips unless a reachable node is configured.
"""

from __future__ import annotations

import ast
import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from comic_render.backends import make_refine_client
from comic_render.backends.comfy import (
    DEFAULT_ENDPOINT,
    ENDPOINT_ENV,
    WORKFLOW_DIR_ENV,
    ComfyRefineClient,
    apply_trigger_word,
    lora_name_for,
    resolve_endpoint,
)
from comic_render.backends.fake import FakeImageClient
from comic_render.dispatch import run_generate, run_refine
from comic_render.extract import parse_chain, plan
from comic_render.manifest import RenderManifest

FIXTURES = Path(__file__).parent / "fixtures" / "comfy"


def _fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


def _uploaded_filename(body: bytes) -> str | None:
    """Parse the multipart body's ``filename="…"`` so the mock echoes what was actually sent."""
    marker = b'name="image"; filename="'
    start = body.find(marker)
    if start == -1:
        return None
    start += len(marker)
    return body[start:body.find(b'"', start)].decode()


def _mock_comfy_http(submitted: dict | None = None, *, refined_bytes: bytes = b"\x89PNG refined"):
    """A urlopen side_effect that speaks the recorded ComfyUI contract, routed by URL."""
    upload = _fixture("upload_image.json")
    prompt_resp = _fixture("prompt.json")
    history = _fixture("history.json")
    prompt_id = prompt_resp["prompt_id"]

    def _urlopen(req, timeout=None):
        url = req.full_url
        mock = MagicMock()
        mock.status = 200
        if url.endswith("/system_stats"):
            payload = _fixture("system_stats.json")
        elif url.endswith("/upload/image"):
            # A real server echoes the name it stored; echoing keeps the mock honest about
            # which file the seed upload actually carried.
            payload = {**upload, "name": _uploaded_filename(req.data) or upload["name"]}
        elif url.endswith("/prompt"):
            if submitted is not None:
                submitted["graph"] = json.loads(req.data)["prompt"]
            payload = prompt_resp
        elif f"/history/{prompt_id}" in url:
            payload = history
        elif "/view?" in url:
            mock.read.side_effect = [refined_bytes, b""]
            mock.__enter__ = MagicMock(return_value=mock)
            mock.__exit__ = MagicMock(return_value=False)
            return mock
        else:  # pragma: no cover — an unrouted URL is a test bug worth failing loudly
            raise AssertionError(f"unexpected ComfyUI call: {url}")
        mock.read.return_value = json.dumps(payload).encode()
        mock.__enter__ = MagicMock(return_value=mock)
        mock.__exit__ = MagicMock(return_value=False)
        return mock

    return _urlopen


# ---------------------------------------------------------------------------
# Endpoint + registry policy
# ---------------------------------------------------------------------------


def test_endpoint_defaults_to_the_wrapper_declared_l1_local(monkeypatch):
    """The federation wrapper declares l1_local — not canvas_core's Anduril-mesh default."""
    monkeypatch.delenv(ENDPOINT_ENV, raising=False)
    assert resolve_endpoint() == DEFAULT_ENDPOINT == "http://localhost:8188"
    assert ComfyRefineClient().endpoint == "http://localhost:8188"


def test_endpoint_env_var_overrides(monkeypatch):
    monkeypatch.setenv(ENDPOINT_ENV, "http://10.42.0.8:8188")
    assert ComfyRefineClient().endpoint == "http://10.42.0.8:8188"


def test_registry_returns_a_protocol_conformant_client():
    client = make_refine_client("comfy")
    assert isinstance(client, ComfyRefineClient)
    assert callable(client.refine_image)
    assert client.model_name == "comfyui-img2img"
    # local inference is free — the budget cap stays a guard on the CLOUD generate stage
    assert client.cost_per_image == 0.0


def test_binding_reaches_comfyui_only_through_canvas_core():
    """The boundary rule, asserted rather than left to the AST guard's forbidden-list."""
    tree = ast.parse((Path(__file__).parents[1] / "src" / "comic_render" / "backends" /
                      "comfy.py").read_text())
    modules = [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module]
    assert "canvas_core.comfyforge_adapter" in modules
    assert not any(m.split(".")[0] in {"comfy", "comfyui", "torch", "diffusers"} for m in modules)


# ---------------------------------------------------------------------------
# Chain syntax
# ---------------------------------------------------------------------------


def test_chain_syntax_carries_a_named_workflow():
    stages = parse_chain("generate:gemini,refine:comfy@0.35/comic_panel_refine")
    assert [s.stage for s in stages] == ["generate", "refine"]
    assert stages[1].backend == "comfy"
    assert stages[1].denoise == 0.35
    assert stages[1].workflow == "comic_panel_refine"


def test_chain_syntax_is_backward_compatible():
    stages = parse_chain("generate:fake,refine:fake@0.4")
    assert stages[1].workflow is None
    assert stages[1].denoise == 0.4
    assert parse_chain("generate:fake")[0].workflow is None


def test_chain_syntax_rejects_malformed_specs():
    for bad in ("generate", "generate:", ":fake", ""):
        with pytest.raises(ValueError):
            parse_chain(bad)


# ---------------------------------------------------------------------------
# LoRA conditioning helpers
# ---------------------------------------------------------------------------


def test_lora_ref_maps_to_a_bare_comfyui_filename():
    assert lora_name_for("ScienceStanley.aDNA/what/loras/stanley_v1.safetensors") == \
        "stanley_v1.safetensors"


def test_trigger_word_injected_only_when_absent():
    assert apply_trigger_word("a hero", "sci_stanley") == "sci_stanley, a hero"
    assert apply_trigger_word("sci_stanley at a desk", "sci_stanley") == "sci_stanley at a desk"
    assert apply_trigger_word("SCI_STANLEY at a desk", "sci_stanley") == "SCI_STANLEY at a desk"
    assert apply_trigger_word("a hero", None) == "a hero"


# ---------------------------------------------------------------------------
# refine_image through the mocked HTTP contract
# ---------------------------------------------------------------------------


def test_refine_sends_prompt_negative_denoise_and_seed_image(tmp_path):
    seed = tmp_path / "spread0_page0_p0_v1.png"
    seed.write_bytes(b"\x89PNG seed")
    out = tmp_path / "refined" / "spread0_page0_p0_v1.png"
    submitted: dict = {}

    client = ComfyRefineClient()
    with patch("urllib.request.urlopen", side_effect=_mock_comfy_http(submitted)):
        result = client.refine_image(
            str(seed), "a hero mid-stride", str(out),
            negative="photorealism, legible text", denoise=0.35,
        )

    assert result["success"] is True
    assert Path(result["image_path"]).read_bytes() == b"\x89PNG refined"
    graph = submitted["graph"]
    assert graph["6"]["inputs"]["text"] == "a hero mid-stride"
    assert graph["7"]["inputs"]["text"] == "photorealism, legible text"
    assert graph["3"]["inputs"]["denoise"] == 0.35
    assert graph["10"]["inputs"]["image"] == "spread0_page0_p0_v1.png"
    assert client.calls[0]["success"] is True


def test_refine_conditions_on_a_pair_gated_lora(tmp_path):
    seed = tmp_path / "p_v1.png"
    seed.write_bytes(b"\x89PNG seed")
    submitted: dict = {}

    client = ComfyRefineClient()
    with patch("urllib.request.urlopen", side_effect=_mock_comfy_http(submitted)):
        client.refine_image(
            str(seed), "at a whiteboard", str(tmp_path / "out.png"),
            lora={"name": "Science Stanley", "trigger_word": "sci_stanley",
                  "lora_ref": "ScienceStanley.aDNA/what/loras/stanley_v1.safetensors"},
        )

    graph = submitted["graph"]
    assert graph["14"]["class_type"] == "LoraLoader"
    assert graph["14"]["inputs"]["lora_name"] == "stanley_v1.safetensors"
    assert graph["3"]["inputs"]["model"] == ["14", 0]
    # the trigger token reaches the positive prompt — a LoRA without it is inert
    assert graph["6"]["inputs"]["text"].startswith("sci_stanley, ")


def test_lora_less_entry_adds_no_lora_node(tmp_path):
    """Reference-images-only is a first-class path (H5 exit criterion; Bearly's required path)."""
    seed = tmp_path / "p_v1.png"
    seed.write_bytes(b"\x89PNG seed")
    submitted: dict = {}

    client = ComfyRefineClient()
    with patch("urllib.request.urlopen", side_effect=_mock_comfy_http(submitted)):
        client.refine_image(
            str(seed), "at a whiteboard", str(tmp_path / "out.png"),
            lora={"name": "Bearly", "reference_images": ["Bearly.aDNA/what/visual_dna/a.png"]},
        )

    graph = submitted["graph"]
    assert not any(n.get("class_type") == "LoraLoader" for n in graph.values())
    assert graph["6"]["inputs"]["text"] == "at a whiteboard"


def test_named_workflow_template_is_used_when_it_resolves(tmp_path):
    seed = tmp_path / "p_v1.png"
    seed.write_bytes(b"\x89PNG seed")
    submitted: dict = {}

    client = ComfyRefineClient(workflow_dir=str(FIXTURES))
    with patch("urllib.request.urlopen", side_effect=_mock_comfy_http(submitted)):
        result = client.refine_image(
            str(seed), "positive", str(tmp_path / "out.png"),
            negative="negative", denoise=0.5, workflow="comic_panel_refine",
        )

    assert result["workflow_source"] == "template:comic_panel_refine"
    graph = submitted["graph"]
    assert graph["9"]["inputs"]["filename_prefix"] == "comic_panel_refine"  # template's own node
    assert graph["6"]["inputs"]["text"] == "positive"
    assert graph["7"]["inputs"]["text"] == "negative"
    assert graph["3"]["inputs"]["denoise"] == 0.5
    assert graph["10"]["inputs"]["image"] == "p_v1.png"


def test_missing_named_workflow_degrades_to_the_builtin_graph(tmp_path):
    """comic_panel_refine does not exist upstream yet — that must not break the chain."""
    seed = tmp_path / "p_v1.png"
    seed.write_bytes(b"\x89PNG seed")
    client = ComfyRefineClient(workflow_dir=str(tmp_path))
    with patch("urllib.request.urlopen", side_effect=_mock_comfy_http()):
        result = client.refine_image(
            str(seed), "p", str(tmp_path / "out.png"), workflow="comic_panel_refine",
        )
    assert result["success"] is True
    assert result["workflow_source"] == "builtin"


def test_unreachable_node_is_reported_not_raised(tmp_path):
    seed = tmp_path / "p_v1.png"
    seed.write_bytes(b"\x89PNG seed")
    client = ComfyRefineClient()
    with patch("urllib.request.urlopen", side_effect=OSError("connection refused")):
        result = client.refine_image(str(seed), "p", str(tmp_path / "out.png"))
    assert result["success"] is False
    assert result["error"] == "comfyui_unreachable"


# ---------------------------------------------------------------------------
# The chain proof — fake generate → comfy refine, through run_refine
# ---------------------------------------------------------------------------


def _plan_hybrid(canvas_path: Path) -> tuple[RenderManifest, Path]:
    return plan(canvas_path, chain="generate:fake,refine:comfy@0.4/comic_panel_refine",
                variant_count=1, force=True)


def test_fake_generate_then_comfy_refine_chain(canvas_path):
    """The H4 exit criterion: the chain flows generate output → comfy refine → results.refined."""
    manifest, mpath = _plan_hybrid(canvas_path)
    run_generate(manifest, mpath, client_overrides={"fake": FakeImageClient()})

    client = ComfyRefineClient(workflow_dir=str(FIXTURES))
    submitted: dict = {}
    with patch("urllib.request.urlopen", side_effect=_mock_comfy_http(submitted)):
        summary = run_refine(manifest, mpath, client_overrides={"comfy": client})

    assert summary["refined"], "no panel refined"
    assert not summary["no_refine_stage"]
    panel = manifest.panel(summary["refined"][0])
    assert panel.results["refined"]
    assert panel.results["model"] == "comfyui-img2img"
    assert panel.final_outputs() == panel.results["refined"]
    for rel in panel.results["refined"]:
        assert (mpath.parent / rel).exists()
    # the named workflow travelled from the chain spec all the way to the submitted graph
    assert client.calls[0]["workflow"] == "comic_panel_refine"
    assert submitted["graph"]["9"]["inputs"]["filename_prefix"] == "comic_panel_refine"


def test_chain_refine_is_idempotent(canvas_path):
    manifest, mpath = _plan_hybrid(canvas_path)
    run_generate(manifest, mpath, client_overrides={"fake": FakeImageClient()})

    first = ComfyRefineClient(workflow_dir=str(FIXTURES))
    with patch("urllib.request.urlopen", side_effect=_mock_comfy_http()):
        run_refine(manifest, mpath, client_overrides={"comfy": first})
    calls_first = len(first.calls)
    assert calls_first > 0

    reloaded = RenderManifest.load(mpath)
    second = ComfyRefineClient(workflow_dir=str(FIXTURES))
    with patch("urllib.request.urlopen",
               side_effect=AssertionError("re-run must not touch the network")):
        summary = run_refine(reloaded, mpath, client_overrides={"comfy": second})
    assert second.calls == []
    assert summary["skipped"]


def test_chain_threads_the_panels_pair_gated_lora(canvas_path):
    """dispatch lifts characters[] → the refine client; H5 emits the pair, H4 conditions on it."""
    manifest, mpath = _plan_hybrid(canvas_path)
    target = manifest.dispatchable()[0]
    target.characters = [
        {"name": "Extra", "reference_images": ["X.aDNA/a.png"]},          # LoRA-less, skipped
        {"name": "Science Stanley", "trigger_word": "sci_stanley",
         "lora_ref": "ScienceStanley.aDNA/what/loras/stanley_v1.safetensors"},
    ]
    manifest.save(mpath)
    run_generate(manifest, mpath, client_overrides={"fake": FakeImageClient()})

    client = ComfyRefineClient()
    with patch("urllib.request.urlopen", side_effect=_mock_comfy_http()):
        run_refine(manifest, mpath, client_overrides={"comfy": client})

    conditioned = [c for c in client.calls if c["lora"]]
    assert conditioned, "the pair-gated LoRA never reached the client"
    assert conditioned[0]["lora"]["name"] == "stanley_v1.safetensors"


# ---------------------------------------------------------------------------
# Live path (flag-gated; skipped by default)
# ---------------------------------------------------------------------------


@pytest.mark.network
def test_live_refine_against_a_reachable_node(tmp_path):
    """Run the day a ComfyUI node is up: COMIC_RENDER_COMFY_ENDPOINT=... pytest -m network."""
    if not os.environ.get(ENDPOINT_ENV):
        pytest.skip(f"set {ENDPOINT_ENV} to run the live refine smoke")
    client = ComfyRefineClient(workflow_dir=os.environ.get(WORKFLOW_DIR_ENV))
    if not client.health_check():
        pytest.skip(f"no ComfyUI at {client.endpoint}")

    from comic_render.png_meta import write_solid_png

    seed = write_solid_png(tmp_path / "seed_v1.png", 1024, 1024, (120, 90, 200))
    result = client.refine_image(
        str(seed), "a comic panel, cel shaded", str(tmp_path / "refined.png"),
        negative="photorealism", denoise=0.4,
    )
    assert result["success"] is True, result.get("error")
    assert Path(result["image_path"]).stat().st_size > 0
