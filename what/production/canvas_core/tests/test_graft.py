"""Tests for canvas_core/graft.py — auto-graft tooling.

10 cases per M-V1-10 S1 plan slate (Stanley election 2026-05-07 Q1
2-session conservative-plus): manifest schema validation + dry-run modes
+ apply modes + 3-way conflict reporting + fixture E2E + negatives +
GraftReport shape.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from pathlib import Path

import pytest

from canvas_core.graft import (
    GraftEntry,
    GraftManifest,
    GraftPolicy,
    GraftReport,
    auto_graft,
)

# Pin the fixture path inside the substrate test corpus per the M-V1-10
# plan-agent CR4-silent-breach mitigation: future maintainers cannot move
# the fixtures without breaking this constant.
FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "graft_demo"
CANONICAL_DIR = FIXTURE_ROOT / "canonical"
WRAPPER_DIR = FIXTURE_ROOT / "wrapper_mock"
MANIFEST_PATH = FIXTURE_ROOT / "manifest.yaml"


# 1. Manifest YAML schema validates required keys + types.
def test_manifest_yaml_schema_validates() -> None:
    manifest = GraftManifest.from_yaml(MANIFEST_PATH)
    assert manifest.schema_version == 1
    assert len(manifest.tracked_files) == 3
    assert all(isinstance(e, GraftEntry) for e in manifest.tracked_files)
    canonical_paths = [e.canonical_path for e in manifest.tracked_files]
    assert "canvas_overview.md" in canonical_paths
    assert "voice_register_doctrine.md" in canonical_paths
    assert "three_way_conflict.md" in canonical_paths


# 2. Dry-run detects canonical-only-changed (canvas_overview.md).
def test_dry_run_detects_canonical_changes() -> None:
    manifest = GraftManifest.from_yaml(MANIFEST_PATH)
    report = auto_graft(
        canonical_dir=CANONICAL_DIR,
        wrapper_dir=WRAPPER_DIR,
        manifest=manifest,
        policy=GraftPolicy.REQUIRE_CONFIRMATION,
        apply=False,
    )
    assert report.dry_run_only is True
    assert any("canvas_overview.md" in c for c in report.changes_applied)
    assert all("canvas_overview.md" not in c for c in report.changes_skipped)


# 3. Dry-run respects wrapper overrides when canonical unchanged from baseline.
def test_dry_run_respects_wrapper_overrides_when_canonical_unchanged() -> None:
    manifest = GraftManifest.from_yaml(MANIFEST_PATH)
    report = auto_graft(
        canonical_dir=CANONICAL_DIR,
        wrapper_dir=WRAPPER_DIR,
        manifest=manifest,
        policy=GraftPolicy.REQUIRE_CONFIRMATION,
        apply=False,
    )
    assert any(
        "voice_register_doctrine.md" in c and "wrapper override preserved" in c
        for c in report.changes_skipped
    )
    assert all(
        "voice_register_doctrine.md" not in c for c in report.changes_applied
    )


# 4. Apply writes canonical when canonical-only-changed (under PRESERVE_WRAPPER_OVERRIDES).
def test_apply_writes_canonical_when_changed_only_canonical_side(
    tmp_path: Path,
) -> None:
    # Copy fixture wrapper tree into a tmp dir so writes don't mutate fixtures.
    tmp_wrapper = tmp_path / "wrapper"
    tmp_wrapper.mkdir()
    for src in WRAPPER_DIR.iterdir():
        (tmp_wrapper / src.name).write_text(src.read_text())
    manifest = GraftManifest.from_yaml(MANIFEST_PATH)
    canonical_text_pre = (CANONICAL_DIR / "canvas_overview.md").read_text()
    report = auto_graft(
        canonical_dir=CANONICAL_DIR,
        wrapper_dir=tmp_wrapper,
        manifest=manifest,
        policy=GraftPolicy.PRESERVE_WRAPPER_OVERRIDES,
        apply=True,
    )
    assert report.dry_run_only is False
    wrapper_text_post = (tmp_wrapper / "canvas_overview.md").read_text()
    assert wrapper_text_post == canonical_text_pre
    assert any(
        "canvas_overview.md" in c and "replaced wrapper with canonical" in c
        for c in report.changes_applied
    )


# 5. Apply preserves wrapper override when canonical unchanged from baseline.
def test_apply_preserves_wrapper_override_when_canonical_unchanged(
    tmp_path: Path,
) -> None:
    tmp_wrapper = tmp_path / "wrapper"
    tmp_wrapper.mkdir()
    for src in WRAPPER_DIR.iterdir():
        (tmp_wrapper / src.name).write_text(src.read_text())
    manifest = GraftManifest.from_yaml(MANIFEST_PATH)
    wrapper_text_pre = (tmp_wrapper / "voice_register_doctrine.md").read_text()
    auto_graft(
        canonical_dir=CANONICAL_DIR,
        wrapper_dir=tmp_wrapper,
        manifest=manifest,
        policy=GraftPolicy.PRESERVE_WRAPPER_OVERRIDES,
        apply=True,
    )
    wrapper_text_post = (tmp_wrapper / "voice_register_doctrine.md").read_text()
    assert wrapper_text_post == wrapper_text_pre  # no-op


# 6. Apply reports three-way conflict; never writes regardless of policy.
def test_apply_reports_conflict_three_way(tmp_path: Path) -> None:
    tmp_wrapper = tmp_path / "wrapper"
    tmp_wrapper.mkdir()
    for src in WRAPPER_DIR.iterdir():
        (tmp_wrapper / src.name).write_text(src.read_text())
    manifest = GraftManifest.from_yaml(MANIFEST_PATH)
    wrapper_text_pre = (tmp_wrapper / "three_way_conflict.md").read_text()
    report = auto_graft(
        canonical_dir=CANONICAL_DIR,
        wrapper_dir=tmp_wrapper,
        manifest=manifest,
        policy=GraftPolicy.REPLACE_CANONICAL,
        apply=True,
    )
    wrapper_text_post = (tmp_wrapper / "three_way_conflict.md").read_text()
    assert wrapper_text_post == wrapper_text_pre  # conflict blocked the write
    assert any(
        "three_way_conflict.md" in c and "3-way conflict" in c
        for c in report.conflicts
    )


# 7. Fixture end-to-end: 1 canonical-update applied + 1 wrapper-override preserved + 1 conflict.
def test_fixture_end_to_end_three_file_graft() -> None:
    manifest = GraftManifest.from_yaml(MANIFEST_PATH)
    report = auto_graft(
        canonical_dir=CANONICAL_DIR,
        wrapper_dir=WRAPPER_DIR,
        manifest=manifest,
        policy=GraftPolicy.REQUIRE_CONFIRMATION,
        apply=False,
    )
    assert len(report.changes_applied) == 1  # canvas_overview.md
    assert len(report.changes_skipped) == 1  # voice_register_doctrine.md
    assert len(report.conflicts) == 1  # three_way_conflict.md
    assert len(report.errors) == 0
    assert report.dry_run_only is True


# 8. Missing manifest path raises ValueError.
def test_missing_manifest_raises_value_error(tmp_path: Path) -> None:
    missing = tmp_path / "does_not_exist.yaml"
    with pytest.raises(ValueError, match="not found"):
        GraftManifest.from_yaml(missing)


# 9. Invalid policy (non-GraftPolicy) raises ValueError.
def test_invalid_policy_string_raises_value_error() -> None:
    manifest = GraftManifest.from_yaml(MANIFEST_PATH)
    with pytest.raises(ValueError, match="GraftPolicy"):
        auto_graft(
            canonical_dir=CANONICAL_DIR,
            wrapper_dir=WRAPPER_DIR,
            manifest=manifest,
            policy="bogus",  # type: ignore[arg-type]
            apply=False,
        )


# 10. GraftReport dataclass exposes exactly the 5 spec fields.
def test_graft_report_has_five_fields() -> None:
    report = GraftReport()
    expected_fields = {
        "changes_applied",
        "changes_skipped",
        "conflicts",
        "errors",
        "dry_run_only",
    }
    actual_fields = {f.name for f in report.__dataclass_fields__.values()}
    assert actual_fields == expected_fields
