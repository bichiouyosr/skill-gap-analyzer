import json
import re

from core.logger import get_logger
from llm.client import call_llm
from llm.prompt import build_batch_prompt

logger = get_logger(__name__)


def clean_json_response(text: str) -> str:
    array_match = re.search(r"\[\s*.*\s*\]", text, re.DOTALL)
    object_match = re.search(r"\{\s*.*\s*\}", text, re.DOTALL)

    if array_match:
        return array_match.group(0)

    if object_match:
        return object_match.group(0)

    return "[]"


def chunk_jobs(jobs: list[dict], batch_size: int) -> list[list[dict]]:
    return [jobs[i:i + batch_size] for i in range(0, len(jobs), batch_size)]


def normalize_skill_list(raw_skills: object) -> list[str]:
    if not isinstance(raw_skills, list):
        return []

    normalized: list[str] = []
    seen: set[str] = set()

    for skill in raw_skills:
        skill_str = str(skill).strip()
        if not skill_str:
            continue

        skill_key = skill_str.lower()
        if skill_key not in seen:
            normalized.append(skill_str)
            seen.add(skill_key)

    return normalized


def parse_single_llm_output(parsed: object) -> list[str]:
    if isinstance(parsed, list):
        return normalize_skill_list(parsed)

    if isinstance(parsed, dict) and "technical_skills" in parsed:
        return normalize_skill_list(parsed["technical_skills"])

    return []


def extract_skills(description: str | None) -> list[str]:
    if not description:
        return []

    prompt = f"""
Extrait uniquement les compétences techniques explicites présentes dans la description suivante.

Retourne uniquement un JSON valide sous forme de liste de chaînes.

Règles :
- Pas d’explication
- Pas de texte en plus
- Pas de markdown
- Pas d’objet JSON avec plusieurs champs inutiles
- Ne retourne que les compétences techniques explicites
- Ne pas inventer de compétences
- Ne pas inclure les intitulés de poste comme "Data Engineer"
- Réponse attendue : ["Python", "SQL", "Docker"]

Description :
{description[:1500]}
"""

    response = call_llm(prompt)
    cleaned = clean_json_response(response)

    try:
        parsed = json.loads(cleaned)
        return parse_single_llm_output(parsed)
    except json.JSONDecodeError:
        logger.error("Failed to parse single-job LLM response")
        return []


def extract_skills_batch(jobs: list[dict], batch_size: int = 2) -> dict[str, list[str]]:
    results: dict[str, list[str]] = {}

    for batch_index, batch in enumerate(chunk_jobs(jobs, batch_size=batch_size), start=1):
        logger.info("Processing LLM batch %s with %s jobs", batch_index, len(batch))

        prompt = build_batch_prompt(batch)
        response = call_llm(prompt)
        cleaned = clean_json_response(response)

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse batch %s JSON: %s", batch_index, exc)
            continue

        if not isinstance(parsed, list):
            logger.warning("Batch %s did not return a JSON list", batch_index)
            continue

        for item in parsed:
            if not isinstance(item, dict):
                continue

            job_id = str(item.get("job_id", "")).strip()
            if not job_id:
                continue

            if "skills" in item:
                raw_skills = item["skills"]
            elif "technical_skills" in item:
                raw_skills = item["technical_skills"]
            else:
                raw_skills = []

            results[job_id] = normalize_skill_list(raw_skills)

    return results