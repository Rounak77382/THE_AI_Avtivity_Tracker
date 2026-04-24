"""
scripts/convert_existing_dataset.py
====================================
Converts your existing Alpaca-format training data (final_data_set.json)
into the ChatML JSONL format that Qwen3 fine-tuning expects.

Run from the project root:
    python scripts/convert_existing_dataset.py

Input  : final_data_set.json  (Alpaca: instruction / input / output)
Output : dataset/train.jsonl  (ChatML: messages list with YES / NO labels)
"""

import json
import os
import re

# ── Config ────────────────────────────────────────────────────────────────────
# Absolute path relative to this script's location so it works from any cwd.
_HERE       = os.path.dirname(os.path.abspath(__file__))
_PROJ_ROOT  = os.path.dirname(_HERE)

INPUT_FILE  = os.path.join(_PROJ_ROOT, "extras/datasets/final_data_set.json")
OUTPUT_FILE = os.path.join(_PROJ_ROOT, "dataset", "train.jsonl")

SYSTEM_PROMPT = (
    "You are a productivity classifier. Given a profession and an active window title, "
    "reply with ONLY YES or NO — whether the task is directly productive for that profession."
)


# ── Helpers ───────────────────────────────────────────────────────────────────
def extract_profession(instruction: str) -> str:
    """
    Extracts the profession name from an Alpaca instruction string.
    e.g. '...directly productive for a SOFTWARE DEVELOPER...' → 'Software Developer'
    """
    match = re.search(r"productive for (?:a |an )?(.+?)\.", instruction, re.IGNORECASE)
    if match:
        return match.group(1).strip().title()
    return "Software Developer"  # safe fallback


def convert_label(output: str) -> str:
    """Converts 'True' / 'False' (any case) → 'YES' / 'NO'."""
    return "YES" if output.strip().lower() == "true" else "NO"


def convert_entry(entry: dict) -> dict:
    profession  = extract_profession(entry["instruction"])
    window      = entry["input"].strip()
    label       = convert_label(entry["output"])

    return {
        "messages": [
            {
                "role":    "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role":    "user",
                "content": (
                    f"Profession: {profession}\n"
                    f"Active Window: {window}\n"
                    f"Is this directly productive?"
                ),
            },
            {
                "role":    "assistant",
                "content": label,
            },
        ]
    }


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}\n"
            "Make sure you run this script from the project root."
        )

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    print(f"Loaded {len(raw_data)} entries from {os.path.basename(INPUT_FILE)}")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    yes_count = no_count = skip_count = 0
    converted = []

    for i, entry in enumerate(raw_data):
        if not all(k in entry for k in ["instruction", "input", "output"]):
            print(f"  [Skip] Entry {i} missing required keys")
            skip_count += 1
            continue
        if not entry["input"].strip():
            skip_count += 1
            continue

        result = convert_entry(entry)
        converted.append(result)

        label = result["messages"][2]["content"]
        if label == "YES":
            yes_count += 1
        else:
            no_count += 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in converted:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"\nConversion complete!")
    print(f"  Total entries    : {len(raw_data)}")
    print(f"  Converted        : {len(converted)}")
    print(f"  Skipped          : {skip_count}")
    print(f"  YES (productive) : {yes_count}")
    print(f"  NO  (not prod.)  : {no_count}")

    total_labeled = yes_count + no_count
    if total_labeled > 0:
        ratio = yes_count / total_labeled
        print(f"  Balance ratio    : {ratio * 100:.1f}% YES")
        if ratio < 0.3 or ratio > 0.7:
            print(
                f"\n⚠️  WARNING: Dataset is imbalanced ({ratio * 100:.0f}% YES).\n"
                "   Consider adding more examples of the minority class before fine-tuning."
            )

    print(f"\nSaved → {OUTPUT_FILE}")
    print("\nNext step: run  python scripts/augment_dataset.py  to label new CSV data.")
