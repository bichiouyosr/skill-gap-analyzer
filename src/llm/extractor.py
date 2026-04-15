import json
import re
from llm.client import call_llm
from llm.prompt import build_batch_prompt


def clean_json_response(text: str) -> str:
    match = re.search(r"\[.*\]", text, re.DOTALL)
    return match.group(0) if match else "[]"


def chunk_jobs(jobs: list[dict], batch_size: int) -> list[list[dict]]:
    return [jobs[i:i + batch_size] for i in range(0, len(jobs), batch_size)]


def extract_skills_batch(jobs: list[dict], batch_size: int = 10) -> dict[str, list[str]]:
    results: dict[str, list[str]] = {}

    for batch in chunk_jobs(jobs, batch_size=batch_size):
        prompt = build_batch_prompt(batch)
        response = call_llm(prompt)
        cleaned = clean_json_response(response)

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            parsed = []

        for item in parsed:
            job_id = str(item.get("job_id", "")).strip()
            skills = item.get("skills", [])

            if not job_id:
                continue

            if not isinstance(skills, list):
                skills = []

            normalized_skills = []
            seen = set()

            for skill in skills:
                skill_str = str(skill).strip()
                if skill_str and skill_str.lower() not in seen:
                    normalized_skills.append(skill_str)
                    seen.add(skill_str.lower())

            results[job_id] = normalized_skills

    return results