"""Fake backends + pure-Python PNG helpers — determinism, protocol conformance, chain data-flow."""

from __future__ import annotations

import pytest

from comic_render.backends import make_generate_client, make_refine_client
from comic_render.backends.comfy import ComfyRefineClient
from comic_render.backends.fake import FakeImageClient, FakeRefineClient, dims_for
from comic_render.png_meta import read_png_size, write_solid_png


def test_png_roundtrip(tmp_path):
    p = write_solid_png(tmp_path / "x.png", 40, 30, (10, 20, 30))
    assert read_png_size(p) == (40, 30)
    with pytest.raises(ValueError):
        write_solid_png(tmp_path / "bad.png", 0, 10, (0, 0, 0))
    (tmp_path / "junk.png").write_bytes(b"not a png")
    with pytest.raises(ValueError):
        read_png_size(tmp_path / "junk.png")


def test_dims_for_aspects():
    assert dims_for("1:1") == (2048, 2048)
    assert dims_for("3:4") == (1536, 2048)
    assert dims_for("16:9") == (2048, 1152)
    assert dims_for("3:4", "1K") == (768, 1024)
    assert dims_for("garbage") == (2048, 2048)  # malformed → 1:1


def test_fake_generate_is_deterministic_by_filename(tmp_path):
    client = FakeImageClient()
    a = tmp_path / "a" / "p_v1.png"
    b = tmp_path / "b" / "p_v1.png"  # same filename, different dir
    for out in (a, b):
        result = client.generate_image("prompt", output_path=str(out), aspect_ratio="3:4")
        assert result["success"]
    assert a.read_bytes() == b.read_bytes()  # location-independent
    c = tmp_path / "p_v2.png"  # different variant name → different bytes
    client.generate_image("prompt", output_path=str(c), aspect_ratio="3:4")
    assert c.read_bytes() != a.read_bytes()
    assert read_png_size(a) == (1536, 2048)


def test_fake_generate_requires_output_path():
    result = FakeImageClient().generate_image("prompt", output_path=None)
    assert result["success"] is False and "output_path" in result["error"]


def test_fake_refine_depends_on_seed_image_bytes(tmp_path):
    gen = FakeImageClient()
    seed1 = tmp_path / "s_v1.png"
    seed2 = tmp_path / "s_v2.png"
    gen.generate_image("p", output_path=str(seed1))
    gen.generate_image("p", output_path=str(seed2))

    refiner = FakeRefineClient()
    out1 = tmp_path / "r1.png"
    out2 = tmp_path / "r2.png"
    assert refiner.refine_image(str(seed1), "p", str(out1))["success"]
    assert refiner.refine_image(str(seed2), "p", str(out2))["success"]
    assert out1.read_bytes() != out2.read_bytes()  # chain data-flow: output tracks its seed image
    assert read_png_size(out1) == read_png_size(seed1)  # dims preserved

    again = tmp_path / "r1_again.png"
    refiner.refine_image(str(seed1), "p", str(again))
    assert again.read_bytes() == out1.read_bytes()  # deterministic

    missing = refiner.refine_image(str(tmp_path / "nope.png"), "p", str(tmp_path / "x.png"))
    assert missing["success"] is False


def test_registry_fake_available_gemini_still_gated(tmp_path):
    assert isinstance(make_generate_client("fake"), FakeImageClient)
    assert isinstance(make_refine_client("fake"), FakeRefineClient)
    with pytest.raises(NotImplementedError, match="H3"):
        make_generate_client("gemini")
    with pytest.raises(ValueError, match="unknown"):
        make_generate_client("dalle")


def test_comfy_is_a_refine_backend_only(tmp_path):
    """H4 opened the refine seam; ComfyUI is deliberately NOT a generate backend (ADR-003)."""
    assert isinstance(make_refine_client("comfy"), ComfyRefineClient)
    with pytest.raises(NotImplementedError, match="not a generate backend"):
        make_generate_client("comfy")
