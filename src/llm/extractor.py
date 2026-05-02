import json
import time

from core.logger import get_logger
from llm.client import call_llm
from llm.prompt import build_prompt

logger = get_logger(__name__)

MAX_RETRIES = 3


def _parse_llm_response(response: str) -> list[dict] | None:
    """Parse LLM JSON response. Returns None if invalid."""
    try:
        parsed = json.loads(response)
    except json.JSONDecodeError as exc:
        logger.warning("JSON decode error: %s", exc)
        return None

    if isinstance(parsed, dict):
        parsed = [parsed]

    if not isinstance(parsed, list):
        logger.warning("Unexpected format (not a list): %s", response[:200])
        return None

    return parsed


def _clean_skills(skills: object) -> list[str]:
    """Normalize skills returned by the LLM."""
    if isinstance(skills, list) and len(skills) == 1 and isinstance(skills[0], list):
        skills = skills[0]

    if not isinstance(skills, list):
        return []

    clean_skills: list[str] = []
    seen: set[str] = set()

    for skill in skills:
        skill_str = str(skill).strip()

        if not skill_str:
            continue

        key = skill_str.lower()

        if key in seen:
            continue

        seen.add(key)
        clean_skills.append(skill_str)

    return clean_skills


def _extract_single_job(job: dict) -> list[str]:
    """Call LLM for one job, retry up to MAX_RETRIES times."""
    prompt = build_prompt([job])
    expected_job_id = str(job["job_id"]).strip()

    for attempt in range(1, MAX_RETRIES + 1):
        logger.info("Job %s — attempt %s/%s", expected_job_id, attempt, MAX_RETRIES)

        response = call_llm(prompt)
        parsed = _parse_llm_response(response)

        if parsed is None:
            logger.warning("Invalid JSON on attempt %s, retrying...", attempt)
            time.sleep(1)
            continue

        logger.info("LLM raw parsed: %s", parsed)

        for item in parsed:
            if not isinstance(item, dict):
                continue

            if str(item.get("job_id", "")).strip() == expected_job_id:
                skills = item.get("skills", [])

            elif expected_job_id in item:
                skills = item[expected_job_id]

            else:
                continue

            clean_skills = _clean_skills(skills)

            logger.info("Job %s — skills: %s", expected_job_id, clean_skills)
            return clean_skills

        logger.warning("Job %s not found in LLM response, retrying...", expected_job_id)
        time.sleep(1)

    logger.error(
        "Job %s — failed after %s attempts, returning []",
        expected_job_id,
        MAX_RETRIES,
    )
    return []


def extract_skills_batch(jobs: list[dict]) -> dict[str, list[str]]:
    """Extract skills for all jobs, one by one with retry."""
    results: dict[str, list[str]] = {}

    for i, job in enumerate(jobs, 1):
        job_id = str(job["job_id"]).strip()

        logger.info("Processing job %s/%s — %s", i, len(jobs), job_id)

        results[job_id] = _extract_single_job(job)

    return results