"""The ``gemini`` backend — now a THIN BINDING to the shared Google layer.

This file used to test a model map, a price table, credential resolution and SDK response parsing.
All of that moved to ``Home.aDNA/what/code/googleai/`` (one copy for the fleet) and is tested there:
lifecycle and pricing in ``googleai/tests/test_models.py``, lane order and secret hygiene in
``test_credentials.py``, refusals and modality-interleaved responses in ``test_client.py``, and
registry-versus-reality in ``test_probe_live.py``.

What is Canvas's and therefore tested HERE: the ``ImageClient`` conformance ``dispatch`` relies on,
the ``SUPPORTED_ASPECTS`` class attribute ``extract.plan`` reads without constructing a client, the
tier-alias mapping, and graceful behaviour when the shared layer is absent.
"""

from __future__ import annotations

import os
from types import SimpleNamespace

import pytest

from comic_render.aspect import DEFAULT_SUPPORTED
from comic_render.backends import GENERATE_BACKENDS, make_generate_client, supported_aspects_for
from comic_render.backends import gemini as backend
from comic_render.backends.gemini import (
    TIER_ALIASES,
    GeminiCredentialError,
    GeminiImageClient,
    projected_spend,
)

HAS_SHARED_LAYER = backend._ga is not None
needs_layer = pytest.mark.skipif(not HAS_SHARED_LAYER, reason="Home.aDNA/googleai not on this node")


class FakeSharedClient:
    """Stands in for ``googleai.GoogleAIClient`` — the seam this backend binds to."""

    def __init__(self, result=None):
        self.lane = "C63 SS_GEMINI_VERTEX_SA (vertex)"
        self.result = result or {"success": True, "image_path": "x.png", "model": "gemini-3-pro-image",
                                 "image_size": "2K", "cost_usd": 0.134}
        self.calls = []

    def resolve(self, name):
        return SimpleNamespace(id="gemini-3-pro-image")

    def cost_of(self, name, image_size="2K"):
        return 0.134

    def generate_image(self, text, output_path, **kw):
        self.calls.append({"text": text, "output_path": output_path, **kw})
        return self.result


class TestBinding:
    def test_forwards_to_the_shared_layer_and_returns_its_contract(self):
        shared = FakeSharedClient()
        c = GeminiImageClient(client=shared)
        r = c.generate_image("a lighthouse", "out.png", aspect_ratio="2:3")
        assert r["success"] is True
        assert shared.calls[0]["output_path"] == "out.png"
        assert shared.calls[0]["aspect_ratio"] == "2:3"

    def test_unwraps_an_ImagePrompt(self):
        from canvas_core.image_generation import ImagePrompt

        shared = FakeSharedClient()
        GeminiImageClient(client=shared).generate_image(ImagePrompt(text="hello"), "out.png")
        assert shared.calls[0]["text"] == "hello"

    def test_cost_per_image_is_real_so_the_budget_cap_bites(self):
        c = GeminiImageClient(client=FakeSharedClient())
        assert c.cost_per_image == 0.134

    def test_exposes_the_lane_so_a_spend_report_can_name_it(self):
        c = GeminiImageClient(client=FakeSharedClient())
        assert "C63" in c.lane

    def test_a_failure_is_returned_not_raised(self):
        shared = FakeSharedClient(result={"success": False, "error": "refused"})
        r = GeminiImageClient(client=shared).generate_image("x", "out.png")
        assert r["success"] is False
        # dispatch runs a whole issue; one refused panel must not abandon the rest.

    def test_only_successful_calls_are_recorded(self):
        shared = FakeSharedClient(result={"success": False, "error": "refused"})
        c = GeminiImageClient(client=shared)
        c.generate_image("x", "out.png")
        assert c.calls == []


