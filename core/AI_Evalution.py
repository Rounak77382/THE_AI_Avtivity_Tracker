# core/AI_Evalution.py  —  Qwen3-1.7B via llama-cpp-python (fully offline)

from llama_cpp import Llama
from core.model_manager import ensure_model
import csv
import os
import datetime

# ── Configuration ─────────────────────────────────────────────────────────────
PROFESSION = "Software Developer"   # Change to match the user's profession

# Prompt template using Qwen3 ChatML format
PROMPT_TEMPLATE = """\
<|im_start|>system
You are a productivity classifier. Given a profession and an active window title, reply with ONLY YES or NO.<|im_end|>
<|im_start|>user
Profession: {profession}
Active Window: {window_title}
Is this directly productive?<|im_end|>
<|im_start|>assistant
"""

# ── Load model once at startup ────────────────────────────────────────────────
# ensure_model() downloads the model if it's missing, then we load it
_model_path = ensure_model()

print("Initializing AI Evaluator...")
llm = Llama(
    model_path   = _model_path,
    n_gpu_layers = 99,      # offload all layers to GPU (GTX 1650 safe at Q8_0)
    n_ctx        = 512,     # short context = faster + less VRAM
    verbose      = False,
)


# ── Core classification function ──────────────────────────────────────────────
def classify_window(window_title: str, profession: str = PROFESSION) -> str:
    """
    Returns "YES" if the window is directly productive for the given profession,
    "NO" if not, or "UNKNOWN" if the model gives an unexpected response.
    """
    prompt = PROMPT_TEMPLATE.format(
        profession   = profession,
        window_title = window_title
    )

    try:
        output = llm(
            prompt,
            max_tokens  = 3,
            temperature = 0.0,   # deterministic — always same answer for same input
            stop        = ["<|im_end|>", "\n"],
        )
        result = output["choices"][0]["text"].strip().upper()
        return "YES" if "YES" in result else ("NO" if "NO" in result else "UNKNOWN")

    except Exception as e:
        print(f"[AI Error] {e}")
        return "UNKNOWN"


# ── Batch evaluation of a daily CSV ──────────────────────────────────────────
def evaluate_csv(csv_path: str) -> list:
    """
    Reads a daily activity CSV (name, time) and evaluates each entry.
    Saves results to *_AI_Evaluated.csv with a 'productive' column.
    """
    if not os.path.isfile(csv_path):
        print(f"File not found: {csv_path}")
        return []

    results = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            next(reader)  # skip header
        except StopIteration:
            return []
        
        rows = list(reader)

    print(f"\nEvaluating {len(rows)} entries...\n")

    for row in rows:
        if len(row) < 2:
            continue
        app_name, time_spent = row[0], row[1]
        verdict = classify_window(app_name)
        results.append([app_name, time_spent, verdict])
        icon = "✅" if verdict == "YES" else "❌"
        print(f"  {icon}  {app_name[:60]:<60}  {verdict}")

    output_path = csv_path.rsplit(".", 1)[0] + "_AI_Evaluated.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "time", "productive"])
        writer.writerows(results)

    print(f"\nSaved → {output_path}")
    return results


# ── Run directly to evaluate today's data ────────────────────────────────────
if __name__ == "__main__":
    _HERE = os.path.dirname(os.path.abspath(__file__))
    _PROJ_ROOT = os.path.dirname(_HERE)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    path  = os.path.join(_PROJ_ROOT, "datas", f"{today}.csv")
    evaluate_csv(path)
