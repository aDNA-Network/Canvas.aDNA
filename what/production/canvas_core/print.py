"""PrintExporter — print-ready export pipeline for canvas page builders.

Composites individual panel images onto full-page canvases at 300 DPI,
converts to CMYK, and exports as individual JPGs matching ComixWellspring
(CWS) saddle-stitch specifications.

Migrated from lattice-protocol/extensions/canvas/canvas_print.py (M-1-03).
Comic-specific imports (ComicPageBuilder, Page, Panel, BLEED_WIDTH,
TOTAL_PAGES) replaced with duck typing via Any + local constants per
ADR 001 — print semantics are app-agnostic substrate. The module receives
pre-built page/panel objects and accesses their attributes; it never
constructs application-specific types. Iterative hardening in Phase 5
M-5-04.
"""

from __future__ import annotations

import pickle
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from PIL import Image, ImageCms

# ---------------------------------------------------------------------------
# Comic-origin constants (local copies — substrate does not import canvas_comic)
# Original source: canvas_comic.py BLEED_WIDTH = 687.5, TOTAL_PAGES = 32
# ---------------------------------------------------------------------------

BLEED_WIDTH = 687.5
TOTAL_PAGES = 32

# ---------------------------------------------------------------------------
# Print-spec constants (300 DPI, derived from canvas units)
# ---------------------------------------------------------------------------
# canvas_comic.py uses 1" = 100 canvas units.
# px = canvas_units × 0.01 × DPI

PRINT_DPI = 300

BLEED_PX_W = 2062  # 687.5 × 0.01 × 300 = 2062.5 → round() = 2062
BLEED_PX_H = 3150  # 1050  × 0.01 × 300 = 3150

TRIM_PX_W = 1988  # 662.5 × 0.01 × 300 = 1987.5 → 1988
TRIM_PX_H = 3075  # 1025  × 0.01 × 300 = 3075

SAFE_PX_W = 1913  # 637.5 × 0.01 × 300 = 1912.5 → 1913
SAFE_PX_H = 3000  # 1000  × 0.01 × 300 = 3000

# Standard 2-col × 3-row grid cell at 300 DPI
STD_PANEL_PX_W = 941  # (637.5 - 10) / 2 × 0.01 × 300 = 941.25 → 941
STD_PANEL_PX_H = 980  # (1000 - 20) / 3 × 0.01 × 300 = 980 → 980

# --- DPI policy (declared at Halftone H6) ---
# PRINT_DPI = 300 is the TARGET: every page is composited and saved at 300 DPI,
# and the JPG carries that in its metadata. It is not a claim about the source.
#
# DPI_WARNING_THRESHOLD = 200 is the FLOOR below which a panel's source image is
# too small for its printed size. "Effective DPI" is measured per panel as
# source_px / target_px × 300 — i.e. what the source actually resolves to once
# scaled into its placement, not what the file says.
#
# The policy is WARN, NEVER BLOCK, and the reason is R7: a 2048px cloud
# generation on a full-bleed page lands at ~195 effective DPI — just under the
# floor — and that is a perfectly reasonable proof page. Blocking would stop the
# pipeline on its most common legitimate output. So a below-floor panel produces
# a warning that names the panel and the number, carried on the ExportResult and
# into export_report.md, and the operator decides whether to accept it, request a
# larger generation, or route it through the ComfyUI upscale (the H4 refine
# chain's RealESRGAN slot exists for exactly this).
#
# Spreads are measured against the COMBINED two-page target (export_spread) —
# a source that clears the floor across one page can fall under it across two,
# which is precisely when the shortfall matters.
DPI_WARNING_THRESHOLD = 200

# CMYK ICC profile path on macOS
MACOS_CMYK_PROFILE = "/System/Library/ColorSync/Profiles/Generic CMYK Profile.icc"
MACOS_SRGB_PROFILE = "/System/Library/ColorSync/Profiles/sRGB Profile.icc"

