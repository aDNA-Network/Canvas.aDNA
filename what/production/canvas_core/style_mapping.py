"""Style mapping loader for ComfyForge ss_style_mapping.yaml.

Loads and resolves style configurations from the ComfyForge style mapping
file (M08 S1, 17 mutation operators). Guarded import of PyYAML — falls
back to empty config if yaml is unavailable.

Migrated: N/A (new in M-3-05)
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def load_style_config(path: str | Path) -> dict[str, Any]:
    """Load a style configuration YAML file.

    Returns an empty dict (with logged warning) if:
    - PyYAML is not installed
    - The file doesn't exist
    - The file is malformed
    """
    path = Path(path)
    if not path.exists():
        logger.warning("Style config not found: %s", path)
        return {}

    try:
        import yaml
    except ImportError:
        logger.warning(
            "PyYAML not installed — style config at %s will not be loaded. "
            "Install with: pip install pyyaml",
            path,
        )
        return {}

    try:
        with open(path) as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            logger.warning("Style config at %s is not a dict, ignoring", path)
            return {}
        return data
    except Exception as e:
        logger.warning("Failed to load style config at %s: %s", path, e)
        return {}


def resolve_style(
    config: dict[str, Any],
    register: str,
    style_hints: str,
) -> dict[str, Any]:
    """Resolve style modifiers from a loaded style config.

    Looks up the register key in the config's mutation operators and
    returns a dict of applicable style modifications. Falls back to
    empty modifiers if the register isn't found.

    Returns a dict with optional keys:
        - positive_suffix: str to append to the positive prompt
        - negative_suffix: str to append to the negative prompt
        - checkpoint: override checkpoint name
        - lora: LoRA configuration (Tier 3, future)
    """
    if not config:
        return {}

    # Try direct register lookup in mutation_operators
    operators = config.get("mutation_operators", {})
    if register and register in operators:
        op = operators[register]
        result: dict[str, Any] = {}
        if isinstance(op, dict):
            if op.get("positive_suffix"):
                result["positive_suffix"] = op["positive_suffix"]
            if op.get("negative_suffix"):
                result["negative_suffix"] = op["negative_suffix"]
            if op.get("checkpoint"):
                result["checkpoint"] = op["checkpoint"]
            if op.get("lora"):
                result["lora"] = op["lora"]
        return result

    # Try style_hints as a fallback lookup key
    if style_hints:
        for key, op in operators.items():
            if isinstance(op, dict) and style_hints.lower() in key.lower():
                result = {}
                if op.get("positive_suffix"):
                    result["positive_suffix"] = op["positive_suffix"]
                return result

    return {}
