import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"


def call_llm(prompt: str) -> str:
    response = httpx.post(
        OLLAMA_URL,
        json={
            "model": "deepseek-coder",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            }
        },
        timeout=60,
    )

    response.raise_for_status()

    return response.json()["response"].strip()