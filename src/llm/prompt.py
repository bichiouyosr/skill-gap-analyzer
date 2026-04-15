import json


def build_batch_prompt(jobs: list[dict]) -> str:
    payload = [
        {
            "job_id": job["job_id"],
            "description": (job.get("description") or "")[:1500],
        }
        for job in jobs
    ]

    jobs_json = json.dumps(payload, ensure_ascii=False, indent=2)

    return f"""
You are a strict information extraction system.

Extract ONLY technical skills from each job description.

STRICT RULES:
- Return ONLY valid JSON
- No explanation
- No markdown
- No comments
- Keep the same job_id values
- Output must be a JSON array
- Each item must have:
  - "job_id": string
  - "skills": array of strings
- Only technical skills: programming languages, frameworks, libraries, cloud, databases, DevOps, data tools
- No soft skills
- No duplicates inside each skills list
- If unsure, return an empty list for that job

Expected output format:
[
  {{"job_id": "123", "skills": ["Python", "SQL"]}},
  {{"job_id": "456", "skills": ["AWS", "Spark"]}}
]

Jobs:
{jobs_json}
"""