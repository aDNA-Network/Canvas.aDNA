"""canvas_core — substrate package for CanvasForge.

Surface re-exports of key substrate symbols so consumers can import from
the package root: ``from canvas_core import CanvasBuilder, VALID_ROLES, ...``

Populated in Phase 1 (M-1-01 session 2, O6) per ADR 001 § Directory Shape.
Additional symbols will be added as subsequent Phase 1 missions populate
remaining skeleton modules (geometry, spatial, mermaid, print, etc.).
"""

# --- Core canvas builder ---
from .core import CanvasBuilder

# --- Substrate configuration ---
from .config_substrate import VALID_ROLES, ImageFormat, PendingImage

# --- Design tokens ---
from .design_tokens import (
    LETTER_SPACING,
    LINE_HEIGHTS,
    SPACING_TOKENS,
    TYPE_SIZES,
    export_css_custom_properties,
    get_slide_tokens,
)

# --- Scoring substrate ---
from .scoring import (
    CategoryScore,
    CriterionScore,
    PresentationReport,
    _GRADE_THRESHOLDS,
    _score_to_grade,
)

# --- Visual review (VR1-VR5) ---
from .visual_review import (
    VISUAL_CRITERIA,
    CanvasVisualScore,
    SlideVisualScore,  # legacy class-name alias; field renames node_* landed at M-V1-06 S2
    VisualCriterionScore,
    VisualReviewReport,
    estimate_visual_scores,
    generate_review_prompt,
    parse_visual_review_response,
)

# --- R11 Patient's Voice gate ---
from .r11_gate import R11GateConfig, R11GateResult, check_r11_gate

# --- HTML renderer ---
from .html_renderer import (
    RenderedPresentation,
    SlideHTML,
    extract_slides,
    render_canvas_data,
    render_presentation,
    render_slide_html,
)

# --- Geometry (golden-ratio math) ---
from .geometry import (
    PHI,
    _DEFAULT_VIEWPORT,
    fibonacci_spacing,
    golden_rect,
    golden_split,
    resolve_viewport,
    thirds_points,
)

# --- Spatial analysis ---
from .spatial import (
    alignment_score,
    bounding_box,
    containment_check,
    detect_overlaps,
    overlaps,
    spacing_analysis,
    structural_summary,
)

# --- CSS fixes ---
from .css_fixes import CSSFix, apply_fixes, get_fixes_for, register_fix

# --- Vault paths ---
from .paths import find_repo_root, find_vault_root

# --- Image generation (Protocol + wiring) ---
from .image_generation import (
    ImageClient,
    ImageRequest,
    ImagenWiring,
    VariantSet,
)

# --- ComfyForge Tier 1 adapter (M-3-05 / ADR 003) ---
from .comfyforge_adapter import ComfyForgeConfig, ComfyForgeTier1Adapter

# --- Style mapping (M-3-05 / ADR 003) ---
from .style_mapping import load_style_config, resolve_style

# --- Mermaid diagram generation ---
from .mermaid import MermaidEdge, MermaidGenerator, MermaidNode

# --- Print export (CMYK/300 DPI) ---
from .print import (
    ExportResult,
    PageExportSpec,
    PanelPlacement,
    PrintExporter,
    canvas_units_to_px,
    effective_dpi,
)

# --- PDF export (Pillar C / ADR-010; substrate-additive carrier; M-V1-2-C-01) ---
from .pdf_export import (
    PdfExporter,
    export_composites_to_pdf,
)

# --- Google Doc export (Pillar D / ADR-011; substrate-additive carrier; M-V1-2-D-01) ---
from .gdoc_export import (
    BulletList,
    DocElement,
    GdocApiError,
    GdocAuthError,
    GdocExporter,
    Heading,
    InlineImage,
    Paragraph,
    export_canvas_to_gdoc,
)

# --- Visual inspector (orchestration) ---
from .visual_inspector import (
    ScreenshotBatch,
    ScreenshotResult,
    build_automated_report,
    build_review_report,
    compare_reviews,
    prepare_screenshots,
    save_review_report,
    visual_inspect,
)

# --- Text metrics ---
from .text_metrics import measure_text_extent

