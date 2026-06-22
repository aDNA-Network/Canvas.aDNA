"""pdf_export — PDF carrier substrate for canvas composites.

Wraps PIL's native multi-page PDF writer to emit publication-grade PDFs from
CMYK (or RGB) PIL Image composites. Substrate-neutral per ADR 001 § Substrate
Scope — print semantics are app-agnostic; this module accepts pre-built PIL
images and produces a PDF carrier, agnostic to whether the composites came
from a comic page builder, presentation builder, diagram pipeline, or future
application.

Authored at M-V1-2-C-01 S1 (2026-05-28) per Pillar C charter and Stanley
"lean reuse" library election (AskUserQuestion 2026-05-28). Library choice:
PIL's built-in PDF writer over reportlab/weasyprint per ADR-010 §D1 — CMYK
fidelity via native PIL mode passthrough; zero new deps; Imagen 4 Ultra
source resolution preserved through PIL compositing.

Substrate-additive opt-in-gated discipline (Memory A
`feedback_substrate_additive_opt_in_gated_pattern.md`): this module is pure
additive. No mutation to `canvas_core/print.py` public API — the existing
JPG-emission path stays untouched. Re-baseline gate Q5 does NOT fire (CR1
LOCKED for Pillar C by charter; Wilhelm 8.80 + Issue 01 8.43 baselines
preserved verbatim).

Re-merge rationale: lattice-labs/who/coordination/coord_2026_04_16_forge_split.md
(2026-04-16 canvas-as-substrate collapse made the canvas the load-bearing
primitive; PDF export is a downstream carrier of the same primitive).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

from .print import PRINT_DPI


__all__ = [
    "PdfExporter",
    "export_composites_to_pdf",
]


@dataclass
class PdfExporter:
    """Multi-page PDF emitter from CMYK (or RGB) PIL Image composites.

    Usage:
        exporter = PdfExporter(output_path="out.pdf", dpi=300)
        exporter.add_page(composite_page_1)
        exporter.add_page(composite_page_2)
        exporter.save()

    The substrate accepts PIL images in any mode supported by PIL's PDF
    writer (CMYK and RGB are the production paths). CMYK mode passes through
    to the PDF unchanged — color-space conversion responsibility stays in
    the upstream pipeline (e.g. ``canvas_core/print.py`` ICC profile path).
    """

    output_path: str
    dpi: int = PRINT_DPI
    _pages: list[Image.Image] = field(default_factory=list, init=False, repr=False)

    def add_page(self, image: Image.Image) -> None:
        """Append a PIL image as a PDF page.

        Raises:
            TypeError: if ``image`` is not a ``PIL.Image.Image``.
            ValueError: if image has zero width or height.
        """
        if not isinstance(image, Image.Image):
            raise TypeError(
                "PdfExporter.add_page expected a PIL.Image.Image, "
                f"got {type(image).__name__}"
            )
        if image.width <= 0 or image.height <= 0:
            raise ValueError(
                "PdfExporter.add_page rejected zero-sized image: "
                f"{image.size}"
            )
        self._pages.append(image)

    def save(self) -> Path:
        """Emit multi-page PDF via PIL's native PDF writer.

        Returns:
            ``pathlib.Path`` of the emitted PDF.

        Raises:
            ValueError: if no pages have been added.
        """
        if not self._pages:
            raise ValueError("PdfExporter.save called with no pages added")

        output = Path(self.output_path)
        first, *rest = self._pages
        first.save(
            output,
            "PDF",
            resolution=float(self.dpi),
            save_all=True,
            append_images=rest,
        )
        return output

    @property
    def page_count(self) -> int:
        """Number of pages currently buffered."""
        return len(self._pages)


def export_composites_to_pdf(
    composites: list[Image.Image],
    output_path: str,
    dpi: int = PRINT_DPI,
) -> Path:
    """Convenience wrapper: render an ordered list of PIL composites as
    a multi-page PDF.

    Single-call API for the common path where the caller already has the
    full ordered list of page composites (e.g. assembled by
    ``PrintExporter._composite_page`` for each page).

    Args:
        composites: ordered list of PIL Images (CMYK or RGB).
        output_path: filesystem path for the emitted PDF.
        dpi: resolution metadata (default ``PRINT_DPI`` = 300).

    Returns:
        ``pathlib.Path`` of the emitted PDF.

    Raises:
        ValueError: if ``composites`` is empty.
    """
    if not composites:
        raise ValueError(
            "export_composites_to_pdf called with empty composites list"
        )

    exporter = PdfExporter(output_path=output_path, dpi=dpi)
    for image in composites:
        exporter.add_page(image)
    return exporter.save()
