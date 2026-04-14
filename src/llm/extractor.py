import json
import re
from llm.client import call_llm
from llm.prompt import build_prompt


def clean_json_response(text: str) -> str:
    match = re.search(r"\[.*\]", text, re.DOTALL)
    return match.group(0) if match else "[]"


def extract_skills(description: str) -> list[str]:
    prompt = build_prompt(description)

    response = call_llm(prompt)

    cleaned = clean_json_response(response)

    try:
        skills = json.loads(cleaned)
        return list(set(skills))  # remove duplicates
    except Exception:
        return []