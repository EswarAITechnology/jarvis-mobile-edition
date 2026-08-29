import os
import requests


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def ask_ai(message, memories=None):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return "J.A.R.V.I.S: OpenRouter API key is not configured."

    memories = memories or []

    recent_memories = memories[-10:]

    memory_text = ""

    if recent_memories:
        memory_text = "\n\nPrevious conversation memory:\n"

        for item in recent_memories:
            memory_text += (
                f"User: {item.get('user', '')}\n"
                f"J.A.R.V.I.S: {item.get('assistant', '')}\n"
            )

    system_prompt = """
You are J.A.R.V.I.S., a helpful AI assistant.

Your communication style is:
- Clear
- Intelligent
- Concise
- Professional
- Helpful

Address the user as "Boss" when appropriate.

Do not claim that you performed an action if you did not actually perform it.
"""

    payload = {
        "model": "openai/gpt-oss-20b:free",
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": memory_text + "\n\nCurrent request:\n" + message
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

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]

    except requests.RequestException as error:
        return f"J.A.R.V.I.S: Connection error: {error}"

    except (KeyError, IndexError, TypeError):
        return "J.A.R.V.I.S: I received an unexpected response from the AI service."