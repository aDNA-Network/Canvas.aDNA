"""Tests for canvas_core.rlhf.tuning_surface (Blueprint P4 b4.3).

The point of most of these is what the module **does not** do. `review_dispatch_contract v0` ships
no dispatcher, so the tuning surface's one `action` affordance must produce a durable *record* and
nothing else — and a refused request must leave no trace at all (D5, a clause Bearly earned by
finding a phantom record behind a refusal in their own loop).
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

import pytest
import yaml

from canvas_core.rlhf import tuning_surface as ts
from canvas_std import ConformanceLevel, validate_suite

FIXTURES = Path(__file__).parent / "fixtures" / "run_manifests"
VAULT_ROOT = Path(__file__).resolve().parents[3]
AT = "2026-09-08T20:00:00+00:00"


@pytest.fixture()
def surface(tmp_path: Path):
    return ts.build_tuning_surface(
        FIXTURES / "well_formed.json", tmp_path / "tune",
        variant_ids=("panel_01_v2",), vault_root=VAULT_ROOT,
    )


def _set(sidecar: Path, **fields) -> None:
    raw = sidecar.read_text(encoding="utf-8")
    _, front, body = raw.split("---", 2)
    fm = yaml.safe_load(front)
    fm.update(fields)
    sidecar.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---" + body,
                       encoding="utf-8")


# ================================================================================================
# It is a record, never a dispatch
# ================================================================================================

def test_module_contains_no_transport() -> None:
    """No HTTP client, no socket, no subprocess — v0 ships no dispatcher, and this must not sneak one in."""
    tree = ast.parse(Path(ts.__file__).read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    forbidden = {"requests", "httpx", "urllib", "http", "socket", "subprocess", "aiohttp", "websocket"}
    assert not (imported & forbidden), f"transport reached the tuning surface: {imported & forbidden}"


def test_the_record_declares_itself_requested_not_dispatched(surface, tmp_path: Path) -> None:
    _set(surface.sidecars["panel_01_v2"], denoise=0.55, re_render_requested=True)
    written, refused = ts.collect_requests(
        surface.sidecars["panel_01_v2"].parent, requested_by="tester", at=AT,
        request_dir=tmp_path / "req")
    assert not refused and len(written) == 1
    record = json.loads(written[0].read_text(encoding="utf-8"))
    assert record["status"] == "requested"
    assert record["contract"] == "review_dispatch_contract v0"


# ================================================================================================
# D1 — derivable intent, and an unset knob is ABSENT rather than restated
# ================================================================================================

def test_request_carries_only_what_the_operator_changed(surface, tmp_path: Path) -> None:
    _set(surface.sidecars["panel_01_v2"], denoise=0.62, prompt_delta="warmer light",
         re_render_requested=True)
    written, _ = ts.collect_requests(surface.sidecars["panel_01_v2"].parent,
                                     requested_by="tester", at=AT, request_dir=tmp_path / "req")
    record = json.loads(written[0].read_text(encoding="utf-8"))
    assert record["params"] == {"denoise": 0.62}, "steps/cfg/lora were untouched — not restated"
    assert record["prompt_delta"] == "warmer light"
    assert record["requested_by"] == "tester" and record["at"] == AT


def test_d2_and_d3_fields_are_mandatory(surface, tmp_path: Path) -> None:
    """A re-roll runs under its parent's contract (D2) and is linked to that parent (D3)."""
    _set(surface.sidecars["panel_01_v2"], steps=30, re_render_requested=True)
    written, _ = ts.collect_requests(surface.sidecars["panel_01_v2"].parent,
                                     requested_by="tester", at=AT, request_dir=tmp_path / "req")
    record = json.loads(written[0].read_text(encoding="utf-8"))
    assert record["parent_variant_id"] == "panel_01_v2"
    assert record["workflow"] == "workflow_comic_panel_refine.json"
    assert record["model"] == "sdxl_base_1.0"


def test_sidecar_knobs_are_seeded_empty_not_with_the_parent_values(surface) -> None:
    fm = yaml.safe_load(surface.sidecars["panel_01_v2"].read_text(encoding="utf-8").split("---")[1])
    assert fm["denoise"] is None and fm["steps"] is None and fm["cfg"] is None
    assert fm["parent_variant_id"] == "panel_01_v2"
    assert fm["re_render_requested"] is False


# ================================================================================================
# Refusals
# ================================================================================================

