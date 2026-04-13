from llm.extractor import extract_skills


def parse_job(job: dict) -> dict:
    description = job.get("description")

    return {
        "job_id": job.get("id"),
        "title": job.get("intitule"),
        "company": job.get("entreprise", {}).get("nom"),
        "location": job.get("lieuTravail", {}).get("libelle"),
        "description": description,
        "skills": extract_skills(description),
        "date_posted": job.get("dateCreation"),
        "source": "france_travail",
    }