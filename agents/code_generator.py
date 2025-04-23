import os
import datetime
import json
import re
import google.generativeai as genai
from pathlib import Path

OUTPUT_DIR = Path("generated_code")
OUTPUT_DIR.mkdir(exist_ok=True)

# Gemini API setup: API key provided via GitHub Secrets as environment variable 'GEMINI_API_KEY'
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise EnvironmentError("GEMINI_API_KEY environment variable not set.")
genai.configure(api_key=api_key)

def generate_code_from_prompt(prompt: str) -> str:
    # Directive to ensure code-only output
    directive = (
        "You are a code generation assistant. "
        "When responding, output only the requested code snippet without any additional explanation or commentary."
    )
    full_prompt = directive + "\n" + prompt
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(full_prompt)
    text = response.text.strip()

    # Strip any Markdown code fences and return pure code
    fence_match = re.search(r"```(?:python)?\n([\s\S]*?)```", text)
    if fence_match:
        return fence_match.group(1).strip()
    return text

def extract_prompt_from_event() -> str:
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        # Fallback for local testing
        return "Write a Python function to sort a list."

    with open(event_path, "r", encoding="utf-8") as f:
        event_data = json.load(f)

    prompt = None
    if "comment" in event_data and event_data["comment"].get("body"):
        prompt = event_data["comment"]["body"]
    elif "issue" in event_data and event_data["issue"].get("body"):
        prompt = event_data["issue"]["body"]
    elif "pull_request" in event_data and event_data["pull_request"].get("body"):
        prompt = event_data["pull_request"]["body"]

    # Ensure we always return a string
    return prompt or "Write a Python function to sort a list."

def main():
    prompt = extract_prompt_from_event()
    generated_code = generate_code_from_prompt(prompt)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"{timestamp}_generated.py"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(generated_code)

    print(f"✅ Code generated and saved to {output_file}")

if __name__ == "__main__":
    main()