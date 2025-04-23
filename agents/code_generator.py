import os
import datetime
import json
import re
import google.generativeai as genai
from pathlib import Path

OUTPUT_DIR = Path("generated_code")
OUTPUT_DIR.mkdir(exist_ok=True)

# Gemini API setup: must set GEMINI_API_KEY in GitHub Secrets
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY environment variable not set.")
genai.configure(api_key=api_key)

def generate_code_from_prompt(prompt: str) -> str:
    directive = (
        "You are a code generation assistant. "
        "Output only the requested code snippet—no explanation or commentary."
    )
    full_prompt = directive + "\n" + prompt
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(full_prompt)
    text = response.text.strip()

    # Strip any Markdown fences
    m = re.search(r"```(?:python)?\n([\s\S]*?)```", text)
    return m.group(1).strip() if m else text

def extract_prompt_from_event() -> str:
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        # local testing fallback
        return "Write a Python function to sort a list."

    with open(event_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    prompt = None
    # 1) comment body
    if "comment" in data and data["comment"].get("body"):
        prompt = data["comment"]["body"]
    # 2) issue body
    elif "issue" in data and data["issue"].get("body"):
        prompt = data["issue"]["body"]
    # 3) PR body
    elif "pull_request" in data and data["pull_request"].get("body"):
        prompt = data["pull_request"]["body"]

    # 4) fallback to issue or PR title if body was empty
    if not prompt:
        if "issue" in data and data["issue"].get("title"):
            prompt = data["issue"]["title"]
        elif "pull_request" in data and data["pull_request"].get("title"):
            prompt = data["pull_request"]["title"]

    # final fallback
    return prompt or "Write a Python function to sort a list."

def main():
    prompt = extract_prompt_from_event()
    generated_code = generate_code_from_prompt(prompt)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = OUTPUT_DIR / f"{timestamp}_generated.py"
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(generated_code)

    print(f"✅ Code generated and saved to {out_file}")

if __name__ == "__main__":
    main()