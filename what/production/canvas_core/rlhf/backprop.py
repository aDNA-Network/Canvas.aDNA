"""Dataset backpropagation — atomic writes to image_gen_dataset/.

Per skill_canvas_variant_selection.md § 6:
- Atomicity is load-bearing (write-temp-then-rename)
- Schema-violation is hard-fail, not silent-skip
- Append-only audit log

Created in M-5-07.
"""

from __future__ import annotations

import json
import logging
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .selection import SelectionRecord, validate_selection_record

logger = logging.getLogger(__name__)

# Default dataset root (relative to forge root)
DEFAULT_DATASET_ROOT = "what/artifacts/image_gen_dataset"


def write_selection(
    record: SelectionRecord,
    dataset_root: str | Path | None = None,
) -> Path:
    """Atomically write a SelectionRecord to the training corpus.

    Writes to: <dataset_root>/<YYYY-MM>/<selection_id>.json
    Appends to: <dataset_root>/<YYYY-MM>/audit.log

    Uses write-temp-then-rename for atomicity. Schema-violation is
    hard-fail — raises ValueError, does NOT silently skip.

    Returns the path to the written JSON file.
    """
    # Validate first — hard fail on schema violation
    errors = validate_selection_record(record)
    if errors:
        raise ValueError(
            f"SelectionRecord schema violation (hard-fail per ADR 003 D4): "
            + "; ".join(errors)
        )

    # Determine output directory
    root = Path(dataset_root) if dataset_root else Path(DEFAULT_DATASET_ROOT)
    year_month = datetime.fromisoformat(record.timestamp).strftime("%Y-%m")
    month_dir = root / year_month
    month_dir.mkdir(parents=True, exist_ok=True)

    # Atomic write: temp file → rename
    target = month_dir / f"{record.selection_id}.json"
    data = json.dumps(record.to_dict(), indent=2) + "\n"

    tmp_fd, tmp_path = tempfile.mkstemp(
        dir=str(month_dir), suffix=".tmp", prefix=".sel_"
    )
    try:
        with open(tmp_fd, "w") as f:
            f.write(data)
        Path(tmp_path).rename(target)
    except Exception:
        # Clean up temp file on failure
        Path(tmp_path).unlink(missing_ok=True)
        raise

    logger.info("Selection record written: %s", target)

    # Append audit log
    append_audit_log(record, month_dir)

    return target


def append_audit_log(
    record: SelectionRecord,
    month_dir: str | Path,
) -> None:
    """Append a one-line entry to the audit log.

    Format: <ISO8601> <selection_id> <approver_id>
    """
    log_path = Path(month_dir) / "audit.log"
    line = f"{record.timestamp} {record.selection_id} {record.approver_id}\n"
    with open(log_path, "a") as f:
        f.write(line)
