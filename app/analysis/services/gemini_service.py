import requests

from app.core.config import GEMINI_API_KEY


GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.0-flash:generateContent"
)


def call_gemini(prompt: str):

    headers = {
        "Content-Type": "application/json"
    }

    params = {
        "key": GEMINI_API_KEY
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(
        GEMINI_API_URL,
        headers=headers,
        params=params,
        json=payload,
        timeout=60
    )

    if response.status_code != 200:
        return {
            "success": False,
            "error": response.text
        }

    data = response.json()

    try:
        text = (
            data["candidates"][0]
            ["content"]["parts"][0]
            ["text"]
        )

        return {
            "success": True,
            "data": text
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }