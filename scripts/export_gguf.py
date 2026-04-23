"""
scripts/export_gguf.py
======================
Merges your saved LoRA adapter into the base model and exports it as a
standard GGUF file for local inference via llama-cpp-python.

Run from the project root:
    python scripts/export_gguf.py

Input  : models/qwen3_activity_lora/
Output : models/qwen3_activity_tracker/model-Q8_0.gguf
"""

import os

try:
    from unsloth import FastLanguageModel
except ImportError as exc:
    raise SystemExit(
        "Unsloth is not installed. Please follow the setup guide or run:\n"
        "pip install unsloth"
    ) from exc

# ── Config ────────────────────────────────────────────────────────────────────
_HERE      = os.path.dirname(os.path.abspath(__file__))
_PROJ_ROOT = os.path.dirname(_HERE)

LORA_DIR   = os.path.join(_PROJ_ROOT, "models", "qwen3_activity_lora")
OUT_DIR    = os.path.join(_PROJ_ROOT, "models", "qwen3_activity_tracker")
# The final filename unsloth writes is typically: model-unsloth-Q8_0.gguf
# but if quantization_method is passed, it manages it.


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not os.path.exists(LORA_DIR):
        raise FileNotFoundError(
            f"LoRA adapter not found at {LORA_DIR}\n"
            "Did you run scripts/finetune.py first?"
        )

    print(f"Loading LoRA from {LORA_DIR}...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name     = LORA_DIR,
        max_seq_length = 512,
        load_in_4bit   = True,  # we load in 4bit to save VRAM during merging
    )

    os.makedirs(OUT_DIR, exist_ok=True)
    print("\nMerging LoRA and exporting to Q8_0 GGUF...")
    print("This may take a few minutes depending on your system.\n")

    # Q8_0 is ~1.9GB and provides near lossless quality.
    model.save_pretrained_gguf(
        OUT_DIR,
        tokenizer,
        quantization_method="q8_0"
    )

    gguf_path = os.path.join(OUT_DIR, "model-unsloth-Q8_0.gguf")
    if os.path.exists(gguf_path):
        target = os.path.join(OUT_DIR, "model-Q8_0.gguf")
        if os.path.exists(target):
            os.remove(target)
        os.rename(gguf_path, target)
        print(f"\n✅ Build complete! GGUF saved to:\n  {target}")
    else:
        # Unsloth naming convention can sometimes vary.
        print(f"\n✅ Build complete! Models are saved in:\n  {OUT_DIR}")
        print("You may need to rename the .gguf file to model-Q8_0.gguf")
