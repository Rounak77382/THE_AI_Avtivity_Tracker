"""
scripts/test_model.py
=====================
Validates your fine-tuned GGUF model directly through the tracking pipeline.
Ensures the predictions are correctly formatted and accurate prior to deployment.

Run from the project root:
    python scripts/test_model.py
"""

import sys
import os

_HERE      = os.path.dirname(os.path.abspath(__file__))
_PROJ_ROOT = os.path.dirname(_HERE)
sys.path.insert(0, _PROJ_ROOT)  # allows absolute imports from core

from core.AI_Evalution import classify_window

test_cases = [
    # (window_title,                                    expected)
    ("Visual Studio Code - Activity_Tracker.py",        "YES"),
    ("YouTube - Movie Trailer",                         "NO"),
    ("SAP BTP Cockpit - Deployment",                    "YES"),
    ("Instagram",                                       "NO"),
    ("Stack Overflow - Fix recursion bug",              "YES"),
    ("GitHub - Pull Request Review",                    "YES"),
    ("Netflix - Breaking Bad S01E01",                   "NO"),
    ("Windows PowerShell - pip install unsloth",        "YES"),
    ("Spotify - Playlist",                              "NO"),
    ("Postman - API Testing",                           "YES"),
]

if __name__ == "__main__":
    print(f"\n{'Window Title':<55} {'Expected':<10} {'Got':<10} {'Pass?'}")
    print("─" * 85)

    correct = 0
    for window, expected in test_cases:
        got  = classify_window(window)
        ok   = "✅" if got == expected else "❌"
        correct += int(got == expected)
        print(f"  {window[:53]:<55} {expected:<10} {got:<10} {ok}")

    total = len(test_cases)
    accuracy = (correct / total) * 100
    print(f"\nAccuracy: {correct}/{total} = {accuracy:.0f}%")
    print("Target: ≥ 90% — if below, add more training examples and re-fine-tune.")
