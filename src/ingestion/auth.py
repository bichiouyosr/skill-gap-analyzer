import httpx
from core.config import FT_CLIENT_ID, FT_CLIENT_SECRET

TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"
SCOPE = "api_offresdemploiv2 o2dsoffre"


def get_token() -> str:
    response = httpx.post(
        TOKEN_URL,
        params={"realm": "/partenaire"},
        data={
            "grant_type": "client_credentials",
            "client_id": FT_CLIENT_ID,
            "client_secret": FT_CLIENT_SECRET,
            "scope": SCOPE,
        },
        timeout=10,
    )

    response.raise_for_status()
    return response.json()["access_token"]