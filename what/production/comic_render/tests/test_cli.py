"""CLI — stage ordering, run --until, resumability, exit codes (in-process)."""

from __future__ import annotations

import json

from comic_render.cli import main
from conftest import PAGE_COUNT


def test_run_until_compose_full_pipeline(canvas_path):
    assert main(["run", "--until", "compose", str(canvas_path)]) == 0
    base = canvas_path.parent
    assert (base / "mini_issue.render_manifest.json").exists()
    assert (base / "mini_issue.rendered.canvas").exists()
    assert len(list((base / "runs/science_stanley_mini/pages").glob("*.jpg"))) == PAGE_COUNT


def test_rerun_is_idempotent(canvas_path, capsys):
    assert main(["run", "--until", "validate", str(canvas_path)]) == 0
    capsys.readouterr()
    assert main(["run", "--until", "validate", str(canvas_path)]) == 0
    out = capsys.readouterr().out
    assert "generated=[]" in out and "selected=[]" in out  # zero new work


def test_run_until_stops_early(canvas_path):
    assert main(["run", "--until", "dispatch", str(canvas_path)]) == 0
    base = canvas_path.parent
    assert (base / "runs/science_stanley_mini").exists()
    assert not (base / "mini_issue.rendered.canvas").exists()


def test_json_output_parses(canvas_path, capsys):
    assert main(["--json", "plan", str(canvas_path)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["stage"] == "plan" and payload["panels"] == 9


def test_stage_before_plan_is_usage_error(canvas_path, capsys):
    assert main(["dispatch", str(canvas_path)]) == 2
    assert "run plan first" in capsys.readouterr().err


def test_stale_manifest_is_gate_fail(canvas_path, capsys):
    assert main(["plan", str(canvas_path)]) == 0
    doc = json.loads(canvas_path.read_text())
    doc["nodes"].append({"id": "intruder", "type": "text", "text": "x",
                         "x": 0, "y": 0, "width": 10, "height": 10})
    canvas_path.write_text(json.dumps(doc))
    assert main(["dispatch", str(canvas_path)]) == 1
    assert "GATE FAIL" in capsys.readouterr().err


def test_missing_canvas_is_usage_error(tmp_path):
    assert main(["plan", str(tmp_path / "nope.canvas")]) == 2


def test_chain_flag_flows_to_manifest(canvas_path):
    assert main(["plan", str(canvas_path), "--chain", "generate:fake,refine:fake@0.4",
                 "--variants", "2", "--budget-cap", "3.5", "--register", "reg_cli"]) == 0
    manifest = json.loads((canvas_path.parent / "mini_issue.render_manifest.json").read_text())
    assert manifest["budget_cap"] == 3.5 and manifest["register"] == "reg_cli"
    assert manifest["panels"][0]["variant_count"] == 2
    assert [s["stage"] for s in manifest["panels"][0]["render_chain"]] == ["generate", "refine"]
