from dotenv import load_dotenv
load_dotenv()

import os
import datetime
import subprocess
from pathlib import Path

REVIEW_DIR = Path("review_reports")
FLAGGED_DIR = Path("flagged_code")
REVIEW_DIR.mkdir(exist_ok=True)
FLAGGED_DIR.mkdir(exist_ok=True)

def run_lint_check(filepath):
    result = subprocess.run(
        ["flake8", filepath],
        capture_output=True,
        text=True
    )
    return result.stdout

def review_files():
    log_file = REVIEW_DIR / f"{datetime.datetime.now():%Y%m%d_%H%M%S}_review.md"
    with open(log_file, "w", encoding="utf-8") as log:  # Ensure log file uses UTF-8 encoding
        for root, _, files in os.walk("."):
            for file in files:
                if file.endswith(".py") and not root.startswith("./agents"):
                    filepath = os.path.join(root, file)
                    issues = run_lint_check(filepath)
                    if issues:
                        log.write(f"## {filepath}\n```\n{issues}\n```\n\n")
                        flagged_copy = FLAGGED_DIR / f"{file}_flagged.py"
                        # Open source file with UTF-8 encoding
                        with open(filepath, "r", encoding="utf-8", errors="ignore") as src, open(flagged_copy, "w", encoding="utf-8") as dst:
                            dst.write(src.read())
    print(f"✅ Review completed. Logs saved to {log_file}")

if __name__ == "__main__":
    review_files()
