from dotenv import load_dotenv
load_dotenv()

import os
import datetime
import json
import google.generativeai as genai
from pathlib import Path

OUTPUT_DIR = Path("generated_code")
OUTPUT_DIR.mkdir(exist_ok=True)

# Gemini API setup
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_code_from_prompt(prompt: str) -> str:
    # Prepend a directive so the model returns only code without explanations
    directive = (
        "You are a code generation assistant. "  
        "When responding, only output the requested code snippet without any additional explanation. "
    )
    full_prompt = directive + prompt
    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(full_prompt)
    return response.text.strip()

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
    prompt="Write a program to sort a hashmap"
    #prompt = extract_prompt_from_event()
    generated_code = generate_code_from_prompt(prompt)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"{timestamp}_generated.py"
    with open(output_file, "w") as f:
        f.write(generated_code)

    print(f"✅ Code generated and saved to {output_file}")

if __name__ == "__main__":
    main()
