from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from services.ai import ask_ai
from services.memory import save_memory, get_memories
from services.web import check_website

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "name": "J.A.R.V.I.S Backend",
        "status": "online"
    })


@app.route("/api/status")
def status():
    return jsonify({
        "ai_core": "online",
        "network": "online",
        "voice": "ready",
        "memory": "online",
        "web_engine": "online"
    })


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "Message is required"
        }), 400

    memories = get_memories()

    response = ask_ai(message, memories)

    save_memory(message, response)

    return jsonify({
        "response": response
    })


@app.route("/api/memory", methods=["GET"])
def memory():
    return jsonify({
        "memories": get_memories()
    })


@app.route("/api/web-check", methods=["POST"])
def web_check():
    data = request.get_json(silent=True) or {}

    url = data.get("url", "").strip()

    if not url:
        return jsonify({
            "error": "URL is required"
        }), 400

    result = check_website(url)

    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)