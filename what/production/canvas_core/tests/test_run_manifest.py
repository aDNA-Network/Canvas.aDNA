"""Tests for canvas_core.rlhf.run_manifest (Blueprint P4 b4.1).

The fixtures under ``fixtures/run_manifests/`` are not incidental test data — they **are** the
contract ComfyUI's emitter has to satisfy (`spec_comfyui_canvas_emission` §3). Their side is
accepted-in-principle and unbuilt; pinning the interface in executable form rather than prose is
the point of building the consumer first.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from canvas_core.rlhf.run_manifest import (
    ABSENT,
    PROVENANCE_FIELDS,
    ManifestError,
    load_run_manifest,
)

FIXTURES = Path(__file__).parent / "fixtures" / "run_manifests"


# ================================================================================================
# The well-formed run
# ================================================================================================

def test_well_formed_run_loads_every_slot_and_variant() -> None:
    manifest = load_run_manifest(FIXTURES / "well_formed.json")
    assert manifest.run_id == "run_wellformed_20260908"
    assert manifest.driver == "comfyui"
    assert [slot.slot_id for slot in manifest.slots] == ["panel_01", "panel_02"]
    assert [len(slot.variants) for slot in manifest.slots] == [3, 2]
    assert manifest.variant_count == 5
    assert manifest.skipped == ()
    assert manifest.unknown_keys == ()


def test_provenance_floor_is_carried_per_variant() -> None:
    manifest = load_run_manifest(FIXTURES / "well_formed.json")
    variant = manifest.slots[0].variants[0]
    assert variant.workflow == "workflow_comic_panel_refine.json"
    assert variant.model == "sdxl_base_1.0"
    assert variant.seed == 20260908
    assert variant.denoise == 0.4
    assert variant.lora_refs == ()
    assert variant.source_backend == "comfy"
    assert variant.missing_provenance == ()
    assert manifest.provenance_gaps == {}


def test_paths_resolve_relative_to_the_manifest_not_the_cwd(tmp_path: Path) -> None:
    """The manifest travels with its pixels; the cwd is irrelevant to it."""
    manifest = load_run_manifest(FIXTURES / "well_formed.json")
    for slot in manifest.slots:
        for variant in slot.variants:
            assert variant.path.is_absolute() and variant.path.is_file()
            assert variant.path.parent == (FIXTURES / "images")


def test_image_dimensions_are_probed() -> None:
    manifest = load_run_manifest(FIXTURES / "well_formed.json")
    assert (manifest.slots[0].variants[0].width,
            manifest.slots[0].variants[0].height) == (512, 512)
    assert (manifest.slots[1].variants[0].width,
            manifest.slots[1].variants[0].height) == (768, 512)


# ================================================================================================
# A half-failed run is still reviewable — the filesystem outranks the run record
# ================================================================================================

def test_partially_failed_run_keeps_what_landed_and_names_what_did_not() -> None:
    manifest = load_run_manifest(FIXTURES / "partially_failed.json")
    assert manifest.variant_count == 1
    assert [slot.slot_id for slot in manifest.slots] == ["panel_01"]
    assert manifest.slots[0].variants[0].variant_id == "panel_01_v1"

    reasons = " ".join(manifest.skipped)
    assert "never_written.png not on disk" in reasons
    assert "panel_01_v3: no path" in reasons
    assert "panel_99" in reasons, "a slot that lost every variant must be named, not vanish"


def test_a_run_with_nothing_on_disk_raises_rather_than_returning_an_empty_board(
    tmp_path: Path,
) -> None:
    """An empty board is worse than an error: it looks like a run with nothing worth reviewing."""
    manifest_path = tmp_path / "empty.json"
    manifest_path.write_text(json.dumps({
        "run_id": "r", "slots": [{"slot_id": "s", "variants": [
            {"variant_id": "v1", "path": "nope.png"}]}]}), encoding="utf-8")
    with pytest.raises(ManifestError, match="no slot has a variant image on disk"):
        load_run_manifest(manifest_path)


# ================================================================================================
# Additive evolution — a newer emitter must load on an older consumer
# ================================================================================================

def test_unknown_keys_are_ignored_but_reported() -> None:
    manifest = load_run_manifest(FIXTURES / "unknown_keys.json")
    assert manifest.variant_count == 1, "unknown keys must not cost us a variant"
    assert set(manifest.unknown_keys) == {
        "scheduler_profile", "cost_usd",
        "slots[].aesthetic_target",
        "slots[].variants[].clip_skip", "slots[].variants[].refiner",
    }


# ================================================================================================
# Absence is explicit — never a fabricated default
# ================================================================================================

def test_missing_provenance_is_marked_absent_never_invented() -> None:
    manifest = load_run_manifest(FIXTURES / "missing_provenance.json")
    gapped, complete = manifest.slots[0].variants
    assert gapped.model is ABSENT
    assert gapped.workflow is ABSENT
    assert gapped.seed is ABSENT
    assert set(gapped.missing_provenance) == {"workflow", "model", "seed"}
    assert manifest.provenance_gaps == {"panel_01_v1": gapped.missing_provenance}

    # The gap must not be filled from a sibling that does carry the field.
    assert complete.model == "sdxl_base_1.0"
    assert gapped.model != complete.model


def test_absent_is_distinguishable_from_a_supplied_empty_value(tmp_path: Path) -> None:
    """``lora_refs: []`` is a statement (LoRA-less); a missing key is not."""
    image = FIXTURES / "images" / "slot_a_v1.png"
    manifest_path = tmp_path / "m.json"
    manifest_path.write_text(json.dumps({
        "run_id": "r", "slots": [{"slot_id": "s", "variants": [
            {"variant_id": "declared", "path": str(image), "lora_refs": []},
            {"variant_id": "silent", "path": str(image)},
        ]}]}), encoding="utf-8")
    declared, silent = load_run_manifest(manifest_path).slots[0].variants
    assert declared.lora_refs == ()
    assert "lora_refs" not in declared.missing_provenance
    assert silent.lora_refs is ABSENT
    assert "lora_refs" in silent.missing_provenance


def test_every_floor_field_is_checked() -> None:
    """Guards the floor list itself against drifting out of step with the spec."""
    assert set(PROVENANCE_FIELDS) == {
        "workflow", "model", "seed", "denoise", "lora_refs", "source_backend"}


# ================================================================================================
# Structural invalidity raises; incompleteness does not
# ================================================================================================

@pytest.mark.parametrize("payload,match", [
    ("[]", "must be a JSON object"),
    ('{"run_id": "r"}', "no slots"),
    ('{"run_id": "r", "slots": []}', "no slots"),
    ('{"run_id": "r", "slots": ["nope"]}', "must be an object"),
    ('{"run_id": "r", "slots": [{"slot_id": "s", "variants": "nope"}]}', "must be a list"),
])
def test_structural_invalidity_raises(tmp_path: Path, payload: str, match: str) -> None:
    path = tmp_path / "bad.json"
    path.write_text(payload, encoding="utf-8")
    with pytest.raises(ManifestError, match=match):
        load_run_manifest(path)


def test_unreadable_manifest_raises_cleanly(tmp_path: Path) -> None:
    with pytest.raises(ManifestError, match="no such manifest"):
        load_run_manifest(tmp_path / "absent.json")
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    with pytest.raises(ManifestError, match="not valid JSON"):
        load_run_manifest(bad)


def test_lora_refs_of_the_wrong_type_is_a_structural_error(tmp_path: Path) -> None:
    image = FIXTURES / "images" / "slot_a_v1.png"
    path = tmp_path / "m.json"
    path.write_text(json.dumps({"run_id": "r", "slots": [{"slot_id": "s", "variants": [
        {"variant_id": "v", "path": str(image), "lora_refs": "not-a-list"}]}]}), encoding="utf-8")
    with pytest.raises(ManifestError, match="lora_refs must be a list"):
        load_run_manifest(path)