# --- Colour policy (Halftone H6) ---
# Before H6 a missing ICC profile fell through to Pillow's soft
# ``img.convert("CMYK")`` inside a bare ``except: pass``. That is a
# machine-dependent approximation: the same canvas produced different bytes on
# a machine with ColorSync profiles than on one without, and NOTHING in the
# result, the report, or the logs said which you got. A print separation that
# silently changes with the host is the defect class the H4 live run punished.
# The soft fallback is now gone; the policy is declared and recorded.
CMYK_STATUS_ICC = "icc"                    # colour-managed separation, reproducible
CMYK_STATUS_RGB_FALLBACK = "rgb-fallback"  # CMYK asked for, unavailable, RGB shipped + recorded
CMYK_STATUS_OFF = "off"                    # RGB by request
CMYK_FALLBACK_POLICIES = ("error", "rgb")


class CMYKProfileUnavailable(RuntimeError):
    """CMYK was requested but no ICC profile is available to do it reproducibly."""


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------


def canvas_units_to_px(units: float, dpi: int = PRINT_DPI) -> int:
    """Convert canvas units (1" = 100) to pixels at given DPI.

    Formula: px = units × (dpi / 100)
    """
    return round(units * dpi / 100)


def effective_dpi(source_px: int, target_px: int, target_dpi: int = PRINT_DPI) -> float:
    """Calculate effective DPI given source and target pixel dimensions.

    If the source image is smaller than the target, upscaling reduces
    effective DPI below the target DPI.
    """
    if target_px <= 0:
        return 0.0
    return source_px / target_px * target_dpi


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class PanelPlacement:
    """Pixel-space placement for a panel on the print canvas."""

    panel_id: str
    x: int
    y: int
    width: int
    height: int
    source_width: int = 0
    source_height: int = 0
    effective_dpi_w: float = 0.0
    effective_dpi_h: float = 0.0
    is_bleed: bool = False
    is_spread: bool = False


@dataclass
class PageExportSpec:
    """Specification for exporting a single page."""

    page_number: int
    page_id: str
    panel_placements: list[PanelPlacement] = field(default_factory=list)
    bg_color: tuple[int, int, int] = (30, 30, 30)  # default dark
    is_ifc: bool = False
    is_ibc: bool = False
    spread_partner_page: int | None = None  # for spread splits


@dataclass
class ExportResult:
    """Result of exporting a single page."""

    page_number: int
    filename: str
    path: str
    width: int
    height: int
    file_size_bytes: int = 0
    cmyk: bool = False  # True only when a colour-managed ICC separation was written
    cmyk_status: str = CMYK_STATUS_OFF  # icc | rgb-fallback | off — what actually happened
    is_spread_half: bool = False  # this page came out of a two-page spread split (H6)
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# PrintExporter
# ---------------------------------------------------------------------------


