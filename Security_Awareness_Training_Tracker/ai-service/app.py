from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

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

# ✅ Day 2: Test prompt route (ADDED ONLY THIS)
@app.route("/test-prompt", methods=["POST"])
def test_prompt():
    data = request.json
    user_input = data.get("text")

    return jsonify({
        "input": user_input,
        "message": "Prompt ready (AI integration next step)"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)