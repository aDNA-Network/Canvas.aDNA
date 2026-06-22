#!/usr/bin/env python3
"""M-5-05: Image-Gen Fidelity Audit — Imagen Baseline Generation

Generates 3 test images via Gemini/Imagen 4 Ultra across Science Stanley's
3 visual registers (Ghibli, Pixel, Transition). Records each as a
SelectionRecord in the RLHF training corpus — the first real corpus entries.

Charter: A/B comparison Imagen vs ComfyForge. ComfyForge columns deferred
(Anduril offline, LoRA not converged). This script produces the Imagen column.

Usage:
    GOOGLE_API_KEY=<key> python mvp_imagen_fidelity.py
"""

import json
import os
import sys
import time
from pathlib import Path

CODE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CODE_ROOT))

from canvas_core.rlhf.selection import SelectionRecord, VariantInfo
from canvas_core.rlhf.backprop import write_selection

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


def generate_with_gemini(prompt: str, output_path: Path, api_key: str) -> dict:
    """Generate a single image via Imagen 4 (google-genai SDK)."""
    from google import genai

    client = genai.Client(api_key=api_key)

    start = time.time()
    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=genai.types.GenerateImagesConfig(number_of_images=1),
        )

        elapsed = time.time() - start

        if response.generated_images:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            img = response.generated_images[0].image
            img.save(str(output_path))

            from PIL import Image as PILImage
            pil_img = PILImage.open(str(output_path))

            return {
                "success": True,
                "image_path": str(output_path),
                "elapsed_s": elapsed,
                "model": "imagen-4.0-generate-001",
                "cost_usd": 0.04,
                "width": pil_img.size[0],
                "height": pil_img.size[1],
            }

        return {"success": False, "error": "No images returned", "elapsed_s": elapsed}

    except Exception as e:
        elapsed = time.time() - start
        return {"success": False, "error": str(e), "elapsed_s": elapsed}


def run_fidelity_audit():
    """Execute the Imagen fidelity baseline generation."""
    print("=" * 60)
    print("M-5-05: Image-Gen Fidelity Audit — Imagen Baseline")
    print("=" * 60)

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not set")
        print("Usage: GOOGLE_API_KEY=<key> python mvp_imagen_fidelity.py")
        sys.exit(1)

    results = {}
    total_cost = 0.0

    for register_name, config in REGISTER_PROMPTS.items():
        print(f"\n[{register_name.upper()}] Generating...")
        output_path = ARTIFACT_DIR / f"stanley_{register_name}.png"

        result = generate_with_gemini(config["prompt"], output_path, api_key)
        results[register_name] = result

        if result["success"]:
            total_cost += result.get("cost_usd", 0.06)
            print(f"  OK: {output_path.name} ({result['elapsed_s']:.1f}s, ${result['cost_usd']:.2f})")

            # Write RLHF corpus entry
            try:
                record = SelectionRecord(
                    prompt=config["prompt"],
                    register=config["register"],
                    variants=[VariantInfo(
                        image_path=str(output_path),
                        model=result.get("model", "imagen-4-ultra"),
                        cost_usd=result.get("cost_usd", 0.06),
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
    print(f"IMAGEN BASELINE RESULTS")
    print(f"{'=' * 60}")
    print(f"  Generated: {succeeded}/3 images")
    print(f"  Total cost: ${total_cost:.2f}")
    print(f"  Output: {ARTIFACT_DIR}")

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
