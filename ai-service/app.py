from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from services.groq_client import GroqClient
from services.security import sanitize_input, detect_prompt_injection

app = Flask(__name__)

# Rate limiter (30 req/min)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["30 per minute"]
)

client = GroqClient()


@app.route("/ai/generate", methods=["POST"])
@limiter.limit("30 per minute")
def generate():
    data = request.get_json()

    if not data or "prompt" not in data:
        return jsonify({"error": "Prompt is required"}), 400

    prompt = sanitize_input(data["prompt"])

    if not prompt or not prompt.strip():
        return jsonify({

            "error": "Prompt cannot be empty"

        }), 400

    # Detect injection
    if detect_prompt_injection(prompt):
        return jsonify({
            "error": "Potential prompt injection detected"
        }), 400

    # Call AI
    result = client.generate_response(prompt)

    if not result["success"]:
        return jsonify({"error": result["error"]}), 500

    return jsonify({
        "response": result["response"],
        "model": result.get("model", "unknown")
    })


@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(port=5000, debug=True)