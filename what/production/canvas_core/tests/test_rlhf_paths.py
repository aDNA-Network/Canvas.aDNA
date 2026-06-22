"""Tests for RLHF SelectionRecord vault-relative path validator (F-36 amendment).

Per F-36 of M-CAMPAIGN-REFRESH-02 (2026-05-03), variant `image_path` MUST be
vault-relative. Absolute paths (operator-specific) break corpus portability per
ADR-003 D4. validate_selection_record surfaces absolute paths as schema errors.

Also verifies the migrated 3 records under what/artifacts/image_gen_dataset/2026-04/
load successfully under the new validator.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from canvas_core.rlhf.selection import (
    SelectionRecord,
    VariantInfo,
    _is_absolute_path,
    validate_selection_record,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_valid_record(image_path: str = "what/artifacts/test/img.png") -> SelectionRecord:
    """Construct a SelectionRecord that passes all OTHER validation checks."""
    return SelectionRecord(
        prompt="Test prompt",
        register="R3",
        variants=[VariantInfo(image_path=image_path, model="imagen-4-ultra")],
        pick_index=0,
        pick_reason="Test pick",
        approver_id="test_user",
    )


# ---------------------------------------------------------------------------
# F-36 amendment 2026-05-03: vault-relative path policy
# ---------------------------------------------------------------------------


class TestIsAbsolutePathHelper:
    """Unit-level coverage of _is_absolute_path detection."""

    def test_posix_absolute(self):
        assert _is_absolute_path("/Users/herb/lattice/CanvasForge.aDNA/what/img.png")

    def test_tilde_absolute(self):
        assert _is_absolute_path("~/aDNA/CanvasForge.aDNA/what/img.png")

    def test_vault_relative(self):
        assert not _is_absolute_path("what/artifacts/img.png")

    def test_nested_vault_relative(self):
        assert not _is_absolute_path("what/artifacts/image_gen_fidelity/imagen/x.png")

    def test_empty_string(self):
        assert not _is_absolute_path("")


class TestSelectionRecordValidator:
    """Validator surfaces absolute paths as schema errors per F-36."""

    def test_vault_relative_path_passes(self):
        record = _make_valid_record(image_path="what/artifacts/test/img.png")
        errors = validate_selection_record(record)
        assert errors == []

    def test_absolute_path_surfaces_error(self):
        record = _make_valid_record(
            image_path="/Users/herb/lattice/CanvasForge.aDNA/what/x.png"
        )
        errors = validate_selection_record(record)
        # Should contain at least one error mentioning vault-relative + path.
        assert len(errors) >= 1
        joined = " ".join(errors)
        assert "vault-relative" in joined
        assert "F-36" in joined

    def test_tilde_path_surfaces_error(self):
        record = _make_valid_record(image_path="~/aDNA/x.png")
        errors = validate_selection_record(record)
        assert len(errors) >= 1
        assert any("vault-relative" in e for e in errors)

    def test_multiple_variants_all_checked(self):
        record = SelectionRecord(
            prompt="Multi-variant test",
            register="R3",
            variants=[
                VariantInfo(image_path="what/artifacts/v1.png"),
                VariantInfo(image_path="/Users/herb/v2.png"),  # absolute - should fail
                VariantInfo(image_path="what/artifacts/v3.png"),
            ],
            pick_index=0,
            pick_reason="Test multi",
            approver_id="test_user",
        )
        errors = validate_selection_record(record)
        # Only variant[1] is absolute; expect exactly one path-related error.
        path_errors = [e for e in errors if "vault-relative" in e]
        assert len(path_errors) == 1
        assert "variants[1]" in path_errors[0]


# ---------------------------------------------------------------------------
# F-36 migration verification: existing records load post-migration
# ---------------------------------------------------------------------------


class TestMigratedRecordsLoad:
    """The 3 RLHF records migrated 2026-05-03 load + validate cleanly."""

    DATASET_DIR = Path(__file__).resolve().parents[3] / "artifacts" / "image_gen_dataset" / "2026-04"
    EXPECTED_RECORDS = (
        "sel_20260423_060227_26e6.json",
        "sel_20260423_060234_835d.json",
        "sel_20260423_060242_6e86.json",
    )

    def test_records_directory_exists(self):
        assert self.DATASET_DIR.is_dir(), (
            f"Expected RLHF dataset directory at {self.DATASET_DIR}; "
            "F-36 migration should not have moved or deleted it"
        )

    def test_each_record_loads_with_vault_relative_path(self):
        for filename in self.EXPECTED_RECORDS:
            record_path = self.DATASET_DIR / filename
            if not record_path.is_file():
                pytest.skip(f"{filename} not present in this checkout")
            with open(record_path) as f:
                data = json.load(f)
            for idx, variant in enumerate(data.get("variants", [])):
                image_path = variant.get("image_path", "")
                assert not _is_absolute_path(image_path), (
                    f"{filename} variants[{idx}].image_path is absolute "
                    f"({image_path!r}); F-36 migration should have stripped "
                    "the /Users/herb/lattice/CanvasForge.aDNA/ prefix"
                )

    def test_each_record_passes_validator(self):
        for filename in self.EXPECTED_RECORDS:
            record_path = self.DATASET_DIR / filename
            if not record_path.is_file():
                pytest.skip(f"{filename} not present in this checkout")
            with open(record_path) as f:
                data = json.load(f)
            variants = [
                VariantInfo(
                    image_path=v["image_path"],
                    model=v.get("model", "imagen-4-ultra"),
                    cost_usd=v.get("cost_usd", 0.06),
                    seed=v.get("seed"),
                )
                for v in data["variants"]
            ]
            record = SelectionRecord(
                prompt=data["prompt"],
                register=data["register"],
                variants=variants,
                pick_index=data["pick_index"],
                pick_reason=data["pick_reason"],
                approver_id=data["approver_id"],
                selection_id=data["selection_id"],
                timestamp=data["timestamp"],
                budget_class=data.get("budget_class", "standard"),
                register_compliance_score=data.get("register_compliance_score"),
                vr_scores=data.get("vr_scores"),
            )
            errors = validate_selection_record(record)
            assert errors == [], (
                f"{filename} fails validation post-migration: {errors}"
            )
