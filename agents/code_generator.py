from dotenv import load_dotenv
load_dotenv()

import os
import datetime
import json
import re
import google.generativeai as genai
from pathlib import Path

OUTPUT_DIR = Path("generated_code")
OUTPUT_DIR.mkdir(exist_ok=True)

# Gemini API setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_code_from_prompt(prompt: str) -> str:
    # Directive to ensure code-only output
    directive = (
        "You are a code generation assistant. "
        "When responding, output only the requested code snippet without any additional explanation or commentary."
        " The code should be in Python and should be complete and functional. "
        "If the code is too long, break it into smaller parts and return them one by one. "
    )
    full_prompt = directive + "\n" + prompt
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(full_prompt)
    text = response.text.strip()

    # Strip any Markdown code fences and return pure code
    fence_match = re.search(r"```(?:python)?\n([\s\S]*?)```", text)
    if fence_match:
        return fence_match.group(1).strip()
    # Otherwise, assume the entire response is code
    return text


def extract_prompt_from_event():
    event_path = os.getenv("GITHUB_EVENT_PATH")
    if not event_path or not os.path.exists(event_path):
        return "Write a Python function to sort a list."  # fallback for local testing

    with open(event_path, "r") as f:
        event_data = json.load(f)

    if "comment" in event_data:
        return event_data["comment"]["body"]
    elif "issue" in event_data and "body" in event_data["issue"]:
        return event_data["issue"]["body"]
    else:
        return "Write a Python function to sort a list."  # fallback


def main():
    prompt = "write a very detailed floppy bird game"
    #prompt = extract_prompt_from_event()
    generated_code = generate_code_from_prompt(prompt)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"{timestamp}_generated.py"
    with open(output_file, "w") as f:
        f.write(generated_code)

    print(f"✅ Code generated and saved to {output_file}")


if __name__ == "__main__":
    main()
