import os
import requests

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def ask_ai(message, memories=None):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "J.A.R.V.I.S: OpenRouter API key is not configured."

    memories = memories or []

    memory_text = ""

    for item in memories[-10:]:
        memory_text += (
            f"User: {item.get('user', '')}\n"
            f"J.A.R.V.I.S: {item.get('assistant', '')}\n"
        )

    payload = {
        "model":"model": "openrouter/free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are J.A.R.V.I.S., a helpful AI assistant. "
                    "Be clear, intelligent, concise and professional. "
                    "Address the user as Boss when appropriate."
                )
            },
            {
                "role": "user",
                "content": (
                    memory_text +
                    "\nCurrent request:\n" +
                    message
                )
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://eswaraitechnology.github.io",
        "X-Title": "J.A.R.V.I.S Mobile Edition"
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if not response.ok:
            return (
                f"J.A.R.V.I.S: OpenRouter returned "
                f"{response.status_code}: {response.text}"
            )

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except requests.RequestException as error:
        return f"J.A.R.V.I.S: Network error: {error}"

    except (KeyError, IndexError, TypeError):
        return "J.A.R.V.I.S: Unexpected response from OpenRouter."