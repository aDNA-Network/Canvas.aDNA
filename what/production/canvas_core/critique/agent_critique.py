"""Agent-autonomous canvas critique orchestrator.

Glues: render → screenshot → vision-call → parse → trap-emit → md-append.
Entry point: ``run_critique(canvas_path, ...)``.

New in M-1-08 (Phase 1 — Substrate Extraction).  Pure substrate.

Budget cap resolution (F-28 amendment 2026-05-03):
    The default budget cap is ``DEFAULT_BUDGET_CAP_USD`` ($0.08). To override
    the default without editing code, set the ``CANVASFORGE_VISION_BUDGET``
    environment variable. Explicit ``budget_cap_usd=`` parameter still takes
    precedence over the env var. Order of precedence (highest first):

        1. Explicit ``budget_cap_usd=`` argument to ``run_critique()``
        2. ``CANVASFORGE_VISION_BUDGET`` environment variable (parsed as float)
        3. Module default ``DEFAULT_BUDGET_CAP_USD``

    A non-numeric env-var value logs a warning and falls back to the module
    default; the call does not fail. Per F-28 of M-CAMPAIGN-REFRESH-02.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import CritiqueFinding, CritiqueResult
from .rule_based_fallback import run_fallback
from .vision_client import (
    VisionClient,
    VisionRequest,
    get_vision_client,
    _parse_findings_json,
)
from ..spatial import bounding_box
from ..traps import TRAP_PACK_REGISTRY

_log = logging.getLogger(__name__)

# F-28 amendment 2026-05-03: budget cap default + env-var override.
DEFAULT_BUDGET_CAP_USD = 0.08
_BUDGET_ENV_VAR = "CANVASFORGE_VISION_BUDGET"


def _resolve_budget_cap_default() -> float:
    """Resolve the default budget cap, honoring the env-var override.

    Returns the parsed value of ``CANVASFORGE_VISION_BUDGET`` if set + parseable,
    otherwise ``DEFAULT_BUDGET_CAP_USD``. A non-numeric env value logs a warning
    and falls back to the module default. Per F-28 of M-CAMPAIGN-REFRESH-02.
    """
    env_value = os.environ.get(_BUDGET_ENV_VAR)
    if env_value is None:
        return DEFAULT_BUDGET_CAP_USD
    try:
        return float(env_value)
    except (TypeError, ValueError):
        _log.warning(
            "Invalid %s value %r; falling back to default $%.2f",
            _BUDGET_ENV_VAR, env_value, DEFAULT_BUDGET_CAP_USD,
        )
        return DEFAULT_BUDGET_CAP_USD


# ---------------------------------------------------------------------------
# Prompt template
# ---------------------------------------------------------------------------

_PROMPT_TEMPLATE_PATH = Path(__file__).parent / "prompts" / "cv_trap_findings.txt"


def _load_prompt_template() -> str:
    """Load the critique prompt template from asset file."""
    return _PROMPT_TEMPLATE_PATH.read_text()


def _build_trap_catalog() -> str:
    """Build a text catalog of known CV-* traps for the prompt."""
    lines = []
    for trap_id, meta in TRAP_PACK_REGISTRY.items():
        lines.append(f"- {trap_id}: {meta['description']} (severity default: {meta['severity_default']})")
    return "\n".join(lines)


def _fill_prompt(
    group_id: str,
    width: int,
    height: int,
    application: str = "canvas",
    register: str = "R1",
) -> str:
    """Fill the prompt template with group metadata."""
    template = _load_prompt_template()
    return template.format(
        group_id=group_id,
        width=width,
        height=height,
        application=application,
        register=register,
        trap_catalog=_build_trap_catalog(),
    )


# ---------------------------------------------------------------------------
# Artifact versioning
# ---------------------------------------------------------------------------


def _artifact_version(canvas_path: Path) -> str:
    """Compute a version hash for idempotency checking."""
    stat = canvas_path.stat()
    return hashlib.sha256(
        f"{canvas_path}:{stat.st_mtime}:{stat.st_size}".encode()
    ).hexdigest()[:12]


# ---------------------------------------------------------------------------
# agent_observations.md append
# ---------------------------------------------------------------------------


def _append_observations(
    artifact_dir: Path,
    findings: list[CritiqueFinding],
    vision_model: str,
    cost_usd: float,
    duration_s: float,
    artifact_version: str,
    fallback_used: bool,
) -> Path:
    """Append findings to canvas_review/agent_observations.md.

    Idempotent: does not clobber prior human notes.  Each run gets its
    own timestamped section.
    """
    review_dir = artifact_dir / "canvas_review"
    review_dir.mkdir(parents=True, exist_ok=True)
    obs_path = review_dir / "agent_observations.md"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    source_label = "rule-based fallback" if fallback_used else vision_model

    lines = [
        f"\n## Agent critique — {now}",
        f"**Artifact version**: {artifact_version}",
        f"**Vision model**: {source_label}",
        f"**Cost**: ${cost_usd:.4f}",
        f"**Duration**: {duration_s:.1f}s",
        "",
        "### Findings",
    ]

    if not findings:
        lines.append("- No issues detected.")
    else:
        for f in findings:
            node_str = ", ".join(f.node_refs) if f.node_refs else "n/a"
            lines.append(
                f"- **{f.trap_id}** ({f.severity}): {f.observation} "
                f"[nodes: {node_str}]"
            )

    lines.append("")

    with open(obs_path, "a") as fh:
        fh.write("\n".join(lines))

    return obs_path


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def run_critique(
    canvas_path: str | Path,
    *,
    vision_model: str = "gemini-2.5-flash",
    viewport_override: tuple[int, int] | None = None,
    budget_cap_usd: float | None = None,
    artifact_version_override: str | None = None,
    vision_client: VisionClient | None = None,
    skip_screenshots: bool = False,
    dry_run: bool = False,
) -> CritiqueResult:
    """Run the agent-autonomous critique pipeline.

    Args:
        canvas_path: Path to the ``.canvas`` file.
        vision_model: Vision model to use (default ``gemini-2.5-flash``).
        viewport_override: Override canvas-group declared dims.
        budget_cap_usd: Cost ceiling per invocation. If ``None`` (default),
            resolves via env var ``CANVASFORGE_VISION_BUDGET`` then falls back
            to ``DEFAULT_BUDGET_CAP_USD`` ($0.08). Explicit value overrides
            both. Per F-28 of M-CAMPAIGN-REFRESH-02.
        artifact_version_override: Override version for idempotency.
        vision_client: Pre-constructed vision client (for testing).
        skip_screenshots: If True, skip browser screenshots and run
            rule-based fallback only.  Useful when Playwright is
            unavailable.
        dry_run: If True, run the full pipeline but skip the
            ``canvas_review/agent_observations.md`` append. The returned
            :class:`CritiqueResult` carries the same findings, screenshots,
            cost, and timing as a normal run; only the on-disk side effect
            is suppressed. Per M-V1-11 (read-only audit invocation).

    Returns:
        :class:`CritiqueResult` with findings, paths, and cost.
    """
    if budget_cap_usd is None:
        budget_cap_usd = _resolve_budget_cap_default()
    t0 = time.monotonic()
    canvas_path = Path(canvas_path)

    # Load canvas data.
    with open(canvas_path) as f:
        canvas_data = json.load(f)

    nodes = canvas_data.get("nodes", [])
    groups = [n for n in nodes if n.get("type") == "group"]
    art_version = artifact_version_override or _artifact_version(canvas_path)

    result = CritiqueResult(vision_model=vision_model)

    # If no groups, run fallback directly.
    if not groups or skip_screenshots:
        _log.info("No groups or screenshots skipped; running rule-based fallback")
        result.findings = run_fallback(canvas_data)
        result.fallback_used = True
        result.duration_s = time.monotonic() - t0
        if not dry_run:
            _append_observations(
                canvas_path.parent, result.findings, vision_model,
                result.cost_usd, result.duration_s, art_version,
                fallback_used=True,
            )
        return result

    # --- Render stage ---
    # Build group viewports.
    from ..geometry import resolve_viewport

    group_viewports: dict[str, tuple[int, int]] = {}
    for grp in groups:
        gid = grp.get("id", "")
        if viewport_override:
            group_viewports[gid] = viewport_override
        else:
            group_viewports[gid] = resolve_viewport(grp)

    # --- Screenshot stage ---
    try:
        from .browser import capture_screenshots

        # Render HTML first via html_renderer.
        from ..html_renderer import render_canvas_data

        with tempfile.TemporaryDirectory(prefix="critique_") as tmpdir:
            tmp = Path(tmpdir)
            html_path = tmp / "rendered.html"

            # Render-stage exception fallback (F-31 fix at M-V1-05).
            try:
                rendered = render_canvas_data(canvas_data)
            except Exception as render_exc:
                _log.warning(
                    "Render stage failed (%s); running fallback",
                    render_exc,
                )
                result.findings = run_fallback(canvas_data)
                result.fallback_used = True
                result.duration_s = time.monotonic() - t0
                if not dry_run:
                    _append_observations(
                        canvas_path.parent, result.findings, vision_model,
                        result.cost_usd, result.duration_s, art_version,
                        fallback_used=True,
                    )
                return result

            html_path.write_text(rendered if isinstance(rendered, str) else str(rendered))
            result.rendered_html_path = html_path

            screenshot_dir = tmp / "screenshots"
            result.screenshots = capture_screenshots(
                html_path, group_viewports, screenshot_dir,
            )

            # --- Vision-call stage ---
            client = vision_client or get_vision_client(vision_model)
            all_findings: list[CritiqueFinding] = []

            for gid, png_path in result.screenshots.items():
                grp = next((g for g in groups if g.get("id") == gid), {})
                w, h = group_viewports.get(gid, (1920, 1080))

                prompt = _fill_prompt(gid, w, h)
                request = VisionRequest(
                    images=[png_path],
                    prompt=prompt,
                    group_id=gid,
                    budget_cap_usd=budget_cap_usd,
                )

                response = client.analyze(request)
                result.cost_usd += response.cost_usd

                if response.success and response.parsed_findings:
                    for fd in response.parsed_findings:
                        all_findings.append(CritiqueFinding(
                            trap_id=fd.get("trap_id", "CV-GENERAL-01"),
                            node_refs=fd.get("node_refs", []),
                            severity=fd.get("severity", "medium"),
                            observation=fd.get("observation", response.raw_text[:200]),
                            source="agent_critique",
                        ))
                elif not response.success:
                    _log.warning(
                        "Vision call failed for group %s: %s; falling back",
                        gid, response.error,
                    )
                    # Fallback for this group.
                    fb = run_fallback(canvas_data)
                    all_findings.extend(fb)
                    result.fallback_used = True

            result.findings = all_findings

    except (RuntimeError, ImportError) as exc:
        _log.warning("Screenshot capture unavailable (%s); running fallback", exc)
        result.findings = run_fallback(canvas_data)
        result.fallback_used = True

    result.duration_s = time.monotonic() - t0

    # --- Append observations ---
    if not dry_run:
        _append_observations(
            canvas_path.parent, result.findings, vision_model,
            result.cost_usd, result.duration_s, art_version,
            fallback_used=result.fallback_used,
        )

    return result
