import json
from llm.client import call_llm
from llm.prompt import build_prompt


def extract_skills(description: str) -> list[str]:
    prompt = build_prompt(description)

    response = call_llm(prompt)

    try:
        skills = json.loads(response)
        return skills
    except json.JSONDecodeError:
        return []