import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "openrouter/free")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

app = Flask(__name__)

PERSONA_PATH = os.path.join(os.path.dirname(__file__), "persona.txt")


def load_persona():
    try:
        with open(PERSONA_PATH, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Sen yardımsever bir asistansın. Her zaman Türkçe cevap ver."


def ask_model(messages, model=MODEL):
    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={"model": model, "messages": messages},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = [{"role": "system", "content": load_persona()}] + data.get("messages", [])
    try:
        answer = ask_model(messages)
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)