# --- III Trap Pack ---
from .traps import TrapFinding, TRAP_PACK_REGISTRY
from .traps.runner import run_all_traps

# --- RLHF variant selection (M-5-07 / ADR 003 D4) ---
from .rlhf import (
    SelectionRecord,
    validate_selection_record,
    write_selection,
    append_audit_log,
)

# --- Multi-voice review ---
from .multi_voice import (
    CANONICAL_VOICES,
    MultiVoiceReport,
    MultiVoiceReviewer,
    ReviewerVoice,
    ReviewFinding,
)

# --- Agent critique pipeline ---
from .critique import CritiqueFinding, CritiqueResult, run_critique

# --- Canvas opener (Obsidian control) ---
from .open import CanvasOpener

__all__ = [
    # Core
    "CanvasBuilder",
    # Config
    "VALID_ROLES",
    "ImageFormat",
    "PendingImage",
    # Design tokens
    "TYPE_SIZES",
    "SPACING_TOKENS",
    "LINE_HEIGHTS",
    "LETTER_SPACING",
    "export_css_custom_properties",
    "get_slide_tokens",
    # Scoring
    "CriterionScore",
    "CategoryScore",
    "PresentationReport",
    "_GRADE_THRESHOLDS",
    "_score_to_grade",
    # Visual review
    "VISUAL_CRITERIA",
    "VisualCriterionScore",
    "CanvasVisualScore",
    "SlideVisualScore",  # legacy alias for CanvasVisualScore
    "VisualReviewReport",
    "estimate_visual_scores",
    "generate_review_prompt",
    "parse_visual_review_response",
    # R11
    "R11GateResult",
    "R11GateConfig",
    "check_r11_gate",
    # Renderer
    "SlideHTML",
    "RenderedPresentation",
    "extract_slides",
    "render_slide_html",
    "render_presentation",
    "render_canvas_data",
    # Geometry
    "PHI",
    "_DEFAULT_VIEWPORT",
    "resolve_viewport",
    "golden_split",
    "golden_rect",
    "thirds_points",
    "fibonacci_spacing",
    # Spatial
    "bounding_box",
    "overlaps",
    "detect_overlaps",
    "alignment_score",
    "containment_check",
    "spacing_analysis",
    "structural_summary",
    # CSS
    "CSSFix",
    "register_fix",
    "get_fixes_for",
    "apply_fixes",
    # Paths
    "find_vault_root",
    "find_repo_root",
    # Image generation
    "ImageClient",
    "ImageRequest",
    "ImagenWiring",
    "VariantSet",
    # ComfyForge Tier 1
    "ComfyForgeConfig",
    "ComfyForgeTier1Adapter",
    "load_style_config",
    "resolve_style",
    # Mermaid
    "MermaidGenerator",
    "MermaidNode",
    "MermaidEdge",
    # Print
    "PrintExporter",
    "PanelPlacement",
    "PageExportSpec",
    "ExportResult",
    "canvas_units_to_px",
    "effective_dpi",
    # PDF export (Pillar C / ADR-010)
    "PdfExporter",
    "export_composites_to_pdf",
    # Google Doc export (Pillar D / ADR-011)
    "DocElement",
    "Paragraph",
    "Heading",
    "BulletList",
    "InlineImage",
    "GdocExporter",
    "export_canvas_to_gdoc",
    "GdocAuthError",
    "GdocApiError",
    # Visual inspector
    "ScreenshotResult",
    "ScreenshotBatch",
    "prepare_screenshots",
    "visual_inspect",
    "build_review_report",
    "save_review_report",
    "compare_reviews",
    "build_automated_report",
    # Text metrics
    "measure_text_extent",
    # III Trap Pack
    "TrapFinding",
    "TRAP_PACK_REGISTRY",
    "run_all_traps",
    # RLHF variant selection
    "SelectionRecord",
    "validate_selection_record",
    "write_selection",
    "append_audit_log",
    # Multi-voice review
    "CANONICAL_VOICES",
    "MultiVoiceReviewer",
    "MultiVoiceReport",
    "ReviewerVoice",
    "ReviewFinding",
    # Agent critique
    "CritiqueFinding",
    "CritiqueResult",
    "run_critique",
    # Opener
    "CanvasOpener",
]
