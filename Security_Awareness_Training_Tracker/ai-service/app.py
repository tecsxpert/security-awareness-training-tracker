from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os


from services.groq_client import call_groq

from services.analysis_service import analyze_security_issue

from datetime import datetime
import json

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
            "explanation": "Fallback response",
            "generated_at": datetime.utcnow().isoformat()
        })
    
    

    import json
    try:
        parsed = json.loads(ai_response)
        parsed["generated_at"] = datetime.utcnow().isoformat()
        return jsonify(parsed)
    except:
        return jsonify({
            "raw": ai_response
        })

    # ✅ Day 4: Recommendation endpoint (ADDED ONLY THIS)
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json

    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400

    user_input = data["text"]

    # load prompt from file
    with open("prompts/recommend_prompt.txt", "r") as f:
        template = f.read()

    final_prompt = template.replace("{input}", user_input)

    ai_response = call_groq(final_prompt)

    if not ai_response:
        return jsonify([
            {
                "action_type": "N/A",
                "description": "AI unavailable",
                "priority": "Low"
            }
        ])

    import json
    try:
        parsed = json.loads(ai_response)
        return jsonify(parsed)
    except:
        return jsonify({
            "raw": ai_response
        }) 
    
    # ✅ Day 5: Service-based AI integration
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    if not data or "text" not in data:
        return jsonify({"error": "Invalid input"}), 400

    user_input = data["text"]

    result = analyze_security_issue(user_input)

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)