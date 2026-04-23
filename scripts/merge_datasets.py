"""
scripts/merge_datasets.py
===========================
Merges dataset/train.jsonl and dataset/new_to_review.jsonl
into dataset/merged_train.jsonl, deduplicating by user message content.

Run from the project root after reviewing new_to_review.jsonl:
    python scripts/merge_datasets.py

Output: dataset/merged_train.jsonl  ← feed this into finetune.py
"""

import json
import os

# ── Config ────────────────────────────────────────────────────────────────────
_HERE      = os.path.dirname(os.path.abspath(__file__))
_PROJ_ROOT = os.path.dirname(_HERE)

DATASET_DIR   = os.path.join(_PROJ_ROOT, "dataset")
INPUT_FILES   = [
    os.path.join(DATASET_DIR, "train.jsonl"),
    os.path.join(DATASET_DIR, "new_to_review.jsonl"),
]
OUTPUT_FILE   = os.path.join(DATASET_DIR, "merged_train.jsonl")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    merged = []
    seen   = set()

    yes_count = no_count = 0

    for file_path in INPUT_FILES:
        if not os.path.exists(file_path):
            print(f"  [Skip] Not found: {os.path.basename(file_path)}")
            continue

        file_count = 0
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError as exc:
                    print(f"  [Skip] Bad JSON line in {os.path.basename(file_path)}: {exc}")
                    continue

                # Deduplicate by the user-turn content (profession + window title)
                try:
                    key = entry["messages"][1]["content"]
                except (KeyError, IndexError):
                    continue

                if key not in seen:
                    seen.add(key)
                    merged.append(entry)
                    file_count += 1

                    # Tally labels for balance report
                    try:
                        label = entry["messages"][2]["content"].strip().upper()
                        if label == "YES":
                            yes_count += 1
                        else:
                            no_count  += 1
                    except (KeyError, IndexError):
                        pass

        print(f"  Loaded  {file_count:>5} unique entries from {os.path.basename(file_path)}")

    os.makedirs(DATASET_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in merged:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    total = len(merged)
    print(f"\n✅ Merged {total} unique entries → {OUTPUT_FILE}")
    print(f"   YES: {yes_count}  |  NO: {no_count}")

    if total > 0:
        ratio = yes_count / total
        print(f"   Balance: {ratio * 100:.1f}% YES")
        if ratio < 0.3 or ratio > 0.7:
            print(
                f"\n⚠️  Dataset is imbalanced ({ratio * 100:.0f}% YES).\n"
                "   Consider adding more minority-class examples before fine-tuning."
            )

    if total < 100:
        print(
            "\n⚠️  Small dataset warning: fewer than 100 entries.\n"
            "   Aim for 300–500+ for reliable fine-tuning."
        )

    print("\nNext step: run  python scripts/finetune.py")
