from ingestion.auth import get_token
from ingestion.fetcher import fetch_jobs
from ingestion.parser import parse_job
from ingestion.saver import save_jobs
from core.logger import get_logger

logger = get_logger(__name__)


def run():
    try:
        logger.info("Getting token...")
        token = get_token()

        logger.info("Fetching jobs...")
        raw_jobs = fetch_jobs(token)
        logger.info(f"{len(raw_jobs)} jobs fetched")

        logger.info("Parsing jobs...")
        parsed_jobs = [parse_job(job) for job in raw_jobs]

        logger.info("Saving jobs...")
        save_jobs(parsed_jobs)

        logger.info("Pipeline completed successfully")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)


if __name__ == "__main__":
    run()