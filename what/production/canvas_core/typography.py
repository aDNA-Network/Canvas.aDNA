"""Typography Token Contract — fine-grained typography control for canvas substrate.

NEW module landed at M-V1-2-B-01 S1 (2026-05-27) per CanvasForge v1.2 Pillar B
charter. Lifts CanvasForge from theme-suggested fonts to publication-grade
typography (tracking, kerning, line-height multipliers, optical sizing, per-element
weight variants, font-family + weight tokenization).

Design discipline (Memory A `feedback_substrate_additive_opt_in_gated_pattern.md`,
codified at Pillar F mission close 2026-05-26 after 4-session substrate-additive
default-None / opt-in-gated streak):

  • Every field on `TypographyToken` defaults to `None`.
  • `to_css_fragment(None)` returns the empty string — V1 CSS path preserved.
  • Caller opts in by passing a constructed `TypographyToken` to
    `PresentationTheme.typography_tokens` or `SlideTypeTokens.typography_tokens`;
    when the field is `None` (default), `_generate_base_css` emits no
    typography-override CSS and existing hardcoded weights / monospace
    family remain authoritative.
  • Wilhelm 8.80 + Issue 01 8.43 parity baselines (SHA `3ce4d341a727…`) are
    preserved by construction at S1; re-baseline gate Q5 fires only at S2
    when (and if) baseline themes are migrated to consume new tokens AND
    the resulting VR shift exceeds ±0.10 median.

Authority: ADR-009 (typography token contract; drafted at S1; ratified at
mission close S(N≥2 or N≥3) per Stanley CR5 sign-off).

Re-merge rationale (CR7+SO7): `lattice-labs/who/coordination/coord_2026_04_16_forge_split.md`
"""

from __future__ import annotations

from dataclasses import dataclass, fields, replace
from typing import Final

__all__ = [
    "TypographyToken",
    "merge",
    "to_css_fragment",
    "ELEMENTS",
]


# Element keys recognized by per-element override dicts (tracking_em /
# line_height_multiplier / weight_axis). Mirrors `design_tokens.LINE_HEIGHTS`
# and `LETTER_SPACING` keys plus `strong` for inline emphasis weight overrides.
ELEMENTS: Final[tuple[str, ...]] = (
    "display",
    "h1",
    "h2",
    "h3",
    "h4",
    "body",
    "caption",
    "label",
    "strong",
)


@dataclass(frozen=True)
class TypographyToken:
    """Opt-in container for fine-grained typography control.

    All fields default to `None`. An unset (`None`) field is inert and
    downstream code preserves V1 behavior verbatim. Caller opts in to a
    specific override by passing a non-`None` value.

    Compose theme-level tokens with slide-type-level tokens via `merge()`.
    """

    # Font families
    font_family_body: str | None = None
    """Overrides `theme.font_suggestion` for body / paragraph text when set."""

    font_family_heading: str | None = None
    """Independent heading family. Falls back to body family when unset."""

    font_family_code: str | None = None
    """Replaces hardcoded `JetBrains Mono, Fira Code, monospace`
    (html_renderer.py:981) for `<code>` elements when set."""

    # Per-element font weights (override hardcoded CSS weights in
    # _generate_base_css: h1=700, h2/h3/h4=600, strong=700)
    weight_h1: int | None = None
    weight_h2: int | None = None
    weight_h3: int | None = None
    weight_h4: int | None = None
    weight_body: int | None = None
    weight_strong: int | None = None

    # Tracking (letter-spacing in em). Keyed by element name; values extend /
    # override `design_tokens.LETTER_SPACING` dict semantics when set.
    tracking_em: dict[str, float] | None = None

    # Per-element line-height multipliers. Multiplies `design_tokens.LINE_HEIGHTS`
    # per element when present. E.g. {"h1": 1.05} tightens h1 line-height to
    # 1.15 × 1.05.
    line_height_multiplier: dict[str, float] | None = None

    # CSS `font-kerning` value: `normal` / `none` / `auto`.
    kerning: str | None = None

    # CSS `font-optical-sizing` value: `auto` / `none`. Activates variable-font
    # optical-sizing axis when the font supports it.
    optical_sizing: str | None = None

    # Per-element variable-font weight-axis values (when the font supports the
    # `wght` axis). Keyed by element name; values emit
    # `font-variation-settings: 'wght' <value>` when set.
    weight_axis: dict[str, int] | None = None


def merge(
    base: TypographyToken | None,
    override: TypographyToken | None,
) -> TypographyToken | None:
    """Field-wise override of `base` by `override`.

    `None` fields in `override` do NOT clobber non-`None` fields in `base`.
    Returns `None` when both inputs are `None` (V1 path preserved).

    For dict fields (`tracking_em`, `line_height_multiplier`, `weight_axis`),
    `override`'s dict (when present) fully replaces `base`'s dict; per-element
    dict-merge is the caller's responsibility (kept explicit to avoid silent
    surprise on partial dicts).

    Caller pattern: theme-level token + slide-type-level token composition.
    """
    if base is None and override is None:
        return None
    if base is None:
        return override
    if override is None:
        return base

    updates: dict[str, object] = {}
    for f in fields(TypographyToken):
        ov = getattr(override, f.name)
        if ov is not None:
            updates[f.name] = ov
    return replace(base, **updates) if updates else base


def to_css_fragment(token: TypographyToken | None) -> str:
    """Emit opt-in CSS rules for a typography token.

    Returns `""` when `token is None` so callers can unconditionally append
    the fragment to base CSS without affecting V1 output.

    Emitted rules use CSS selectors that match the existing `_generate_base_css`
    selectors (`body`, `h1`-`h4`, `code`, `strong`). Order matters: the
    fragment is appended AFTER the base CSS so the cascade ensures overrides
    win over hardcoded V1 rules when set.
    """
    if token is None:
        return ""

    parts: list[str] = ["\n/* Typography token overrides (ADR-009) */"]

    # Body-level: font-family-body + kerning + optical-sizing + body weight
    body_decls: list[str] = []
    if token.font_family_body is not None:
        body_decls.append(f"font-family: {token.font_family_body};")
    if token.kerning is not None:
        body_decls.append(f"font-kerning: {token.kerning};")
    if token.optical_sizing is not None:
        body_decls.append(f"font-optical-sizing: {token.optical_sizing};")
    if token.weight_body is not None:
        body_decls.append(f"font-weight: {token.weight_body};")
    if (
        token.line_height_multiplier is not None
        and "body" in token.line_height_multiplier
    ):
        body_decls.append(
            f"line-height: calc(var(--cl-lh-body) * {token.line_height_multiplier['body']});"
        )
    if token.tracking_em is not None and "body" in token.tracking_em:
        body_decls.append(f"letter-spacing: {token.tracking_em['body']}em;")
    if token.weight_axis is not None and "body" in token.weight_axis:
        body_decls.append(
            f"font-variation-settings: 'wght' {token.weight_axis['body']};"
        )
    if body_decls:
        parts.append("body { " + " ".join(body_decls) + " }")

    # Heading family (h1-h4); independent override for headings.
    if token.font_family_heading is not None:
        parts.append(
            f"h1, h2, h3, h4 {{ font-family: {token.font_family_heading}; }}"
        )

    # Per-element heading overrides (weight + tracking + line-height + weight-axis)
    weight_by_element: dict[str, int | None] = {
        "h1": token.weight_h1,
        "h2": token.weight_h2,
        "h3": token.weight_h3,
        "h4": token.weight_h4,
    }
    for element in ("h1", "h2", "h3", "h4"):
        decls: list[str] = []
        wt = weight_by_element[element]
        if wt is not None:
            decls.append(f"font-weight: {wt};")
        if (
            token.line_height_multiplier is not None
            and element in token.line_height_multiplier
        ):
            decls.append(
                f"line-height: calc(var(--cl-lh-{element}) * "
                f"{token.line_height_multiplier[element]});"
            )
        if token.tracking_em is not None and element in token.tracking_em:
            decls.append(f"letter-spacing: {token.tracking_em[element]}em;")
        if token.weight_axis is not None and element in token.weight_axis:
            decls.append(
                f"font-variation-settings: 'wght' {token.weight_axis[element]};"
            )
        if decls:
            parts.append(f"{element} {{ " + " ".join(decls) + " }")

    # Code family
    if token.font_family_code is not None:
        parts.append(f"code {{ font-family: {token.font_family_code}; }}")

    # Strong weight
    if token.weight_strong is not None:
        parts.append(f"strong {{ font-weight: {token.weight_strong}; }}")

    # Caption / label per-element (tracking + line-height); no weight surface
    # because base CSS doesn't define them as separate selectors (they are
    # body-class variants in templates).
    for element in ("caption", "label"):
        decls = []
        if (
            token.line_height_multiplier is not None
            and element in token.line_height_multiplier
        ):
            decls.append(
                f"line-height: calc(var(--cl-lh-{element}) * "
                f"{token.line_height_multiplier[element]});"
            )
        if token.tracking_em is not None and element in token.tracking_em:
            decls.append(f"letter-spacing: {token.tracking_em[element]}em;")
        if decls:
            parts.append(f".{element} {{ " + " ".join(decls) + " }")

    # Trailing newline so concatenation onto base CSS stays clean.
    return "\n".join(parts) + "\n" if len(parts) > 1 else ""
