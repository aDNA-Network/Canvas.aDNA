"""Halftone H5 — VisualDNA auto-compose tests.

The exit-criterion test is named for it: ``test_lora_less_compose_reference_images_only`` — reference-images-only
compose is Bearly's *required* path (rights-HELD LoRA) and Stanley's *effective* path (PENDING_TRAINING).

Fixture bundles are committed YAML (``fixtures/visual_dna/``) mirroring the LIVE bundle shapes; tests materialize
them into tmp ``<workspace>/<Vault>.aDNA/…`` trees with generated 1-px PNGs (no binary fixtures committed; real
``*.aDNA`` vault-root detection exercised hermetically — a bundle committed inside Canvas.aDNA would resolve
vault-root paths against Canvas.aDNA itself). Live-bundle smokes skip when the sibling vaults are absent.
"""

from __future__ import annotations

import base64
import json
import warnings
from pathlib import Path

import pytest
import yaml

from comic_generator import compose_input
from comic_generator.__main__ import main
from comic_generator.consume import build_comic
from comic_generator.model import ComicInput, load_comic

FIXTURES = Path(__file__).parent / "fixtures" / "visual_dna"
WORKSPACE = Path(__file__).resolve().parents[5]
LIVE_STANLEY = WORKSPACE / "ScienceStanley.aDNA/what/visual_dna/characters/stanley/stanley.yaml"
LIVE_BEARLY = WORKSPACE / "Bearly.aDNA/what/visual_dna/characters/bearly/bearly.yaml"

_PNG_1PX = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