class PrintExporter:
    """Export page-builder state to print-ready page images.

    Composites panel PNGs onto full-bleed page canvases at 300 DPI,
    converts to CMYK (optional), and saves as individual JPGs following
    CWS naming conventions.

    Duck-typed interface: ``cpb`` must expose ``.pages`` (iterable of page
    objects with ``.page_number``, ``.id``, ``.panel_ids``, ``.color_script``)
    and ``.get_panel(id)`` returning panel objects with ``.id``, ``.x``,
    ``.y``, ``.width``, ``.height``, ``.bleed``, ``.span_rows``,
    ``.span_cols``, ``.image_path``.
    """

    def __init__(
        self,
        cpb: Any,
        output_dir: str | Path,
        issue_name: str = "ScienceStanley_Issue01",
        cmyk: bool = True,
        jpeg_quality: int = 95,
        cmyk_profile: str | Path | None = None,
        srgb_profile: str | Path | None = None,
        on_missing_profile: str = "error",
    ) -> None:
        self.cpb = cpb
        self.output_dir = Path(output_dir)
        self.issue_name = issue_name
        self.cmyk = cmyk
        self.jpeg_quality = jpeg_quality
        self.cmyk_profile = Path(cmyk_profile or MACOS_CMYK_PROFILE)
        self.srgb_profile = Path(srgb_profile or MACOS_SRGB_PROFILE)
        if on_missing_profile not in CMYK_FALLBACK_POLICIES:
            raise ValueError(
                f"on_missing_profile must be one of {CMYK_FALLBACK_POLICIES}, "
                f"got {on_missing_profile!r}"
            )
        self.on_missing_profile = on_missing_profile
        self._results: list[ExportResult] = []
        # Resolved ONCE, at construction — a colour policy that can only fail
        # after compositing 32 pages is not a policy (H6). Raises here if the
        # profiles are unavailable under the "error" policy.
        self.cmyk_status, self._cmyk_transform = self._resolve_cmyk()

    # --- Colour policy (Halftone H6) ---

    def _resolve_cmyk(self) -> tuple[str, Any]:
        """Decide the colour path up front and name it. Never machine-dependent.

        Returns ``(status, transform)`` where status is one of
        ``CMYK_STATUS_*``. Under ``on_missing_profile="error"`` an unavailable
        ICC profile raises rather than silently degrading.
        """
        if not self.cmyk:
            return CMYK_STATUS_OFF, None

        missing = [str(p) for p in (self.srgb_profile, self.cmyk_profile) if not p.exists()]
        reason: str | None = None
        transform = None

        if missing:
            reason = "ICC profile(s) not found: " + ", ".join(missing)
        else:
            try:
                transform = ImageCms.buildTransform(
                    ImageCms.getOpenProfile(str(self.srgb_profile)),
                    ImageCms.getOpenProfile(str(self.cmyk_profile)),
                    "RGB",
                    "CMYK",
                    renderingIntent=ImageCms.Intent.RELATIVE_COLORIMETRIC,
                )
            except Exception as exc:  # noqa: BLE001 - any ICC failure is the same decision
                reason = f"ICC transform could not be built: {exc}"

        if reason is None:
            return CMYK_STATUS_ICC, transform

        if self.on_missing_profile == "error":
            raise CMYKProfileUnavailable(
                f"{reason}. CMYK was requested but cannot be produced reproducibly on this "
                f"machine. Pass on_missing_profile='rgb' to export RGB with a recorded "
                f"warning instead, or cmyk=False if RGB is what you want. "
                f"(Pillow's soft convert('CMYK') is NOT used: it is a machine-dependent "
                f"approximation that would ship as if it were a colour-managed separation.)"
            )
        self._cmyk_fallback_reason = reason
        return CMYK_STATUS_RGB_FALLBACK, None

    @classmethod
    def from_pickle(
        cls,
        pkl_path: str | Path,
        output_dir: str | Path,
        issue_name: str = "ScienceStanley_Issue01",
        cmyk: bool = True,
    ) -> PrintExporter:
        """Create a PrintExporter from a pickled page-builder state."""
        with open(pkl_path, "rb") as f:
            cpb = pickle.load(f)  # noqa: S301
        return cls(cpb, output_dir, issue_name, cmyk)

    # --- Public API ---

    def build_page_specs(self) -> list[PageExportSpec]:
        """Build export specifications for all pages in order."""
        specs = []
        pages = self.cpb.pages

        for page in pages:
            spec = PageExportSpec(
                page_number=page.page_number,
                page_id=page.id,
                bg_color=self._get_bg_color(page),
                is_ifc=(page.page_number == 2),
                is_ibc=(page.page_number == TOTAL_PAGES - 1),
            )

            for panel_id in page.panel_ids:
                panel = self.cpb.get_panel(panel_id)
                if panel:
                    placement = self._compute_panel_placement(panel)
                    spec.panel_placements.append(placement)

            specs.append(spec)
        return specs

    def export_page(self, spec: PageExportSpec) -> ExportResult:
        """Export a single page to a print-ready JPG."""
        img = self._composite_page(spec)

        if self.cmyk_status == CMYK_STATUS_ICC:
            img = self._convert_to_cmyk(img)

        self.output_dir.mkdir(parents=True, exist_ok=True)
        filename = self._format_filename(spec.page_number)
        path = self.output_dir / filename

        img.save(str(path), "JPEG", quality=self.jpeg_quality, dpi=(PRINT_DPI, PRINT_DPI))

        warnings = self._colour_warnings()
        for placement in spec.panel_placements:
            min_eff_dpi = min(placement.effective_dpi_w, placement.effective_dpi_h)
            if min_eff_dpi > 0 and min_eff_dpi < DPI_WARNING_THRESHOLD:
                warnings.append(
                    f"Panel {placement.panel_id[:8]}: effective DPI "
                    f"{min_eff_dpi:.0f} < {DPI_WARNING_THRESHOLD}"
                )

        result = ExportResult(
            page_number=spec.page_number,
            filename=filename,
            path=str(path),
            width=img.size[0],
            height=img.size[1],
            file_size_bytes=path.stat().st_size if path.exists() else 0,
            # Reports what the file IS, not what was asked for.
            cmyk=(self.cmyk_status == CMYK_STATUS_ICC),
            cmyk_status=self.cmyk_status,
            warnings=warnings,
        )
        self._results.append(result)
        return result

    def export_spread(
        self,
        left_page: PageExportSpec,
        right_page: PageExportSpec,
        spread_panel: Any,
    ) -> list[ExportResult]:
        """Export a two-page spread as two separate page files.

        Loads the spread image, upscales to combined target, splits at
        center, and saves each half as a separate page file.
        """
        results = []

        if not spread_panel.image_path:
            # No image — export blank pages
            results.append(self.export_page(left_page))
            results.append(self.export_page(right_page))
            return results

        spread_img = self._load_panel_image(spread_panel)
        if spread_img is None:
            results.append(self.export_page(left_page))
            results.append(self.export_page(right_page))
            return results

        # Target: two bleed pages side by side
        target_w = BLEED_PX_W * 2
        target_h = BLEED_PX_H

        spread_img_source_size = spread_img.size  # before fit — the real resolution
        spread_img = self._fit_image(spread_img, target_w, target_h)

        # Split at center
        left_img = spread_img.crop((0, 0, BLEED_PX_W, BLEED_PX_H))
        right_img = spread_img.crop((BLEED_PX_W, 0, target_w, BLEED_PX_H))

        # Effective DPI is measured on the SOURCE image against the combined
        # two-page target — a spread that is fine at one page's width can be
        # under-resolved across two, and that is exactly when it matters.
        src_w, src_h = spread_img_source_size
        spread_warnings = list(self._colour_warnings())
        eff_dpi = min(
            effective_dpi(src_w, target_w, PRINT_DPI),
            effective_dpi(src_h, target_h, PRINT_DPI),
        )
        if 0 < eff_dpi < DPI_WARNING_THRESHOLD:
            spread_warnings.append(
                f"Spread {spread_panel.id[:8]}: effective DPI {eff_dpi:.0f} < "
                f"{DPI_WARNING_THRESHOLD} across the combined {target_w}×{target_h} spread"
            )

        for page_spec, page_img in [(left_page, left_img), (right_page, right_img)]:
            if self.cmyk_status == CMYK_STATUS_ICC:
                page_img = self._convert_to_cmyk(page_img)

            self.output_dir.mkdir(parents=True, exist_ok=True)
            filename = self._format_filename(page_spec.page_number)
            path = self.output_dir / filename
            page_img.save(str(path), "JPEG", quality=self.jpeg_quality, dpi=(PRINT_DPI, PRINT_DPI))

            result = ExportResult(
                page_number=page_spec.page_number,
                filename=filename,
                path=str(path),
                width=page_img.size[0],
                height=page_img.size[1],
                file_size_bytes=path.stat().st_size if path.exists() else 0,
                cmyk=(self.cmyk_status == CMYK_STATUS_ICC),
                cmyk_status=self.cmyk_status,
                is_spread_half=True,
                warnings=list(spread_warnings),
            )
            self._results.append(result)
            results.append(result)

        return results

    def _spread_panel_for(self, spec: PageExportSpec) -> Any | None:
        """The spread panel on ``spec``, if any (placement marked ``is_spread``)."""
        for placement in spec.panel_placements:
            if placement.is_spread:
                return self.cpb.get_panel(placement.panel_id)
        return None

    def export_all(self) -> list[ExportResult]:
        """Export all pages. Returns list of ExportResults.

        Spread-aware since Halftone H6: a page carrying a two-page spread panel
        is exported together with its right-hand partner through
        ``export_spread`` (load once → fit to the combined target → split at
        centre), consuming both specs. Before H6 this loop only ever called
        ``export_page``, so ``export_spread`` was written, correct, and
        **unreachable** — every spread silently exported as two independent
        pages, each fitting the full spread image into one page's width.
        """
        self._results = []
        specs = self.build_page_specs()

        i = 0
        while i < len(specs):
            spec = specs[i]
            spread_panel = self._spread_panel_for(spec)
            if spread_panel is not None and i + 1 < len(specs):
                self.export_spread(spec, specs[i + 1], spread_panel)
                i += 2
                continue
            if spread_panel is not None:
                # A spread with no right-hand page to land on: export the left
                # half rather than dropping it, and say so.
                result = self.export_page(spec)
                result.warnings.append(
                    f"Panel {spread_panel.id[:8]} is a two-page spread but page "
                    f"{spec.page_number} has no following page — exported as a single page"
                )
            else:
                self.export_page(spec)
            i += 1

        self._write_export_report()
        return list(self._results)

    # --- Internal compositing ---

    def _composite_page(self, spec: PageExportSpec) -> Image.Image:
        """Composite all panels onto a bleed-sized canvas."""
        bg = spec.bg_color
        canvas = Image.new("RGB", (BLEED_PX_W, BLEED_PX_H), bg)

        for placement in spec.panel_placements:
            # Find the panel to get image_path
            panel = self.cpb.get_panel(placement.panel_id)
            if not panel or not panel.image_path:
                continue

            panel_img = self._load_panel_image(panel)
            if panel_img is None:
                continue

            # Fit to target dimensions
            fitted = self._fit_image(panel_img, placement.width, placement.height)

            # Update effective DPI
            placement.source_width = panel_img.size[0]
            placement.source_height = panel_img.size[1]
            placement.effective_dpi_w = effective_dpi(panel_img.size[0], placement.width)
            placement.effective_dpi_h = effective_dpi(panel_img.size[1], placement.height)

            # Paste onto canvas
            canvas.paste(fitted, (placement.x, placement.y))

        return canvas

    def _load_panel_image(self, panel: Any) -> Image.Image | None:
        """Load a panel image from its image_path."""
        if not panel.image_path:
            return None
        path = Path(panel.image_path)
        if not path.exists():
            return None
        try:
            return Image.open(path).convert("RGB")
        except Exception:
            return None

    @staticmethod
    def _fit_image(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
        """Scale-to-fill and center-crop to exact target dimensions.

        Uses LANCZOS resampling for high-quality scaling.
        """
        if target_w <= 0 or target_h <= 0:
            return img

        src_w, src_h = img.size
        # Scale factor to fill (cover) the target
        scale = max(target_w / src_w, target_h / src_h)
        new_w = round(src_w * scale)
        new_h = round(src_h * scale)

        if new_w != src_w or new_h != src_h:
            img = img.resize((new_w, new_h), Image.LANCZOS)

        # Center crop
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        return img.crop((left, top, left + target_w, top + target_h))

    def _convert_to_cmyk(self, img: Image.Image) -> Image.Image:
        """Apply the ICC transform resolved at construction.

        There is deliberately **no soft fallback**: if we reach here without a
        transform the policy already decided to ship RGB (and recorded why), so
        the image passes through unchanged rather than being silently
        approximated. See the colour-policy note at the module constants.
        """
        if self._cmyk_transform is None:
            return img
        if img.mode == "CMYK":
            return img
        if img.mode != "RGB":
            img = img.convert("RGB")
        return ImageCms.applyTransform(img, self._cmyk_transform)

    def _colour_warnings(self) -> list[str]:
        """Per-page warning naming a degraded colour path, so it reaches the report."""
        if self.cmyk_status != CMYK_STATUS_RGB_FALLBACK:
            return []
        reason = getattr(self, "_cmyk_fallback_reason", "ICC profiles unavailable")
        return [f"CMYK requested but exported RGB — {reason}"]

    def _compute_panel_placement(self, panel: Any) -> PanelPlacement:
        """Convert canvas-unit panel coordinates to pixel placement."""
        is_bleed = panel.bleed and panel.span_rows >= 3 and panel.span_cols >= 2
        # Check if this is a spread panel (width > single bleed page)
        is_spread = panel.width > BLEED_WIDTH * 1.5

        if is_bleed and not is_spread:
            # Full-bleed single page
            return PanelPlacement(
                panel_id=panel.id,
                x=0,
                y=0,
                width=BLEED_PX_W,
                height=BLEED_PX_H,
                is_bleed=True,
            )

        if is_spread:
            # Spread panel — handled separately by export_spread
            return PanelPlacement(
                panel_id=panel.id,
                x=0,
                y=0,
                width=BLEED_PX_W * 2,
                height=BLEED_PX_H,
                is_bleed=True,
                is_spread=True,
            )

        # Standard panel — convert coordinates
        return PanelPlacement(
            panel_id=panel.id,
            x=canvas_units_to_px(panel.x),
            y=canvas_units_to_px(panel.y),
            width=canvas_units_to_px(panel.width),
            height=canvas_units_to_px(panel.height),
        )

    @staticmethod
    def _get_bg_color(page: Any) -> tuple[int, int, int]:
        """Get background color from spread color script dominant hex."""
        if page.color_script and page.color_script.dominant:
            hex_color = page.color_script.dominant.lstrip("#")
            try:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                return (r, g, b)
            except (ValueError, IndexError):
                pass
        return (30, 30, 30)

    @staticmethod
    def _is_spine_left(page_number: int) -> bool:
        """Determine if a page is on the spine-left side (odd pages).

        For saddle stitch, there is no spine offset, but this is useful
        for identifying recto (right/odd) vs verso (left/even) pages.
        """
        return page_number % 2 == 1

    def _format_filename(self, page_number: int) -> str:
        """Format output filename per CWS naming convention."""
        return f"{self.issue_name}_{page_number:02d}.jpg"

    def _write_export_report(self) -> None:
        """Write a summary report of the export run."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        report_path = self.output_dir / "export_report.md"

        colour_line = {
            CMYK_STATUS_ICC: f"**colour-managed CMYK** via ICC (`{self.cmyk_profile.name}`)",
            CMYK_STATUS_RGB_FALLBACK: (
                "⚠️ **RGB — CMYK was requested and could not be produced**: "
                + getattr(self, "_cmyk_fallback_reason", "ICC profiles unavailable")
            ),
            CMYK_STATUS_OFF: "RGB (by request)",
        }[self.cmyk_status]

        spread_halves = sum(1 for r in self._results if r.is_spread_half)

        lines = ["# Print Export Report\n\n"]
        lines.append(f"**Issue**: {self.issue_name}\n")
        lines.append(f"**Pages exported**: {len(self._results)}\n")
        lines.append(f"**Colour**: {colour_line}\n")
        lines.append(f"**Target DPI**: {PRINT_DPI} "
                     f"(warning below {DPI_WARNING_THRESHOLD} effective)\n")
        if spread_halves:
            lines.append(f"**Spread halves**: {spread_halves} "
                         f"(exported via split, not as independent pages)\n")
        lines.append("\n")

        lines.append("## Pages\n\n")
        lines.append("| Page | File | Size (px) | File Size | Colour | Spread | Warnings |\n")
        lines.append("|------|------|-----------|-----------|--------|--------|----------|\n")

        total_warnings = 0
        for r in self._results:
            size_mb = r.file_size_bytes / (1024 * 1024) if r.file_size_bytes else 0
            warn_str = "; ".join(r.warnings) if r.warnings else "—"
            total_warnings += len(r.warnings)
            lines.append(
                f"| {r.page_number} | {r.filename} | {r.width}×{r.height} "
                f"| {size_mb:.1f} MB | {r.cmyk_status} | {'half' if r.is_spread_half else '—'} "
                f"| {warn_str} |\n"
            )

        lines.append(f"\n**Total warnings**: {total_warnings}\n")

        report_path.write_text("".join(lines))

    @property
    def results(self) -> list[ExportResult]:
        """Read-only list of export results."""
        return list(self._results)
