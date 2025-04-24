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

# Helper to prevent recursive "_flagged.py" naming
def get_safe_flagged_filename(file):
    base_name = file
    while base_name.endswith("_flagged.py"):
        base_name = base_name[:-12]  # remove "_flagged.py"
    return f"{base_name}_flagged.py"

def review_files():
    log_file = REVIEW_DIR / f"{datetime.datetime.now():%Y%m%d_%H%M%S}_review.md"
    with open(log_file, "w", encoding="utf-8") as log:
        for root, _, files in os.walk("."):
            for file in files:
                if file.endswith(".py") and not root.startswith("./agents"):
                    filepath = os.path.join(root, file)
                    issues = run_lint_check(filepath)
                    if issues:
                        log.write(f"## {filepath}\n```\n{issues}\n```\n\n")
                        flagged_filename = get_safe_flagged_filename(file)
                        flagged_copy = FLAGGED_DIR / flagged_filename
                        with open(filepath, "r", encoding="utf-8") as src, open(flagged_copy, "w", encoding="utf-8") as dst:
                            dst.write(src.read())
    print(f"✅ Review completed. Logs saved to {log_file}")

if __name__ == "__main__":
    review_files()