def _materialize(tmp_path: Path, fixture: str, *, vault: str = "TestVault.aDNA",
                 convention: str = "bundle_dir") -> Path:
    """Copy a fixture bundle into a tmp workspace vault and create every referenced PNG (except '*missing*'),
    honoring the bundle's path convention (bundle-dir-relative vs vault-root-relative)."""
    bdir = tmp_path / vault / "what" / "visual_dna" / "characters" / "x"
    bdir.mkdir(parents=True, exist_ok=True)
    bpath = bdir / fixture
    bpath.write_text((FIXTURES / fixture).read_text(encoding="utf-8"), encoding="utf-8")
    vd = yaml.safe_load(bpath.read_text(encoding="utf-8"))["visual_dna"]
    root = bdir if convention == "bundle_dir" else tmp_path / vault
    for items in vd.get("reference_image_set", {}).values():
        for it in items if isinstance(items, list) else []:
            if isinstance(it, dict) and it.get("path") and "missing" not in it["path"]:
                target = root / it["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(_PNG_1PX)
    return bpath


def _load_quiet(path: Path) -> compose_input.Bundle:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return compose_input.load_bundle(path)


def _comic_dict(char_names=("stanley",), characters=None) -> dict:
    chars = characters if characters is not None else [{"name": n} for n in char_names]
    return {
        "title": "T",
        "id": "t_comic",
        "version": "0.1.0",
        "characters": chars,
        "pages": [
            {
                "number": 1,
                "layout_type": "splash",
                "panels": [{"panel_type": "splash", "scene": "s", "characters": list(char_names)}],
            }
        ],
    }


# ============================================================================================================
# The exit criterion + the LoRA pair-gate.
# ============================================================================================================

def test_lora_less_compose_reference_images_only(tmp_path):
    """H5 EXIT CRITERION: both live bundle shapes compose to reference-images-only — no trigger, no lora."""
    sp = _materialize(tmp_path, "stanley_like.yaml")
    bp = _materialize(tmp_path, "bearly_like.yaml", vault="Bearly.aDNA", convention="vault_root")
    raw = _comic_dict(("stanley", "bearly"))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out = compose_input.enrich_comic_dict(raw, [(None, _load_quiet(sp)), (None, _load_quiet(bp))])
    dumped = json.dumps(out)
    assert "trigger_word" not in dumped and "lora_ref" not in dumped
    rows = {c["name"]: c for c in out["characters"]}
    assert rows["stanley"]["reference_images"]
    assert rows["bearly"]["reference_images"] == ["Bearly.aDNA/what/corpus/characters/Bearly.png"]
    # The enriched dict still loads and the emitted qualities stay LoRA-less end-to-end.
    doc = build_comic(ComicInput.from_dict(out))
    assert "trigger_word" not in json.dumps(doc)


def test_pending_training_excludes_trigger_word_and_lora_ref(tmp_path):
    sp = _materialize(tmp_path, "stanley_like.yaml")
    b = _load_quiet(sp)
    assert any(e.get("trigger_word") == "sciencestanley" for e in b.lora_entries)  # present in the bundle…
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assets = compose_input.compose_assets(b, art_style="pixel")
    assert assets.trigger_word is None and assets.lora_ref is None  # …absent from the composed output


def test_trained_lora_emits_paired_trigger_and_ref(tmp_path):
    tp = _materialize(tmp_path, "trained_like.yaml")
    b = _load_quiet(tp)
    ghibli = compose_input.compose_assets(b, art_style="ghibli")
    assert (ghibli.trigger_word, ghibli.lora_ref) == (
        "testhero", "ComfyForge.aDNA/what/loras/hero_ghibli_v1.safetensors"
    )
    pixel = compose_input.compose_assets(b, art_style="pixel")  # register preference
    assert (pixel.trigger_word, pixel.lora_ref) == (
        "testhero_pixel", "ComfyForge.aDNA/what/loras/hero_pixel_v1.safetensors"
    )
    other = compose_input.compose_assets(b, art_style="noir")  # no register match -> first eligible
    assert other.trigger_word == "testhero"


def test_lora_refs_four_shapes(tmp_path):
    def entries_of(lora_yaml: str) -> tuple:
        p = tmp_path / "b.yaml"
        p.write_text(
            "visual_dna:\n  id: x_character_x\n  display_name: X\n  entity_type: character\n"
            "  version: '1.0'\n  status: active_canonical_anchor\n" + lora_yaml,
            encoding="utf-8",
        )
        return _load_quiet(p).lora_entries

    assert entries_of("  lora_refs: []\n") == ()                                   # spec list-form, empty
    assert entries_of("")[0:0] == () and entries_of("") == ()                      # absent
    assert entries_of("  lora_refs:\n    entries:\n      - {path: p, trigger_word: t, status: TRAINED}\n")[0]["path"] == "p"
    with pytest.warns(UserWarning, match="placeholder-string"):
        p = tmp_path / "c.yaml"
        p.write_text(
            "visual_dna:\n  id: y_character_y\n  display_name: Y\n  entity_type: character\n"
            "  version: '1.0'\n  status: active_canonical_anchor\n  lora_refs: 'see ComfyForge'\n",
            encoding="utf-8",
        )
        assert compose_input.load_bundle(p).lora_entries == ()


# ============================================================================================================
# Reference selection + path normalization.
# ============================================================================================================

def test_reference_paths_bundle_dir_relative_normalized(tmp_path):
    sp = _materialize(tmp_path, "stanley_like.yaml")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        refs = compose_input.select_reference_images(_load_quiet(sp))
    assert refs and all(r.startswith("TestVault.aDNA/") for r in refs)
    assert refs[0] == "TestVault.aDNA/what/visual_dna/characters/x/references/anchor_iconic_portrait.png"


def test_reference_paths_vault_root_relative_normalized(tmp_path):
    bp = _materialize(tmp_path, "bearly_like.yaml", vault="Bearly.aDNA", convention="vault_root")
    refs = compose_input.select_reference_images(_load_quiet(bp))
    assert refs == ["Bearly.aDNA/what/corpus/characters/Bearly.png"]


def test_ref_category_override_reaches_series_panels(tmp_path):
    """Bearly's self-declared primary references live outside the default set — the override reaches them."""
    bp = _materialize(tmp_path, "bearly_like.yaml", vault="Bearly.aDNA", convention="vault_root")
    refs = compose_input.select_reference_images(
        _load_quiet(bp), categories=("portraits", "series_panels")
    )
    assert "Bearly.aDNA/what/corpus/series/1. Bearly made it.png" in refs      # space in filename survives
    assert not any("practicing" in r for r in refs)                            # dual-listed -> discarded wins


def test_missing_reference_warns_and_skips(tmp_path):
    sp = _materialize(tmp_path, "stanley_like.yaml")
    with pytest.warns(UserWarning, match="does not resolve"):
        refs = compose_input.select_reference_images(_load_quiet(sp))
    assert not any("var_5_missing" in r for r in refs)


def test_strict_refs_raises(tmp_path):
    sp = _materialize(tmp_path, "stanley_like.yaml")
    with pytest.raises(FileNotFoundError, match="var_5_missing"):
        compose_input.select_reference_images(_load_quiet(sp), strict=True)


def test_discarded_items_excluded_by_substring(tmp_path):
    sp = _materialize(tmp_path, "stanley_like.yaml")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        refs = compose_input.select_reference_images(_load_quiet(sp))
    assert not any("var_4_expression_focused" in r for r in refs)  # on disk AND in a category — discarded wins


def test_mapping_categories_and_restricted_skipped(tmp_path):
    sp = _materialize(tmp_path, "stanley_like.yaml")
    bp = _materialize(tmp_path, "bearly_like.yaml", vault="Bearly.aDNA", convention="vault_root")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        s_refs = compose_input.select_reference_images(_load_quiet(sp))
        b_refs = compose_input.select_reference_images(
            _load_quiet(bp), categories=("portraits", "series_panels", "restricted")
        )
    assert not any("real_photos" in r for r in s_refs)   # mapping-shaped category never composes
    assert not any("blink" in r for r in b_refs)         # restricted never composes, even if named


def test_canonical_first_ordering_and_cap(tmp_path):
    sp = _materialize(tmp_path, "stanley_like.yaml")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        b = _load_quiet(sp)
        refs = compose_input.select_reference_images(b)
        capped = compose_input.select_reference_images(b, cap=2)
    names = [Path(r).name for r in refs]
    # canonical first (incl. a canonical item OUTSIDE the default category set), then category priority.
    assert names == [
        "anchor_iconic_portrait.png",
        "establishing_canonical.png",
        "var_1_portrait_closeup.png",
        "var_3_expression_warm_laughing.png",
        "var_2_wide_cinematic.png",
    ]
    assert "establishing_extra.png" not in names  # non-canonical outside the default set never composes
    assert [Path(r).name for r in capped] == ["anchor_iconic_portrait.png", "establishing_canonical.png"]


# ============================================================================================================
# Descriptor + matching + enrichment.
# ============================================================================================================

def test_descriptor_precedence_and_fallback_chain(tmp_path):
    tp = _materialize(tmp_path, "trained_like.yaml")
    assert compose_input.derive_descriptor(_load_quiet(tp)).startswith("A caped test hero,")  # compressed wins

    sp = _materialize(tmp_path, "stanley_like.yaml")
    assert "Ghibli-style" in compose_input.derive_descriptor(_load_quiet(sp))  # portrait fallback (short: no warn)

    big = tmp_path / "big.yaml"
    big.write_text(
        "visual_dna:\n  id: z_character_z\n  display_name: Z\n  entity_type: character\n"
        "  version: '1.0'\n  status: active_canonical_anchor\n"
        f"  text_prompt:\n    portrait_subset: \"{'x' * 900}\"\n",
        encoding="utf-8",
    )
    with pytest.warns(UserWarning, match="framing-lock"):
        compose_input.derive_descriptor(compose_input.load_bundle(big))

    # In.yaml author descriptor always wins; the bundle fills only empty ones.
    raw = _comic_dict(characters=[{"name": "hero", "descriptor": "author text"}])
    raw["pages"][0]["panels"][0]["characters"] = ["hero"]
    out = compose_input.enrich_comic_dict(raw, [(None, _load_quiet(tp))])
    assert out["characters"][0]["descriptor"] == "author text"
    raw2 = _comic_dict(characters=[{"name": "hero"}])
    raw2["pages"][0]["panels"][0]["characters"] = ["hero"]
    out2 = compose_input.enrich_comic_dict(raw2, [(None, _load_quiet(tp))])
    assert out2["characters"][0]["descriptor"].startswith("A caped test hero,")


def test_bundle_matching_heuristic_explicit_ambiguous_unmatched(tmp_path):
    sp = _materialize(tmp_path, "stanley_like.yaml")
    b = _load_quiet(sp)
    # Direction-safe: agent_stanley never matches Stanley's bundle…
    with pytest.raises(ValueError, match="no character"):
        compose_input.match_bundle_to_character(b, ["agent_stanley"])
    # …so alongside stanley it is unambiguous.
    assert compose_input.match_bundle_to_character(b, ["stanley", "agent_stanley"]) == "stanley"
    with pytest.raises(ValueError, match="ambiguous"):
        compose_input.match_bundle_to_character(b, ["stan", "stanley"])
    # Explicit name=bundle escape hatch + auto-created bible row for a panel-only character.
    raw = {"title": "T", "id": "t", "version": "1",
           "characters": [],
           "pages": [{"number": 1, "layout_type": "splash",
                      "panels": [{"panel_type": "splash", "scene": "s", "characters": ["stanley"]}]}]}
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        out = compose_input.enrich_comic_dict(raw, [(None, b)])
    assert out["characters"][0]["name"] == "stanley" and out["characters"][0]["reference_images"]
    assert out["composed_from"][0]["character"] == "stanley"
    # Recompose is idempotent for provenance (one entry per character).
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        again = compose_input.enrich_comic_dict(out, [(None, b)])
    assert len([e for e in again["composed_from"] if e["character"] == "stanley"]) == 1


def test_non_character_bundle_skipped_with_warning(tmp_path):
    p = tmp_path / "loc.yaml"
    p.write_text(
        "visual_dna:\n  id: lab_location\n  display_name: Lab\n  entity_type: location\n"
        "  version: '1.0'\n  status: active_canonical_anchor\n",
        encoding="utf-8",
    )
    raw = _comic_dict(("lab",))
    with pytest.warns(UserWarning, match="only characters compose"):
        out = compose_input.enrich_comic_dict(raw, [(None, compose_input.load_bundle(p))])
    assert "composed_from" not in out


def test_from_dict_maps_character_asset_fields():
    comic = ComicInput.from_dict(
        {
            "title": "T", "id": "t", "version": "1",
            "characters": [
                {"name": "a", "descriptor": "d", "trigger_word": "tw", "lora_ref": "lr",
                 "reference_images": ["V.aDNA/x.png"]},
                {"name": "b"},
            ],
            "pages": [{"number": 1, "panels": [{"panel_type": "action"}]}],
        }
    )
    a, b = comic.characters
    assert (a.trigger_word, a.lora_ref, a.reference_images) == ("tw", "lr", ("V.aDNA/x.png",))
    assert (b.trigger_word, b.lora_ref, b.reference_images) == (None, None, ())
    assets = comic.character_assets()
    assert set(assets) == {"a"} and assets["a"]["reference_images"] == ["V.aDNA/x.png"]


# ============================================================================================================
# Emission (qualities.characters) + E2E.
# ============================================================================================================

def _asset_comic() -> ComicInput:
    return ComicInput.from_dict(
        {
            "title": "T", "id": "t", "version": "1",
            "characters": [
                {"name": "a", "descriptor": "da", "reference_images": ["V.aDNA/a.png"]},
                {"name": "b", "descriptor": "db"},
            ],
            "pages": [
                {"number": 1, "panels": [
                    {"panel_type": "action", "characters": ["a"], "row": 0},
                    {"panel_type": "dialogue", "characters": ["b"], "row": 1},
                    {"panel_type": "close_up", "row": 2},
                ]},
            ],
        }
    )


def _panel_quals(doc: dict) -> dict[str, dict]:
    ct = doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
    return {nid: e.get("qualities", {}) for nid, e in ct.items() if e.get("class") == "image"}


def test_panels_emit_qualities_characters_per_panel_only():
    doc = build_comic(_asset_comic())
    quals = _panel_quals(doc)
    with_assets = {nid: q for nid, q in quals.items() if "characters" in q}
    assert len(with_assets) == 1  # only panel 'a' — 'b' has no asset fields, panel 3 no characters
    (entry,) = next(iter(with_assets.values()))["characters"]
    assert entry == {"name": "a", "reference_images": ["V.aDNA/a.png"]}
    # No aliasing: mutating the emitted entry must not touch the model's tuple-backed assets.
    entry["reference_images"].append("mutated")
    assert _asset_comic().characters[0].reference_images == ("V.aDNA/a.png",)


def test_qualities_characters_absent_without_assets(comic):
    doc = build_comic(comic)
    assert all("characters" not in q for q in _panel_quals(doc).values())


def test_cli_compose_writes_enriched_yaml_that_builds(tmp_path):
    sp = _materialize(tmp_path, "stanley_like.yaml")
    inp = tmp_path / "in.yaml"
    inp.write_text(yaml.safe_dump(_comic_dict(("stanley",)), sort_keys=False), encoding="utf-8")
    enriched = tmp_path / "in.composed.yaml"
    out_canvas = tmp_path / "out.canvas"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert main(["compose", str(inp), "-o", str(enriched), "--bundle", str(sp)]) == 0
        comic = load_comic(enriched)
        assert comic.characters[0].reference_images
        assert main(["build", str(enriched), str(out_canvas)]) == 0
    doc = json.loads(out_canvas.read_text(encoding="utf-8"))
    assert any("characters" in q for q in _panel_quals(doc).values())


def test_cli_compose_requires_a_bundle(tmp_path, capsys):
    inp = tmp_path / "in.yaml"
    inp.write_text(yaml.safe_dump(_comic_dict()), encoding="utf-8")
    assert main(["compose", str(inp), "-o", str(tmp_path / "o.yaml")]) == 2


def test_e2e_build_bundle_one_shot_carries_characters_into_canvas(tmp_path):
    sp = _materialize(tmp_path, "stanley_like.yaml")
    inp = tmp_path / "in.yaml"
    inp.write_text(yaml.safe_dump(_comic_dict(("stanley",)), sort_keys=False), encoding="utf-8")
    out_canvas = tmp_path / "out.canvas"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert main(["build", str(inp), str(out_canvas), "--bundle", f"stanley={sp}"]) == 0
    doc = json.loads(out_canvas.read_text(encoding="utf-8"))
    quals = [q for q in _panel_quals(doc).values() if "characters" in q]
    assert quals and quals[0]["characters"][0]["name"] == "stanley"
    assert "trigger_word" not in json.dumps(doc)  # PENDING_TRAINING stays LoRA-less end-to-end


# ============================================================================================================
# Live-bundle smokes (skip when the sibling vaults are absent on this machine).
# ============================================================================================================

@pytest.mark.skipif(not LIVE_STANLEY.exists(), reason="live Stanley bundle not present")
def test_live_stanley_bundle_smoke():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assets = compose_input.compose_assets(compose_input.load_bundle(LIVE_STANLEY), art_style="ghibli")
    assert assets.trigger_word is None and assets.lora_ref is None  # PENDING_TRAINING -> LoRA-less
    assert assets.reference_images and all(
        r.startswith("ScienceStanley.aDNA/") for r in assets.reference_images
    )
    assert assets.descriptor  # portrait_subset fallback


@pytest.mark.skipif(not LIVE_BEARLY.exists(), reason="live Bearly bundle not present")
def test_live_bearly_bundle_smoke():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assets = compose_input.compose_assets(compose_input.load_bundle(LIVE_BEARLY))
    assert assets.trigger_word is None and assets.lora_ref is None  # rights-HELD [] -> LoRA-less
    assert assets.reference_images and all(
        r.startswith("Bearly.aDNA/") for r in assets.reference_images
    )
