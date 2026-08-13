#!/usr/bin/env python3
"""M-5-05: Image-Gen Fidelity Audit — cloud baseline generation

Generates 3 test images via the shared Google model layer across Science
Stanley's 3 visual registers (Ghibli, Pixel, Transition). Records each as a
SelectionRecord in the RLHF training corpus.

Charter: A/B comparison cloud vs ComfyForge. ComfyForge columns deferred
(Anduril offline, LoRA not converged). This script produces the cloud column.

Migrated 2026-08-13 off `imagen-4.0-generate-001` (shutdown 2026-08-17) onto
`Home.aDNA/what/code/googleai/`, requesting the `image.pro` capability instead
of a literal model ID. Operation Rosetta Stone R5.

Usage:
    python mvp_imagen_fidelity.py

Credentials are resolved by the shared Google model layer (Home.aDNA broker, lane order
C63 Vertex SA -> C62 -> C57 -> C04 -> C05); no API key is read here and none should be.
"""

import json
import sys
import time
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_ROOT))

from _googleai import require_googleai
from canvas_core.rlhf.selection import SelectionRecord, VariantInfo
from canvas_core.rlhf.backprop import write_selection

# Requested by CAPABILITY, never by literal ID — the registry owns which model that resolves to,
# so a model retirement is a registry edit rather than a sweep of every call site in the fleet.
DEFAULT_MODEL = "image.pro"
IMAGE_SIZE = "2K"

# Output paths
ARTIFACT_DIR = CODE_ROOT.parent / "artifacts" / "image_gen_fidelity" / "imagen"
DATASET_ROOT = CODE_ROOT.parent / "artifacts" / "image_gen_dataset"

# Science Stanley character invariance anchors
CHARACTER_PROMPT_BASE = (
    "Science Stanley, a warm and approachable science communicator, "
    "wearing a purple turtleneck sweater, round glasses, holding a clipboard. "
    "Professional portrait style, detailed, high quality"
)

REGISTER_PROMPTS = {
    "ghibli": {
        "prompt": f"{CHARACTER_PROMPT_BASE}, Studio Ghibli anime art style, "
                  "soft watercolor textures, warm golden lighting, Miyazaki-inspired, "
                  "lush background, whimsical atmosphere",
        "register": "R3",
    },
    "pixel": {
        "prompt": f"{CHARACTER_PROMPT_BASE}, pixel art retro style, "
                  "8-bit aesthetic, terminal green CRT glow, limited color palette, "
                  "retro computing atmosphere, scanline effect",
        "register": "R3",
    },
    "transition": {
        "prompt": f"{CHARACTER_PROMPT_BASE}, blending Studio Ghibli warmth with "
                  "pixel art edges, mixed media style, watercolor base with digital "
                  "pixel overlay, transitional atmosphere between analog and digital",
        "register": "R3",
    },
}


def generate_with_gemini(prompt: str, output_path: Path) -> dict:
    """Generate a single image via the shared Google model layer.

    Migrated 2026-08-13 (Operation Rosetta Stone R5). This used to inline
    ``imagen-4.0-generate-001`` and a hardcoded ``$0.04``; that model family shuts down 2026-08-17.
    The model is now requested **by capability** (``image.pro``) so the registry decides which ID
    that is, and the price comes from the registry's table rather than from a literal here.

    The layer writes the file itself and returns errors rather than raising, so there is no
    ``try/except`` and no response unwrapping left to get wrong.
    """
    googleai = require_googleai()

    start = time.time()
    result = googleai.get_client().generate_image(
        prompt, str(output_path), model=DEFAULT_MODEL, image_size=IMAGE_SIZE
    )
    result["elapsed_s"] = time.time() - start

    if result.get("success"):
        from PIL import Image as PILImage

        with PILImage.open(str(output_path)) as pil_img:
            result["width"], result["height"] = pil_img.size

    return result


def run_fidelity_audit():
    """Execute the Imagen fidelity baseline generation."""
    print("=" * 60)
    print("M-5-05: Image-Gen Fidelity Audit — Imagen Baseline")
    print("=" * 60)

    results = {}
    total_cost = 0.0

    for register_name, config in REGISTER_PROMPTS.items():
        print(f"\n[{register_name.upper()}] Generating...")
        output_path = ARTIFACT_DIR / f"stanley_{register_name}.png"

        result = generate_with_gemini(config["prompt"], output_path)
        results[register_name] = result

        if result["success"]:
            total_cost += result["cost_usd"]
            print(f"  OK: {output_path.name} ({result['elapsed_s']:.1f}s, "
                  f"${result['cost_usd']:.3f}, lane {result['lane']})")

            # Write RLHF corpus entry.
            # `model` and `cost_usd` come from the RESULT, never from a default here. Until
            # 2026-08-13 this recorded model="imagen-4-ultra" / cost=0.06 as fallbacks while the
            # call actually used imagen-4.0-generate-001 at 0.04 — so the corpus could attribute a
            # judgement to a model that was never invoked. A training corpus that misnames its own
            # generator is worse than an empty one.
            try:
                record = SelectionRecord(
                    prompt=config["prompt"],
                    register=config["register"],
                    variants=[VariantInfo(
                        image_path=result["image_path"],
                        model=result["model"],
                        cost_usd=result["cost_usd"],
                    )],
                    pick_index=0,
                    pick_reason=f"Single variant — Imagen baseline for {register_name} register",
                    approver_id="herb",
                    budget_class="standard",
                )
                corpus_path = write_selection(record, dataset_root=str(DATASET_ROOT))
                print(f"  Corpus: {corpus_path.name}")
            except Exception as e:
                print(f"  Corpus write failed: {e}")
        else:
            print(f"  FAILED: {result.get('error', 'unknown')}")

    # Summary
    succeeded = sum(1 for r in results.values() if r.get("success"))
    print(f"\n{'=' * 60}")
    print(f"IMAGE FIDELITY BASELINE RESULTS")
    print(f"{'=' * 60}")
    print(f"  Generated: {succeeded}/3 images")
    print(f"  Total cost: ${total_cost:.3f}")  # 3dp: image prices are sub-cent-sensitive ($0.134)
    print(f"  Output: {ARTIFACT_DIR}")
    for name, r in results.items():
        if not r.get("success"):
            print(f"  FAILED [{name}]: {r.get('error', 'unknown')}")

    # Character invariance notes (qualitative — images must be viewed)
    if succeeded > 0:
        print(f"\n  Character invariance check (manual review required):")
        print(f"    - Purple turtleneck: [view images]")
        print(f"    - Round glasses: [view images]")
        print(f"    - Clipboard: [view images]")
        print(f"    - Consistent face/build: [view images]")

    return results


if __name__ == "__main__":
    run_fidelity_audit()
