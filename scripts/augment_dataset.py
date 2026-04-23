"""
scripts/augment_dataset.py
============================
Reads all datas/*.csv files produced by Activity_Tracker.py,
finds window titles not yet in your training data, and auto-labels
them using Qwen3 zero-shot via a local Ollama instance.

USE THIS FOR LABELING ONLY — Ollama is NOT used in the final app.

Prerequisites (one-time):
    ollama pull qwen3:1.7b-q8_0
    # Then keep Ollama running in the background.

Run from the project root:
    python scripts/augment_dataset.py

Output: dataset/new_to_review.jsonl  ← MANUALLY REVIEW before merging!
"""

import csv
import glob
import json
import os

import requests

# ── Config ────────────────────────────────────────────────────────────────────
_HERE       = os.path.dirname(os.path.abspath(__file__))
_PROJ_ROOT  = os.path.dirname(_HERE)

OLLAMA_URL  = "http://localhost:11434/api/generate"
PROFESSION  = "Software Developer"   # Change to match your profession
MODEL       = "qwen3:1.7b-q8_0"

TRAIN_JSONL   = os.path.join(_PROJ_ROOT, "dataset", "train.jsonl")
REVIEW_JSONL  = os.path.join(_PROJ_ROOT, "dataset", "new_to_review.jsonl")
CSV_GLOB      = os.path.join(_PROJ_ROOT, "datas", "*.csv")

SYSTEM_PROMPT = (
    "You are a productivity classifier. Given a profession and an active window title, "
    "reply with ONLY YES or NO — whether the task is directly productive for that profession."
)


# ── Zero-shot labeling via Ollama ─────────────────────────────────────────────
def zero_shot_label(window_title: str) -> str:
    payload = {
        "model":  MODEL,
        "prompt": (
            "/no_think\n"
            f"Profession: {PROFESSION}\n"
            f"Active Window: {window_title}\n"
            "Is this directly productive? Reply YES or NO only."
        ),
        "stream":  False,
        "options": {"temperature": 0.0, "num_predict": 5, "num_ctx": 256},
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=15)
        resp.raise_for_status()
        text = resp.json()["response"].strip().upper()
        return "YES" if "YES" in text else "NO"
    except requests.exceptions.ConnectionError:
        raise SystemExit(
            "\n[Error] Cannot reach Ollama at localhost:11434.\n"
            "Make sure Ollama is running:  ollama serve\n"
            "And the model is pulled:      ollama pull qwen3:1.7b-q8_0\n"
        )
    except Exception as exc:
        print(f"  [Warning] Label request failed ({exc}) — defaulting to UNKNOWN")
        return "UNKNOWN"


# ── Collect window titles from CSV files ──────────────────────────────────────
def collect_titles_from_csvs() -> set:
    titles = set()
    csv_files = glob.glob(CSV_GLOB)
    if not csv_files:
        print(f"No CSV files found in {os.path.join(_PROJ_ROOT, 'datas')}/")
        return titles

    print(f"Scanning {len(csv_files)} CSV file(s)...")
    for csv_file in csv_files:
        try:
            with open(csv_file, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header
                for row in reader:
                    if row and row[0].strip():
                        titles.add(row[0].strip())
        except Exception as exc:
            print(f"  [Skip] {os.path.basename(csv_file)}: {exc}")

    return titles


# ── Collect already-labeled titles ────────────────────────────────────────────
def collect_labeled_titles() -> set:
    labeled = set()
    if not os.path.exists(TRAIN_JSONL):
        return labeled

    with open(TRAIN_JSONL, "r", encoding="utf-8") as f:
        for line in f:
            try:
                entry    = json.loads(line)
                user_msg = entry["messages"][1]["content"]
                # Extract the window title from   "Active Window: <title>\n..."
                title    = user_msg.split("Active Window: ")[1].split("\n")[0]
                labeled.add(title)
            except (json.JSONDecodeError, KeyError, IndexError):
                continue

    return labeled


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    all_titles    = collect_titles_from_csvs()
    labeled       = collect_labeled_titles()
    new_titles    = all_titles - labeled

    print(f"\nTotal unique titles in CSVs : {len(all_titles)}")
    print(f"Already labeled             : {len(labeled)}")
    print(f"New titles to label         : {len(new_titles)}\n")

    if not new_titles:
        print("Nothing to do. All window titles are already labeled.")
        raise SystemExit(0)

    os.makedirs(os.path.dirname(REVIEW_JSONL), exist_ok=True)

    new_entries = []
    for title in sorted(new_titles):
        label = zero_shot_label(title)
        new_entries.append((title, PROFESSION, label))
        icon = "✅" if label == "YES" else ("❌" if label == "NO" else "❓")
        print(f"  {icon}  {title[:65]:<65}  {label}")

    with open(REVIEW_JSONL, "w", encoding="utf-8") as f:
        for title, prof, label in new_entries:
            entry = {
                "messages": [
                    {"role": "system",    "content": SYSTEM_PROMPT},
                    {
                        "role":    "user",
                        "content": (
                            f"Profession: {prof}\n"
                            f"Active Window: {title}\n"
                            f"Is this directly productive?"
                        ),
                    },
                    {"role": "assistant", "content": label},
                ]
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"\n✅ Saved {len(new_entries)} entries to {REVIEW_JSONL}")
    print("⚠️  IMPORTANT: Open the file and correct any wrong YES/NO labels before merging!")
    print("   Then run:  python scripts/merge_datasets.py")