@pytest.mark.parametrize("fields,match", [
    ({"re_render_requested": True}, "nothing to re-render"),
    ({"re_render_requested": True, "denoise": 0.5, "parent_variant_id": ""}, "no parent_variant_id"),
    ({"re_render_requested": True, "denoise": 0.5, "workflow": ""}, "no workflow recorded"),
])
def test_undeliverable_intents_are_refused(surface, tmp_path: Path, fields, match) -> None:
    _set(surface.sidecars["panel_01_v2"], **fields)
    written, refused = ts.collect_requests(
        surface.sidecars["panel_01_v2"].parent, requested_by="tester", at=AT,
        request_dir=tmp_path / "req")
    assert not written
    assert len(refused) == 1 and match in refused[0]


def test_d5_a_refusal_leaves_zero_trace(surface, tmp_path: Path) -> None:
    """Guards run before any append; a refusal is file-count-invariant across every sink.

    Bearly's `bearly_s030` found this the expensive way — a phantom `approve` left behind a
    refusal in a single-machine loop. A batch that half-writes and then refuses is the same defect
    at higher cost, so the batch here is all-or-nothing.
    """
    request_dir = tmp_path / "req"
    before = sorted(p.name for p in tmp_path.rglob("*"))

    # One good, one undeliverable, in the same directory.
    _set(surface.sidecars["panel_01_v2"], denoise=0.5, re_render_requested=True)
    bad = surface.sidecars["panel_01_v2"].parent / "orphan.md"
    bad.write_text(
        "---\n" + yaml.safe_dump({"type": "tuning_sidecar", "re_render_requested": True,
                                  "denoise": 0.4, "parent_variant_id": ""}) + "---\n",
        encoding="utf-8")

    written, refused = ts.collect_requests(bad.parent, requested_by="tester", at=AT,
                                           request_dir=request_dir)
    assert refused and not written
    assert not request_dir.exists(), "a refused batch wrote a record for its healthy sibling"

    bad.unlink()
    after_cleanup = sorted(p.name for p in tmp_path.rglob("*"))
    assert set(before) <= set(after_cleanup)


def test_requests_are_idempotent_on_request_id(surface, tmp_path: Path) -> None:
    _set(surface.sidecars["panel_01_v2"], denoise=0.5, re_render_requested=True)
    kwargs = dict(requested_by="tester", at=AT, request_dir=tmp_path / "req")
    first, _ = ts.collect_requests(surface.sidecars["panel_01_v2"].parent, **kwargs)
    body = first[0].read_bytes()
    second, _ = ts.collect_requests(surface.sidecars["panel_01_v2"].parent, **kwargs)
    assert second == first
    assert first[0].read_bytes() == body
    assert len(list((tmp_path / "req").glob("*.json"))) == 1


def test_dry_run_writes_nothing(surface, tmp_path: Path) -> None:
    _set(surface.sidecars["panel_01_v2"], denoise=0.5, re_render_requested=True)
    written, refused = ts.collect_requests(
        surface.sidecars["panel_01_v2"].parent, requested_by="tester", at=AT,
        request_dir=tmp_path / "req", dry_run=True)
    assert written and not refused
    assert not (tmp_path / "req").exists()


def test_a_sidecar_without_the_intent_flag_is_ignored(surface, tmp_path: Path) -> None:
    _set(surface.sidecars["panel_01_v2"], denoise=0.5)   # knob set, button never pressed
    written, refused = ts.collect_requests(
        surface.sidecars["panel_01_v2"].parent, requested_by="tester", at=AT,
        request_dir=tmp_path / "req")
    assert not written and not refused


# ================================================================================================
# The surface itself
# ================================================================================================

def test_surface_declares_input_affordances_and_exactly_one_action(surface) -> None:
    doc = json.loads(surface.canvas.read_text(encoding="utf-8"))
    affordances = doc["metadata"]["frontmatter"]["_reserved"]["interaction"]["affordances"]
    inputs = {k for k, v in affordances.items() if v["kind"] == "input"}
    actions = {k for k, v in affordances.items() if v["kind"] == "action"}
    assert inputs == {f"panel_01_v2.{p}" for p in ts.TUNING_PARAMS}
    assert actions == {"panel_01_v2.re_render"}, "§1.2 specifies exactly one action affordance"


def test_surface_self_gates_on_adna_native(surface) -> None:
    doc = json.loads(surface.canvas.read_text(encoding="utf-8"))
    assert validate_suite(doc, ConformanceLevel.ADNA_NATIVE).level_reached is (
        ConformanceLevel.ADNA_NATIVE)


def test_rebuild_refuses_to_discard_a_pending_request(surface, tmp_path: Path) -> None:
    _set(surface.sidecars["panel_01_v2"], denoise=0.5, re_render_requested=True)
    with pytest.raises(FileExistsError, match="carries a re-render request"):
        ts.build_tuning_surface(FIXTURES / "well_formed.json", tmp_path / "tune",
                                variant_ids=("panel_01_v2",), vault_root=VAULT_ROOT)
