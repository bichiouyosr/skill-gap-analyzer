import json


def save_jobs(jobs: list[dict], filename: str = "jobs_clean.json") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs, f, ensure_ascii=False, indent=2)