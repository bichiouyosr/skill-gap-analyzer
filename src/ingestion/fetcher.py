import httpx

BASE_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2"


def fetch_jobs(token: str, keyword: str = "data engineer") -> list[dict]:
    headers = {"Authorization": f"Bearer {token}"}

    params = {
        "motsCles": keyword,
        "range": "0-49",
    }

    response = httpx.get(
        f"{BASE_URL}/offres/search",
        headers=headers,
        params=params,
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()
    return data.get("resultats", [])