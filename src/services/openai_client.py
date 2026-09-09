import os

import requests
from dotenv import load_dotenv

from src.config.settings import MODEL


def send_prompt(prompt: str, schema: dict) -> str:
    load_dotenv()
    api_key = os.environ["OPENAI_KEY"]

    response = requests.post(
        url="https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"bearer {api_key}"},
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "response_format": schema,
        },
    )
    first_layer = response.json()
    return first_layer["choices"][0]["message"]["content"]
