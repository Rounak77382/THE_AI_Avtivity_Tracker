"""
core/model_manager.py
Ensures the Qwen3-1.7B GGUF model is present locally.
On first run it downloads the file from HuggingFace (~1.9 GB).
All subsequent runs just return the cached path — no network needed.
"""

import os
import requests
from tqdm import tqdm

# ── Paths ─────────────────────────────────────────────────────────────────────
# Resolve relative to this file so the app works regardless of cwd.
_HERE       = os.path.dirname(os.path.abspath(__file__))
_PROJ_ROOT  = os.path.dirname(_HERE)

MODEL_PATH = os.path.join(
    _PROJ_ROOT, "models", "qwen3_activity_tracker", "model-Q8_0.gguf"
)

# Public HuggingFace mirror for the base Qwen3-1.7B Q8_0 GGUF.
# If you ship a fine-tuned GGUF, replace this URL (or leave it and just
# place the file at MODEL_PATH before distributing).
MODEL_URL = (
    "https://huggingface.co/bartowski/Qwen_Qwen3-1.7B-GGUF/resolve/main/"
    "Qwen_Qwen3-1.7B-Q8_0.gguf"
)


# ── Public API ────────────────────────────────────────────────────────────────
def ensure_model() -> str:
    """
    Returns the absolute path to the GGUF model file.
    Downloads the file on first call if it is not already present.
    """
    if os.path.exists(MODEL_PATH):
        return MODEL_PATH

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    print("=" * 60)
    print("First-time setup: Downloading AI model (~1.9 GB)...")
    print("This only happens once. Please wait.")
    print("=" * 60)

    try:
        response = requests.get(MODEL_URL, stream=True, timeout=60)
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))

        with open(MODEL_PATH, "wb") as f, tqdm(
            total=total,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc="Qwen3-1.7B Q8_0",
        ) as bar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                bar.update(len(chunk))

    except Exception as exc:
        # Clean up partial download so the next run retries cleanly.
        if os.path.exists(MODEL_PATH):
            os.remove(MODEL_PATH)
        raise RuntimeError(
            f"Model download failed: {exc}\n"
            "Check your internet connection and try again.\n"
            f"Or manually place the GGUF at:\n  {MODEL_PATH}"
        ) from exc

    print("\nModel downloaded successfully. Starting tracker...\n")
    return MODEL_PATH
