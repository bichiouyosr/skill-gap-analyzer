from ingestion.auth import get_token
from ingestion.fetcher import fetch_jobs
from ingestion.parser import parse_job
from ingestion.saver import save_jobs


def run():
    print("Getting token...")
    token = get_token()

    print("Fetching jobs...")
    raw_jobs = fetch_jobs(token)

    print(f"{len(raw_jobs)} jobs fetched")

    parsed_jobs = [parse_job(job) for job in raw_jobs]

    print("Saving jobs...")
    save_jobs(parsed_jobs)

    print("Done!")


if __name__ == "__main__":
    run()