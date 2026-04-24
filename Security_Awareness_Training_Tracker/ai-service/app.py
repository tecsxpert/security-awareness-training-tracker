from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os


from services.groq_client import call_groq

# load environment variables
load_dotenv()

app = Flask(__name__)

# basic route
@app.route("/")
def home():
    return jsonify({
        "message": "AI Service Running "
    })

# health check (important for project)
@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "service": "AI Service",
        "port": 5000
    })


@app.route("/test-prompt", methods=["POST"])
def test_prompt():
    data = request.json
    user_input = data.get("text")

    return jsonify({
        "input": user_input,
        "message": "Prompt ready (AI integration next step)"
    })


@app.route("/describe", methods=["POST"])
def describe():
    data = request.json

    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400

    user_input = data["text"]

    # load prompt from file
    with open("prompts/describe_prompt.txt", "r") as f:
        template = f.read()

    final_prompt = template.replace("{input}", user_input)

    ai_response = call_groq(final_prompt)

    if not ai_response:
        return jsonify({
            "description": "AI unavailable",
            "risk_level": "Unknown",
            "explanation": "Fallback response"
        })

 
    import json
    try:
        parsed = json.loads(ai_response)
        return jsonify(parsed)
    except:
        return jsonify({
            "raw": ai_response
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)