class TestTierAliases:
    def test_the_wiring_default_tier_maps_to_the_ruled_pro_class(self):
        # ImagenWiring.DEFAULT_MODEL is "pro" — the operator's 2026-08-04 ruling.
        assert TIER_ALIASES["pro"] == "image.pro"

    def test_ultra_maps_to_pro_not_to_a_dying_imagen_model(self):
        # "ultra" used to mean imagen-4.0-ultra, which retires 2026-08-17.
        assert TIER_ALIASES["ultra"] == "image.pro"

    def test_no_alias_names_a_raw_model_id(self):
        # Every value must be a capability alias — a literal here would reintroduce the drift.
        assert all(v.startswith(("image.", "text.")) for v in TIER_ALIASES.values())


class TestPlanIntegration:
    def test_supported_aspects_readable_without_constructing_a_client(self, monkeypatch):
        # THE property that keeps planning free of credentials.
        for name in ("SS_GEMINI_VERTEX_SA", "WGA_GEMINI_API_KEY", "SWS_GEMINI_API_KEY",
                     "SS_GEMINI_API_KEY", "GEMINI_API_KEY"):
            monkeypatch.delenv(name, raising=False)
        assert supported_aspects_for("gemini") == backend.SUPPORTED_ASPECT_RATIOS

    @needs_layer
    def test_the_menu_comes_from_the_shared_registry(self):
        assert len(backend.SUPPORTED_ASPECT_RATIOS) == 14
        assert "2:3" in backend.SUPPORTED_ASPECT_RATIOS

    @needs_layer
    def test_the_splash_snaps_to_2_3_on_this_menu(self, canvas_path, monkeypatch):
        # The payoff of backend-owned menus: ~3% residual instead of the conservative menu's ~14%.
        from comic_render.extract import plan

        manifest, _ = plan(canvas_path, chain="generate:gemini")
        splash = manifest.panel("spread0_page0_p0")
        assert splash.aspect_ratio == "3:4"          # the author's declaration, untouched
        assert splash.effective_aspect_ratio == "2:3"
        assert splash.aspect_snap_error < 0.04

    def test_projected_spend_for_the_mini_issue_run(self):
        if not HAS_SHARED_LAYER:
            pytest.skip("needs the shared registry for pricing")
        assert projected_spend(27) == pytest.approx(3.618)


class TestRegistry:
    def test_gemini_is_a_live_generate_backend(self):
        assert GENERATE_BACKENDS["gemini"] is GeminiImageClient

    @needs_layer
    def test_constructing_it_resolves_a_lane(self):
        assert isinstance(make_generate_client("gemini"), GeminiImageClient)

    def test_generate_comfy_still_refuses(self):
        with pytest.raises(NotImplementedError):
            make_generate_client("comfy")


class TestDegradation:
    def test_the_package_imports_without_the_shared_layer(self):
        # backends/__init__ imports this module, so a hard dependency here would stop a node
        # without Home.aDNA from running even the offline `fake` pipeline.
        assert backend.SUPPORTED_ASPECT_RATIOS
        if not HAS_SHARED_LAYER:
            assert backend.SUPPORTED_ASPECT_RATIOS == DEFAULT_SUPPORTED

    def test_constructing_without_the_layer_says_what_to_do(self, monkeypatch):
        monkeypatch.setattr(backend, "_ga", None)
        with pytest.raises(GeminiCredentialError) as exc:
            GeminiImageClient()
        assert "generate:fake" in str(exc.value)
        assert "googleai" in str(exc.value)


@pytest.mark.network
def test_live_smoke_one_image(tmp_path):
    """The only test here that can spend money. Skips unless explicitly enabled."""
    if not HAS_SHARED_LAYER or not os.environ.get("COMIC_RENDER_LIVE_SMOKE"):
        pytest.skip("set COMIC_RENDER_LIVE_SMOKE=1 to run (costs ~$0.13)")
    c = GeminiImageClient()
    r = c.generate_image("a lighthouse at dusk, cel-shaded comic panel",
                         str(tmp_path / "smoke.png"), aspect_ratio="2:3", image_size="2K")
    assert r["success"] is True, r.get("error")
    assert (tmp_path / "smoke.png").stat().st_size > 10_000
