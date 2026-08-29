import json
import os

MEMORY_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "memory",
    "memory.json"
)


def get_memories():
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_memory(user_message, ai_response):
    memories = get_memories()

    memories.append({
        "user": user_message,
        "assistant": ai_response
    })

    # Keep the most recent 100 conversations
    memories = memories[-100:]

    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memories, file, indent=2, ensure_ascii=False)