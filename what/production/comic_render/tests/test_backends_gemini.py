"""The ``gemini`` generate backend (H3) — offline, against the recorded API shape.

No network. The SDK client is injected, and the fake responses reproduce the shape recorded in
``tests/fixtures/gemini/api_surface_20260809.json``: modality-interleaved parts, refusals that
arrive as a 200 with no image part, and the result contract ``dispatch`` depends on.

The live-path smoke at the foot is marked ``network`` and is the only thing here that can spend.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from types import SimpleNamespace

import pytest

from comic_render.backends import GENERATE_BACKENDS, make_generate_client, supported_aspects_for
from comic_render.backends.gemini import (
    API_KEY_ENV,
    MODELS,
    PRICING,
    SUPPORTED_ASPECT_RATIOS,
    GeminiCredentialError,
    GeminiImageClient,
    projected_spend,
)

PNG = b"\x89PNG\r\n\x1a\n" + b"fake-bytes"
SURFACE = json.loads(
    (Path(__file__).parent / "fixtures" / "gemini" / "api_surface_20260809.json").read_text()
)


# --------------------------------------------------------------------------------------------
# Fake SDK doubles — the shape the real client returns, per the recorded capture
# --------------------------------------------------------------------------------------------


def _response(parts):
    return SimpleNamespace(
        candidates=[SimpleNamespace(content=SimpleNamespace(parts=parts), finish_reason="STOP")]
    )


def _image_part(data=PNG):
    return SimpleNamespace(inline_data=SimpleNamespace(data=data))


def _text_part(text="here is your image"):
    return SimpleNamespace(inline_data=None, text=text)


class FakeSDK:
    """Stands in for ``genai.Client`` — records the call, returns a scripted response."""

    def __init__(self, response=None, raises=None):
        self._response = response if response is not None else _response([_image_part()])
        self._raises = raises
        self.calls = []
        self.models = SimpleNamespace(generate_content=self._generate_content)

    def _generate_content(self, **kwargs):
        self.calls.append(kwargs)
        if self._raises:
            raise self._raises
        return self._response


def client(**kw):
    sdk = kw.pop("sdk", None) or FakeSDK()
    return GeminiImageClient(client=sdk, **kw), sdk


# --------------------------------------------------------------------------------------------


class TestCredential:
    def test_missing_key_raises_and_names_the_variable(self, monkeypatch):
        monkeypatch.delenv(API_KEY_ENV, raising=False)
        with pytest.raises(GeminiCredentialError) as exc:
            GeminiImageClient()
        assert API_KEY_ENV in str(exc.value)

    def test_the_key_value_never_appears_in_the_error(self, monkeypatch):
        monkeypatch.delenv(API_KEY_ENV, raising=False)
        with pytest.raises(GeminiCredentialError) as exc:
            GeminiImageClient()
        # Broker discipline: names only. The message may say what is missing, never what it is.
        assert "sk-" not in str(exc.value) and "AIza" not in str(exc.value)

    def test_reads_the_key_from_the_environment_by_name(self, monkeypatch, tmp_path):
        monkeypatch.setenv(API_KEY_ENV, "test-key-value")
        c = GeminiImageClient()
        assert c._api_key == "test-key-value"

    def test_the_key_is_absent_from_every_success_result(self, monkeypatch, tmp_path):
        monkeypatch.setenv(API_KEY_ENV, "test-key-value")
        c, _ = client()
        result = c.generate_image("a lighthouse", str(tmp_path / "a.png"), aspect_ratio="1:1")
        assert "test-key-value" not in json.dumps(result)


class TestGenerate:
    def test_writes_the_bytes_and_returns_the_contract(self, tmp_path):
        c, _sdk = client()
        out = tmp_path / "panel_v1.png"
        r = c.generate_image("a lighthouse at dusk", str(out), aspect_ratio="2:3")
        assert r["success"] is True
        assert r["image_path"] == str(out)
        assert out.read_bytes() == PNG
        assert r["adapter"] == "gemini"
        assert r["cost_usd"] == PRICING[("pro", "2K")]

    def test_finds_the_image_when_it_is_not_the_first_part(self, tmp_path):
        # Gemini interleaves modalities; assuming parts[0] is the image works until it doesn't.
        sdk = FakeSDK(_response([_text_part(), _image_part()]))
        c, _ = client(sdk=sdk)
        r = c.generate_image("x", str(tmp_path / "a.png"), aspect_ratio="1:1")
        assert r["success"] is True

    def test_a_refusal_is_a_failure_not_an_empty_success(self, tmp_path):
        # The safety-filter shape: HTTP 200, no image part. Succeeding here would write nothing
        # and report success, which is the worst available outcome.
        sdk = FakeSDK(_response([_text_part("I can't generate that")]))
        c, _ = client(sdk=sdk)
        r = c.generate_image("x", str(tmp_path / "a.png"), aspect_ratio="1:1")
        assert r["success"] is False
        assert "no image" in r["error"]
        assert not (tmp_path / "a.png").exists()

    def test_an_sdk_exception_is_returned_not_raised(self, tmp_path):
        # dispatch runs a whole issue; one refused panel must not abandon the other twenty-six.
        sdk = FakeSDK(raises=RuntimeError("429 RESOURCE_EXHAUSTED"))
        c, _ = client(sdk=sdk)
        r = c.generate_image("x", str(tmp_path / "a.png"), aspect_ratio="1:1")
        assert r["success"] is False
        assert "RESOURCE_EXHAUSTED" in r["error"]

    def test_requires_an_explicit_output_path(self):
        c, _ = client()
        assert c.generate_image("x", None)["success"] is False

    def test_creates_missing_parent_directories(self, tmp_path):
        c, _ = client()
        out = tmp_path / "runs" / "issue" / "p_v1.png"
        assert c.generate_image("x", str(out), aspect_ratio="1:1")["success"] is True
        assert out.exists()


class TestAspectAndSize:
    def test_forwards_the_requested_ratio_to_the_sdk(self, tmp_path):
        c, sdk = client()
        c.generate_image("x", str(tmp_path / "a.png"), aspect_ratio="9:16", image_size="4K")
        cfg = sdk.calls[0]["config"]
        assert cfg.image_config.aspect_ratio == "9:16"
        assert cfg.image_config.image_size == "4K"

    def test_refuses_an_unsupported_ratio_instead_of_substituting(self, tmp_path):
        # plan() already snapped to this backend's menu, so an unsupported value here means the
        # manifest and the backend disagree. Silently fixing it would hide that.
        c, sdk = client()
        r = c.generate_image("x", str(tmp_path / "a.png"), aspect_ratio="7:13")
        assert r["success"] is False
        assert "not supported" in r["error"]
        assert sdk.calls == [], "must not spend on a request it knows will be rejected"

    def test_the_declared_menu_matches_the_live_capture(self):
        # If the service's menu changes, this fails and points at the fixture to re-verify.
        assert sorted(SUPPORTED_ASPECT_RATIOS) == sorted(SURFACE["supported_aspect_ratios"])

    def test_an_invalid_image_size_falls_back_to_the_configured_one(self, tmp_path):
        c, sdk = client(image_size="2K")
        c.generate_image("x", str(tmp_path / "a.png"), aspect_ratio="1:1", image_size="9K")
        assert sdk.calls[0]["config"].image_config.image_size == "2K"

    def test_constructor_rejects_an_invalid_image_size(self):
        with pytest.raises(ValueError):
            GeminiImageClient(client=FakeSDK(), image_size="9K")


class TestModelSelection:
    def test_defaults_to_the_ruled_pro_image_class(self, tmp_path):
        c, sdk = client()
        c.generate_image("x", str(tmp_path / "a.png"), aspect_ratio="1:1")
        assert sdk.calls[0]["model"] == "gemini-3-pro-image"

    def test_ultra_is_an_alias_for_pro_not_a_dead_imagen_id(self, tmp_path):
        # The old Imagen tier vocabulary must resolve to something live: imagen-4.0-ultra is
        # deprecated with a 2026-08-17 shutdown.
        assert MODELS["ultra"] == MODELS["pro"]
        assert not MODELS["ultra"].startswith("imagen")

    def test_no_model_in_the_map_is_a_deprecated_imagen_id(self):
        assert not any(m.startswith("imagen") for m in MODELS.values())

    def test_env_override_wins(self, monkeypatch, tmp_path):
        monkeypatch.setenv("COMIC_RENDER_GEMINI_MODEL", "gemini-3.1-flash-image")
        c, sdk = client()
        c.generate_image("x", str(tmp_path / "a.png"), aspect_ratio="1:1")
        assert sdk.calls[0]["model"] == "gemini-3.1-flash-image"

    def test_every_model_id_exists_in_the_live_capture(self):
        available = {n.removeprefix("models/") for n in SURFACE["image_capable_models"]}
        assert set(MODELS.values()) <= available


class TestSpend:
    def test_cost_per_image_is_real_so_the_budget_cap_bites(self):
        c, _ = client()
        assert c.cost_per_image > 0, "a zero cost would make budget_cap decorative"

    def test_projected_spend_for_the_mini_issue_run(self):
        # 9 panels x 3 variants, the pre-ruled parameters. Reported BEFORE dispatching.
        assert projected_spend(27, "pro", "2K") == pytest.approx(3.618)

    def test_4k_pro_would_exceed_the_five_dollar_cap(self):
        # Recorded because it is the reason the live run requests 2K and leans on refine-upscale
        # for DPI, rather than simply asking for more pixels.
        assert projected_spend(27, "pro", "4K") > 5.0

    def test_pricing_matches_the_captured_table(self):
        captured = SURFACE["pricing_usd_per_image"]["gemini-3-pro-image"]
        assert PRICING[("pro", "1K")] == captured["1K"]
        assert PRICING[("pro", "2K")] == captured["2K"]
        assert PRICING[("pro", "4K")] == captured["4K"]


class TestRegistry:
    def test_gemini_is_a_live_generate_backend(self):
        assert GENERATE_BACKENDS["gemini"] is GeminiImageClient

    def test_no_longer_raises_not_implemented(self, monkeypatch):
        monkeypatch.setenv(API_KEY_ENV, "test-key-value")
        assert isinstance(make_generate_client("gemini"), GeminiImageClient)

    def test_plan_can_read_the_menu_without_a_credential(self, monkeypatch):
        # THE property that keeps planning free: no construction, so no key needed.
        monkeypatch.delenv(API_KEY_ENV, raising=False)
        assert supported_aspects_for("gemini") == SUPPORTED_ASPECT_RATIOS

    def test_generate_comfy_still_refuses(self):
        with pytest.raises(NotImplementedError):
            make_generate_client("comfy")


class TestPlanIntegrationWithTheRealMenu:
    def test_the_splash_snaps_to_2_3_on_geminis_richer_menu(self, canvas_path, monkeypatch):
        # With the real 14-entry menu the splash lands on 2:3 (~3% residual) instead of the
        # conservative default's 9:16 (~14%). This is the payoff for making the menu belong to
        # the backend rather than hardcoding one.
        monkeypatch.delenv(API_KEY_ENV, raising=False)
        from comic_render.extract import plan

        manifest, _ = plan(canvas_path, chain="generate:gemini")
        splash = manifest.panel("spread0_page0_p0")
        assert splash.aspect_ratio == "3:4"
        assert splash.effective_aspect_ratio == "2:3"
        assert splash.aspect_snap_error < 0.04


@pytest.mark.network
def test_live_smoke_one_image(tmp_path):
    """The only test here that can spend money. Skips unless explicitly enabled."""
    if not os.environ.get(API_KEY_ENV) or not os.environ.get("COMIC_RENDER_LIVE_SMOKE"):
        pytest.skip("set GEMINI_API_KEY and COMIC_RENDER_LIVE_SMOKE=1 to run (costs ~$0.13)")
    c = GeminiImageClient()
    r = c.generate_image(
        "a lighthouse at dusk, cel-shaded comic panel", str(tmp_path / "smoke.png"),
        aspect_ratio="2:3", image_size="2K",
    )
    assert r["success"] is True, r.get("error")
    assert (tmp_path / "smoke.png").stat().st_size > 10_000
