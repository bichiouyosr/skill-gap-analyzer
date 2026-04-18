import json


def build_prompt(jobs: list[dict]) -> str:
    payload = [
        {
            "job_id": str(job["job_id"]).strip(),
            "description": (job.get("description") or "")[:2000],
        }
        for job in jobs
    ]

    return f"""
You are a strict information extraction system.

Extract ONLY technical skills from each job description.

STRICT RULES:
- Return ONLY valid JSON
- No explanation
- No markdown
- No comments
- Output must be a JSON array
- Return exactly one object per input job
- Keep the exact same job_id values
- Each item must have:
  - "job_id": string
  - "skills": array of strings
- "skills" must always be a real JSON array, never a string
- Only technical skills: programming languages, frameworks, libraries, cloud, databases, DevOps, data tools
- No soft skills
- No duplicates inside each skills list
- If no technical skill is found, return an empty list for that job
- Never omit a job

Jobs:
{json.dumps(payload, ensure_ascii=False, indent=2)}
"""