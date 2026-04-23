"""
scripts/prepare_dataset.py
============================
Use this script ONLY if you are starting fresh without an existing dataset.
If you already have final_data_set.json, run convert_existing_dataset.py instead.

Paste your labeled (window_title, profession, label) tuples into raw_data below,
then run:
    python scripts/prepare_dataset.py

Output: dataset/train.jsonl
"""

import json
import os

# ── Config ────────────────────────────────────────────────────────────────────
_HERE      = os.path.dirname(os.path.abspath(__file__))
_PROJ_ROOT = os.path.dirname(_HERE)
OUTPUT_FILE = os.path.join(_PROJ_ROOT, "dataset", "train.jsonl")

PROFESSION = "Software Developer"  # Change to match your actual profession

# Format: (window_title, profession, "YES"/"NO")
# Add your own entries below. The more diverse the better.
raw_data = [
    ("Visual Studio Code - main.py",                  "Software Developer", "YES"),
    ("YouTube - Lo-fi Music",                         "Software Developer", "NO"),
    ("Stack Overflow - Python error fix",             "Software Developer", "YES"),
    ("Netflix - Stranger Things",                     "Software Developer", "NO"),
    ("GitHub - Pull Request Review",                  "Software Developer", "YES"),
    ("WhatsApp Web",                                  "Software Developer", "NO"),
    ("SAP BTP Cockpit - Deployment",                  "Software Developer", "YES"),
    ("Marvel Rivals",                                 "Software Developer", "NO"),
    ("Windows PowerShell - pip install requests",     "Software Developer", "YES"),
    ("Spotify - Playlist",                            "Software Developer", "NO"),
    ("Postman - API Testing",                         "Software Developer", "YES"),
    ("Instagram",                                     "Software Developer", "NO"),
    # ── Add more entries here ────────────────────────────────────────────────
]

# ── Prompt ────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are a productivity classifier. Given a profession and an active window title, "
    "reply with ONLY YES or NO — whether the task is directly productive for that profession."
)


def to_chat_format(window_title: str, profession: str, label: str) -> dict:
    return {
        "messages": [
            {"role": "system",    "content": SYSTEM_PROMPT},
            {
                "role":    "user",
                "content": (
                    f"Profession: {profession}\n"
                    f"Active Window: {window_title}\n"
                    f"Is this directly productive?"
                ),
            },
            {"role": "assistant", "content": label},
        ]
    }


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for window, profession, label in raw_data:
            entry = to_chat_format(window, profession, label)
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    yes = sum(1 for _, _, l in raw_data if l == "YES")
    no  = sum(1 for _, _, l in raw_data if l == "NO")
    print(f"Saved {len(raw_data)} entries to {OUTPUT_FILE}")
    print(f"  YES: {yes}  |  NO: {no}")

    if len(raw_data) < 100:
        print(
            "\n⚠️  Small dataset warning: you have fewer than 100 entries.\n"
            "   Fine-tuning on very little data can cause over-fitting.\n"
            "   Aim for at least 300–500 diverse examples."
        )
