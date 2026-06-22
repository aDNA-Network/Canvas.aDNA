"""canvas_core.rlhf — Canvas-as-RLHF-surface package.

Formalizes variant-selection behavior into a first-class capability:
- VariantBoard: 2×N canvas grid for human pick in Obsidian
- SelectionRecord: canonical schema for recording selections
- Dataset backpropagation: atomic writes to image_gen_dataset/

Per ADR 003 § D4 and skill_canvas_variant_selection.md.
Informative for v1.0; load-bearing for post-v1.0 style transfer.

Created in M-5-07.
"""

from .selection import SelectionRecord, validate_selection_record
from .backprop import write_selection, append_audit_log
from .iii_bridge import (
    accumulate,
    accumulate_directory,
    selection_to_iii_signal,
)

__all__ = [
    "SelectionRecord",
    "validate_selection_record",
    "write_selection",
    "append_audit_log",
    "accumulate",
    "accumulate_directory",
    "selection_to_iii_signal",
]
