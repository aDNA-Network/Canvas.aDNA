"""Tests for canvas_core.rlhf.variant_board + the slot-sidecar path through review_collect.

Blueprint P4 b4.2. The board is the HR pilot's **second consumer** and the first surface that can
emit a reject through the S-4 gate opened at P2b, so the round-trip assertions here (a pick becomes
a real ``SelectionRecord``; a reject becomes a real reject signal; neither is synthesised from the
other) matter more than the geometry ones.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from canvas_core.rlhf import review_collect
from canvas_core.rlhf.run_manifest import ABSENT
from canvas_core.rlhf.variant_board import build_variant_board
from canvas_std import ConformanceLevel, validate_suite

FIXTURES = Path(__file__).parent / "fixtures" / "run_manifests"
VAULT_ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture()
def board(tmp_path: Path):
    return build_variant_board(FIXTURES / "well_formed.json", tmp_path / "board",
                               vault_root=VAULT_ROOT)


# ================================================================================================
# Shape — one choice per SLOT, not per variant
# ================================================================================================

def test_board_declares_one_pick_affordance_per_slot(board) -> None:
    doc = json.loads(board.canvas.read_text(encoding="utf-8"))
    affordances = doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["affordances"]

    assert affordances["panel_01.pick"]["kind"] == "choice"
    assert affordances["panel_01.pick"]["required"] is True
    assert affordances["panel_01.pick"]["options"] == [
        "panel_01_v1", "panel_01_v2", "panel_01_v3"]
    assert affordances["panel_02.pick"]["options"] == ["panel_02_v1", "panel_02_v2"]

    picks = [key for key in affordances if key.endswith(".pick")]
    assert len(picks) == 2, "one pick per slot — not one per variant"


def test_open_state_lists_the_picks(board) -> None:
    doc = json.loads(board.canvas.read_text(encoding="utf-8"))
    state = doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["state"]
    assert state["open"] == ["panel_01.pick", "panel_02.pick"]


def test_reject_is_keyed_on_the_variant_not_the_slot(board) -> None:
    """The III reject signal is derivable only when attributed to a variant (spec_rlhf_seam §4.3)."""
    doc = json.loads(board.canvas.read_text(encoding="utf-8"))
    affordances = doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["affordances"]
    assert affordances["panel_01_v1.verdict"]["options"] == ["reject"]
    assert "panel_01.reject" not in affordances


def test_one_sidecar_per_slot(board) -> None:
    assert set(board.sidecars) == {"panel_01", "panel_02"}
    fm = yaml.safe_load(board.sidecars["panel_01"].read_text(encoding="utf-8").split("---")[1])
    assert fm["type"] == "selection_sidecar"
    assert fm["slot_id"] == "panel_01"
    assert fm["options"] == ["panel_01_v1", "panel_01_v2", "panel_01_v3"]
    assert fm["pick"] is None and fm["rejected"] == []


# ================================================================================================
# Provenance floor
# ================================================================================================

def test_every_variant_node_carries_the_provenance_floor(board) -> None:
    doc = json.loads(board.canvas.read_text(encoding="utf-8"))
    types = doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
    qualities = types["panel_01_v1_image"]["qualities"]
    assert qualities["model"] == "sdxl_base_1.0"
    assert qualities["workflow"] == "workflow_comic_panel_refine.json"
    assert qualities["seed"] == "20260908"
    assert qualities["denoise"] == "0.4"
    assert qualities["lora_refs"] == []
    assert qualities["source_backend"] == "comfy"
    assert qualities["aspect_ratio"] == "1:1"


def test_a_provenance_gap_is_shown_as_absent_never_backfilled(tmp_path: Path) -> None:
    built = build_variant_board(FIXTURES / "missing_provenance.json", tmp_path / "b",
                                vault_root=VAULT_ROOT)
    doc = json.loads(built.canvas.read_text(encoding="utf-8"))
    types = doc["metadata"]["frontmatter"]["_reserved"]["component_types"]
    assert types["panel_01_v1_image"]["qualities"]["model"] == ABSENT
    # The sibling that DOES carry a model must not have leaked into the gap.
    assert types["panel_01_v2_image"]["qualities"]["model"] == "sdxl_base_1.0"

    header = next(n for n in doc["nodes"] if n["id"] == "board_header")
    assert "were not inferred" in header["text"]


# ================================================================================================
# Paths + geometry
# ================================================================================================

def test_image_nodes_are_vault_relative(board) -> None:
    """A manifest-relative path resolves for the builder's cwd and nowhere else.

    Asserted on the image nodes specifically: the assets live in the vault wherever the board is
    written, so this holds unconditionally. The sidecars are a separate case — see below.
    """
    doc = json.loads(board.canvas.read_text(encoding="utf-8"))
    images = [n for n in doc["nodes"] if n.get("type") == "file" and n["id"].endswith("_image")]
    assert images
    for node in images:
        assert not node["file"].startswith("/"), node["file"]
        assert (VAULT_ROOT / node["file"]).exists(), node["file"]


def test_a_board_written_inside_the_vault_is_wholly_vault_relative(tmp_path: Path) -> None:
    """Sidecar nodes can only be vault-relative when the board is written inside a vault.

    Built outside one — as the tmp-path fixtures are — the sidecar node falls back to an absolute
    path. That is the honest outcome rather than a fabricated relative path, and it costs nothing
    real: a board outside the vault cannot be opened in Obsidian anyway. Boards are written to
    ``what/artifacts/`` in practice (`adr_010`), which this asserts.
    """
    out = VAULT_ROOT / "what/artifacts" / f"_test_board_{tmp_path.name}"
    try:
        built = build_variant_board(FIXTURES / "well_formed.json", out, vault_root=VAULT_ROOT)
        doc = json.loads(built.canvas.read_text(encoding="utf-8"))
        for node in doc["nodes"]:
            if node.get("type") != "file":
                continue
            assert not node["file"].startswith("/"), node["file"]
            assert (VAULT_ROOT / node["file"]).exists(), node["file"]
    finally:
        import shutil
        shutil.rmtree(out, ignore_errors=True)


def test_board_self_gates_on_adna_native(board) -> None:
    doc = json.loads(board.canvas.read_text(encoding="utf-8"))
    report = validate_suite(doc, ConformanceLevel.ADNA_NATIVE)
    assert report.level_reached is ConformanceLevel.ADNA_NATIVE


def test_print_size_variant_never_overflows_its_cell(tmp_path: Path) -> None:
    """A 2062x3150 page reduces to 1031x1575 — the inherited sizer would have emitted it whole."""
    built = build_variant_board(FIXTURES / "print_size.json", tmp_path / "b",
                                vault_root=VAULT_ROOT)
    doc = json.loads(built.canvas.read_text(encoding="utf-8"))
    image = next(n for n in doc["nodes"] if n["id"] == "page_01_v1_image")
    assert image["width"] <= 420 and image["height"] <= 420


# ================================================================================================
# Never destroy operator signal
# ================================================================================================

def test_rebuild_refuses_to_overwrite_a_sidecar_carrying_a_pick(board, tmp_path: Path) -> None:
    sidecar = board.sidecars["panel_01"]
    text = sidecar.read_text(encoding="utf-8")
    sidecar.write_text(text.replace("pick: null", "pick: panel_01_v2"), encoding="utf-8")

    with pytest.raises(FileExistsError, match="carries a pick"):
        build_variant_board(FIXTURES / "well_formed.json", tmp_path / "board",
                            vault_root=VAULT_ROOT)

    build_variant_board(FIXTURES / "well_formed.json", tmp_path / "board",
                        vault_root=VAULT_ROOT, force=True)  # explicit override still works


# ================================================================================================
# The round trip — a pick reaches Schema-A, a reject reaches the reject path
# ================================================================================================

def _set(sidecar: Path, **fields) -> None:
    raw = sidecar.read_text(encoding="utf-8")
    _, front, body = raw.split("---", 2)
    fm = yaml.safe_load(front)
    fm.update(fields)
    sidecar.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---" + body,
                       encoding="utf-8")


def test_a_pick_becomes_a_selection_record(board, tmp_path: Path) -> None:
    _set(board.sidecars["panel_01"], pick="panel_01_v2", rating=4, note="cleanest linework")
    dataset, store = tmp_path / "ds", tmp_path / "store.json"

    counts = review_collect.collect(
        board.canvas, approver="tester", participant_kind="ai",
        dataset_root=dataset, store_path=store,
    )
    assert counts["selections"] == 1
    assert counts["skipped"] == 1, "the unanswered slot is skipped, not invented"

    records = list(dataset.rglob("*.json"))
    assert len(records) == 1
    record = json.loads(records[0].read_text(encoding="utf-8"))
    # pick_index must point at the picked variant within the slot's candidate set.
    assert record["variants"][record["pick_index"]]["image_path"].endswith("slot_a_v2.png")
    assert "variant-selection board" in record["pick_reason"]
    assert record["pick_reason"].count("panel_01_v2") >= 1


def test_the_candidate_set_is_the_slot_not_one_row_per_sidecar(board, tmp_path: Path) -> None:
    _set(board.sidecars["panel_01"], pick="panel_01_v1")
    review_collect.collect(board.canvas, approver="tester", participant_kind="ai",
                           dataset_root=tmp_path / "ds", store_path=tmp_path / "store.json")
    record = json.loads(next((tmp_path / "ds").rglob("*.json")).read_text(encoding="utf-8"))
    assert len(record["variants"]) == 5, "all five variants of the run are the candidate set"


def test_collect_is_idempotent(board, tmp_path: Path) -> None:
    _set(board.sidecars["panel_01"], pick="panel_01_v2")
    dataset, store = tmp_path / "ds", tmp_path / "store.json"
    kwargs = dict(approver="tester", participant_kind="ai",
                  dataset_root=dataset, store_path=store)

    first = review_collect.collect(board.canvas, **kwargs)
    canvas_after_first = board.canvas.read_text(encoding="utf-8")
    second = review_collect.collect(board.canvas, **kwargs)

    assert first["selections"] == 1 and second["selections"] == 0
    assert second["responses"] == 0
    assert board.canvas.read_text(encoding="utf-8") == canvas_after_first
    assert len(list(dataset.rglob("*.json"))) == 1


def test_an_explicit_reject_reaches_the_reject_path_and_the_pick_still_lands(
    board, tmp_path: Path,
) -> None:
    """Not picking is a skip; rejecting is a judgement. They are recorded as different things."""
    _set(board.sidecars["panel_01"], pick="panel_01_v1", rejected=["panel_01_v3"],
         defect_tags=["off-model"])
    counts = review_collect.collect(
        board.canvas, approver="tester", participant_kind="ai",
        dataset_root=tmp_path / "ds", store_path=tmp_path / "store.json",
        emit_rejects=True,
    )
    assert counts["selections"] == 1, "the pick still produces a Schema-A record"
    assert counts["rejects"] == 1, "the explicit reject produces a reject signal"

    doc = json.loads(board.canvas.read_text(encoding="utf-8"))
    responses = doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["responses"]
    affordances = {r["affordance"] for r in responses}
    assert "panel_01.pick" in affordances
    assert "panel_01_v3.verdict" in affordances
    # panel_01_v2 was neither picked nor rejected — it must carry no verdict at all.
    assert "panel_01_v2.verdict" not in affordances


def test_agent_attribution_is_recorded_honestly(board, tmp_path: Path) -> None:
    _set(board.sidecars["panel_02"], pick="panel_02_v1")
    review_collect.collect(board.canvas, approver="tester", participant_kind="ai",
                           dataset_root=tmp_path / "ds", store_path=tmp_path / "store.json")
    doc = json.loads(board.canvas.read_text(encoding="utf-8"))
    responses = doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["responses"]
    assert responses and all(r["participant"]["kind"] == "ai" for r in responses)


def test_dry_run_writes_nothing(board, tmp_path: Path) -> None:
    _set(board.sidecars["panel_01"], pick="panel_01_v2")
    before = board.canvas.read_bytes()
    dataset, store = tmp_path / "ds", tmp_path / "store.json"
    counts = review_collect.collect(board.canvas, approver="tester", participant_kind="ai",
                                    dataset_root=dataset, store_path=store, dry_run=True)
    assert counts["selections"] == 1          # would write
    assert board.canvas.read_bytes() == before
    assert not dataset.exists() and not store.exists()
