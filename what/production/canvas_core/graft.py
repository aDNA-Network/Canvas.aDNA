"""Auto-graft tooling — pull-style canonical → wrapper-local context propagation.

Per F-14 (informational) at how/campaigns/campaign_canvasforge_review/missions/
artifacts/r1_02_context_audit.md and § 6 cross-walk #12 of M-R6-01:

  Federated wrappers (e.g., science_stanley.aDNA/presentationforge/,
  context_commons.aDNA/presentationforge/) hold curated subsets of CanvasForge
  canonical context locally. When canonical context updates, wrappers do not
  pick up changes automatically. Auto-graft is the substrate primitive that
  closes that gap while respecting wrapper-curation authority.

Doctrine:

- Pull-style. Wrappers initiate; canonical never pushes.
- Curation-respecting. Wrapper-local divergence preserved unless wrapper
  explicitly asks for canonical replacement.
- Dry-run by default. ``GraftPolicy.REQUIRE_CONFIRMATION`` (the default)
  reports planned changes without writing. ``apply=True`` is required to
  mutate the wrapper tree, and even then a 3-way conflict aborts the write.
- Three-way merge. ``last_grafted_sha`` in the manifest pins the baseline
  the wrapper last accepted; comparing canonical / wrapper / baseline
  classifies each tracked file into ``unchanged`` / ``canonical_only_changed``
  / ``wrapper_only_changed`` / ``both_changed``. Missing baseline (first graft)
  collapses to canonical-vs-wrapper equality.

Substrate-neutral. Imports stdlib + ``yaml`` only; no per-application
coupling. Consumers pass canonical_dir + wrapper_dir + manifest path
explicitly so the library has no application-specific path knowledge.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Literal

import yaml


class GraftPolicy(str, Enum):
    """Policy for handling tracked files during a graft.

    REQUIRE_CONFIRMATION — dry-run; never writes; reports planned actions.
        The default; mirrors the F-46 paperwork-runnable precedent.
    REPLACE_CANONICAL — overwrite wrapper-local content with canonical when
        canonical changed, regardless of wrapper divergence. Aggressive.
    PRESERVE_WRAPPER_OVERRIDES — write canonical only when wrapper has not
        diverged from baseline (canonical_only_changed); preserve wrapper
        when wrapper diverged (wrapper_only_changed) or both changed
        (both_changed → reported as conflict, no write).
    """

    REQUIRE_CONFIRMATION = "require_confirmation"
    REPLACE_CANONICAL = "replace_canonical"
    PRESERVE_WRAPPER_OVERRIDES = "preserve_wrapper_overrides"


@dataclass
class GraftEntry:
    """One tracked file in a graft manifest."""

    canonical_path: str
    wrapper_path: str
    last_grafted_sha: str | None = None


@dataclass
class GraftManifest:
    """Wrapper-side declaration of canonical files to graft-track.

    YAML schema (schema_version: 1):

        schema_version: 1
        tracked_files:
          - canonical_path: relative/path/from/canonical_dir.md
            wrapper_path: relative/path/from/wrapper_dir.md
            last_grafted_sha: <sha256 hex of last accepted canonical>  # optional
    """

    schema_version: int = 1
    tracked_files: list[GraftEntry] = field(default_factory=list)

    @classmethod
    def from_yaml(cls, path: Path) -> GraftManifest:
        """Load a graft manifest from a YAML file. Raises on malformed input."""
        if not path.exists():
            raise ValueError(f"GraftManifest source not found: {path}")
        raw = yaml.safe_load(path.read_text())
        if not isinstance(raw, dict):
            raise ValueError(
                f"GraftManifest YAML must be a mapping at top level; got {type(raw).__name__}"
            )
        if "schema_version" not in raw or "tracked_files" not in raw:
            raise ValueError(
                "GraftManifest YAML missing required keys "
                "(schema_version, tracked_files)"
            )
        if not isinstance(raw["schema_version"], int):
            raise ValueError(
                f"GraftManifest schema_version must be int; got {type(raw['schema_version']).__name__}"
            )
        if not isinstance(raw["tracked_files"], list):
            raise ValueError(
                f"GraftManifest tracked_files must be a list; "
                f"got {type(raw['tracked_files']).__name__}"
            )
        entries = []
        for idx, item in enumerate(raw["tracked_files"]):
            if not isinstance(item, dict):
                raise ValueError(
                    f"GraftManifest tracked_files[{idx}] must be a mapping"
                )
            if "canonical_path" not in item or "wrapper_path" not in item:
                raise ValueError(
                    f"GraftManifest tracked_files[{idx}] missing required keys "
                    "(canonical_path, wrapper_path)"
                )
            entries.append(
                GraftEntry(
                    canonical_path=item["canonical_path"],
                    wrapper_path=item["wrapper_path"],
                    last_grafted_sha=item.get("last_grafted_sha"),
                )
            )
        return cls(schema_version=raw["schema_version"], tracked_files=entries)


@dataclass
class GraftReport:
    """Result of an auto_graft run."""

    changes_applied: list[str] = field(default_factory=list)
    changes_skipped: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    dry_run_only: bool = True


_DiffOutcome = Literal[
    "unchanged",
    "canonical_only_changed",
    "wrapper_only_changed",
    "both_changed",
]


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _diff_three_way(
    canonical_sha: str,
    wrapper_sha: str,
    baseline_sha: str | None,
) -> _DiffOutcome:
    """Classify a tracked file across canonical / wrapper / baseline by SHA.

    When baseline is missing (first graft, no last_grafted_sha), the
    classification collapses to canonical-vs-wrapper equality — divergence
    surfaces as ``canonical_only_changed`` so the wrapper sees the proposed
    update without claiming the wrapper diverged from a baseline it never
    accepted.
    """
    if baseline_sha is None:
        return "unchanged" if canonical_sha == wrapper_sha else "canonical_only_changed"
    canonical_eq_baseline = canonical_sha == baseline_sha
    wrapper_eq_baseline = wrapper_sha == baseline_sha
    if canonical_eq_baseline and wrapper_eq_baseline:
        return "unchanged"
    if not canonical_eq_baseline and wrapper_eq_baseline:
        return "canonical_only_changed"
    if canonical_eq_baseline and not wrapper_eq_baseline:
        return "wrapper_only_changed"
    return "both_changed"


def auto_graft(
    canonical_dir: Path,
    wrapper_dir: Path,
    manifest: GraftManifest,
    policy: GraftPolicy,
    apply: bool = False,
) -> GraftReport:
    """Run the auto-graft against a manifest.

    Args:
        canonical_dir: Root of the canonical context tree.
        wrapper_dir: Root of the wrapper-local context tree.
        manifest: Loaded ``GraftManifest`` declaring tracked files.
        policy: ``GraftPolicy`` member; decides handling of divergence.
        apply: If False (the default), no writes happen — the report
            describes what *would* happen. If True, writes proceed per
            policy (still subject to conflict-blocks-write).

    Returns:
        ``GraftReport`` capturing per-file disposition.

    Notes:
        - ``GraftPolicy.REQUIRE_CONFIRMATION`` always implies dry-run.
        - ``both_changed`` (3-way conflict) never writes regardless of
          ``apply``. Wrapper-side resolution required.
        - Baseline is sourced from ``last_grafted_sha`` in the manifest. If
          the wrapper file is missing, that surfaces as an error.
    """
    if not isinstance(policy, GraftPolicy):
        raise ValueError(
            f"policy must be a GraftPolicy member; got {type(policy).__name__}"
        )

    dry_run = policy == GraftPolicy.REQUIRE_CONFIRMATION or not apply
    report = GraftReport(dry_run_only=dry_run)

    for entry in manifest.tracked_files:
        canonical_file = canonical_dir / entry.canonical_path
        wrapper_file = wrapper_dir / entry.wrapper_path

        if not canonical_file.exists():
            report.errors.append(
                f"canonical missing: {entry.canonical_path}"
            )
            continue
        if not wrapper_file.exists():
            report.errors.append(
                f"wrapper missing: {entry.wrapper_path}"
            )
            continue

        canonical_text = canonical_file.read_text()
        wrapper_text = wrapper_file.read_text()
        outcome = _diff_three_way(
            _sha256(canonical_text),
            _sha256(wrapper_text),
            entry.last_grafted_sha,
        )
        label = entry.canonical_path

        if outcome == "unchanged":
            report.changes_skipped.append(f"{label}: unchanged")
            continue

        if outcome == "both_changed":
            report.conflicts.append(
                f"{label}: 3-way conflict — canonical and wrapper both diverged"
            )
            continue

        if outcome == "wrapper_only_changed":
            report.changes_skipped.append(
                f"{label}: wrapper override preserved"
            )
            continue

        # canonical_only_changed: this is the propagation case.
        if policy == GraftPolicy.REQUIRE_CONFIRMATION:
            report.changes_applied.append(
                f"{label}: would replace wrapper with canonical (dry-run)"
            )
            continue

        if not apply:
            report.changes_applied.append(
                f"{label}: would replace wrapper with canonical (apply=False)"
            )
            continue

        wrapper_file.write_text(canonical_text)
        report.changes_applied.append(
            f"{label}: replaced wrapper with canonical"
        )

    return report
