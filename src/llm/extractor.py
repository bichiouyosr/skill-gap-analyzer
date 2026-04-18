import json

from core.logger import get_logger
from llm.client import call_llm
from llm.prompt import build_prompt

logger = get_logger(__name__)


def extract_skills_batch(jobs: list[dict], batch_size: int = 1) -> dict[str, list[str]]:
    results: dict[str, list[str]] = {}

    for i in range(0, len(jobs), batch_size):
        batch = jobs[i:i + batch_size]

        logger.info(
            "Processing LLM batch %s with %s jobs",
            (i // batch_size) + 1,
            len(batch),
        )

        prompt = build_prompt(batch)
        response = call_llm(prompt)

        try:
            parsed = json.loads(response)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse batch JSON: %s", exc)
            logger.info("Raw response: %s", response[:1000])
            continue

        # IMPORTANT: if model returns a single object, wrap it in a list
        if isinstance(parsed, dict):
            parsed = [parsed]

        if not isinstance(parsed, list):
            logger.warning("Unexpected JSON format (not a list)")
            logger.info("Raw response: %s", response[:1000])
            continue

        for item in parsed:
            if not isinstance(item, dict):
                continue

            job_id = str(item.get("job_id", "")).strip()
            skills = item.get("skills", [])

            if not job_id:
                continue

            if not isinstance(skills, list):
                skills = []

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

            results[job_id] = clean_skills
            logger.info("Extracted skills for job %s: %s", job_id, clean_skills)

    return results