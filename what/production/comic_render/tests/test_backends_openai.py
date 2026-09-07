"""The ``openai`` backend — a THIN BINDING to the shared OpenAI layer, tested at the seam.

Mirror of ``test_backends_gemini.py``: the layer itself (registry lifecycle, lane order,
secret hygiene, transport) is tested in ``Home.aDNA/what/code/openaiapi/tests/``. What is
Canvas's and therefore tested HERE: ``ImageClient`` conformance, the ``SUPPORTED_ASPECTS``
class attribute read without construction, tier aliasing, registry membership, and
graceful behaviour when the shared layer is absent.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from comic_render.backends import GENERATE_BACKENDS, make_generate_client, supported_aspects_for
from comic_render.backends import openai as backend
from comic_render.backends.openai import (
    TIER_ALIASES,
    OpenAICredentialError,
    OpenAIImageClient,
)

HAS_SHARED_LAYER = backend._oa is not None
needs_layer = pytest.mark.skipif(not HAS_SHARED_LAYER, reason="Home.aDNA/openaiapi not on this node")


class FakeSharedClient:
    """Stands in for ``openaiapi.OpenAIImagesClient`` — the seam this backend binds to."""

    def __init__(self, result=None):
        self.lane = "C07 OPENAI_API_KEY"
        self.result = result or {"success": True, "image_path": "x.png", "model": "gpt-image-2",
                                 "image_size": "1K", "cost_usd": 0.03}
        self.calls = []

    def resolve(self, name):
        return SimpleNamespace(id="gpt-image-2")

    def cost_of(self, name, image_size="1K"):
        return 0.03

    def generate_image(self, text, output_path, **kw):
        self.calls.append({"text": text, "output_path": output_path, **kw})
        return self.result


class TestRegistry:
    def test_registered_as_a_generate_backend(self):
        assert GENERATE_BACKENDS["openai"] is OpenAIImageClient

    def test_supported_aspects_readable_without_a_client(self):
        # plan runs before any credential is needed — this must not construct anything
        menu = supported_aspects_for("openai")
        assert "1:1" in menu and "3:2" in menu and "2:3" in menu

    def test_openai_menu_is_narrower_than_the_package_default(self):
        # the OpenAI size grid has no 16:9 — plan must not approve what the API refuses
        assert "16:9" not in supported_aspects_for("openai")


class TestBinding:
    def test_forwards_to_the_shared_layer_and_returns_its_contract(self):
        shared = FakeSharedClient()
        c = OpenAIImageClient(client=shared)
        r = c.generate_image("a lighthouse", "out.png", aspect_ratio="2:3")
        assert r["success"] is True
        assert shared.calls[0]["output_path"] == "out.png"
        assert shared.calls[0]["aspect_ratio"] == "2:3"

    def test_unwraps_an_ImagePrompt(self):
        from canvas_core.image_generation import ImagePrompt

        shared = FakeSharedClient()
        OpenAIImageClient(client=shared).generate_image(ImagePrompt(text="hello"), "out.png")
        assert shared.calls[0]["text"] == "hello"

    def test_cost_per_image_is_real_so_the_budget_cap_bites(self):
        assert OpenAIImageClient(client=FakeSharedClient()).cost_per_image == 0.03

    def test_exposes_the_lane_so_a_spend_report_can_name_it(self):
        assert "C07" in OpenAIImageClient(client=FakeSharedClient()).lane

    def test_a_failure_is_returned_not_raised(self):
        shared = FakeSharedClient(result={"success": False, "error": "refused"})
        r = OpenAIImageClient(client=shared).generate_image("x", "out.png")
        assert r["success"] is False and r["error"] == "refused"

    def test_tier_aliases_map_into_shared_vocabulary(self):
        shared = FakeSharedClient()
        OpenAIImageClient(client=shared).generate_image("x", "out.png", model="ultra")
        assert shared.calls[0]["model"] == "image.pro"
        assert TIER_ALIASES["mini"] == "image.economy"


@needs_layer
class TestWithRealLayerOffline:
    def test_constructing_without_credentials_is_a_named_error(self, monkeypatch):
        for v in backend._oa.credentials.ENV_CHAIN:
            monkeypatch.delenv(v, raising=False)
        with pytest.raises(OpenAICredentialError, match="C07"):
            make_generate_client("openai")

    def test_aspect_menu_comes_from_the_shared_registry(self):
        assert tuple(OpenAIImageClient.SUPPORTED_ASPECTS) == tuple(
            backend._oa.models.OPENAI_IMAGE_ASPECTS)
