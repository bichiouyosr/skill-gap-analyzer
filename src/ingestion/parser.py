def parse_job(job: dict) -> dict:
    return {
        "job_id": str(job.get("id", "")),
        "title": job.get("intitule"),
        "company": job.get("entreprise", {}).get("nom"),
        "location": job.get("lieuTravail", {}).get("libelle"),
        "description": job.get("description"),
        "date_posted": job.get("dateCreation"),
        "source": "france_travail",
    }