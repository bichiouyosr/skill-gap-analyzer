import httpx

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "deepseek-coder"


def call_llm(prompt: str) -> str:
    with httpx.Client(timeout=240.0) as client:
        response = client.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0,
                },
            },

            
        )
        response.raise_for_status()
        return response.json()["message"]["content"].strip()