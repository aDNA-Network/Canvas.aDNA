"""Multi-voice review orchestrator — substrate-level 5-voice III review.

Defines the canonical 5 reviewer voices per ADR 000 and orchestrates
multi-perspective qualitative review of canvas artifacts. Consumer wrappers
overlay additional voices (SS: 4-voice comic roster; CC: Community Consent
Critic) via the ReviewerConfig overlay pattern.

Productionization wire-up (M-V1-06 S3 2026-05-06): the substrate now exposes
``run_multi_voice_review()`` as the top-level orchestration entry-point, plus
``FakeVisionClient`` for paperwork-runnable runs/tests and
``derive_vr_scores_from_report()`` for SelectionRecord aggregation. Per
M-V1-06 Stanley plan-mode election Q1 2026-05-06, the wire-up lives in this
file only; agent_critique.py integration is deferred.

Migrated: N/A (new in M-5-02; productionized at M-V1-06 S3)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class ReviewerVoice:
    """A single reviewer perspective in the multi-voice review."""

    voice_id: str
    name: str
    focus: str
    prompt_template: str = ""
    is_overlay: bool = False  # True for consumer-specific voices


@dataclass
class ReviewFinding:
    """A qualitative finding from one reviewer voice."""

    voice_id: str
    severity: str  # "observation" | "concern" | "blocker"
    finding: str
    node_ids: list[str] = field(default_factory=list)
    recommendation: str = ""


@dataclass
class MultiVoiceReport:
    """Aggregated report from all reviewer voices."""

    findings: list[ReviewFinding] = field(default_factory=list)
    voices_invoked: list[str] = field(default_factory=list)
    blockers: int = 0
    concerns: int = 0
    observations: int = 0

    def add(self, finding: ReviewFinding) -> None:
        self.findings.append(finding)
        if finding.severity == "blocker":
            self.blockers += 1
        elif finding.severity == "concern":
            self.concerns += 1
        else:
            self.observations += 1

    @property
    def has_blockers(self) -> bool:
        return self.blockers > 0


# ---------------------------------------------------------------------------
# Canonical 5 reviewer voices (substrate)
# ---------------------------------------------------------------------------

CANONICAL_VOICES: list[ReviewerVoice] = [
    ReviewerVoice(
        voice_id="visual_quality",
        name="Visual Quality Critic",
        focus="Layout, spacing, typography, color coherence, whitespace balance",
    ),
    ReviewerVoice(
        voice_id="narrative_coherence",
        name="Narrative Coherence",
        focus="Story arc, information flow, slide/page sequencing, audience journey",
    ),
    ReviewerVoice(
        voice_id="accessibility",
        name="Accessibility",
        focus="WCAG contrast, alt text, heading hierarchy, text density, colorblind safety",
    ),
    ReviewerVoice(
        voice_id="character_consistency",
        name="Character Consistency",
        focus="Visual identity preservation across panels/slides, style lock, pose anchors",
    ),
    ReviewerVoice(
        voice_id="compositional_balance",
        name="Compositional Balance",
        focus="Visual weight distribution, reading flow, focal points, edge usage",
    ),
]


class MultiVoiceReviewer:
    """Orchestrate multi-voice qualitative review of a canvas artifact.

    The substrate provides 5 canonical voices. Consumer wrappers can overlay
    additional voices (e.g., SS comic 4-voice roster, CC Community Consent
    Critic) via ``add_overlay_voice()``.
    """

    def __init__(self, voices: list[ReviewerVoice] | None = None) -> None:
        self.voices = list(voices or CANONICAL_VOICES)

    def add_overlay_voice(self, voice: ReviewerVoice) -> None:
        """Add a consumer-specific overlay voice."""
        voice.is_overlay = True
        self.voices.append(voice)

    def voice_ids(self) -> list[str]:
        """Return list of active voice IDs."""
        return [v.voice_id for v in self.voices]

    def build_review_prompts(
        self,
        canvas_data: dict[str, Any],
        context: str = "",
        *,
        domain_noun: str = "presentation slide",
        item_label: str = "Slide",
        r11_node_ids: set[str] | None = None,
    ) -> dict[str, str]:
        """Build per-voice review prompts for a canvas artifact.

        Returns a dict mapping voice_id → prompt string. The actual
        invocation (via LLM or human) is caller-side.

        Application-context kwargs (per BV-3 substrate hardening, M-V1-06 S2):
        ``domain_noun`` (e.g. "presentation slide", "comic page") and
        ``item_label`` (e.g. "Slide", "Page") parameterize the prompt body so
        consumer applications surface their own canvas-application language.
        Defaults preserve deck-canonical wording.

        R11 honor-by-construction (Critical Rule 7; M-V1-05 uniform kwarg
        contract): when ``r11_node_ids`` is provided, the per-voice prompt
        names the gated node ids so voices can avoid critiquing Patient's
        Voice content prior to human approval. The canonical R11 gate at
        ``r11_gate.check_r11_gate`` is untouched by this prompt-time hint.
        """
        prompts: dict[str, str] = {}
        for voice in self.voices:
            prompt = (
                f"You are the {voice.name} reviewer.\n"
                f"Focus: {voice.focus}\n\n"
                f"Review the following {domain_noun} canvas and provide findings.\n"
                f"Classify each finding as: observation, concern, or blocker.\n"
                f"Reference items as '{item_label}' in your output.\n\n"
            )
            if voice.prompt_template:
                prompt += voice.prompt_template + "\n\n"
            if context:
                prompt += f"Additional context:\n{context}\n\n"
            if r11_node_ids:
                prompt += (
                    f"R11 (Patient's Voice) gated nodes — do not critique "
                    f"prior to human approval: {sorted(r11_node_ids)}\n\n"
                )
            prompt += f"Canvas data: {len(canvas_data.get('nodes', []))} nodes, "
            prompt += f"{len(canvas_data.get('edges', []))} edges."
            prompts[voice.voice_id] = prompt
        return prompts


# ---------------------------------------------------------------------------
# Productionization wire-up (M-V1-06 S3)
# ---------------------------------------------------------------------------


class VisionClient(Protocol):
    """Duck-typed contract: any object with ``.analyze(prompt) -> list[ReviewFinding]``."""

    def analyze(self, prompt: str) -> list[ReviewFinding]: ...  # noqa: D401,E704


_VOICE_NAME_RE = re.compile(r"You are the (.+?) reviewer\.")


def _default_canned_findings(
    voices: list[ReviewerVoice],
) -> dict[str, list[ReviewFinding]]:
    """Default canned findings: 1 observation per voice (paperwork-runnable)."""
    return {
        v.voice_id: [
            ReviewFinding(
                voice_id=v.voice_id,
                severity="observation",
                finding=f"[mock] {v.name} sample observation on canvas artifact",
                node_ids=[],
                recommendation=f"[mock] {v.name} default recommendation",
            )
        ]
        for v in voices
    }


class FakeVisionClient:
    """Deterministic canned vision client for paperwork-runnable runs and tests.

    Per M-V1-06 S3 Stanley plan-mode election Q2 2026-05-06: the m_h4_00
    multi-voice runner defaults to this client; live Gemini calls are gated
    behind ``--live`` (and a budget guardrail). Tests use this client to keep
    CI offline and deterministic.

    Voice routing: parses ``"You are the {voice.name} reviewer."`` from the
    prompt prefix and returns the canned findings for the matched voice. A
    parse failure raises ``ValueError`` rather than silently returning empty
    (R1 fail-loudly mitigation).
    """

    def __init__(
        self,
        canned: dict[str, list[ReviewFinding]] | None = None,
        voices: list[ReviewerVoice] | None = None,
    ) -> None:
        self.voices = list(voices or CANONICAL_VOICES)
        self.canned = (
            canned if canned is not None else _default_canned_findings(self.voices)
        )
        self._name_to_id = {v.name: v.voice_id for v in self.voices}

    def analyze(self, prompt: str) -> list[ReviewFinding]:
        match = _VOICE_NAME_RE.search(prompt)
        if not match:
            raise ValueError(
                f"FakeVisionClient: cannot parse voice name from prompt prefix; "
                f"got: {prompt[:80]!r}"
            )
        voice_name = match.group(1).strip()
        voice_id = self._name_to_id.get(voice_name)
        if voice_id is None:
            raise ValueError(
                f"FakeVisionClient: unknown voice name {voice_name!r} "
                f"(registered: {sorted(self._name_to_id)})"
            )
        return list(self.canned.get(voice_id, []))


def run_multi_voice_review(
    canvas_data: dict[str, Any],
    vision_client: VisionClient,
    *,
    voices: list[ReviewerVoice] | None = None,
    r11_node_ids: set[str] | None = None,
    domain_noun: str = "presentation slide",
    item_label: str = "Slide",
    context: str = "",
) -> MultiVoiceReport:
    """Drive a canvas through all configured voices via the vision client.

    Top-level orchestration entry-point added at M-V1-06 S3. Returns a
    ``MultiVoiceReport`` aggregating per-voice findings + severity counters.

    The ``vision_client`` is duck-typed (``.analyze(prompt) -> list[ReviewFinding]``);
    pass ``FakeVisionClient()`` for paperwork-runnable smoke runs or a real
    Gemini client for live evidence. ``r11_node_ids`` is threaded into the
    per-voice prompts via the M-V1-05 uniform kwarg contract; ``domain_noun``
    and ``item_label`` follow the BV-3 application-pluggable convention from
    ``visual_review.generate_review_prompt`` (M-V1-06 S2).
    """
    reviewer = MultiVoiceReviewer(voices=voices)
    prompts = reviewer.build_review_prompts(
        canvas_data,
        context=context,
        domain_noun=domain_noun,
        item_label=item_label,
        r11_node_ids=r11_node_ids,
    )
    report = MultiVoiceReport()
    for voice_id, prompt in prompts.items():
        findings = vision_client.analyze(prompt)
        for finding in findings:
            report.add(finding)
        report.voices_invoked.append(voice_id)
    return report


# Severity → vr_score mapping for SelectionRecord aggregation. Voices with no
# findings score 9.0 (clean review). Mirrors VR1-VR5 0-10 scale convention.
DEFAULT_SEVERITY_TO_SCORE: dict[str, float] = {
    "observation": 8.0,
    "concern": 6.0,
    "blocker": 4.0,
}


def derive_vr_scores_from_report(
    report: MultiVoiceReport,
    *,
    severity_to_score: dict[str, float] | None = None,
    no_findings_score: float = 9.0,
) -> dict[str, float]:
    """Derive per-voice scalar scores from a MultiVoiceReport.

    Aggregation rule: minimum severity-mapped score across each voice's
    findings (worst issue dominates). Voices invoked but with no findings
    score ``no_findings_score`` (default 9.0). Used by the m_h4_00 runner to
    populate ``SelectionRecord.vr_scores``.
    """
    mapping = (
        severity_to_score
        if severity_to_score is not None
        else DEFAULT_SEVERITY_TO_SCORE
    )
    by_voice: dict[str, float] = {}
    for f in report.findings:
        score = mapping.get(f.severity, 7.0)
        if f.voice_id not in by_voice or score < by_voice[f.voice_id]:
            by_voice[f.voice_id] = score
    for voice_id in report.voices_invoked:
        if voice_id not in by_voice:
            by_voice[voice_id] = no_findings_score
    return by_voice
