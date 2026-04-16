from ingestion.auth import get_token
from ingestion.fetcher import fetch_jobs
from ingestion.parser import parse_job
from ingestion.saver import save_jobs
from llm.extractor import extract_skills_batch
from core.logger import get_logger

logger = get_logger(__name__)


def run() -> None:
    try:
        logger.info("Getting token...")
        token = get_token()

        logger.info("Fetching jobs...")
        raw_jobs = fetch_jobs(token)
        logger.info("%s jobs fetched", len(raw_jobs))

        logger.info("Parsing jobs...")
        parsed_jobs = [parse_job(job) for job in raw_jobs]

        logger.info("Extracting skills with batch LLM processing...")
        skills_by_job_id = extract_skills_batch(parsed_jobs, batch_size=2)

        logger.info("Merging extracted skills...")
        enriched_jobs = []
        for job in parsed_jobs:
            job_id = job["job_id"]
            enriched_job = {
                **job,
                "skills": skills_by_job_id.get(job_id, []),
            }
            enriched_jobs.append(enriched_job)

        logger.info("Saving jobs...")
        save_jobs(enriched_jobs)

        logger.info("Pipeline completed successfully")

    except Exception as exc:
        logger.error("Pipeline failed: %s", exc, exc_info=True)


if __name__ == "__main__":
    run()